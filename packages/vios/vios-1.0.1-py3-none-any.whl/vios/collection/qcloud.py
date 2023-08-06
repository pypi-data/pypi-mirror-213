QMAP = {0: 'Q0101', 1: 'Q0102', 2: 'Q0103', 3: 'Q0104', 4: 'Q0105', 5: 'Q0106', 6: 'Q0107', 7: 'Q0109', 8: 'Q0110', 9: 'Q0111', 10: 'Q0112',
        11: 'Q0201', 12: 'Q0202', 13: 'Q0203', 14: 'Q0204', 15: 'Q0205', 16: 'Q0206', 17: 'Q0208', 18: 'Q0209', 19: 'Q0210', 20: 'Q0211', 21: 'Q0212',
        22: 'Q0301', 23: 'Q0302', 24: 'Q0303', 25: 'Q0304', 26: 'Q0305', 27: 'Q0306', 28: 'Q0307', 29: 'Q0308', 30: 'Q0309', 31: 'Q0310', 32: 'Q0311', 33: 'Q0312',
        34: 'Q0401', 35: 'Q0402', 36: 'Q0403', 37: 'Q0404', 38: 'Q0405', 39: 'Q0406', 40: 'Q0407', 41: 'Q0408', 42: 'Q0409', 43: 'Q0410', 44: 'Q0411', 45: 'Q0412',
        46: 'Q0501', 47: 'Q0503', 48: 'Q0504', 49: 'Q0505', 50: 'Q0506', 51: 'Q0507', 52: 'Q0509', 53: 'Q0510', 54: 'Q0511',
        55: 'Q0601', 56: 'Q0602', 57: 'Q0603', 58: 'Q0604', 59: 'Q0605', 60: 'Q0606', 61: 'Q0607', 62: 'Q0608', 63: 'Q0609', 64: 'Q0610', 65: 'Q0611', 66: 'Q0612',
        67: 'Q0701', 68: 'Q0702', 69: 'Q0703', 70: 'Q0704', 71: 'Q0705', 72: 'Q0706', 73: 'Q0708', 74: 'Q0709', 75: 'Q0710', 76: 'Q0711', 77: 'Q0712',
        78: 'Q0801', 79: 'Q0802', 80: 'Q0803', 81: 'Q0804', 82: 'Q0805', 83: 'Q0806', 84: 'Q0807', 85: 'Q0808', 86: 'Q0809', 87: 'Q0810', 88: 'Q0811', 89: 'Q0812',
        90: 'Q0901', 91: 'Q0902', 92: 'Q0903', 93: 'Q0904', 94: 'Q0905', 95: 'Q0906', 96: 'Q0907', 97: 'Q0908', 98: 'Q0909', 99: 'Q0910', 100: 'Q0911', 101: 'Q0912',
        102: 'Q1001', 103: 'Q1002', 104: 'Q1003', 105: 'Q1004', 106: 'Q1005', 107: 'Q1006', 108: 'Q1007', 109: 'Q1008', 110: 'Q1009', 111: 'Q1010', 112: 'Q1012',
        113: 'Q1101', 114: 'Q1102', 115: 'Q1103', 116: 'Q1104', 117: 'Q1105', 118: 'Q1106', 119: 'Q1107', 120: 'Q1108', 121: 'Q1109', 122: 'Q1110', 123: 'Q1111',
        124: 'Q1201', 125: 'Q1202', 126: 'Q1203', 127: 'Q1204', 128: 'Q1205', 129: 'Q1206', 130: 'Q1207', 131: 'Q1208', 132: 'Q1209', 133: 'Q1210', 134: 'Q1211', 135: 'Q1212'
        }



import re
import time
from pprint import pprint

import numpy as np

from vios import CLOUD

from . import Task, s

default_shots = 1000

try:
    from quafu import QuantumCircuit, Task as QuafuTask, User

    user = User()
    user.save_apitoken(CLOUD['quafu']['token'])
    task = QuafuTask()
    task.config(backend="ScQ-P136", shots=3000, compile=True)
except Exception as e:
    print(e)


