def get_cmap(n, name='gist_rainbow'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)



def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)



def plot_raw(raw_signal,raw_reference,signal,reference,s_base,r_base,
            time_=None,events=None,measurements=None,
            figtitle=None,figsize=(22, 13),
            save=False,save_path='',image_format='.pdf'):

  if time_ is None:
    time_ = range(len(raw_signal))

  if (measurements is None) or arebinary(measurements):
   # Create figure
    fig, axs = plt.subplots(2,2,figsize=figsize)
    axs = axs.ravel()
   # Plot recordings
    axs[0].plot(time_,raw_signal, color='blue', linewidth=1.5)
    axs[0].plot(time_,s_base, color='black', linewidth=1.5)
    axs[0].set_ylabel('signal', fontsize='x-large', multialignment='center')
    axs[1].plot(time_,signal, color='blue',linewidth=1.5)

    axs[2].plot(time_,raw_reference, color='purple', linewidth=1.5)
    axs[2].plot(time_,r_base, color='black', linewidth=1.5)
    axs[2].set_ylabel('reference', fontsize='x-large', multialignment='center')
    axs[3].plot(time_,reference, color='purple',linewidth=1.5)

    axs[2].set_xlabel('time', fontsize='x-large', multialignment='center')
    axs[3].set_xlabel('time', fontsize='x-large', multialignment='center')

   # Plot events
    if events is not None:
      cmap = get_cmap(len(events))
      for k,key in enumerate(events): # plot all events
      # if it's empty
        if len(events[key])==0:
          pass
        else:
          for ax in axs:
          # one occurance event
            if events[key].shape[1]==1:
              for event in events[key]:
                ax.axvline(event,linewidth=1,color=cmap(k),label=key)
          # event with onset and offset     
            elif events[key].shape[1]==2:
              for event0,event1 in events[key]:
                ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
   # X-ticks
    for ax in axs:
      ax.set_xlim([0,max(time_)])
      ax.tick_params(labelsize='large')
   # Legend
    for ax in axs:    
      handles, labels = ax.get_legend_handles_labels()
      by_label = OrderedDict(zip(labels, handles))
      ax.legend(by_label.values(), by_label.keys(), prop={'size': 'small'})
  
   # Title
    if figtitle is not None:
      fig.suptitle(figtitle, fontsize='xx-large')
    
   # Save figure
    if save:
      imgname = figtitle.replace(' ','_') + '_raw' + image_format
      fig.savefig(save_path+imgname)

  else:
    for measure in measurements:
      if not isbinary(measurements[measure]['values']):
       # Create figure
        fig, axs = plt.subplots(2,2,figsize=figsize)
        axs = axs.ravel()
       # Plot recordings
        axs[0].plot(time_,raw_signal, color='blue', linewidth=1.5)
        axs[0].plot(time_,s_base, color='black', linewidth=1.5)
        axs[0].set_ylabel('signal', fontsize='x-large', multialignment='center')

        axs[1].plot(time_,signal, color='blue',linewidth=1.5)

        axs[2].plot(time_,raw_reference, color='purple', linewidth=1.5)
        axs[2].plot(time_,r_base, color='black', linewidth=1.5)
        axs[2].set_ylabel('reference', fontsize='x-large', multialignment='center')
        axs[2].set_xlabel('time', fontsize='x-large', multialignment='center')
        
        axs[3].plot(time_,reference, color='purple',linewidth=1.5)      
        axs[3].set_xlabel('time', fontsize='x-large', multialignment='center')

       # Plot events
        cmap = get_cmap(len(events))
        for k,key in enumerate(events): # plot all events
         # if it's empty
          if len(events[key])==0:
            pass
          else:
            for ax in axs:
            # one occurance event
              if events[key].shape[1]==1:
                for event in events[key]:
                  ax.axvline(event,linewidth=1,color=cmap(k),label=key)
            # event with onset and offset     
              elif events[key].shape[1]==2:
                for event0,event1 in events[key]:
                  ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
      # Plot continious measurements
        if not np.array_equal(measurements[measure]['values'], measurements[measure]['values'].astype(bool)):
          for ax in axs:
            ax_m = ax.twinx()
            ax_m.plot(measurements[measure]['time'], measurements[measure]['values'], color='black',label=key)
            ax_m.set_ylabel(measure,fontsize='x-large',multialignment='center',color='black')
            ax_m.tick_params('y', colors='black')
            m_max = np.nanmax(measurements[measure]['values'])
            m_min = np.nanmin(measurements[measure]['values'])
            ax_m.set_ylim([m_min, m_max + (m_max-m_min)]) # plot on the bottom half
            ax.set_zorder(ax_m.get_zorder()+1) # put ax in front of ax_m
            ax.patch.set_visible(False) # hide the 'canvas'
      # X-ticks
        for ax in axs:
          ax.set_xlim([0,max(time_)])
          ax.tick_params(labelsize='large')
      # Legend
        for ax in axs:    
          handles, labels = ax.get_legend_handles_labels()
          by_label = OrderedDict(zip(labels, handles))
          ax.legend(by_label.values(), by_label.keys(), prop={'size': 'small'})   
      # Title
        if figtitle is not None:
          fig.suptitle(figtitle, fontsize='xx-large')
        
      # Save figure
        if save:
          if figtitle is None:
            imgname = 'raw' + image_format
          else:
            imgname = figtitle.replace(' ','_') + '_' + measure + '_raw' + image_format
          fig.savefig(save_path+imgname)



