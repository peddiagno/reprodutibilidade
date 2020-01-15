import os
import glob
import painter as pnt
import reproducibility as rpd
import correlation as crr
import sys

data_path = 'dados/'
base_results_path = 'resultados/'

data_directories = glob.glob(data_path + '*/')
selector = sys.argv[1]

if selector == "reproducibility":
    for data_directory in data_directories:
        basename = data_directory.split("/")[1]
        measures = glob.glob(data_directory + '*results.csv')
        pulses_plt_files = glob.glob(data_directory + '*plt.csv')
        pulses_wbc_files = glob.glob(data_directory + '*wbc.csv')
        pulses_rbc_files = glob.glob(data_directory + '*rbc.csv')
        if not measures:
            print("Arquivo de resultados nao encontrado no diretorio {}".format(basename))
            continue       
        
        results_path = base_results_path + basename + "/"
        try: 
            os.mkdir(results_path) 
        except OSError as error: 
            print("Diretorio {} nao foi criado pois ja existe".format(results_path))     
        
        rpd.reproducibility_table(measures[0],basename,results_path)
        pnt.create_histogram(pulses_plt_files,"plt",basename,results_path)
        pnt.create_histogram(pulses_wbc_files,"wbc",basename,results_path)
        pnt.create_histogram(pulses_rbc_files,"rbc",basename,results_path)
        
elif selector == "correlation":
    measures_path_list = []
    for data_directory in data_directories:
        measures_path = glob.glob(data_directory + '*results.csv')
        if not measures_path:
            print("Arquivo de resultados nao encontrado no diretorio {}".format(basename))
            continue 
        measures_path_list.append(measures_path[0])
    results_path = base_results_path + "correlacao/"
    try: 
        os.mkdir(results_path) 
    except OSError as error: 
        print("Diretorio {} nao foi criado pois ja existe".format(results_path))
    
    crr.correlation_table(measures_path_list, results_path)
    
        
        
