import numpy as np
import pandas as pd
import pickle

# file name/path
excelName = 'Data/1_final_drehmomente_daten.xlsx'

input_pickle_path = 'Data/training_input.pickle'
input_parameter_pickle_path = 'Data/parameter_training_input.pickle'
output_pickle_path = 'Data/training_output.pickle'
output_parameter_pickle_path = 'Data/parameter_training_output.pickle'

# parameter
number_of_trajectories = 1000
num_train = int(number_of_trajectories * 0.7)
num_test = num_train
j = 0


# create empty arrays
input = np.zeros((number_of_trajectories, 1200, 18))
output = np.zeros((number_of_trajectories, 1200, 1))

# reading the data from an Excel sheet and saving it in the arrays
while j < number_of_trajectories:
    # save data from Exel to dataframe
    Data = pd.read_excel(excelName,sheet_name='Sheet'+str(j+1))

    # separate input and output
    Data_x = Data [['Position 1', 'Velocity 1','Position 2', 'Velocity 2',
                    'Position 3', 'Velocity 3', 'Position 4', 'Velocity 4',
                    'Position 5','Velocity 5', 'Position 6', 'Velocity 6',
                    'Acceleration 1', 'Acceleration 2', 'Acceleration 3',
                    'Acceleration 4', 'Acceleration 5', 'Acceleration 6']]
    Data_y = Data[['Torque 1']]

    # save data to array
    data_x = np.array(Data_x, dtype=float)
    data_y = np.array(Data_y, dtype=float)

    # restore data
    input [j] = data_x
    output [j] = data_y

    # running variable
    j=j+1

    # create counter to check progress
    print(j,"/",number_of_trajectories)




# delete the first 100 entries because they are without movement
del_num = np.linspace(0,100,100, dtype=int)

input = np.delete(input, [del_num], axis=1)
output = np.delete(output, [del_num], axis=1)


# delete the last 100 entries to make a clean cut
input = input[:,:1000,:]
output = output[:,:1000,:]


# data reshaping
reshape = (number_of_trajectories*1000)/5
reshape = int(reshape)

input = input.reshape(reshape,5,18)
output = output.reshape(reshape,5,1)



par_input =[]

# normalization of the input
for i in range(17):
    in_max = np.amax(input[:,:,i])
    in_min = np.amin(input[:,:,i])
    in_norm = max(in_max, abs(in_min))
    input[:,:,i] = input[:, :, i] / in_norm
    par_input = par_input +[in_norm]

par_output =[]

# normalization of the output
for i in range(1):
    out_max = np.amax(output[:,:,i])
    out_min = np.amin(output[:,:,i])
    out_norm = max(out_max, abs(out_min))
    output[:,:,i] = output[:, :, i] / out_norm
    par_output = par_output + [out_norm]
    #---------------------------------------------------------------------------------------------------------------------------------
    # sign change due to wrong direction of rotation between model and real robot
    output[:,:,:] = -output[:,:,:]
    # ---------------------------------------------------------------------------------------------------------------------------------


# saving the input in pickle
pickle_input = open(input_pickle_path,'wb')
pickle.dump(input, pickle_input)
pickle_input.close()

# saving the output in pickle
pickle_output = open(output_pickle_path,'wb')
pickle.dump(output, pickle_output)
pickle_output.close()

# saving the input parameters in pickle
pickle_par_input = open(input_parameter_pickle_path,'wb')
pickle.dump(par_input, pickle_par_input)
pickle_par_input.close()

# saving the output parameters in pickle
pickle_par_output = open(output_parameter_pickle_path,'wb')
pickle.dump(par_output, pickle_par_output)
pickle_par_output.close()

print('Input shape:', input.shape)
print('Output shape', output.shape)
print('done')