def plot_fit(signal,reference,reference_fitted,
             figtitle=None,figsize=(15,13),save=False,save_path='',image_format='.pdf'):
  
  fig = plt.figure(figsize=figsize)
  ax = fig.add_subplot(111)
  ax.plot(reference,signal,'b.')
  ax.plot(reference,reference_fitted, 'r--',linewidth=1.5)
  ax.set_xlabel('reference', fontsize='x-large', multialignment='center')
  ax.set_ylabel('signal', fontsize='x-large', multialignment='center')
  ax.tick_params(labelsize='large')
 # Title
  if figtitle is not None:
    fig.suptitle(figtitle, fontsize='xx-large')
  
  # Save figure
  if save:
    if figtitle is None:
      imgname = 'fit' + image_format
    else:
      imgname = figtitle.replace(' ','_') + '_fit' + image_format
    fig.savefig(save_path+imgname)




def plot_aligned(signal,reference,time_=None,events=None,measurements=None,
                 figtitle=None,figsize=(20,13),save=False,save_path='',image_format='.pdf'):
  
  if time_ is None:
    time_ = range(len(signal))

  if (measurements is None) or arebinary(measurements):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
   # Signal
    ax.plot(time_, signal, 'black' ,linewidth=1.5)
    ax.plot(time_, reference, 'purple',linewidth=1.5)
   # Events
    if events is not None:
      cmap = get_cmap(len(events))
      for k,key in enumerate(events): # plot all events
        if len(events[key])==0:
          pass
        # one occurance event
        elif events[key].shape[1]==1:
          for event in events[key]:
            ax.axvline(event,linewidth=1,color=cmap(k),label=key)
        # event with onset and offset     
        elif events[key].shape[1]==2:
          for event0,event1 in events[key]:
            ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
   # Params
    ax.set_xlabel('time', fontsize='x-large', multialignment='center')
    ax.set_ylabel('Intensity', fontsize='x-large', multialignment='center')
    ax.set_xlim([0,max(time_)])
    ax.tick_params(labelsize='x-large')
   # Legend    
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), prop={'size': 'medium'})
   # Title
    if figtitle is not None:
      fig.suptitle(figtitle, fontsize='xx-large')
    
   # Save figure
    if save:
      imgname = figtitle.replace(' ','_') +'_align' + image_format
      fig.savefig(save_path+imgname)


  else:
    for measure in measurements:
      if not isbinary(measurements[measure]['values']):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
      # Signal
        ax.plot(time_, signal, 'black' ,linewidth=1.5)
        ax.plot(time_, reference, 'purple',linewidth=1.5)
      # Events
        cmap = get_cmap(len(events))
        for k,key in enumerate(events): # plot all events
          if len(events[key])==0:
            pass
         # one occurance event
          elif events[key].shape[1]==1:
            for event in events[key]:
              ax.axvline(event,linewidth=1,color=cmap(k),label=key)
         # event with onset and offset     
          elif events[key].shape[1]==2:
            for event0,event1 in events[key]:
              ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
      # Measurements
        ax_m = ax.twinx()
        ax_m.plot(measurements[measure]['time'], measurements[measure]['values'], color=cmap(k),label=key)
        ax_m.set_ylabel(measure,fontsize='x-large',multialignment='center',color=cmap(k))
        ax_m.tick_params('y', colors=cmap(k))
        m_max = np.nanmax(measurements[measure]['values'])
        m_min = np.nanmin(measurements[measure]['values'])
        ax_m.set_ylim([m_min, m_max + (m_max-m_min)]) # plot on the bottom half
        ax.set_zorder(ax_m.get_zorder()+1) # put ax in front of ax_e
        ax.patch.set_visible(False) # hide the 'canvas'
      # Params
        ax.set_xlabel('time', fontsize='x-large', multialignment='center')
        ax.set_ylabel('Intensity', fontsize='x-large', multialignment='center')
        ax.set_xlim([0,max(time_)])
        ax.tick_params(labelsize='x-large')
      # Legend    
        handles, labels = ax.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), prop={'size': 'medium'})
      # Title
        if figtitle is not None:
          fig.suptitle(figtitle, fontsize='xx-large')
        
      # Save figure
        if save:
          if figtitle is None:
            imgname = 'align' + image_format
          else:
            imgname = figtitle.replace(' ','_') + '_'+ measure +'_align' + image_format
          fig.savefig(save_path+imgname)
          
          
          
