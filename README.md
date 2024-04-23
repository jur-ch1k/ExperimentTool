# ExperimentTool

## Клонирование репозитория

```commandline
git clone https://github.com/jur-ch1k/ExperimentTool
```

## Обзор компанентов

<ul>
    <li>test_runner.py позволяет автоматически запускать задачи в очередь, управляему через компонент slurm, перебирая в это время все настроенные комбинации параметров.</li>
    <li>С попощью collect_data.py возможно собирать однотипыне данные из большого количетсва файлов.</li>
</ul>

## Насктройка конфигурационного файала для test_runner

```json
{
  "printQueue": true,
  "logTime": 5,
  "runsCount": 3,
  "maxQueue": 3,
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
<ol>
  <li>printQueue - влк/выкл печати в очереди задачи в лог</li>
  <li>logTime - время в секундах, через которое будут писаться логи</li>
  <li>runsCount - число повторных запусков с одной конфигурацией параметров</li>
  <li>maxQueue - максимальное число задач в очереди</li>
  <li>cmd - значение командной строки, используемое для запуска</li>
  <li>file - описание конфигурационного файла использумого запускаемой программой
    <ol>
      <li>fileName - полный путь к файлу</li>
      <li>text - содержимое конфигурационного файла</li>
    </ol>
  </li>
  <li>paramArr - массив содержащий в себе все значения подставляемых параметров
    <ol>
      <li>cmdParams - объект содержащий в себе все необоходимые значения параметров, подствляемые в конмадную строку</li>
      <li>fileParams - объект содержащий в себе все необоходимые значения параметров, подствляемые в конфигурационный файл</li>
      <ul>
        <li>В cmdParams и fileParams объектах имена полей должны совпадать со значениями выделенными в фигурные скобки ранее в полях cmd и file. (в указанном выше примере это procNum в cmd, а также nx, nx, nx и time в file)</li>
        <li>Все поля этих обектов должны быть всегда массивами!</li>
      </ul>
    </ol>
  </li>
</ol>

<p>file и paramArr являются опицональныеми параметрами</p>
<p>printQueue, runsCount, maxQueue, logTime - также опцианальные параметры и имеют значения по умолчанию:</p>

<ul>
  <li>printQueue = false</li>
  <li>runsCount = 10</li>
  <li>maxQueue = 3</li>
  <li>logTime = 10</li>
</ul>

## Запуск программы test_runner
```commandline
python test_runner.py config_for_hpcg.json
```
Передача JSON-файла обязательна

## Насктройка конфигурационного файала для collect_data
## Запуск программы collect_data