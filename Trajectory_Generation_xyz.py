import math
import random as rnd
import pandas as pd



# create ExelWriter
xyz_data = 'Data/Trajectory_Data_xyz.xlsx'
writer = pd.ExcelWriter(xyz_data, engine='xlsxwriter')


# create Dataframe
trajectory_df = pd.DataFrame(columns=['x','y','z','gamma','teta'])


# running variable
j = 0

# number of trajectories
number_of_trajectories = 5

# Defining area
x_min = 1.1
x_max = 1.5
y_min = -0.3
y_max = 0.3
z_min = 0.6
z_max = 1.0

# termination number
kill_value = 50

# max number of calculations per trajectory
overflow = 10000

# number of points per trajectory
trajectory_length = 1000

# number of correction iterations
fallback = 20
fallback_addition = 1

# max change of angle
delta_angle = 7

while j < number_of_trajectories:

    # Random startpositions
    x_0 = rnd.uniform(x_min, x_max)
    y_0 = rnd.uniform(y_min, y_max)
    z_0 = rnd.uniform(z_min, z_max)

    # Random startangle
    gamma_0 = rnd.uniform(0, 2*math.pi) #Winkel um die y-Achse
    teta_0 = rnd.uniform(0, math.pi) #Winkel um die z-Achse

    # Saving of startpoint and startangle
    trajectory_df.loc[(0), ('x')] = x_0
    trajectory_df.loc[[0], ['y']] = y_0
    trajectory_df.loc[[0], ['z']] = z_0
    trajectory_df.loc[[0], ['gamma']] = gamma_0
    trajectory_df.loc[[0], ['teta']] = teta_0

    # define standard length and deviation
    standard_length = 0.002 #beschreibt die mittlere Länge zwischen zwei Punkten
    correction_low = 0.5 #minimaler Faktor für Länge
    correction_high = 1.5 #maximaler Faktor für Länge



    # define the maximum angular deviations between two steps
    delta_gamma = math.pi/180*delta_angle  #letzte Zahl gibt maximale Winkeländerung in ° an
    delta_teta = math.pi/180*delta_angle #letzte Zahl gibt maximale Winkeländerung in ° an


    # give first point and angle
    x = x_0
    y = y_0
    z = z_0
    gamma = gamma_0
    teta = teta_0

    # define termination variables
    fail_counter = 0
    approval_counter = 0
    final_fail_counter = 0

    # running variable
    k = 0
    i = 0

    while i < trajectory_length:

        # determine length
        length = rnd.uniform(correction_low, correction_high) * standard_length

        # determine angle
        gamma = gamma + rnd.uniform(-delta_gamma, delta_gamma)
        teta = teta + rnd.uniform(-delta_teta, delta_teta)

        # determine x,y,z
        z = z + math.sin(gamma) * length  # erst Drehung um y-Achse
        y = y + math.cos(gamma) * length * math.sin(teta)  # erst Drehung um y-Achse, dann um z-Achse
        x = x + math.cos(gamma) * length * math.cos(teta)  # erst Drehung um y-Achse, dann um z-Achse

        # saving the points
        trajectory_df.loc[(i), ('x')] = x
        trajectory_df.loc[(i), ('y')] = y
        trajectory_df.loc[(i), ('z')] = z
        trajectory_df.loc[(i), ('gamma')] = gamma
        trajectory_df.loc[(i), ('teta')] = teta

        # check if the new point is in our range
        if x > x_min and x < x_max and y > y_min and y < y_max and z > z_min and z < z_max:

            # termination variables
            fail_counter = 0
            approval_counter = approval_counter + 1
            if approval_counter > fallback + fallback_addition:
                final_fail_counter = 0

        # if new point is not in valid range
        else:
            # termination variables
            fail_counter = fail_counter + 1
            approval_counter = 0
            final_fail_counter = final_fail_counter + 1

            # exclude early fail, otherwise i would be negative
            if i > fallback:

                # to go back "fallback" steps
                value = i-fallback
                x = trajectory_df.loc[(value), ('x')]
                y = trajectory_df.loc[(value), ('y')]
                z = trajectory_df.loc[(value), ('z')]
                gamma = trajectory_df.loc[(value), ('gamma')]
                teta = trajectory_df.loc[(value), ('teta')]
                i = value

            # early fail
            else:

                print("Fail_e")
                break

        # increase run variables
        i = i+1
        k = k+1

        # failed too often at the same point (can't get out of corner)
        if final_fail_counter>kill_value:
            print("Fail_n")
            break
        if k > overflow:
            print("Fail_o")
            break


    # end of program
    if i == 1000:
        print("Erfolg " + str(j+1))
        j = j + 1
        # Ablegen in Exel
        trajectory_df.to_excel(writer, sheet_name='Sheet' + str(j))



writer.save()

