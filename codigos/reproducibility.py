import pandas as pd
import os
import glob
import statistics
import painter as pnt

data_path = 'dados/'
results_path = '../resultados/'
extension="csv"
os.chdir(data_path)

measures   = glob.glob('*results.csv')
pulses_plt_files = glob.glob('*plt.csv')
pulses_wbc_files = glob.glob('*wbc.csv')
pulses_rbc_files = glob.glob('*rbc.csv')

measures_table = pd.read_csv(measures[0], na_values = "?", comment='\t',
                              sep=",", skipinitialspace=True )

results_order = ["wbc","lynp","monp","midp","neup","eosp","rbc","hgb",
                 "hct","mcv","mch","mchc","rdw_cv","rdw_sd","plt",
                 "mpv","pct","pdw","plcr"]

headers = measures_table.columns
sds = []
means = []
cvs = []

basename = measures[0][:10]

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

pnt.create_histogram(pulses_plt_files,"plt",basename,results_path)
pnt.create_histogram(pulses_wbc_files,"wbc",basename,results_path)
pnt.create_histogram(pulses_rbc_files,"rbc",basename,results_path)

measures_table.to_csv(results_path + measures[0], index=False)
