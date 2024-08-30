from datetime import datetime   
from matplotlib import pyplot as plt
import math


#open file and read into list
f = open('hands_output.txt', 'r')
filelines = f.readlines()
#print(filelines)

# python plot
printcount = 0
plt.ion()
plt.show()
plt.xlabel("Time")
plt.ylabel("Angle")

#parse out the file, only looking for time, and x,y,z coordinates for wrist, thumb,index
for x in filelines:
    if "frame" in x:
        #print(x)
        timestr = x.split(' ')[2]
        #print(timestr)
        t1 = datetime.strptime(timestr, "%H:%M:%S-%f ")
        #print('time:', t1.time())
    if "WRIST" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        wrist_x = float(split_x[2])
        wrist_y = float(split_x[4])
        wrist_z = float(split_x[6])
        #print(wrist_x,wrist_y,wrist_z)
    if "THUMBS_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        thumb_x = float(split_x[2])
        thumb_y = float(split_x[4])
        thumb_z = float(split_x[6])
        #print(thumb_x,thumb_y,thumb_z)
    if "INDEX_FINGER_TIP" in x:
        #print(x)
        split_x = x.split(',')
        #print(split_x)
        index_x = float(split_x[2])
        index_y = float(split_x[4])
        index_z = float(split_x[6])
        #print(index_x,index_y,index_z)
        
        #index finger is last variable ... process data
        #calculate thumb and index finger vector
        #https://www.omnicalculator.com/math/angle-between-two-vectors
        #https://math.stackexchange.com/questions/361412/finding-the-angle-between-three-points
        
        thumb_x_v = thumb_x - wrist_x
        thumb_y_v = thumb_y - wrist_y
        thumb_z_v = thumb_z - wrist_z            
          
        index_x_v = index_x - wrist_x
        index_y_v = index_y - wrist_y
        index_z_v = index_z - wrist_z  
            
        thumb_len = math.sqrt(thumb_x_v * thumb_x_v + thumb_y_v * thumb_y_v + thumb_z_v * thumb_z_v) 
        index_len = math.sqrt(index_x_v * index_x_v + index_y_v * index_y_v + index_z_v * index_z_v)
           
        dot_prod = thumb_x_v * index_x_v + thumb_y_v * index_y_v + thumb_z_v * index_z_v
            
        angle = math.degrees(math.acos( dot_prod / (thumb_len * index_len)))        

        #plot time and angle
        plt.scatter(t1,angle)
            
        #displaying on screen slows down system, don't print every frame
        printcount = printcount + 1
        if ((printcount % 10) == 0):        
            plt.draw()
            plt.pause(0.0001)


plt.draw()
plt.pause(1)
plt.savefig('plot.png')
f.close()


