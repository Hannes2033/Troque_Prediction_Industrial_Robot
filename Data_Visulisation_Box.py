import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

pos_df = pd.read_excel('Data/Learning_Data_Minh.xlsx',sheet_name='Sheet1')
# pickle_Learning_Data_Minh = open('Data/Learning_Data_Minh.pickle','wb')
# pickle.dump(pos_df, pickle_Learning_Data_Minh)
# pickle_Learning_Data_Minh.close()
print(pos_df.keys())
Position = pos_df[['Position 1','Position 2','Position 3','Position 4','Position 5','Position 6']]
Velocity = pos_df[['Velocity 1','Velocity 2','Velocity 3','Velocity 4','Velocity 5','Velocity 6']]
Acceleration = pos_df[['Acceleration 1', 'Acceleration 2', 'Acceleration 3', 'Acceleration 4',
       'Acceleration 5', 'Acceleration 6']]
Torque = pos_df[['Torque 1','Torque 2','Torque 3','Torque 4','Torque 5','Torque 6']]
y_scale = np.linspace(0,10,10)
# fig = plt.figure()
#
# position = fig.add_subplot(1,1,1)
# position.boxplot(x = Position)
#
# velocity = fig.add_subplot(1,1,2)
# velocity.boxplot(x = Velocity)
#
# acceleration = fig.add_subplot(1,1,3)
# acceleration.boxplot(x = Acceleration)
#
# torque = fig.add_subplot(1,1,4)
# torque.boxplot(x = Torque)
# plt.show()

fig, axs = plt.subplots(2,2)
axs[0, 0].boxplot(Position,showfliers = False)
axs[0, 0].set_title('Position')

axs[0, 1].boxplot(Velocity, 'tab:orange',showfliers = False)
axs[0, 1].set_title('Velocity')

axs[1, 0].boxplot(x =Acceleration, showfliers = False)
axs[1, 0].set_title('Acceleration')

axs[1, 1].boxplot(Torque,  'tab:red',showfliers = False)
axs[1, 1].set_title('Torque')

plt.show()
print(Acceleration)