import warnings
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from scipy.interpolate import interp1d
import seaborn as sns
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

def main(data_input,bin_side,bin_period,bin_center=None,bin_FUN='mean',bin_max_f_NA=0.2,SCI_min=0.6,coeff_outlier='auto',ylim=(float('-inf'),float('inf'))):
    """
    The goal of ctbi is to clean, decompose, impute and aggregate univariate time series. ctbi stands for Cyclic/Trend decomposition using Bin Interpolation: the time series is divided into a sequence of non-overlapping bins (inputs: bin_side or bin_center, and bin_period). Bins with enough data (input: bin_max_f_NA) are accepted, and otherwise rejected (their values are set to NA). The long-term trend is a linear interpolation of the mean values between successive bins. The cyclic component is the mean stack of detrended data within all accepted bins.

    Outliers present in the residuals are flagged using an enhanced box plot rule (called Logbox, input: coeff_outlier) that is adapted to non-Gaussian data and keeps the type I error at 0.1/sqrt(n) % (percentage of erroneously flagged outliers). Logbox replaces the original alpha = 1.5 constant of the box plot rule with alpha = A times log(n)+B+C/n. The variable n geq 9 is the sample size, C = 36 corrects biases emerging in small samples, and A and B are automatically calculated on a predictor of the maximum tail weight m*).

    The strength of the cyclic pattern within each bin is quantified by a new metric, the Stacked Cycles Index defined as eqn SCI = 1 - SS_res/SS_tot - 1/N_bin. The variable eqn SS_tot is the sum of the squared detrended data, eqn SS_res is the sum of the squared detrended & deseasonalized data, and eqn N_bin is the number of accepted bins. A value of eqn SCI leq 0 is associated  with no cyclicity, while SCI = 1 is associated with a perfectly cyclic signal. Data can be imputed if eqn SCI_min leq SCI (input: SCI_min). Finally, data are aggregated in each bin (input: bin_FUN).

    Important functions of the package: ctbi, outlier (flag outliers in univariate datasets with the Logbox method) and plot (plot the time series).
    
    Arguments :
    - data_input : two columns data frame with the first column being the time component (datetime or numeric) and the second column the value (numeric)
    - bin_side : one side of any bin (same class as the time component)
    - bin_center : if bin_side is not specified, one center of a bin (same class as the time component)
    - bin_period : time interval between two sides of a bin. If the time component x_t of data_input is numeric, bin_period is numeric. If x_t is datetime, bin_period = 'k units', with k an integer and units = (seconds, minutes, hours, days, weeks, half-months, months, years, decades, centuries, millenaries)
    - bin_FUN : character ('mean', 'median' or 'sum') that defines the aggregating operator
    - bin_max_f_NA : numeric between 0 and 1 that specifies the maximum fraction of missing values for a bin to be accepted. The minimum number of non-NA points for a bin to be accepted is bin_size_min_accepted = bin_size*(1-bin_max_f_NA) with bin_size the number of points per bin
    - SCI_min : numeric between 0 and 1 that is compared to the Stacked Cycles Index (SCI). If SCI > SCI_min, missing values are imputed in accepted bins with the sum of the long-term and cyclic components. If SCI_min = NA, no values are imputed
    - coeff_outlier : one of coeff_outlier = 'auto' (default value), coeff_outlier = 'gaussian', coeff_outlier = c(A,B,C) or coeff_outlier = None. If coeff_outlier = 'auto', C = 36 and the coefficients A and B are calculated on m*. If coeff_outlier = 'gaussian', coeff_outlier = c(0.08,2,36), adapted to the Gaussian distribution. If coeff_outlier = None, no outliers are flagged
    - ylim : numeric vector of length 2 that defines the range of possible values. Values strictly below ylim[0] or strictly above ylim[1] are set to NA. Values equal to ylim[0] or ylim[1] are discarded from the residuals

    Returns :
    - out_main, a list that contains: 
      - data0, the raw dataset (same class as data_input), with 9 columns: (i) time; (ii) outlier-free and imputed data; (iii) index_bin: index of the bins associated with each data points (the index is negative if the bin is rejected); (iv) long_term: long-term trend; (v) cycle: cyclic component; (vi) residuals: residuals including the outliers; (vii) outliers: quarantined outliers; (viii) imputed: value of the imputed data points; (ix) time_bin: relative position of the data points in their bins, between 0 and 1
      - data1, the aggregated dataset (same class as data_input), with 10 columns: (i) aggregated time (center of the bins); (ii) aggregated data; (iii) index_bin: index of the bin (negative value if the bin is rejected); (iv) bin_start: start of the bin; (v) bin_end: end of the bin; (vi) n_points: number of points per bin (including NA values); (vii) n_NA: number of NA values per bin, originally; (viii) n_outliers: number of outliers per bin; (ix) n_imputed: number of imputed points per bin; (x) variability associated with the aggregation (standard deviation for the mean, MAD for the median and nothing for the sum)
      - mean_cycle, a dataset (same class as data_input) with bin_size rows and 4 columns: (i) generic_time_bin1: time of the first bin; (ii) mean: the mean stack of detrended data; (iii) sd: the standard deviation on the mean; (iv) time_bin: relative position of the data points in the bin, between 0 and 1
      - summary_bin, a vector that contains bin_size (median number of points in non-empty bins), bin_size_min_accepted (minimum number of points for a bin to be accepted) and SCI
      - summary_outlier, a vector that contains A, B, C, m*, the size of the residuals (n), and the lower and upper outlier threshold

    """
    
    # Check data_input
    char_format = "data_input is a two columns DataFrame with the first column being the time series (numeric or datetime) and the second column the variable to be temporally aggregated (numeric)."

    if data_input is None:
        raise ValueError(char_format)
    elif not isinstance(data_input, pd.DataFrame):
        raise ValueError("data_input is not a DataFrame")
    elif data_input.shape[1] != 2:
        raise ValueError(char_format)
    elif not (pd.api.types.is_numeric_dtype(data_input.iloc[:, 0]) or pd.api.types.is_datetime64_dtype(data_input.iloc[:, 0])):
        raise ValueError("The first column being the time series (numeric or datetime).")
    elif not pd.api.types.is_numeric_dtype(data_input.iloc[:, 1]):
        raise ValueError("The second column the variable to be temporally aggregated (numeric).")

    # Check bin_side and bin_center
    if bin_side is None and bin_center is None: 
        raise ValueError("bin_side (or bin_center) is a mandatory input. It has the same class as the time component and corresponds to one side of any bin.")

    # Check bin_period
    if bin_period is None:
        raise ValueError("bin_period is a mandatory input. It is the time interval between two sides of a bin. If x_t the time component of data_input is numeric, bin_period is numeric. If x_t the time component of data_input is datetime, bin_period = \'k units\', with k a numeric and units = (seconds, minutes, hours, days, weeks, half-months, months, years, decades, centuries, millenaries)")

    # Check bin_max_f_NA
    char_frac_NA = "bin_max_f_NA is a numeric between 0 and 1 and corresponds to the maximum fraction of NA values accepted in a bin (otherwise the bin is rejected)."
    if isinstance(bin_max_f_NA, (int, float)):
        if bin_max_f_NA < 0 or bin_max_f_NA > 1:
            raise ValueError(char_frac_NA)
    else:
        raise ValueError(char_frac_NA)

    # Check ylim
    char_ylim = "ylim is the range of possible values with the default being ylim=c(-Inf,Inf). Example: ylim=c(0,Inf) for a precipitation dataset (important for the imputation process)."

    if len(ylim) == 2:
        if ylim[0] > ylim[1]:
            raise ValueError(char_ylim)
    else:
        raise ValueError(char_ylim)

    # Check bin_FUN    
    char_bin_FUN = "bin_FUN is one of 'mean', 'median' or 'sum' to perform the temporal aggregation."
    if not isinstance(bin_FUN, str):
        raise ValueError(char_bin_FUN)
    if bin_FUN not in ['mean', 'sum', 'median']:
        raise ValueError(char_bin_FUN)

    # Check SCI_min
    char_cycle = "SCI_min is a value between 0 and 1 that is compared to the Stacked Cycles Index (impute if SCI > SCI_min). If SCI = NA, no imputation is performed."

    if not pd.isnull(SCI_min):
        if not np.isinf(SCI_min):
            if isinstance(SCI_min, (int, float)):
                if SCI_min < 0 or SCI_min > 1:
                    raise ValueError(char_cycle)
            else:
                raise TypeError(char_cycle)
        else:
            raise TypeError(char_cycle)
    else:
        SCI_min = np.inf

    # Check coeff_outliers
    char_coeff_outlier = "'coeff_outlier' is one of 'auto' (default value), 'gaussian', (A,B,C) or NA. If 'coeff_outlier' = 'auto', C = 36 and the coefficients A and B are calculated on 'm_star', a predictor of the kurtosis excess. If 'coeff_outlier' = 'gaussian', 'coeff_outlier' = [0.08, 2, 36], adapted to the Gaussian distribution. If 'coeff_outlier' = NA, no outliers are flagged."

    if coeff_outlier is not None:
        if isinstance(coeff_outlier, str):
            if coeff_outlier != 'auto' and coeff_outlier != 'gaussian':
                raise ValueError(char_coeff_outlier)

        else:
            if len(coeff_outlier) == 3:
                if not all(isinstance(i, (int, float)) for i in coeff_outlier):
                    raise ValueError(char_coeff_outlier)
                else:
                    if np.count_nonzero(coeff_outlier) == 0:
                        coeff_outlier = None
                    else:
                        coeff_outlier = tuple(0 if x is None else x for x in coeff_outlier)
            else:
                raise ValueError(char_coeff_outlier)
    
    data_input_names = data_input.columns
    # Change dataframe name and colnames 
    data0 = data_input
    data0.columns = ['x', 'y']

    # Force the numeric class of y
    data0['y'] = pd.to_numeric(data0['y'])

    # Calculate the sequence of bin_side and bin_center
    out = timeseries(x_t=data0['x'],bin_period=bin_period,bin_side=bin_side,bin_center=bin_center)
    seq_bin_side = out.seq_bin_side_
    seq_bin_center = out.seq_bin_center_
    time_step_median = out.time_step_median_

    # Calculate the number of bins, N_bin_tot
    N_bin_tot = len(seq_bin_center)

    # Find the intervals for the seq_bin_side,seq_bin_center, and add extra columns outliers & imputed
    data0['index_bin'] = np.searchsorted(seq_bin_side, data0['x'], side='right') - 1
    data0['side_index'] = np.searchsorted(seq_bin_center, data0['x'], side='right') - 0.5
    data0['outliers'] = np.full(len(data0['y']), np.nan)
    data0['imputed'] = np.full(len(data0['y']), np.nan)

    # Create the aggregated dataset, data1
    counts = data0.groupby('index_bin')['x'].count().reset_index()
    counts = counts.rename(columns={'x': 'n_points'})
    indices = pd.DataFrame({'index_bin': range(0, N_bin_tot)})
    data1 = pd.merge(counts, indices, on='index_bin', how='outer').sort_values('index_bin').reset_index(drop=True)
    data1.loc[data1['n_points'].isna(), 'n_points'] = 0

    # Calculate the median number of points per bin, bin_size
    bin_size = data1['n_points'].values
    bin_size = bin_size[bin_size != 0]

    if len(bin_size) <= 4:
        bin_size = int(round(max(bin_size), 0))
    else:
        bin_size = int(round(np.median(bin_size), 0))

    if bin_size == 1:
        raise ValueError('The bin_period is too low (bin_size of 1).')

    # Calculate the minimum number of points for a bin to be accepted, n_bin_min
    n_bin_min = int(np.ceil(bin_size * (1 - bin_max_f_NA)))
    if n_bin_min < 1:
        n_bin_min = 1

    # Add columns to data1: bin_center, bin_start, bin_end and the number of NA values per bin
    data1 = pd.merge(data1, data0.groupby('index_bin')['y'].apply(lambda x: np.sum(pd.isna(x))), on='index_bin', how='outer')
    data1 = data1.rename(columns={'y': 'n_NA'})
    data1.loc[data1['n_NA'].isna(), 'n_NA'] = 0
    data1['bin_center'] = seq_bin_center
    data1['bin_start'] = seq_bin_side[:len(seq_bin_side)-1]
    data1['bin_end'] = seq_bin_side[1:]

    # Calculate the relative position of the values with respect to their bin.
    data0['time_bin'] = data0.apply(lambda row: hidd_rel_time(data0.loc[(data0['index_bin'] == row['index_bin']) & (data0['x'] >= row['x']), 'x'].reset_index(drop=True), seq_bin_side), axis=1)

    all_mins = data0.groupby('index_bin')['time_bin'].min().reset_index()

    if all_mins.shape[0] > 4:
        shift_min = (1 / (2 * bin_size)) - np.median(all_mins['time_bin'])
    else:
        shift_min = (1 / (2 * bin_size)) - np.min(all_mins['time_bin'])

    data0['time_bin'] = data0['time_bin'] + shift_min
    data0['cycle_index'] = np.searchsorted(np.arange(1, bin_size) / bin_size, data0['time_bin']) + 1

    # Step 0 : remove errors
    data0.loc[np.isinf(data0['y']) | (data0['y'] < ylim[0]) | (data0['y'] > ylim[1]), 'outliers'] = data0['y']
    data0.loc[np.isinf(data0['y']) | (data0['y'] < ylim[0]) | (data0['y'] > ylim[1]), 'y'] = np.nan

    # Step 1 : replace bins with insufficient data with NA values
    data0.loc[data0['index_bin'].isin(data1.loc[(data1['n_points'] - data1['n_NA']) < n_bin_min, 'index_bin'].values), 'y'] = np.nan

    # Step 2 : calculate the long_term trend with the median
    data0 = long_term(data0,n_bin_min,seq_bin_side,outliers_checked=False)

    # Step 3 : calculate the median cycle
    list_cycle = cycle(data0,bin_size,outliers_checked=False)
    data0 = list_cycle.data0_l

    # Step 4 : calculate the outliers
    data0['residuals'] = data0['y'] - data0['long_term'] - data0['cycle'] # residuals
    # Residuals that exactly fall on ylim are discarded
    data0.loc[(data0['residuals'] == ylim[0]) | (data0['residuals'] == ylim[1]), 'residuals'] = np.nan

    list_out = outlier(data0['residuals'],coeff_outlier)
    data0['residuals'] = list_out.xy_l['outliers']
    data0.loc[~np.isnan(data0['residuals']),'outliers'] = data0.loc[~np.isnan(data0['residuals']),'y']
    data0.loc[~np.isnan(data0['outliers']),'y'] = np.nan # Update y values
    data0.drop('residuals', axis=1, inplace=True) # Remove the column residuals
    summary_outlier = list_out.summary_xy_l # Contains A_coeff,B_coeff,C_coeff,m_star,n_residuals,lower_outlier_threshold and upper_outlier_threshold

    # Repeat steps 1,2,3 with the mean
    data0['y'] = np.where(data0['index_bin'].isin(data1.loc[(data1['n_points'] - data1['n_NA']) < n_bin_min, 'index_bin'].values), np.nan, data0['y'])

    data0 = long_term(data0,n_bin_min,seq_bin_side,outliers_checked=True)

    list_cycle = cycle(data0,bin_size,outliers_checked=True)
    data0 = list_cycle.data0_l
    mean_cycle = list_cycle.FUN_cycle_l

    # Change bin sign for rejected bins
    data0['index_bin']=data0['index_bin']+1
    data0['side_index']=data0['side_index']+1
    data1['index_bin']=data1['index_bin']+1
    data0['bin_accepted']=data0['index_bin']
    data0['bin_accepted'] = np.where(data0['index_bin'].isin(data1.loc[(data1['n_points'] - data1['n_NA']) < n_bin_min, 'index_bin'].values), -data0['index_bin'], data0['bin_accepted'])

    # Calculate SCI
    N_bin_accepted = np.unique(data0['bin_accepted'])
    N_bin_accepted = len(N_bin_accepted[N_bin_accepted > 0])
    if N_bin_accepted > 2:
        SS_tot = np.sum(np.square(data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'y'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'long_term']), axis=0)
        SS_res = np.sum(np.square(data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'y'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'long_term'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'cycle']), axis=0)

        if SS_tot != 0:
            SCI = round(1 - (SS_res/SS_tot) - (1/N_bin_accepted), 3)

            # Impute data
            if SCI >= SCI_min:
                data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].isna()),'imputed'] = data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].isna()),'long_term'] + data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].isna()),'cycle']
                # Some imputed values might be impossible
                data0.loc[data0['imputed'] <= ylim[0],'imputed'] = ylim[0]
                data0.loc[data0['imputed'] >= ylim[1],'imputed'] = ylim[1]
                data0.loc[data0['imputed'].notna(),'y'] = data0.loc[data0['imputed'].notna(),'imputed']

                for i in range(1,3): # Repeat twice
                    # The cycle + long_term need to be recalculated.
                    data0 = long_term(data0,n_bin_min,seq_bin_side,outliers_checked=True)

                    list_cycle = cycle(data0,bin_size,outliers_checked=True)
                    data0 = list_cycle.data0_l
                    mean_cycle = list_cycle.FUN_cycle_l

                    data0.loc[data0['imputed'].notna(),'imputed'] = data0.loc[data0['imputed'].notna(),'long_term'] + data0.loc[data0['imputed'].notna(),'cycle']
                    # Some imputed values might be impossible
                    data0.loc[data0['imputed'] <= ylim[0],'imputed'] = ylim[0]
                    data0.loc[data0['imputed'] >= ylim[1],'imputed'] = ylim[1]
                    data0.loc[data0['imputed'].notna(),'y'] = data0.loc[data0['imputed'].notna(),'imputed']

                # Recalculate SCI
                SS_tot = np.sum(np.square(data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'y'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'long_term']), axis=0)
                SS_res = np.sum(np.square(data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'y'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'long_term'] - data0.loc[(data0['bin_accepted'] > 0) & (data0['y'].notna()) & (data0['long_term'].notna()), 'cycle']), axis=0)
                SCI = round(1 - (SS_res/SS_tot) - (1/N_bin_accepted), 3)
        else:
            SCI = np.nan
    else:
        SCI = np.nan

    # Add columns to data1: n_imputed and n_outliers
    data1 = pd.merge(data1, data0.groupby('index_bin')['imputed'].apply(lambda x: np.sum(pd.notna(x))), on='index_bin', how='outer')
    data1 = data1.rename(columns={'imputed': 'n_imputed'})
    data1 = pd.merge(data1, data0.groupby('index_bin')['outliers'].apply(lambda x: np.sum(pd.notna(x))), on='index_bin', how='outer')
    data1 = data1.rename(columns={'outliers': 'n_outliers'})
    data1.loc[pd.isna(data1['n_imputed']),'n_imputed'] = 0
    data1.loc[pd.isna(data1['n_outliers']),'n_outliers'] = 0

    if bin_FUN == 'mean':
        compute_std = pd.DataFrame(data0.groupby('index_bin')['y'].std()).reset_index()
        compute_std = compute_std.rename(columns={'y': 'sd_' + data_input_names[1]})
        compute_mean = pd.DataFrame(data0.groupby('index_bin')['y'].mean()).reset_index()
        data1 = pd.merge(data1, compute_std, on='index_bin', how='outer')
        data1 = pd.merge(data1, compute_mean, on='index_bin', how='outer')
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'sd_' + data_input_names[1]] = np.nan
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'y'] = np.nan
        add_char = 'sd_' + data_input_names[1]

    if bin_FUN == 'median':
        data0['absolute_deviation'] = 1.4826 * np.abs(data0['y'] - data0.groupby('index_bin')['y'].transform(lambda x: np.nanmedian(x)))
        compute_mad = pd.DataFrame(data0.groupby('index_bin')['absolute_deviation'].median()).reset_index()
        compute_mad = compute_mad.rename(columns={'absolute_deviation': 'mad_' + data_input_names[1]})
        compute_median = pd.DataFrame(data0.groupby('index_bin')['y'].median()).reset_index()
        data1 = pd.merge(data1, compute_mad, on='index_bin', how='outer')
        data1 = pd.merge(data1, compute_median, on='index_bin', how='outer')
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'mad_' + data_input_names[1]] = np.nan
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'y'] = np.nan
        data0 = data0.drop(columns={'absolute_deviation'})
        add_char = 'mad_' + data_input_names[1]

    if bin_FUN == 'sum':
        compute_mean = pd.DataFrame(data0.groupby('index_bin')['y'].mean()).reset_index()
        compute_mean = compute_mean.rename(columns={'y': 'mean_y'})
        compute_sum = pd.DataFrame(data0.groupby('index_bin')['y'].sum(min_count=1)).reset_index()
        data1 = pd.merge(data1, compute_mean, on='index_bin', how='outer')
        data1 = pd.merge(data1, compute_sum, on='index_bin', how='outer')
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'mean_y'] = np.nan
        data1.loc[data1['n_points'] - (data1['n_NA']+data1['n_imputed']+data1['n_outliers']) < n_bin_min, 'y'] = np.nan
        data1.loc[data1['mean_y'].notna(),'y'] = data1['y'] + data1['n_NA'] * data1['mean_y'] + data1['n_outliers'] * data1['mean_y']
        data1 = data1.drop(columns={'mean_y'})
        add_char = None

    # Change sign of the bins that have been rejected
    data1.loc[data1['y'].isna(),'index_bin'] = -data1['index_bin']

    # Put back the raw data, remove the outliers, add the imputed data, remove useless columns and add the residuals.
    data0['y'] = data_input.iloc[:,1]
    data0['residuals'] = data0['y'] - data0['long_term'] - data0['cycle']
    data0.loc[data0['outliers'].notna(),'y'] = np.nan
    data0.loc[data0['imputed'].notna(),'y'] = data0['imputed']
    data0['index_bin'] = data0['bin_accepted']
    data0 = data0.drop(columns=['bin_accepted','cycle_index','side_index'])
    data0.loc[(data0['y']==ylim[0]) | (data0['y']==ylim[1]),'residuals'] = np.nan

    # The long_term, cycle and residuals components are NA for rejected bins
    data0.loc[data0['index_bin'] < 0,'long_term'] = np.nan
    data0.loc[data0['index_bin'] < 0,'cycle'] = np.nan
    data0.loc[data0['index_bin'] < 0,'residuals'] = np.nan

    # Add the time step of the mean_cycle based on the first bin
    if data0['x'].dtype == 'datetime64[ns]':
        epsilon = ((1/(2*bin_size))-shift_min)*(seq_bin_side[1]-seq_bin_side[0]).total_seconds()
        t_cycle = hidd_seq(start = seq_bin_side[0]+timedelta(seconds=epsilon), end = seq_bin_side[1]+timedelta(seconds=epsilon)-time_step_median*1000000000, length_out = bin_size)
    else:
        epsilon = ((1/(2*bin_size))-shift_min)*(seq_bin_side[1]-seq_bin_side[0])
        t_cycle = hidd_seq(start = seq_bin_side[0]+epsilon, end = seq_bin_side[1]+epsilon-time_step_median, length_out = bin_size)

    t_bin = np.arange(1, bin_size + 1) / bin_size - 1 / (2 * bin_size)
    mean_cycle['generic_time_bin1'] = t_cycle
    mean_cycle['time_bin'] = t_bin
    mean_cycle = mean_cycle.drop(columns=['cycle_index'])
    mean_cycle = mean_cycle[["generic_time_bin1","mean","sd","time_bin"]] 

    summary_bin = pd.Series([bin_size, n_bin_min, SCI], index=['bin_size', 'bin_size_min_accepted', 'SCI'])
    
    # Rearrange columns and column names

    data0 = data0.rename(columns={'x': data_input_names[0]})
    data1 = data1.rename(columns={'bin_center': data_input_names[0]})
    data0 = data0.rename(columns={'y': data_input_names[1]})
    data1 = data1.rename(columns={'y': data_input_names[1]})
    data0 = data0[[data_input_names[0],data_input_names[1],'index_bin','long_term','cycle','residuals','outliers','imputed','time_bin']]

    if bin_FUN == 'sum':
        data1 = data1[[data_input_names[0],data_input_names[1],'bin_start','bin_end','index_bin','n_points','n_NA','n_imputed','n_outliers']]
    else:
        data1 = data1[[data_input_names[0],data_input_names[1],'bin_start','bin_end','index_bin','n_points','n_NA','n_imputed','n_outliers',add_char]]  

    data0_ = data0
    data1_ = data1
    mean_cycle_ = mean_cycle
    summary_bin_ = summary_bin
    summary_outlier_ = summary_outlier

    class Def_Return:
            data0 = data0_
            data1 = data1_
            mean_cycle = mean_cycle_
            summary_bin = summary_bin_
            summary_outlier = summary_outlier_

    out_main = Def_Return()

    return out_main
    
