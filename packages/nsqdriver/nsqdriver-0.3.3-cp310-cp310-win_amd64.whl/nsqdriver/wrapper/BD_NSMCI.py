import time
from typing import Dict, Any, List

import numpy as np

from nsqdriver import MCIDriver, QSYNCDriver


try:
    import Instrument
except ImportError as e:
    class Instrument(object):
        ...


class NSInstrument(Instrument):
    """ Instrument for GuoDun devices """
    ParameterMC = {
        'OUTSrate': 8e9,      # 配置OUT通道采样率
        'OUTMix': 2,          # 设置OUT通道增强第二奈奎斯特区信号
        'INZone': 'zone3'     # 设置IN通道输入为Zone4，即要IN通道要采集的信号范围为6~8G
    }
    ParameterZ = {
        'OUTSrate': 2e9,      # 配置OUT通道采样率
        'OUTMix': 1,          # 设置OUT通道增强第一奈奎斯特区信号
        'KeepAmp': 2          # 开启Z通道的保持电平模式，2为保持drive信号电平
    }
    ParameterQSYNC = {
        'RefClock': 'in'      # MC112的100M参考信号来源，机箱上的100M IN没有接的情况下，选择为in，反之选out
    }

    def __init__(self):
        """ Initialization """
        super(NSInstrument, self).__init__()

        # 设备驱动
        self.driver_mc: MCIDriver = MCIDriver('192.168.111.152')
        self.driver_z: MCIDriver = MCIDriver('192.168.111.132')
        self.qsync: QSYNCDriver = QSYNCDriver('192.168.111.152')

        # 参数
        self.waves = dict()
        self.roFreq = dict()
        self.roQubits = dict()
        self.roLength = dict()
        self.roDADelay = dict()
        self.zpdc = dict()
        self.group = dict()
        self.roLines = dict()
        self.connectDict = dict()
        self.deviceDict = dict()
        self.qubitROChannels = dict()
        self.integrationDelay = dict()
        self.inputRange = dict()
        self.outputRange = dict()
        self.devices = {
            'awg': self.driver_mc,
            'dc': self.driver_z,
            'qa': self.driver_mc,
        }  # type: Dict[str, Any]
        self.shots = 1000
        self.devicesList = {
            'awg': [],
            'dc': [],
            'qa': []
        }  # type: Dict[str, Any]

    def connectDevices(self, *args, **kwargs):
        """ Connect and initialize devices """
        if 'devices' not in kwargs.keys():
            raise ValueError('Parameter `devices` does not exist in connectDevices().')
        if 'connect' not in kwargs.keys():
            raise ValueError('Parameter `connect` does not exist in connectDevices().')
        if 'roLines' not in kwargs.keys():
            raise ValueError('Parameter `roLines` does not exist in connectDevices().')

        self.roLines = kwargs['roLines']
        """
        The readout line dict. Example:
        {"r1":["q01","q02","q03","q04","q05"], "r2": ["q06","q07","q08","q09","q10"], ...}
        """

        self.deviceDict = kwargs['devices']
        """
        The dict for all devices. Example:
        {
            "XY":["mc_1", ...],
            "Z":["z_1", ...],
            "ZDC":["z_1", ...],
            "RO":["out01", "out09", ...],
            "QA":["in01", "in09", ...]
        }
        """

        self.connectDict = kwargs['connect']
        """
        The mapping between device channels and logical channels. Example:
        {
            "QA": {"r1QA": ["in01", "range(20)"], "r2QA": ["in09", "range(20)"], ...},
            "RO": {"r1RO": ["out01", "range(20)"], "r2RO": ["out09", "range(20)"], ...},
            "RO_qubits": {"q01RO": "r1RO", "q02RO": "r1RO", "q03RO": "r1RO", ...},
            "RO_trig": {"r1RO": "AWG5M1", "r2RO": "AWG5M1", ...},
            "XY": {"q03XY": ["mc_1", "out03"], "q04XY": ["mc_1", "out04"], ...},
            "Z": {"q03Z": ["z_1", "out01"], "q04Z": ["z_1", "out02"]}
        }

        """

        # Parse readout channels
        for _line, _qubits in self.roLines.items():
            ro_channels = [i for i in eval(self.connectDict['RO'][f'{_line}RO'][1])]
            if len(ro_channels) != len(_qubits):
                raise RuntimeError(f'Qubit number in {_line} does not equal to '
                                   f'the number of channels ({ro_channels}).')
            for _q, _c in zip(self.roLines[_line], ro_channels):
                self.qubitROChannels[f'{_q}RO'] = _c

        # Connect device
        # 在kw参数中寻找系统初始化相关参数
        qs_sp = self.ParameterQSYNC.copy()
        qs_sp.update(kwargs.get('qs_param', {}))
        mc_sp = self.ParameterMC.copy()
        mc_sp.update(kwargs.get('mc_param', {}))
        z_sp = self.ParameterZ.copy()
        z_sp.update(kwargs.get('z_param', {}))

        self.qsync.open(system_parameter=qs_sp)
        self.driver_mc.open(system_parameter=mc_sp)
        self.driver_z.open(system_parameter=z_sp)
        self.qsync.sync_system()

    def _rline2chnl(self, rline):
        return int(self.connectDict['QA'][f'{rline}QA'][0][-2:])

    def _xy2chnl(self, _key):
        return int(self.connectDict['XY'][_key][1][-2:])

    def _z2chnl(self, _key):
        return int(self.connectDict['Z'][_key][1][-2:])

    def _qubit2rline(self, qubit):
        return self.connectDict['RO_qubits'][f'{qubit}RO'][:2]

    def disconnectDevices(self, *args, **kwargs):
        """ Initialize devices """
        ...

    # def expendBatchChannels(self):

    def stopOutput(self, *args, **kwargs):
        """ Stop the output of waveforms """
        self.qsync.set('ResetTrig')

    def startOutput(self, *args, **kwargs):
        """ Stop the output of waveforms """
        self.qsync.set('GenerateTrig')

    def uploadWaveforms(self, *args, **kwargs):
        """ Upload waveforms """
        if 'waves' not in kwargs.keys():
            raise ValueError('Parameter `waves` does not exist in uploadWaveforms().')
        if 'zpdc' not in kwargs.keys():
            raise ValueError('Parameter `zpdc` does not exist in uploadWaveforms().')

        self.setINDemod(**kwargs)
        self.setRODADelay(**kwargs)
        self.zpdc = kwargs['zpdc']

        waves = kwargs['waves']
        waves_map = {}
        for _key, _wave in waves.items():
            _devChannel = None
            if _key in self.connectDict['XY'].keys():
                _devChannel = self._xy2chnl(_key)
                self.driver_mc.set('Waveform', _wave, _devChannel)
            elif _key in self.connectDict['Z'].keys():
                _devChannel = self._z2chnl(_key)
                self.driver_mc.set('Waveform', _wave, _devChannel)
            elif _key in self.qubitROChannels.keys():
                _devChannel = self._qubit2rline(_key)
                wave_list = waves_map.get(_devChannel, [])
                wave_list.append(_wave)
            if _devChannel is None:
                raise RuntimeError(f'Channel {_key} does not found.')
            print(_key, _devChannel, len(_wave))

        # 合并下发probe da波形
        for _line, wave_list in waves_map.items():
            max_points = max(_w.size() for _w in wave_list)
            wave_array = np.zeros((len(self.roLines[_line]), max_points))
            for idx, _w in enumerate(wave_list):
                wave_array[idx][:_w.size()] = _w
            self.driver_mc.set('Waveform', wave_array.mean(axis=0), self._rline2chnl(_line))

        # import matplotlib.pyplot as plt
        # for _key, _seq in self.waves.items():
        #     plt.plot(_seq, label=_key)
        # plt.legend()
        # plt.show()

    def downloadIQ(self, *args, **kwargs):
        """ Download IQ data """
        self.setIntegrationDelay(**kwargs)
        self.startOutput()
        st_time = time.time()
        roChannels = {}
        print('self.roQubits', self.roQubits)
        for _r in self.roQubits.keys():
            roChannels[_r] = [self.qubitROChannels[f'{_q}RO'] for _q in self.roQubits[_r]]
        print('roChannels', roChannels)
        full = {
            _r: self.driver_mc.get('IQ', channel=self._rline2chnl(_r))
            for _r in self.roQubits.keys()
        }
        print('get iq data timing:', time.time() - st_time)

        iqDict = dict()
        for qubit, iqData in zip(self.roQubits.values(), full.values()):
            for _q in qubit:
                iqDict[_q] = iqData[self.qubitROChannels[f'{_q}RO']]
        return iqDict

    def setINDemod(self, *args, **kwargs):
        """!
        配置MC设备的解模系数
        @param args:
        @param kwargs:
        @return:
        """
        if 'roQubits' not in kwargs.keys():
            raise ValueError('Parameter `roQubits` does not exist in uploadWaveforms().')
        if 'roLength' not in kwargs.keys():
            raise ValueError('Parameter `roLength` does not exist in uploadWaveforms().')
        if 'roFreq' not in kwargs.keys():
            raise ValueError('Parameter `roFreq` does not exist in uploadWaveforms().')
        self.roQubits = kwargs['roQubits']
        self.roLength = {_line: [length / 1e9 for length in lengths] for _line, lengths in kwargs['roLength'].items()}
        self.roFreq = {_line: [freq / 1e9 for freq in freqs] for _line, freqs in kwargs['roFreq'].items()}

        for _line, qubits in self.roQubits.items():
            freqs = {_q: 1e9 for _q in self.roLines[_line]}
            lengths = {_q: 512e-9 for _q in self.roLines[_line]}
            for _q, _freq, _len in zip(qubits, self.roFreq[_line], self.roLength[_line]):
                freqs[_q] = _freq
                lengths[_q] = _len
            print(f'The configured demodulation frequency point is ({freqs})')
            self.driver_mc.set('TimeWidth', list(lengths.values()), self._rline2chnl(_line))
            self.driver_mc.set('FreqList', max(freqs.values()), self._rline2chnl(_line))

    def setRODADelay(self, *args, **kwargs):
        """!
        配置probe da相对触发的延迟
        配置粒度为16ns的整倍数
        @param args:
        @param kwargs:
        @return:
        """
        if 'roDADelay' in kwargs.keys():
            for _line, delay in kwargs['roDADelay'].items():
                self.roDADelay[_line] = delay/1e9
                self.driver_mc.set('OUTDelay', self.roDADelay[_line], self._rline2chnl(_line))
        else:
            raise ValueError('Parameter `roDADelay` does not exist in uploadWaveforms().')

    def setShots(self, *args, **kwargs):
        """ Set shots """
        if 'shots' not in kwargs.keys():
            raise ValueError('Parameter `shots` does not exist in setShots().')
        shots = kwargs['shots']
        self.shots = shots
        self.qsync.set('Shot', shots)
        self.driver_mc.set('Shot', shots)
        print("set shots:", shots)

    def setHoldoffTime(self, *args, **kwargs):
        """ Set hold-off time """
        if 'interval' not in kwargs.keys():
            raise ValueError('Parameter `interval` does not exist in setHoldoffTime().')
        interval = kwargs['interval']
        self.qsync.set('TrigPeriod', interval / 1e9)  # 单位：s

    def setLO(self, *args, **kwargs):
        """ Set LO """
        ...

    def setIntegrationDelay(self, *args, **kwargs):
        """ Set readout integration delay. """
        if 'integrationDelay' in kwargs.keys():
            for _channel, delay in kwargs['integrationDelay'].items():
                self.integrationDelay[_channel] = delay
                self.driver_mc.set('INDelay', delay / 1e9, self._rline2chnl(_channel))
        else:
            raise ValueError('Parameter `integrationDelay` does not exist in setIntegrationDelay().')

    def setInputRange(self, *args, **kwargs):
        """ Set input range for output channels """
        if 'inputRange' in kwargs.keys():
            for _channel, _value in kwargs['inputRange'].items():
                devChannel = self.connectDict['QA'][_channel][1]
                self.inputRange[devChannel] = _value
        else:
            raise ValueError('Parameter `inputRange` does not exist in setInputRange().')

    def setOutputRange(self, *args, **kwargs):
        """ Set output range for output channels """
        if 'outputRange' in kwargs.keys():
            for _channel, delay in kwargs['outputRange'].items():
                self.outputRange[_channel] = delay
        else:
            raise ValueError('Parameter `outputRange` does not exist in setOutputRange().')
