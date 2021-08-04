import math
import numpy
import random as rnd
import pandas as pd



#ExelWriter erstellen
writer = pd.ExcelWriter('Data/2_final_Trajektorien_Daten.xlsx', engine='xlsxwriter')


#Dataframe erstellen
trajectory_df = pd.DataFrame(columns=['x','y','z','gamma','teta'])


#Laufvariable
j = 0

#Anzahl der Trajektorien
number_of_trajectories = 5

#Bereich definieren
x_min = 1.1
x_max = 1.5
y_min = -0.3
y_max = 0.3
z_min = 0.6
z_max = 1.0

# Höchste Abbruchszahl
kill_value = 50

# Maximale Zahl der Berechnungen pro Trajektorie
overflow = 10000

#Anzahl der Punkte je Trajektorie
trajectory_length = 1000

# Anzahl der Korrekturschritte
fallback = 20
fallback_addition = 1

#maximaler Änderungswinkel in Grad
delta_angle = 7

while j < number_of_trajectories:

    # Startpositionen zufällig wählen
    x_0 = rnd.uniform(x_min, x_max)
    y_0 = rnd.uniform(y_min, y_max)
    z_0 = rnd.uniform(z_min, z_max)

    #Startwinkel zufällig wählen
    gamma_0 = rnd.uniform(0, 2*math.pi) #Winkel um die y-Achse
    teta_0 = rnd.uniform(0, math.pi) #Winkel um die z-Achse

    # Abspeichern des Startpunkts und Startwinkel
    trajectory_df.loc[(0), ('x')] = x_0
    trajectory_df.loc[[0], ['y']] = y_0
    trajectory_df.loc[[0], ['z']] = z_0
    trajectory_df.loc[[0], ['gamma']] = gamma_0
    trajectory_df.loc[[0], ['teta']] = teta_0

    #definiere Standardlänge und Abweichungen
    standard_length = 0.002 #beschreibt die mittlere Länge zwischen zwei Punkten
    correction_low = 0.5 #minimaler Faktor für Länge
    correction_high = 1.5 #maximaler Faktor für Länge



    #definieren der maximalen Winkelabweichungen zwischen zwei Schritten
    delta_gamma = math.pi/180*delta_angle  #letzte Zahl gibt maximale Winkeländerung in ° an
    delta_teta = math.pi/180*delta_angle #letzte Zahl gibt maximale Winkeländerung in ° an


    #ersten Punkt und Winkel mitgeben
    x = x_0
    y = y_0
    z = z_0
    gamma = gamma_0
    teta = teta_0

    #Abbruchvariablen definieren
    fail_counter = 0
    approval_counter = 0
    final_fail_counter = 0

    k = 0
    i = 0

    #While Schleife da das besser mit i funktioniert
    while i < trajectory_length:

        # Länge bestimmen
        length = rnd.uniform(correction_low, correction_high) * standard_length

        # Winkel bestimmen
        gamma = gamma + rnd.uniform(-delta_gamma, delta_gamma)
        teta = teta + rnd.uniform(-delta_teta, delta_teta)

        # x,y,z bestimmen
        z = z + math.sin(gamma) * length  # erst Drehung um y-Achse
        y = y + math.cos(gamma) * length * math.sin(teta)  # erst Drehung um y-Achse, dann um z-Achse
        x = x + math.cos(gamma) * length * math.cos(teta)  # erst Drehung um y-Achse, dann um z-Achse

        # Abspeichern der Punkte
        trajectory_df.loc[(i), ('x')] = x
        trajectory_df.loc[(i), ('y')] = y
        trajectory_df.loc[(i), ('z')] = z
        trajectory_df.loc[(i), ('gamma')] = gamma
        trajectory_df.loc[(i), ('teta')] = teta

        # Prüfen ob der neue Punkt in unserem Bereich liegt
        if x > x_min and x < x_max and y > y_min and y < y_max and z > z_min and z < z_max:

            #Abbruch Variablen
            fail_counter = 0
            approval_counter = approval_counter + 1
            if approval_counter > fallback + fallback_addition:
                final_fail_counter = 0

        #Wenn neuer Punkt nicht in gültigem Bereich liegt
        else:
            #Abbruch Variablen
            fail_counter = fail_counter + 1
            approval_counter = 0
            final_fail_counter = final_fail_counter + 1

            #early Fail ausschließen, da i sonst negativ wäre
            if i > fallback:

                # um "Fallback" Schritte zurück gehen
                value = i-fallback
                x = trajectory_df.loc[(value), ('x')]
                y = trajectory_df.loc[(value), ('y')]
                z = trajectory_df.loc[(value), ('z')]
                gamma = trajectory_df.loc[(value), ('gamma')]
                teta = trajectory_df.loc[(value), ('teta')]
                i = value

            #early Fail
            else:

                print("Fail_e")
                break

        #Laufvariablen erhöhen
        i = i+1
        k = k+1

        # zu oft am selben Punkt gescheitert (kommt nicht aus Ecke raus)
        if final_fail_counter>kill_value:
            print("Fail_n")
            break
        if k>overflow:
            print("Fail_o")
            break



    if i==1000:
        print("Erfolg " + str(j+1))
        j = j + 1
        # Ablegen in Exel
        trajectory_df.to_excel(writer, sheet_name='Sheet' + str(j))



writer.save()