def cycle(data0,bin_size,outliers_checked):
    """
    Calculate the mean (or median) stack of the detrended data for all bins, and add the cyclic component column to data0.
    
    Arguments :
    - data0 : a data frame with the columns x (time series), y (values), time_bin (position of x between 0 and 1 with respect to the bin boundaries), cycle_index (index between 1 and bin_size attached to time_bin), and long_term (the long-term trend)
    - bin_size : median number of points within all non-empty bins
    - outliers_checked : boolean to indicate if the median (outliers_checked = False) or the mean (outliers_checked = True) should be used to calculate the stack
    
    Returns :
    - list_all, a list that contains: 
      - data0_l
      - FUN_cycle_l, dataframe that contains the mean (or median) stack of all accepted bins
    """
    
    data0['detrended'] = data0['y']-data0['long_term']

    if data0['detrended'].notna().sum() != 0:
        if outliers_checked == False:
            FUN_cycle = data0.groupby('cycle_index')['detrended'].median()         
        else:
            FUN_cycle = data0.groupby('cycle_index')['detrended'].mean() 

        std_cycle = data0.groupby('cycle_index')['detrended'].std()
        FUN_cycle = pd.DataFrame(FUN_cycle).reset_index().merge(pd.DataFrame(std_cycle).reset_index(), on="cycle_index")

        if outliers_checked == False:
            FUN_cycle.columns = ['cycle_index', 'median', 'sd']        
        else:
            FUN_cycle.columns = ['cycle_index', 'mean', 'sd']

        # some NA values in the mean_cycle can be linearly interpolated.
        y_int = np.concatenate([FUN_cycle.iloc[:, 1].values] * 3)

        if FUN_cycle.iloc[:, 1].notna().sum() != 0:
            x = np.arange(1, len(y_int) + 1)
            f = interp1d(x, y_int, kind='linear')
            yapp = f(np.arange(1, len(y_int) + 1))
            y_int = yapp
            FUN_cycle.iloc[:, 1] = y_int[bin_size:2*bin_size]

        y_int = y_int[bin_size-1:(2*bin_size+1)]
        x_int = np.concatenate(([(-1/(2*bin_size))], np.arange(1, bin_size+1) / bin_size - (1/(2*bin_size)), [1+1/(2*bin_size)]))

        # remove the mean value of the mean cycle and add it to the long_term
        mean_int = np.nanmean(FUN_cycle.iloc[:,1])
        FUN_cycle.iloc[:,1] = FUN_cycle.iloc[:,1] - mean_int
        y_int = y_int - mean_int
        data0['long_term'] = data0['long_term'] + mean_int

        f = interp1d(x=x_int, y=y_int, kind='linear')
        data0['cycle'] = f(np.array(data0['time_bin']).flatten())

    else:
        data0['cycle'] = np.nan

        if outliers_checked == False:
            FUN_cycle = pd.DataFrame({'cycle_index': range(1, bin_size+1),'median': [np.nan]*bin_size,'sd': [np.nan]*bin_size})
        else:
            FUN_cycle = pd.DataFrame({'cycle_index': range(1, bin_size+1),'mean': [np.nan]*bin_size,'sd': [np.nan]*bin_size})

    data0 = data0.drop('detrended', axis=1)
    
    class Def_Return:
        data0_l = data0
        FUN_cycle_l = FUN_cycle

    list_all = Def_Return()
    
    return list_all     

