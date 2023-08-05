class recording:

  '''
    A class used to represent a fiber photometry recording
    ...

    Attributes
    ----------
    signals : dict
        Calcium-dependent traces recorded with 470 nm (e.g. GCaMP) or 560 nm (e.g. jrGECO) LEDs
    references : dict
        Calcium-independent traces recorded with 405-415 nm LED
    time_ : numpay.ndarray
        Timestamps of the recording
    events : dict
        External or behavioral events that happening during the recoring
    meaurements : dict
        Other continious recordings happening along with the fiber photometry recording
    mouse : str
        Name of a mouse
    test : str
        Name of a test
    trial : str
        Number of a trial

    Methods
    -------
    loadRecording(filename,mouse,test,trial='1')
        Loads a recording from a specified filename file for specified mouse, test, and trial
    
    '''

  import numpy as np   

  def __init__(self,signals=None,references=None,time_=None,
               events=None,measurements=None,mouse='mouse',test='test',trial='1'):

    s = signals is None; r = references is None; t = time_ is None
    if (s^r or r^t or s^t):
      raise TypeError('To initialize the object, the function takes either 0 or 3-8 arguments (signals, references, time_, ...).')

    if signals and references and time_ is not None:
      if (type(signals) or type(references)) is not dict:
        raise TypeError('signals and references have to be dictionaries with keys indicating names of neural populations and values indicating corresponding traces as 1D numpy.ndarray.')

      if signals.keys() != references.keys():
        raise KeyError('Keys in signals and references dictionaries have to be the same.')

      for output in signals:
        if (type(signals[output]) or type(references[output])) is not np.ndarray:
          raise TypeError('Values of signals and references dictionaries have to be 1D numpy.ndarray.')
        if signals[output].ndim != 1 or references[output].ndim != 1:
          raise ValueError('Values of signals and refernces dictionaries have to be 1D numpy.ndarray.')

      if type(time_) is not np.ndarray:
        raise TypeError('time_ argument has to be 1D numpy.ndarray.')
      if time_.ndim != 1:
        raise ValueError('time_ argument has to be 1D numpy.ndarray.')
      
      for output in signals:
        if signals[output].size != time_.size or references[output].size != time_.size:
          raise ValueError('All signals, references, and time arrays have to be the same length.')

      if events is not None:
        if type(events) is not dict:
          raise TypeError('events argument has to be a dictionary.')
        for e in events:
          if type(events[e]) is not np.ndarray:
            raise TypeError('Values of events dictionary have to be 2D numpy.ndarrays.')
          if events[e].ndim != 2:
            raise ValueError('Values of events dictionary have to be 2D numpy.ndarrays.')

      if measurements is not None:
        if type(measurements) is not dict:
          raise TypeError('measurements argument has to be a dictionary.')
        for m in measurements:
          if type(measurements[m]) is not dict:
            raise TypeError('Values of measurements dictionary have to be dictionaries with keys "time" and "values".')
          if list(measurements[m].keys()) != ['time', 'values']:
            raise TypeError('Values of measurements dictionary have to be dictionaries with keys "time" and "values".')
          if (type(measurements[m]['time']) or type(measurements[m]['values'])) is not np.ndarray:
            raise TypeError('Values of "time" and "values" in measurements dictionary have to be 1D numpy.ndarray.')
          if measurements[m]['time'].ndim != 1 or measurements[m]['values'].ndim != 1:
            raise ValueError('Values of "time" and "values" in measurements dictionary have to be 1D numpy.ndarray.')

        if type(mouse) is not str:
          raise TypeError('Argument mouse has to be a string.')
        if type(test) is not str:
          raise TypeError('Argument test has to be a string.')
        if type(trial) is not str:
          raise TypeError('Argument test has to be a string.')

          
    self.rawSignals = signals
    self.rawReferences = references
    self.signals = None
    self.references = None
    self.dFFs = None
    self.time = time_
    self.events = events
    self.measurements = measurements
    self.perievents = None
    self.measurePerievents = None
    self.mouse = mouse
    self.test = test
    self.trial = trial

    if self.rawSignals is not None:
      self.outputs = list(self.rawSignals.keys())
    else:
      self.outputs = None

    if time_ is not None:
      self.period = find_avg_period(self.time)
      self.frequency = 1 / self.period
    else:
      self.period = None
      self.frequency = None

    self.timeDFF = None
    


  def __repr__(self):
    if self.outputs is None:
      self = None
      return 'No recording was loaded.'

    outputs_string = ''
    for output in self.outputs:
      outputs_string += output + ', '
    return 'Fiber photometry recordings for mouse {} in outputs/pathways {}during test {}-{}.'\
            .format(self.mouse,outputs_string,self.test,self.trial)



  def loadRecording(self,fileHDF,mouse,test,trial='1'):
    
    import h5py
    import numpy as np
        
    self.mouse = mouse
    self.test = test
    self.trial = trial

    with h5py.File(fileHDF, 'r') as f:

      if 'Raw/'+test in f:
        outputs = list(f['Raw/'+test].keys())
      else:
        return print('No recordings are saved for test {}.'.format(test))

      self.rawSignals = {}
      self.rawReferences = {}
      for output in outputs:
        path = 'Raw/'+test+'/'+output+'/'+mouse+'/'+trial+'/'
        if path in f:
          self.rawSignals[output] = np.array(f[path].get('signal'))
          self.rawReferences[output] = np.array(f[path].get('reference'))
          self.time = np.array(f[path].get('time'))
      if self.rawSignals == {}:
        self.mouse = None
        self.test = None
        self.trial = None
        self.rawSignals = None
        self.rawReferences = None
        return 'The recording for animal {} in the experiment {}-{} is not saved in the file.'.format(mouse,test,trial)
        
      self.outputs = list(self.rawSignals.keys())

      self.period = find_avg_period(self.time)
      self.frequency = 1 / self.period
      
      if 'Recordings/'+self.test in f:
        self.signals = {}
        self.references = {}
        for output in self.outputs:
          path = 'Recordings/'+test+'/'+output+'/'+mouse+'/'+trial+'/'
          if path in f:
            self.signals[output] = np.array(f[path].get('signal'))
            self.references[output] = np.array(f[path].get('reference'))

      if 'DFFs/'+test in f:
        self.dFFs = {}
        for output in outputs:
          path = 'DFFs/'+test+'/'+output+'/'+mouse+'/'+trial+'/'
          if path in f:
            self.dFFs[output] = np.array(f[path].get('dFF'))
            self.timeDFF = np.array(f[path].get('time'))

      if 'Events/'+test in f:
        self.events = {}
        for event in f['Events/'+test]:
          path = 'Events/'+test+'/'+event+'/'+mouse+'/'+trial+'/'
          if path in f:
            self.events[event] = np.array(f[path].get('timestamps'))

      if 'Measurements/'+test in f:    
        self.measurements = {}
        for measure in f['Measurements/'+test]:
          path = 'Measurements/'+test+'/'+measure+'/'+mouse+'/'+trial+'/'
          if path in f:
            self.measurements[measure] = {'time': np.array(f[path].get('time')),
                                        'values': np.array(f[path].get('values'))}
         
      if 'Perievents/'+test in f:
        self.perievents = {}
        for output in f['Perievents/'+test]:
          self.perievents[output] = {}
          for event in f['Perievents/'+test+'/'+output]:
            self.perievents[output][event] = {}
            for onoffset in f['Perievents/'+test+'/'+output+'/'+event]:
              path = 'Perievents/'+test+'/'+output+'/'+event+'/'+onoffset+'/'+mouse
              if path+'/'+trial in f:
                self.perievents[output][event][onoffset] = np.array(f[path].get(trial))
              else:
                self.perievents = {}
                break
            else:
              continue # continue if the inner loop wasn't broken
            break      # break if the inner loop was broken


      if 'MeasurePerievents/'+test in f:
        self.measurePerievents = {}
        for measure in f['MeasurePerievents/'+test]:
          self.measurePerievents[measure] = {}
          for event in f['MeasurePerievents/'+test+'/'+measure]:
            self.measurePerievents[measure][event] = {}
            for onoffset in f['MeasurePerievents/'+test+'/'+measure+'/'+event]:
              path = 'MeasurePerievents/'+test+'/'+measure+'/'+event+'/'+onoffset+'/'+mouse
              if path+'/'+trial in f:
                self.measurePerievents[measure][event][onoffset] = np.array(f[path].get(trial))
              else:
                self.measurePerievents = {}
                break
            else:
              continue
            break

    return print('The recording for mouse {} in the experiment {}-{} is successfully loaded.'.format(mouse,test,trial))




  def getDFF(self,
            smooth=True,smooth_filter='low-pass',smooth_parameter=1,
            remove_slope=True,airpls_lambda=1e4,absolute_intensities=False,
            remove_beginning=True,remove=10,
            standardize=True,
            model='Lasso',
            interpolate=False,period=0.1,
            plot=False,figsize=(20,13),save=False,image_format='.pdf'):

    self.preprocess(smooth,smooth_filter,smooth_parameter,
                    remove_slope,airpls_lambda,absolute_intensities,
                    remove_beginning,remove,standardize,
                    plot,figsize,save,image_format)

    self.align(model,plot,figsize,save,image_format)

    self.calculateDFF(standardize,plot,figsize,save,image_format)

    if interpolate:
      self.interpolateDFF(period)

    plt.close('all')




  def getPerievents(self,info_for_array=None,
                    plot=False,save=False,image_format='.pdf'):
    
    import numpy as np
    
    if self.timeDFF is not None:
      time_ = self.timeDFF
    else:
      time_ = self.time

   # Adjust events   
   # Remove events that are at the beginning of dF/F where are NANs
    dFF = self.dFFs[list(self.dFFs.keys())[0]]    
    idx = np.max(np.argwhere(np.isnan(dFF))) + 1
    events = self.events
    for event in events:
      e = events[event]
      if e.size != 0:
        events[event] = e[np.all(e > time_[idx], axis=1)]
    
    self.perievents = {}
    for output in self.outputs:
      self.perievents[output] = {}

    if self.measurements is not None:
      self.measurePerievents = {}
      for measure in self.measurements:
        m = self.measurements[measure]['values']
        if not isbinary(m):
          self.measurePerievents[measure] = {}

    period = find_avg_period(time_)

    cmap = get_cmap(len(self.events))

    for k,event in enumerate(self.events):

      if self.events[event].size != 0:

        try:
          window = info_for_array[event]['window']
        except:
          window = [-5.0,5.0]
        try: 
          dur = info_for_array[event]['duration']
        except:
          dur = None
        try:
          iei = info_for_array[event]['interval']
        except:
          iei = None
        try:    
          avg_win = info_for_array[event]['avg_frame']
        except:
          avg_win = None
        try:    
          figsize = info_for_array[event]['figsize']
        except:
          figsize = None  

        for output in self.dFFs:
          Array = create_perievents(self.dFFs[output],time_,events[event],
                                  window,dur,iei,avg_win)
          self.perievents[output][event] = Array
            
        if self.measurements is not None:
          for measure in self.measurements:
            measure_values = self.measurements[measure]['values']
            measure_time = self.measurements[measure]['time']
            if not isbinary(measure_values):
              Array1 = create_perievents(measure_values,measure_time,events[event],
                                        window,dur,iei)
              self.measurePerievents[measure][event] = Array1
            
      # Plot if asked 
        if plot:
          
          plt.close('all')

          if save:
            create_folder('./figures')
            create_folder('./figures/5_mean')
          for output in self.outputs:
            Array = self.perievents[output][event]
            if self.measurePerievents is not None:
              for measure in self.measurePerievents:
                Array1 = self.measurePerievents[measure][event]
                period1 = find_avg_period(self.measurements[measure]['time'])
                figtitle = self.mouse + ' ' + output + ' ' + self.test + \
                          self.trial + ' ' + event + ' ' + measure
                plot_perievents(Array,period,Array1,period1,
                                window,cmap(k),figtitle,figsize,
                                save,'./figures/5_mean/',image_format)
            else:
              figtitle = self.mouse + ' ' + output + ' ' + self.test + self.trial + ' ' + event 
              plot_perievents(Array,period,window=window,
                              color=cmap(k),figtitle=figtitle,figsize=figsize,
                              save=save,save_path='./figures/5_mean/',
                              image_format=image_format)
          
    plt.close('all')
    


  def preprocess(self,
                 smooth=True,smooth_filter='low-pass',smooth_parameter=1,
                 remove_slope=True,airpls_lambda=1e4,absolute_intensities=False,
                 remove_beginning=True,remove=10,
                 standardize=True,
                 plot=False,figsize=(24,13),
                 save=False,image_format='.pdf'):
  
    self.signals = self.rawSignals.copy()
    self.references = self.rawReferences.copy()

   # Smooth
    if smooth:
      self.smooth(smooth_filter,smooth_parameter)

   # Remove the slope
    if remove_slope:
      s_slope,r_slope = self.removeSlope(airpls_lambda,absolute_intensities)

   # Remove the begining
    if remove_beginning:
      self.removeBeginning(remove)

   # Standardize signal to mean 0 and std 1
    if standardize:
      self.standardize()

            
   # Plot and save if needed
    if save:
      create_folder('figures')
      create_folder('figures/1_raw')

    if plot:
      for output in self.outputs:  
        
        figtitle = self.mouse + ' ' + output + ' ' + self.test + self.trial

        plot_raw(self.rawSignals[output],self.rawReferences[output],
                self.signals[output],self.references[output],
                s_slope[output],r_slope[output],
                self.time,self.events,self.measurements,
                figtitle,figsize,save,'./figures/1_raw/',image_format)



  def smooth(self, smooth_filter='low-pass',smooth_parameter=1,take_raw=False):
        
    if smooth_filter not in ['low-pass','moving average']:
      raise TypeError('Argument smooth_filter can be only "low-pass" or "moving average".')

    if take_raw or self.signals is None:
      self.signals = self.rawSignals.copy()
      self.references = self.rawReferences.copy()

    for output in self.outputs:

      s = self.signals[output].copy()
      r = self.references[output].copy()

     # Smooth 
      if smooth_filter=='moving average':
        s = smooth_signal(s,window_len=int(smooth_parameter/self.period))
        r = smooth_signal(r,window_len=int(smooth_parameter/self.period))

      elif smooth_filter=='low-pass':
        cutoff = smooth_parameter
        f = int(round(self.frequency))
        s = butter_lowpass_filter(s, cutoff, f, order=5)
        r = butter_lowpass_filter(r, cutoff, f, order=5)  

      self.signals[output] = s
      self.references[output] = r



  def removeSlope(self, airpls_lambda=1e4,absolute_intensities=False,take_raw=False):

    if take_raw or self.signals is None:
      self.signals = self.rawSignals.copy()
      self.references = self.rawReferences.copy()

    s_slope = {}
    r_slope = {}

    for output in self.outputs:

      s = self.signals[output].copy()
      r = self.references[output].copy()

      s, s_slope[output] = flatten_signal(s,lambda_=airpls_lambda)
      r, r_slope[output] = flatten_signal(r,lambda_=airpls_lambda)
        
      if absolute_intensities:
        s = s + min(s_slope)
        r = r + min(r_slope)

      self.signals[output] = s
      self.references[output] = r

    return s_slope,r_slope



  def removeBeginning(self, remove=10,take_raw=False):

    import numpy as np    

    if take_raw or self.signals is None:
      self.signals = self.rawSignals.copy()
      self.references = self.rawReferences.copy()

    for i,t in enumerate(self.time):
      if t > remove:
        i0 = i-1
        break

    for output in self.outputs:
        
      self.signals[output][:i0] = np.nan
      self.references[output][:i0] = np.nan




  def standardize(self, take_raw=False):

    if take_raw or self.signals is None:
      self.signals = self.rawSignals.copy()
      self.references = self.rawReferences.copy()
  
    for output in self.outputs:

      self.signals[output] = standardize_signal(self.signals[output])
      self.references[output] = standardize_signal(self.references[output])




  def align(self, model='Lasso',
            plot=False,figsize=(24,13),
            save=False,image_format='.pdf'):

    for output in self.outputs:

      r_fitted = fit_signal(self.signals[output],self.references[output],model)

      if plot:
        plt.close('all')

        figtitle = self.mouse + ' ' + output + ' ' + self.test + self.trial

        if save:
          create_folder('figures')
          create_folder('figures/2_fit')
          create_folder('figures/3_align')

        plot_fit(self.signals[output],self.references[output],r_fitted,
                figtitle,(15,13),save,'./figures/2_fit/',image_format)
        plot_aligned(self.signals[output],r_fitted,self.time,self.events,self.measurements,
                    figtitle,figsize,save,'./figures/3_align/',image_format)
    
      self.references[output] = r_fitted



  def calculateDFF(self,standardized=True,
                   plot=False,figsize=(24, 13),save=False,image_format='.pdf'):
    
    self.dFFs = {}

    for output in self.outputs:
 
      self.dFFs[output] = calculate_dff(self.signals[output],self.references[output])

      if plot:
        plt.close('all')

        figtitle = self.mouse + ' ' + output + ' ' + self.test + self.trial

        if save:
          create_folder('figures')
          create_folder('figures/4_dFF')
        
        plot_dff(self.dFFs[output],self.time,self.events,self.measurements,
                figtitle,figsize,save,'./figures/4_dFF/',image_format)




  def interpolateDFF(self,period=0.1):
    
    import numpy as np

    time_ = self.time

    for output in self.outputs:

      signal = self.dFFs[output]

      i_nans = np.argwhere(np.isnan(signal))
      if i_nans.size != 0:
        i0 = np.max(i_nans) + 1
        t_nans = np.arange(0,time_[i0],period)
        t0 = np.max(t_nans) + period
        t1 = np.max(time_)
        t_new = np.arange(t0,t1,period)
        intrp_signal = interpolate_signal(signal[i0:],time_[i0:],t_new)
        nans = np.empty((len(t_nans),))
        nans[:] = np.nan
        new_signal = np.r_[nans,intrp_signal]
        new_time = np.r_[t_nans,t_new]
      else:
        t_new = np.arrange(0,time[-1],period)
        signal = interpolate_signal(signal,time_,t_new)

      self.dFFs[output] = new_signal
      self.timeDFF = new_time




  def smoothMeasurements(self,smooth_filter='low-pass',smooth_win=1):
    
    import numpy as np

    for measure in self.measurements:
      if not isbinary(self.measurements[measure]['values']):

        m = self.measurements[measure]['values']
        t = self.measurements[measure]['time']

        T = find_avg_period(t)

        i_nans = np.argwhere(np.isnan(m))
        if i_nans.size != 0:
          i0 = np.max(i_nans) + 1
          m = m[i0:]
          nans = m[:i0]

      
        if smooth_filter=='moving average':
          m = smooth_signal( m, window_len=int(round(smooth_win/T)) )

        elif smooth_filter=='low-pass':
          cutoff = 1 / smooth_win
          f = 1 / T
          m = butter_lowpass_filter(m, cutoff, f, order=10)


        if i_nans.size != 0:
          m = np.r_[nans,m]

        self.measurements[measure]['values'] = m




  def interpolateMeasurements(self,period=0.1):
    
    import numpy as np

    for measure in self.measurements:
      if not isbinary(self.measurements[measure]['values']):

        signal = self.measurements[measure]['values']
        time_ = self.measurements[measure]['time']

        if time_[0] < 0:
          i0 = np.max(np.argwhere(time_<0))
          signal = signal[i0:]
          time_ = time_[i0:]

        i_nans = np.argwhere(np.isnan(signal))
        if i_nans.size != 0:
          i0 = np.max(i_nans) + 1
          t_nans = np.arange(0,time_[i0],period)
          t0 = np.max(t_nans) + period
          t1 = np.max(time_)
          t_new = np.arange(t0,t1,period)
          intrp_signal = interpolate_signal(signal[i0:],time_[i0:],t_new)
          nans = np.empty((len(t_nans),))
          nans[:] = np.nan
          new_signal = np.r_[nans,intrp_signal]
          new_time = np.r_[t_nans,t_new]
        else:
          if time_[0] > 0:
            t_nans = np.arange(0,time_[0]+period,period)
            t0 = np.max(t_nans) + period
            t1 = np.max(time_)
            t_new = np.arange(t0,t1,period)
            intrp_signal = interpolate_signal(signal,time_,t_new)
            nans = np.empty((len(t_nans),))
            nans[:] = np.nan
            new_signal = np.r_[nans,intrp_signal]
            new_time = np.r_[t_nans,t_new]
          else:
            new_time = np.arange(0,time_[-1],period)
            new_signal = interpolate_signal(signal,time_,new_time)

        self.measurements[measure]['values'] = new_signal
        self.measurements[measure]['time'] = new_time





  def plotExample(self,outputs,event=None,measure=None,t0=0,t1=90,**kwargs):
    
    import numpy as np

    if self.timeDFF is not None:
      time_ = self.timeDFF
    else:
      time_ = self.time

    i0 = find_idx(t0,time_)
    i1 = find_idx(t1,time_)

    time_ = time_[i0:i1] - t0

    dFF1 = None
    dFF2 = None
    for i,output in enumerate(outputs):
      if i==0:
        dFF = self.dFFs[output][i0:i1]
      elif i==1:
        dFF1 = self.dFFs[output][i0:i1]
      elif i==2:
        dFF2 = self.dFFs[output][i0:i1]

    events = None
    if event is not None:
      events = self.events[event]
      events = events[np.all(events > t0, axis=1)]
      events = events[np.all(events < t1, axis=1)]
      events = events - t0

    measurement = None
    time_m = None
    if measure is not None:
      measurement = self.measurements[measure]['values']
      time_m = self.measurements[measure]['time']

      j0 = find_idx(t0,time_m)
      j1 = find_idx(t1,time_m)

      measurement = measurement[j0:j1]
      time_m = time_m[j0:j1]

  
    plot_example(dFF,time_,events,dFF1,dFF2,measurement,time_m,**kwargs)