
import logging, os, shutil, time, yaml, warnings, json
import pandas as pd
import bpyth as bpy

from munch import DefaultMunch

from ludwig.api       import LudwigModel
from ludwig.visualize import learning_curves
from ludwig.visualize import compare_performance
from ludwig.visualize import confusion_matrix
from ludwig.visualize import roc_curves_from_test_statistics
from torchinfo        import summary

from bludwig.helper import *

# logging.DEBUG   == 10
# logging.INFO    == 20
# logging.WARNING == 30


# LudwigJob wird einmal instanziiert
#
class LudwigJob():

    
#####################################################################################################
# Basics
#     
    
    def __init__( self, configs=[], experiment_name=None, verbose=False ):  
        '''
        LudwigJob wird einmal instanziiert, z.B. so:
        ludwig_job = bludwig.LudwigJob( configs=configs, verbose=True) 
        * configs: list of Ludwig-configs as YAML-String, Path to yaml-file or yaml-object
            
        '''
        # Parameter         
        if experiment_name is None:
            experiment_name = 'ex'
        self.experiment_name = experiment_name
        self.verbose = verbose        

        # configs ggf. in YAML wandeln
        self.configs = []
        for config in configs:
            if isinstance(config, str):
                if config.count('\n') > 2: 
                    self.configs += [yaml.safe_load(config)]
                else:
                    self.configs += [config]   

        try:
            import google.colab
            self.in_colab = True 
        except:
            self.in_colab = False     

        # Tensorflow warnings unterdrücken
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    

        # gpu_info
        if verbose:
            gpu_info()

        # aktuelles model
        self.model = None
        self.output_feature_name = ''

        # job
        self.train_jobs = []
        self.model_names = []
        self.model_paths = []

        # train_log
        self.train_log_raw = pd.DataFrame()

        # results
        self.train_stats      = []
        self.test_stats       = []
        self.output_dirs      = []       

        if len(configs) > 0:
            print()
            print('{} configs loaded'.format(len(configs)))



    def __str__(self):
        result = f'''LudwigJob object
        experiment_name:     {self.experiment_name}
        output_feature_name: {self.output_feature_name}
        train_jobs:          {self.train_jobs}
        model_names:         {self.model_names}
        model_paths:         {self.model_paths}        
        output_dirs:         {self.output_dirs}
        '''
        return result


    
    def load_from_results(self):    
        '''
        Loads data from results directory
        '''
        results_dir = os.listdir('results')
        self.output_dirs = [ 'results/' + d                for d in results_dir ]
        self.train_jobs  = [ int(d.split('_')[1])          for d in results_dir ]
        self.model_names = [ 'model_' + str(j)             for j in self.train_jobs ]    
        self.model_paths = [d + '/model'                   for d in self.output_dirs]
        
        train_stats = [ d + '/training_statistics.json'    for d in self.output_dirs ]
        train_stats = [ json.load( open(p) )               for p in train_stats]
        self.train_stats = [ DefaultMunch.fromDict(d)      for d in train_stats]

        test_stats = [ d + '/test_statistics.json'         for d in self.output_dirs ]
        test_stats = [ json.load( open(p) )                for p in test_stats]
        self.test_stats = [ DefaultMunch.fromDict(d)       for d in test_stats]

        # output_feature_name
        a = list(self.test_stats[0].keys())
        a.remove('combined')
        self.output_feature_name = a[0]   
        # nochmal gegenprüfen
        b = list(self.train_stats[0]['test'].keys())
        b.remove('combined')
        assert self.output_feature_name in b


    
    def load_model(self, model_no):
        '''
        Loads a model identified by model number
        '''
        self.model = LudwigModel.load( self.model_paths[model_no] )


        
#####################################################################################################
# print_models
#

    def print_model(self, model_no=0):
        '''
        Uses torchinfo.summary to print a model
        '''
        self.load_model(model_no)
        _ = self.model.model.to('cpu')
        print( '### {} ###'.format(self.model_names[model_no]))
        print( summary(self.model.model, 
                       input_data=[self.model.model.get_model_inputs()], 
                       depth=20, 
                       col_names=['input_size','output_size','num_params','trainable'] 
                      ) )
        print('\n'*3)   


    
    def print_models(self):        
        for model_no in self.train_jobs:
            self.print_model(model_no)

            
        
#####################################################################################################
# experiment
#
    
    def experiment(self, train_jobs, dataset):
        '''
        train and evaluate a list of Ludwig models
        '''
        self.train_jobs = train_jobs
        self.model_names = ['model_' + str(c) for c in train_jobs]
        
        
        for config_no in train_jobs:
            experiment_subname = self.experiment_name + '_' + str(config_no) 
            experiment_path = 'results/' + experiment_subname + '_run'  
            print()
            print( 'Training config_no {} >> {}'.format( config_no, experiment_path) )   
            
            # Zielverzeichnis rekursiv löschen
            try:
                shutil.rmtree(experiment_path)
            except:
                pass

            logging_level = 20 if self.verbose else 30

            # lade model
            self.model               = LudwigModel(config=self.configs[config_no], logging_level=logging_level)   
            self.output_feature_name = self.model.config['output_features'][0]['name']
            self.output_feature_type = self.model.config['output_features'][0]['type']

            # trainiere
            start_time = time.time()     
            test_stat, train_stat, _, output_dir = self.model.experiment( dataset=dataset, experiment_name=experiment_subname)
            self.test_stats  += [test_stat]
            self.train_stats += [train_stat]
            self.output_dirs += [output_dir]

            # logge config
            train_secs        = round( time.time() - start_time )
            train_time        = bpy.human_readable_seconds( train_secs )
            epochs            = len(train_stat.test['combined']['loss']) 
            validation_metric = self.model.config['trainer']['validation_metric']
            log = pak.dataframe([
                [ config_no, 'train_secs',          train_secs        ],
                [ config_no, 'train_time',          train_time        ],
                [ config_no, 'epochs',              epochs            ],
                [ config_no, 'time/epoch',          bpy.human_readable_seconds( train_secs/epochs ) ],     
                [ config_no, 'validation_metric',   validation_metric ],     
                [ config_no, 'experiment_path',     experiment_path   ], 
                [ config_no, 'output_feature_name', self.output_feature_name   ],    
                [ config_no, 'output_feature_type', self.output_feature_type   ],                    
                
            ])
            log.columns = ['config_no','name','value']
            self.train_log_raw = pak.add_rows( self.train_log_raw, log ) 
            print('train_time:',train_time) 
            print()

        # logge Gesamtprozess
        self.train_log_raw = pak.add_rows( self.train_log_raw, entwirre_test_stat(self.test_stats))            



        
