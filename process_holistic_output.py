from datetime import datetime   
from matplotlib import pyplot as plt
import math


#open file and read into list
f = open('BrownLion67.txt', 'r')
filelines = f.readlines()
#print(filelines)

f = open("holistic_process_output.txt", "w")

# python plot
frame = 0

fig, ax = plt.subplots(2, sharex=True)

plt.ion()
plt.show()
plt.xlabel("Time")
plt.ylabel("Angle")

ax[0].set_title('Left Hand')
ax[0].set_ylabel("Angle")
ax[1].set_title('Right Hand')

#Left Hand
left_tap_start = 0
left_last_tap = 0
left_tap_time = 0
left_max_time = 0
left_tapdiff_f = 0

left_last_angle = 0
left_angle = 0
left_velocity = 0
left_velocity_up = 0
left_velocity_down = 0
left_position_closed = 1
left_finger_taps = 0
left_last_time = 0

left_angle_sum = 0
left_velocity_sum = 0

#Right Hand
right_tap_start = 0
right_last_tap = 0
right_max_time = 0
right_tap_time = 0
right_tapdiff_f = 0

right_last_angle = 0
right_angle = 0
right_velocity = 0
right_velocity_up = 0
right_velocity_down = 0
right_position_closed = 1
right_finger_taps = 0
right_last_time = 0

right_angle_sum = 0
right_velocity_sum = 0

# when finger tap angle is X degrees position is closed
# if the position is closed, X degree angle will be considered open
left_angle_closed = 10
right_angle_closed = 10
left_angle_open = 35
right_angle_open = 35
left_max_angle = 0
right_max_angle = 0

#print runtime parameters to output file
f.write('Run parameters angle_open=' + str(left_angle_open) + ' angle_closed=' + str(left_angle_closed) + "\n")

