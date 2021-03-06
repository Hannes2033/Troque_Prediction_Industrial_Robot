import pickle
import time
import tensorflow as tf
from bayes_opt import BayesianOptimization
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.compat.v1.keras.layers import CuDNNLSTM

# input and output path
input_path = "/content/drive/MyDrive/Projektarbeit WZL/training_input.pickle"
output_path = "/content/drive/MyDrive/Projektarbeit WZL/training_output.pickle"

# define limits for the values to be optimized
pbounds = {'input_units': (128, 768),
           'conv_units': (128, 384),
           'n_layers': (1, 4),
           'neuron_shrink': (0.01, 1),
           'dropout': (0.0, 0.3),
           'dense_units': (32, 64),
           'lr': (1e-5, 1e-2),
           'batch': (1, 50)}

# method which creates the KNN
def build_model(input_units, conv_units, n_layers, neuron_shrink, dropout, dense_units):
    # model type
    model = keras.models.Sequential()

    # add input LSTM layer + dropout
    model.add(CuDNNLSTM(int(input_units), batch_input_shape=(None, 5, 18), return_sequences=True))
    model.add(Dropout(dropout))

    # add variable number of LSTM layer + dropout
    for i in range(int(n_layers)):
        model.add(CuDNNLSTM(int(conv_units), return_sequences=True))
        model.add(Dropout(dropout))

        conv_units = int(conv_units * neuron_shrink)

    # add a denslayer + dropout
    model.add(Dense(dense_units, activation='tanh'))
    model.add(Dropout(dropout))

    # add output dense layer
    model.add(Dense(1))

    return model


def evaluate_network(input_units, conv_units, n_layers, neuron_shrink, dropout, dense_units, lr, batch):
    # import the input data
    pickle_in = open(input_path, "rb")
    input = pickle.load(pickle_in)

    # import the output data
    pickle_out = open(output_path, "rb")
    output = pickle.load(pickle_out)

    # variable
    data_num = input.shape[0]

    # split into training and validation data
    num_train = int(data_num * 0.7)
    num_test = num_train

    input_train = input[0:num_train]
    output_train = output[0:num_train]
    input_test = input[num_test:]
    output_test = output[num_test:]

    # build model with inputs
    model = build_model(input_units, conv_units, n_layers, neuron_shrink, dropout, dense_units)
    opt = tf.keras.optimizers.Adam(learning_rate=lr, decay=1e-5)
    model.compile(loss='mean_absolute_error', optimizer=opt, metrics=['accuracy'])

    history = model.fit(input_train, output_train, epochs=40, validation_data=(input_test, output_test),
                        batch_size=int(batch))

    # determine optimization parameters
    val_loss = history.history['val_loss'][-1]

    return -val_loss


# set optimizer
optimizer = BayesianOptimization(
    f=evaluate_network,
    pbounds=pbounds,
    verbose=2,
    random_state=1337,  # random seed
)

# determine calculation time
start_time = time.time()
optimizer.maximize(init_points=40, n_iter=10)
time_took = time.time() - start_time

print(f"Total runtime: {time_took}")
print(optimizer.max)