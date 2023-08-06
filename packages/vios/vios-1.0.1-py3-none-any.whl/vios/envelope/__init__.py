"""本模块为实验中需由用户实现的部分构成。模块调用所需参数见各自模块的说明文档。
每个实验Step依次流经以下环节即执行完毕。实验者可以自行定各环节行为，即

@compiler       -->   @rule           -->   @calculator       -->   @device          -->   @demodulator
    |           |       |             |          |            |        |             |          |
    &ccompile -->       &decode       |          &calculate   |        &read|write -->          &process
                        |             |          |            |
                        &preprocess -->          &calibrate   | 
                                                 |            |
                                                 &crosstalk --> 

>>> 线路编绎：compiler.ccompile，编绎Step中的线路生成对应操作的波形。核心功能由HKXu提供
>>> 指令规则：rule.decode--->preprocess，通道规则，如通道如何映射、多个波形共用一个通道时如何处理
>>> 指令处理：calculator.calculate--->calibrate--->crosstalk，包括采样、失真、串扰、校准等操作
>>> 设备读写：device.read|write，将处理后的指令送入设备执行
>>> 数据处理：demodulator.process--->postprocess，将从设备得到的结果进行解调等处理。最终数据处理由postprocess定义
"""


from .calculator import calculate, calibrate, crosstalk
from .compiler import QuarkLocalConfig, ccompile
from .demodulator import postprocess, process
from .device import read, write
from .rule import MAPPING, decode, preprocess
