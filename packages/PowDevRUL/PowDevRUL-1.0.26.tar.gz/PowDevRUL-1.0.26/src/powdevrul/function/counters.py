# Import necessary modules
from rainflow import extract_cycles
import numpy as np

def count(Temp, dic):
    """
    This function calculates the cycles and counter_Nf based on the given temperature (Temp) and dictionary (dic) of constants.

    Parameters:
    Temp (numpy array): Array of temperature values
    dic (dict): Dictionary of constants required for calculations

    Returns:
    counter (numpy array): Calculated cycles for the given Temp
    counter_Nf (numpy array): Calculated counter_Nf values for the given Temp
    """

    # Constants from the dictionary
    a = dic["A"]
    alpha = dic["alpha"]
    ea = dic["Ea"]
    k = dic["k"]

    # Calculate the cycles for given Temp using the rainflow algorithm
    counter = np.array(list(extract_cycles(Temp)))
    counter = np.transpose(counter)

    # Calculate counter_Nf based on the calculated cycles and dictionary values
    counter_Nf = counter.copy()
    counter_Nf[2, :] = a * counter_Nf[0, :] ** alpha * np.exp(ea / (k * counter_Nf[1, :]))

    return(counter, counter_Nf)
