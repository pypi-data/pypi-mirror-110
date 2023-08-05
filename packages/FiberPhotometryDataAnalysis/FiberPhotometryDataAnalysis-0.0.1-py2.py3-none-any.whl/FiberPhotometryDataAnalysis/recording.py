class recording:

  '''
    A class used to represent a Fiber Photometry Recording
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


  import h5py
  import numpy as np
  import pandas as pd

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