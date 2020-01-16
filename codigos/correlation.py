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

    return( { "machine0": exam_dataframes[0], 
              "machine1": exam_dataframes[1],
              "correlation": correlation_table } )
