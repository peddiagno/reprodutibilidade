import pandas as pd
import statistics
def reproducibility_table(exams_path, basename, results_path):
    measures_table = pd.read_csv(exams_path, na_values = "?", comment='\t',
            sep=",", skipinitialspace=True )

    results_order = ["wbc","lynp","monp","midp","neup","eosp","rbc","hgb",
                    "hct","mcv","mch","mchc","rdw_cv","rdw_sd","plt",
                    "mpv","pct","pdw","plcr"]

    headers = measures_table.columns
    sds = []
    means = []
    cvs = []
    if len(measures_table) < 2:
        print("Somente um exame no diretorio, nao e possivel obter as estatisticas")
        return
    for j in headers:
        sd = statistics.stdev(measures_table[j])
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
    measures_table.to_csv(results_path + basename + ".csv", index=False)
