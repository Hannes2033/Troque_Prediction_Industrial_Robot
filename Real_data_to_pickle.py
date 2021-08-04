import numpy as np
import pandas as pd
import pickle

#Dateinen Namen/Pfad
CSV_name='Data/Real_data/Input_x_LSTM.csv'

input_pickle_path='Data/transfer_input_ganz.pickle'
input_parameter_pickle_path='Data/parameter_transfer_input_ganz.pickle'
output_pickle_path='Data/transfer_output_ganz.pickle'
output_parameter_pickle_path='Data/parameter_transfer_output_ganz.pickle'



#csv auslesen
real_input_data_df_unordert = pd.read_csv(CSV_name, header = None, delimiter=',', na_values=' ',
                                 names= [
                                     'Position 1', 'Velocity 1','Acceleration 1','Position 2', 'Velocity 2','Acceleration 2',
                                     'Position 3','Velocity 3','Acceleration 3', 'Position 4', 'Velocity 4','Acceleration 4',
                                     'Position 5','Velocity 5','Acceleration 5','Position 6', 'Velocity 6','Acceleration 6'])
real_output_data_df = pd.read_csv('Data/Real_data/Input_y_LSTM.csv',header = None, delimiter=',', na_values=' ',
                                  names= ['Torque 1'])


real_input_data_df = real_input_data_df_unordert[[
                                    'Position 1', 'Velocity 1','Position 2', 'Velocity 2',
                                    'Position 3','Velocity 3', 'Position 4', 'Velocity 4',
                                    'Position 5','Velocity 5','Position 6', 'Velocity 6',
                                    'Acceleration 1','Acceleration 2','Acceleration 3','Acceleration 4','Acceleration 5','Acceleration 6']]


#Daten in Array speichern
real_input_data_array = np.array(real_input_data_df, dtype=float)
real_output_data_array = np.array(real_output_data_df, dtype=float)

# #Daten kürzen um alle Achsen zu bewegen
# print(real_input_data_array.shape)
# anzahl_daten=67475
# real_input_data_array=real_input_data_array[int(anzahl_daten/2)-int(anzahl_daten/2)%5:,:]
# real_output_data_array=real_output_data_array[int(anzahl_daten/2)-int(anzahl_daten/2)%5:,:]
# print(real_input_data_array.shape)


#Daten reshapen zahl berechnen
reshape = real_input_data_array.shape[0]/5
reshape = int(reshape)

#Daten reshapen
real_input_data_array = real_input_data_array.reshape(reshape,5,18)
real_output_data_array = real_output_data_array.reshape(reshape,5,1)


print(real_input_data_array.shape)

par_input =[]

#Normalisierung des Inputs
for i in range(18):
    in_max = np.amax(real_input_data_array[:,:,i])
    in_min = np.amin(real_input_data_array[:,:,i])
    in_norm = max(in_max, abs(in_min))
    #output[:,:,i] = (output[:,:,i] - out_min) / (out_max - out_min)
    real_input_data_array[:,:,i] = real_input_data_array[:, :, i] / in_norm
    par_input = par_input +[in_norm]


par_output =[]

#Normalisierung des Outputs
for i in range(1):
    out_max = np.amax(real_output_data_array[:,:,i])
    out_min = np.amin(real_output_data_array[:,:,i])
    out_norm = max(out_max, abs(out_min))
    #output[:,:,i] = (output[:,:,i] - out_min) / (out_max - out_min)
    real_output_data_array[:,:,i] = real_output_data_array[:, :, i] / out_norm
    par_output = par_output + [out_norm]

    #---------------------------------------------------------------------------------------------------------------------------------
    #Vorzeichen wechsel aufgrund falscher Drehrichtung zwischen Modell und Real-Roboter
    real_output_data_array[:,:,:] = -real_output_data_array[:,:,:]
    # ---------------------------------------------------------------------------------------------------------------------------------

#Abspeichern der Real Input Data in Pickle
pickle_real_input_data = open(input_pickle_path,'wb')
pickle.dump(real_input_data_array, pickle_real_input_data)
pickle_real_input_data.close()

#Abspeichern der Real Output Data in Pickle
pickle_real_output_data = open(output_pickle_path,'wb')
pickle.dump(real_output_data_array, pickle_real_output_data)
pickle_real_output_data.close()

#Abspeichern der Input parameter in Pickle
pickle_par_input = open(input_parameter_pickle_path,'wb')
pickle.dump(par_input, pickle_par_input)
pickle_par_input.close()

#Abspeichern der Output parameter in Pickle
pickle_par_output = open(output_parameter_pickle_path,'wb')
pickle.dump(par_output, pickle_par_output)
pickle_par_output.close()

print('fertig')