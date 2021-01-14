from lmfit import Model, minimize, fit_report
import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import sys
import re
import os.path


def model_tau(x, amp, tau):
	#droop and undershoot fitting with single tau
	return (amp*np.exp(-x/tau))


def fit_droop(Times, Voltages):
	mask = Voltages >= np.max(Voltages)*0.5
	V = Voltages[mask]
	T = Times[mask]
	#remove the rise and down time behavior
	T = T[150:-30]
	V = V[150:-30]
	#define the time T0 as the begining of the pulse
	T = T - T[0]
	#call the fitting function and print results
	y = np.array(V)
	x = np.array(T)
	gmodel = Model(model_tau, calc_covar=True)
	params = gmodel.make_params(amp=0.1, tau=20E-6)
	result = gmodel.fit(y, params, x=x)
	print(result.fit_report())
	Amp = result.params['amp'].value
	sAmp = result.params['amp'].stderr
	tau = result.params['tau'].value
	stau = result.params['tau'].stderr
	chi2 = result.chisqr
	covar_matrix = result.covar
	'''
	f = open("/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitudes.txt","a")
	f.write("%f" % (Directory_board))#Number of board
	f.write(" ")
	f.write("%s" % (Directory_temp))#Temperature
	f.write(" ")
	f.write("%.11f" % (max(Voltages)))#maximum voltage
	f.write(" ")
	f.write("%.11f" % (V[150]))#voltage that begins to fit
	f.write(" ")
	f.write("%s" % (Temperature))#temperature
	f.write(" ")
	f.write("%s" % (Batch))#batch num
	f.write("\r\n")
	f.close()'''
	return  Amp, sAmp, tau, stau, chi2, covar_matrix, max(Voltages), V[150]


def fit_under(Times, Voltages):
	mask_under = Voltages >= np.max(Voltages)*0.4
	T = Times[mask_under]
	mask = Times >= T[-1]
	T = Times[mask]
	V = Voltages[mask]
	#remove the rise and down time behavior
	T = T[150:-2]
	V = V[150:-2]
	T = T - T[0]
	#call the fitting function and print results
	y = np.array(V)
	x = np.array(T)
	gmodel = Model(model_tau, calc_covar=True)
	params = gmodel.make_params(amp=-0.1, tau=30E-6)
	result = gmodel.fit(y, params, x=x)
	print(result.fit_report())
	Amp = result.params['amp'].value
	sAmp = result.params['amp'].stderr
	tau = result.params['tau'].value
	stau = result.params['tau'].stderr
	chi2 = result.chisqr
	covar_matrix = result.covar
	return Amp, sAmp, tau, stau, chi2, covar_matrix


def plot_results_droop(time, voltage, amp_d, tau_d, stau_d):
	TIME = sum(time)/len(time)
	VOLT = sum(voltage)/len(voltage)
	mask_droop = VOLT >= np.max(VOLT)*0.5
	T_d = TIME[mask_droop]
	V_d = VOLT[mask_droop]
	T_d_fit = T_d[150:-30]
	V_d_fit = np.mean(amp_d)*np.exp(-(T_d_fit-T_d_fit[0])/np.mean(tau_d))

	plt.figure(00)
	plt.ylabel(r'Voltage (mV)')
	plt.xlabel('Time ($\mu$s)')
	plt.plot(T_d*1E6, V_d*1E3, label= r'Data at %s$^\circ$C' %(Directory_temp))
	plt.plot(T_d_fit*1E6, V_d_fit*1E3, label= r'Fitted Data at %s$^\circ$C' %(Directory_temp))
	plt.title(r'Droop HVB %s: %.2f +/- %.2f [$\mu$s]' %(Directory_board,np.mean(tau_d)*1E6,np.mean(stau_d)*1E6))
	plt.grid(linestyle='dotted')
	plt.legend(loc='best')
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/fit/png/HVB%s_Temp%s_Droop.png' %(Directory_board, Directory_temp))
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/fit/svg/HVB%s_Temp%s_Droop.svg' %(Directory_board, Directory_temp))
	#plt.show()
	plt.clf()
	plt.cla()
	plt.close()



def plot_results_undershoot(time, voltage, amp_u, tau_u, stau_u):
	TIME = sum(time)/len(time)
	VOLT = sum(voltage)/len(voltage)
	mask_under = VOLT >= np.max(VOLT)*0.4
	T = TIME[mask_under]
	mask = TIME >= T[-1]
	T_u = TIME[mask]
	V_u = VOLT[mask]
	T_u_fit = T_u[150:-2]
	V_u_fit = np.mean(amp_u)*np.exp(-(T_u_fit-T_u_fit[0])/np.mean(tau_u))

	plt.figure(00)
	plt.ylabel(r'Voltage (mV)')
	plt.xlabel('Time ($\mu$s)')
	plt.ylim(np.min(V_u)*1E3,0)
	plt.plot(T_u*1E6, V_u*1E3, label= r'data %s$^\circ$C' %(Directory_temp))
	plt.plot(T_u_fit*1E6, V_u_fit*1E3, label= r'Mean data %s$^\circ$C' %(Directory_temp))
	plt.title(r'Undershoot HVB %s: %.2f +/- %.2f [$\mu$s]' %(Directory_board,np.mean(tau_u)*1E6,np.mean(stau_u)*1E6))
	plt.grid(linestyle='dotted')
	plt.legend(loc='best')
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/fit/png/HVB%s_Temp%s_Undershoot.png' %(Directory_board, Directory_temp))
	plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/figures/fit/svg/HVB%s_Temp%s_Undershoot.svg' %(Directory_board, Directory_temp))
	#plt.show()
	plt.clf()
	plt.cla()
	plt.close()



