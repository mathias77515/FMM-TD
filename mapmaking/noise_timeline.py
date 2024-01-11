import qubic
import mapmaking.frequency_acquisition as frequency_acquisition
import numpy as np

class QubicNoiseTD:
    
    def __init__(self, npointings, comm=None, size=1, detector_nep=4.7e-17):
        
        dictfilename = 'dicts/pipeline_demo.dict'
        d = qubic.qubicdict.qubicDict()
        d.read_from_file(dictfilename)
        
        d['TemperatureAtmosphere150']=None
        d['TemperatureAtmosphere220']=None
        d['EmissivityAtmosphere150']=None
        d['EmissivityAtmosphere220']=None
        d['detector_nep'] = detector_nep
        self.npointings = npointings
        d['npointings'] = npointings
        d['comm'] = comm
        d['nprocs_instrument'] = size
        d['nprocs_sampling'] = 1
        d['config'] = 'TD'
        
        self.dict = d.copy()
        self.dict['filter_nu'] = int(150)
        self.dict['nf_sub'] = 1
        self.dict['nf_recon'] = 1
        self.dict['type_instrument']=''
        self.acq = frequency_acquisition.QubicIntegrated(self.dict, Nsub=1, Nrec=1)
        
    def get_noise(self, det_noise, pho_noise):
        n = self.detector_noise() * 0
        
        if det_noise:
            n += self.detector_noise()
        if pho_noise:
            n += self.photon_noise()
        return n
    
    def photon_noise(self):
        return self.acq.get_noise(det_noise=False, photon_noise=True)
    
    def detector_noise(self):
        return self.acq.get_noise(det_noise=True, photon_noise=False)
    
    def total_noise(self, wdet, wpho):
        ndet = wdet * self.detector_noise()
        npho = wpho * self.photon_noise()
        return ndet + npho