import logging
logger = logging.getLogger('')

import numpy as np
import matplotlib.pyplot as plt

import matplotlib.cm

def plot_matrix_as_image(ee, pp, kind='E', normalize=True,outfile=None, cmap=matplotlib.cm.gist_earth,
                         sliders=False, n_levels=30, min_level=None, max_level=None, source_name=None,
                         energy_on_y=True, axis=None, axis_cb=None, colorbar=True, plot_big = False, 
                         scale='log'):
    '''
    :param ee: y-scale (time or energy)
    :param pp: Energy-Phase or Time-Phase matrix (# of rows must equal len(ee))
    :param kind: * 'E' energy phase
                 * 'T' Time-phase
                 * 'NE' energy phase with energy normalized to the cyclotron energy
    :param normalize: normalize each pulse at its average and divide by the standard deviation
    :param outfile: the file to save the figure as image (optional)
    ;param cmap the colormap of matplotlib, defaults to matplotlib.cm.gist_earth
    ;param sliders if True uses sliders
    ;param n_levels the number of linearly spaced contour levels
    ;param min_level the minimum level for contours
    ;param max_level the maximum level for contours
    ;param source_name if not None, it is used as plot title
    ;param energy_on_y (def True) if plotting energy on vertical axis
    ;param axis ,axis_cb The axes to plot the image and colorbar, default None, create a new figure
    ;param colorbar Make the colorbar or not (default True)
    ;plot_big remove name of Energy scale and ticks form y axis default False
    ;scale the scale of energy (default 'log', you can use 'linear')
    :return:
    '''

    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider
    # from matplotlib.widgets import Button

    if pp.shape[0] != len(ee):
        raise ImportError('len(ee) [%d] != # rows pp [%d]' % (len(ee), pp.shape[0]))
    pp1 = pp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pp1[i, :] = (x - m) / s

    phi = np.linspace(0, 1, pp.shape[1])
    if axis is None:
        fig = plt.figure(figsize=(5.5, 4.2))
        axis = plt.gca()
    # if sliders:
    #     plt.subplots_adjust(top=0.82)
    if min_level is None:
        min_level = np.min(pp1)
    if max_level is None:
        max_level = np.max(pp1)
    levels = np.linspace(min_level, max_level, n_levels)
    if energy_on_y:
        cs = axis.contourf(phi, ee, pp1, cmap=cmap, levels=levels,
                           extend="both", zorder=0)
    else:
        cs = axis.contourf(ee, phi, np.transpose(pp1), cmap=cmap, levels=levels,
                           extend="both", zorder=0)
    cs.cmap.set_under('k')
    cs.set_clim(np.min(levels), np.max(levels))
    if colorbar:
        cb = plt.colorbar(cs, ax=axis, cax= axis_cb)

    if energy_on_y:
        axis.set_xlabel('Phase')
        if kind == 'E':
            axis.set_yscale(scale)
            axis.set_ylabel('Energy [keV]')
            if plot_big:
                axis.set_ylabel(None)
                axis.set_yticks([])

        elif kind == 'T':
            axis.set_ylabel('Time [s]')
        elif kind == 'NE':
            axis.set_yscale(scale)
            axis.set_ylabel('$E/E_\\mathrm{Cyc}$')
    else:
        axis.set_ylabel('Phase')
        if kind == 'E':
            axis.set_xscale(scale)
            axis.set_xlabel('Energy [keV]')
        elif kind == 'T':
            axis.set_xlabel('Time [s]')
        elif kind == 'NE':
            axis.set_xscale(scale)
            axis.set_xlabel('$E/E_\\mathrm{Cyc}$')        

    if source_name is not None:
        axis.set_title(source_name)
    if outfile is not None:
        axis.set_savefig(outfile)

    if sliders:
        # Nice to have : slider
        cmin = plt.axes([0.05, 0.95, 0.3, 0.02])
        cmax = plt.axes([0.65, 0.95, 0.3, 0.02])

        smin = Slider(cmin, 'Min', min_level, max_level, valinit=np.min(levels), orientation='horizontal')
        smax = Slider(cmax, 'Max', min_level, max_level, valinit=np.max(levels), orientation='horizontal')
        # areplot = plt.axes([0.4, 0.88, 0.1, 0.05])
        # bnext = Button(areplot, 'Reset', color='0.55', hovercolor='0.9')
        n_levels = 10

        # def reset(x):
        #     smin.reset()
        #     smax.reset()
        # cid = bnext.on_clicked(reset)

        def update(x):
            if smin.val < smax.val:
                cs.set_clim(smin.val, smax.val)

        smin.on_changed(update)
        smax.on_changed(update)

    return axis




