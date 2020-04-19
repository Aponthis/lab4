import pandas as pd
import os
import matplotlib.pyplot as plt
import math
import numpy as np

import math
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))

w = 2 * 0.0254
t = 1/8 * 0.0254
Area = w * t # Calculates cross-sectional area of plate in m^2

class Data:  # Holds the data for each hole diameter
    def __init__(self, diameter, load):
        self.StrDiameter = diameter

        d = float(diameter[:1] + '.' + diameter[1:]) * 0.0254  # Gets diameter as a decimal (in m)
        self.Diameter = d

        dfNF = pd.read_csv(dir_path + '\\' + diameter + r'nearfield.csv')
        dfFF = pd.read_csv(dir_path + '\\' + diameter + r'farfield.csv')

        self.NFLength = np.array(dfNF['Length [mm]'] / 1000)  # Near field length vector in meters
        self.NFStrain =np.array( dfNF['Section 1.epsX [%]'] / 100)  # Near field strain vector

        self.FFLength = np.array(dfFF['Length [mm]'] / 1000)  # Near field length vector in meters
        self.FFStrain = np.array(dfFF['Section 2.epsX [%]'] / 100)  # Near field strain vector

        FFStress = load/Area  # Calculates theoretical far-field stress
        AvgStrain = np.average(self.FFStrain)  # Calculates average far-field strain
        self.E = FFStress/AvgStrain / 10**9 # Young's Modulus in GPa

        self.NFStress = self.E * self.NFStrain * 10**3

        a = d/2

        end = np.max(self.NFLength)
        midpoint = end / 2

        self.Position = np.linspace(0, midpoint - a, 50)
        self.Position = np.append(self.Position, np.linspace(midpoint + a, end, 50))

        y = []

        for x in self.Position:
            if x > midpoint:
                y.append(x - midpoint)
            else:
                y.append(x - midpoint)

        y = np.array(y)

        self.TheorNFStress = (FFStress/2 * (1 + a**2/y**2) + \
                             FFStress/2 * (1+3*a**4/y**4)) / 10 **6 #  In MPa

        self.TheorKt = 3 - 3.13*(d/w) + 3.66 * (d/w)**2 - 1.53 * (d/w)**3

        AreaNom = (w-d)*t
        SigmaNom = load/AreaNom

        self.TheorSigmaMax = self.TheorKt*SigmaNom / 10**6

        self.SigmaMax = np.max(self.NFStress)
        self.Kt = (self.SigmaMax * 10**6)/SigmaNom

Diameter = ['00625', '0125', '0250', '0500', '0750', '1000']
Loads = [4000, 4000, 4000, 3500, 2900, 2300]  # Loads corresponding to each plate in N

DataSet = []

for x in range(len(Diameter)):  # Fills out a data class for each geometry and adds it to a list
    exec('d' + Diameter[x] + '=Data(Diameter[' + str(x) + '], Loads[' + str(x) + '])')
    exec('DataSet.append(d' + Diameter[x] + ')')

EArray = []

for i in range(len(DataSet)):
    EArray.append(DataSet[i].E)

# a
print("Young's Modulus: ", Diameter, EArray)

# b
for i in DataSet:  # For each stress geometry
    plt.figure()

    ExpStress = plt.scatter(i.NFLength, i.NFStress)
    TheorStress = plt.scatter(i.Position, i.TheorNFStress)

    plt.grid(b=True, which='major', color='#666666', linestyle='-')

    plt.legend((ExpStress, TheorStress), ('Experimental Stress', 'Theoretical Stress'))

    plt.title('Stress vs. Position Along Cross-Section ' + str(round(i.Diameter/0.0254*10000)/10000) + ' in.')
    plt.ylabel('Engineering Stess (MPa)')
    plt.xlabel('Position (m)')

# c

KtTheorArray = []

for i in range(len(DataSet)):
    KtTheorArray.append(DataSet[i].TheorKt)

print("Theoretical Kt: ", Diameter, KtTheorArray)

# d

TheorSigmaMaxArray = []
SigmaMaxArray = []

for i in range(len(DataSet)):
    TheorSigmaMaxArray.append(DataSet[i].TheorSigmaMax)
    SigmaMaxArray.append(DataSet[i].SigmaMax)

print("Theoretical & Actual SigmaMax (MPa): ", Diameter, TheorSigmaMaxArray, SigmaMaxArray)

# e

KtArray = []

for i in range(len(DataSet)):
    KtArray.append(DataSet[i].Kt)

print("Kt: ", Diameter, KtArray)

plt.show()
