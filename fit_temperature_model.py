from lmfit import Model, minimize, fit_report #calculate the covariance matrix
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import sys
import re
import os.path
#import matplotlib.colors as colors


def model_temp(x, A, B, C):
	return (A + B/(1+np.exp(-x/C)))


def model_line(x, A, B):
	return (A*x + B)


def line_fit(x, y):
	gmodel = Model(model_line, calc_covar=True)
	params = gmodel.make_params(A=1, B=0)
	result = gmodel.fit(y, params, x=x)
	print(result.fit_report())
	A_eval = result.params['A'].value
	A_stdr = result.params['A'].stderr
	B_eval = result.params['B'].value
	B_stdr = result.params['B'].stderr
	chi2 = result.chisqr
	covar_matrix = result.covar
	return A_eval, A_stdr, B_eval, B_stdr, chi2, covar_matrix, result.best_fit


def temp_fit(x, y):
	gmodel = Model(model_temp, calc_covar=True)
	params = gmodel.make_params(A=5E-6, B=40E-6, C=30)#unit [us]
	result = gmodel.fit(y, params, x=x)
	print(result.fit_report())
	p_A = result.params['A'].value
	sp_A = result.params['A'].stderr
	p_B = result.params['B'].value
	sp_B = result.params['B'].stderr
	p_C = result.params['C'].value
	sp_C = result.params['C'].stderr
	chi2 = result.chisqr
	covar_matrix = result.covar
	return p_A, sp_A, p_B, sp_B, p_C, sp_C, chi2, covar_matrix, result.best_fit


def get_mean_std(temp, tau):
	Temperature = np.unique(temp)
	Tau = []
	sTau = []
	for t in Temperature:
		mask = temp == t
		tau_mask = tau[mask]
		Tau.append(np.mean(tau_mask))
		sTau.append(np.std(tau_mask))
	Tau = np.asarray(Tau)
	sTau = np.asarray(sTau)
	return Temperature, Tau, sTau


def load_dataframe():
	'''
	df == fit droop and undershoot report dataframe (16 variables for the header)
	Index(['Channel', 'Directory_temperature', 'Real_temperature', 'Batch',
       'Amplitude_droop', 'Error_Amplitude_droop', 'Tau_droop',
       'Error_Tau_Droop', 'chi2_droop', 'Maximum Voltage',
       'Maximum Voltage for Fit', 'Amplitude_undershoot',
       'Error_Amplitude_undershoot', 'Tau_undershoot', 'Error_Tau_undershoot',
       'chi2_undershoot'],
      dtype='object')
	'''
	fit_report = '/home/stephy/ICECUBE/undershoot/20200609/Results_droop_undershoot.h5'
	if os.path.isfile(fit_report):
		df = pd.read_hdf(fit_report)
		print('The columns in this dataframe are:', df.columns)
		return df
	else:
		print('The fit of Droop/Unsershoot dataframe is missing! \n\n Current name: Results_droop_undershoot.h5')


def droop_undershoot():
	df = load_dataframe()
	sum = df.reset_index().groupby('Board_ID').count()#sum[0]=HVB_1
	HV_Boards = sum.index
	alpha = []
	salpha = []
	beta = []
	sbeta = []
	chi2 = []
	covar_matrix = []
	board_id = []
	df_channel = []
	df_temperature = []
	df_batch = []
	for HVB in HV_Boards:
		locate = df.loc[HVB]
		board_id.append(HVB)
		Td = locate['Tau_droop']
		Tu = locate['Tau_undershoot']
		Ch = locate['Channel']
		Temp = locate['Real_temperature']
		bh = locate['Batch']
		u_ch = np.unique(Ch)
		if len(u_ch) == 1 and len(np.unique(bh)) == 1:
			bh = bh[0]
			u_ch = u_ch[0]
		else:
			print(f'Channels found for {HVB}: {np.unique(Ch)}')
			print(f'Batches found for  {HVB}: {np.unique(bh)}')
			raise ValueError('HVB has multiple channels, please check dataframe!')
		df_channel.append(u_ch)
		inter_temp = np.unique(Temp)
		df_temperature.append(inter_temp.tolist())
		df_batch.append(np.unique(bh))
		a, sa, b, sb, c, cov, best_fit = line_fit(Tu, Td)
		alpha.append(a)
		salpha.append(sa)
		beta.append(b)
		sbeta.append(sb)
		chi2.append(c)
		covar_matrix.append(cov.tolist())
		plot_results_droop_undershoot(HVB, Tu, Td, best_fit, a, b)
	DroopVsUndershoot = [board_id, df_channel, df_temperature, df_batch, alpha, salpha, beta, sbeta, chi2, covar_matrix]
	return DroopVsUndershoot


