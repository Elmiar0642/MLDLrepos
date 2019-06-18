import os,math,random
A=[ord(os.urandom(1)) for x in range(5)]
print(A)
B=[a for a in A]
B.append(ord(os.urandom(1)))
print(B)
C=[]*0
for x,y in zip(A[:-1],A[1:]):
    C.append(y-x)
print(C)
CODE=[]*0
for y,z in zip(A[:-(len(A)//2)],A[1:]):
    CODES=[]*0
    for x in C:
        if(x<0):
            #print(y-x)
            if(y+x==z):
                CODES.append(1)
            else:
                CODES.append(0)
        else:
            #print(y+x)
            if(y+x==z):
                CODES.append(1)
            else:
                CODES.append(0)
    #print(CODES)
    CODE.append(CODES)
WEIGHT=[]*0
print(len(CODE))
for i in range(len(CODE)):
    WEIGHT.append(C)
print(WEIGHT)
for j in range(len(A)//2):
    CODE.append([random.randint(0,1) for x in range(len(C))])
print(CODE,"\n\n",len(C))
for x in range((len(C)//2)):
    for y,z in zip(CODE,WEIGHT):
        WEIGHT.append([random.choice(z)for g in range((len(C)//2)-1)]+[ord(os.urandom(1)) for g in range((len(C)//2)+1)])
print(len(WEIGHT),len(WEIGHT)/len(CODE))
for i in range(0,len(WEIGHT),4):
    print(WEIGHT[i:i+4],"\n\n")
    input()
    

