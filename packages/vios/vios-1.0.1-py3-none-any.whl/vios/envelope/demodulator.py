"""所有仪器操作的结果，以字典形式传给process进行处理，
处理完毕存入server，可供用户获取。
"""


import numpy as np
import requests
from waveforms.qlisp import get_arch, register_arch

from waveforms.systemq_kernel.lib.arch import baqisArchitecture
from vios import CLOUD

register_arch(baqisArchitecture)


def demodulate(raw_data, **kwds):
    pass


def process(raw_data, **kwds):
    """处理数据

    Args:
        raw_data (dict): 从设备获取的原始结果

    Returns:
        dict: 处理后的数据，形式为{'key1':np.array,'key2':np.array, ...}
    """
    # print('ddddddddddoooooooooooooooooooooo', kwds)
    # print("=============================================",raw_data)

    dataMap = kwds.get('dataMap', {'arch': 'baqis'})
    result = {}

    try:

        if 'arch' in dataMap and dataMap['arch'] == 'general':
            return raw_data['READ']['AD']
        elif list(dataMap.keys()) == ['arch']:  # for NA
            if 'READ' in raw_data:
                print(raw_data)
                nadata = result['data'] = raw_data['READ']['NA']
                if 'CH1.Trace' in nadata:
                    result['data'] = raw_data['READ']['NA'].pop('CH1.Trace')
                elif 'CH1.S' in nadata:
                    result['data'] = raw_data['READ']['NA'].pop('CH1.S')
            result['extra'] = raw_data
        else:
            result = get_arch(dataMap['arch']).assembly_data(raw_data, dataMap)
    except Exception as e:
        print('>'*10, 'Failed to process the result', e, '<'*10)
        result['error'] = [
            f'Failed to process the result, raise Exception: {e.__class__.__name__}("{str(e)}")',
            raw_data,
            dataMap
        ]

    return result


def postprocess(result: dict):
    """任务执行完后对数据的操作，如存储到自定义路径或回传到云平台等

    Args:
        result (dict): 任务结果，包含数据段和基本描述信息
    """
    def _delete_dict(ret: dict, num: int = 0):
        while num>0:
            tmp = np.cumsum(list(ret.values()))
            ran_num = np.random.randint(tmp[-1]+1)
            ran_pos = np.searchsorted(tmp, ran_num)
            ret[list(ret.keys())[ran_pos]] -= 1
            num -= 1

    # print(result.keys(),result['meta'].keys())

    meta = result['meta']
    print('Send result back  to', meta['user'])
    if not meta['user'].startswith('quafu'):
        return
    
    srv = CLOUD[meta['user']]

    task_id = hex(meta['tid'])[2:].upper()
    task_status = 'failed'
    if meta['status'] in ['Finished','Archived']:
        task_status = 'finished'
        try:
            data: list[dict] = result['data']['count']
        except Exception as e:
            print('Failed to process result',e)
            task_status = 'failed'
    
    if task_status == 'finished':
        dres = {}
        for dat in data:
            for k, v in dat.items():
                dres[k] = dres.get(k, 0)+v

        shots = sum(dres.values())
        # _delete_dict(dres, shots - (shots//1000)*1000)

        dic_res = {}
        for k, v in dres.items():
            dic_res[''.join((str(i) for i in k))] = v

        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": str(dic_res).replace("\'", "\""),
                     "res": str(dic_res).replace("\'", "\""),
                     "server": 2}

    elif task_status == 'failed':
        post_data = {"task_id": task_id,
                     "status": task_status,
                     "raw": "",
                     "res": "",
                     "server": 2}
    # print(post_data)
    try:
        resp = requests.post(url=f"http://{srv['server']}/scq_result/",
                             data=post_data,
                             headers={'api_token': srv['token']})
        print(resp.text)
    except:
        print('POST ERROR')
