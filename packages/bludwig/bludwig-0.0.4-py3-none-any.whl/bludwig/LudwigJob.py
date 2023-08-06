
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
        self.model_no = None
        self.cuda = None
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
        model_no:            {self.model_no}   
        cuda:                {self.cuda}             
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


    
    def load_model(self, model_no, cuda=True):
        '''
        Loads a model identified by model number.
        * cuda: Use cuda, if available
        '''
        if model_no == self.model_no and cuda == self.cuda:
            return
            
        self.model = LudwigModel.load( self.model_paths[model_no] )
        if cuda and torch.cuda.is_available():
            self.model.model.to('cuda')
            self.cuda = True
        else:
            self.model.model.to('cpu')   
            self.cuda = False
        self.model_no = model_no




        
#####################################################################################################
# print_models
#

    def print_model(self, model_no=None):
        '''
        Uses torchinfo.summary to print a model
        '''
        if model_no is None:
            model_no = self.model_no
        self.load_model(model_no, cuda=False)
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
            self.model_no            = config_no
            self.cuda                = torch.cuda.is_available()
            self.output_feature_name = self.model.config['output_features'][0]['name']
            self.output_feature_type = self.model.config['output_features'][0]['type']

            # trainiere
            start_time = time.time()     
            test_stat, train_stat, _, output_dir = self.model.experiment( dataset=dataset, experiment_name=experiment_subname)
            self.test_stats  += [test_stat]
            self.train_stats += [train_stat]
            self.output_dirs += [output_dir]
            self.model_paths += [output_dir + '/model']

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
# predict
#

    def predict(self, data, merge=True):
        pred, _ = self.model.predict(data)
        if not merge:
            return pred
            
        pred.index = data.index
        result = pd.merge( data, pred, left_index=True, right_index=True)
        result = pak.move_cols( result, [self.output_feature_name, self.output_feature_name + '_predictions'])
        result.rename(columns=lambda x: x.replace('_predictions', '_pred').replace('probabilities', 'prob').replace('probability', 'prob'), inplace=True)
        return result        


        
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
    
        '''
        # Kein bestimmer output_feature_name angefragt >> Default
        if output_feature_name is None:
            output_feature_name = self.output_feature_name  
            
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                roc_curves_from_test_statistics(self.test_stats, output_feature_name=output_feature_name)   
            except KeyError:
                print('No roc_curve found')
                pass
            except TypeError:
                print('No roc_curve found')
                pass                
            except:
                raise  # Löst die Ausnahme erneut aus        
                



