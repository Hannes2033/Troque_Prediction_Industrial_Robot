import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# select data
Data = 'Data/Trajectory_Data_xyz.xlsx' # data you want to visualize
sheet = 'Sheet1' # sheet you want to visualize

# loading data
pos_df = pd.read_excel(Data,sheet_name=sheet)

# order data
Position = pos_df[['Position 1','Position 2','Position 3','Position 4','Position 5','Position 6']]
Velocity = pos_df[['Velocity 1','Velocity 2','Velocity 3','Velocity 4','Velocity 5','Velocity 6']]
Acceleration = pos_df[['Acceleration 1', 'Acceleration 2', 'Acceleration 3', 'Acceleration 4',
                       'Acceleration 5', 'Acceleration 6']]
Torque = pos_df[['Torque 1','Torque 2','Torque 3','Torque 4','Torque 5','Torque 6']]

# rescale y axis
y_scale = np.linspace(0,10,10)

# plot data
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