import numpy as np
import time
surface = np.array([[0,0,1,1,1],[2,1,2,1,1],[2,1,1,2,1],[0,1,1,1,0],[0,0,2,2,0]])

def makeSurf(N):
    surf=np.zeros(N*N)
    surf[0:N*N-3*N+2] = 1
    surf[N*N-3*N+2:N*N-7]=2
    surf=np.random.permutation(surf)
    surf=np.reshape(surf,(N,N))
    return surf

###Simple implementation###
### Test ###
    
def check_Ag_O_config(i,j,array):
    E=0
    if i==size-1:
        i=-1
    if j==size-1:
        j=-1
    
    if array[i-1,j-1]==1 and array[i-1,j]==1 and array[i,j+1]!=1 and array[i+1,j+1]==1 and array[i+1,j]==1 and array[i,j-1]!=1:
        E-=4
    if array[i-1,j]==1 and array[i,j+1]==1 and array[i+1,j+1]!=1 and array[i+1,j]==1 and array[i,j-1]==1 and array[i-1,j-1]!=1:
        E-=4
    if array[i,j+1]==1 and array[i+1,j+1]==1 and array[i+1,j]!=1 and array[i,j-1]==1 and array[i-1,j-1]==1 and array[i-1,j]!=1:
        E-=4
    return E    

def check_Ag_triangle(i,j,array):
    E=0
    if i==size-1:
        i=-1
    if j==size-1:
        j=-1
    if array[i-1,j-1]==1 and array[i-1,j]==1:
        E-=1
    if array[i-1,j]==1 and array[i,j+1]==1:
        E-=1
    if array[i,j+1]==1 and array[i+1,j+1]==1:
        E-=1
    if array[i+1,j+1]==1 and array[i+1,j]==1:
        E-=1
    if array[i+1,j]==1 and array[i,j-1]==1:
        E-=1
    if array[i,j-1]==1 and array[i-1,j-1]==1:
        E-=1
    return E

def check_O_triangle(i,j,array):
    E=0
    if i==size-1:
        i=-1
    if j==size-1:
        j=-1
    if array[i-1,j-1]==2 and array[i-1,j]==2:
        E+=1
    if array[i-1,j]==2 and array[i,j+1]==2:
        E+=1
    if array[i,j+1]==2 and array[i+1,j+1]==2:
        E+=1
    if array[i+1,j+1]==2 and array[i+1,j]==2:
        E+=1
    if array[i+1,j]==2 and array[i,j-1]==2:
        E+=1
    if array[i,j-1]==2 and array[i-1,j-1]==2:
        E+=1
    return E
def calcEnergy(size,surf):
    E=0
    for i in range(size):
        for j in range(size):
            if surface[i,j]==1:
                E+=check_Ag_triangle(i,j,surface)
            if surface[i,j]==2:
                E+=check_Ag_O_config(i,j,surface)
                E+=check_O_triangle(i,j,surface)
    return E

def calcEnergyOptim(myboard):
    myboard_right_neighbor = np.roll(myboard,-1,axis=1)
    myboard_left_neighbor = np.roll(myboard,1,axis=1)
    myboard_upper_right_neighbor = np.roll(myboard,1,axis=0)
    myboard_lower_left_neighbor = np.roll(myboard,-1,axis=0)
    myboard_upper_left_neighbor = np.roll(myboard_left_neighbor,1,axis=0)
    myboard_lower_right_neighbor = np.roll(myboard_right_neighbor,-1,axis=0)

    # Ag triangles
    e1 = -3 * sum(sum((myboard == 1) * (myboard_right_neighbor == 1) * (myboard_upper_right_neighbor == 1)))
    e2 = -3 * sum(sum((myboard == 1) * (myboard_right_neighbor == 1) * (myboard_lower_right_neighbor == 1)))

    # O triangles
    e3 =  3 * sum(sum((myboard == 2) * (myboard_right_neighbor == 2) * (myboard_upper_right_neighbor == 2)))
    e4 =  3 * sum(sum((myboard == 2) * (myboard_right_neighbor == 2) * (myboard_lower_right_neighbor == 2)))

    # O in perfect 4 Ag setup
    e5 =  -4 * sum(sum((myboard == 2) * (myboard_right_neighbor == 1) * (myboard_upper_right_neighbor == 1) * (myboard_upper_left_neighbor != 1) * (myboard_left_neighbor == 1) * (myboard_lower_left_neighbor == 1) * (myboard_lower_right_neighbor != 1) ))
    e6 =  -4 * sum(sum((myboard == 2) * (myboard_right_neighbor != 1) * (myboard_upper_right_neighbor == 1) * (myboard_upper_left_neighbor == 1) * (myboard_left_neighbor != 1) * (myboard_lower_left_neighbor == 1) * (myboard_lower_right_neighbor == 1) ))
    e7 =  -4 * sum(sum((myboard == 2) * (myboard_right_neighbor == 1) * (myboard_upper_right_neighbor != 1) * (myboard_upper_left_neighbor == 1) * (myboard_left_neighbor == 1) * (myboard_lower_left_neighbor != 1) * (myboard_lower_right_neighbor == 1) ))

    return e1+e2+e3+e4+e5+e6+e7

size = 5
t1=0
t2=0
for n in range(1000):
    surface = makeSurf(size)
    t_start=time.time()
    E_nonoptim=calcEnergy(size,surface)
    t_inter=time.time()
    E_optim=calcEnergyOptim(surface)
    t_end=time.time()
    t1+=t_inter-t_start
    t2+=t_end-t_inter

t1=t1/1000
t2=t2/1000

print("time (nonoptimized):",t1)
print("time (optimized):",t2)
