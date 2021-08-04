import numpy as np
import pandas as pd
import pickle

# file path
csv_name = 'Data/Real_data/Input_x_LSTM.csv'

input_pickle_path = 'Data/Real_data/transfer_input_hole.pickle'
input_parameter_pickle_path = 'Data/Real_data/parameter_transfer_input_hole.pickle'
output_pickle_path = 'Data/Real_data/transfer_output_hole.pickle'
output_parameter_pickle_path = 'Data/Real_data/parameter_transfer_output_hole.pickle'



#save data from csv in dataframe
real_input_data_df_unordert = pd.read_csv(csv_name, header = None, delimiter =',', na_values =' ',
                                          names = [
                                     'Position 1', 'Velocity 1','Acceleration 1','Position 2', 'Velocity 2','Acceleration 2',
                                     'Position 3','Velocity 3','Acceleration 3', 'Position 4', 'Velocity 4','Acceleration 4',
                                     'Position 5','Velocity 5','Acceleration 5','Position 6', 'Velocity 6','Acceleration 6'])

real_output_data_df = pd.read_csv(csv_name,header = None, delimiter=',', na_values=' ',
                                  names= ['Torque 1'])

# order dataframe
real_input_data_df = real_input_data_df_unordert[[
                                    'Position 1', 'Velocity 1','Position 2', 'Velocity 2',
                                    'Position 3','Velocity 3', 'Position 4', 'Velocity 4',
                                    'Position 5','Velocity 5','Position 6', 'Velocity 6',
                                    'Acceleration 1','Acceleration 2','Acceleration 3','Acceleration 4','Acceleration 5','Acceleration 6']]


# save data in array
real_input_data_array = np.array(real_input_data_df, dtype=float)
real_output_data_array = np.array(real_output_data_df, dtype=float)


# calculate data reshapen number
reshape = real_input_data_array.shape[0]/5
reshape = int(reshape)

# data reshapen
real_input_data_array = real_input_data_array.reshape(reshape,5,18)
real_output_data_array = real_output_data_array.reshape(reshape,5,1)

par_input = []

# normalization of the input
for i in range(18):
    in_max = np.amax(real_input_data_array[:,:,i])
    in_min = np.amin(real_input_data_array[:,:,i])
    in_norm = max(in_max, abs(in_min))
    #output[:,:,i] = (output[:,:,i] - out_min) / (out_max - out_min)
    real_input_data_array[:,:,i] = real_input_data_array[:, :, i] / in_norm
    par_input = par_input +[in_norm]


par_output =[]

# normalization of the output
for i in range(1):
    out_max = np.amax(real_output_data_array[:,:,i])
    out_min = np.amin(real_output_data_array[:,:,i])
    out_norm = max(out_max, abs(out_min))
    real_output_data_array[:,:,i] = real_output_data_array[:, :, i] / out_norm
    par_output = par_output + [out_norm]

    #---------------------------------------------------------------------------------------------------------------------------------
    #Vorzeichen wechsel aufgrund falscher Drehrichtung zwischen Modell und Real-Roboter
    real_output_data_array[:,:,:] = -real_output_data_array[:,:,:]
    # ---------------------------------------------------------------------------------------------------------------------------------

# saving the real input data in pickle
pickle_real_input_data = open(input_pickle_path,'wb')
pickle.dump(real_input_data_array, pickle_real_input_data)
pickle_real_input_data.close()

# saving the real output data in pickle
pickle_real_output_data = open(output_pickle_path,'wb')
pickle.dump(real_output_data_array, pickle_real_output_data)
pickle_real_output_data.close()

# saving the input parameter in pickle
pickle_par_input = open(input_parameter_pickle_path,'wb')
pickle.dump(par_input, pickle_par_input)
pickle_par_input.close()

# saving the output parameter in pickle
pickle_par_output = open(output_parameter_pickle_path,'wb')
pickle.dump(par_output, pickle_par_output)
pickle_par_output.close()

print('fertig')