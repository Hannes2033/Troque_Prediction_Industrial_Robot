import math
import random as rnd
import pandas as pd

# path of output
output_path = 'Data/1_final_Trajektorien_Daten.xlsx'

# number of trajectories
number_of_trajectories = 1000

# number of constant points, until the sinus starts
pre_sinus_number=100

# points per trajectory, after initial constant points
length=1100

# create excel writer
writer = pd.ExcelWriter(output_path, engine='xlsxwriter')

# create dataframe
trajectory_df = pd.DataFrame(columns=['Pos1','Pos2','Pos3','Pos4','Pos5','Pos6'])

# running variable
j = 0

# repeat for every trajectory
while j < number_of_trajectories:

    # repeat for every axis
    for i in range (1,7):

        # randomize sinus parameters
        a = rnd.uniform(-0.5,0.5)
        b = rnd.uniform(0.5,3)
        c = math.pi/2
        d = 0

        # special values for second axis. robot would otherwise collide with floor.
        if i==2:
            a = rnd.uniform(-0.2, 0.2)
            b = rnd.uniform(0.5, 3)
            d = 0.2

        # special values for second axis. robot would otherwise collide with floor.
        if i==3:
            a = rnd.uniform(-0.5, 0.5)
            b = rnd.uniform(0.5, 3)
            d = 0.5


        # calculate every Point
        for k in range (-pre_sinus_number, length):
            x= 5 * k / length
            Position = a*math.sin(b*x+c)+d

            # constant Points stay at start Position (x=0)
            if k<1:
                Position=a+d

            # save Position in Dataframe
            trajectory_df.loc[k + pre_sinus_number, 'Pos' + str(i)] = Position


    # create counter to keep track of status
    print("trajectory " + str(j+1) + " done")

    # increase running variable
    j = j + 1

    # save trajectory to an Excel sheet
    trajectory_df.to_excel(writer, sheet_name='Sheet' + str(j))


# close writer
writer.save()

# the end