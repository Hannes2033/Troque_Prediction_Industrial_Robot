import numpy as np
import pandas as pd
import pickle

#Dateinen Namen/Pfad
excelName='Data/1_final_drehmomente_daten.xlsx'

input_pickle_path='Data/training_input.pickle'
input_parameter_pickle_path='Data/parameter_training_input.pickle'
output_pickle_path='Data/training_output.pickle'
output_parameter_pickle_path='Data/parameter_training_output.pickle'

#Parameter
number_of_trajectories = 1000
num_train = int(number_of_trajectories * 0.7)
num_test = num_train
j = 0


#Erstellen von leeren Arrays
input = np.zeros((number_of_trajectories, 1200, 18))
output = np.zeros((number_of_trajectories, 1200, 1))

#Auslesen der Daten aus einer Exel und abspeichern in den Arrays
while j < number_of_trajectories:
    #Daten aus Exel in dataframe speichern
    Data = pd.read_excel(excelName,sheet_name='Sheet'+str(j+1))

    #Input und Output trennen
    Data_x = Data [['Position 1', 'Velocity 1','Position 2', 'Velocity 2',
                    'Position 3', 'Velocity 3', 'Position 4', 'Velocity 4',
                    'Position 5','Velocity 5', 'Position 6', 'Velocity 6',
                    'Acceleration 1', 'Acceleration 2', 'Acceleration 3',
                    'Acceleration 4', 'Acceleration 5', 'Acceleration 6']]
    Data_y = Data[['Torque 1']]

    #Daten in Array speichern
    data_x = np.array(Data_x, dtype=float)
    data_y = np.array(Data_y, dtype=float)

    #Daten umspeichern
    input [j] = data_x
    output [j] = data_y

    #Laufvariable
    j=j+1

    #Zähler erstellen um Fortschritt zu prüfen
    print(j,"/",number_of_trajectories)




#Löschen der ersten 100 Einträge da diese ohne Bewegung sind
del_num = np.linspace(0,100,100, dtype=int)

input = np.delete(input, [del_num], axis=1)
output = np.delete(output, [del_num], axis=1)


#Löschen der letzten 100 Einträge um einen sauberen Schnitt zu machen
input = input[:,:1000,:]
output = output[:,:1000,:]


#Daten reshapen
reshape = (number_of_trajectories*1000)/5
reshape = int(reshape)

input = input.reshape(reshape,5,18)
output = output.reshape(reshape,5,1)



par_input =[]

#Normalisierung des Inputs
for i in range(17):
    in_max = np.amax(input[:,:,i])
    in_min = np.amin(input[:,:,i])
    in_norm = max(in_max, abs(in_min))
    #output[:,:,i] = (output[:,:,i] - out_min) / (out_max - out_min)
    input[:,:,i] = input[:, :, i] / in_norm
    par_input = par_input +[in_norm]

par_output =[]

#Normalisierung des Outputs
for i in range(1):
    out_max = np.amax(output[:,:,i])
    out_min = np.amin(output[:,:,i])
    out_norm = max(out_max, abs(out_min))
    #output[:,:,i] = (output[:,:,i] - out_min) / (out_max - out_min)
    output[:,:,i] = output[:, :, i] / out_norm
    par_output = par_output + [out_norm]
    #---------------------------------------------------------------------------------------------------------------------------------
    #Vorzeichen wechsel aufgrund falscher Drehrichtung zwischen Modell und Real-Roboter
    output[:,:,:] = -output[:,:,:]
    # ---------------------------------------------------------------------------------------------------------------------------------


#Abspeichern des Imputs in Pickle
pickle_input = open(input_pickle_path,'wb')
pickle.dump(input, pickle_input)
pickle_input.close()

#Abspeichern des outputs in Pickle
pickle_output = open(output_pickle_path,'wb')
pickle.dump(output, pickle_output)
pickle_output.close()

#Abspeichern der Input parameter in Pickle
pickle_par_input = open(input_parameter_pickle_path,'wb')
pickle.dump(par_input, pickle_par_input)
pickle_par_input.close()

#Abspeichern der Output parameter in Pickle
pickle_par_output = open(output_parameter_pickle_path,'wb')
pickle.dump(par_output, pickle_par_output)
pickle_par_output.close()

print('Input shape:', input.shape)
print('Output shape', output.shape)
print('fertig')