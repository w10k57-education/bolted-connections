import numpy as np
import pandas as pd

class bolt():
    """A class representing a bolt and its properties.
    
    This class calculates various properties of a bolt based on its thread designation,
    strength class, and preload. It provides methods to calculate axial load, bolt strength,
    torque, and retrieve bolt data summary.
    
    Parameters:
    ----------
    thread : str
        The thread designation of the bolt.
    klasa : str
        The strength class of the bolt in the format 'x.y', where x and y are integers.
    preload : float, optional
        The preload value applied to the bolt, by default 0.6.
    
    Attributes:
    ----------
    Re : int
        The yield strength of the bolt.
    Rm : int
        The ultimate tensile strength of the bolt.
    P : float
        The pitch of the bolt thread.
    d : float
        The nominal diameter of the bolt.
    d2 : float
        The diameter at the root of the bolt thread.
    d1 : float
        The diameter at the crest of the bolt thread.
    d3 : float
        The mean diameter of the bolt thread.
    A : float
        The tensile stress area of the bolt.
    Fi : float
        The axial load on the bolt.
    preload : float
        The preload value applied to the bolt.
    dim : pandas.Series
        A series containing summary data of the bolt.
    
    Methods:
    -------
    axial_load(load):
        Calculate the axial load on the bolt.
    bolt_strength(klasa):
        Calculate the bolt's yield strength (Re) and ultimate tensile strength (Rm).
    data_extract(designation):
        Extract bolt data from the 'sruby.csv' file based on designation.
    torque(dm, mi):
        Calculate the torque applied to the bolt.
    data_summary(designation):
        Get summary data of the bolt from the 'sruby.csv' file.
    """
    def __init__(self, thread, klasa, preload=0.6):
        self.Re, self.Rm = self.bolt_strength(klasa)
        self.P, self.d, self.d2, self.d1, self.d3, self.A = self.data_extract(thread) 
        self.Fi = self.axial_load(preload)
        self.preload = preload
        self.dim = self.data_summary(thread)
        
    def axial_load(self, load):
        """Calculate the axial load on the bolt.
        
        Parameters:
        ----------
        load : float
            The external load applied to the bolt.
        
        Returns:
        -------
        float
            The calculated axial load on the bolt.
        """
        return round(( load * self.Re * self.A ) / 1000, 2)
    
    def bolt_strength(self, klasa):
        """Calculate the bolt's yield strength and ultimate tensile strength.
        
        Parameters:
        ----------
        klasa : str
            The strength class of the bolt in the format 'x.y'.
        
        Returns:
        -------
        int
            The calculated yield strength (Re) of the bolt.
        int
            The calculated ultimate tensile strength (Rm) of the bolt.
        """
        first_sign = int(klasa.split('.')[0])
        second_sign = int(klasa.split('.')[1])
        Re = first_sign * second_sign * 10
        Rm = second_sign * 100
        return Re, Rm
    
    def data_extract(self, designation):
        """Extract bolt data from the 'sruby.csv' file based on designation.
        
        Parameters:
        ----------
        designation : str
            The thread designation of the bolt.
        
        Returns:
        -------
        float
            The pitch of the bolt thread.
        float
            The nominal diameter of the bolt.
        float
            The diameter at the root of the bolt thread.
        float
            The diameter at the crest of the bolt thread.
        float
            The mean diameter of the bolt thread.
        float
            The tensile stress area of the bolt.
        """
        sruby = pd.read_csv('data/sruby.csv', index_col='OZNACZENIE')
        P = sruby.loc[designation][0]
        d = sruby.loc[designation][1]
        d2 = sruby.loc[designation][2]
        d1 = sruby.loc[designation][3]
        d3 = sruby.loc[designation][4]
        A = sruby.loc[designation][5]
        return P, d, d2, d1, d3, A
    
    def torque(self, dm, mi=0.15):
        """Calculate the torque applied to the bolt.
        
        Parameters:
        ----------
        dm : float
            Mean diameter of the bolt thread.
        mi : float, optional
            Coefficient of friction, by default 0.15.
        
        Returns:
        -------
        float
            The calculated torque applied to the bolt.
        """
        incl_angle = self.P / (np.pi * self.d2)
        friction_angle = np.arctan(mi)
        return round(self.Fi / 2 * (self.d2 * np.tan(incl_angle + friction_angle) + dm * mi), 2) 
    
    def data_summary(self, designation):
        """Get summary data of the bolt from the 'sruby.csv' file.
        
        Parameters:
        ----------
        designation : str
            The thread designation of the bolt.
        
        Returns:
        -------
        pandas.Series
            A series containing summary data of the bolt.
        """
        sruby = pd.read_csv('data/sruby.csv', index_col='OZNACZENIE')
        return sruby.loc[designation]