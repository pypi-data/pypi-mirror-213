#!/usr/bin/env python
#

import sys
import os
import glob

import argparse
import astropy.coordinates as coord

import logging
from subprocess import Popen, PIPE, STDOUT
from astroquery.simbad import Simbad
import yaml
import numpy as np
import matplotlib.pyplot as plt


# file_handler = logging.FileHandler(filename='nustar_process_%s.log' % (strftime("%Y-%m-%dT%H:%M:%S", gmtime())))
# stdout_handler = logging.StreamHandler(sys.stdout)
# handlers = [stdout_handler, file_handler]
#
# logging.basicConfig(level=logging.INFO, format=' %(levelname)s - %(message)s', handlers=handlers)
#[%(asctime)s] {%(filename)s:%(lineno)d}
logger = logging.getLogger()

def log_subprocess_output(pipe):
	for line in iter(pipe.readline, b''): # b'\n'-separated lines
		logging.info(line.decode()[0:-1])

def get_latest_file(path, *paths):
	'''
	Returns the name of the latest (most recent) file
	of the joined path(s)
	'''
	fullpath = os.path.join(path, *paths)
	files = glob.glob(fullpath)  # You may use iglob in Python3
	if not files:                # I prefer using the negation
		return None                      # because it behaves like a shortcut
	latest_file = max(files, key=os.path.getctime)
	_, filename = os.path.split(latest_file)
	return filename

def get_channel(e):
	'''
	gets the PI channel from energy scale
	http://heasarc.gsfc.nasa.gov/docs/nustar/nustar_faq.html#pi_to_energy
	'''

	return int((e-1.6)/0.04)

def rate_filter(time, rate, drate, level_down=0, level_up = 1e10, quantile=0.8, make_plot=True, 
                far=1e-4, rate_label='rate', histo_bins=300, title=''):
	'''
rate_filter(self, typical_level=0.5, quantile=0.7,  make_plot=True, far=1e-3,
                    tmin=0,tmax=1e12):
This function prepares cleaned events by apllying a standard filter eliminating bins with FAR < far
This is useful if one want to eliminate a peculiar part of an observation.
The filter is controlled in the following way:
- a Gaussian is fitted on LC data within the innner quantile (default=0.8) of the light curve
- a limit is set on FAR, but it can be overrided by using the level_up and level_down parameters, which are the lowest/highest possible limit.
It returns the limits and a handle to the figure (or None)
	'''
		
	print(rate_filter.__doc__)

	f = None
	cmap = plt.cm.magma
	colors = iter(cmap(np.linspace(0, 1, 4)))
	col1=next(colors)
	col2=next(colors)
	col3=next(colors)
	#col4=next(colors)
	
	if make_plot:
		f, axes = plt.subplots(1, 2, figsize=(6, 6*(5**.5 - 1)/2.), sharey=True, gridspec_kw={'wspace': 0.0, \
									'width_ratios': [3,1]})
		axes[0].errorbar(time/1e3, rate, yerr=drate, linestyle='none', color=col1, ecolor=col1, 
												alpha=0.75)
		axes[0].set_ylabel(rate_label)
		axes[0].set_xlabel('Time [ks]')
		n_hist, edges, patches = axes[1].hist(rate, bins=histo_bins, density=True, facecolor=col1,
												alpha=0.75, orientation='horizontal')
		plt.suptitle(title)
		
	# x=(edges[0:-2]+edges[1:])/2
	from scipy.stats import norm
	ind = (rate <= np.quantile(rate, quantile)) & (rate >= np.quantile(rate, 1.-quantile))
	(mu, sigma) = norm.fit(rate[ind])

	y = norm.pdf(edges, mu, sigma)

	fap = np.min([1. / len(rate), far])
	tmp = norm.isf(fap, loc=mu, scale=sigma)
	limit_up = np.min([level_up, tmp ])
	limit_down = np.max([level_down, 2*mu-tmp])

	if make_plot:
		_ = axes[1].plot(y, edges, 'r--', linewidth=2)
		_ = axes[1].axhline(limit_up, 0, 1, color=col2)
		_ = axes[0].axhline(limit_up, 0, 1, color=col2)
		_ = axes[1].axhline(limit_down, 0, 1, color=col3)
		_ = axes[0].axhline(limit_down, 0, 1, color=col3)
	
	return limit_down, limit_up, f

def create_user_gti(time, in_rate, in_drate, lognormal=True, gti_name='user_gtis.fits', 
                    in_level_down=0, in_level_up = 1e10, quantile=0.8, plot_file_name=None, 
                    far=1e-4, histo_bins=300, time0=0, title=''):
	"""Creates user GTI based on hisogram of rates

	Args:
		time (numpy array): time array
		in_rate (numpy array): input rate
		in_drate (numpy array): input rate uncertainty
		lognormal (bool, optional): if using a lognorml distribution. Defaults to True.
		gti_name (str, optional): GTI file name to be generated. Defaults to 'user_gtis.fits'.
		level_down (int, optional): not lower than this. Defaults to 0. 
		level_up (int, optional): not larger than this. Defaults to 1e10.
		quantile (float, optional): quantile to fit the distribution. Defaults to 0.8.
		plot_file_name (str, optional): if making plots. Defaults to None (no plot).
		far (_type_, optional): the False Alarm Rate to exclude intervals from the fitted distribution. Defaults to 1e-4.
		histo_bins (int, optional): number of bins in the histogram. Defaults to 300.
		time0: a time to add to GTI times to be consistnt with observations

	Returns:
		_type_: _description_
	"""	
	
	from stingray.gti import create_gti_from_condition
	from astropy.io import fits as pf

	if plot_file_name is None:
		make_plot=False
	else:
		make_plot=True

	if lognormal:
		rate = np.log10(in_rate)
		drate = in_drate/in_rate
		rate_label = '$\\log_{10}(\\mathrm{rate})$'
		level_down = np.log10(max(in_level_down, 1e-5))
		level_up = np.log10(max(in_level_up, 1e-5))		
	else:
		rate = in_rate
		drate = in_drate
		rate_label = 'rate'
		level_down = in_level_down
		level_up = in_level_up

	limit_down, limit_up, fig = rate_filter(time, rate, drate, 
                                       level_down=level_down, 
                                       level_up = level_up, 
                                       quantile=quantile, 
                                       make_plot=make_plot, 
                                       far=far, rate_label=rate_label, histo_bins=histo_bins,
									   title=title)
    
	new_gti = create_gti_from_condition(time, (rate > limit_down) & (rate < limit_up) )

	if make_plot:
		ax = fig.axes[0]
		start=new_gti[:,0]
		stop=new_gti[:,1]
		cmap = plt.cm.magma
		colors = cmap(np.linspace(0, 1, 4))
		col4 = colors[2]
		if time[0] < start[0]:
			ax.axvspan(time[0]/1e3, start[0]/1e3, alpha=0.5, color=col4)
			print(time[0]/1e3, start[0]/1e3,)
		for ini, fin in zip(stop[0:-1], start[1:]):
			ax.axvspan(ini/1e3, fin/1e3, alpha=0.5, color=col4)
			print(ini/1e3, fin/1e3)
		if stop[-1] < time[-1]:
			ax.axvspan(stop[-1]/1e3, time[-1]/1e3, alpha=0.5, color=col4)
			print(stop[-1]/1e3, time[-1]/1e3)
		fig.savefig(plot_file_name)

	if len(new_gti.shape)>1:
		start=new_gti[:,0]+time0
		stop=new_gti[:,1]+time0
		c1 = pf.Column(name='START', format='D', unit='s', array=start)
		c2 = pf.Column(name='STOP', format='D', unit='s', array=stop)
		coldefs = pf.ColDefs([c1, c2])
		tbhdu = pf.BinTableHDU.from_columns(coldefs)
		tbhdu.header['EXTNAME']='GTI'
		tbhdu.writeto(gti_name, overwrite=True)
		logger.info('Written %s on disk' % gti_name)
	else:
		logger.warning('No GTI file written, as no GTIs are present')
    
	return new_gti.shape[0]