def open_fit_return():
	#open data files, fit data and return the time constant results
	files = '/home/stephy/ICECUBE/database/B%s_HVB_%s/%s/*.CSV' %(Batch, Directory_board, Directory_temp)
	filename=sorted(glob.glob(files))
	NumF = len(glob.glob(files))
	Voltage = []
	Time = []
	Amp_d = []
	sAmp_d = []
	Tau_dr = []
	sTau_dr = []
	X2_dr = []
	Amp_u = []
	sAmp_u = []
	Tau_un = []
	sTau_un = []
	X2_un = []
	V_max = []
	V150 = []
	for i in range(0,NumF):
		data = np.loadtxt(fname=filename[i], delimiter=',', skiprows=25)
		time = data[:,0]
		volt = data[:,1]
		volts = volt - np.mean(volt[0:100]) #Extract the baseline
		A_d, sA_d, Tau_d, Stau_d, X2_d, covar_matrix_d, v_max, v150 = fit_droop(time, volts)
		A_u, sA_u, Tau_u, Stau_u, X2_u, covar_matrix_u = fit_under(time, volts)
		if Tau_d <1E-4 and Tau_d > 0 and Tau_u <1E-4 and Tau_u > 0:
			Voltage.append(volts)
			Time.append(time)
			Amp_d.append(A_d)
			sAmp_d.append(sA_d)
			Tau_dr.append(Tau_d)
			sTau_dr.append(Stau_d)
			X2_dr.append(X2_d)
			V_max.append(v_max)
			V150.append(v150)
			Amp_u.append(A_u)
			sAmp_u.append(sA_u)
			Tau_un.append(Tau_u)
			sTau_un.append(Stau_u)
			X2_un.append(X2_u)
	Droop = [Amp_d, sAmp_d, Tau_dr, sTau_dr, X2_dr, V_max, V150]
	Undershoot = [Amp_u, sAmp_u, Tau_un, sTau_un, X2_un]
	plot_results_droop(Time, Voltage, Droop[0], Droop[2], Droop[3])
	plot_results_undershoot(Time, Voltage, Undershoot[0], Undershoot[2], Undershoot[3])
	return Droop, Undershoot


def build_data_frame(Droop, Undershoot):
	num_files = len(Droop[0])
	board_id = ['HVB_{}'.format(Directory_board)] * num_files
	idxs = ['HVB_{}'.format(Directory_board)]
	channel = int(Channel)*np.ones((1,num_files))
	iterables = [idxs, np.arange(num_files)]
	m_idx = pd.MultiIndex.from_product(iterables, names=['Board_ID', 'Waveform_number'])
	fit_data = np.concatenate((np.asarray(Droop), np.asarray(Undershoot)))
	dir_temp = int(Directory_temp)*np.ones((1, num_files))
	real_temp = float(Temperature)*np.ones((1, num_files))
	batch = int(Batch)*np.ones((1, num_files))
	data = np.concatenate((channel, dir_temp, real_temp, batch, fit_data)).T
	print(fit_data.ndim, fit_data.shape, dir_temp.shape, dir_temp.ndim, data.shape)
	df = pd.DataFrame(data, columns = ['Channel', 'Directory_temperature', 'Real_temperature',
		'Batch', 'Amplitude_droop', 'Error_Amplitude_droop', 'Tau_droop', 'Error_Tau_Droop',
		'chi2_droop', 'Maximum Voltage', 'Maximum Voltage for Fit', 'Amplitude_undershoot', 'Error_Amplitude_undershoot', 'Tau_undershoot',
		'Error_Tau_undershoot', 'chi2_undershoot'], index = m_idx)
	return df


def store_df(Droop, Undershoot):
	df = build_data_frame(Droop, Undershoot)
	filename = '/home/stephy/ICECUBE/undershoot/20200609/Results_droop_undershoot.h5'
	if os.path.isfile(filename):
		previous_df = pd.read_hdf(filename)
		new_df = df.append(previous_df)
		new_df.to_hdf(filename, key='new_df', mode='w')
		print('The data has been succesfully attached!')
	else:
		df.to_hdf(filename, key='df', mode='w')
		print('A new data frame has been created!')


def main():
	Droop, Undershoot = open_fit_return() #open the files, fit and return values
	store_into_dataframe = store_df(Droop, Undershoot)
	print(store_into_dataframe)

if __name__ == "__main__":
	plt.rcParams.update({'font.size': 13})
	global Directory_board
	Directory_board = int(sys.argv[1]) #17,18,19,20
	print('\n\n', Directory_board, '\n\n')
	global Directory_temp
	Directory_temp = sys.argv[2] #-55,-50,-45,-40,-35,20
	global Temperature
	Temperature = sys.argv[3]
	global Batch
	Batch = sys.argv[4] #1, 2, 3, 4
	global Channel
	Channel = sys.argv[5] #1, 2, 3, 4, 5, 6, 7, ...
	main()
