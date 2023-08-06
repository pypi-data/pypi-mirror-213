



import warnings
import argparse
import csv
import faulthandler
import sys
import timeit
from collections import namedtuple
print('loaded standard packages')

import numpy as np

import pandas as pd

import helperprocess
print('loaded helper')
from metaheuristics import (differential_evolution_non_mp,
                            harmony_search_non_mp, 
                            simulated_annealing_non_mp)
print('loaded algorithnms')
from solution import ObjectiveFunction
print('loaded solution')
warnings.simplefilter("ignore")
# Add tkdesigner to path
faulthandler.enable()

def convert_df_columns_to_binary_and_wide(df):
    columns = list(df.columns)
      
    df = pd.get_dummies(df, columns=columns, drop_first=True)
    return df

def main(args):
   
    AnalystSpecs = None
    IS_MULTI = 0;
    MAX_ITER = 2000;
    NUM_INTL_SLNS = 25;
    SEED = 25;
    OBJ_1 = 'bic';
    OBJ_2 = 'MAE';
    TEST_SET_SIZE = 0;
    MAX_TIME = 2600;
    POPULATION = 25;
    CR_R = 0.2

    initial_complexity = 6 #representes hetrogeneity in the the means group random paramers
    dual_complexities = 0
    secondary_complexity = 6 #5 Group Random Parmss
    forced_variables = None
    seperate_out_factors = 0  # convert data into binary (long format)
    removeFiles = 1  # remove the tex files which store the saved models
    postprocess = 0 #postprocess the solutions..
    
    helperprocess.remove_files(removeFiles)
    
    dataset = 7
  
    defineApp = 0 # if using the APP as input
    if defineApp:
        from tk_app import App

        app = App()
        algorithm = app.algorithm
        IS_MULTI = app.is_multi
        print('is it multi', IS_MULTI)
        if IS_MULTI:
            TEST_SET_SIZE = app.test_set_size
        else:
            TEST_SET_SIZE = 0
        MAX_TIME = app.max_time_limit
        MAX_ITER = app.max_iteration_limit
        OBJ_1 = 'bic'
        OBJ_2 = 'aic'
        if algorithm == 'simulated annealing':
            algorithm = 'sa'
            NUM_INTL_SLNS = app.population_size
            SWAP_SA = app.swap_sa
            STEP_SA = app.step_sa
        elif algorithm == 'harmony search':
            algorithm = 'hs'
            POPULATION = app.population_size
        elif algorithm == 'differential evolution':
            algorithm = 'de'
            POPULATION = app.population_size
            CR_R = app.CR_R

        forced_variables = app.forced_variables
        intial_complexity = app.complexity_level
        helperprocess.check_list_type([app.all_data], pd.DataFrame)
        x_df = app.all_data
        
        if not isinstance(x_df, pd.DataFrame):
            raise TypeError
        y_df = app.all_data[app.y]
        
        x_df = x_df.drop(columns=[app.y])
        if app.offset is not None:
            x_df['Offset'] = app.offset
        else:
            x_df['Offset'] = np.zeros((len(x_df), 1))

        if algorithm == 'select decisions':
            AnalystSpecs = namedtuple('Analst',
                                      ['predictor', 'normal', 'random', 'random_dist', 'model', 'zi_terms'])
            print(app.model)
            
            reader = csv.DictReader(open('set_data.csv', 'r'))
            arguments = list()
            loop_condition = 1
            line_number_obs = 0
            for dictionary in reader: #TODO find a way to handle multiple arguments
                print(line_number_obs)
                arguments = dictionary
                if line_number_obs == int(args['line']):
                    break
                line_number_obs += 1
            print('the arguments is:', arguments)
            
            AnalystSpecs = app.y, app.normal_pars, app.random_pars, app.random_pars_dist, app.model, app.zi_variables, app.betas
            arguments['Manuel_Estimate'] = AnalystSpecs
            arguments['instance_number'] = 5
            arguments['is_multi'] = IS_MULTI
            if IS_MULTI == 0:
                arguments['_obj_2'] = None
                arguments['test_percentage'] = 0
            obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
            print('cool')
            #obj_fun = ObjectiveFunction(y_df, x_df, AnalystSpecs, algorithm='analyst specific')  # type: ignore
        if algorithm == 'simulated annealing':
            if app.specify is not None:
                AnalystSpecs = app.y, app.normal_pars, app.random_pars, app.random_pars_dist, app.model

        print(app.model)
        if '16-3' in app.output_path1:
            dataset = 4
            if 'variable' in app.output_path1:
                dataset = 20
                df = pd.read_csv('Ex-16-3variables.csv')  # read in the data
                y_df = df[['FREQ']]  # only consider crashes
                y_df.rename(columns={"FREQ": "Y"}, inplace=True)
                x_df = df.drop(columns=['FREQ'])
                print(df)
        elif 'artificial' in app.output_path1:  # todo handle datsets properly
            # const, x1, x6, POS
            dataset = 5
        elif 'ThaiAccident' in app.output_path1:
            dataset = 6
        elif '1848' in app.output_path1:
            dataset = 1
        else:
            dataset = 20
    else:
        print('reading set data...')
        app = None
        reader = csv.DictReader(open('set_data.csv', 'r'))
        arguments = list()
        loop_condition = 1
        line_number_obs = 0
        for dictionary in reader: #TODO find a way to handle multiple arguments
            print(line_number_obs)
            arguments = dictionary
            if line_number_obs == int(args['line']):
                break
            line_number_obs += 1
        print('the arguments is:', arguments)
        dataset = int(arguments['problem_number'])
    start = timeit.default_timer()
    
    print('the dataset is', dataset)
    if dataset == 1:
        df = pd.read_csv('1848.csv')  # read in the data
        y_df = df[['FSI']]  # only consider crashes
        y_df.rename(columns={"FSI": "Y"}, inplace=True)
        x_df = df.drop(columns=['FSI'])
        x_df = helperprocess.as_wide_factor(x_df)
    elif dataset == 2:
        df = pd.read_csv('4000.csv')  # read in the data
        y_df = df[['Y']].copy()  # only consider crashes
        x_df = df.drop(columns=['Y', 'CT'])
        x_df.rename(columns={"O": "Offset"}, inplace=True)
        x_df = helperprocess.as_wide_factor(x_df)
    elif dataset == 3:
        x_df = pd.read_csv('Stage5A_1848_All_Initial_Columns.csv')  # drop the ID columns
        drop_these = ['Id', 'ID', 'old', 'G_N']
        for i in drop_these:
            x_df.drop(x_df.filter(regex=i).columns, axis=1, inplace=True)
        y_df = x_df[['Headon']].copy()  # only consider crashes
        y_df.rename(columns={"Headon": "Y"}, inplace=True)
        x_df['Offset'] = np.log(x_df['LEN_YR'] * 1000) / 10  # Offset
       
        x_df = x_df.drop(columns=['Headon', 'LEN_YR'])  # drop the main predictor
        drop_these_too = ['LEN']
        for i in drop_these_too:
            x_df.drop(x_df.filter(regex=i).columns, axis=1, inplace=True)
        
        helperprocess.as_wide_factor(x_df, seperate_out_factors, keep_original=1)
        x_df = helperprocess.interactions(x_df)



    elif dataset == 4:
        df = pd.read_csv('Ex-16-3.csv')  # read in the data
        y_df = df[['FREQ']].copy()  # only consider crashes
        y_df.rename(columns={"FREQ": "Y"}, inplace=True)
        x_df = df.drop(columns=['FREQ', 'ID'])
        try:  # grabbing the offset amount
            x_df['Offset'] = np.log(1+x_df['AADT'] * x_df['LENGTH'] * 365 / 100000000)
            x_df = x_df.drop(columns=['AADT' , 'LENGTH'])
        except:
            raise Exception

        if seperate_out_factors:
            x_df = helperprocess.as_wide_factor(x_df, keep_original=1)
        else:

            x_df = pd.get_dummies(x_df, columns=['FC'], prefix=['FC'], prefix_sep='_')
            
        x_df = helperprocess.interactions(x_df)    

    elif dataset == 5:
        df = pd.read_csv('artificial_ZA.csv')  # read in the data
        y_df = df[['Y']].copy()  # only consider crashes
        #y_df.rename(columns={"fsi": "Y"}, inplace=True)
        x_df = df.drop(columns=['Y'])  # was dropped postcode
        x_df = helperprocess.as_wide_factor(x_df, keep_original=1)
        x_df = helperprocess.interactions(x_df)
        print(x_df)
        
    elif dataset ==6:
        print('check here')
        df = pd.read_csv('ThaiAccident.csv')  # read in the data
        print('the lenght of the dataset is', len(df))
        print(df.head())
        print('true mean', np.mean(df['Death']))
        
        #df = df.groupby('Month', group_keys =False).apply(lambda x: x.sample(frac = 0.1))
        print(df.head())
        print('Mean after sampling:', np.mean(df['Death']))
        y_df = df[['Death']].copy()  # only consider crashes
        y_df.rename(columns={"Death": "Y"}, inplace=True)
        x_df = df.drop(columns=['Death', 'ID'])  # was dropped postcode
        x_df = convert_df_columns_to_binary_and_wide(x_df)
       
    elif dataset ==7:
        df = pd.read_csv('artificial_mixed_corr_2023_MOOF.csv')  # read in the data
        y_df = df[['Y']].copy()  # only consider crashes
        #y_df.rename(columns={"fsi": "Y"}, inplace=True)
        try:
            x_df = df.drop(columns=['Y'])  # was dropped postcode
        except:
            x_df = df.drop(columns=['Y'])  # was dropped postcode
        x_df = helperprocess.as_wide_factor(x_df, keep_original=1)
        x_df = helperprocess.interactions(x_df)
    elif dataset == 8:
        df = pd.read_csv('rural_int.csv')  # read in the data
        y_df = df[['crashes']].copy()  # only consider crashes
        y_df.rename(columns={"crashes": "Y"}, inplace=True)
        panels = df['orig_ID']
        try:
            x_df = df.drop(columns=['crashes', 'year', 'orig_ID', 
                                    'jurisdiction', 'town', 'maint_region', 'weather_station'])  # was dropped postcode
            print('dropping for test')
            x_df = x_df.drop(columns=['month', 'inj.fat'])  
            x_df = x_df.drop(columns = [ 'zonal_ID', 'ln_AADT', 'ln_seg'])   
            x_df['rumble_install_year'] = x_df['rumble_install_year'].astype('category').cat.codes
            x_df.rename(columns={"rumble_install_year": "has_rumble"}, inplace=True)
            
        except:
            x_df = df.drop(columns=['Y'])  # was dropped postcode
        x_df = helperprocess.as_wide_factor(x_df, keep_original=1)
        x_df = helperprocess.interactions(x_df)
    elif dataset == 9:
        df = pd.read_csv('panel_synth.csv')  # read in the data
        y_df = df[['Y']].copy()  # only consider crashes
        y_df.rename(columns={"crashes": "Y"}, inplace=True)
        panels = df['ind_id']
        
        x_df = df.drop(columns=['Y', 'alt'])
        print(x_df)
                                 
           
        #x_df = helperprocess.as_wide_factor(x_df, keep_original=1)
        #x_df = helperprocess.interactions(x_df)
             
    
    else:  # the datasett has been selected in the program as something else
        raise Exception('dataset not found')
        

    
    reader = csv.DictReader(open('set_data.csv', 'r'))
    arguments = list()
    loop_condition = 1
    line_number_obs = 0
    for dictionary in reader: #TODO find a way to handle multiple arguments
        arguments = dictionary
        if line_number_obs == int(args['line']):
            break
        line_number_obs += 1
    arguments['instance_number'] = args['line']    
    arguments = dict(arguments)
    print('the arguments is:', arguments)
    if arguments['problem_number'] == str(8):
        arguments['group'] = 'county'
        arguments['panels'] =  'element_ID'
        arguments['ID'] ='element_ID'
    elif arguments['problem_number'] == str(9):
        arguments['group'] = 'group'
        arguments['panels'] =  'ind_id'
        arguments['ID'] ='ind_id'
   
    if not isinstance(arguments, dict):
        raise Exception
    else:
        arguments['test_percentage'] = 0.2
        if 'complexity_level' in arguments:
             arguments['complexity_level'] = int( arguments['complexity_level'])
        else:    
            arguments['complexity_level'] = initial_complexity
    if not defineApp:  # if no manual input ALGORITHMS DEPEND ON The SET_DATA_CSV TO DEFINE HYPERPARAMATERS
        AnalystSpecs = None
        if dataset != 9:
            x_df = helperprocess.drop_correlations(x_df) 
        arguments['AnalystSpecs'] = AnalystSpecs
        multi_threaded = 0
        if arguments['algorithm'] == 'sa':
            arguments_hyperparamaters = {'alpha': float(arguments['temp_scale']), 
                                         'STEPS_PER_TEMP': int(arguments['steps']), 
                                         'INTL_ACPT': 0.5, 
                                         '_crossover_perc': arguments['crossover'], 
                                         'MAX_ITERATIONS': int(arguments['_max_imp'])
                                         ,'_num_intl_slns': 25}
            helperprocess.entries_to_remove(('crossover', '_max_imp', '_hms', '_hmcr', '_par'), arguments)
            print(arguments)
            obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
          
               # results = simulated_annealing(obj_fun, 1, 1, None, arguments_hyperparamaters)
            
            results = simulated_annealing_non_mp(obj_fun, None, **arguments_hyperparamaters)
            helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi']))
            if dual_complexities:
                arguments['complexity_level'] = secondary_complexity
                obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
               
                    #results = simulated_annealing(obj_fun, 1, 1, None, arguments_hyperparamaters)
                
                results = simulated_annealing_non_mp(obj_fun, None, **arguments_hyperparamaters)
                helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi']))
             
        elif arguments['algorithm'] == 'hs':
            arguments['_mpai'] = 1
            obj_fun = ObjectiveFunction(x_df, y_df, **arguments)

           
            
            
            results = harmony_search_non_mp(obj_fun, None)
            helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi']))    
            
            if dual_complexities:
                arguments['complexity_level'] = secondary_complexity
                obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
                #if multi_threaded:
                #    results = harmony_search(obj_fun, 1, 1, None)
                #else:
                results = harmony_search_non_mp(obj_fun, None)
                helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi']))  

                      
        elif arguments['algorithm'] =='de':
            arguments_hyperparamaters = {'_AI': 1, 
                                        '_crossover_perc': float(arguments['crossover']), 
                                         '_max_iter': int(arguments['_max_imp'])
                                         ,'_pop_size': int(arguments['_hms']), 'instance_number': int(args['line'])}
            arguments_hyperparamaters = dict(arguments_hyperparamaters)
            helperprocess.entries_to_remove(('crossover', '_max_imp', '_hms', '_hmcr', '_par'), arguments)
            obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
           # if multi_threaded:
                
              #  results = differential_evolution(obj_fun, 1, 1, None, **arguments_hyperparamaters)
           # else:
            results = differential_evolution_non_mp(obj_fun, None, **arguments_hyperparamaters) 
            
            helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi'])) 
            if dual_complexities:
                arguments['complexity_level'] = secondary_complexity
                obj_fun = ObjectiveFunction(x_df, y_df, **arguments)
                
                    
               # results = differential_evolution(obj_fun, 1, 1, None, **arguments_hyperparamaters)
                
              
                results = differential_evolution_non_mp(obj_fun, None, **arguments_hyperparamaters) 
                
                helperprocess.results_printer(results, arguments['algorithm'], int(arguments['is_multi'])) 
                  
               
            



if __name__ == '__main__':
    """Loading in command line arguments.  """
    parser = argparse.ArgumentParser(prog='main',
                                    epilog=main.__doc__,
                                    formatter_class= argparse.RawDescriptionHelpFormatter)

    parser.add_argument('line', type=int, default=10,
                        help='line to read csv')

    




        


    try:
        args = vars(parser.parse_args())
        print('args is ',args)
    except:
        args = {'line': 0}
    print(args)
    main(args)  
    
  

    
    
    