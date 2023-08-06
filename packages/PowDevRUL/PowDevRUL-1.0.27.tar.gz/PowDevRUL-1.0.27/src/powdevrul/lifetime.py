import pandas as pd
# Importing required modules from the local directories
from src.powdevrul.function.counters import count
from src.powdevrul.function.cumul_endommagement import calculate_damage_cumulation
from src.powdevrul.function.losses import Losses
from src.powdevrul.function.temperature import calculate_temperature
from src.powdevrul.function.graphs import graph
from src.powdevrul.function.path_reader import import_variables

def rul_calculation(variables_file_path):
  """
  This function executes a sequence of calculations related to thermal 
  and electrical properties of some materials, based on data from an Excel file.
  """
  # Choice of dictionary for the analysis. This could be modified in the future for flexibility.
  dic = import_variables(variables_file_path).variables
  
  # Load the Excel file defined in 'variables'
  xls = pd.ExcelFile(dic["excel_file_path"])
  
  # Read a specific sheet from the Excel file (also defined in 'variables')
  file = xls.parse(dic["excel_page"])

  
  # Instantiate a Losses object and calculate losses
  losses = Losses(dic, file)
  losses.calculate_losses()
  
  # Calculate the temperature based on the losses and thermal resistances
  Temp_IGBT, Temp_diode, Temp_case = calculate_temperature( losses, dic, file)

  # Calculate the counters and lifetimes for both IGBT and Diode
  counter_IGBT, counter_Nf_IGBT = count(Temp_IGBT, dic)
  counter_diode, counter_Nf_diode = count(Temp_diode, dic)

  # Display Torque, Speed, Current, Loss through a graph
  # Uncomment this line if you want to show the graphs
  # graph(file,dic,losses,Temp_IGBT,Temp_diode,Temp_case, counter_IGBT, counter_diode)
  
  # Calculate the cumulative damage law
  lifetime_IGBT, lifetime_diode, e_kwh_byhours, efficiency = calculate_damage_cumulation(counter_IGBT, counter_Nf_IGBT, counter_diode, counter_Nf_diode, losses, dic, file)

  results=[["IGBT Cycles",lifetime_IGBT],["Diode Cycles",lifetime_diode],["Efficiency",efficiency],["e_kwh_byhours",e_kwh_byhours]]
  
  # Return the calculated lifetimes and other datas
  return (results[0:3]) #add  e_kwh_byhours if you want

def rul_graphs(variables_file_path):
  """
  This function executes a sequence of calculations related to thermal 
  and electrical properties of some materials, based on data from an Excel file.
  """
  # Choice of dictionary for the analysis. This could be modified in the future for flexibility.
  dic = import_variables(variables_file_path).variables
  
  # Load the Excel file defined in 'variables'
  xls = pd.ExcelFile(dic["excel_file_path"])
  
  # Read a specific sheet from the Excel file (also defined in 'variables')
  file = xls.parse(dic["excel_page"])

  
  # Instantiate a Losses object and calculate losses
  losses = Losses(dic, file)
  losses.calculate_losses()
  
  # Calculate the temperature based on the losses and thermal resistances
  Temp_IGBT, Temp_diode, Temp_case = calculate_temperature( losses, dic, file)

  # Calculate the counters and lifetimes for both IGBT and Diode
  counter_IGBT, counter_Nf_IGBT = count(Temp_IGBT, dic)
  counter_diode, counter_Nf_diode = count(Temp_diode, dic)

  # Display graphs
  graph(file,dic,losses,Temp_IGBT,Temp_diode,Temp_case, counter_IGBT, counter_diode)