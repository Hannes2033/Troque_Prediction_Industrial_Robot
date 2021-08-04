import time
import math
import pickle
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.compat.v1.keras.layers import CuDNNLSTM
import numpy as np




#Input Daten aus Pickle lesen
pickle_in = open("/content/drive/MyDrive/Projektarbeit WZL/Data_Pickle/transfer_input_halb.pickle","rb")
input = pickle.load(pickle_in)

#Output Daten aus Pickle lesen
pickle_out = open("/content/drive/MyDrive/Projektarbeit WZL/Data_Pickle/transfer_output_halb.pickle","rb")
output = pickle.load(pickle_out)

print(input.shape)
print(output.shape)


#Variablen bestimmen
inp=input
outp=output
percentage=0.7 #Prozent an Trainingsdaten
neuronen_num1=758 #Neuronen Input-Layer
neuronen_num2=302 #Neuronen LSTM Layer
neuron_shrink=0.423973728 #reduktion der Neuronen pro Layer
dense_neuronen_num=32 #Neuronen in Dense Layer
dropout=0.07471951 #Dropout Rate nach jedem Layer
epoch_num=10 #wie oft werden die Daten durchlafen
batch_num=1 #wie viele Daten bis Anpassung durchlaufen werden
learning_rate_num=0.0003020243
dacay_rate_num=1e-5

# Zahl der Daten bestimmen
data_num = inp.shape[0]

# Aufteilen in Training und Validierung(Test)
num_train = int(data_num * percentage)
num_test = num_train

input_train = inp[0:num_train]
output_train = outp[0:num_train]
input_test = inp[num_test:]
output_test = outp[num_test:]

#Model erstellen
model = Sequential()

#Input Layer erstellen
layer_0=CuDNNLSTM(neuronen_num1, batch_input_shape=(None, 5, 18),return_sequences=True)
model.add(layer_0)
model.add(Dropout(dropout))

#LSTM1 erstellen und hinzufügen
layer_1=CuDNNLSTM(neuronen_num2, return_sequences=True)
model.add(layer_1)
model.add(Dropout(dropout))

#LSTM2 erstellen und hinzufügen
layer_2=CuDNNLSTM(int(neuronen_num2*neuron_shrink), return_sequences=True)
model.add(layer_2)
model.add(Dropout(dropout))

#LSTM3 erstellen und hinzufügen
layer_3=CuDNNLSTM(int(neuronen_num2*neuron_shrink*neuron_shrink), return_sequences=True)
model.add(layer_3)
model.add(Dropout(dropout))

#Dense1 erstellen und hinzufügen
layer_4=Dense(dense_neuronen_num,activation='tanh')
model.add(layer_4)
model.add(Dropout(dropout))

#Output Layer erstellen
layer_5=Dense(1)
model.add(layer_5)

#lernen aktivieren
opt = tf.keras.optimizers.Adam(learning_rate=learning_rate_num, decay=dacay_rate_num)

model.compile(loss='mean_absolute_error', optimizer=opt, metrics=['accuracy'])

model.summary()

history = model.fit(input_train, output_train, epochs=epoch_num, validation_data=(input_test, output_test),batch_size=batch_num)

#Weights in Pickel abspeichern
pickle_layer_0=open("/content/drive/MyDrive/Projektarbeit WZL/layer_0_real_1.pickle","wb")
pickle_layer_1=open("/content/drive/MyDrive/Projektarbeit WZL/layer_1_real_1.pickle","wb")
pickle_layer_2=open("/content/drive/MyDrive/Projektarbeit WZL/layer_2_real_1.pickle","wb")
pickle_layer_3=open("/content/drive/MyDrive/Projektarbeit WZL/layer_3_real_1.pickle","wb")
pickle_layer_4=open("/content/drive/MyDrive/Projektarbeit WZL/layer_4_real_1.pickle","wb")
pickle_layer_5=open("/content/drive/MyDrive/Projektarbeit WZL/layer_5_real_1.pickle","wb")
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

print("Fertig")