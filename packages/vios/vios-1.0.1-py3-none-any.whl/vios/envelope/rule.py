"""设备逻辑预处理，数据后处理
"""
# 设备通道与config表中字段的映射关系
MAPPING = {
    "setting_LO": "LO.Frequency",
    "setting_POW": "LO.Power",
    "setting_OFFSET": "ZBIAS.Offset",
    "waveform_RF_I": "I.Waveform",
    "waveform_RF_Q": "Q.Waveform",
    "waveform_TRIG": "TRIG.Marker1",
    "waveform_SW": "SW.Marker1",
    "waveform_Z": "Z.Waveform",
    "setting_PNT": "ADC.PointNumber",
    "setting_SHOT": "ADC.Shot",
    "setting_TRIGD": "ADC.TriggerDelay"
}


suffix = ('Waveform', 'Shot', 'Coefficient', 'TriggerDelay')


def decode(target: str, context: dict, mapping: dict = MAPPING):
    """Qubit等属性与硬件通道之间的映射转换

    Args:
        target (str): 待解析对象，如Q0.setting.LO
        context (dict): 对象所在cfg的字段
        mapping (dict, optional): 通道和硬件属性的映射关系. Defaults to MAPPING.

    Raises:
        KeyError: 通道映射不存在
        ValueError: 通道不存在

    Returns:
        str: 通道，如AD.CH1.TraceIQ
    """
    try:
        mkey = target.split('.', 1)[-1].replace('.', '_')
        chkey, quantity = mapping[mkey].split('.', 1)
    except KeyError as e:
        raise KeyError(f'{e} not found in mapping!')

    try:
        channel = context.get('channel', {})[chkey]
    except KeyError as e:
        raise KeyError(f'{chkey} not found!')

    if channel is None:
        raise ValueError('ChannelNotFound')
    elif 'Marker' not in channel:
        channel = '.'.join((channel, quantity))

    return channel


def merge(context: dict, cached: dict = {'Q0101.calibration.Z.delay': 12345}):
    """合并指令执行上下文环境，如将{'Q0101.calibration.z.delay':12345}合并至Q0101
    context['target']: 如Q010.waveform.Z，根据Q0101来判断合并cached中的哪个字段

    Args:
        context (dict): 从cfg表中获取，即Qubit、Coupler等字段
        cached (dict): 无实际通道的指令缓存，形如{'Q0101.calibration.z.delay':12345}
    """
    for ck, cv in cached.items():
        node, path = ck.split('.', 1)
        if context['target'].startswith(node):
            for k in path.split('.'):
                dk = context.get(k, {})
                if isinstance(dk, dict):
                    context = dk
                    continue
                context[k] = cv


def preprocess(target: str, cmd: list, cache: dict, bypass: dict = {}):
    """设备逻辑预处理（如相同通道写多个波形等），处理完毕送往calculator进行采样等计算。

    Args:
        target (str): 设备通道，如AWG.CH1.Waveform
        cmd (list): 待执行指令，格式为(READ|WRITE,value,unit,kwds)。其中kwds为
                    {'target':'原始指令如Q0101.waveform.Z', 
                     'filter':calculator中波形是否采样列表,
                     'srate':'对应设备采样率',
                     'context':'cfg表中字段，如Q0101', 
                     'cached':'无实际通道指令，详见merge函数'}
        cache (dict): 已缓存指令，格式为{target: cmd}
        bypass (dict): 缓存重复指令以避免重复设置
    """
    kwds = cmd[-1]

    # 重复指令缓存
    if target in bypass and target.endswith(suffix) and bypass[target][0] == cmd[1]:
        return cache
    bypass[target] = (cmd[1], kwds['target'])

    # context设置，用于calculator.calculate
    context = kwds.pop('context', {})  # 即Qubit、Coupler等
    if context:
        kwds['LEN'] = context['waveform']['LEN']
        kwds['calibration'] = context['calibration']
        merge(context=kwds, cached=kwds.pop('cached', {}))

    # 波形采样率设置
    if target.endswith('Waveform') and type(cmd[1]).__name__ == 'Waveform':
        cmd[1].sample_rate = kwds['srate']

    # 处理多通道共用逻辑
    if target in cache and target.endswith('Waveform'):
        cache[target][1] += cmd[1]
    else:
        cache[target] = cmd
    return cache