def send_to_quafu(circuit: str, shots: int = 3000):
    task.submit_history.clear()
    task.config(backend="ScQ-P136", shots=shots, compile=True)
    qc = QuantumCircuit(circuit.count('measure'))
    qc.from_openqasm(circuit)

    task.send(qc, wait=False, group='HW')

    while True:
        try:
            res = task.retrieve_group('HW', verbose=False)
            if res:
                break
            time.sleep(2)
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{t}  wait for result', end='\r')
        except Exception as e:
            time.sleep(2)
            t = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f'{t} failed to wait for result', end='\r')
            continue

    # status_map = {0:"In Queue", 1:"Running", 2:"Completed", "Canceled":3, 4:"Failed"}
    return qc, task, res[0]


def openqasm_to_qlisp(openqasm: str, QMAP: dict=QMAP):
    t = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{'='*80}\r\n|{t}{' '*10}{'Transform circuit to qlisp'.ljust(68-len(t))} {openqasm.count('measure')}|\r\n{'='*80}")
    if openqasm.count('measure') > 0:
        print(openqasm)

    lines = openqasm.split(';')

    qlisp = []
    read_qubits = []
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue
        
        operations_qbs = line.split(" ")
        operations = operations_qbs[0]
        if operations == "qreg":
            qbs = operations_qbs[1]
            num = int(re.findall("\d+", qbs)[0])
        elif operations == "creg":
            pass
        elif operations == "measure":
            mb = int(re.findall("\d+", operations_qbs[1])[0])
            cb = int(re.findall("\d+", operations_qbs[3])[0])
            qlisp.append((("Measure", cb), QMAP[mb]))
            read_qubits.append(QMAP[mb])
        else:
            qbs = operations_qbs[1]
            indstr = re.findall("\d+", qbs)
            inds = [int(indst) for indst in indstr]
            if operations == "barrier":
                qlisp.append(("Barrier", tuple([QMAP[i] for i in inds])))
            else:
                sp_op = operations.split("(")
                gatename = sp_op[0]
                if len(sp_op) > 1:
                    paras = sp_op[1].strip("()")
                    parastr = paras.split(",")
                    # paras = [eval(parai, {"pi":pi}) for parai in parastr]
                    paras = []
                    for parai in parastr:
                        if parai.endswith('ns'):
                            paras.append(eval(parai.removesuffix('ns'))*1e-9)
                        else:
                            paras.append(eval(parai, {"pi": np.pi}))

                if gatename == "cx":
                    qlisp.append(("Cnot", (QMAP[inds[0]], QMAP[inds[1]])))
                elif gatename == 'delay':
                    qlisp.append((('Delay', *paras), QMAP[inds[0]]))
                elif gatename == "cz":
                    qlisp.append(("CZ", (QMAP[inds[0]], QMAP[inds[1]])))
                elif gatename == "rx":
                    qlisp.append((("Rx", *paras), QMAP[inds[0]]))
                elif gatename == "ry":
                    qlisp.append((("Ry", *paras), QMAP[inds[0]]))
                elif gatename == "rz":
                    qlisp.append((("Rz", *paras), QMAP[inds[0]]))
                elif gatename in ("xyzh"):
                    qlisp.append((gatename.upper(), QMAP[inds[0]]))
                elif gatename in ["u1", "u2", "u3"]:
                    qlisp.append(((gatename, *paras), QMAP[inds[0]]))

    return qlisp, read_qubits


def readout_cali(qubits, repeat=1,user:str='quafu',priority:int=15):

    task = {'metainfo': {'name': f'testtask:/Scatter', 'priority': priority, 'user': user,'mutex':False,
                         'other': {'shots': 1024, 'signal': 'iq'}},
            'taskinfo': {'STEP': {'main': ['WRITE', ('repeat',)],
                                  'trigger': ['WRITE', 'trig'],
                                  'READ': ['READ', 'read'],
                                  },
                         'CIRQ': [[*[(g, q) for q in qubits],
                                  ('Barrier', tuple(qubits)),
                                  *[(('Measure', i), q) for i, q in enumerate(qubits)]
                                   ] for g in ['I', 'X']*repeat],
                         'LOOP': {'repeat': [('repeat', np.arange(repeat*2), '1')],
                                  'trig': [('LH_Trig.CH1.TRIG', 0, 'any')]
                                  }
                         },
            }
    
    t = Task(task, 500.0)
    t.run()
    t.join()
    
    result = np.asarray(t.result()['iq'])
    s0, s1 = np.concatenate(result[::2,...],0),np.concatenate(result[1::2,...],0)

    from qos_tools.analyzer.lib import analyzer_Scatter2
    cali = {}
    for i, q in enumerate(qubits):
        flag, ans = analyzer_Scatter2(s0[:, i], s1[:, i], tol=0.2)
        readout_type = s.query(f'gate.Measure.{q}.default_type')
        if readout_type == 'default':
            readout_type = 'params'
        if flag:
            cali[f'gate.Measure.{q}.{readout_type}.threshold'] = ans[0]
            cali[f'gate.Measure.{q}.{readout_type}.phi'] = ans[1] 
    
    pprint(cali)
    for k, v in cali.items():
        s.update(k, v)