def long_term(data0,n_bin_min,seq_bin_side,outliers_checked):
    """
    Calculate the long-term trend with a linear interpolation between the mean (or median) of bins defined between two consecutive centers. Bins defined between two consecutive sides are calculated as well to complete for missing values if they have neighbors. Bins without sufficient data are discarded.
    
    Arguments :
    - data0 : a data frame with the columns x (time series), y (values), side_index (index associated with each bin defined between two consecutive centers) and index_bin (index associated with each bin defined between two consecutive sides)
    - n_bin_min : minimum number of points for a bin to be accepted
    - seq_bin_side : sequence of the sides of the bins
    - outliers_checked : boolean to indicate if the median (outliers_checked = FALSE) or the mean (outliers_checked = TRUE) should be used to calculate the long-term trend

    Returns :
    - data0, with the long-term trend added (column long_term)
    """
    N_bin_tot = max(data0['index_bin'])
    count_y_side_index = data0.groupby('side_index')['y'].count().reset_index()
    count_y_center_index = data0.groupby('index_bin')['y'].count().reset_index()
    
    if outliers_checked == False:

        side_dt = data0.groupby('side_index')['y'].median().reset_index()
        side_dt.loc[count_y_side_index['y'] < n_bin_min, 'y'] = np.nan

        center_dt = data0.groupby('index_bin')['y'].median().reset_index()
        center_dt.loc[count_y_center_index['y'] < n_bin_min, 'y'] = np.nan
                
    else:
        
        side_dt = data0.groupby('side_index')['y'].mean().reset_index()
        side_dt.loc[count_y_side_index['y'] < n_bin_min, 'y'] = np.nan        

        center_dt = data0.groupby('index_bin')['y'].mean().reset_index()
        center_dt.loc[count_y_center_index['y'] < n_bin_min, 'y'] = np.nan
                
    side_dt = side_dt.rename(columns={'side_index': 'index'})
    center_dt = center_dt.rename(columns={'index_bin': 'index'})
    
    if side_dt.loc[0,'index'] > center_dt.loc[0,'index']:
        side_dt = pd.concat([side_dt, pd.DataFrame({'index': [center_dt.loc[0,'index']-0.5], 'y': [np.nan]})])
        side_dt = side_dt.sort_values('index').reset_index(drop=True)

    if side_dt.loc[len(side_dt)-1,'index'] < center_dt.loc[len(center_dt)-1,'index']:
        side_dt = pd.concat([side_dt, pd.DataFrame({'index': [center_dt.loc[len(center_dt)-1,'index']+0.5], 'y': [np.nan]})])
        side_dt = side_dt.sort_values('index').reset_index(drop=True)
    
    center_dt = center_dt.append(pd.DataFrame({'index': list(filter(lambda i: i not in center_dt['index'].values, range(min(center_dt['index']), max(center_dt['index'])))), 'y': np.nan})).sort_values('index').reset_index(drop=True)

    side_dt = side_dt.append(pd.DataFrame({'index': list(filter(lambda i: i not in (side_dt['index']+0.5).values, range(int(min(side_dt['index'])+0.5), int(max(side_dt['index'])+0.5)))), 'y': np.nan})).sort_values('index').reset_index(drop=True)
    
    both_dt = pd.concat([side_dt, center_dt])
    both_dt = both_dt.sort_values(by=['index']).reset_index(drop=True)
                
    # Some of the sides might be missing. If there is a valid value for the center around, complete it linearly.
    
    length_obj = len(both_dt) - 1
    
    arr = np.zeros(length_obj, dtype=bool)
    arr[::2] = True
    r1 = np.concatenate([arr, [False]])
    arr = np.ones(length_obj, dtype=bool)
    arr[::2] = False
    r2 = np.concatenate([arr, [False]])
    arr = np.ones(length_obj, dtype=bool)
    arr[::2] = False
    r3 = np.concatenate([[False], arr])
    y_int = both_dt['y']
    y_save = y_int.copy()

    # Case 1 : (center OK) (side NA) (center OK)
    if both_dt.shape[0] >= 5:
        arr = np.zeros(length_obj - 2, dtype=bool)
        arr[::2] = True
        r4 = np.concatenate([[False, False], arr, [False]])
        arr = np.ones(length_obj - 2, dtype=bool)
        arr[::2] = False
        r5 = np.concatenate((arr, [False, False, False]))
        arr = np.zeros(length_obj - 2, dtype=bool)
        arr[::2] = True
        r6 = np.concatenate(([False, False, False], arr))
        indices = np.where(r4)[0]
        y_int[indices] = (y_int[r5].reset_index(drop=True) + y_int[r6].reset_index(drop=True))/2
        y_int[~np.isnan(y_save)] = y_save[~np.isnan(y_save)].copy()
        y_save = y_int.copy()

    # Case 2 : (side OK) (center OK) (side NA)
    indices = np.where(r3)[0]
    y_int[indices] = 2*y_int[r2].reset_index(drop=True) - y_int[r1].reset_index(drop=True)
    y_int[~np.isnan(y_save)] = y_save[~np.isnan(y_save)].copy()
    y_save = y_int.copy()

    # Case 3 : (side NA) (center OK) (side OK)
    indices = np.where(r1)[0]
    y_int[indices] = 2*y_int[r2].reset_index(drop=True) - y_int[r3].reset_index(drop=True)
    y_int[~np.isnan(y_save)] = y_save[~np.isnan(y_save)].copy()
    y_save = y_int.copy()

    # Case 4 : (side NA) (center OK) (side NA)
    indices = np.where(r1)[0]
    y_int[indices] = y_int[r2].reset_index(drop=True)
    y_int[~np.isnan(y_save)] = y_save[~np.isnan(y_save)].copy()
    y_save = y_int.copy()
    indices = np.where(r3)[0]
    y_int[indices] = y_int[r2].reset_index(drop=True)
    y_int[~np.isnan(y_save)] = y_save[~np.isnan(y_save)].copy()
    y_save = y_int.copy()

    # Get the interpolation
    arr = np.zeros(len(y_int) - 1, dtype=bool)
    arr[::2] = True
    indices = np.where(np.concatenate((arr, [True])))[0]
    y_int=y_int[indices]
        
    # Interpolation
    if (~np.isnan(y_int)).sum() >= 2:
        data0['long_term'] = data0.apply(lambda row: y_int.reset_index(drop=True)[int(row['index_bin'] - data0.loc[0,'index_bin'])] + (y_int.reset_index(drop=True)[int(row['index_bin'] - data0.loc[0,'index_bin'] + 1)] - y_int.reset_index(drop=True)[int(row['index_bin'] - data0.loc[0,'index_bin'])]) * ((row['x']-seq_bin_side[int(row['index_bin'] - data0.loc[0,'index_bin'])])/(seq_bin_side[int(row['index_bin'] - data0.loc[0,'index_bin'] + 1)]-seq_bin_side[int(row['index_bin'] - data0.loc[0,'index_bin'])])) , axis=1)
    else:
        data0['long_term'] = np.nan

    return data0