def plot_matrix_as_lines(t, pp, dpp, 
                         kind='E', 
                         normalize=True, 
                         offset=2, 
                         n_lines=10, 
                         axis=None, 
                         axis_legend=None,
                         stem='', 
                         phase_on_y = False,
                         log_spacing=True,
                         annotate=True,
                         double_plot=True,
                         x_axis_on_top=False,cmap = plt.cm.magma):
    '''

    :param t: time or energy array
    :param pp: time-phase or energy-phase matrix
    :param dpp: uncertainty on time-phase or energy-phase matrix
    :param kind: 'E' or 'T'
    :param normalize: normalize the pulses to mean and standard deviation
    :param offset: Offset between on profile and the following one
    :return:
    '''

    pt = pp.copy()
    dpt = dpp.copy()
    if normalize:
        for i in range(pp.shape[0]):
            x = pp[i, :]
            dx = dpp[i, :]
            m = np.mean(x)
            s = np.std(x)
            pt[i, :] = (x - m) / s
            dpt[i, :] = dx / s

    import matplotlib.pyplot as plt
    if axis is None:
        fig = plt.figure()
        axis = plt.gca()
    else:
        fig = plt.gcf()

    if x_axis_on_top:
        axis.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        axis.xaxis.set_label_position('top')
        x_range_addition = np.array([0.01,0.0])
    else:
        x_range_addition = np.array([0.01,0.0])

    if double_plot:
        phi = np.linspace(0, 2, 2*pt.shape[1])
        plot_pt = np.tile(pt, 2)
        plot_dpt = np.tile(dpt, 2)
        x_range=np.array([0,2])+x_range_addition
    else:
        phi = np.linspace(0, 1, pt.shape[1])
        plot_pt = pt
        plot_dpt = dpt
        x_range=np.array([0,1])+x_range_addition

    total_offset = 0
    colors = iter(cmap(np.linspace(0, 1, n_lines+1)))

    if log_spacing:
        sample = 10**np.linspace(np.log10(t[0]),np.log10(t[-1]), n_lines)
        ind = np.abs(np.subtract.outer(t, sample)).argmin(0)
    else:
        ind = np.linspace(1,pt.shape[0], n_lines, dtype=int)

    i=0
    for i in ind:
        y = plot_pt[i, :]
        dy = plot_dpt[i, :]
        if np.sum(dy) > 0:
            # if np.sum(y) / np.sqrt(np.sum(dy ** 2)) > 10:
            
            if kind == 'E':
                label = "%.1f keV" % t[i]
            else:
                label = "%.0f s" % ( t[i] - t[0])

            phi_max = np.argmax(y)
            phi_min = np.argmin(y)

            if phase_on_y:
                ebar = axis.errorbar(y+total_offset, phi, yerr=0.5 / pt.shape[1], xerr=dy, linestyle='-',
                                marker='.', label=label,color = next(colors))
                if annotate:
                    axis.text(y[phi_min]+total_offset+0.3, phi[phi_min-2], label,
                         color=ebar[0].get_color())
        
            else:
                ebar = axis.errorbar(phi, y+total_offset, xerr=0.5 / pt.shape[1], yerr=dy, linestyle='-',
                                marker='.', label=label,color = next(colors))
                if annotate:
                    axis.text(phi[phi_max], y[phi_max]+total_offset+0.1, label,
                         color=ebar[0].get_color())
            #print(int(pt.shape[1]/2), phi[int(pt.shape[1]/2)], y[int(pt.shape[1]/2)]+total_offset,)
            total_offset += offset
    
    if normalize:
        ylabel = 'Normalized rate'
    else:
        ylabel = 'Rate per bin'
    
    if phase_on_y:
        axis.set_xlabel(ylabel)
        axis.set_ylabel('Phase')
        axis.set_ylim(x_range)
    else:
        axis.set_ylabel(ylabel)
        axis.set_xlabel('Phase')
        axis.set_xlim(x_range)

    if not annotate:
        if axis_legend is None:
            axis.legend()
        else:
            axis.legend(bbox_to_anchor=(0, -0.1, 1, 1), bbox_transform=axis_legend.transAxes, 
                        borderaxespad=0, borderpad=0, frameon=False)
            axis_legend.axis('off')
    if stem != '':
        fig.savefig(stem+kind+'matrix_as_lines.pdf')


