from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os.path
from pandas import DataFrame
import re


def load_dataframe(file):
    if os.path.isfile(file):
        df = pd.read_hdf(file)
        print('The columns in this dataframe are:', df.columns)
        return df
    else:
        print('The file dataframe is missing!')


def amplitude_vs_channel(df, temp, channel, number):
    mean = []
    mean_std = []
    median = []
    waveforms = []
    for i, ch in enumerate(channel):
        df_cut1 = df.loc[[(df['Channel'] == ch)] & (df['Directory_temperature'] == temp)]
        mean.append(df_cut1['Maximum Voltage for Fit'].mean() * 1E3)
        mean_std.append(np.std(df_cut1['Maximum Voltage for Fit']) * 1E3)
        median.append(np.median(df_cut1['Maximum Voltage for Fit']) * 1E3)
        waveforms.append(len(df_cut1['Maximum Voltage for Fit']))

        m = np.mean(df_cut1['Maximum Voltage for Fit'])*1E3
        s = np.std(df_cut1['Maximum Voltage for Fit'])*1E3
        #y, x, _ = plt.hist(a)
        dif = np.mean(df_cut1['Maximum Voltage for Fit']) - np.median(df_cut1['Maximum Voltage for Fit'])
        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title(f'Voltage Distribution ')
        plt.xlabel('Voltage for Fit (mV)')
        plt.ylabel('Waveforms')
        plt.hist(df_cut1['Maximum Voltage for Fit']*1E3, 10, stacked=True, alpha=0.35)
        #plt.fill_between(a, 0, y, y.max(), where = (a >= m - sigma_cut*s) & (a <= m + sigma_cut*s), color = 'g', alpha=0.25)
        #plt.fill_between(x, m - sigma_cut*s,  m + sigma_cut*s, color = 'g', alpha=0.25)
        plt.axvline(np.mean(df_cut1['Maximum Voltage for Fit'])*1E3, label='mean = {0:.2f}mV'.format(np.mean(df_cut1['Maximum Voltage for Fit'])*1E3))
        plt.axvline(np.median(df_cut1['Maximum Voltage for Fit'])*1E3, color='r', label='median = {0:.2f}mV \n mean-median = {1:.2f}mV'.format(np.median(df_cut1['Maximum Voltage for Fit'])*1E3, dif*1E3))
        #plt.axvline(m - sigma_cut*s, color='g')
        #plt.axvline(m + sigma_cut*s, color='g')
        fig.set_size_inches(12.5, 8.5, forward=True)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(linestyle='dotted')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/channel{ch}_temperature{temp}.png', bbox_inches='tight')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/channel{ch}_temperature{temp}.svg', bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()

    '''fig, ax = plt.subplots()
    plt.ylabel('%s (mV)' %('Mean Maximum Voltage for Fit'))
    plt.xlabel('Channel')
    plt.title(r'Voltage vs Channel at {}$^\circ C$'.format(temp))
    plt.errorbar(channel, mean, yerr=mean_std, fmt='o', color='tomato', ms=5, label='Mean')
    ax.scatter(channel, median, label='Median')
    plt.ylim(26, 44)
    for i, n in enumerate(number):
        ax.annotate(n, (channel[i], median[i]), fontsize=9, xytext=(channel[i]-0.3, mean[i]- (mean_std[i]+1.5)))
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
    plt.grid(linestyle='dotted')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/Temperature{}.png'.format(temp), bbox_extra_artists=(lgd, ), bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/Temperature{}.svg'.format(temp), bbox_extra_artists=(lgd, ), bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    number = np.asarray(number)*100
    missingWF = number-waveforms
    fig, ax = plt.subplots()
    plt.ylabel('%s ' %('Missing Waveforms'))
    plt.xlabel('Channel')
    plt.title(r'Expected - Analyzed Waveforms at {}$^\circ C$'.format(temp))
    plt.ylim(1.1*min(missingWF)-20, 1.1*max(missingWF)+20)
    ax.scatter(channel, missingWF, label='Median')
    for i, n in enumerate(number):
        ax.annotate(int(n*0.01), (channel[i], missingWF[i]), fontsize=9, xytext=(channel[i]-0.2, missingWF[i]+10))
    plt.grid(linestyle='dotted')
    #plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/Temperature{}missingWF.png'.format(temp))
    #plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/Temperature{}missingWF.svg'.format(temp))
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()'''


