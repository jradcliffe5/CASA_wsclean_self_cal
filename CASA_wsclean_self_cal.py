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
path_to_casa = inputs['path_to_casa']

os.system('python run_wsclean.py %d' % -1)
for i in range(len(self_cal_solints)):
    os.system('%s --nologger --log2term -c run_casa.py %d' % (path_to_casa,i))
    os.system('python run_wsclean.py %d' % i)
os.system('python run_wsclean.py %d' % i+1)