def plot_pf(ee_pulsed, dee_pulsed, 
            pulsed_frac, dpulsed_frac, 
            e_turn, pulsed_fit_low, pulsed_fit_high, 
            noFe, 
            forced_gaussian_centroids,
            ylabel='PF', y_lim=[-0.1, 1.1],
            title=None, ax1=None, ax2=None, scale='linear'):
    """Utility function to plot the pulsed fraction

    Args:
        ee_pulsed (numpy array): energy grid
        dee_pulsed (numpy array):  energy grid uncertainties
        pulsed_frac (numpy array): pulse fraction 
        dpulsed_frac (numpy array): pulse fraction uncertainties
        e_turn (float): energy that divides the two regimes
        pulsed_fit_low (OBJ): spectral fit results (low part)
        pulsed_fit_high (OBJ): spectral fit results (high part, can be None)
        noFe (bool): if Iron line is fitted
        forced_gaussian_centroids (list): initial values for the Gaussian values
        ylabel (str, optional): y-axis label. Defaults to 'PF'.
        y_lim (list, optional): y-axis limits. Defaults to [-0.1, 1.1].
        title (_type_, optional): plot title. Defaults to None.
        ax1 (_type_, optional): axis to draw the PF (if None it makes a new figure). Defaults to None.
        ax2 (_type_, optional): axis to draw residuals (if None it makes a new figure). Defaults to None.
        scale (str, optional): x-axis scale. Defaults to 'linear'.

    Returns:
        OBJ: the current figure instance
    """    

    if e_turn > 0:
        ind_low = ee_pulsed <= e_turn
        ind_high = ee_pulsed > e_turn
    else:
        #all values
        ind_low = ee_pulsed > 0
        #no value
        ind_high = ee_pulsed < 0

    from matplotlib.pyplot import cm
    comps_low = pulsed_fit_low.eval_components(x=ee_pulsed[ind_low])
    bb_low = (pulsed_frac[ind_low] - pulsed_fit_low.best_fit) / dpulsed_frac[ind_low]
    if e_turn> 0 :
        comps_high = pulsed_fit_high.eval_components(x=ee_pulsed[ind_high])
        bb_high = (pulsed_frac[ind_high] - pulsed_fit_high.best_fit) / dpulsed_frac[ind_high]

    col =cm.viridis(np.linspace(0, 1, 6))

    if ax1 is None and ax2 is None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 6.0), sharex=True, gridspec_kw={'height_ratios': [3, 1],
                                                                        'hspace': 0.0}
                                )
    ax1.errorbar(ee_pulsed,pulsed_frac, xerr=dee_pulsed, yerr=dpulsed_frac, linestyle=''
                , fmt='.', color=col[4], label='data')
    ax1.plot(ee_pulsed[ind_low], pulsed_fit_low.best_fit, '-', label='best fit (low)', color=col[0])
    ax1.plot(ee_pulsed[ind_low], comps_low['poly_'], '--', label='Polynomial (low)', color=col[1])
    if e_turn >0 :
        ax1.plot(ee_pulsed[ind_high], pulsed_fit_high.best_fit, '-', label='best fit (high)', color=col[2])
        ax1.plot(ee_pulsed[ind_high], comps_high['poly_'], '--', label='Polynomial (high)', color=col[3])

    ax1.legend(loc='upper left')
    ax1.set_xscale(scale)
    ax2.set_xlabel('E [keV]')
    ax1.set_ylabel(ylabel)
    ax1.set_ylim(y_lim)
    #ax1.set_xlim(x_lim)
    if title is not None and title != '':
        ax1.set_title(title)
    if forced_gaussian_centroids is not None:
        if noFe is False:
            ax1.axvline(6.5, 0,1, linestyle='--', color='cyan')
        for x in forced_gaussian_centroids:
            ax1.axvline(x, 0,1, linestyle='--', color='cyan')

    ax2.set_ylabel('Residuals')
    #ax1.set_ylim(-0.1, 1)
    if e_turn>0:
        ax2.errorbar(ee_pulsed, np.concatenate([bb_low, bb_high]), xerr=dee_pulsed, yerr=1., fmt='.', color=col[2])
    else:
        ax2.errorbar(ee_pulsed, bb_low, xerr=dee_pulsed, yerr=1., fmt='.', color=col[2])

        
    ax2.axhline(y=0, color='k', linestyle='--')
    return plt.gcf()


