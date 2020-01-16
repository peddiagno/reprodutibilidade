import pandas as pd
def correlation_table(exams_path, results_path):
    exam_dataframes = []
    for i in range(2):
        exam_dataframes.append( pd.read_csv( exams_path[i], na_values = "?", comment='\t',
            sep=",", skipinitialspace=True ) )
    headers = exam_dataframes[0].columns
    correlation_values = []
    for col in headers:
        measures_from_each_dataframe = pd.DataFrame()
        for exam_dataframe in exam_dataframes:
            measures_from_each_dataframe = pd.concat([measures_from_each_dataframe
                                                     , exam_dataframe[col]], axis = 1)
        correlation = measures_from_each_dataframe.corr().iloc[0,0]
        correlation_values.append(correlation)
    correlation_table = pd.DataFrame([correlation_values], columns=headers)

    correlation_table = correlation_table.round(2)
    
    writer = pd.ExcelWriter(results_path + "correlacao.xlsx", engine = 'xlsxwriter')
    serial_number0 = exams_path[0].split("/")[2].split("_")[0]
    serial_number1 = exams_path[1].split("/")[2].split("_")[0]
    

    workbook = writer.book
    title_format = workbook.add_format({'bold': True})
    
    prepare_sheets(exam_dataframes[0], serial_number0,
                   "Exames {}".format(serial_number0), writer, title_format )
    
    prepare_sheets(exam_dataframes[1], serial_number1,
                   "Exames {}".format(serial_number1), writer, title_format )
    
    prepare_sheets(correlation_table, "Correlacao",
                   "Correlacao entre os equipamentos", writer, title_format )

    writer.save()
    
def prepare_sheets(dataframe, sheet_name, title, excel_writer, style):

    dataframe.to_excel(excel_writer, sheet_name=sheet_name,
                   startcol = 0, startrow = 1, index = False)
    worksheet = excel_writer.sheets[sheet_name]
    worksheet.write('I1', title, style)