def run_circut(circuit, shots: int = 1024, read_qubits: list[str] =[], tid: int=0, 
               name: str='QuafuCircuit', user: str='quafu', priority: int=15, result: bool = False):

    if shots<=1000:
        repeat = 1
    else:
        repeat = (shots+default_shots-1)//default_shots
        shots = 1000

    cloud = {'metainfo': {'name': f'testtask:/{name}','priority': priority, 'user': user,'mutex':False,
                          'other': {'shots': shots, 'signal': 'count'}},
             'taskinfo': {'STEP': {'main': ['WRITE', ('repeat',)],
                                   'trigger': ['WRITE', 'trig'],
                                   'READ': ['READ', 'read'],
                                   },
                          'CIRQ': [circuit]*repeat,
                          'LOOP': {'repeat': [('repeat', np.arange(repeat), '1')],
                                   'trig': [('LH_Trig.CH1.TRIG', 0, 'any')]
                                   }
                          },
             }

    # t = time.strftime('%Y-%m-%d %H:%M:%S')
    # print(f"{'='*80}\r\n|{t}{' '*18}{'Running scatter on systemQ'.ljust(60-len(t))}|\r\n{'='*80}")

    # try:
    #     readout_cali(read_qubits) 
    # except Exception as e:
    #     print('Failed to calibrate readout', e)
    if tid:
        cloud['metainfo']['tid'] = tid

    t = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{'='*80}\r\n|{t}{' '*10}{f'Running {tid} {shots}'.ljust(68-len(t))}|\r\n{'='*80}")
    # pprint(circuit)

    task = Task(cloud, 500.0)
    task.run()
    # task.join()

    ret = {}
    if result:
        task.join()
        def _union_dict(ret: dict, count: dict):
            for k, v in count.items():
                ret[k] = ret.get(k, 0)+v

        def _delete_dict(ret: dict, num: int = 0):
            while num > 0:
                tmp = np.cumsum(list(ret.values()))
                ran_num = np.random.randint(tmp[-1]+1)
                ran_pos = np.searchsorted(tmp, ran_num)
                ret[list(ret.keys())[ran_pos]] -= 1
                num -= 1

        res = task.result()['count']
        

        for i in range(repeat):
            _union_dict(ret, res[i])
        # _delete_dict(ret, default_shots*repeat-shots)
        print('res',ret)

    t = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"{'='*80}\r\n|{t}{' '*10}{f'Finished {tid} {default_shots*repeat}'.ljust(68-len(t))}|\r\n{'='*80}")

    return ret, task.status()['status']


circ = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[136];
creg c[8];
h q[119];
cx q[119],q[108];
cx q[108],q[109];
cx q[109],q[110];
barrier q[119],q[108],q[109],q[110];
measure q[119] -> c[0];
measure q[108] -> c[1];
measure q[109] -> c[2];
measure q[110] -> c[3];"""


if __name__ == '__main__':
    circ = 'OPENQASM 2.0;include qelib1.inc;qreg q[8];creg c[8];h q[0];h q[1];cx q[0],q[1];measure q[0] -> c[0];measure q[1] -> c[1];'.replace(';',';\n')
    # qlisp, qubits = openqasm_to_qlisp(circ, QMAP)
    # try:
    #     result, task_status = run_circut(
    #         qlisp, shots=1024*1, read_qubits=qubits, result=True, user='yltest', tid=12)
    # except Exception as e:
    #     import traceback
    #     traceback.print_exc()
    #     result, task_status = {}, 'failed'

    # print(result, task_status)
    print(send_to_quafu(circ)[-1])

