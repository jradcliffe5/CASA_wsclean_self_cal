import os,re,sys
import numpy as np

try:
    index = int(sys.argv[sys.argv.index('run_wsclean.py')+1])
except IndexError:
    print 'Failed...run_wsclean.py'

def headless(inputfile):
    ''' Parse the list of inputs given in the specified file. (Modified from evn_funcs.py)'''
    INPUTFILE = open(inputfile, "r")
    control = {}
    # a few useful regular expressions
    newline = re.compile(r'\n')
    space = re.compile(r'\s')
    char = re.compile(r'\w')
    comment = re.compile(r'#.*')
    # parse the input file assuming '=' is used to separate names from values
    for line in INPUTFILE:
        if char.match(line):
            line = comment.sub(r'', line)
            line = line.replace("'", '')
            (param, value) = line.split('=')
            param = newline.sub(r'', param)
            param = param.strip()
            param = space.sub(r'', param)
            value = newline.sub(r'', value)
            value = value.replace(' ','').strip()
            valuelist = value.split(',')
            if len(valuelist) == 1:
                if valuelist[0] == '0' or valuelist[0]=='1' or valuelist[0]=='2':
                    control[param] = int(valuelist[0])
                else:
                    control[param] = str(valuelist[0])
            else:
                control[param] = ','.join(valuelist)
    return control

inputs = headless('inputs.txt')
wsclean_loc = str(inputs['wsclean_loc'])
ncore = int(inputs['ncore'])
cell = float(inputs['cell']) ## in arcsec
imsize = float(inputs['imsize']) ## in arcmins
mem = float(inputs['mem']) ##percentage memory
niter = int(inputs['niter'])
gain = float(inputs['gain'])
mgain = float(inputs['mgain'])
auto_threshold = float(inputs['auto_threshold'])
do_MFS = str(inputs['do_MFS'])
channels_out = int(inputs['channels_out'])
deconvolution_channels = int(inputs['deconvolution_channels'])
nterms = int(inputs['nterms'])
weight = str(inputs['weight'])
do_multiscale = str(inputs['do_multiscale'])
multi_scale_scales = str(inputs['multi_scale_scales'])
################

if len(multi_scale_scales) == 0:
    multi_scale_scales = ''
else:
    multi_scale_scales = '-multiscale-scales %s' % multi_scale_scales

#df = pd.read_csv('combination_information.csv')
size_scale = int(imsize*60.*(1./cell))

ms1 = str(inputs['ms'])


if do_MFS == 'True':
    if do_multiscale == 'True':
        os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -joinchannels -stopnegative -channelsout %s -deconvolution-channels %s -fit-spectral-pol %s -multiscale %s %s' % (wsclean_loc,mem, ncore, '%s_%s.wsclean' % (ms1.split('.ms')[0],index), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, channels_out, deconvolution_channels, nterms, multi_scale_scales, ms1))
    else:
        os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -joinchannels -stopnegative -channelsout %s -deconvolution-channels %s -fit-spectral-pol %s %s' % (wsclean_loc,mem, ncore, '%s_%s.wsclean' % (ms1.split('.ms')[0],index), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, channels_out, deconvolution_channels, nterms, ms1))
else:
    if do_multiscale == 'True':
        os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -niter %s -stopnegative -multiscale %s %s' % (wsclean_loc,mem, ncore, '%s_%s.wsclean' % (ms1.split('.ms')[0],index), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter,multi_scale_scales, ms1))
    else:
        os.system('%s -mem %d -j %d -name %s -size %d %d -scale %sasec -weight %s -gain %.2f -mgain %.2f -auto-threshold %.1f -stopnegative -niter %s %s' % (wsclean_loc,mem, ncore, '%s_%s.wsclean' % (ms1.split('.ms')[0],index), size_scale,size_scale,cell, weight, gain, mgain, auto_threshold, niter, ms1))
