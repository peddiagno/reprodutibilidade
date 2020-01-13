import os
import glob
import painter as pnt
import reproducibility as rpd

data_path = '../dados/'
results_path = '../resultados/'

os.chdir(data_path)
measures   = glob.glob('*results.csv')
pulses_plt_files = glob.glob('*plt.csv')
pulses_wbc_files = glob.glob('*wbc.csv')
pulses_rbc_files = glob.glob('*rbc.csv')
basename = measures[0][:10]

rpd.reproducibility_table(measures[0],basename,results_path)
pnt.create_histogram(pulses_plt_files,"plt",basename,results_path)
pnt.create_histogram(pulses_wbc_files,"wbc",basename,results_path)
pnt.create_histogram(pulses_rbc_files,"rbc",basename,results_path)