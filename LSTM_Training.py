import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
import numpy as np


# input and output path
input_path = "/content/drive/MyDrive/Projektarbeit WZL/Data_Pickle/transfer_input_halb.pickle"
output_path = "/content/drive/MyDrive/Projektarbeit WZL/Data_Pickle/transfer_output_halb.pickle"

# weights path
layer_0_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_0_real_1.pickle"
layer_1_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_1_real_1.pickle"
layer_2_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_2_real_1.pickle"
layer_3_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_3_real_1.pickle"
layer_4_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_4_real_1.pickle"
layer_5_weights_path = "/content/drive/MyDrive/Projektarbeit WZL/layer_5_real_1.pickle"

# determine variables
inp = input
outp = output
percentage = 0.7 # percent of training data
neuronen_num1 = 758 # neurons input layer
neuronen_num2 = 302 # neurons LSTM layer
neuron_shrink = 0.423973728 # reduction of neurons per layer
dense_neuronen_num = 32 # neurons dense layer
dropout = 0.07471951 # dropout rate
epoch_num = 10 # how often the data is passed through
batch_num = 1 # how much data is passed through until adjustment
learning_rate_num = 0.0003020243 # learning rate
dacay_rate_num = 1e-5 # decay of learning rate



# read input data from pickle
pickle_in = open(input_path,"rb")
input = pickle.load(pickle_in)

# read output data from pickle
pickle_out = open(output_path,"rb")
output = pickle.load(pickle_out)

print(input.shape)
print(output.shape)


# determine number of data
data_num = inp.shape[0]

# Split into training and validation
num_train = int(data_num * percentage)
num_test = num_train

input_train = inp[0:num_train]
output_train = outp[0:num_train]
input_test = inp[num_test:]
output_test = outp[num_test:]

# build model
model = Sequential()

# create input layer
layer_0=CuDNNLSTM(neuronen_num1, batch_input_shape=(None, 5, 18),return_sequences=True)
model.add(layer_0)
model.add(Dropout(dropout))

# create and add LSTM1
layer_1=CuDNNLSTM(neuronen_num2, return_sequences=True)
model.add(layer_1)
model.add(Dropout(dropout))

# Create and add LSTM2
layer_2=CuDNNLSTM(int(neuronen_num2*neuron_shrink), return_sequences=True)
model.add(layer_2)
model.add(Dropout(dropout))

# Create and add LSTM3
layer_3=CuDNNLSTM(int(neuronen_num2*neuron_shrink*neuron_shrink), return_sequences=True)
model.add(layer_3)
model.add(Dropout(dropout))

# Create and add dense1
layer_4=Dense(dense_neuronen_num,activation='tanh')
model.add(layer_4)
model.add(Dropout(dropout))

# create output layer
layer_5=Dense(1)
model.add(layer_5)

# activate learning
opt = tf.keras.optimizers.Adam(learning_rate=learning_rate_num, decay=dacay_rate_num)

model.compile(loss='mean_absolute_error', optimizer=opt, metrics=['accuracy'])

model.summary()

history = model.fit(input_train, output_train, epochs=epoch_num, validation_data=(input_test, output_test),batch_size=batch_num)

# save weights in pickel
pickle_layer_0=open(layer_0_weights_path,"wb")
pickle_layer_1=open(layer_1_weights_path,"wb")
pickle_layer_2=open(layer_2_weights_path,"wb")
pickle_layer_3=open(layer_3_weights_path,"wb")
pickle_layer_4=open(layer_4_weights_path,"wb")
pickle_layer_5=open(layer_5_weights_path,"wb")

pickle.dump(layer_0.get_weights(),pickle_layer_0)
pickle.dump(layer_1.get_weights(),pickle_layer_1)
pickle.dump(layer_2.get_weights(),pickle_layer_2)
pickle.dump(layer_3.get_weights(),pickle_layer_3)
pickle.dump(layer_4.get_weights(),pickle_layer_4)
pickle.dump(layer_5.get_weights(),pickle_layer_5)

pickle_layer_0.close()
pickle_layer_1.close()
pickle_layer_2.close()
pickle_layer_3.close()
pickle_layer_4.close()
pickle_layer_5.close()

print("done")