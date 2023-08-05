def find_idx(t, time_vector, time_format='total seconds'):

  if time_format == 'real time':
    time_vector = np.array([(pd.Timedelta(t)-t0).total_seconds() for t in time_vector])
  
  elif time_format == 'total seconds':
    time_vector = np.array(time_vector)

  idx = (np.abs(time_vector-t)).argmin()

  return idx 



def find_avg_period(t, time_format='total seconds'):

  if time_format=='real time':
    t = time_to_seconds(t, t[0])

  dt = np.diff(t)

  T = np.median(dt)

  T = round(T,10)

  return T



def time_to_seconds(t, t0=None):

  if t0 is not None:
    t = np.array([(pd.Timedelta(x)-pd.Timedelta(t0)).total_seconds() for x in t])
  else:
    t = np.array([pd.Timedelta(x).total_seconds() for x in t])

  return t




def create_realtime(hh,mm,ss,ms):
  
 # Hours
  if hh is not list:
    hh = hh*np.ones(len(mm),dtype=int)
    dif_mm = np.diff(mm)
    hour_change = [i+1 for i in range(len(dif_mm)) if dif_mm[i]<0]
    if len(hour_change) != 0:
      for i in hour_change:
        hh[i:] = [h+1 for h in hh[i:]]
    hh = [str(int(h)) for h in hh]

 # Minutes
  for i in range(len(mm)):
    if mm[i]<10:
      mm[i] = '0'+str(int(mm[i]))
    else:
      mm[i] = str(int(mm[i]))
 
 # Seconds
  for i in range(len(ss)):
    if ss[i]<10:
      ss[i] = '0'+str(int(ss[i]))
    else:
      ss[i] = str(int(ss[i]))
 
 # Miliseconds
  for i in range(len(ms)):
    if ms[i]<10:
      ms[i] = '00'+str(int(ms[i]))
    elif ms[i]<100:
      ms[i] = '0'+str(int(ms[i]))
    else:
      ms[i] = str(int(ms[i]))

  realtime = [h+':'+m+':'+s+'.'+x for h,m,s,x in zip(hh,mm,ss,ms)]

  return realtime