def plot_results_droop_undershoot(Directory_board, tau_under, tau_droop, best_fit, alpha, beta):
	plt.ylabel(r'Droop ($\mu$s)')
	plt.xlabel(r'Undershoot ($\mu$s)')
	if beta < 0:
		plt.title(r'$\tau$(droop) = %.3f * $\tau$(undershoot)  %.3f' %(alpha, beta*1E6))
	else:
		plt.title(r'$\tau$(droop) = %.3f * $\tau$(undershoot) + %.3f' %(alpha, beta*1E6))
	plt.plot(tau_under*1E6, tau_droop*1E6, 'o', ms=1, label='HV Board {}'.format(Directory_board))
	plt.plot(tau_under*1E6, best_fit*1E6, ms=20, alpha=0.5)
	plt.legend(loc='best')
	plt.grid(linestyle='dotted')
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/DroopUndershoot/png/{}_DroopUndershoot.png'.format(Directory_board))
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/DroopUndershoot/svg/{}_DroopUndershoot.svg'.format(Directory_board))
	#plt.show()
	plt.clf()
	plt.cla()
	plt.close()


def droop_temperature():
	df = load_dataframe()
	sum = df.reset_index().groupby('Board_ID').count()#sum[0]=HVB_1
	HV_Boards = sum.index
	p0 = []
	sp0 = []
	p1 = []
	sp1 = []
	p2 = []
	sp2 = []
	chi2 = []
	covar_matrix = []
	for HVB in HV_Boards:
		locate = df.loc[HVB]
		Td = locate['Tau_droop']
		Temp = locate['Real_temperature']
		pA, spA, pB, spB, pC, spC, c, cov, best_fit = temp_fit(Temp, Td)
		p0.append(pA)
		sp0.append(spA)
		p1.append(pB)
		sp1.append(spB)
		p2.append(pC)
		sp2.append(spC)
		chi2.append(c)
		covar_matrix.append(cov.tolist())
		plot_results_droop_temperature(HVB, Temp, Td, best_fit, pA, pB, pC)
	DroopVsTemp = [p0, sp0, p1, sp1, p2, sp2, chi2, covar_matrix]
	return DroopVsTemp


def plot_results_droop_temperature(Directory_board, temp, tau_droop, best_fit, p0, p1, p2):
	Temperature, TD, sTD = get_mean_std(temp, tau_droop)
	plt.ylabel(r'%s ($\mu$s)' %('Droop'))
	plt.xlabel(r'Temperature ($^\circ$C)')
	plt.title(r'$\tau$(u) = %.1f + %.1f/(1+exp(T/%.1f))' %(p0*1E6, p1*1E6, p2))
	plt.errorbar(Temperature, TD*1E6, yerr=sTD*1E6, fmt='o', ms=5, label='Directory_board-%s' %(Directory_board))
	plt.plot(temp, best_fit*1E6, ms=25, alpha=0.5, label='Temp-droop fit')
	plt.legend(loc='best')
	plt.grid(linestyle='dotted')
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/DroopTemperature/png/{}_DroopTemperature.png'.format(Directory_board))
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/DroopTemperature/svg/{}_DroopTemperature.svg'.format(Directory_board))
	#plt.show()
	plt.clf()
	plt.cla()
	plt.close()