def plot_harmonics_all(energy, a1 , phi1, a2, phi2, Feline, Ecycl, title = None, stem = None,
                       axis1 = None, axis2 = None, axis3 = None, axis4 = None, include_index = None, scale='log'):
    """ final visual results of the analysis performed on the harmonics
    Args:
        energy: np.2d-array [energy,denergy]
        a1: np.2d-array amplitude, damplitude first harmonics
        phi1: np.2d-array: phases, dphases first harmonics
        a2: np.2d-array amplitude, damplitude first harmonics
        phi2: np.2d-array: phases, dphases first harmonics
        Feline (list (2 el)): _description_
        Ecycl (list (2 el)): _description_
        title (_type_, optional): Figure. Defaults to None.
        stem (_type_, optional): PRefix for output file. Defaults to None.
        axis1 (_type_, optional): a1 axis. Defaults to None. Defaults to None to create a new figure.
        axis2 (_type_, optional): phi2 axis. Defaults to None. Defaults to None to create a new figure.
        axis3 (_type_, optional): A2 axis. Defaults to None. Defaults to None to create a new figure.
        axis4 (_type_, optional): phi2 axis. Defaults to None. Defaults to None to create a new figure.
        include_index (_type_, optional): index to select data. Defaults to None and takes all
        scale (str, optional): X-axis scale. Defaults to 'log'.

    Returns:
        OBJ: current figure instance
    """    

    # 

    if axis1 is None or axis2 is None or axis3 is None or axis4 is None:
        fig, ax = plt.subplots(2, 2, sharex=True, figsize=(8, 6), gridspec_kw={'height_ratios': [1, 1],
                                                                           'hspace': 0.0})
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.3)
    else:
        ax = [[axis1, axis2], [axis3, axis4]]

    if title is not None:
        plt.suptitle(str(title))
    color = iter(plt.cm.viridis(np.linspace(0, 1, 7)))
    #col = next(color)

    ax[0][0] = axis1
    ax[0][1] = axis2
    ax[1][0] = axis3
    ax[1][1] = axis4

    if include_index is None:
        ind = range(energy.shape[1])
    else:
        ind = include_index

    axis1.set_title('1$^\\mathrm{st}$ Harmonic')

    axis1.errorbar(energy[0][ind], a1[0][ind], xerr=energy[1][ind], yerr=a1[1][ind], linestyle='', marker='.', color=next(color),linewidth= 1.1,markersize =3.5 )
    axis3.errorbar(energy[0][ind], phi1[0][ind], xerr=energy[1][ind], yerr=phi1[1][ind], linestyle='', marker='.',color=next(color),linewidth= 1.1,markersize =3.5)
    axis2.errorbar(energy[0][ind], a2[0][ind], xerr=energy[1][ind], yerr=a2[1][ind], linestyle='', marker='.', color=next(color),linewidth= 1.1,markersize =3.5)
    axis4.errorbar(energy[0][ind], phi2[0][ind], xerr=energy[1][ind], yerr=phi2[1][ind], linestyle='', marker='.', color=next(color),linewidth= 1.1,markersize =3.5)

    axis2.set_title('2$^\\mathrm{nd}$ Harmonic')
    axis4.set_ylabel('$\phi_2$')
    axis2.set_ylabel('$A_2$')
    axis3.set_ylabel('$\phi_1$')
    axis1.set_ylabel('$A_1$')


    axis3.set_xlabel('E [keV]')
    axis4.set_xlabel('E [keV]')
    for [aa, bb] in ax[:][:]:
        aa.set_xscale(scale)
        bb.set_xscale(scale)
        plot_energies(aa, Feline, Ecycl)
        plot_energies(bb, Feline, Ecycl)

    #plt.show()
    if stem is not None:
        plt.savefig(stem+'plot_all.pdf')
    return plt.gcf()