def outlier(y,coeff_outlier='auto'):
    """
    Both functions have been calibrated on the Generalized Extreme Value and Pearson families.
    
    Arguments :
    - y : univariate data (numeric vector)
    - coeff_outlier:  one of coeff_outlier = 'auto' (default value), coeff_outlier = 'gaussian', coeff_outlier = (A,B,C) or coeff_outlier = None.

    Returns :
    - out_outlier, a list that contains: 
      - xy_l, a two columns data frame that contains the clean data (first column) and the outliers (second column)
      - summary_outlier_l, a vector that contains A, B, C, m_star, the size of the residuals (n), and the lower and upper outlier threshold

    """
    
    # Type of outlier checking
    log_user_coeff = False
    log_no_outlier_checking = False

    if coeff_outlier is None:
        log_no_outlier_checking = True
    else:
        if coeff_outlier == 'gaussian':
            log_user_coeff = True
            coeff_outlier = [0.08, 2, 36] # gaussian values

        if len(coeff_outlier) == 3:
            for i in range(0,len(coeff_outlier)):
                if coeff_outlier[i] == np.nan:
                    coeff_outlier[i] = 0
            log_user_coeff = True

    xy = pd.DataFrame({'y_clean': y, 'outliers': [float('nan')]*len(y)})

    if log_no_outlier_checking:
        A_coeff = np.nan
        B_coeff = np.nan
        C_coeff = np.nan
        m_star = np.nan
        n_residuals = np.nan
        lower_outlier_threshold = np.nan
        upper_outlier_threshold = np.nan
    else:
        res_nonylim = xy['y_clean']
        res_nonylim = res_nonylim[res_nonylim.notna()]
        n_residuals = len(res_nonylim)

        if n_residuals > 8:
            if log_user_coeff:
                q0_25 = np.quantile(res_nonylim, 0.25)
                q0_75 = np.quantile(res_nonylim, 0.75)
                A_coeff = coeff_outlier[0]
                B_coeff = coeff_outlier[1]
                C_coeff = coeff_outlier[2]
                m_star = np.nan
            else:
                q0_125 = np.quantile(res_nonylim, 0.125)
                q0_25 = np.quantile(res_nonylim, 0.25)
                q0_375 = np.quantile(res_nonylim, 0.375)
                q0_625 = np.quantile(res_nonylim, 0.625)
                q0_75 = np.quantile(res_nonylim, 0.75)
                q0_875 = np.quantile(res_nonylim, 0.875)

                m_plus = (q0_875-q0_625)/(q0_75-q0_25)
                m_minus = (q0_375-q0_125)/(q0_75-q0_25)

                if (m_minus != np.nan) & (m_plus != np.nan):
                    m_star = max(m_plus,m_minus)-0.6165        
                    if m_star < 0:
                        m_star = 0
                    if m_star > 2:
                        m_star = 2

                    # version 13
                    a1 = 0.2294
                    a2 = 2.9416
                    a3 = -0.0512
                    a4 = -0.0684
                    A_coeff = round(a1*np.exp(a2*m_star+a3*m_star**2+a4*m_star**3), 2)


                    # version 13
                    b1 = 1.0585
                    b2 = 15.6960
                    b3 = -17.3618
                    b4 = 28.3511
                    b5 = -11.4726
                    B_coeff = round(b1+b2*m_star+b3*(m_star**2)+b4*(m_star**3)+b5*(m_star**4), 2)

                    C_coeff = 36

                else:
                    m_star = np.nan
                    A_coeff = np.nan
                    B_coeff = np.nan
                    C_coeff = np.nan
                    lower_outlier_threshold = np.nan
                    upper_outlier_threshold = np.nan

            if A_coeff != np.nan:
                alpha = A_coeff * np.log(n_residuals) + B_coeff + C_coeff / n_residuals
                lower_outlier_threshold = q0_25 - alpha * (q0_75 - q0_25)
                upper_outlier_threshold = q0_75 + alpha * (q0_75 - q0_25)

                read_ = (xy['y_clean'] < lower_outlier_threshold) | (xy['y_clean'] > upper_outlier_threshold)
                read_[np.isnan(read_)] = False
                xy.loc[read_, 'outliers'] = xy.loc[read_, 'y_clean']
                xy.loc[read_, 'y_clean'] = np.nan

        else:
            A_coeff = np.nan
            B_coeff = np.nan
            C_coeff = np.nan
            m_star = np.nan
            lower_outlier_threshold = np.nan
            upper_outlier_threshold = np.nan


    summary_xy = [A_coeff, B_coeff, C_coeff, m_star, n_residuals, lower_outlier_threshold, upper_outlier_threshold]
    summary_xy = dict(zip(['A', 'B', 'C', 'm_star', 'n', 'lower_outlier_threshold', 'upper_outlier_threshold'], summary_xy))

    class Def_Return:
        xy_l = xy
        summary_xy_l = summary_xy

    out_outlier = Def_Return()

    return out_outlier 