def amplitude_vs_channel_cut(df, channel):
    mean = []
    mean_std = []
    median = []
    waveforms = []
    x_hist = []
    for i, ch in enumerate(channel):
        df_cut1 = df.loc[(df['Channel'] == ch)]
        mean.append(df_cut1['Maximum Voltage for Fit'].mean() * 1E3)
        mean_std.append(np.std(df_cut1['Maximum Voltage for Fit']) * 1E3)
        median.append(np.median(df_cut1['Maximum Voltage for Fit']) * 1E3)
        waveforms.append(len(df_cut1['Maximum Voltage for Fit']))

        m = np.mean(df_cut1['Maximum Voltage for Fit'])*1E3
        s = np.std(df_cut1['Maximum Voltage for Fit'])*1E3

        y_h, x_h, _ = plt.hist(df_cut1['Maximum Voltage for Fit']*1E3)
        plt.clf()
        plt.cla()
        plt.close()
        x_hist.append(x_h)
        '''dif = np.mean(df_cut1['Maximum Voltage for Fit']) - np.median(df_cut1['Maximum Voltage for Fit'])
        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title(f'Voltage Distribution ')
        plt.xlabel('Voltage for Fit (mV)')
        plt.ylabel('Waveforms')
        (n, bins, patches) = plt.hist(df_cut1['Maximum Voltage for Fit']*1E3, 10, stacked=True, alpha=0.35)
        #plt.fill_between(a, 0, y, y.max(), where = (a >= m - sigma_cut*s) & (a <= m + sigma_cut*s), color = 'g', alpha=0.25)
        #plt.fill_between(x, m - sigma_cut*s,  m + sigma_cut*s, color = 'g', alpha=0.25)
        plt.axvline(np.mean(df_cut1['Maximum Voltage for Fit'])*1E3, label='mean = {0:.2f}mV'.format(np.mean(df_cut1['Maximum Voltage for Fit'])*1E3))
        plt.axvline(np.median(df_cut1['Maximum Voltage for Fit'])*1E3, color='r', label='median = {0:.2f}mV \n mean-median = {1:.2f}mV'.format(np.median(df_cut1['Maximum Voltage for Fit'])*1E3, dif*1E3))
        #plt.axvline(m - sigma_cut*s, color='g')
        #plt.axvline(m + sigma_cut*s, color='g')
        fig.set_size_inches(12.5, 8.5, forward=True)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.grid(linestyle='dotted')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/channel{ch}_ALLTemp.png', bbox_inches='tight')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/channel{ch}_ALLTemp.svg', bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()'''
    return np.asarray(x_hist)

