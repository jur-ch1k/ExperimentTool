# ExperimentTool

## Клонирование репозитория

## Насктройка конфигурационного файала

```json
{
  "printQueue": true,
  "runsCount": 3,
  "maxQueue": 3,
  "logTime": 5, 
  "cmd": "sbatch -p test -n {procNum} ompi xhpcg",
  "file": {
    "fileName": "/hpcg.dat",
    "text": "HPCG benchmark input file\nSandia National Laboratories; University of Tennessee, Knoxville\n{nx} {ny} {nz}\n{time}"
  },
  "paramArr": [{
    "cmdParams": {
        "procNum": [8, 14]
      },
      "fileParams": {
        "nx": [16, 64],
        "ny": [16, 64],
        "nz": [16, 64],
        "time": [15]
      }
    }
  ]
}
```
Описание параметров 
printQueue, runsCount, maxQueue, logTime - опцианальные параметры, значения по умолчанию:
<ul>
  <li>printQueue = false</li>
  <li>runsCount = 10</li>
  <li>maxQueue = 3</li>
  <li>logTime = 10</li>
</ul>

## Запуск программы
```sh
python main.py config_for_hpcg.json
```
