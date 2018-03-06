import os,re,sys
import numpy as np

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

def test_list(inputs,float):
    if ',' in str(inputs):
        inputs = inputs.split(',')
        if float == True:
            inputs = [float(i) for i in inputs]
    else:
        if float == True:
            inputs = [float(inputs)]
        else:
            inputs = [str(inputs)]
    return inputs

inputs = headless('inputs.txt')
self_cal_solints = test_list(inputs['self_cal_solint'],float=False)
self_cal_type = test_list(inputs['self_cal_type'],float=False)
combine = test_list(inputs['sc_combine'],float=False)
measurement_set = str(inputs['ms'])
minsnr = float(inputs['minsnr'])

try:
    i = int(sys.argv[sys.argv.index('run_casa.py')+1])
except IndexError:
    print 'Failed...run_casa.py'

gaintable = []
spwmap = []
interp = []
tb.open(measurement_set+'/SPECTRAL_WINDOW/')
nspw = np.zeros(len(tb.getcol('REF_FREQUENCY'))).astype(int).tolist()
tb.close()

for j in range(i):
    gaintable = gaintable + ['%s.%s%d' % (measurement_set.split('.ms')[0],self_cal_type[j],j)]
    interp = interp + ['linear']
    if combine[j] == 'spw':
        spwmap = spwmap + [nspw]
    else:
        spwmap = spwmap + [np.array([])]

print gaintable
print spwmap

if self_cal_type[i] == 'p':
    minblperant = 3
else:
    minblperant = 4
gaincal(vis=measurement_set, caltable='%s.%s%d' % (measurement_set.split('.ms')[0],self_cal_type[i],i), solint=self_cal_solints[i], combine=combine[i], calmode=self_cal_type[i],gaintable=gaintable,parang=True,minsnr=minsnr,minblperant=minblperant,interp=interp,spwmap=spwmap)

gaintable = gaintable + ['%s.%s%d' % (measurement_set.split('.ms')[0],self_cal_type[i],i)]
interp = interp + ['linear']
if combine[i] == 'spw':
    spwmap = spwmap + [nspw]
else:
    spwmap = spwmap + [np.array([])]

applycal(vis=measurement_set,gaintable=gaintable,interp=interp,parang=True,spwmap=spwmap)

plotcal(caltable='%s.%s%d' % (measurement_set.split('.ms')[0],self_cal_type[i],i), xaxis='time', yaxis='phase', subplot=321, iteration='antenna', showgui=False, plotrange=[0,0,-180,180], figfile='%s_%s%d.pdf' % (measurement_set.split('.ms')[0],self_cal_type[i],i))

if (self_cal_type[i] == 'ap') or (self_cal_type[i] =='a'):
    plotcal(caltable='%s.%s%d' % (measurement_set.split('.ms')[0],self_cal_type[i],i), xaxis='time', yaxis='amp', subplot=321, iteration='antenna', showgui=False, figfile='%s_%s%d_amp.pdf' % (measurement_set.split('.ms')[0],self_cal_type[i],i))