def undershoot_temperature():
	df = load_dataframe()
	sum = df.reset_index().groupby('Board_ID').count()#sum[0]=HVB_1
	HV_Boards = sum.index
	p3 = []
	sp3 = []
	p4 = []
	sp4 = []
	p5 = []
	sp5 = []
	chi2 = []
	covar_matrix = []
	for HVB in HV_Boards:
		locate = df.loc[HVB]
		Tu = locate['Tau_undershoot']
		Temp = locate['Real_temperature']
		pA, spA, pB, spB, pC, spC, c, cov, best_fit = temp_fit(Temp, Tu)
		p3.append(pA)
		sp3.append(spA)
		p4.append(pB)
		sp4.append(spB)
		p5.append(pC)
		sp5.append(spC)
		chi2.append(c)
		covar_matrix.append(cov.tolist())
		plot_results_undershoot_temperature(HVB, Temp, Tu, best_fit, pA, pB, pC)
	UndershootVsTemp = [p3, sp3, p4, sp4, p5, sp5, chi2, covar_matrix]
	return UndershootVsTemp


def plot_results_undershoot_temperature(Directory_board, temp, tau_undershoot, best_fit, p3, p4, p5):
	Temperature, TU, sTU = get_mean_std(temp, tau_undershoot)
	plt.ylabel(r'%s ($\mu$s)' %('Undershoot'))
	plt.xlabel(r'Temperature ($^\circ$C)')
	plt.title(r'$\tau$(u) = %.1f + %.1f/(1+exp(T/%.1f))' %(p3*1E6, p4*1E6, p5))
	plt.errorbar(Temperature, TU*1E6, yerr=sTU*1E6, fmt='o', ms=5, label='Directory_board-%s' %(Directory_board))
	plt.plot(temp, best_fit*1E6, ms=25, alpha=0.5, label='Temp-droop fit')
	plt.legend(loc='best')
	plt.grid(linestyle='dotted')
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/UndershootTemperature/png/{}_UndershootTemperature.png'.format(Directory_board))
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/UndershootTemperature/svg/{}_UndershootTemperature.svg'.format(Directory_board))
	#plt.show()
	plt.clf()
	plt.cla()
	plt.close()


def build_data_frame():
	DroopVsUndershoot = droop_undershoot()
	DroopVsTemp = droop_temperature()
	UndershootVsTemp = undershoot_temperature()
	data = np.concatenate((DroopVsUndershoot, DroopVsTemp, UndershootVsTemp)).T
	df = pd.DataFrame(data, columns = ['Board_ID', 'Channel', 'Real_temperature',
		'Batch', 'Alpha', 'Error_Alpha', 'Beta', 'Error_Beta', 'chi2_AlphaBeta',
		'covar_matrix_AlphaBeta', 'p0', 'Error_p0', 'p1', 'Error_p1', 'p2', 'Error_p2',
		'chi2_p0p1p2', 'covar_matrix_p0p1p2', 'p3', 'Error_p3', 'p4', 'Error_p4', 'p5',
		'Error_p5', 'chi2_p3p4p5', 'covar_matrix_p3p4p5'])
	return df


def store_df():
	df = build_data_frame()
	filename = '/home/stephy/ICECUBE/undershoot/20200609/Results_DroopUndershootTemperature.h5'
	df.to_hdf(filename, key='df', mode='w')
	print(df)
	return print('A new data frame has been created!')


def main():
	store_into_dataframe = store_df()

if __name__ == "__main__":
	np.set_printoptions(precision=10)
	plt.rcParams.update({'font.size': 13})
	input('WARNING: this script will erase any previous dataframe created under the name --Results_DroopUndershootTemperature.h5--, if sure, press any key to continue.')
	main()
