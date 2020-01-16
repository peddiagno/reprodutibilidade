import pandas as pd
import statistics
def reproducibility_table(exams_path, basename, results_path):
    measures_table = pd.read_csv(exams_path, na_values = "?", comment='\t',
            sep=",", skipinitialspace=True )

    headers = measures_table.columns
    sds = []
    means = []
    cvs = []

    for j in headers:
        sd = statistics.stdev(measures_table[j]) if len(measures_table) > 1 else 0
        mean = statistics.mean(measures_table[j])
        variation_coefficient = 100 * sd / mean if mean != 0 else 0
        sds.append(sd)
        means.append(mean)
        cvs.append(variation_coefficient)      

    identifiers = list(range(len(measures_table)))
    identifiers = identifiers + ["DP", "Media", "CV"]

    measures_table.loc[len(measures_table)] = sds
    measures_table.loc[len(measures_table)] = means
    measures_table.loc[len(measures_table)] = cvs

    measures_table.insert(0,"Exame",identifiers)
    measures_table = measures_table.round(2)
    
    return(measures_table)