def amplitude_analysis(df, generate_plot):
    HV_Boards = np.unique(df.index.get_level_values('Board_ID'))
    Ideal_temperature = np.unique(df['Directory_temperature'])
    channel = np.unique(df['Channel'])

    #For all temperatures
    mean = []
    mean_std = []
    median = []
    number = []
    waveforms = []
    outlier_df = pd.DataFrame()
    non_outlier_df = pd.DataFrame()
    x_hist_values = amplitude_vs_channel_cut(df, channel)
    print(x_hist_values[0][-1])

    a = 8
    cut = sigma_cut
    for i, ch in enumerate(channel):
        df_cut1 = df.loc[(df['Channel'] == ch)]# & (df['Directory_temperature'] >= -30)]
        mean.append(df_cut1['Maximum Voltage for Fit'].mean() * 1E3)
        mean_std.append(np.std(df_cut1['Maximum Voltage for Fit']) * 1E3)
        median.append(np.median(df_cut1['Maximum Voltage for Fit']) * 1E3)
        number.append(len(np.unique(df_cut1.index.get_level_values('Board_ID'))))
        waveforms.append(len(df_cut1['Maximum Voltage for Fit']))
        if ch <= 4:
            cut_criteria_up = np.mean(df_cut1['Maximum Voltage for Fit'])*1E3 + cut * np.std(df_cut1['Maximum Voltage for Fit'])*1E3
            cut_criteria_low = np.mean(df_cut1['Maximum Voltage for Fit'])*1E3 - cut * np.std(df_cut1['Maximum Voltage for Fit'])*1E3
            #print('up:', cut_criteria_up, 'low:', cut_criteria_low)
            mask1 = df_cut1['Maximum Voltage for Fit']*1E3 > cut_criteria_up
            mask2 = df_cut1['Maximum Voltage for Fit']*1E3 < cut_criteria_low
            final_mask = np.logical_or(mask1, mask2)
            outlier = df_cut1.loc[final_mask]
            non_outlier = df_cut1.loc[~final_mask]
        else:
            cut_criteria_up = x_hist_values[i][-1]
            cut_criteria_low = x_hist_values[i][8]
            #print('up:', cut_criteria_up, 'low:', cut_criteria_low)
            mask3 = df_cut1['Maximum Voltage for Fit']*1E3 > cut_criteria_low
            outlier = df_cut1.loc[mask3]
            non_outlier = df_cut1.loc[~mask3]
        outlier_df = outlier_df.append(outlier)
        non_outlier_df = non_outlier_df.append(non_outlier)
        #print(number,'/n', waveforms)

    #highlight outliers in the plot

    x = df['Channel']
    y = df['Maximum Voltage for Fit']*1E3
    xr = outlier_df['Channel']
    yr = outlier_df['Maximum Voltage for Fit']*1E3
    #print(len(x), len(y))
    plt.ylabel('%s (mV)' %('Mean Maximum Voltage for Fit'))
    plt.xlabel('Channel')
    plt.title(r'Voltage vs Channel: All temperatures')
    #plt.ylim(27, 44)
    #plt.errorbar(channel, mean, yerr=mean_std, fmt='o', color='tomato', ms=5, label='Mean')
    plt.plot(x, y, 'o', ms=1, label='Individual Values')
    plt.plot(xr, yr, 'o', ms=1, label='outlier Values')
    plt.plot(channel, mean, 'o', label='Mean values')
    plt.plot(channel, median, 'o', label='Median')
    lgd = plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
    plt.grid(linestyle='dotted')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/Temperature_IndividualData.png', bbox_extra_artists=(lgd, ), bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/Temperature_IndividualData.svg', bbox_extra_artists=(lgd, ), bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()


    #For each temperature
    #for i in range(len(Ideal_temperature)):
    #    amplitude_vs_channel(df, Ideal_temperature[0], channel, number)

    '''
    for HV in HV_Boards:
        #histogram for fitting amplitudes for a given board at a given temperature
        try:
            temp_cut = 0
            sub1_df = df.loc[(df['Directory_temperature'] == temp_cut)]
            HVB_ch = np.unique(sub1_df.index.get_level_values('Board_ID'))
            counter = HV
            sub2_df = sub1_df.loc[counter]

            temp_cut2 = -45
            sub3_df = df.loc[(df['Directory_temperature'] == temp_cut2)]
            sub4_df = sub3_df.loc[counter]
            dif = np.median(sub2_df['Maximum Voltage for Fit']) - np.mean(sub2_df['Maximum Voltage for Fit'])
            dif2 = np.median(sub4_df['Maximum Voltage for Fit']) - np.mean(sub4_df['Maximum Voltage for Fit'])

            fig = plt.figure()
            ax = plt.subplot(111)
            plt.title(f'Voltage Distribution for {counter}')
            plt.xlabel('Voltage for Fit (mV)')
            plt.ylabel('Waveforms')
            plt.hist(sub2_df['Maximum Voltage for Fit']*1E3, 10, stacked=True, label=f'{temp_cut}${{^\circ}}$C', alpha=0.35)
            plt.hist(sub4_df['Maximum Voltage for Fit']*1E3, 10, stacked=True, label=f'{temp_cut2}${{^\circ}}$C', alpha=0.35)
            plt.axvline(np.mean(sub2_df['Maximum Voltage for Fit'])*1E3, color='r', label='mean at {0}°C = {1:.2f}mV \n mean-median = {2:.2f}mV'.format(temp_cut, np.mean(sub2_df['Maximum Voltage for Fit'])*1E3, dif*1E3))
            plt.axvline(np.mean(sub4_df['Maximum Voltage for Fit'])*1E3, label='mean at {0}°C = {1:.2f}mV \n mean-median = {2:.2f}mV'.format(temp_cut2, np.mean(sub4_df['Maximum Voltage for Fit'])*1E3, dif2*1E3))
            fig.set_size_inches(12.5, 8.5, forward=True)
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.grid(linestyle='dotted')
            plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/{counter}_Amplitude_hist.png', bbox_inches='tight')
            plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/{counter}_Amplitude_hist.svg', bbox_inches='tight')
            #plt.show()
            plt.clf()
            plt.cla()
            plt.close()


            dif = np.mean(sub2_df['Maximum Voltage for Fit']) - np.median(sub2_df['Maximum Voltage for Fit'])
            fig = plt.figure()
            ax = plt.subplot(111)
            plt.title(f'Voltage Distribution for {HV} ALL Temperatures')
            plt.xlabel('Voltage for Fit (mV)')
            plt.ylabel('Waveforms')
            plt.hist(sub2_df['Maximum Voltage for Fit']*1E3, 10, stacked=True, alpha=0.35)
            plt.axvline(np.mean(sub2_df['Maximum Voltage for Fit'])*1E3, color='r', label='mean = {0:.2f}mV \n mean-median = {1:.2f}mV'.format(np.mean(sub2_df['Maximum Voltage for Fit'])*1E3, dif*1E3))
            fig.set_size_inches(12.5, 8.5, forward=True)
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.grid(linestyle='dotted')
            plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/{HV}_Amplitude_hist_ALLTemperatures.png', bbox_inches='tight')
            plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/{HV}_Amplitude_hist_ALLTemperatures.svg', bbox_inches='tight')
            #plt.show()
            plt.clf()
            plt.cla()
            plt.close()

        except:
            pass'''


    if generate_plot == 1:
        fig, ax = plt.subplots()
        plt.ylabel('%s (mV)' %('Mean Maximum Voltage for Fit'))
        plt.xlabel('Channel')
        plt.title(r'Voltage vs Channel: All temperatures')
        plt.ylim(27, 44)
        plt.errorbar(channel, mean, yerr=mean_std, fmt='o', color='tomato', ms=5, label='Mean')
        ax.scatter(channel, median, label='Median')
        for i, n in enumerate(number):
            ax.annotate(n, (channel[i], median[i]), fontsize=9, xytext=(channel[i]-0.3, mean[i]- (mean_std[i]+1.5)))
        lgd = plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
        plt.grid(linestyle='dotted')
        #plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/Temperature.png', bbox_extra_artists=(lgd, ), bbox_inches='tight')
        #plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/Temperature.svg', bbox_extra_artists=(lgd, ), bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()

        number = np.asarray(number)*100*a
        missingWF = number-waveforms
        fig, ax = plt.subplots()
        plt.ylabel('%s ' %('Missing Waveforms'))
        plt.xlabel('Channel')
        plt.title(r'Expected - Analyzed Waveforms')
        plt.ylim(1.1*min(missingWF)-20, 1.1*max(missingWF)+20)
        ax.scatter(channel, missingWF, label='Median')
        for i, n in enumerate(number):
            ax.annotate(int(n/(100*a)), (channel[i], missingWF[i]), fontsize=9, xytext=(channel[i]-0.2, missingWF[i]+10))
        plt.grid(linestyle='dotted')
        plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/png/Temperature_missingWF.png', bbox_inches='tight')
        plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/Amplitude_analysis/svg/Temperature_missingWF.svg', bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()

    return outlier_df, non_outlier_df


