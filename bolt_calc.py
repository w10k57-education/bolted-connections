import numpy as np
import pandas as pd

class bolt():
    def __init__(self, thread, klasa, preload=0.6):
        self.Re, self.Rm = self.bolt_strength(klasa)
        self.P, self.d, self.d2, self.d1, self.d3, self.A = self.data_extract(thread) 
        self.Fi = self.axial_load(preload)
        self.preload = preload
        self.dim = self.data_summary(thread)
        
    def axial_load(self, load):
        return round(( load * self.Re * self.A ) / 1000, 2)
    
    def bolt_strength(self, klasa):
        first_sign = int(klasa.split('.')[0])
        second_sign = int(klasa.split('.')[1])
        Re = first_sign * second_sign * 10
        Rm = second_sign * 100
        return Re, Rm
    
    def data_extract(self, designation):
        sruby = pd.read_csv('data/sruby.csv', index_col='OZNACZENIE')
        P = sruby.loc[designation][0]
        d = sruby.loc[designation][1]
        d2 = sruby.loc[designation][2]
        d1 = sruby.loc[designation][3]
        d3 = sruby.loc[designation][4]
        A = sruby.loc[designation][5]
        return P, d, d2, d1, d3, A
    
    def torque(self, dm, mi=0.15):
        incl_angle = self.P / (np.pi * self.d2)
        friction_angle = np.arctan(mi)
        return round(self.Fi / 2 * (self.d2 * np.tan(incl_angle + friction_angle) + dm * mi), 2) 
    
    def data_summary(self, designation):
        sruby = pd.read_csv('data/sruby.csv', index_col='OZNACZENIE')
        return sruby.loc[designation]