from funcs import readJSON, getParamsNames, getParamsCombinations, strFromParams
from datetime import datetime
import subprocess
import traceback
import time
import os
import sys
import getpass


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
        config['printQueue'] = False

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