def prepare_outdir(outdir):

	'''
	:param outdir:
	:return:
	Creates outdir and pfiles directory
	sets pfiles in there
	'''

	if (not os.path.isdir(outdir)):
		os.makedirs(outdir)

	if (not os.path.isdir(os.path.join(outdir, "pfiles"))):
		os.makedirs(os.path.join(outdir, "pfiles"))

	old_pfiles=os.environ["PFILES"]
	tmp=old_pfiles.split(";")
	sys_pfiles=tmp[-1]

	os.environ["PFILES"]=os.path.join(os.getcwd(),os.path.join(outdir, "pfiles"))+";"+sys_pfiles
	logger.info("PFILES = "+os.environ["PFILES"])
	return
	# time_stamp=strftime("%Y-%m-%dT%H:%M:%S", gmtime())
	# return outdir+"/logfile_"+time_stamp+".txt"

def run(command):
	#source $CALDB/software/tools/caldbinit.sh;
	true_command = 'export HEADASNOQUERY="";export HEADASPROMPT=/dev/nul;' + \
		command
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("**** running %s ****\n" % command)
	#out=subprocess.call(cmd, stdout=logger, stderr=logger, shell=True)
	process = Popen(true_command, stdout=PIPE, stderr=STDOUT, shell=True)
	with process.stdout:
		log_subprocess_output(process.stdout)
	ret_value = process.wait()  # 0 means success
	logger.info("------------------------------------------------------------------------------------------------\n")
	logger.info("Command '%s' finished with exit value %d" % (command, ret_value))
	return ret_value

def get_data(obsid):
	cmd="wget -q -nH --no-check-certificate --cut-dirs=6 -r -l0 -c -N -np -R 'index*' -erobots=off --retr-symlinks https://heasarc.gsfc.nasa.gov/FTP/nustar/data/obs/"+obsid[1:3]+"/"+obsid[0]+"/"+obsid+"/"
	return run(cmd)

def extract_counts(img, nominal_y, nominal_x, pix_region):
	
	from photutils import CircularAperture
	from photutils import aperture_photometry

	aperture = CircularAperture((nominal_x, nominal_y), r=pix_region)
	# aperture = CircularAnnulus((nominal_x, nominal_y), r_in=pix_region, r_out=pix_region+1)

	phot_table = aperture_photometry(img, aperture)
	#print(phot_table)
	return phot_table['aperture_sum'].data[0]  # , aperture.area

