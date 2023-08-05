import numpy as np
from . import misc

"""
According to ISO 527-1: https://cdn.standards.iteh.ai/samples/75824/61c480ef4bf0494aa6966bd4c2244c2e/ISO-527-1-2019.pdf
"""
class tensile_modulus:
    def __init__(self,
                 stress,
                 strain,
                 percent_strain=False,
                 lower_limit=0.05,
                 upper_limit=0.25
                 ):
        """
        Tensile, or Young's modulus is the slope of strain/stress curve, between strains equals to 0.05 and 0.25 percent
        """
        stress=np.array(stress)
        strain=np.array(strain)
        if not percent_strain:
            strain=strain*100
        module_strain=strain[(strain>lower_limit) & (strain<upper_limit)]
        low_idx = np.where(strain==min(module_strain))[0][0]
        upp_idx = np.where(strain==max(module_strain))[0][0]
        module_stress = stress[low_idx:upp_idx+1]
        if not percent_strain:
            module_strain=module_strain/100
        array = np.vstack([module_strain, np.ones(len(module_strain))]).T
        E, c = np.linalg.lstsq(array, module_stress, rcond=-1)[0]
        r2 = 1 - c / (module_stress.size * module_stress.var())
        self.r2 = round(r2,4)
        self.tensile_modulus=misc.round_sig(E, sig=3)
        self.module_strain, self.module_stress =module_strain, module_stress


class at_break:
    def __init__(self, stress, strain):
        self.stress=misc.round_sig(stress[len(stress)-1], sig=3)
        self.strain=misc.round_sig(strain[len(strain)-1])
        
class strenght:
    def __init__(self, stress, strain):
        self.value=misc.round_sig(self.find_local_maximum(stress), sig=3)
        self.strain=misc.round_sig(strain[self.idx])
    def find_local_maximum(self, stress):
        for i in range(1, len(stress)-1):
            if stress[i-1] < stress[i] > stress[i+1] and stress[i]>1:
                self.idx=i
                return  stress[i]

        print("Local maximum not found, gives max value")
        self.idx=np.where(stress==np.max(stress))[0][0]
        val = np.max(stress)
        return val
                

class yield_strenght:
    def __init__(self,stress, strain):
        self.value=misc.round_sig(stress[self.find_idx(stress,strain)], sig=3)
        self.strain=misc.round_sig(strain[self.find_idx(stress,strain)])
    def find_idx(self, stress,strain):
        for i in range(1, len(strain)):
            if strain[i] > strain[i-1] and stress[i] <= stress[i-1]:
                if stress[i]>1:
                    return i
                else:
                    continue
                    # exit()
        return len(strain)-1

        

