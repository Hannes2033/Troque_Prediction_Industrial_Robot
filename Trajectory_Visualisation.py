import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pos_df = pd.read_excel('Data/2_final_Trajektorien_Daten.xlsx',sheet_name='Sheet3')
pos = pos_df.values.tolist()

# Figure erstellen
fig = plt.figure(figsize = (4,4))
ax = fig.add_subplot(111, projection='3d')

#Achsen beschriften
ax.set_xlabel("X")

ax.set_ylabel("Y")

ax.set_zlabel("Z")


x = pos_df['x']
y = pos_df['y']
z = pos_df['z']
ax.plot3D(xs=x,ys=y,zs=z, c = 'b')
#for i in range(len(pos)):

    #ax.plot3D(xs=pos[i][0],ys=pos[i][1],zs=pos[i][2], c = 'b')
plt.show()