def plot(out_main,show_outliers=True,show_n_bin=10):
    """
    Plot the raw data with the bins, long-term trend and cyclic component shown.
    
    Arguments :
    - out_main : the output from the function ctbi
    - show_n_bin : number of bins shown within one graphic
    - show_outliers : boolean to show or hide flagged outliers

    Returns :
    - No return value
    
    """

    data1 = out_main.data1
    data0 = out_main.data0

    # Add NA values to data0 if entire bins are missing
    read_ = data1['n_points'] == 0

    if sum(read_) != 0:
        missing_bins = data1.loc[read_].reset_index(drop=True)

        for i in range(0,len(missing_bins)):
            add_bin = pd.DataFrame(data0.iloc[0]).transpose()
            add_bin.iloc[0,0] = missing_bins.iloc[i,0]
            add_bin.iloc[0,1:] = np.nan
            add_bin.loc[0,'index_bin'] = missing_bins.loc[i,'index_bin']
            data0 = pd.concat([data0, add_bin], ignore_index=True)

        data0 = data0.sort_values(data0.columns[0])
        data0 = data0.reset_index(drop=True)

    if data1['bin_start'].dtype == 'datetime64[ns]':
        seq_bin_side = pd.Series(dtype='datetime64[ns]', index=range(len(data1)+1))
    else:
        seq_bin_side = pd.Series(index=range(len(data1)+1))

    seq_bin_side[0] = data1.loc[0,'bin_start']
    seq_bin_side[1:] = data1['bin_end']   

    # Number of variables
    n_var = len(data0.columns)-1
    col_var = data0.columns
    col_var = col_var[1:]
    col_var

    if show_n_bin > len(seq_bin_side):
        loop_k = [1,len(seq_bin_side)]
    else:
        loop_k = np.arange(start=1, stop=len(seq_bin_side), step=show_n_bin)
        if loop_k[len(loop_k)-1] < len(seq_bin_side):
            loop_k = np.append(loop_k,len(seq_bin_side)) 

    loop_k = loop_k-1

    data0_save = data0  

    for k in range(0,len(loop_k)-1):
        beg_ = seq_bin_side[loop_k[k]]        
        end_ = seq_bin_side[loop_k[k+1]]

        data0 = data0_save[(beg_ <= data0_save.iloc[:,0]) & (data0_save.iloc[:,0] < end_)]

        read_good = data0['index_bin'] > 0
        if sum(read_good)!=0:
            if show_outliers==False:
                data_ylim = data0.loc[read_good]
            else:
                data_ylim = data0

            data0_values = np.concatenate([data_ylim.iloc[:, 1], data_ylim['outliers'], data_ylim['long_term'] + data_ylim['cycle']])
            y_lim = [np.nanmin(np.array(data0_values)),np.nanmax(np.array(data0_values))]

            fig, ax = plt.subplots()
            fig.subplots_adjust(bottom=0, left=0, top=1, right=2)

            data_graph = data0.loc[read_good]
            data_graph2 = data0.loc[~read_good]

            sns.scatterplot(data=data_graph, x=data_graph.iloc[:, 0], y=data_graph.iloc[:, 1], color='black', label="data")
            sns.scatterplot(data=data_graph2, x=data_graph2.iloc[:, 0], y=data_graph2.iloc[:, 1], color='grey')
            sns.scatterplot(data=data0, x=data0.iloc[:, 0], y=data0['imputed'], color='tan', marker='s', label="imputed")
            if show_outliers:
                sns.scatterplot(data0.iloc[:, 0], data0['outliers'], color='red', marker='o', label="outliers")
            ax.plot(data0.iloc[:, 0], data0['long_term'], color='red', linewidth=2, label="long-term")
            if data0['cycle'].sum(skipna=True) != 0:
                ax.plot(data0.iloc[:, 0], data0['long_term'] + data0['cycle'], color='blue', linewidth=2, label="long-term + cycles")

            for value in seq_bin_side[(beg_ <= seq_bin_side) & (seq_bin_side <= end_)]:
                plt.axvline(x=value, color='black', linestyle='--')

            plt.xlabel('time')
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.show()

