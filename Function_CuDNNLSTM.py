def func_CuDNNLSTM (inp, outp, LSTM_num=1, Dense_num=1, percentage=0.7, neuronen_num1=128, neuronen_num2=128, dense_neuronen_num=60, dropout=0.2, epoch_num=10):
    print("fertig")

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, LSTM
    from tensorflow.compat.v1.keras.layers import CuDNNLSTM

    data_num = inp.shape[0]

    num_train = int(data_num * percentage)
    num_test = num_train

    input_train = inp[0:num_train]
    output_train = outp[0:num_train]
    input_test = inp[num_test:]
    output_test = outp[num_test:]

    model = Sequential()

    model.add(CuDNNLSTM(neuronen_num1, batch_input_shape=(None, 5, 3), return_sequences=True))
    #model.add(LSTM(neuronen_num1, batch_input_shape=(None, 5, 3), return_sequences=True))
    model.add(Dropout(dropout))

    for i in range(LSTM_num):
        model.add(CuDNNLSTM(neuronen_num2, return_sequences=True))
        #model.add(LSTM(neuronen_num2, return_sequences=True))
        model.add(Dropout(dropout))


    for j in range(Dense_num):
        model.add(Dense(dense_neuronen_num, activation='tanh'))
        model.add(Dropout(dropout))

    model.add(Dense(6, activation='tanh'))


    opt = tf.keras.optimizers.Adam(lr=1e-3, decay=1e-5)

    model.compile(loss='mean_absolute_error', optimizer=opt, metrics=['accuracy'])

    history = model.fit(input_train, output_train, epochs=epoch_num, validation_data=(input_test, output_test), batch_size=1)