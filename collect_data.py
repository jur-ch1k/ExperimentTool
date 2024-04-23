from funcs import readJSON, tupleForSort
from collections import defaultdict
import os
import sys


if __name__ == '__main__':

    config = readJSON(sys.argv[1])
    files = os.listdir(config['path'])
    lines = []
    data = []
    if config['separator'] == ' ':
        config['separator'] = None

    for file in files:
        tmp = []
        if config['fileMask'] in file:
            with open(config['path'] + '/' + file) as f:
                lines = f.readlines()

                tmp += [file]
                for elem in config['collectFrom']:
                    try:
                        tmp += lines[elem['line']-1].split(config['separator'])[elem['word']-1],
                    except IndexError:
                        tmp += [None]

            if 'orderBy' in config:
                for i, elem in enumerate(config['orderBy']):
                    value = lines[elem['line']-1].split(config['separator'])[elem['word']-1]
                    tmp += [value]
            data += [tmp]

    if 'orderBy' in config:
        combinations = defaultdict(list)
        collectLen = len(config['collectFrom']) + 1
        for tmp in data:
            combinations[tuple(tmp[collectLen:])] += [tmp[:collectLen]]
        for key in sorted(combinations.keys(), key=lambda x: tupleForSort(x, config)):
            print(*key)
            for elem in combinations[key]:
                print(*elem, sep='\t')

    else:
        for tmp in sorted(data, key=lambda x: x[0]):
            print(*tmp, sep='\t')