#####################################################################################################
# train_log
#

    def train_log(self):
        ''' returns small log'''
        if self.train_log_raw.shape[0] > 0:
            result = prepare_train_log(self.train_log_raw, size='small')
            return result
        else:
            zeilen = ['roc_auc','accuracy','recall','specificity','precision','loss','epochs','time/epoch','train_time']
            result = pd.DataFrame(zeilen)
            result.columns = ['name']
            return result

    
    
    def train_log_big(self):
        ''' returns bigger log'''
        return prepare_train_log(self.train_log_raw, size='big')        


        
    def train_log_to_csv(self):
        '''
        Saves train_log_big to csv file
        Shows train_log (small version)
        '''
        t = self.train_log_big()
        if self.in_colab:
            t.to_csv('train_log_colab.csv', index=False)
        else:
            if torch.cuda.is_available():
                t.to_csv('train_log_GPU.csv', index=False)    
            else:
                t.to_csv('train_log_CPU.csv', index=False)
                
        return self.train_log()


        
        
#####################################################################################################
# Visualisierungen
#

    def compare_performance(self, output_feature_name=None):

        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name
        
        # test_stats_small (verhindert Fehler)
        test_stats_small = []
        keys_to_keep = list(self.train_log().name)
        for stat in self.test_stats:
            r = {key: value  for key, value in stat[output_feature_name].items()  if key in keys_to_keep}
            r = { output_feature_name: r }    
            test_stats_small += [r]        

        # ausgeben
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            compare_performance( test_stats_small, model_names=self.model_names, output_feature_name=output_feature_name )


    
    def learning_curves(self, output_feature_name=None):
        
        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name    
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            learning_curves( self.train_stats, model_names=self.model_names, output_feature_name=output_feature_name)     


    
    def confusion_matrix(self, output_feature_name=None, normalize=True, top_n_classes=[10]):

        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name  

        #load_model
        if self.model is None:
            try:
                self.load_model(0)
            except:
                print('No model loaded')
            
        # confusion_matrix
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            confusion_matrix( self.test_stats, 
                              self.model.training_set_metadata, 
                              output_feature_name=output_feature_name, 
                              top_n_classes=top_n_classes, 
                              model_names=self.model_names, 
                              normalize=True )


    
    def roc_curves(self, output_feature_name=None):
        '''
Die ROC-Kurve (Receiver Operating Characteristic) ist ein grafisches Maß zur Bewertung der Leistung eines Klassifikators, wie z.B. eines neuronalen Netzwerks, insbesondere bei binären Klassifikationsproblemen. Die ROC-Kurve stellt die True Positive Rate (TPR) gegen die False Positive Rate (FPR) dar.

Der Verlauf der ROC-Kurve wird durch den Schwellenwert bestimmt, der festlegt, ab welchem Ausgabewert des neuronalen Netzwerks eine Instanz als positiv oder negativ klassifiziert wird. Die Schwellenwertänderung ermöglicht es, die TPR und FPR zu variieren und somit die Leistung des Klassifikators zu analysieren.

Zu Beginn, wenn der Schwellenwert sehr niedrig ist, werden viele Instanzen als positiv klassifiziert, was zu einer hohen FPR und TPR führt. Mit zunehmendem Schwellenwert werden einige wahre positive Instanzen fälschlicherweise als negativ klassifiziert, was zu einem Anstieg der FPR und einem möglichen Abfall der TPR führen kann. Wenn der Schwellenwert sehr hoch ist, werden die meisten Instanzen als negativ klassifiziert, was zu einer niedrigen FPR und TPR führt.

Idealerweise strebt man bei der ROC-Analyse eine Kurve an, die möglichst nahe am linken oberen Rand des Diagramms liegt. Ein Punkt in diesem Bereich repräsentiert einen hohen TPR bei einer niedrigen FPR und deutet auf eine gute Leistung des Klassifikators hin. Ein zufälliger Klassifikator würde eine diagonal verlaufende Linie (45-Grad-Linie) erzeugen, da seine FPR und TPR gleich wären.

Die Leistung des Klassifikators kann anhand des Bereichs unter der ROC-Kurve (AUC, Area Under the Curve) quantifiziert werden. Ein AUC-Wert von 1.0 bedeutet perfekte Vorhersage, während ein Wert von 0.5 einem zufälligen Klassifikator entspricht.

Daher ermöglicht die ROC-Kurve die Beurteilung und Vergleich der Leistung eines neuronalen Netzwerks für verschiedene Schwellenwerte und unterstützt bei der Auswahl des optimalen Schwellenwerts, abhängig von den Anforderungen des Anwendungsfalls.        
        '''
        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name  
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            roc_curves_from_test_statistics(self.test_stats, output_feature_name=output_feature_name)   
        
        



