import cv2
import numpy as np
import math
print('enter arithmetic code file path.......')
file_path = input()

print('enter limits  file path.......')
file_path2 = input()
print('enter image first dimension.....')
n = input()
n = int(n)

print('enter image second dimension.....')
m = input()
m = int(m)
tot = n*m
print('enter block size.....')
block_size = input()
block_size = int(block_size)
print('enter the encoding percision....')
percesion = input()
percesion = int(percesion)
whole = pow(2,percesion) # represent 1 in float
half = whole/2
quarter = whole/4

def getUpper(j):
    return limits[j+1]

# handle if blocksize not divible by n*m
additional = 0
if((n*m)%block_size != 0):
    if(n*m < block_size):
        block_size = n*m
    else:
        x = math.ceil(n*m/block_size)
        additional = x*block_size - n*m
arithmetic_code = np.load(file_path)
limits = np.load(file_path2)
# decodeing
decoded_arr = np.array([])
counter = 0 
rem = block_size - additional
decoded_arr = np.array([])
v = 0 # check if -1
R = tot # total number 
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
        


decoded_arr = np.reshape(decoded_arr,(n,m))
#save decoded image
cv2.imwrite('decoded.jpg', decoded_arr)