
import torch  #, os,warnings
import bpyth as bpy
import pandas as pd
import pandasklar as pak

#from ludwig.api       import LudwigModel
#from ludwig.visualize import learning_curves
#from ludwig.visualize import compare_performance
#from ludwig.visualize import confusion_matrix
    
#############################################################################################################
###
### Helper for Ludwig
###
#############################################################################################################    


def gpu_info():
    # GPU und CUDA
    if torch.cuda.is_available():
        print('CUDA is available on ' + torch.cuda.get_device_name(torch.cuda.current_device()))
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch.cuda.empty_cache() # Cache leeren
        print('max_memory_allocated: {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_allocated(device=device)) )  )
        print('max_memory_reserved:  {}'.format(bpy.human_readable_bytes(torch.cuda.max_memory_reserved( device=device)) )  )  

    else:
        print('no CUDA!')    



def entwirre_test_stat(test_stats):
    result = []
    for config_no, test_stat in enumerate(test_stats):
        print(config_no)
        for output_feature_name, stat in test_stat.items():
            if output_feature_name == 'combined':
                continue
            for key, value in stat.items():
                if isinstance(value, (int, float)):
                    result += [[config_no, key, bpy.human_readable_number(value,3) ]]    
                    
    result = pak.dataframe(result)
    result.columns = ['config_no','name','value']
    return result




def prepare_train_log(train_log_raw, size='small'):

    result = pd.pivot_table( train_log_raw, 
                              index='name',
                              columns='config_no',
                              values='value', 
                              aggfunc='first')
    result = pak.drop_multiindex(result).reset_index() 
    
    # Namen korrigieren
    mask = result.name.str.startswith('average')
    result.loc[mask,'name'] = result[mask].name.str.replace('average_','') + '_avg'   

    # validation_metric ganz nach vorne
    mask = result.name == 'validation_metric'
    zeilen_ganzvorne = list(set(result[mask].iloc[0]))    
    #print(zeilen_ganzvorne)


    # Zeilen sortieren
    if size == 'small':
        zeilen_vorne =  ['accuracy','recall','specificity','precision','roc_auc','loss',]
        zeilen_hinten = ['epochs','time/epoch','train_time',]    
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )
        result = pak.move_cols( result, zeilen_ganzvorne )        
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()

        # Zeilen löschen
        zeilen_verboten = ['validation_metric']
        zeilen_erlaubt = [z for z in (zeilen_ganzvorne + zeilen_vorne + zeilen_hinten) if not z in zeilen_verboten ]
        mask = result.name.isin( zeilen_erlaubt )
        result = result[mask]
        
    else: # size == 'big'
        result = result.sort_values('name')
        zeilen_vorne =  ['validation_metric',]
        zeilen_hinten = ['experiment_path','output_feature_type','output_feature_name','epochs','train_secs','time/epoch','train_time',]     
        result = result.set_index('name').T
        result = pak.move_cols( result, zeilen_vorne )         
        result = pak.move_cols( result, zeilen_hinten, -1 )    
        result = result.T.reset_index()        

    result = pak.reset_index(result)
    result.columns = [c if isinstance(c,str) else 'model_' + str(c) for c in result.columns ]
    return result

