def plot_dff(dFF,time_=None,events=None,measurements=None,
            figtitle=None,figsize=(20,13),save=False,save_path='',image_format='.pdf'):

  if time_ is None:
    time_ = range(len(dFF))

  ymin = np.nanmin([-3, np.nanmin(dFF)])
  ymax = np.nanmax([3, np.nanmax(dFF)])

  if (measurements is None) or arebinary(measurements):
   # Figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
   # Signal
    ax.plot(time_, dFF, 'black' ,linewidth=1.5)
   # Events
    if events is not None:
      cmap = get_cmap(len(events))
      for k,key in enumerate(events): # plot all events
        if len(events[key])==0:
          pass
      # one occurance event
        elif events[key].shape[1]==1:
          for event in events[key]:
            ax.axvline(event,linewidth=1,color=cmap(k),label=key)
      # event with onset and offset     
        elif events[key].shape[1]==2:
          for event0,event1 in events[key]:
            ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
   # Params
    ax.set_xlabel('time', fontsize='x-large', multialignment='center')
    ax.set_ylabel('dF/F', fontsize='x-large', multialignment='center')
    ax.set_xlim([0,max(time_)])
    ax.set_ylim([ymin, ymax])
    ax.tick_params(labelsize='large')
   # Legend    
    handles, labels = ax.get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), prop={'size': 'medium'})
   # Title
    if figtitle is not None:
      fig.suptitle(figtitle, fontsize='xx-large')

   # Save figure
    if save:
      imgname = figtitle.replace(' ','_') +'_dFF' + image_format
      fig.savefig(save_path+imgname)

  else:
    for measure in measurements:
      if not isbinary(measurements[measure]['values']):
      # Figure
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
      # Signal
        ax.plot(time_, dFF, 'black' ,linewidth=1.5)
      # Events
        cmap = get_cmap(len(events))
        for k,key in enumerate(events): # plot all events
          if len(events[key])==0:
            pass
        # one occurance event
          elif events[key].shape[1]==1:
            for event in events[key]:
              ax.axvline(event,linewidth=1,color=cmap(k),label=key)
        # event with onset and offset     
          elif events[key].shape[1]==2:
            for event0,event1 in events[key]:
              ax.axvspan(event0,event1,alpha=0.3,color=cmap(k),label=key)
      # Measurements
        ax_m = ax.twinx()
        ax_m.plot(measurements[measure]['time'], measurements[measure]['values'], color=cmap(k),label=key)
        ax_m.set_ylabel(measure,fontsize='x-large',multialignment='center',color=cmap(k))
        ax_m.tick_params('y', colors=cmap(k))
        m_max = np.nanmax(measurements[measure]['values'])
        m_min = np.nanmin(measurements[measure]['values'])
        ax_m.set_ylim([m_min, m_max + (m_max-m_min)]) # plot on the bottom half
        ax.set_zorder(ax_m.get_zorder()+1) # put ax in front of ax_e
        ax.patch.set_visible(False) # hide the 'canvas'
      # Params
        ax.set_xlabel('time', fontsize='x-large', multialignment='center')
        ax.set_ylabel('dF/F', fontsize='x-large', multialignment='center')
        ax.set_xlim([0,max(time_)])
        ax.set_ylim([ymin, ymax])
        ax.tick_params(labelsize='large')
      # Legend    
        handles, labels = ax.get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), prop={'size': 'medium'})
      # Title
        if figtitle is not None:
          fig.suptitle(figtitle, fontsize='xx-large')

      # Save figure
        if save:
          if figtitle is None:
            imgname = 'dFF' + image_format
          else:
            imgname = figtitle.replace(' ','_') + '_'+ measure +'_dFF' + image_format
          fig.savefig(save_path+imgname)
          
          
          
          