def timeseries(x_t,bin_period,bin_side,bin_center=None):
    """
    Calculate the sequence of bin sides that encompasses the original time series based on a bin period and a bin side (or a bin center). The sequence of bin centers is calculated as well.
    
    Arguments :
    - x_t : original time series (datetime or numeric)
    - bin_period : time interval between two sides of a bin. If x_t is numeric, bin_period is numeric. If x_t is datetime, bin_period = 'k units', with k an integer and units = (seconds, minutes, hours, days, weeks, half-months, months, years, decades, centuries, millenaries)
    - bin_side : one side of a bin (same class as x_t)
    - bin_center : if bin_side is not specified, one center of a bin (same class as x_t)
    
    Returns :
    - list_all, a list that contains: 
      - seq_bin_side_, the sequence of bin sides (same class as bin_side)
      - seq_bin_center_, the sequence of bin centers (same class as bin_side)
      - time_step_median_, the median time step in seconds (numeric)
    """

    # Check x_t
    if not (pd.api.types.is_numeric_dtype(x_t) or pd.api.types.is_datetime64_dtype(x_t)):
        raise ValueError("The class of the first column (time series) needs to be numeric or datetime.")

    # Type of x_t and bin_period
    log_character_t = pd.api.types.is_datetime64_dtype(x_t)
    log_numeric_t = pd.api.types.is_numeric_dtype(x_t)
    log_character_by = isinstance(bin_period, str)
    log_numeric_by = isinstance(bin_period, (int, float))

    # Check types of x_t and bin_period
    if log_numeric_t:
        if not log_numeric_by:
            raise ValueError("When the first column (time series) is numeric, argument bin_period must be numeric as well.")
    else:
        if not log_character_by:
            raise ValueError("When the first column (time series) is datetime, argument bin_period is a character string (ex: bin.period = \'1 month\'). Format: bin_period=\'k units\', with k an integer and units = {seconds, minutes, hours, days, weeks, half-months, months, years, decades, centuries, millenaries}.")

    # Extract information from log_character_by
    if log_character_by: 
        bin_period_number = hidd_check_bin_period(bin_period)[0]
        bin_period_units = hidd_check_bin_period(bin_period)[1]
        bin_period_value_seconds = hidd_check_bin_period(bin_period)[2]
        bin_period_value_days = hidd_check_bin_period(bin_period)[3]
          
        if (bin_period_units == 'secs').values:
            by_plus = str(bin_period_number) + 'S'
            by_minus = '-' + str(bin_period_number) + 'S'
            
        if (bin_period_units == 'mins').values:
            by_plus = str(bin_period_number) + 'T'
            by_minus = '-' + str(bin_period_number) + 'T'
            
        if (bin_period_units == 'hours').values:
            by_plus = str(bin_period_number) + 'H'
            by_minus = '-' + str(bin_period_number) + 'H'
        
        if (bin_period_units == 'days').values:
            by_plus = str(bin_period_number) + 'D'
            by_minus = '-' + str(bin_period_number) + 'D'
            
        if (bin_period_units == 'weeks').values:
            by_plus = str(bin_period_number) + 'W'
            by_minus = '-' + str(bin_period_number) + 'W'
            
        if (bin_period_units == 'half-months').values:
            by_plus = str(bin_period_number) + 'SMS'
            by_minus = '-' + str(bin_period_number) + 'SMS'
            
        if (bin_period_units == 'months').values:
            by_plus = str(bin_period_number) + 'MS'
            by_minus = '-' + str(bin_period_number) + 'MS'
            
        if (bin_period_units == 'years').values:
            by_plus = str(bin_period_number) + 'YS'
            by_minus = '-' + str(bin_period_number) + 'YS'
            
        if (bin_period_units == 'decades').values:
            by_plus = str(bin_period_number*10) + 'YS'
            by_minus = '-' + str(bin_period_number*10) + 'YS'
            
        if (bin_period_units == 'centuries').values:
            by_plus = str(bin_period_number*100) + 'YS'
            by_minus = '-' + str(bin_period_number*100) + 'YS'
            
        if (bin_period_units == 'millenaries').values:
            by_plus = str(bin_period_number*1000) + 'YS'
            by_minus = '-' + str(bin_period_number*1000) + 'YS'
        
    else:
        bin_period_units = 'unit'
        bin_period_value = bin_period
        by_plus = bin_period
        by_minus = -bin_period
    
    log_bin_side = bin_side is not None
    log_bin_center = bin_center is not None

    if log_bin_side and log_bin_center:
        raise ValueError("Specify either bin_center (time centered around a bin) or bin_side (time boundary of a bin), but not both. They have the same class than the time series.")

    if not log_bin_side and not log_bin_center:
        raise ValueError("Specify bin_center (time centered around a bin) or bin_side (time boundary of a bin). They have the same class than the time series.")

    # Class of the bin_side
    if log_bin_side:
        class_bin_side = isinstance(bin_side, pd.Timestamp)
        if log_character_t:
            if class_bin_side != True:
                raise ValueError("The bin_side needs to have the same class than the time series (datetime)")
        else:
            if not isinstance(bin_side, (int, float)):
                raise ValueError("The bin_side needs to have the same class than the time series (int or float)")

    # Class of the bin_center
    if log_bin_center:
        class_bin_center = isinstance(bin_center, pd.Timestamp)
        if log_character_t:
            if class_bin_center != True:
                raise ValueError("The bin_center needs to have the same class than the time series (datetime)")
        else:
            if not isinstance(bin_center, (int, float)):
                raise ValueError("The bin_center needs to have the same class than the time series (int or float)")
            
    # Check there are no NA in x_t
    if sum(np.isnan(x_t)) != 0:
        raise ValueError("The time series contains NA timesteps.")
    
    # Timestep (= sampling period) of the time series
    if log_character_t:
        # Time difference expressed in seconds
        diff_consecutive = (x_t[1:].to_numpy() - x_t[:-1].to_numpy())/1000000000
        length_timeseries = (x_t[len(x_t)-1].to_numpy() - x_t[0].to_numpy())/1000000000
    else:
        # Time difference expressed as default units
        diff_consecutive = round(pd.Series(np.diff(x_t)),4)
        length_timeseries = round(x_t[len(x_t)-1] - x_t[0], 4)

    if (len(diff_consecutive) % 2 == 0): # The median has to be calculated on an odd time series to avoid approximation.
        time_step_median = np.median(diff_consecutive[1:])
    else:
        time_step_median = np.median(diff_consecutive)
    
    time_step = np.unique(diff_consecutive)
    if max(time_step) < 0:
        raise ValueError("The time series contains backward or redundant timesteps.")

    if log_character_t:
        log_bin_min = time_step_median * 0.95 <= int(bin_period_value_seconds)
        log_bin_max = int(bin_period_value_seconds) < length_timeseries
    else:
        log_bin_min = time_step_median * 0.95 <= bin_period
        log_bin_max = bin_period < length_timeseries
    
    if not log_bin_min:
        raise ValueError("The bin_period is too small. It needs to be at least equal to the sampling period of the time series.")

    if not log_bin_max:
        raise ValueError("The bin_period is too big. Its maximum size is half the length of the time series.")

    # if not log_bin_side, find the exact bin_side so that mean(bin_side,bin_side+period) = bin_center
    if not log_bin_side:
        # Approximate bin_side
        if log_character_t:
            
            if (bin_period_units == 'secs').values:
                bin_side = bin_center - timedelta(seconds = int(bin_period_number/2))
            
            if (bin_period_units == 'mins').values:
                bin_side = bin_center - timedelta(minutes = int(bin_period_number/2))
                
            if (bin_period_units == 'hours').values:
                bin_side = bin_center - timedelta(hours = int(bin_period_number/2))
                
            if (bin_period_units == 'days').values:
                bin_side = bin_center - timedelta(days = int(bin_period_number/2))
                
            if (bin_period_units == 'weeks').values:
                bin_side = bin_center - timedelta(weeks = int(bin_period_number/2))
                
            if (bin_period_units == 'half-months').values:
                bin_side = bin_center - timedelta(days = 15*int(bin_period_number/2))
                
            if (bin_period_units == 'months').values:
                                
                year_bin = bin_center.year
                
                if bin_period_number % 2 != 0:
                    month_bin = bin_center[0].month-(bin_period_number-1)/2 
                    day_bin = bin_center[0].day
                    
                    if day_bin < 28:
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin))

                    if day_bin >= 28:
                        day_bin = day_bin - 5
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin)) + timedelta(days = 5)
                        
                    bin_side = bin_side - timedelta(days = 15)
                    
                else:
                    month_bin = bin_center.month-bin_period_number/2
                    day_bin = bin_center.day

                    if day_bin < 28:
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin))

                    if day_bin >= 28:
                        day_bin = day_bin - 5
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin)) + timedelta(days = 5)
                        
            if (bin_period_units == 'decades').values:
                
                bin_period_number = bin_period_number*10
                bin_period_units = 'years' 
                
            if (bin_period_units == 'centuries').values:
                
                bin_period_number = bin_period_number*100
                bin_period_units = 'years'
                
            if (bin_period_units == 'millenaries').values:
                
                bin_period_number = bin_period_number*1000
                bin_period_units = 'years'
                
            if (bin_period_units == 'years').values:
                
                if bin_period_number % 2 != 0:
                
                    year_bin = bin_center.year-(bin_period_number-1)/2
                    month_bin = bin_center.month
                    day_bin = bin_center.day

                    if day_bin < 28:
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin))

                    if day_bin >= 28:
                        day_bin = day_bin - 5
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin)) + timedelta(days = 5) 
                        
                    bin_side = bin_side - timedelta(days = 183)
                    
                else:                    
                    year_bin = bin_center.year-bin_period_number/2
                    month_bin = bin_center.month
                    day_bin = bin_center.day

                    if day_bin < 28:
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin))

                    if day_bin >= 28:
                        day_bin = day_bin - 5
                        bin_side = pd.to_datetime(str(year_bin)+'-'+str(month_bin)+'-'+str(day_bin)) + timedelta(days = 5)        
            
        else:
            bin_side = bin_center - bin_period/2
      
        # Calculate the next consecutive bin_side and the mean(bin_side,bin_side+period)
        if log_character_t:
            
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                bin_side_next = hidd_seq(start=bin_side,length_out=2,by=by_plus)
                
            if (bin_period_units == 'half-months').values: 
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
            
            if (bin_period_units == 'months').values: 
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)
            
        else:
            bin_side_next = hidd_seq(start=bin_side,length_out=2,by=by_plus)
        
        bin_side_next = bin_side_next[1]
        bin_center_compare = bin_side + ((bin_side_next-bin_side)/2)

        # Calculate the shift
        shift_bin_side = bin_center-bin_center_compare
        bin_side = bin_side+shift.bin.side
        
    # if log_bin_side, find the exact bin_center to that mean(bin_side,bin_side+period) = bin_center
    if log_bin_side:
        # Calculate the next consecutive bin_side and the mean(bin_side,bin_side+period)
        if log_character_t:
            
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                bin_side_next = hidd_seq(start=bin_side,length_out=2,by=by_plus)
                
            if (bin_period_units == 'half-months').values: 
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
            
            if (bin_period_units == 'months').values: 
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                bin_side_next = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),length_out=2,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)

        else:
            bin_side_next = hidd_seq(start=bin_side,length_out=2,by=by_plus)
        
        bin_side_next = bin_side_next[1]
        bin_center = bin_side + ((bin_side_next-bin_side)/2)
        
    # We now have two consistent bin_side and bin_center. They could be outside the time series.
    # find seq_bin_side
    
    seq_temp_beg = None
    seq_temp_fin = None
    
    if log_character_t:
        seq_bin_side = bin_side
    
        if bin_side >= x_t[0]:
                        
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                seq_temp_beg = hidd_seq(start=bin_side,end=x_t[0],by=by_minus)[::-1]  
                seq_temp_beg = hidd_seq(start=bin_side,length_out=len(seq_temp_beg)+1,by=by_minus)[::-1] 
                
            if (bin_period_units == 'half-months').values: 
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),end=x_t[0]-timedelta(days = (x_t[0]-pd.to_datetime(str(x_t[0].year)+'-'+str(x_t[0].month)+'-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=len(seq_temp_beg)+1,by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
            
            if (bin_period_units == 'months').values: 
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),end=x_t[0]-timedelta(days = (x_t[0]-pd.to_datetime(str(x_t[0].year)+'-'+str(x_t[0].month)+'-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=len(seq_temp_beg)+1,by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),end=x_t[0]-timedelta(days = (x_t[0]-pd.to_datetime(str(x_t[0].year)+'-01-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)
                seq_temp_beg = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),length_out=len(seq_temp_beg)+1,by=by_minus)[::-1]+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)
                
        if bin_side <= x_t[len(x_t)-1]:
                
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                seq_temp_fin = hidd_seq(start=bin_side,end=x_t[len(x_t)-1],by=by_plus) 
                seq_temp_fin = hidd_seq(start=bin_side,length_out=len(seq_temp_fin)+1,by=by_plus)
                
            if (bin_period_units == 'half-months').values: 
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),end=x_t[len(x_t)-1]-timedelta(days = (x_t[len(x_t)-1]-pd.to_datetime(str(x_t[len(x_t)-1].year)+'-'+str(x_t[len(x_t)-1].month)+'-01')).days),by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=len(seq_temp_fin)+1,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
            
            if (bin_period_units == 'months').values: 
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),end=x_t[len(x_t)-1]-timedelta(days = (x_t[len(x_t)-1]-pd.to_datetime(str(x_t[len(x_t)-1].year)+'-'+str(x_t[len(x_t)-1].month)+'-01')).days),by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days),length_out=len(seq_temp_fin)+1,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-'+str(bin_side.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),end=x_t[len(x_t)-1]-timedelta(days = (x_t[len(x_t)-1]-pd.to_datetime(str(x_t[len(x_t)-1].year)+'-01-01')).days),by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)
                seq_temp_fin = hidd_seq(start=bin_side-timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days),length_out=len(seq_temp_fin)+1,by=by_plus)+timedelta(days = (bin_side-pd.to_datetime(str(bin_side.year)+'-01-01')).days)
        
        if seq_temp_beg is not None and seq_temp_fin is not None:
            seq_bin_side = seq_temp_beg.append(seq_temp_fin[1:])  
        else:
            if seq_temp_beg is not None:
                seq_bin_side = seq_temp_beg
            else:
                if seq_temp_fin is not None:
                    seq_bin_side = seq_temp_fin
            
    else:
        seq_bin_side = bin_side
    
        if bin_side >= x_t[0]:
            seq_temp_beg = hidd_seq(start=bin_side,end=x_t[0],by=by_minus)[::-1]  
            seq_temp_beg = hidd_seq(start=bin_side,length_out=len(seq_temp_beg)+1,by=by_minus)[::-1]  

        if bin_side <= x_t[len(x_t)-1]:
            seq_temp_fin = hidd_seq(start=bin_side,end=x_t[len(x_t)-1],by=by_plus)        
            seq_temp_fin = hidd_seq(start=bin_side,length_out=len(seq_temp_fin)+1,by=by_plus) 
               
        if seq_temp_beg is not None and seq_temp_fin is not None:
            seq_bin_side = np.concatenate([seq_temp_beg, seq_temp_fin[1:]]) 
        else:
            if seq_temp_beg is not None:
                seq_bin_side = seq_temp_beg
            else:
                if seq_temp_fin is not None:
                    seq_bin_side = seq_temp_fin
        
    # Cut seq_bin_side
    index_side = list(range(0, len(seq_bin_side)))
    ind_min = np.where(seq_bin_side[index_side] <= x_t[0])[0].tolist()
    ind_max = np.where(seq_bin_side[index_side] > x_t[len(x_t)-1])[0].tolist()
    seq_bin_side = seq_bin_side[max(ind_min):min(ind_max)+1]
    
    # Find seq_bin_center
    
    seq_bin_center_beg = None
    seq_bin_center_fin = None
    
    if log_character_t:        
        seq_bin_center = bin_center

        if bin_center > seq_bin_side[0]:          
                        
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                seq_bin_center_beg = hidd_seq(start=bin_center,end=seq_bin_side[0],by=by_minus)[::-1]
                
            if (bin_period_units == 'half-months').values:
                seq_bin_center_beg = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days),end=seq_bin_side[0]-timedelta(days = (seq_bin_side[0]-pd.to_datetime(str(seq_bin_side[0].year)+'-'+str(seq_bin_side[0].month)+'-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days)
                
            if (bin_period_units == 'months').values: 
                seq_bin_center_beg = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days),end=seq_bin_side[0]-timedelta(days = (seq_bin_side[0]-pd.to_datetime(str(seq_bin_side[0].year)+'-'+str(seq_bin_side[0].month)+'-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                seq_bin_center_beg = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-01-01')).days),end=seq_bin_side[0]-timedelta(days = (seq_bin_side[0]-pd.to_datetime(str(seq_bin_side[0].year)+'-01-01')).days),by=by_minus)[::-1]+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-01-01')).days)            
            
        if bin_center < seq_bin_side[len(seq_bin_side)-1]:          
                        
            if (bin_period_units == 'secs').values | (bin_period_units == 'mins').values | (bin_period_units == 'hours').values | (bin_period_units == 'days').values | (bin_period_units == 'weeks').values:
                seq_bin_center_fin = hidd_seq(start=bin_center,end=seq_bin_side[len(seq_bin_side)-1],by=by_plus)
                
            if (bin_period_units == 'half-months').values:
                seq_bin_center_fin = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days),end=seq_bin_side[len(seq_bin_side)-1]-timedelta(days = (seq_bin_side[len(seq_bin_side)-1]-pd.to_datetime(str(seq_bin_side[len(seq_bin_side)-1].year)+'-'+str(seq_bin_side[len(seq_bin_side)-1].month)+'-01')).days),by=by_plus)+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days)
                
            if (bin_period_units == 'months').values: 
                seq_bin_center_fin = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days),end=seq_bin_side[len(seq_bin_side)-1]-timedelta(days = (seq_bin_side[len(seq_bin_side)-1]-pd.to_datetime(str(seq_bin_side[len(seq_bin_side)-1].year)+'-'+str(seq_bin_side[len(seq_bin_side)-1].month)+'-01')).days),by=by_plus)+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-'+str(bin_center.month)+'-01')).days)
                
            if (bin_period_units == 'years').values | (bin_period_units == 'decades').values | (bin_period_units == 'centuries').values | (bin_period_units == 'millenaries').values:
                seq_bin_center_fin = hidd_seq(start=bin_center-timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-01-01')).days),end=seq_bin_side[len(seq_bin_side)-1]-timedelta(days = (seq_bin_side[len(seq_bin_side)-1]-pd.to_datetime(str(seq_bin_side[len(seq_bin_side)-1].year)+'-01-01')).days),by=by_plus)+timedelta(days = (bin_center-pd.to_datetime(str(bin_center.year)+'-01-01')).days)            

        if seq_bin_center_beg is not None and seq_bin_center_fin is not None:
            seq_bin_center = seq_bin_center_beg.append(seq_bin_center_fin[1:])  
        else:
            if seq_bin_center_beg is not None:
                seq_bin_center = seq_bin_center_beg
            else:
                if seq_bin_center_fin is not None:
                    seq_bin_center = seq_bin_center_fin        
    else:        
        seq_bin_center = bin_center

        if bin_center > seq_bin_side[0]:
            seq_bin_center_beg = hidd_seq(start=bin_center,end=seq_bin_side[0],by=by_minus)[::-1]

        if bin_center < seq_bin_side[len(seq_bin_side)-1]:
            seq_bin_center_fin = hidd_seq(start=bin_center,end=seq_bin_side[len(seq_bin_side)-1],by=by_plus)

        if seq_bin_center_beg is not None and seq_bin_center_fin is not None:
            seq_bin_center = np.concatenate([seq_bin_center_beg, seq_bin_center_fin[1:]])
        else:
            if seq_bin_center_beg is not None:
                seq_bin_center = seq_bin_center_beg
            else:
                if seq_bin_center_fin is not None:
                    seq_bin_center = seq_bin_center_fin
    
    # Cut seq_bin_center
    index_center = list(range(0, len(seq_bin_center)))
    ind_min = np.where(seq_bin_side[0] < seq_bin_center[index_center])[0].tolist()
    ind_max = np.where(seq_bin_center[index_center] < seq_bin_side[-1])[0].tolist()
    seq_bin_center = seq_bin_center[min(ind_min):max(ind_max)+1]
    
    class Def_Return:
        seq_bin_side_ = seq_bin_side
        seq_bin_center_ = seq_bin_center
        time_step_median_ = time_step_median

    list_all = Def_Return()
    
    return list_all

def hidd_check_bin_period(bin_period):
    """
    Interpret the string character bin_period used in timeseries or main
    
    Arguments :
    - bin_period : str or int or float, a character string or a numeric
    
    Returns :
    - list_return, a list that contains: 
      - number, a numeric that indicates the value of bin_period
      - units, a character that indicates the unit of bin_period
      - bin_period_value_seconds, a numeric that indicates the value in seconds of bin_period
      - bin_period_value_days, a numeric that indicates the value in days of bin_period
    """
    
    char_stop = "When the first column (time series) is datetime, argument 'bin_period' is a character string. Example: bin_period='k units', with k an integer and units = {seconds, minutes, hours, days, weeks, half-months, months, years, decades, centuries, millenaries}."

    input_values = ['s', 'sec', 'secs', 'second', 'seconds', 'm', 'min', 'mins', 'minute', 'minutes', 'h', 'hr', 'hour', 'hours', 'd', 'day', 'days', 'w', 'week', 'weeks', 'hm', 'h-m', 'half-month', 'half-months', 'halfmonth', 'halfmonths', 'half month', 'half months', 'month', 'months', 'y', 'yr', 'yrs', 'year', 'years', 'decade', 'decades', 'century', 'centuries', 'millenary', 'millenaries', 'millennium']
    output_standard = ['secs', 'secs', 'secs', 'secs', 'secs', 'mins', 'mins', 'mins', 'mins', 'mins', 'hours', 'hours', 'hours', 'hours', 'days', 'days', 'days', 'weeks', 'weeks', 'weeks', 'half-months', 'half-months', 'half-months', 'half-months', 'half-months', 'half-months', 'half-months', 'half-months', 'months', 'months', 'years', 'years', 'years', 'years', 'years', 'decades', 'decades', 'centuries', 'centuries', 'millenaries', 'millenaries', 'millenaries']
    output_value_seconds = [1, 1, 1, 1, 1, 60, 60, 60, 60, 60, 60*60, 60*60, 60*60, 60*60, 60*60*24, 60*60*24, 60*60*24, 60*60*24*7, 60*60*24*7, 60*60*24*7, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*15, 60*60*24*30.5, 60*60*24*30.5, 60*60*24*365, 60*60*24*365, 60*60*24*365, 60*60*24*365, 60*60*24*365, 60*60*24*365*10, 60*60*24*365*10, 60*60*24*365*100, 60*60*24*365*100, 60*60*24*365*1000, 60*60*24*365*1000, 60*60*24*365*1000]
    output_value_days = [1/(60*60*24), 1/(60*60*24), 1/(60*60*24), 1/(60*60*24), 1/(60*60*24), 1/(60*24), 1/(60*24), 1/(60*24), 1/(60*24), 1/(60*24), 1/24, 1/24, 1/24, 1/24, 1, 1, 1, 7, 7, 7, 15, 15, 15, 15, 15, 15, 15, 15, 30.4167, 30.4167, 365, 365, 365, 365, 365, 365*10, 365*10, 365*100, 365*100, 365*1000, 365*1000, 365*1000]

    data_units = pd.DataFrame({'input_values': input_values, 'output_standard': output_standard, 'output_value_seconds': output_value_seconds, 'output_value_days': output_value_days})

    # Search number in bin_period
    search_bin_period_number = re.search(r'\d+', bin_period)
    
    if search_bin_period_number != None:
        bin_period_number = int(search_bin_period_number.group())
    else:
        raise ValueError(char_stop)

    # Search unit in bin_period
    search_bin_period_unit = bin_period.replace(str(bin_period_number), "")
    bin_period_unit = search_bin_period_unit.replace(" ", "")

    if not isinstance(bin_period_number, (int, float)):
        raise ValueError(char_stop)
    elif bin_period_unit not in input_values:
        raise ValueError(char_stop)
    else:
        # Compute bin_period_value_seconds and bin_period_value_days
        bin_period_value_seconds = bin_period_number*data_units.loc[data_units['input_values']==bin_period_unit,'output_value_seconds']
        bin_period_value_days = bin_period_number*data_units.loc[data_units['input_values']==bin_period_unit,'output_value_days']
        bin_period_unit = data_units.loc[data_units['input_values']==bin_period_unit,'output_standard']
        
        list_return = [bin_period_number, bin_period_unit, bin_period_value_seconds, bin_period_value_days]
        return list_return 

def hidd_rel_time(x, seq_bin_side):
    """
    Calculate the relative position of each timestep of a vector with respect to the bin boundaries
    
    Arguments :
    - x : a vector (datetime or numeric)
    - seq_bin_side : the sequence of bin sides
    
    Returns :
    - r_out, the relative position of each value of x with respect to the bins in seq_bin_side (between 0 and 1)
    """
    
    x1 = max(seq_bin_side[seq_bin_side <= x[0]])
    x2 = min(seq_bin_side[x[len(x)-1] < seq_bin_side])
    r_out = (x[0] - x1) / (x2 - x1)
    
    return r_out

def hidd_seq(start = 1, end = 1, by = None, length_out = None):
    """
    Similar to np.arrange() if 'start' it's a numeric or pd.date_range() a datetime
    
    Arguments :
    - start : the starting value of the sequence
    - end : the end value of the sequence
    - by : increment of the sequence
    - length_out : desired length of the sequence, by default 'None'
    
    Returns :
    - seq_all, a vector of same class than 'start'
    """
    # Check if by is None
    if by is None and length_out is not None:
        by = ((end - start)/(length_out - 1))
    
    class_start = type(start).__name__
    if class_start == 'Timestamp':
        if length_out is not None:
            seq_all = pd.date_range(start=start, freq=by, periods=length_out)
        else:
            seq_all = pd.date_range(start=start, end=end, freq=by)
    else:
        if length_out is not None:
            seq_all = np.arange(start, stop=start+length_out*by, step=by)
        else:
            seq_all = np.arange(start, stop=end, step=by)

    return seq_all    