import math
import numpy
import random as rnd
import pandas as pd



#ExelWriter erstellen
writer = pd.ExcelWriter('Data/1_final_Trajektorien_Daten.xlsx', engine='xlsxwriter')


#Dataframe erstellen
trajectory_df = pd.DataFrame(columns=['Pos1','Pos2','Pos3','Pos4','Pos5','Pos6'])

#Punkte pro Trajektorie
length=1100

#Laufvariable
j = 0

#Anzahl Punkte die Konstant gehalten werden, bis Trajektorie Beginnt
vorlauf=100

#Anzahl der Trajektorien
number_of_trajectories = 1000

#Bereich definieren
Pos_1_min=-math.pi/2
Pos_1_max=math.pi/2
Pos_2_min=0
Pos_2_max=math.pi
Pos_3_min=0
Pos_3_max=math.pi
Pos_4_min=-math.pi/2
Pos_4_max=math.pi/2
Pos_5_min=-math.pi/2
Pos_5_max=math.pi/2
Pos_6_min=-math.pi/2
Pos_6_max=math.pi/2

while j < number_of_trajectories:

    for i in range (1,7):

        a = rnd.uniform(-0.5,0.5)
        b = rnd.uniform(0.5,3)
        c = math.pi/2
        d = 0

        if i==2:
            a = rnd.uniform(-0.2, 0.2)
            b = rnd.uniform(0.5, 3)
            d = 0.2

        if i==3:
            a = rnd.uniform(-0.5, 0.5)
            b = rnd.uniform(0.5, 3)
            d = 0.5



        for k in range (-vorlauf, length):
            x= 5 * k / length
            Position= a*math.sin(b*x+c)+d
            if k<1:
                Position=a+d
            trajectory_df.loc[k+vorlauf,'Pos'+str(i)] = Position






    print("Erfolg " + str(j+1))
    j = j + 1
    # Ablegen in Exel
    trajectory_df.to_excel(writer, sheet_name='Sheet' + str(j))



writer.save()