def plot_perievents(Array,period=0.10,
                    Array1=None,period1=None,
                    window=[-5.0,5.0],color='green',
                    figtitle=None,figsize=None,
                    save=False,save_path='',image_format='.pdf'):

  Mean = {}
  Error = {}
  for key in Array:
    Mean[key] = np.nanmean(Array[key],axis=0)
    Error[key] = np.nanstd(Array[key],axis=0) / np.sqrt(Array[key].shape[0])
  
  ymax = 2
  ymin = -2
  for key in Array:
    ymax = max(ymax,1.1*Array[key].max())
    ymin = min(ymin,1.1*Array[key].min())

  ts = create_centered_time_vector(period,window)

  if Array1 is not None:
    Mean1 = {}
    Error1 = {}
    for key in Array1:
      Mean1[key] = np.nanmean(Array1[key],axis=0)
      Error1[key] = np.nanstd(Array1[key],axis=0) / np.sqrt(Array1[key].shape[0])

    ymax1 = max( [Array1[key1].max() for key1 in Array1.keys()] )
    ymin1 = min( [Array1[key1].min() for key1 in Array1.keys()] )
    std1 = np.nanstd( [np.nanstd(Array1[key1]) for key1 in Array1.keys()] )

    ts1 = create_centered_time_vector(period,window)

  if figsize is None:
    if len(Array) == 1:
      figsize = (12,10)
    else:
      figsize = (20,10)

  from matplotlib import gridspec

  fig = plt.figure(figsize=figsize)
  gs = gridspec.GridSpec(1, len(Array))
  for i,key in enumerate(Array):
    ax = fig.add_subplot(gs[i])  
    ax.set_title(key, fontsize='xx-large')
    ax.plot(ts,Array[key].T,color=color,alpha=0.5,linewidth=1)
    ax.plot(ts,Mean[key],color=color,linewidth=2)
    ax.fill_between(ts, Mean[key]-Error[key],Mean[key]+Error[key],
                    alpha=0.3,edgecolor=color,facecolor=color,linewidth=0)
    ax.axvline(0,linestyle='--',color='black',linewidth=1.5)
    ax.set_xlabel('time', fontsize='xx-large', multialignment='center')
    ax.set_ylabel('z dF/F', fontsize='xx-large', multialignment='center')
    ax.set_ylim([ymin,ymax])
    ax.set_xlim(window)
    ax.tick_params(labelsize='x-large')
    if Array1 is not None:
      ax_m = ax.twinx()
      ax_m.plot(ts1,Array1[key].T,color='black',alpha=0.5,linewidth=1)
      ax_m.plot(ts1,Mean1[key],color='black',linewidth=2)
      ax_m.fill_between(ts1, Mean1[key]-Error1[key], Mean1[key]+Error1[key],
                    alpha=0.3,edgecolor='black',facecolor='black',linewidth=0)
      ax_m.set_ylim([ymin1, ymax1 + std1]) # plot on the bottom half
      ax.set_zorder(ax_m.get_zorder()+1) # put ax in front of ax_m
      ax.patch.set_visible(False) # hide the 'canvas'
  # Title
  if figtitle is not None:
    fig.suptitle(figtitle, fontsize='xx-large')

 # Save figure
  if save:
    if figtitle is None:
      imgname = 'mean' + image_format
    else:
      imgname = figtitle.replace(' ','_') +'_mean' + image_format
    fig.savefig(save_path+imgname)
    
    
    
    
    
