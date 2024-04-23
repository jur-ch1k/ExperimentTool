import subprocess
import traceback
from datetime import datetime
import time
import json
import os
import sys
import itertools
import getpass


def readJSON(path):
    with open(path, 'r') as f:
        file = f.read()
    return json.loads(file)


def getParamsNames(paramArr):
    fileParamsNames = None
    cmdParamsNames = None

    if 'fileParams' in paramArr[0]:
        fileParamsNames = list(paramArr[0]['fileParams'].keys())
    if 'cmdParams' in paramArr[0]:
        cmdParamsNames = list(paramArr[0]['cmdParams'].keys())

    return {'fileParams': fileParamsNames, 'cmdParams': cmdParamsNames}


def getParamsCombinations(params, paramsNames):
    combinations = []
    paramDict = dict.fromkeys(paramsNames)
    for paramList in itertools.product(*list(params.values())):
        for i in range(len(paramsNames)):
            paramDict[paramsNames[i]] = paramList[i]
        combinations.append(paramDict.copy())
    return combinations


def strFromParams(paramDict, templateStr):
    if paramDict:
        for params in paramDict:
            yield templateStr.format(**params)
    else:
        yield templateStr


if __name__ == '__main__':

    print('main poc PID = ' + str(os.getpid()))
    sys.stdout.flush()

    config = readJSON(sys.argv[1])
    if 'runsCount' not in config:
        config['runsCount'] = 10
    if 'maxQueue' not in config:
        config['runsCount'] = 3
    if 'logTime' not in config:
        config['logTime'] = 10
    if 'printQueue' not in config:
        config['printQueue'] = false

    longUserName = getpass.getuser()
    shortUserName = longUserName[:8]
    queueCmd = ['squeue', '-u', longUserName]

    paramCount = len(config['paramArr'])
    if paramCount == 0:
        print('paramArr is empty. Add at least one item')
        sys.exit(1)

    paramsNames = getParamsNames(config['paramArr'])

    for paramArrElem in config['paramArr']:
        fileParamsDict = None
        cmdParamDict = None
        if 'cmdParams' in paramArrElem:
            cmdParamDict = getParamsCombinations(paramArrElem['cmdParams'], paramsNames['cmdParams'])
        if 'fileParams' in paramArrElem:
            fileParamsDict = getParamsCombinations(paramArrElem['fileParams'], paramsNames['fileParams'])

        output = subprocess.check_output(queueCmd).decode('ascii')

        for cmd in strFromParams(cmdParamDict, config['cmd']):
            for file in strFromParams(fileParamsDict, config['file']['text']):
                try:
                    with open(config['file']['fileName'], 'w') as f:
                        f.write(file)
                    print('\nCurrent running config:\n' + cmd + '\n' + file
                          + '\ntime: ' + datetime.now().strftime('%H:%M:%S'))
                    sys.stdout.flush()

                    for i in range(config['runsCount']):
                        while True:
                            if output.count(shortUserName) != config['maxQueue']:
                                output = subprocess.check_output(cmd.split()).decode('ascii')
                                print('Started: ' + output.split(' ')[-1])
                                output = subprocess.check_output(queueCmd).decode('ascii')
                                break
                            else:
                                print('Waiting...')
                                if (config['printQueue']):
                                    print(output)
                                sys.stdout.flush()
                                time.sleep(config['logTime'])
                                output = subprocess.check_output(queueCmd).decode('ascii')
                        sys.stdout.flush()
                    while output.count(shortUserName) != 0:
                        output = subprocess.check_output(queueCmd).decode('ascii')
                        print('Waiting current config to finish')
                        if (config['printQueue']):
                            print(output)
                        sys.stdout.flush()
                        time.sleep(config['logTime'])
                except Exception:
                    print(traceback.print_exc(file=sys.stdout))
                    sys.stdout.flush()

            print('Main loop finished, whaitig all tasks...\n')
            sys.stdout.flush()

            output = subprocess.check_output(queueCmd).decode('ascii')
            while output.count(shortUserName) != 0:
                time.sleep(config['logTime'])
                print('Waiting...')
                if (config['printQueue']):
                    print(output)
                sys.stdout.flush()
                output = subprocess.check_output(queueCmd).decode('ascii')
                sys.stdout.flush()
