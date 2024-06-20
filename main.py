from ast import Num
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

radiodata1 = pd.read_fwf('/workspaces/Velocities_Of_Stars_In_The_Milky_Way/data/ad3a-16500.txt', header=0)
radiodata2 = pd.read_fwf('/workspaces/Velocities_Of_Stars_In_The_Milky_Way/data/ad3a-16952.txt', header=0)
radiodata3 = pd.read_fwf('/workspaces/Velocities_Of_Stars_In_The_Milky_Way/data/ad3a-17123.txt', header=0)
radiodata4 = pd.read_fwf('/workspaces/Velocities_Of_Stars_In_The_Milky_Way/data/ad3a-17332.txt', header=0)
radiodata5 = pd.read_fwf('/workspaces/Velocities_Of_Stars_In_The_Milky_Way/data/ad3a-18081.txt', header=0)

radiodatas = [radiodata1, radiodata2, radiodata3, radiodata4, radiodata5]
expected_frequencies = np.array([42.373341, 42.519375, 42.583827, 42.820570, 42.879941, 43.122090, 43.423853])


def flux_avg(data, num):  
  top_5_percent = np.percentile(data['Flux (Jy)'], 95)
  bottom_5_percent = np.percentile(data['Flux (Jy)'], 5)
  wo5percent = data[(data['Flux (Jy)'] > bottom_5_percent) & (data['Flux (Jy)'] < top_5_percent)]

  mean = np.mean(wo5percent['Flux (Jy)'])
  std = np.std(wo5percent['Flux (Jy)'])
  d = mean + 5 * std
  spectral_lines = (data[data['Flux (Jy)'] > d]).sort_values('Frequency (GHz)')
  
  velocities = []
  for frequency, flux in zip(spectral_lines['Frequency (GHz)'], spectral_lines['Flux (Jy)']):
    differences = np.abs(expected_frequencies - frequency)
    closest_index = np.argmin(differences)
    closest_expected_frequency = expected_frequencies[closest_index]
    expected_frequency = closest_expected_frequency
    c = 6.706e8
    velocity = (1 - (expected_frequency/frequency)) * c
    velocities.append(velocity)
    
  print(f"Based on the spectral lines, the possible velocities are {velocities}")
  average_velocity = np.mean(velocities)
  print(f"The final velocity of star {num} is {average_velocity} km/s.")

  if average_velocity > 0:
    print(f"Star {num} is moving away from you.")
  else:
    print(f"Star {num} is moving towards you.")
  error = std/np.sqrt(len(velocities))
  print(f"The error in the average velocity is {error} km/s.")
  
  print('----------------')

numbers = [1,2,3,4,5]
for radiodata, num in zip(radiodatas, numbers):
  print(f"The file is file #{num}, and star #{num}")
  flux_avg(radiodata, num)