def plot_example(dFF,time_,events=None,dFF1=None,dFF2=None,measurement=None,time_m=None,
                 color='purple',ylim=None,yticks=None,ylabel=None,xticks=None,
                 color1='blue',ylim1=None,yticks1=None,ylabel1=None,
                 color2='red',ylim2=None,yticks2=None,ylabel2=None,
                 color_m='magenta',ylim_m=None,yticks_m=None,
                 color_e='red',
                 figsize=(5,3),save=False,imgname='example.pdf'):

  fig = plt.figure(figsize=figsize)
  sns.set(style='ticks')

  if measurement is not None:
    from matplotlib import gridspec
    gs = gridspec.GridSpec(2,1, height_ratios=[1,3])
      
    ax_m = fig.add_subplot(gs[0])
    sns.lineplot(x=time_m,y=measurement,color=color_m)

    ax_m.set_xticks([])
    make_patch_spines_invisible(ax_m)
    ax_m.spines['right'].set_visible(True)
    ax_m.yaxis.set_ticks_position('right')
    ax_m.yaxis.set_label_position('right')

    ax_m.spines['right'].set_color('magenta')
    ax_m.set_ylabel('Mobility\n score',color=color_m)
    ax_m.tick_params(axis='y', colors=color_m)

    ax_m.set_xlim(time_m[0], time_m[-1])
    if ylim_m is not None:
      ax_m.set_ylim(ylim_m)
    if yticks_m is not None:
      ax_m.set_yticks(yticks_m)

    ax = fig.add_subplot(gs[1])

  else:
    ax = fig.add_subplot()

  sns.lineplot(x=time_,y=dFF,color=color,ax=ax)

  if events is not None:
    if events.shape[1]==1:
      for e0 in events:
        ax.axvline(e0,linestyle='--',color='black')
    elif events.shape[1]==2:
      for e0,e1 in events:
        ax.axvspan(e0,e1,color=color_e,alpha=0.3)

  ax.spines['top'].set_visible(False)
  ax.spines['right'].set_visible(False)

  ax.spines['left'].set_color(color)
  ax.yaxis.label.set_color(color)
  ax.tick_params(axis='y',colors=color)

  ax.set_xlabel('Time (s)',fontsize='large')
  ax.set_ylabel('z dF/F',fontsize='large',color='black')

  ax.set_xlim(time_[0],time_[-1])
  if xticks is not None:
    ax.set_xticks(xticks)
  if ylim is not None:
    ax.set_ylim(ylim)
  if yticks is not None:
    ax.set_yticks(yticks)
  if ylabel is not None:
    ax.set_ylabel(ylabel,fontsize='large',color=color)

  if dFF1 is not None:
    ax1 = ax.twinx()
    sns.lineplot(x=time_,y=dFF1,color=color1,ax=ax1)

    if ylim1 is not None:
      ax1.set_ylim(ylim1)
    if yticks1 is not None:
      ax1.set_yticks(yticks1)
    if ylabel1 is not None:
      ax1.set_ylabel(ylabel1,fontsize='large',color=color1)

    make_patch_spines_invisible(ax1)
    ax1.spines['right'].set_visible(True)

    ax1.spines['right'].set_color(color1)
    ax1.yaxis.label.set_color(color1)
    ax1.tick_params(axis='y',colors=color1)


  if dFF2 is not None:
    ax2 = ax.twinx()  
    sns.lineplot(x=time_,y=dFF2,color=color2,ax=ax2)

    if ylim2 is not None:
      ax2.set_ylim(ylim2)
    if yticks2 is not None:
      ax2.set_yticks(yticks2)
    if ylabel2 is not None:
      ax2.set_ylabel(ylabel2,fontsize='large' ,color=color2)

    fig.subplots_adjust(right=0.9)
    ax2.spines['right'].set_position(('axes',1.15))

    make_patch_spines_invisible(ax2)
    ax2.spines['right'].set_visible(True)

    ax2.spines['right'].set_color(color2)
    ax2.yaxis.label.set_color(color2)
    ax2.tick_params(axis='y', colors=color2)

  plt.tight_layout()


  if save:
    fig.savefig(imgname)