def plot_energies(axes,feline,ecycl):
    """It plots vertical shaded bars on axes with fixed colors
        Just a utility

    Args:
        axes (list): list of axes to use
        feline (list (2 el)): central value and semi-width
        ecycl (list (2 el)): central value and semi-width
    """    
    n_colors = 7
    if ecycl is not None:
        n_colors += int((len(ecycl)-2)/2)
    colors = plt.cm.viridis(np.linspace(0,1,n_colors))
    
    col_fe = colors[4]
    if ecycl is not None:
        n_lines = int(len(ecycl)/2)
        for i in range(n_lines):
            col_e = colors[5+i]
            axes.axvspan(ecycl[0+2*i] - ecycl[1+2*i], ecycl[0+2*i] + ecycl[1+2*i], alpha=0.5, color=col_e)
    if feline is not None:
        axes.axvspan(feline[0] - feline[1], feline[0] + feline[1], alpha=0.5, color=col_fe)

latex_figure='''\\begin{figure*}
    \centering
    \includegraphics[width=1.0\linewidth]{%s}
    \caption{Pulse profile main properties for %s. 
        \emph{Panel (a)}: the pulse fraction (green points) and its best-fit model (solid lines),
        polynomial functions are also shown.
        \emph{Panel (b)}: fit residuals.
        \emph{Panels (c--f)}: phases and amplitudes of the first ($A_1$, $\phi_1$) and second ( $A_2$, $\phi_2$) harmonics. 
        Vertical colored bands indicate the energy and width of the Gaussian functions fitted to the pulse fraction.
        \emph{Panel (g)}: a selection of normalized pulse profiles at equally logarithmic spaced energies, horizontally shifted for clarity.
        In each bin, we have normalized the pulse by subtracting the average and dividing by the standard deviation. 
        \emph{Panel (h)}: color-map representation of the normalized pulse profiles as function of energy. Thin lines represent 100 equally spaced contours.
        \emph{Panel (i)}: the cross correlation between the pulse profile in each energy band and the average profile. 
        \emph{Panel (j)}: the corresponding phase lag. Colored vertical bands are as for panels (d--f).
    }
    \label{fig:%s}
\end{figure*}'''