def prepare_region(unit, default_psf_arcsec=120., criterion='95', critical_surface_brightness=1, use_max_coord = False, n_bins=10, 
						min_psf = 0.1, max_psf = 2, forced_r_pix = 0, back_offset = 2, make_plots=True):
	from astropy.io import fits as pf
	from astropy.wcs import WCS
	import numpy as np

	import matplotlib.pyplot as plt

	from photutils import CircularAperture
	from photutils import CircularAnnulus
	from photutils import aperture_photometry

	from astropy.visualization.mpl_normalize import ImageNormalize
	from astropy.visualization import LogStretch

	from IPython.display import Image
	from IPython.display import display

	default_psf_deg = default_psf_arcsec / 3600.

	filename='ima%s.fits' % unit
	f_header = pf.open(filename)
	hdu = f_header[0]
	my_wcs = WCS(hdu.header)
	image = hdu.data

	ra = hdu.header['RA_OBJ']
	dec = hdu.header['DEC_OBJ']


	xscale = np.abs(hdu.header['CDELT1P'])
	yscale = np.abs(hdu.header['CDELT2P'])

	xscale_wcs = np.abs(hdu.header['CDELT1'])
	yscale_wcs = np.abs(hdu.header['CDELT2'])

	ra_pnt = hdu.header['RA_PNT']
	dec_pnt = hdu.header['DEC_PNT']

	f_header.close()

	ind_max = np.unravel_index(np.argmax(image, axis=None), image.shape)
	max_ima_coord = my_wcs.wcs_pix2world(ind_max[1], ind_max[0], 0)
	logger.info("Image the maximum is at %f %f", max_ima_coord[0], max_ima_coord[1])

	if use_max_coord:
		logger.info("Using maximum of image as center of source image")
		nominal_x = ind_max[1]
		nominal_y = ind_max[0]
	else:
		logger.info("Using the nominal source coordinates of image as center of source image")
		nominal_x, nominal_y = my_wcs.all_world2pix(ra, dec, 0)
		
	centre_x, centre_y = my_wcs.all_world2pix(ra_pnt, dec_pnt, 0)

	scale_matrix = my_wcs.pixel_scale_matrix
	pix_region = default_psf_deg / scale_matrix[1, 1]
	delta_r = pix_region / n_bins

	if make_plots:
		fig1 = plt.figure()
		ax = plt.subplot() #projection=my_wcs)
		minv, maxv = np.percentile(image, [5, 95])
		img_norm = ImageNormalize(image, vmin=minv, vmax=maxv, stretch=LogStretch(10))
		plt.imshow(image, norm=img_norm)  # , vmin=-2.e-5, vmax=2.e-4, origin='lower')
		plt.colorbar()
		ax.grid(color='white', ls='solid')
		ax.set_xlabel('RA')
		ax.set_ylabel('Dec')
		
		# PLOTS THE default SRC REGION WITH 90% CONFINEMENT
		ax.scatter(nominal_x, nominal_y, s=40, marker='x', color='red')

		circle = plt.Circle([nominal_x, nominal_y], pix_region, color='red', fill=False, linestyle='--')
		ax.add_artist(circle)
	
	# Computes the PSF
	r_psf = np.linspace(1, 2 * int(np.floor(pix_region)), 2 * int(np.floor(pix_region)))
	# psf = [(x, extract_counts(image, nominal_y, nominal_x, x)) for x in r_psf]
	# apertures = [CircularAperture((nominal_x, nominal_y), r=x) for x in r_psf]
	apertures = [CircularAnnulus((nominal_x, nominal_y), r_in=x, r_out=x + delta_r) for x in r_psf]
	back_apertures = [CircularAnnulus((nominal_x, nominal_y), r_in=x + delta_r, r_out=x + 2 * delta_r) for x in r_psf]

	phot_table = aperture_photometry(image, apertures)
	back_phot_table = aperture_photometry(image, back_apertures)

	aperture_areas = np.array([aa.area for aa in apertures])
	back_aperture_areas = np.array([aa.area for aa in back_apertures])

	my_keys = [x for x in phot_table.keys() if 'aperture_sum' in x]
	my_back_keys = [x for x in back_phot_table.keys() if 'aperture_sum' in x]

	c_psf = np.array([phot_table[kk][0] for kk in my_keys])
	c_psf /= aperture_areas

	back_c_psf = np.array([phot_table[kk][0] for kk in my_back_keys])
	back_c_psf /= back_aperture_areas

	# psf_back = [(x, extract_counts(image, back_y, back_x, x)) for x in r_psf]
	psf_back = [(x, y) for x,y in zip(r_psf, back_c_psf)]  # *x**2
	# gets and plots the maximum S/N
	# r_psf = [x[0] for x in psf]
	# print(r_psf)
	# c_psf = [x[1] for x in psf]
	r_back = np.array([x[0] for x in psf_back])
	c_back = np.array([x[1] for x in psf_back])

	c_net = np.array(c_psf) - np.array(c_back)
	# scan change of slope
	last_ind = 2
	for i in range(2, len(c_net)):
		last_ind = i
		if c_net[i] >= np.mean(c_net[i - 2:i - 1]):
			logger.info('found change of slope in PSF at index %d' % i)
			break

	real_psf = np.array([extract_counts(image, nominal_y, nominal_x, x) for x in r_psf])
	real_psf_net = real_psf - c_back * r_back ** 2

	norm_cum_sum = real_psf_net / real_psf_net.max()

	gradient = np.gradient(real_psf_net)
	# back_gradient = np.gradient(c_back)
	gradient /= gradient.max()

	# gradient2 = np.gradient(gradient)
	# gradient2 /= np.max(np.abs(gradient))
	# s_n = c_net * aperture_areas / np.sqrt(c_psf * aperture_areas)
	s_n = real_psf_net / np.sqrt(real_psf)

	if make_plots:
		fig2, ax_2 = plt.subplots(1, 2, sharex=True)
		ax_2[0].plot(r_psf, c_psf, color='blue', label="anulus brillance")
		ax_2[0].plot(r_back, c_back, color='red', label="background brillance")
		ax_2[0].plot(r_back, c_net, color='green', label="anulus net brillance")

		# ax_2[0].plot(r_psf, real_psf, color='blue', label="Cum PSF")
		# ax_2[0].plot(r_back, c_back*r_back**2, color='red', label="background")
		# ax_2[0].plot(r_back, real_psf_net, color='green', label="Net PSF")

		#ax_2[0].set_title(self.target + ' ' + self.obs_id)
		ax_2[0].legend()

		ax_2[1].plot(r_psf, norm_cum_sum, color='black', label="Cum PSF")

		ax_2[1].plot(r_psf, gradient, color='blue', label='PSF')
		# ax_2[1].plot(r_psf, back_gradient, color='red', label='back gradient')
		# ax_2[1].plot(r_psf, gradient2, color='green', label='gradient2')

		ax_2[1].plot(r_psf, s_n / s_n.max(), color='cyan', label='S/N')

		ax_2[1].grid(True)
		ax_2[1].legend()

	ind_95 = int(np.argmin(np.abs(c_net[0:last_ind] - critical_surface_brightness)) + delta_r / 2)
	if ind_95 >= len(r_psf):
		ind_95 = len(r_psf) - 1

	if criterion == '95':
		ind_95 = np.argmin(np.abs(norm_cum_sum - 0.95))

	if make_plots:
		ax_2[1].scatter(r_psf[ind_95], norm_cum_sum[ind_95], marker='x', color='red')

	r_max = r_psf[ind_95]
	c_max = c_net[ind_95]

	logger.info("Optimal inclusion is r=%.1f +/- %.1f with %.1f cts/pix " % (r_max, delta_r / 2, c_max))
	logger.info("Cumulative PSF is %.2f" % norm_cum_sum[ind_95])

	if r_max < min_psf*pix_region:
		logger.info('r_max is lower than %.1f' % min_psf)
		r_max = min_psf

	if r_max > max_psf * pix_region:
		logger.info('r_max is larger than %.1f' % max_psf)
		r_max = max_psf

	if forced_r_pix > 0:
		r_max = forced_r_pix
		logger.info("Input forced radius for extraction region at %.1f" % r_max)

	if make_plots:
		# plt.scatter(r_max,c_max,s=60,marker='x', color='red')

		ax_2[0].axvline(r_max, 0, 1, color='black', linestyle='--', linewidth=2)
		ax_2[1].axvline(r_max, 0, 1, color='black', linestyle='--', linewidth=2)

	distance = np.sqrt( (centre_x - nominal_x)**2 + (centre_y - nominal_y)**2 )
	back_offset *= r_max / distance 
	back_x = centre_x + back_offset * (centre_x - nominal_x)
	back_y = centre_y + back_offset * (centre_y - nominal_y)
	logger.info('Source image coordinates are %f %f', nominal_x, nominal_y)
	logger.info('Aim point image coordinates are %f %f', centre_x, centre_y)
	logger.info('Background reg. image coordinates are %f %f', back_x, back_y)
	logger.info('Image shape is %d %s', image.shape[0], image.shape[1])
	
	x_bary=0.0
	y_bary=0.0
	min_y=10000
	x_min_y = 0
	min_x=10000
	y_min_x = 0
	max_x=0
	y_max_x = 0
	max_y=0
	x_max_y = 0

	count = 0
	
	for x in range(image.shape[0]):
		for y in range(image.shape[1]):
			if image[y,x]>0:
				count += 1
				x_bary+=1.0*x
				y_bary+=1.0*y
				if x < min_x:
					min_x = x
					y_min_x = y
				if y < min_y:
					min_y = y
					x_min_y = x
				if x > max_x:
					max_x = x
					y_max_x = y
				if y > max_y:
					max_y = y
					x_max_y = x


	x_bary/=count
	y_bary/=count

	logger.info('Image barycenter is %f %f', x_bary, y_bary)
	logger.info('min_x %d , min_y %d , max_x %d . max_y %d' , min_x, min_y, max_x, max_y)
	logger.info('y_min_x %d , x_min_y %d , y_max_x %d . x_max_y %d' , y_min_x, x_min_y, y_max_x, x_max_y)

	vertexes = [ (min_x, y_min_x), (x_max_y, max_y) , (max_x, y_max_x) , (x_min_y, min_y) ] 

	vertex_distances = []

	for i, (x,y) in enumerate(vertexes):
		vertex_distances.append(np.sqrt( (x - nominal_x)**2 + (y - nominal_y)**2 ))
		logger.info('Vertex %d %d %d %f', i, x, y, vertex_distances[-1])
		if make_plots:
			ax.scatter(x,y, s=40, marker='+', color='cyan')
			ax.text(x,y, '%d %.1f %.1f' %(i,x,y), color='white')

	src_vertex = np.argmin(vertex_distances)
	logger.info('src_vertex %d', src_vertex)

	back_vertex = src_vertex+2

	if back_vertex >= 4:
		back_vertex -= 4

	logger.info('back_vertex %d', back_vertex)

	# m = ( ) / ( )
	# logger.info('m %f' , m )
	alpha = np.arctan2( vertexes[src_vertex][1] - vertexes[back_vertex][1],  vertexes[src_vertex][0] - vertexes[back_vertex][0])
	logger.info('alpha %f' % (alpha *180 / np.pi))

	back_x = vertexes[back_vertex][0] + np.cos(alpha) * pix_region * (np.sqrt(2)+0.1)
	back_y = vertexes[back_vertex][1] + np.sin(alpha) * pix_region * (np.sqrt(2)+0.1)

	logger.info("back_x back_y = %f %f", back_x, back_y)

	if make_plots:
		ax.scatter(centre_x, centre_y, s=40, marker='+', color='black')
		ax.scatter(x_bary, y_bary, s=40, marker='*', color='blue')
		
		circle = plt.Circle([back_x, back_y], pix_region, color='white', fill=False)
		ax.add_artist(circle)
		circle = plt.Circle([nominal_x, nominal_y], r_max, color='red', fill=False)
		ax.add_artist(circle)
		fig1.savefig('RegionImage.png')
		fig2.savefig('EnclosureGraph.png')
	
	r_max_arcsec = r_max * scale_matrix[1, 1] * 3600.
	ra_back, dec_back = my_wcs.all_pix2world(back_x,back_y, 0)

	return ra, dec, r_max_arcsec, ra_back, dec_back

