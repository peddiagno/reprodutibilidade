import os
import glob
import painter as pnt
import reproducibility as rpd
import correlation as crr
import pandas as pd
import sys

def save_sheet(dataframe, excel_writer, sheet_name, title, save_now):
    workbook = excel_writer.book
    title_format = workbook.add_format({'bold': True}) 
    dataframe.to_excel(excel_writer, sheet_name=sheet_name,
                   startcol = 0, startrow = 2, index = False)
    worksheet = excel_writer.sheets[sheet_name]
    worksheet.write('I1', title, title_format)
    if save_now: writer.save() 

#os.chdir("../")
    
data_path = 'dados/'
base_results_path = 'resultados/'

data_directories = glob.glob(data_path + '*/')

#selector = "correlation"

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
        
        pnt.create_histogram(pulses_plt_files,"plt",basename,results_path)
        pnt.create_histogram(pulses_wbc_files,"wbc",basename,results_path)
        pnt.create_histogram(pulses_rbc_files,"rbc",basename,results_path)
        
        rep_table = rpd.reproducibility_table(measures[0],basename,results_path)
        
        writer = pd.ExcelWriter(results_path + basename + ".xlsx", engine = 'xlsxwriter')
        save_sheet(rep_table, writer, "Reprodutibilidade",
                   "Reprodutibilidade {}".format(basename), True)
        

        
        
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
    
    exam_tables = crr.correlation_table(measures_path_list, results_path)
    serial_number0 = measures_path_list[0].split("/")[2].split("_")[0]
    serial_number1 = measures_path_list[1].split("/")[2].split("_")[0]
    
    writer = pd.ExcelWriter(results_path + "correlacao.xlsx", engine = 'xlsxwriter')
    save_sheet( exam_tables["machine0"], writer, serial_number0,
               "Exames {}".format(serial_number0), False )
    save_sheet( exam_tables["machine1"], writer, serial_number1,
               "Exames {}".format(serial_number1), False )
    save_sheet( exam_tables["correlation"], writer, "Correlacao",
               "Correlacao entre os equipamentos", False )
    
    worksheet = writer.sheets["Correlacao"]
    workbook = writer.book
    excelent_format = workbook.add_format({'font_color': '14a600', 'bold': True })
    good_format = workbook.add_format({'font_color': '#0000ff', 'bold': True })
    regular_format = workbook.add_format({'font_color': 'black', 'bold': True })
    bad_format = workbook.add_format({'font_color': 'red', 'bold': True })
                                           
    worksheet.conditional_format('A4:Z4', {'type':     'cell',
                                        'criteria': '>=',
                                        'value':    0.95,
                                        'format':   excelent_format})

    worksheet.conditional_format('A4:Z4', {'type':     'cell',
                                        'criteria': 'between',
                                        'minimum':   0.9,
                                        'maximum':   0.95,
                                        'format':   good_format})
    worksheet.conditional_format('A4:Z4', {'type':     'cell',
                                        'criteria': 'between',
                                        'minimum':   0.9,
                                        'maximum':   0.75,
                                        'format':   regular_format})
    worksheet.conditional_format('A4:Z4', {'type':     'cell',
                                        'criteria': '<',
                                        'value':    0.75,
                                        'format':   bad_format})
    writer.save()
    
    
    
        
        
