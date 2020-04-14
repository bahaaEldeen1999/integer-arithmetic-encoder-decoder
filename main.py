import cv2
import numpy as np
import math
import matplotlib.pyplot as plt


img = cv2.imread('img1.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
block_size = 16
#cv2.imshow( "Display window", img );    
#cv2.waitKey(0)
#print(img.shape)
n = img.shape[0]
m = img.shape[1]
print(n,m)
arr_flattend = np.reshape(img,n*m)

    


#get frequency of colors from 0 - 255
fact = 1
freq_arr = np.zeros((256,),dtype=np.longdouble)
tot = n*m*fact
for i in range(n*m):
    freq_arr[ arr_flattend[i] ] += (1*fact)

#print(freq_arr)
#normalize frequencies

# for i in range(256):
#     freq_arr[i] /= (tot)
   

# get limits
limits = np.array([0],dtype=np.longdouble)
for i in range(1,257):
    limits = np.append(limits,limits[i-1]+freq_arr[i-1])
# handle 0 probs
def getUpper(j):
    # nexty = j+1
    # while(nexty<257 and limits[j] == limits[nexty]):
    #     nexty+=1
    # if(nexty < 257 ):
    #     return limits[nexty]
    # else:
    #     return limits[nexty-1]
    return limits[j+1]

#integer encoding
# for i in range(1,limits.size):
#     print('pixel '+ str(i) + ' upper limit '+str(limits[i]) + ' in frequency '+str(freq_arr[i-1]))

percesion = 50
whole = pow(2,percesion) # represent 1 in float
half = whole/2
quarter = whole/4
print(whole,half,quarter)
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
# mapping limits to match percision
# max_limit = limits[limits.size-1]
# for i in range(limits.size):
#     limits[i] = (limits[i]*whole)/max_limit

# print('scaled limits')
# print(limits)
# arithmetic code each block in flattened array
arithmetic_code = np.array([])
loop_times = int((n*m+additional)/block_size)
print('additional')
print(additional)
print('loop times')
print(loop_times)

count = 0

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
    


# print('limits')
# print(limits)


# print('arithmetic code')
# print(arithmetic_code)
      

counter = 0 
rem = block_size - additional
decoded_arr = np.array([])
#print('################################')
# arithmetic decoding integer
for k in arithmetic_code:
    #print(k)
    z = k
    a = 0
    b = whole
    rng = block_size
    if(counter == arithmetic_code.size - 1 ):
        rng = rem
    counter += 1
    for i in range(rng):
        f = 0
        # try all possibilities
        # if  k == arithmetic_code[0]:
        #     print('prev a, pev b')
        #     print(a,b)
        for j in range(256):
            if(limits[j] == 0 and limits[j+1] == 0):
                continue
            w = b-a
            b_t = a + round(w*getUpper(j)/R)
            a_t = a + round(w*limits[j]/R)
            
            if z >= a_t and z < b_t:
                #if k == arithmetic_code[0]:
                    # print('z')
                    # print(z)
                    # print('a_t , b_t')
                    # print(a_t,b_t)
                    # print('j')
                    # print(j)
                    # print('\n')
                    # print('lower limit , upper limit')
                    # print(limits[j],getUpper(j))
                decoded_arr = np.append(decoded_arr,j)
                a = a_t
                b = b_t
                f=1
                break
        # if f == 0:
        #     print('not decoded')
        #     print('z')
        #     print(z)
        #     print('a,b')
        #     print(a,b)
        while b<half or a>=half:
            if b<half:
                a=2*a
                b=2*b
                z=2*z
            elif a >= half:
                a = 2*(a-half)
                b = 2*(b-half)
                z = 2*(z-half)
        while a>=quarter and b <3*quarter:
            a = 2*(a-quarter)
            b = 2*(b-quarter)
            z = 2*(z-quarter)
        

print(decoded_arr)
print(arr_flattend)
decoded_arr = np.reshape(decoded_arr,(n,m))
plt.figure(1)
plt.imshow(np.reshape(np.reshape(img,n*m),(n,m)),cmap='gray')

plt.figure(2)
plt.imshow(decoded_arr,cmap='gray')
plt.show()














# print(limits)
# def getUpper(j):
#     nexty = j+1
#     while(nexty<257 and limits[j] == limits[nexty]):
#         nexty+=1
#     if(nexty < 257 ):
#         return limits[nexty]
#     else:
#         return limits[nexty-1]


# # handle if blocksize not divible by n*m
# additional = 0
# if((n*m)%block_size != 0):
#     if(n*m < block_size):
#         block_size = n*m
#     else:
#         x = math.ceil(n*m/block_size)
#         additional = x*block_size - n*m

# # add additional values as -1
# for i in range(additional):
#     arr_flattend = np.append(arr_flattend,-1)    

# # arithmetic code each block in flattened array
# arithmetic_code = np.array([])
# loop_times = int((n*m+additional)/block_size)
# print('loop times')
# print(loop_times)

# count = 0
# b = 0
# for i in range(loop_times):
#     L = 0
#     U = 0
#     if b == 1:
#         break
#     for j in range(block_size):
#         if(arr_flattend[count] == -1):
#             b=1
#             break
#         if(j == 0):           
#             L = limits[arr_flattend[count]]
#             U = getUpper(arr_flattend[count])
#         else:
#             L_n_1 = L
#             U_n_1 = U
#             L = L_n_1 + (U_n_1-L_n_1)*(limits[arr_flattend[count]]/tot)
#             U = L_n_1 + (U_n_1-L_n_1)*(getUpper(arr_flattend[count])/tot)
#         count += 1 
#     Tx = (U+L)/2
#     arithmetic_code = np.append(arithmetic_code,Tx)   

# print(arithmetic_code)
# # decodeing
# decoded_arr = np.array([])
# rem = block_size - additional
# counter = 0 
# d = 0
# for k in arithmetic_code: 
#     tag = k
#     L = -1
#     U = -1
#     #print('tag')
#     #print(tag)
#     rng = block_size
#     if(counter == arithmetic_code.size - 1 ):
#         rng = rem
#     counter += 1
#     for i in range(rng):
#         for j in range(256):
#             if L == -1 and U == -1:
#                 if( (limits[j] <= tag) and (getUpper(j) > tag) ):
#                     L = limits[j]
#                     U = getUpper(j)
#                     decoded_arr = np.append(decoded_arr,j)
#                     break
#             else:
#                 L_n_1 = L
#                 U_n_1 = U
#                 L_P = L_n_1 + (U_n_1-L_n_1)*(limits[j]/tot)
#                 U_P = L_n_1 + (U_n_1-L_n_1)*( getUpper(j)/tot)
#                 if( (L_P <= tag) and (U_P > tag) ):
#                     L = L_P
#                     U = U_P
#                     decoded_arr = np.append(decoded_arr,j)
#                     break
#     #print('L , U')
#     #print(L,U)
# print(decoded_arr)
# #for i in range(decoded_arr.size):
#     #if( decoded_arr[i] != arr_flattend[i] ):
#         # print('NOOOO')
#         # print(decoded_arr[i] , arr_flattend[i])
#     #print(decoded_arr[i],arr_flattend[i])
# print('d ')
# print(d)

# decoded_arr = np.reshape(decoded_arr,(n,m))

# # cv2.imshow( "original", img );  
# # cv2.imshow("decoded",decoded_arr)  
# # cv2.waitKey(0)
# plt.figure(1)
# plt.imshow(np.reshape(np.reshape(img,n*m),(n,m)),cmap='gray')

# plt.figure(2)
# plt.imshow(decoded_arr,cmap='gray')
# plt.show()