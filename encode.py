import cv2
import numpy as np
import math
print('enter image path.....')
file_path = input()
img = cv2.imread(file_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print('enter block size.....')
block_size = input()
block_size = int(block_size)

n = img.shape[0]
m = img.shape[1]
arr_flattend = np.reshape(img,n*m)

    
#print(arr_flattend)
def getUpper(j):
    return limits[j+1]

#integer encoding
print('enter the percision not more than 63 as most cpus cant handle more than 64 bits.....')
percesion = input()
percesion = int(percesion)
whole = pow(2,percesion) # represent 1 in float
half = whole/2
quarter = whole/4
#get frequency of colors from 0 - 255
freq_arr = np.zeros((256,),dtype=np.longdouble)
tot = n*m
for i in range(tot):
    freq_arr[ arr_flattend[i] ] += 1
#print(freq_arr)    
  

   

# get limits
limits = np.array([0],dtype=np.longdouble)
for i in range(1,257):
    limits = np.append(limits,limits[i-1]+freq_arr[i-1])
#print(limits)

# handle if blocksize not divible by n*m
additional = 0
if((n*m)%block_size != 0):
    if(n*m < block_size):
        block_size = n*m
    else:
        x = math.ceil(n*m/block_size)
        additional = x*block_size - n*m

# add additional values as -1
for i in range(additional):
    arr_flattend = np.append(arr_flattend,-1)    

# arithmetic code each block in flattened array
count = 0
arithmetic_code = np.array([])
loop_times = int((n*m+additional)/block_size)
v = 0 # check if -1
R = tot # total number 
for i in range(loop_times): 
    a = 0 # loweer bound
    b = whole # upper bound   
    if v == 1:
        break
    binary = np.array([],dtype=int)
    s = 0
    for j in range(block_size):      
        if(arr_flattend[count] == -1):    
            v=1
            break
        w = b-a
        pixel = arr_flattend[count]
        b = a + round(w*getUpper(pixel)/R)
        a = a + round(w*limits[pixel]/R)
        # if count < 4:
        #     print('a,b')
        #     print(a,b)
        count += 1 
        while b < half or a >= half:
            if b < half:
                binary = np.append(binary,0)
                for x in range(s):                   
                    binary = np.append(binary,1)
                s = 0
                a = 2*a
                b = 2*b
            elif a >= half:
                binary = np.append(binary,1)
                for x in range(s):                    
                    binary = np.append(binary,0)
                s = 0
                a = 2*(a-half)
                b = 2*(b-half)
        while a >= quarter and b < 3*quarter:
            s = s + 1
            a = 2*(a-quarter)
            b = 2*(b-quarter)
        # if  i ==0:    
        #     print('new a,new b')
        #     print(a,b)
        #     print('new binary')
        #     print(binary)
        #     print('\n')
    s = s + 1
    if a <= quarter:
        binary = np.append(binary,0)
        for x in range(s):            
            binary = np.append(binary,1)
    else :
        binary = np.append(binary,1)
        for x in range(s):
            binary = np.append(binary,0)
    code = 0
    # if j == 0 and i ==0:
    #     print('binary')
    #     print(binary)
    for x in range( binary.size ):
        if binary[x] == 1:
            code += pow(2, percesion-x-1)
    arithmetic_code = np.append(arithmetic_code,code) 
#save arithmetic coding 
np.save('code.npy', arithmetic_code)
np.save('limits.npy', limits)