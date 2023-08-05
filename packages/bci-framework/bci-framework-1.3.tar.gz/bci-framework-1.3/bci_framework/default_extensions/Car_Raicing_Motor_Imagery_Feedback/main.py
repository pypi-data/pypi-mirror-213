from bci_framework.extensions.data_analysis import DataAnalysis, loop_consumer, fake_loop_consumer
import logging

import os
import gym
import numpy as np

# from predictor import predict
from predict_eegnet import Predict_EEGNet
from predict_csp import Predict_CSP

BUFFER = 4.5  # Segundos de analisis de la señal
SLIDING_DATA = 100  # Cantidad de datos que se actualizaran en cada clasificación
GAS = 0.01
BREAK_SYSTEM = 0


########################################################################
class Analysis(DataAnalysis):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(*args, **kwargs)
        
        model_path_csp = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models', 'Modelo_UNAL_S01_2class_f1.pkl')
        model_path_eegnet = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'models', 'model_eegnet.h5')
        
        self.model_eegnet = Predict_EEGNet(model_path_eegnet)
        self.model_csp= Predict_CSP(model_path_csp)
        
        self.steering_wheel = 0
        
        # Car raicing
        self.env = gym.make('CarRacing-v0')
        self.env.reset()

        # Buffer
        self.create_buffer(BUFFER, fill=0)
        self.stream()
        
        
    # ----------------------------------------------------------------------
    @loop_consumer('eeg')
    def stream(self):
        """"""
        
        # action = self.model_eegnet.predict(self.buffer_eeg.reshape(1, 16, -1, 1))
        action = self.model_csp.predict(self.buffer_eeg.reshape(1, 16, -1))
        
        match action:
            
            case 1:
                self.steering_wheel += 0.1
                
            case 0:
                self.steering_wheel -= 0.1
        
        # Move Car
        logging.warning(f'Action: {action}')
    
        self.env.render()
        self.env.step([self.steering_wheel, GAS, BREAK_SYSTEM])
        
        
if __name__ == '__main__':
    Analysis()
