"""线路编绎，并返回编绎后的结果及相关额外参数
"""


import numpy as np
from lib import stdlib
from waveforms.qlisp import compile as _compile
from waveforms.systemq_kernel.lib.arch.baqis import assembly_code
from waveforms.systemq_kernel.lib.arch.baqis_config import QuarkLocalConfig
from waveforms.systemq_kernel.qlisp import Signal


def _form_signal(sig):
    sig_tab = {
        'trace': Signal.trace,
        'iq': Signal.iq,
        'state': Signal.state,
        'count': Signal.count,
        'diag': Signal.diag,
        'population': Signal.population,
        'trace_avg': Signal.trace_avg,
        'iq_avg': Signal.iq_avg,
        'remote_trace_avg': Signal.remote_trace_avg,
        'remote_iq_avg': Signal.remote_iq_avg,
        'remote_state': Signal.remote_state,
        'remote_population': Signal.remote_population,
        'remote_count': Signal.remote_count,
    }
    if isinstance(sig, str):
        if sig == 'raw':
            sig = 'iq'
        try:
            return sig_tab[sig]
        except KeyError:
            pass
    elif isinstance(sig, Signal):
        return sig
    raise ValueError(f'unknow type of signal "{sig}".'
                     f" optional signal types: {list(sig_tab.keys())}")


def ccompile(circuit: list, cfg: QuarkLocalConfig, **kwds):
    """编绎线路

    Args:
        circuit (list): 用户定义的线路(@HK)
        cfg (QuarkQuarkLocalConfigConfig): 线路编绎所需配置

    Returns:
        tuple: 编绎后的线路，数据处理所需参数

    >>> from quark import connect
    >>> s = connect('QuarkServer')
    >>> cfg = QuarkLocalConfig(s.snapshot())
    >>> circuit = [(('Measure',0),'Q0503')]
    >>> ccompile(circuit,cfg,signal='iq')

    """
    kwds['signal'] = _form_signal(kwds.get('signal'))
    kwds['lib'] = stdlib

    # print('Compiling', circuit)
    code = _compile(circuit, cfg=cfg, **kwds)
    cmds, datamap = assembly_code(code)
    # print('Compiled', cmds)
    compiled = {}
    for cmd in cmds:
        ctype = type(cmd).__name__  # WRITE,TRIG,READ
        if ctype == 'WRITE':
            step = 'main'
        else:
            step = ctype
        op = (ctype, cmd.address, cmd.value, '')
        if step in compiled:
            compiled[step].append(op)
        else:
            compiled[step] = [op]
    return compiled, {'dataMap': datamap}


# %%
if __name__ == "__main__":
    import doctest
    doctest.testmod()
