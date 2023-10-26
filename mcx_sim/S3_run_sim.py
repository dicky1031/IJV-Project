from mcx_ultrasound_opsbased import MCX
import calculateR_CV
import json
import os
import numpy as np
import pandas as pd
from glob import glob
from time import sleep
from tqdm import tqdm
import time
import sys

# %% run
class Timer():
    def __init__(self):
        self.o = time.time()

    def measure(self, p=1):
        x = (time.time() - self.o) / p
        x = int(x)
        if x >= 3600:
            return '{:.1f}h'.format(x / 3600)
        if x >= 60:
            return '{}m'.format(round(x / 60))
        return '{}s'.format(x)

def run_mcx(result_mother_folder, subject, mus_start, mus_end, NA_enable, NA, runningNum, cvThreshold, repeatTimes, ijv_type):
    """_summary_

    Args:
        result_mother_folder (_type_): _description_
        subject (_type_): _description_
        mus_start (_type_): _description_
        mus_end (_type_): _description_
        NA_enable (_type_): _description_
        NA (_type_): _description_
        runningNum (_type_): _description_
        cvThreshold (_type_): _description_
        repeatTimes (_type_): _description_
        ijv_type (_type_): _description_
    """
    timer = Timer()
    ID = f'{subject}_ijv_{ijv_type}'
    for run_idx in tqdm(range(mus_start, mus_end+1)):
        now = time.time()
        
        # Setting
        session = f"run_{run_idx}"
        sessionID = os.path.join("dataset", result_mother_folder, ID, session)
        
        # Do simulation
        # initialize
        simulator = MCX(sessionID)
        
        # load config 
        with open(os.path.join(sessionID, "config.json")) as f:
            config = json.load(f)
        simulationResultPath = os.path.join(config["OutputPath"], session, "post_analysis", f"{session}_simulation_result.json")
        with open(simulationResultPath) as f:
            simulationResult = json.load(f)
        existedOutputNum = simulationResult["AnalyzedSampleNum"]
        
        # run forward mcx
        if runningNum:
            for idx in range(existedOutputNum, existedOutputNum+runningNum):
                # run
                simulator.run(idx)
                if NA_enable:
                    simulator.NA_adjust(NA)
            mean, CV = calculateR_CV.calculate_R_CV(sessionID, session, "mua_test.json")
            print(f" Session name: {sessionID} \n Reflectance mean: {mean} \nCV: {CV} ", end="\n\n")

        else:
            # run stage1 : run N sims to precalculate CV
            for idx in range(existedOutputNum, existedOutputNum+repeatTimes):
                # run
                simulator.run(idx)
                if NA_enable:
                    simulator.NA_adjust(NA)
            # calculate reflectance
            mean, CV = calculateR_CV.calculate_R_CV(sessionID, session, "mua_test.json")
            print(f"Session name: {sessionID} \n" \
                  f"Reflectance mean: {mean} \n" \
                  f"CV: {CV} \n" \
                  f"Predict CV: {CV/np.sqrt(repeatTimes+existedOutputNum)}" , end="\n\n")
            # run stage2 : run more sim to make up cvThreshold
            predict_CV = max(CV)/np.sqrt(repeatTimes+existedOutputNum)
            old_needAddOutputNum = 0
            while (predict_CV > cvThreshold):
                needAddOutputNum = int(np.ceil((max(CV)**2)/(cvThreshold**2)) - (repeatTimes+existedOutputNum))
                if needAddOutputNum > 0:
                    for idx in range(repeatTimes+existedOutputNum+old_needAddOutputNum, repeatTimes+existedOutputNum+old_needAddOutputNum+needAddOutputNum):
                        # run
                        simulator.run(idx)
                        if NA_enable:
                            simulator.NA_adjust(NA)
                    # calculate reflectance
                    mean, CV = calculateR_CV.calculate_R_CV(sessionID, session, "mua_test.json")
                    print(f"Session name: {sessionID} \n" \
                        f"Reflectance mean: {mean} \n" \
                        f"CV: {CV} \n" \
                        f"Predict CV: {CV/np.sqrt(repeatTimes+existedOutputNum+needAddOutputNum)}", end="\n\n")
                    
                    predict_CV = max(CV)/np.sqrt(repeatTimes+existedOutputNum+needAddOutputNum)
                    old_needAddOutputNum += needAddOutputNum
                else:
                    break
                    
            with open(simulationResultPath) as f:
                simulationResult = json.load(f)
            simulationResult['elapsed time'] = time.time() - now
            with open(simulationResultPath, "w") as f:
                json.dump(simulationResult, f, indent=4)

        print('ETA:{}/{}'.format(timer.measure(),
                                 timer.measure(run_idx / mus_end)))
        sleep(0.01)


if __name__ == "__main__":
    # ====================== Modify your setting here ======================
    result_mother_folder = "Julie_low_scatter_train"
    subject = "Julie"
    ijv_type_set = ['large', 'small']
    mus_start = 1
    mus_end = 225
    NA_enable = 1  # 0 not consider NA, 1 consider NA
    NA = 0.22
    runningNum = 0  # (Integer or False) 
    cvThreshold = 3
    repeatTimes = 10 # repeat n times to calculate CV
    # ======================================================================

    for ijv_type in ijv_type_set:
        run_mcx(result_mother_folder = result_mother_folder, 
                subject = subject, 
                mus_start = mus_start, 
                mus_end = mus_end, 
                NA_enable = NA_enable,
                NA = NA, 
                runningNum = runningNum, 
                cvThreshold = cvThreshold, 
                repeatTimes = repeatTimes, 
                ijv_type = ijv_type)