def write_region(fname, ra, dec, src_flag, ra_back=-1, dec_back=-1, radius=120):
	ff = open(fname, 'w')
	ff.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\nfk5\n")
	if src_flag:
		ff.write("circle(%.4f,%.4f,%.0f\")" % (ra, dec, radius))
	else:
		#The default is just a guess
		if ra_back == -1:
			ra_deg = float(ra)-0.14
		else:
			ra_deg = float(ra_back)
		if dec_back == -1:
			dec_deg = float(dec)-0.08
		else:
			dec_deg = float(dec_back)

		ff.write("circle(%.4f,%.4f,%.4f\")" % (ra_deg, dec_deg, float(radius)))
	ff.close()


def get_src_from_obsid(obsid, repository_path=os.environ['HOME'] + '/NUSTAR/Repository'):
	'''
	Gets the source and the coordinates from the data repository
	:param obsid:
	:param repository_path:
	:return:
	'''
	from astropy.io import fits as pf
	search_str = repository_path + '/' + obsid + '/event_cl/nu*A*_cl.evt.gz'
	logger.debug(search_str)
	eventsA = glob(search_str)
	if len(eventsA) == 0:
		logger.warning('no event data for ' + obsid + '? Reurning none')
		return None
	with pf.open(eventsA[0]) as ff:
		src = ff[1].header['OBJECT']
		ra = ff[1].header['RA_OBJ']
		dec = ff[1].header['DEC_OBJ']
	logger.debug('Found source ' + src)
	return src, ra, dec

def prepare_folder_from_obsid(oo, output_base_folder='.'):
	'''
	Prepare a folder to process data
	:param oo: the obsid
	:return: None
	'''

	src, ra, dec = get_src_from_obsid(oo)
	result_table = Simbad.query_region(coord.SkyCoord(ra,dec, unit='deg', frame='icrs'), radius='1m')
	all_names = Simbad.query_objectids(result_table['MAIN_ID'][0])

	try:
		os.mkdir(output_base_folder+'/'+src)
	except OSError as error:
		print(error)

	workdir = output_base_folder+'/'+src+'/'+oo

	try:
		os.mkdir(workdir)
	except OSError as error:
		print(error)

	src_dict = {
		'OBJECT': src,
		'RA': ra,
		'DEC': dec,
		'NAMES': [str(ss) for ss in all_names['ID']],
		'OBSID': oo
	}

	with open(workdir + '/observation.yml', 'w') as outfile:
		yaml.dump(src_dict, outfile, default_flow_style=False)

	print("Processed " + src + ' with obsid ' + oo)



def wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag=False, region_flag=False,
				 spec_flag=False, lc_flag=False,
				 no_ds9_flag=False, ra_back=-1, dec_back=-1, radius=120, write_baryevtfile_flag=False,
				 filter_evt_flag=False, user_gti_file='none',
				 repository_location=os.environ['HOME'] + '/NUSTAR/Repository', t_bin=100., e_min=3., e_max=30.,
				 J_A=None, J_B=None):
	'''

	:param obsid: the observation ID
	:param ra_src: RA of the source
	:param dec_src: Dec of the source
	:param outdir_base: the basename for products
	:param pipeline_flag: it tuns the pipeline
	:param region_flag: it writes region (if not existent) and allows the user to check them
	:param spec_flag: it extracts spectra
	:param lc_flag: extracts light crves (set also t_bin e_min and e_max
	:param no_ds9_flag: this is relevant just if region_flag is true, if set to True, it will use JS9, with the diplays
						for FPMA and FPMB provided by the caller
	:param ra_back: optional RA of the center of background region (otherise offset from the source)
	:param dec_back: optional Dec of the center of background region (otherise offset from the source)
	:param radius: the radius for source regions )defaults to 120
	:param write_baryevtfile_flag: to be used with lightcurve to extract barycentric corrected event files
	:param filter_evt_flag: This is to be used when lightcurves are extracted to extract barycentric corrected
							event files for the source and backgroud for FPMA and FPMB
	:param user_gti_file: if this is provided
	:param repository_location: the location of the repository of raw data
	:param t_bin: time bin for light curves
	:param e_min: Minimum energy for lightcurve
	:param e_max: Maximium energy for lightcurve
	:param J_A:  handler for the JS9 display for FPMA
	:param J_B:  handler for the JS9 display for FPMA
	:return: zero
	'''
	if (not os.path.isdir(repository_location + "/" + obsid)):
		logger.error("The obsid you specified (" + obsid + ") does not exist in the repository " + repository_location)
		return 1

	logger.info("Processing OBSID %s for RA=%f Dec=%f with outdir base %s" % (obsid, ra_src, dec_src, outdir_base))
	logger.info("Pipeline flag %r" % (pipeline_flag))
	logger.info("Spectrum flag %r" % (spec_flag))
	logger.info("Lightcurve flag %r" % (lc_flag))

	outdir_pipeline = outdir_base + "_pipeline"
	logger.info("The output of standard pipelines are in " + outdir_pipeline)

	if pipeline_flag:

		# logfile_name =
		prepare_outdir(outdir_pipeline)
		# logfile = open(logfile_name, 'w')
		#print("writing output to log file: %s" % logfile_name)

		cmd = "nupipeline indir=" + repository_location + "/" + obsid + " steminputs=nu" + obsid + " obsmode=Science outdir=" + outdir_pipeline

		return run(cmd)
		# logfile.close()

	if region_flag:
		
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before spectral extraction. Folder %s does not exist in %s" % (
				outdir_pipeline, os.getcwd()))
			return 1
		outdir = outdir_base + "_spec"
		outdir_pipeline = outdir_base + "_pipeline"
		prepare_outdir(outdir)

		logger.info('Extracting images')
		xsel_cmd = '''dummy
		read eve
		./ 
		nu%s%s01_cl.evt 
		yes
		filter pha_cut %d %d
		extra ima
		save ima ima%s.fits




		quit





		'''

		chan_min = get_channel(e_min)
		chan_max = get_channel(e_max)
		
		os.chdir(outdir_pipeline)
		for unit in ['A', 'B']:
			if not os.path.isfile('ima%s.fits' % unit):
				with open('xsel_%s.txt' % unit, 'w') as ff:
					ff.write(xsel_cmd % (obsid, unit, chan_min, chan_max, unit))
				cmd = 'xselect < ' + 'xsel_%s.txt' % (unit)
				run(cmd)
		
		raA, decA, r_max_arcsecA, ra_backA, dec_backA = prepare_region('A')
		raB, decB, r_max_arcsecB, ra_backB, dec_backB = prepare_region('B')
		os.chdir('..')

		logger.info("We store regions in the spectral extraction folder '%s'" % outdir)

		src_regionA = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_regionA)):
			write_region(src_regionA, ra_src, dec_src, True, radius=r_max_arcsecA)
		src_regionB = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_regionB)):
			write_region(src_regionB, ra_src, dec_src, True, radius=r_max_arcsecB)
		bkg_regionA = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_regionA)):
			write_region(bkg_regionA, ra_src, dec_src, False, ra_back=ra_backA, dec_back=dec_backA, radius=r_max_arcsecA)
		bkg_regionB = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_regionB)):
			write_region(bkg_regionB, ra_src, dec_src, False, ra_back=ra_backB, dec_back=dec_backB, radius=r_max_arcsecB)


		if no_ds9_flag==False:
			logger.info("Please check the regions for FPMA")
			cmd = "ds9 -scale log " + outdir_pipeline + "/imaA.fits -regions " + src_regionA + " -regions " + bkg_regionA
			run(cmd)
			logger.info("Please check the regions for FPMB")
			cmd = "ds9 -scale log " + outdir_pipeline + "/imaB.fits -regions " + src_regionB + " -regions " + bkg_regionB
			run(cmd)

			#logger.info("Have you checked properly the region files?(y/Y will continue the processing any other key stop it)")
			logger.warning("We ask to rerun the analysis disabling the ds9 iteractive command with which you have checked the region files")
			# ans = input("Please enter the key: ...")
			# if (not (ans == 'y')) and (not (ans == 'Y')):
			# 	print("Exit processing")
			return 0
		else:
			# JS9 does not load event files, I need to create an image first

			logger.warning("Please check the regions for FPMA")

			if J_A is None or J_B is None:
				logger.warning('We need a JS9 display for FPMA and FPMB to check regions and events, leave ds9_flag=False to use ds9')	
				#raise RuntimeError('We need a JS9 display for FPMA and FPMB to check regions and events, leave ds9_flag=False to use ds9')
				return 0
			J_A.Load(outdir_pipeline + "/imaA.fits")
			J_A.LoadRegions(src_regionA)
			J_A.LoadRegions(bkg_regionA)
			J_A.send({'cmd': 'SetScale', 'args': ['log']})
			J_A.SetColormap('red')

			logger.warning("Please check the regions for FPMB")

			J_B.Load(outdir_pipeline + "/imaB.fits")
			J_B.LoadRegions(src_regionB)
			J_B.LoadRegions(bkg_regionB)
			J_B.send({'cmd': 'SetScale', 'args': ['log']})
			J_B.SetColormap('red')
			return 0

	if lc_flag:

		import shutil
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before light curve extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_lc"
		# logfile_name = \
		prepare_outdir(outdir)
		# logfile = open(logfile_name, 'w')
		# logger.info("writing output to log file: %s" % logfile_name)

		##searh clock file
		latest_clock = get_latest_file(repository_location + "/clock/*")

		ch_min = get_channel(e_min)
		ch_max = get_channel(e_max)
		logger.info("Energy scale E = Channel Number * 0.04 keV + 1.6 keV\n")
		logger.info("E_min=%f E_max=%f t_bin=%f ch_min=%d ch_max=%d\n" % (e_min, e_max, t_bin, ch_min, ch_max))


		if ((not os.path.isfile(outdir_base + "_spec/sourceA.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/sourceB.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/backgroundA.reg")) or \
				(not os.path.isfile(outdir_base + "_spec/backgroundB.reg")) ):
			raise RuntimeError('You need to have region files in %s_spec make them with the option region_flag' % outdir_base)

		src_region = outdir + "/sourceA.reg"
		if (not os.path.isfile(src_region)):
			spec_src = outdir_base + "_spec/sourceA.reg"
			shutil.copy(spec_src, src_region)

		bkg_region = outdir + "/backgroundA.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundA.reg"
			shutil.copy(spec_bkg, bkg_region)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		# print("My latest clock is " + latest_clock)
		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		src_region = outdir + "/sourceB.reg"
		if (not os.path.isfile(src_region)):
			spec_src = outdir_base + "_spec/sourceB.reg"
			shutil.copy(spec_src, src_region)

		bkg_region = outdir + "/backgroundB.reg"
		if (not os.path.isfile(bkg_region)):
			spec_bkg = outdir_base + "_spec/backgroundB.reg"
			shutil.copy(spec_bkg, bkg_region)

		cmd = "nuproducts indir=" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB_%.1f_%.1f outdir=" % (
		e_min, e_max) + outdir
		cmd += " srcregionfile=" + src_region + " bkgextract=yes runbackscale=no binsize=%f pilow=%d pihigh=%d barycorr=yes" % (
		t_bin, ch_min, ch_max)
		cmd += " orbitfile=" + repository_location + "/" + obsid + "/auxil/nu" + obsid + "_orb.fits.gz cleanup=no srcra_barycorr=%f" % (
			ra_src)
		cmd += " srcdec_barycorr=%f" % (
			dec_src) + " bkglcfile=DEFAULT bkgregionfile=" + bkg_region + " runmkarf=no runmkrmf=no phafile=NONE imagefile=NONE"
		if write_baryevtfile_flag:
			cmd += " write_baryevtfile=yes"

		if latest_clock != None:
			cmd += " clockfile=\"" + repository_location + "/clock/" + latest_clock + "\""

		if user_gti_file != 'none':
			cmd += " usrgtifile=" + user_gti_file + " usrgtibarycorr=yes"

		run(cmd)

		if filter_evt_flag:
			xsel_cmd = '''dummy
	read eve
	./ 
	FPM%s_%.1f_%.1f_cl_barycorr.evt 
	yes 
	filter reg %s%s.reg 
	extra eve
	save eve %s%s.evt




	quit





	'''
			os.chdir(outdir_base + '_lc')
			for unit in ['A', 'B']:
				for reg in ['source', 'background']:
					with open('xsel_%s_%s.txt' % (reg, unit), 'w') as ff:
						ff.write(xsel_cmd % (unit, e_min, e_max, reg, unit, reg, unit))
					cmd = 'xselect < ' + 'xsel_%s_%s.txt' % (reg, unit)
					run(cmd)
			os.chdir('..')
		# logfile.close()

	if spec_flag:
		if not os.path.isdir(outdir_pipeline):
			logger.error("You need to have processed the pipeline before spectral extraction. Folder %s does not exist" % (
				outdir_pipeline))
			return 1
		outdir = outdir_base + "_spec"
		#logfile_name = \
		prepare_outdir(outdir)

		src_regionA = outdir + "/sourceA.reg"
		src_regionB = outdir + "/sourceB.reg"
		bkg_regionA = outdir + "/backgroundA.reg"
		bkg_regionB = outdir + "/backgroundB.reg"

		if ((not os.path.isfile(src_regionA)) or \
				(not os.path.isfile(src_regionB)) or \
				(not os.path.isfile(bkg_regionA)) or \
				(not os.path.isfile(bkg_regionB))):
			raise RuntimeError('You need to have region files in %s make them with the option region_flag' % outdir)

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMA steminputs=nu" + obsid + " stemout=FPMA outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionA + " bkgregionfile=../" + bkg_regionA + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."
		run(cmd)

		cmd = "cd " + outdir + ";nuproducts indir=../" + outdir_pipeline + " instrument=FPMB steminputs=nu" + obsid + " stemout=FPMB outdir=."  # +outdir
		cmd += " srcregionfile=../" + src_regionB + " bkgregionfile=../" + bkg_regionB + " bkgextract=yes runbackscale=yes cleanup=yes "
		cmd += " lcfile=NONE bkglcfile=NONE runmkarf=yes runmkrmf=yes imagefile=NONE clobber=yes"

		if user_gti_file != 'none':
			cmd += " usrgtifile=../" + user_gti_file + " usrgtibarycorr=no"

		cmd += ";cd .."

		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMA_sr.pha -b " + outdir + "/FPMA_bk.pha -r " + outdir + "/FPMA_sr.rmf -a " + outdir + "/FPMA_sr.arf -e 3 -E 78"
		run(cmd)

		cmd = "optimal_binning.py " + outdir + "/FPMB_sr.pha -b " + outdir + "/FPMB_bk.pha -r " + outdir + "/FPMB_sr.rmf -a " + outdir + "/FPMB_sr.arf -e 3 -E 78"
		run(cmd)

		#logfile.close()
	return 0

