import matplotlib.pyplot as plt
import pandas as pd


# select data
Data = 'Data/Trajectory_Data_xyz.xlsx' # data you want to visualize
sheet = 'Sheet1' # sheet you want to visualize

# loading data
pos_df = pd.read_excel(Data, sheet_name = sheet)

# transform to list
pos = pos_df.values.tolist()

# create figure
fig = plt.figure(figsize = (4,4))
ax = fig.add_subplot(111, projection = '3d')

# label axes
ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")

# data to axis
x = pos_df['x']
y = pos_df['y']
z = pos_df['z']

# plot figure
ax.plot3D(xs = x, ys = y, zs = z, c = 'b')
plt.show()