def plot_all_paper(pp_in, dpp_in, ee_pulsed_in,dee_pulsed_in, pulsed_frac_in, dpulsed_frac_in, 
                   e_turn, pulsed_fit_low, pulsed_fit_high, noFe, forced_gaussian_centroids,
                   correlation_in, correlation_error_in,lag_in,lag_error_in,a1,phi1,a2,phi2,feline,ecycl,stem='', title='',
                   ind_selected=None, scale='linear',mark_panels = True, source='', n_levels=20):

    """This function makes a global summary plot. It should be run at the end of the notebook as in the example below.
       Not for general purpose.
    
if pulsed_fit_high is not None:
    e_iron = [pulsed_fit_low.best_values['g1_center'],   pulsed_fit_low.best_values['g1_sigma'] ]
    e_cyc = [pulsed_fit_high.best_values['g1_center'] ,  pulsed_fit_high.best_values['g1_sigma']]
else:
    e_iron = [pulsed_fit_low.best_values['g1_center'] ,  pulsed_fit_low.best_values['g1_sigma']]


_=utils.plot_all_paper(pp, ee_pulsed,dee_pulsed,
                       pulsed_frac,dpulsed_frac,
                   e_change, pulsed_fit_low, pulsed_fit_high, noFe, None,
                   correlation, correlation_error,lag,lag_error,
                    np.array([As,dAs]) ,
                     np.array([phi0, dphases]) ,
                     np.array([A2s, dA2s]),
                     np.array([phi0_2,dphases2]),
                     e_iron,e_cyc,
                       stem = output_dir_figures+'/'+source.replace(' ','_')+obsid,
                       title=source + ' ' + obsid,
                  ind_selected=ind_selected, scale='log', source=source + ' in OBSID ' + obsid )

    Returns:
        OBJ: The current figure instance
    """        
    if ind_selected is None:
        ind_selected = range(len(ee_pulsed_in))
    
    ee_pulsed = ee_pulsed_in[ind_selected]
    dee_pulsed = dee_pulsed_in[ind_selected]
    pulsed_frac = pulsed_frac_in[ind_selected]
    dpulsed_frac = dpulsed_frac_in[ind_selected]
    correlation = correlation_in[ind_selected]
    correlation_error = correlation_error_in[ind_selected]
    lag = lag_in[ind_selected]
    lag_error = lag_error_in[ind_selected]
    pp=pp_in[ind_selected, :]
    dpp=dpp_in[ind_selected, :]


    SMALL_SIZE = 10
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 18

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    from matplotlib.gridspec import GridSpec
    import string
    color = iter(plt.cm.viridis(np.linspace(0, 1, 4)))
    fig = plt.figure(figsize=(11.69,8.27))
    fig.suptitle(title)

    def format_axes(fig):
        #for ax in fig.axes:
            # ax.text(0.5, 0.5, "ax%d" % (i+1), va="center", ha="center")
            #ax.tick_params(labelbottom=False, labelleft=True)
        ax10.tick_params(labelbottom=False, labelleft=False)
        # ax2.set_rcParams(bottom = 0.2)

    #Definaes a suitable gridspec
    gs = GridSpec(19, 20, figure=fig, hspace=0.0, wspace=1.5)

    # plots the FIT to PF and residuals
    ax1 = fig.add_subplot(gs[0:7, :11])
    ax2 = fig.add_subplot(gs[7:9, :11])
    ax2.sharex(ax1)

    plot_pf(ee_pulsed, dee_pulsed, 
            pulsed_frac, dpulsed_frac, 
            e_turn, pulsed_fit_low, pulsed_fit_high, 
            noFe, 
            forced_gaussian_centroids,
            ylabel='PF', y_lim=[np.min(pulsed_frac-dpulsed_frac)-0.1,np.max(pulsed_frac+dpulsed_frac)+0.1 ],
            title=None, ax1=ax1, ax2=ax2, scale=scale)

    # harmonics

    ax3 = fig.add_subplot(gs[11:15, 0:5])
    ax4 = fig.add_subplot(gs[11:15, 6:11])
    ax5 = fig.add_subplot(gs[15:19, 0:5])
    ax6 = fig.add_subplot(gs[15:19, 6:11])

    cs = plot_harmonics_all(np.array([ee_pulsed,dee_pulsed]), a1 , phi1, a2, phi2, Feline = feline, Ecycl =ecycl , title=title,
                                  stem=None, axis1=ax3,
                                  axis2=ax4, axis3=ax5, axis4=ax6, scale=scale)
    # shares x-axis
    ax3.sharex(ax5)
    ax4.sharex(ax6)
    
    #Defines axes
    ax7 = fig.add_subplot(gs[5:11, 13:19])
    ax7_1 = fig.add_subplot(gs[0:5, 13:19])
    ax7_2 = fig.add_subplot(gs[0:5, -1])    
    ax8 = fig.add_subplot(gs[11:15, 13:19])
    ax9 = fig.add_subplot(gs[15:20, 13:19])
    ax10 = fig.add_subplot(gs[5:11, -1])

    #plots matrix
    plot_matrix_as_lines(ee_pulsed, pp, dpp, axis=ax7_1, kind='E', n_lines=7, phase_on_y=True, log_spacing=True, 
                         axis_legend=ax7_2, annotate=False,double_plot=False, x_axis_on_top=True)

    cm = plot_matrix_as_image(ee_pulsed, pp, normalize=True, sliders=False,
                                    max_level=2, min_level=-2,
                                    n_levels=n_levels, cmap=plt.cm.viridis, energy_on_y=False,
                                    axis=ax7, axis_cb=ax10, plot_big=True, scale=scale)

    color = iter(plt.cm.viridis(np.linspace(0, 1, 4)))

    #plots lag and correlation
    #print(len(ee_pulsed), len(correlation), len(dee_pulsed), len(correlation_error))
    ax8.errorbar(ee_pulsed, correlation, xerr=dee_pulsed, yerr=correlation_error,
                 marker='.', linestyle='', color=next(color), linewidth=1.1, markersize=3.5)
    ax8.set_ylabel('Correlation')
    ax8.set_xscale(scale)

    ax9.errorbar(ee_pulsed, lag, xerr=dee_pulsed, yerr=lag_error,
                 marker='.', linestyle='', color=next(color), linewidth=1.1, markersize=3.5)
    ax9.set_xlabel('E [keV]')
    ax9.set_ylabel('Lag [phase units]')
    ax9.set_xscale(scale)
    for el in (ax8,ax9):
        plot_energies(el,feline,ecycl)

    # Shares the x-axis
    ax7.sharex(ax8)
    ax9.sharex(ax8)

    # Put labels in the panels
    if mark_panels:
        posy=0.95
        for i, ax in enumerate([ax1, ax2, ax3,ax5, ax4, ax6, ax7_1, ax7, ax8,ax9]):
            posx=0.15
            pad=3.0
            if i <= 1:
                posx=0.95
                pad=1.0

            ax.text(posx, posy, '(' + string.ascii_lowercase[i] + ')', horizontalalignment='right',
                            verticalalignment='top', transform=ax.transAxes,
                            bbox=dict(facecolor='none', edgecolor='none', pad=pad))
    
    #Replace ticks
    from matplotlib import ticker        
    for ax in [ax2, ax5, ax6, ax9]:
        ax.set_xticks([ 4, 8, 10, 20, 40])
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f"))
        ax.set_xlim([ee_pulsed[ind_selected][0]-dee_pulsed[ind_selected][0]-0.2,
                     ee_pulsed[ind_selected][-1]+dee_pulsed[ind_selected][-1]+2])
        


    fig.savefig(stem+'_summary_plot.pdf')
    tmp = stem+'_summary_plot.pdf'
    out_str = tmp.split('/')[-1]
    with open(stem+'summary_plot.tex', 'w') as of:
        of.write(latex_figure % (out_str, source, out_str.replace('.pdf','')))
        print(latex_figure % (out_str, source, out_str.replace('.pdf','')))
    
    return fig
