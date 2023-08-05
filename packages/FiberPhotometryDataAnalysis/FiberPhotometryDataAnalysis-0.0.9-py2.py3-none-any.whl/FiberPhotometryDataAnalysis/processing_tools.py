def smooth_signal(x,window_len=10,window='flat'):

    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    The code taken from: https://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                'flat' window will produce a moving average smoothing.

    output:
        the smoothed signal        
    """

    if x.ndim != 1:
        raise(ValueError, "smooth only accepts 1 dimension arrays.")

    if x.size < window_len:
        raise(ValueError, "Input vector needs to be bigger than window size.")

    if window_len<3:
        return x

    if window_len % 2 == 1:
      window_len -= 1

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise(ValueError, "Window is one of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s=np.r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]

    if window == 'flat': # Moving average
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')

    return y[(int(window_len/2)-1):-int(window_len/2)]




from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=10):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=10):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y




def flatten_signal(signal,lambda_=1e4,order=0.5,itermax=50):

# Find the signal baseline using airPLS alghorithm
  # add_beginning=600
  # signal = np.insert(signal, 0, signal[0]*np.ones(add_beginning)).reshape(len(signal)+add_beginning,1)
  # base = airPLS(signal[:,0],lambda_=lambda_,porder=order,itermax=itermax).reshape(len(signal),1)
  # signal = signal[add_beginning:]
  # base = base[add_beginning:]

  add=600
  s = np.r_[signal[add-1:0:-1],signal,signal[-2:-add-1:-1]]
  b = airPLS(s,lambda_=lambda_,porder=order,itermax=itermax)
  signal = s[add-1:-add+1]
  base = b[add-1:-add+1]

# Remove the begining of the signal baseline
  signal = (signal - base)

  return signal, base




def standardize_signal(signal):

  z_signal = (signal - np.nanmedian(signal)) / np.nanstd(signal)

  return z_signal


'''
airPLS.py Copyright 2014 Renato Lombardo - renato.lombardo@unipa.it
Baseline correction using adaptive iteratively reweighted penalized least squares

This program is a translation in python of the R source code of airPLS version 2.0
by Yizeng Liang and Zhang Zhimin - https://code.google.com/p/airpls
Reference:
Z.-M. Zhang, S. Chen, and Y.-Z. Liang, Baseline correction using adaptive iteratively reweighted penalized least squares. Analyst 135 (5), 1138-1146 (2010).

Description from the original documentation:

Baseline drift always blurs or even swamps signals and deteriorates analytical results, particularly in multivariate analysis.  It is necessary to correct baseline drift to perform further data analysis. Simple or modified polynomial fitting has been found to be effective in some extent. However, this method requires user intervention and prone to variability especially in low signal-to-noise ratio environments. The proposed adaptive iteratively reweighted Penalized Least Squares (airPLS) algorithm doesn't require any user intervention and prior information, such as detected peaks. It iteratively changes weights of sum squares errors (SSE) between the fitted baseline and original signals, and the weights of SSE are obtained adaptively using between previously fitted baseline and original signals. This baseline estimator is general, fast and flexible in fitting baseline.


LICENCE
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import numpy as np
from scipy.sparse import csc_matrix, eye, diags
from scipy.sparse.linalg import spsolve

def WhittakerSmooth(x,w,lambda_,differences=1):
    '''
    Penalized least squares algorithm for background fitting
    
    input
        x: input data (i.e. chromatogram of spectrum)
        w: binary masks (value of the mask is zero if a point belongs to peaks and one otherwise)
        lambda_: parameter that can be adjusted by user. The larger lambda is,  the smoother the resulting background
        differences: integer indicating the order of the difference of penalties
    
    output
        the fitted background vector
    '''
    X=np.matrix(x)
    m=X.size
    #i=np.arange(0,m)
    E=eye(m,format='csc')
    D=E[1:]-E[:-1] # numpy.diff() does not work with sparse matrix. This is a workaround.
    W=diags(w,0,shape=(m,m))
    A=csc_matrix(W+(lambda_*D.T*D))
    B=csc_matrix(W*X.T)
    background=spsolve(A,B)
    return np.array(background)

def airPLS(x, lambda_=100, porder=1, itermax=15):
    '''
    Adaptive iteratively reweighted penalized least squares for baseline fitting
    
    input
        x: input data (i.e. chromatogram of spectrum)
        lambda_: parameter that can be adjusted by user. The larger lambda is,  the smoother the resulting background, z
        porder: adaptive iteratively reweighted penalized least squares for baseline fitting
    
    output
        the fitted background vector
    '''
    m=x.shape[0]
    w=np.ones(m)
    for i in range(1,itermax+1):
        z=WhittakerSmooth(x,w,lambda_, porder)
        d=x-z
        dssn=np.abs(d[d<0].sum())
        if(dssn<0.001*(abs(x)).sum() or i==itermax):
            if(i==itermax): print('WARING max iteration reached!')
            break
        w[d>=0]=0 # d>0 means that this point is part of a peak, so its weight is set to 0 in order to ignore it
        w[d<0]=np.exp(i*np.abs(d[d<0])/dssn)
        w[0]=np.exp(i*(d[d<0]).max()/dssn) 
        w[-1]=w[0]
    return z




def interpolate_signal(signal,t_old,t_new):

  from scipy.interpolate import interp1d

  func = interp1d(t_old,signal)
  s_new = func(t_new)

  return s_new




def fit_signal(signal, reference, model='RANSAC'):

  i0 = np.max(np.argwhere(np.isnan(signal)))
  signal = signal[i0+1:]
  reference = reference[i0+1:]

  signal = np.array(signal).reshape(len(signal),1)
  reference = np.array(reference).reshape(len(reference),1)

# Positive linear regression
  if model == 'RANSAC':
    from sklearn.linear_model import RANSACRegressor
    lin = RANSACRegressor(max_trials=1000,random_state=9999)
  elif model == 'Lasso':
    from sklearn.linear_model import Lasso
    lin = Lasso(alpha=0.0001,precompute=True,max_iter=1000,
                positive=True, random_state=9999, selection='random')

  lin.fit(reference, signal)
  reference_fitted = lin.predict(reference)
  reference_fitted = reference_fitted.reshape(len(reference_fitted),)

  a = np.empty((i0+1,))
  a[:] = np.nan   
  reference_fitted = np.r_[a,reference_fitted]
      
  return reference_fitted




def calculate_dff(signal,reference,standardized=True):

  if standardized:
    dFF = signal - reference
  else:
    dFF = (signal - reference) / reference

  dFF = standardize_signal(dFF)

  return dFF  




def create_perievents(signal,time_,event,window=[-5.0,5.0],dur=None,iei=None,avg_win=None):

  period = find_avg_period(time_, time_format='total seconds')

 # Remove events at the beginning and end of test that less than win 
  event = event[np.all(event > abs(window[0]), axis=1)]
  event = event[np.all(event < max(time_)-window[1], axis=1)]

 # Events with one occurence ---------------------------------------------------
  if event.shape[1]==1:
    Array = []
    for e in event:
      s_event = chunk_signal(signal,e,time_,window)
      if avg_win is not None:
        s_event_mean = (s_event[int((-window[0]+avg_win[0])/period):int((-window[0]+avg_win[1])/period)]).mean()
        s_event = s_event - s_event_mean
      Array.append(s_event)    
    Array = np.array(Array).squeeze()
    if Array.ndim == 1:
      Array = Array.reshape(1,len(Array))
    Array = Array[~np.isnan(Array).any(axis=1)]

    Perievents = {'onset': Array}

 # Events with onset and offset ------------------------------------------------
  elif event.shape[1]==2:

 # Remove short intervals and durations
    event = adjust_intervals_durations(event, iei, dur)
      
   # Create Perievent Arrays
   # Initialize Arrays
    Array_onset = []
    Array_offset = []
   # Loop through all onsets and offsets
    for e0,e1 in event:
      s_onset = chunk_signal(signal,e0,time_,window)
      s_offset = chunk_signal(signal,e1,time_,window)
     # Normalize signals to signals in avg_win
      if avg_win is not None:
        s_event_mean = (s_onset[int((-window[0]+avg_win[0])/period):int((-window[0]+avg_win[1])/period)]).mean()
        s_onset = s_onset - s_event_mean
        s_offset = s_offset - s_event_mean
     # Append to arrays   
      Array_onset.append(s_onset)
      Array_offset.append(s_offset)
   # Squeeze to 2D arrays   
    Array_onset = np.array(Array_onset).squeeze()
    Array_offset = np.array(Array_offset).squeeze()
   # Reshape Arrays if squeezed to 1D 
    if Array_onset.ndim == 1:
      Array_onset = Array_onset.reshape(1,len(Array_onset))
      Array_offset = Array_offset.reshape(1,len(Array_offset))
   # Remove elements with nans   
    Array_onset = Array_onset[~np.isnan(Array_onset).any(axis=1)]
    Array_offset = Array_offset[~np.isnan(Array_offset).any(axis=1)]

    Perievents = {'onset': Array_onset,
                 'offset': Array_offset}

  return Perievents




def chunk_signal(signal, t0, t, w):

  idx = find_idx(t0, t, 'total seconds')

  period = find_avg_period(t, 'total seconds')

  i0 = idx + int(w[0]/period - 1/2)
  i1 = idx + int(w[1]/period + 1/2) + 1

  chunk = signal[i0:i1]

  return chunk




def create_centered_time_vector(period=0.1,window=[-5.0,5.0]):

  t_pre = np.arange(-period,window[0]-period/2,-period)
  t_post = np.arange(0,window[1]+period/2,period)
  t = np.concatenate([t_pre[-1::-1],t_post])

  return t



def calculate_auc(means, period=0.10, window=[-5.0,5.0], time_frames=[[-3,0],[0,3]]):

  from sklearn import metrics

  t = create_centered_time_vector(period,window)

  stats = np.zeros([len(means),len(time_frames)])

  for i,frame in enumerate(time_frames):
    idx = [i for i in range(len(t)) if t[i]>frame[0] and t[i]<frame[1]]
    #stats1 = np.mean(means[:,idx],axis=1)
    for m in range(len(means)):
      auc = metrics.auc(t[idx],means[m,idx])
      stats[m,i] = auc / (frame[1] - frame[0])

  return stats
