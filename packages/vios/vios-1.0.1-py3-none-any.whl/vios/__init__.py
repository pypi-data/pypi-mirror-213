# vios(Virtual Input and Output System)，主要定义设备驱动及执行流程，包含以下功能模块：

# 一、driver：设备驱动
#     1、所有驱动继承自BaseDriver，类名统一为Driver，并要求实现open/close/read/write四个方法。样板见VirtualDevice
#     2、以设备或厂家为名新建文件夹（并于其内新建__init__.py文件）放于driver/common内，将厂家提供的底层库（若有）置于其内

# 二、envelope：执行流程，见各模块开头的说明

# 三、collection：一些工具、函数、类或其他

# 四、tutorial：使用示例，详见模块自身说明 


import datetime
import string
import sys

import numpy as np

CLOUD = {'quafu': {'server': '124.70.54.59/qbackend',
                   'token': "Ei60GCN4eIGAUE-doAsUW54A00CUfkR539x5LTxG-om.9RDOwkDM1cDO2EjOiAHelJCL3YzM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye"
                   },
         'quafudev': {'server': '120.46.209.71/qbackend',
                      'token': "k1J_V8y_86aY_EH_Zvb-3MHkTSmihXrA92v4v7TpfvB.9lDN1kDN4UDO2EjOiAHelJCL3YzM6ICZpJye.9JiN1IzUIJiOicGbhJCLiQ1VKJiOiAXe0Jye"
                      }
         }


try:
    srv = sys.argv[1:][0]
except Exception as e:
    srv = 'quafu'

try:
    cloud = CLOUD[srv]
except Exception as e:
    print(e)


# region cloud
def get_date_range(start: str = '2023-05-18', end: str = '2023-05-25',
                   days: int = 0, hours: int = 1, dfmt: str = "%Y-%m-%d-%H"):
    dates = []
    date = start
    dt = datetime.datetime.strptime(start, dfmt)
    while date <= end:
        dates.append(date)
        dt = dt+datetime.timedelta(days=days, hours=hours)
        date = dt.strftime(dfmt)

    return dates


def plot_stat(dates: list[str], counts: list[int]):
    import matplotlib.pyplot as plt
    _x = [s[6:] for s in dates]
    plt.bar(_x, counts, color='lightblue', edgecolor='k')
    plt.plot(counts, '-go', lw=2)
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Tasks/Day')
    plt.grid()


TABLE = string.digits+string.ascii_uppercase


def basen(number: int, base: int, table: str = TABLE):
    mods = []
    while True:
        div, mod = divmod(number, base)
        mods.append(mod)
        if div == 0:
            mods.reverse()
            return ''.join([table[i] for i in mods])
        number = div


def baser(number: str, base: int, table: str = TABLE):
    return sum([table.index(c)*base**i for i, c in enumerate(reversed(number))])
# endregion cloud


# region performance
def analyze(info: list[dict], start: int = 0):
    ppl, dvm = {}, {}
    for sid, record in enumerate(info):
        for name in ['Cal', 'Dev', 'Dem']:
            if name in ppl:
                ppl[name].append(record['summary'][name])
            else:
                ppl[name] = [record['summary'][name]]

        for step, device in record['details'].items():
            for dev, val in device.items():
                if val['actual'] <= 0.0:
                    continue
                key = f'{step}.{dev}'
                if key in dvm:
                    dvm[key].append(val['actual'])
                else:
                    dvm[key] = [val['actual']]
    return ppl, dvm


def barplot(ax, data: dict, width: float = 0.35, threshod: float = 0.0, title: str = 'Performance'):
    for i, (k, v) in enumerate(data.items()):
        if i == 0:
            bottom = np.zeros(len(v))
            ticks = list(range(len(v)))
        value = np.asarray(v)
        if value.max() >= threshod:
            label = ax.bar(ticks, value, width, yerr=0.0,
                           bottom=bottom, label=k)
            bottom += value
        else:
            label = ''

    ax.set_xlabel('Step')
    ax.set_ylabel('Duration (s)')
    ax.set_title(title)
    ax.legend()
# endregion performance