def analysis_AlphaBeta(df, outlier_df, non_outlier_df):
    HV_Boards = np.unique(outlier_df.index.get_level_values('Board_ID'))
    HVB_outliers_df = pd.DataFrame()
    HV_Boards_non = np.unique(non_outlier_df.index.get_level_values('Board_ID'))
    HVB_non_outliers_df = pd.DataFrame()

    for num in HV_Boards:
        cut_df = df.loc[(df['Board_ID'] == num)]
        HVB_outliers_df = HVB_outliers_df.append(cut_df)

    for nume in HV_Boards_non:
        non_cut_df = df.loc[(df['Board_ID'] == nume)]
        HVB_non_outliers_df = HVB_non_outliers_df.append(non_cut_df)
    #print(HVB_outliers_df)

    alpha = df['Alpha']
    salpha = df['Error_Alpha']
    beta = df['Beta']*1E6
    sbeta = df['Error_Beta']*1E6
    channel = df['Channel']

    alpha_out = HVB_outliers_df['Alpha']
    salpha_out = HVB_outliers_df['Error_Alpha']
    beta_out = HVB_outliers_df['Beta']*1E6
    sbeta_out = HVB_outliers_df['Error_Beta']*1E6
    channel_out = HVB_outliers_df['Channel']

    alpha_non = HVB_non_outliers_df['Alpha']
    salpha_non = HVB_non_outliers_df['Error_Alpha']
    beta_non = HVB_non_outliers_df['Beta']*1E6
    sbeta_non = HVB_non_outliers_df['Error_Beta']*1E6
    channel_non = HVB_non_outliers_df['Channel']

    fig, (ax1, ax2) = plt.subplots(2, sharex = True)
    ax1.errorbar(channel, alpha, yerr=salpha, fmt='o', ms=5, label='All data')
    ax1.errorbar(channel_out, alpha_out, yerr=salpha_out, fmt='o', ms=5, label='Outliers')
    ax1.set(title='Alpha and Beta values vs Channel', ylabel=r'%s ' %('Alpha'))
    ax1.grid(linestyle='dotted')
    ax2.errorbar(channel, beta, yerr=sbeta, fmt='o', ms=5)
    ax2.errorbar(channel_out, beta_out, yerr=sbeta_out, fmt='o', ms=5)
    ax2.set(xlabel='Channel', ylabel=r'%s ($\mu$s)' %('Beta'))
    ax2.grid(linestyle='dotted')
    fig.set_size_inches(11,10)
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/png/AlphaBeta_Channel.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/svg/AlphaBeta_Channel.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for alpha
    plt.figure()
    plt.title(r'$\alpha$, where $\tau_{Droop}$ = $\alpha \cdot \tau_{Undershoot} + \beta$')
    plt.xlabel(r'$\alpha$ [dimensionless]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(alpha, 10, stacked=True, label=r'{} HVBs'.format(len(alpha)), alpha=0.35)
    plt.hist(alpha_out, 10, stacked=True, label=r'{} HVBs: Outliers$'.format(len(alpha_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/png/Alpha_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/svg/Alpha_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for beta
    plt.figure()
    plt.title(r'$\beta$ ,where $\tau_{Droop}$ = $\alpha \cdot \tau_{Undershoot} + \beta$')
    plt.xlabel(r'$\beta$ [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(beta, 10, stacked=True, label=r'{} HVBs'.format(len(beta)), alpha=0.35)
    plt.hist(beta_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(beta_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/png/Beta_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/svg/Beta_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for alpha without outliers
    plt.figure()
    plt.title(r'$\alpha$, where $\tau_{Droop}$ = $\alpha \cdot \tau_{Undershoot} + \beta$')
    plt.xlabel(r'$\alpha$ [dimensionless]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(alpha_non, 10, stacked=True, label=r'{} HVBs'.format(len(alpha)), alpha=0.35)
    #plt.hist(alpha_out, 10, stacked=True, label=r'{0} HVBs > {1}$\sigma$'.format(len(alpha_out), sigma_cut), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/png/Alpha_hist_non.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/svg/Alpha_hist_non.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for beta without outliers
    plt.figure()
    plt.title(r'$\beta$ ,where $\tau_{Droop}$ = $\alpha \cdot \tau_{Undershoot} + \beta$')
    plt.xlabel(r'$\beta$ [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(beta_non, 10, stacked=True, label=r'{} HVBs'.format(len(beta)), alpha=0.35)
    #plt.hist(beta_out, 10, stacked=True, label=r'{0} HVBs > {1}$\sigma$'.format(len(beta_out), sigma_cut), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/png/Beta_hist_non.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/AlphaBeta/svg/Beta_hist_non.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def analysis_p0p1p2(df, outlier_df):
    HV_Boards = np.unique(outlier_df.index.get_level_values('Board_ID'))
    HVB_outliers_df = pd.DataFrame()

    for num in HV_Boards:
        cut_df = df.loc[(df['Board_ID'] == num)]
        HVB_outliers_df = HVB_outliers_df.append(cut_df)

    p0 = df['p0']*1E6
    sp0 = df['Error_p0']*1E6
    p1 = df['p1']*1E6
    sp1 = df['Error_p1']*1E6
    p2 = df['p2']
    sp2 = df['Error_p2']
    channel = df['Channel']

    p0_out = HVB_outliers_df['p0']*1E6
    sp0_out = HVB_outliers_df['Error_p0']*1E6
    p1_out = HVB_outliers_df['p1']*1E6
    sp1_out = HVB_outliers_df['Error_p1']*1E6
    p2_out = HVB_outliers_df['p2']
    sp2_out = HVB_outliers_df['Error_p2']
    channel_out = HVB_outliers_df['Channel']

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex = True)
    ax1.errorbar(channel, p0, yerr=sp0, fmt='o', ms=5, label=r'All data')
    ax1.errorbar(channel_out, p0_out, yerr=sp0_out, fmt='o', ms=5, label=r'Outliers')
    ax1.set(title='p0, p1, p2 vs Channel', ylabel=r'%s ($\mu$s)' %('p0'))
    ax1.grid(linestyle='dotted')
    ax2.errorbar(channel, p1, yerr=sp1, fmt='o', ms=5)
    ax2.errorbar(channel_out, p1_out, yerr=sp1_out, fmt='o', ms=5)
    ax2.set(ylabel=r'%s ($\mu$s)' %('p1'))
    ax2.grid(linestyle='dotted')
    ax3.errorbar(channel, p2, yerr=sp2, fmt='o', ms=5)
    ax3.errorbar(channel_out, p2_out, yerr=sp2_out, fmt='o', ms=5)
    ax3.set(xlabel='Channel', ylabel=r'%s ($^\circ$C)' %('p1'))
    ax3.grid(linestyle='dotted')
    fig.legend(loc='upper right')
    fig.set_size_inches(12,10)
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/png/p0p1p2.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/svg/p0p1p2.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p0
    plt.figure()
    plt.title(r'$p_0$, where $\tau_{Droop} = p_0 + p_1/(1+e^{-T/p_2})$')
    plt.xlabel(r'$p_0$ [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p0, 10, stacked=True, label=r'{} HVBs'.format(len(p0)), alpha=0.35)
    plt.hist(p0_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(p0_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/png/p0_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/svg/p0_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p1
    plt.figure()
    plt.title(r'$p_1$, where $\tau_{Droop} = p_0 + p_1/(1+e^{-T/p_2})$')
    plt.xlabel(r'$p_1$  [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p1, 10, stacked=True, label=r'{} HVBs'.format(len(p1)), alpha=0.35)
    plt.hist(p1_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(p1_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/png/p1_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/svg/p1_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p2
    plt.figure()
    plt.title(r'$p_2$, where $\tau_{Droop} = p_0 + p_1/(1+e^{-T/p_2})$')
    plt.xlabel(r'$p_2$ [$^{\circ}$C]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p2, 10, stacked=True, label=r'{} HVBs'.format(len(p2)), alpha=0.35)
    plt.hist(p2_out, 10, stacked=True, label=r'{0} HVBs: Outliers'.format(len(p2_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/png/p2_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p0p1p2/svg/p2_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def analysis_p3p4p5(df, outlier_df):
    HV_Boards = np.unique(outlier_df.index.get_level_values('Board_ID'))
    HVB_outliers_df = pd.DataFrame()

    for num in HV_Boards:
        cut_df = df.loc[(df['Board_ID'] == num)]
        HVB_outliers_df = HVB_outliers_df.append(cut_df)

    p3 = df['p3']*1E6
    sp3 = df['Error_p3']*1E6
    p4 = df['p4']*1E6
    sp4 = df['Error_p4']*1E6
    p5 = df['p5']
    sp5 = df['Error_p5']
    channel = df['Channel']

    p3_out = HVB_outliers_df['p3']*1E6
    sp3_out = HVB_outliers_df['Error_p3']*1E6
    p4_out = HVB_outliers_df['p4']*1E6
    sp4_out = HVB_outliers_df['Error_p4']*1E6
    p5_out = HVB_outliers_df['p5']
    sp5_out = HVB_outliers_df['Error_p5']
    channel_out = HVB_outliers_df['Channel']

    fig, (ax1, ax2, ax3) = plt.subplots(3, sharex = True)
    ax1.errorbar(channel, p3, yerr=sp3, fmt='o', ms=5, label=r'All data')
    ax1.errorbar(channel_out, p3_out, yerr=sp3_out, fmt='o', ms=5, label=r'Outliers')
    ax1.set(title='p3, p4, p5 vs Channel', ylabel=r'%s ($\mu$s)' %('p3'))
    ax1.grid(linestyle='dotted')
    ax2.errorbar(channel, p4, yerr=sp4, fmt='o', ms=5)
    ax2.errorbar(channel_out, p4_out, yerr=sp4_out, fmt='o', ms=5)
    ax2.set(ylabel=r'%s ($\mu$s)' %('p4'))
    ax2.grid(linestyle='dotted')
    ax3.errorbar(channel, p5, yerr=sp5, fmt='o', ms=5)
    ax3.errorbar(channel_out, p5_out, yerr=sp5_out, fmt='o', ms=5)
    ax3.set(xlabel='Channel', ylabel=r'%s ($^\circ$C)' %('p5'))
    ax3.grid(linestyle='dotted')
    fig.legend(loc='upper right')
    fig.set_size_inches(12,10)
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/png/p3p4p5.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/svg/p3p4p5.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p3
    plt.figure()
    plt.title(r'$p_3$, where $\tau_{Undershoot} = p_3 + p_4/(1+e^{-T/p_5})$')
    plt.xlabel(r'$p_3$ [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p3, 10, stacked=True, label=r'{} HVBs'.format(len(p3)), alpha=0.35)
    plt.hist(p3_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(p3_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/png/p3_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/svg/p3_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p4
    plt.figure()
    plt.title(r'$p_4$, where $\tau_{Undershoot} = p_3 + p_4/(1+e^{-T/p_5})$')
    plt.xlabel(r'$p_4$ [$\mu$s]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p4, 10, stacked=True, label=r'{} HVBs'.format(len(p4)), alpha=0.35)
    plt.hist(p4_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(p4_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/png/p4_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/svg/p4_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    #Histogram for p5
    plt.figure()
    plt.title(r'$p_5$, where $\tau_{Undershoot} = p_3 + p_4/(1+e^{-T/p_5})$')
    plt.xlabel(r'$p_5$ [$^{\circ}$C]')
    plt.ylabel('High Voltage Boards (HVBs)')
    plt.hist(p5, 10, stacked=True, label=r'{} HVBs'.format(len(p5)), alpha=0.35)
    plt.hist(p5_out, 10, stacked=True, label=r'{} HVBs: Outliers'.format(len(p5_out)), alpha=0.35)
    plt.legend()
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/png/p5_hist.png', bbox_inches='tight')
    plt.savefig('/home/stephy/ICECUBE/undershoot/20200609/analysis/p3p4p5/svg/p5_hist.svg', bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def temp_HVB(df, df_outliers):
    channels = np.unique(df['Channel'])
    for ch in channels:
        df_cut = df.loc[(df['Channel'] == ch)]
        df_outliers_cut = df_outliers.loc[(df_outliers['Channel'] == ch)]
        HVB_num = df_cut.index.get_level_values('Board_ID')
        temperature = df_cut['Real_temperature']

        #plot for chi2_droop
        chi2_d = df_cut['chi2_droop']
        '''
        plt.scatter(HVB_num, temperature, c=chi2_d, s=100)
        cbar = plt.colorbar()
        plt.title(rf'$\chi ^2$ for channel {int(ch)}')
        plt.xlabel('High Voltage Board')
        plt.ylabel(r'Measured temperature ($^\circ$C)')
        cbar.set_label('$\chi ^2$')
        plt.clim(0.0004, 0.0012)
        plt.grid(linestyle='dotted')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/png/chi2_droop_channel{int(ch)}.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/svg/chi2_droop_channel{int(ch)}.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        '''

        #plot for chi2_droop
        chi2_u = df_cut['chi2_undershoot']
        '''
        plt.scatter(HVB_num, temperature, c=chi2_u, s=100)
        cbar = plt.colorbar()
        plt.title(rf'$\chi ^2$ for channel {int(ch)}')
        plt.xlabel('High Voltage Board')
        plt.ylabel(r'Measured temperature ($^\circ$C)')
        cbar.set_label('$\chi ^2$')
        plt.clim(0.004, 0.012)
        plt.grid(linestyle='dotted')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/png/chi2_undershoot_channel{int(ch)}.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
        plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/svg/chi2_undershoot_channel{int(ch)}.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
        #plt.show()
        plt.clf()
        plt.cla()
        plt.close()
        '''

        #plot for droop/undershoot
        droop = df_cut['Tau_droop']
        undershoot = df_cut['Tau_undershoot']
        D_U = droop/undershoot

        droop_out = df_outliers_cut['Tau_droop']
        undershoot_out = df_outliers_cut['Tau_undershoot']
        D_U_out = droop_out/undershoot_out

    plt.title(f'Ratio Droop/Undershoot for channel {int(ch)}')
    plt.xlabel('Ratio Droop/Undershoot')
    plt.ylabel('Waveforms')
    plt.xlim(0.85, 1.15)
    plt.hist(D_U, 10, stacked=True, label=f'{ch} HVBs', alpha=0.35)
    plt.hist(D_U_out, 10, stacked=True, label=f'{ch} HVBs', alpha=0.35)
    plt.grid(linestyle='dotted')
    plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/png/hist_DroopUndershoot_channel.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/svg/hist_DroopUndershoot_channel.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()

    '''
    plt.scatter(HVB_num, temperature, c=D_U, s=100)
    cbar = plt.colorbar()
    plt.title(rf'Ratio Droop/Undershoot for channel {int(ch)}')
    plt.xlabel('High Voltage Board')
    plt.ylabel(r'Measured temperature ($^\circ$C)')
    cbar.set_label('Ratio Droop/Undershoot')
    plt.clim(0.85, 1.15)
    plt.grid(linestyle='dotted')
    plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/png/ratio_DroopUndershoot_channel{int(ch)}.png')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    plt.savefig(f'/home/stephy/ICECUBE/undershoot/20200609/analysis/temp_HVB/svg/ratio_DroopUndershoot_channel{int(ch)}.svg')#, bbox_extra_artists=(lgd, ))#, bbox_inches='tight')
    #plt.show()
    plt.clf()
    plt.cla()
    plt.close()
    '''


def remove_weird_fits(df, err_threshs=[10, 10, 10, 10, 10, 10]):
    masks = []
    for i, err_thresh in enumerate(err_threshs):
        mask = df[f'Error_p{i}'] > err_thresh
        masks.append(mask)
    final_mask = np.logical_or(masks[0], masks[1])
    final_mask = np.logical_or(final_mask, masks[2])
    final_mask = np.logical_or(final_mask, masks[3])
    final_mask = np.logical_or(final_mask, masks[4])
    final_mask = np.logical_or(final_mask, masks[5])
    print('Removed the following entries from the dataframe due to irregular ',
          'fit errors!',
          df.loc[final_mask])
    return df.loc[~final_mask], df.loc[final_mask]


def main():
    droop_undershoot_file = '/home/stephy/ICECUBE/undershoot/20200609/Results_droop_undershoot.h5'
    df = load_dataframe(droop_undershoot_file)

    outliers_df, non_outlier_df = amplitude_analysis(df, 0)#To generate plots use 1
    #temp_HVB(df, outliers_df)
    print(np.unique(outliers_df.index.get_level_values('Board_ID')))

    '''temperature_file = '/home/stephy/ICECUBE/undershoot/20200609/Results_DroopUndershootTemperature.h5'
    df_temp = load_dataframe(temperature_file)
    df_temp, df_weird = remove_weird_fits(df_temp)
    analysis_AlphaBeta(df_temp, outliers_df, non_outlier_df)
    analysis_p0p1p2(df_temp, outliers_df)
    analysis_p3p4p5(df_temp, outliers_df)'''


if __name__ == "__main__":
    plt.rcParams.update({'font.size': 14})
    global sigma_cut
    sigma_cut = 2.5
    main()
