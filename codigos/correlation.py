import pandas as pd
def correlation_table(exams_path, results_path):
    exam_dataframes = []
    for exam in exams_path:
        exam_dataframes.append( pd.read_csv(exam, na_values = "?", comment='\t',
            sep=",", skipinitialspace=True ) )
    2+2

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
    
    exam_dataframes[0].to_excel(writer, sheet_name='Sheet1')
    exam_dataframes[1].to_excel(writer, sheet_name='Sheet2')
    correlation_table.to_excel(writer, sheet_name='Correlacao')
    writer.save()