import papermill as pm 
import json
import shutil
import re
from datetime import datetime

def get_parameter_dict(nb_fname):
    master_nb_parameters = {}
    if os.path.isfile(nb_fname):
        for kk, ii in pm.inspect_notebook(nb_fname).items():
            #print(ii['default'])
            value = ii['default']
            inferred_type = ii['inferred_type_name']
            if inferred_type == 'str':
                real_value = value.replace('\'','')
            elif inferred_type == 'bool':
                if value == 'False':
                    real_value = False
                else:
                    real_value = True
                #real_value = gettype(inferred_type)(value)
            else:
                real_value = json.loads(value)
            #print(value, real_value)
            master_nb_parameters.update({kk:real_value})
    return master_nb_parameters

def get_last_file(pattern="*/*.ipynb"):
    # get list of files that matches pattern

    files = list(filter(os.path.isfile, glob.glob(pattern)))
    files = list(filter(lambda x :('output' not in x), files))
    # sort by modified time
    files.sort(key=lambda x: os.path.getmtime(x))
    if len(files)== 0:
        return ''
    # get last item in list
    lastfile = files[-1]

    print("Most recent file matching {}: {}".format(pattern,lastfile))
    return lastfile

def process_notebook():
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process a notebook\n'

	parser = argparse.ArgumentParser(description='Process Nustar Data',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('OBSID', metavar='obsid', type=str, nargs=1, help='OBSID with full path, e.g. Cen_X3/30101055002')
	parser.add_argument("basenb", metavar='basenb', nargs=1, help="base notebook (absolute oath or relative to obsid)", type=str)

	parser.add_argument("--force_matrix", help="Force computation of EN-Phase and T-Phase matrixes",
						action='store_true')
	parser.add_argument("--in_nb", help="Notebook to derive input parameters (to be found in OBSID)", type=str, default='none')
	parser.add_argument("--in_yaml", help="yaml file with parameters (to be found in OBSID, or relative path)", type=str, default='none')
	parser.add_argument("--select_nb", help="Select the last nb with pattern ep_??_*", action='store_true')
	parser.add_argument("--min_sn_matrix", help="Minimum S/N to rebin matrixes", type=float, default=-1)
	parser.add_argument("--use_nb2workflow", help="If running the notebook as ", action='store_true')
	parser.add_argument("--set_cwd", help="Set the folder when the nb should be run", type=str, default=os.getcwd())

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()

	obsid = args.OBSID[0]
	if (not os.path.isdir(obsid)):
		logger.error("The obsid location you specified does not exist "+obsid)
		return 1

	os.chdir(obsid)

	if not os.path.isdir('obs_spec'):
		print(obsid + ' has not been processed, return quitly')
		return 0

	logger.info('We are in ' + os.getcwd())
	base_nb = args.basenb[0]
	if (not os.path.isfile(base_nb)):
		logger.error("The base notebook you specified does not exist "+base_nb)
		return 1

	p  = re.compile('ep[_-][a-z]{2}[_-]*')
	p1 = re.compile('Elaboration[_-][0-9]{11}.ipynb')

	local_nb_parameters = {}

	if args.select_nb:
		my_nb = get_last_file('*.ipynb')
		if p.match(my_nb):
			logger.info(f'Using {my_nb}')
			local_nb_parameters.update(get_parameter_dict(my_nb))
		else:
			if p1.match(my_nb):
				logger.info(f'Using {my_nb}')
				local_nb_parameters.update(get_parameter_dict(my_nb))
			else:
				print(f'not using {my_nb}')

	if args.in_nb != 'none':
		if not os.path.isfile(args.in_nb):
			print(f"{args.in_nb} does not exist, not using parameters")
		else:
			local_nb_parameters.update(get_parameter_dict(args.in_nb))
	
	if args.in_yaml != 'none':
		if not os.path.isfile(args.in_yaml):
			print(f"{args.in_yaml} does not exist, not using parameters")
		else:
			with open(args.in_yaml) as ff:
				local_nb_parameters.update(get_parameter_dict(yaml.safe_load(ff)))

	if args.force_matrix:
		local_nb_parameters.update({'recompute_matrixes' : True})
	
	if args.min_sn_matrix != -1:
		local_nb_parameters.update({'min_sn_matrix' : args.min_sn_matrix})

	cwd = args.set_cwd
	logger.info('We will run the notebook in "%s"' % cwd)

	now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
	basename = os.path.basename(base_nb).replace('.ipynb','')
	output_mosaics_notebook_path = basename+f'_output_{now}.ipynb'
	print(f'Processing {obsid}')
	print(local_nb_parameters)

	if args.use_nb2workflow:
		from nb2workflow import nbadapter
		shutil.copy(base_nb, output_mosaics_notebook_path)
		nb_mosaics_execution = nbadapter.nbrun(
				output_mosaics_notebook_path,
				local_nb_parameters,
				inplace=True
			)
	else:
		shutil.copy(base_nb, 'notebook_to_run.ipynb')
		print(base_nb + ' into ' + output_mosaics_notebook_path)
		nb_mosaics_execution = pm.execute_notebook(
				'notebook_to_run.ipynb',
				output_mosaics_notebook_path,
				parameters=local_nb_parameters,
				log_output=True,
				cwd=cwd
			)	
		os.remove('notebook_to_run.ipynb')

	return nb_mosaics_execution
	

def process():
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process Nustar repository and extracts only LC and image or also spectrum with background\n'

	parser = argparse.ArgumentParser(description='Process Nustar Data',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('OBSID', metavar='obsid', type=str, nargs=1, help='OBSID in the Repository folder')
	parser.add_argument("RA", metavar='ra', nargs=1, help="RA of the source", type=float)
	parser.add_argument("Dec", metavar='dec', nargs=1, help="Dec of the source", type=float)
	parser.add_argument('outdir', metavar='outdir', type=str, nargs=1,
						help='output folder base name (to be appended with _pipeline, _lc, or _spec')
	parser.add_argument("--regions", help="Writes (if not present) and checks regions with ds9 (no js9)",
						action='store_true')
	parser.add_argument("--pipeline", help="Run pipeline", action='store_true')
	parser.add_argument("--spec", help="Run spectral extraction", action='store_true')
	parser.add_argument("--lightcurve", help="Run light curve extraction", action='store_true')
	parser.add_argument("--filter_evt", help="Extract events for region files", action='store_true')

	parser.add_argument("--no-ds9", help="Avoid ds9 display", action='store_true')

	parser.add_argument("--usergti", help="User defined GTIs", type=str, default='none')

	parser.add_argument("--timebin", help="timebin for LC (s)", type=float, default=100)

	parser.add_argument("--eMin", help="minimum energy (keV) for LC", type=float, default=3)
	parser.add_argument("--eMax", help="maximum energy (keV) for LC", type=float, default=30)

	parser.add_argument("--ra_back", help="RA center of background region", type=float, default=-1)
	parser.add_argument("--dec_back", help="Dec center of background region", type=float, default=-1)
	parser.add_argument("--radius", help="radius of regions", type=float, default=120)

	parser.add_argument("--write_baryevtfile", help="write barycentric corrected event files (in lightcurve)",
						action='store_true')

	parser.add_argument("--repository", help='Location of the repository', type=str,
						default=os.environ['HOME']+'/NuSTAR/Repository')

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()

	repository_location = args.repository
	if (not os.path.isdir(repository_location)):
		logger.error("The repository location you specified does not exist "+repository_location)
		sys.exit(1)

	PID = os.getpid()
	logger.info("------------------------------------------------------------------------------------------------")
	logger.info(" PID of the process %d" % PID)
	logger.info(" kill -9 -%d  to kill current proc and children" % PID)
	logger.info("------------------------------------------------------------------------------------------------")

	obsid = args.OBSID[0]
	outdir_base = args.outdir[0]
	ra_src = args.RA[0]
	dec_src = args.Dec[0]
	pipeline_flag = args.pipeline
	region_flag = args.regions
	lc_flag = args.lightcurve
	spec_flag = args.spec
	ds9_flag = args.no_ds9
	ra_back = args.ra_back
	dec_back = args.dec_back
	radius = args.radius
	write_baryevtfile_flag = args.write_baryevtfile
	filter_evt_flag = args.filter_evt
	t_bin = args.timebin
	e_min = args.eMin
	e_max = args.eMax
	user_gti_file = args.usergti

	out = wrap_process(obsid, ra_src, dec_src, outdir_base, pipeline_flag, region_flag, spec_flag, lc_flag,
				 ds9_flag, ra_back, dec_back, radius, write_baryevtfile_flag, filter_evt_flag,
				 user_gti_file, repository_location, t_bin, e_min, e_max)

	if out != 0:
		sys.exit(out)

def script_data():
	help = "get_data.py OBSID\n"

	if len(sys.argv) < 2:
		print(help)
		sys.exit(1)

	obsid = sys.argv[1]

	from nustarpipeline import process

	process.get_data(obsid)

def standard_processing_after_regions():
	# Not a completely general tool, specific for a project
	# Usable calling this file
	help = sys.argv[0] + '\n'
	help += '\n'
	help += 'Process Nustar repository and extracts standard products for the HMXB project\n'

	parser = argparse.ArgumentParser(description='Standard Process Nustar Data for the HMXB project',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('mypath', metavar='mypath', type=str, nargs=1,
						help='Path whenre you process data , e.g. Her_X1/10202002002 ')

	parser.add_argument('--outdir', type=str, default='obs',
						help='output folder base name (to be appended with _pipeline, _lc, or _spec')

	parser.add_argument("--timebin", help="timebin for LC (s)", type=float, default=0.1)

	parser.add_argument("--eMin", help="minimum energy (keV) for LC", type=float, default=3)
	parser.add_argument("--eMed", help="medium energy (keV) for LC", type=float, default=7)
	parser.add_argument("--eMax", help="maximum energy (keV) for LC", type=float, default=30)
	parser.add_argument("--repository", help='Location of the repository', type=str,
						default=os.environ['HOME']+'/NUSTAR/Repository')
	parser.add_argument("--clean", help="Cleans products before extracting", action='store_true')

	if len(sys.argv) == 1:
		parser.print_help()
		print(help)
		sys.exit(1)

	args = parser.parse_args()
	my_path = args.mypath[0]
	outdir_base = args.outdir

	t_bin = args.timebin
	e_min = args.eMin
	e_med = args.eMed
	e_max = args.eMax
	repository = args.repository
	clean = args.clean

	print("Path is %s" % my_path)

	try:
		os.chdir(my_path)
	except:
		raise FileExistsError("The folder %s does not exist" % my_path)

	import yaml

	try:
		with open('observation.yml', 'r') as outfile:
			src_dict = yaml.load(outfile, Loader=yaml.FullLoader)
	except:
		raise FileExistsError("The file observation.yams does not exist in  %s" % my_path)

	print(src_dict)

	from nustarpipeline import process, utils

	obsid = src_dict['OBSID']
	ra_src = src_dict['RA']
	dec_src = src_dict['DEC']

	if ((not os.path.isfile(outdir_base + "_spec/sourceA.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/sourceB.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/backgroundA.reg")) or \
			(not os.path.isfile(outdir_base + "_spec/backgroundB.reg"))):
		raise FileExistsError(
			'You need to have region files in %s_spec make them with the option region_flag' % outdir_base)

	if clean:
		extensions_spec = ['pha', 'pi', 'arf', 'rmf', 'gif']
		cmd = 'rm -f'
		for ee in extensions_spec:
			cmd += ' %s_spec/*.%s' % (outdir_base, ee)
		process.run(cmd)

		extensions_lc = ['pha', 'evt', 'lc', 'pco', 'xco', 'reg', 'txt']
		cmd = 'rm -f'
		for ee in extensions_lc:
			cmd += ' %s_lc/*.%s' % (outdir_base, ee)
		process.run(cmd)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base,  spec_flag=True, repository_location=repository)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base, lc_flag=True, t_bin=t_bin, e_min=e_min, e_max=e_med,
						 repository_location=repository)

	process.wrap_process(obsid, ra_src, dec_src, outdir_base, lc_flag=True, t_bin=t_bin, e_min=e_med,
						 e_max=e_max, write_baryevtfile_flag=True, filter_evt_flag=True,
						 repository_location=repository)

	os.chdir(outdir_base+'_spec/')
	utils.make_basic_fit()
	os.chdir('..')

if __name__ == "__main__":
	standard_processing_after_regions()