#parse out the file, only looking for time, and x,y,z coordinates for wrist, thumb,index
for x in filelines:

    ###############################
    # Frame Time
    if "frame" in x:
        #print(x)
        timestr = x.split(' ')[2]
        #print(timestr)
        frametime = datetime.strptime(timestr, "%H:%M:%S-%f ")
        #print('time:', t1.time())
        
        #initialize time variables
        if (left_last_time == 0):
            left_last_time = frametime
            left_last_tap = frametime
            left_tap_start = frametime
            left_max_time = frametime
            right_last_time = frametime
            right_last_tap = frametime
            right_tap_start = frametime
            right_max_time = frametime

    ########################################
    # Left Hand
    #parse this         
    #LEFT_HAND,WRIST,X,0.5899660587310791,Y,0.6407750248908997,Z,1.733735928155511e-07
    if "LEFT_HAND,WRIST" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        left_wrist_x = float(split_x[3])
        left_wrist_y = float(split_x[5])
        left_wrist_z = float(split_x[7])
        #print(wrist_x,wrist_y,wrist_z)
    if "LEFT_HAND,THUMBS_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        left_thumb_x = float(split_x[3])
        left_thumb_y = float(split_x[5])
        left_thumb_z = float(split_x[7])
        #print(thumb_x,thumb_y,thumb_z)
    if "LEFT_HAND,INDEX_FINGER_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        left_index_x = float(split_x[3])
        left_index_y = float(split_x[5])
        left_index_z = float(split_x[7])
        #print(index_x,index_y,index_z)
        
        #index finger is last variable ... process data
        #calculate thumb and index finger vector
        #https://www.omnicalculator.com/math/angle-between-two-vectors
        #https://math.stackexchange.com/questions/361412/finding-the-angle-between-three-points
        
        left_thumb_x_v = left_thumb_x - left_wrist_x
        left_thumb_y_v = left_thumb_y - left_wrist_y
        left_thumb_z_v = left_thumb_z - left_wrist_z            
          
        left_index_x_v = left_index_x - left_wrist_x
        left_index_y_v = left_index_y - left_wrist_y
        left_index_z_v = left_index_z - left_wrist_z  
            
        left_thumb_len = math.sqrt(left_thumb_x_v * left_thumb_x_v + left_thumb_y_v * left_thumb_y_v + left_thumb_z_v * left_thumb_z_v) 
        left_index_len = math.sqrt(left_index_x_v * left_index_x_v + left_index_y_v * left_index_y_v + left_index_z_v * left_index_z_v)
           
        left_dot_prod = left_thumb_x_v * left_index_x_v + left_thumb_y_v * left_index_y_v + left_thumb_z_v * left_index_z_v
            
        left_angle = math.degrees(math.acos( left_dot_prod / (left_thumb_len * left_index_len)))

        if (left_angle > left_max_angle):
            left_max_angle =  left_angle
            left_max_time = frametime

        #plot time and angle
        ax[0].plot(frametime,left_angle, '-o')

        framediff = frametime - left_last_time;
           
        #velocity = (angle - last_angle) / framediff_f
            
        left_last_time = frametime
        left_last_angle = left_angle

        #see if angle changes position to open or closed
        if (left_position_closed == 0) and (left_angle < left_angle_closed):
            left_position_closed = 1
            left_finger_taps = left_finger_taps + 1
            left_last_tap = left_tap_start
            left_tap_start = frametime
            left_tapdiff = left_tap_start - left_last_tap
            left_tapdiff_f = left_tapdiff.total_seconds()
            left_velocity = (2 *  left_max_angle) / left_tapdiff_f
            left_tapdiff =  left_max_time - left_last_tap
            left_velocity_up = left_max_angle / left_tapdiff.total_seconds()
            left_tapdiff =  left_tap_start - left_max_time
            left_velocity_down = left_max_angle / left_tapdiff.total_seconds()
            left_angle_sum = left_angle_sum + left_max_angle
            left_velocity_sum = left_velocity_sum + left_velocity
            print('Left Hand Taps=' + str(left_finger_taps) + ' Time=' + str(left_tapdiff_f) +
                  ' Max Angle=' + str(round(left_max_angle, 0)) + ' Total Velocity= ' + str(round(left_velocity, 1)) +
                  ' Up Velocity= ' + str(round(left_velocity_up, 1)) + ' Down Velocity= ' + str(round(left_velocity_down, 1)) + 
                  ' Avg Angle=' + str(round(left_angle_sum/left_finger_taps, 0)) + ' Avg Velocity= ' + str(round(left_velocity_sum/left_finger_taps, 1)))
            f.write('Left Hand Taps=' + str(left_finger_taps) + ' Time=' + str(left_tapdiff_f) +
                  ' Max Angle=' + str(round(left_max_angle, 0)) + ' Total Velocity= ' + str(round(left_velocity, 1)) + 
                  ' Up Velocity= ' + str(round(left_velocity_up, 1)) + ' Down Velocity= ' + str(round(left_velocity_down, 1))  + 
                  ' Avg Angle=' + str(round(left_angle_sum/left_finger_taps, 0)) + ' Avg Velocity= ' + str(round(left_velocity_sum/left_finger_taps, 1)) + "\n")

        # hand is closed    
        if (left_position_closed != 0) and (left_angle > left_angle_open):
            left_position_closed = 0
            left_max_angle = 0
            left_tap_start = frametime            

    ###################################################
    # Right Hand
    #parse this         
    #RIGHT_HAND,WRIST,X,0.5899660587310791,Y,0.6407750248908997,Z,1.733735928155511e-07
    if "RIGHT_HAND,WRIST" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        right_wrist_x = float(split_x[3])
        right_wrist_y = float(split_x[5])
        right_wrist_z = float(split_x[7])
        #print(wrist_x,wrist_y,wrist_z)
    if "RIGHT_HAND,THUMBS_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        right_thumb_x = float(split_x[3])
        right_thumb_y = float(split_x[5])
        right_thumb_z = float(split_x[7])
        #print(thumb_x,thumb_y,thumb_z)
    if "RIGHT_HAND,INDEX_FINGER_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        right_index_x = float(split_x[3])
        right_index_y = float(split_x[5])
        right_index_z = float(split_x[7])
        #print(index_x,index_y,index_z)
        
        #index finger is last variable ... process data
        #calculate thumb and index finger vector
        #https://www.omnicalculator.com/math/angle-between-two-vectors
        #https://math.stackexchange.com/questions/361412/finding-the-angle-between-three-points
        
        right_thumb_x_v = right_thumb_x - right_wrist_x
        right_thumb_y_v = right_thumb_y - right_wrist_y
        right_thumb_z_v = right_thumb_z - right_wrist_z            
          
        right_index_x_v = right_index_x - right_wrist_x
        right_index_y_v = right_index_y - right_wrist_y
        right_index_z_v = right_index_z - right_wrist_z  
            
        right_thumb_len = math.sqrt(right_thumb_x_v * right_thumb_x_v + right_thumb_y_v * right_thumb_y_v + right_thumb_z_v * right_thumb_z_v) 
        right_index_len = math.sqrt(right_index_x_v * right_index_x_v + right_index_y_v * right_index_y_v + right_index_z_v * right_index_z_v)
           
        right_dot_prod = right_thumb_x_v * right_index_x_v + right_thumb_y_v * right_index_y_v + right_thumb_z_v * right_index_z_v
            
        right_angle = math.degrees(math.acos( right_dot_prod / (right_thumb_len * right_index_len)))        

        if (right_angle > right_max_angle):
            right_max_angle =  right_angle
            right_max_time = frametime

        #plot time and angle
        ax[1].scatter(frametime,right_angle)

        framediff = frametime - right_last_time
            
        right_last_time = frametime
        right_last_angle = right_angle
 
        #see if angle changes position to open or closed
        if (right_position_closed == 0) and (right_angle < right_angle_closed):
            right_position_closed = 1
            right_finger_taps = right_finger_taps + 1
            right_last_tap = right_tap_start
            right_tap_start = frametime
            right_tapdiff = right_tap_start - right_last_tap
            right_tapdiff_f = right_tapdiff.total_seconds()
            right_velocity = (2 *  right_max_angle) / right_tapdiff_f
            right_tapdiff =  right_max_time - right_last_tap
            right_velocity_up = right_max_angle / right_tapdiff.total_seconds()
            right_tapdiff =  right_tap_start - right_max_time
            right_velocity_down = right_max_angle / right_tapdiff.total_seconds()
            right_angle_sum = right_angle_sum + right_max_angle
            right_velocity_sum = right_velocity_sum + right_velocity            
            print('Right Hand Taps=' + str(right_finger_taps) + ' Time=' + str(right_tapdiff_f) + 
                  ' Max Angle=' + str(round(right_max_angle, 0)) + ' Velocity= ' + str(round(right_velocity, 1)) + 
                  ' Up Velocity= ' + str(round(right_velocity_up, 1)) + ' Down Velocity= ' + str(round(right_velocity_down, 1)) +
                  ' Avg Angle=' + str(round(right_angle_sum/right_finger_taps, 0)) + ' Avg Velocity= ' + str(round(right_velocity_sum/right_finger_taps, 1)))
            f.write('Right Hand Taps=' + str(right_finger_taps) + ' Time=' + str(right_tapdiff_f) + 
                  ' Max Angle=' + str(round(right_max_angle, 0)) + ' Velocity= ' + str(round(right_velocity, 1)) + 
                  ' Up Velocity= ' + str(round(right_velocity_up, 1)) + ' Down Velocity= ' + str(round(right_velocity_down, 1)) +  
                  ' Avg Angle=' + str(round(right_angle_sum/right_finger_taps, 0)) + ' Avg Velocity= ' + str(round(right_velocity_sum/right_finger_taps, 1)) + "\n")

        # hand opens                
        if (right_position_closed != 0) and (right_angle > right_angle_open):
            right_position_closed = 0
            right_max_angle = 0
            right_tap_start = frametime

plt.draw()
plt.pause(5)
plt.savefig('Holistic_Plot.png')
f.close()


