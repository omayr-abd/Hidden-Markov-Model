from sys import argv

filename1 = argv[1]
filename2 = argv[2]

hmm = open(filename1)

lines = hmm.readlines()


for i in range(len(lines)):
	lines[i] = lines[i].replace("\n","")
	lines[i] = lines[i].replace("\r","")
## Store the states:

states = lines[1].split(' ')
if states[-1] == '':
    del states[-1]


    
## Store the observations

words = lines[2].split(' ')



## Store matrix a
a = [ [0 for x in range(0,4)] for y in range(0,4)]
for i in range(4,8):
   a[i-4] = lines[i].split(' ')
for i in range(0,4):
    for j in range(0,4):
        a[i][j] = float(a[i][j])


   
## Store matrix b    
b = [ [0 for x in range(0,8)] for y in range(0,4)]
for i in range(9,13):
    b[i-9] = lines[i].split(' ')

for i in range(0,4):
   for j in range(0,8):
       b[i][j] = float(b[i][j])



## Store matrix c
pi = [0 for x in range(0,4)]
pi = lines[14].split(' ')
for i in range(len(pi)):
    pi[i] = float(pi[i])



#####################################################################
## Store observations as index number
txt2 = open(filename2)
obslines = txt2.readlines()
for i in range(len(obslines)):
	obslines[i] = obslines[i].replace("\n","")

numObs = int(obslines[0])


listObs = [None] * numObs
for i in range(numObs):
	listObs[i] = obslines[2 + i*2].split()
	


for i in range(len(listObs)):
    for j in range(len(listObs[i])):
        if listObs[i][j] == 'kids':
            listObs[i][j] =0
        if listObs[i][j] == 'robots':
            listObs[i][j] =1
        if listObs[i][j] == 'do':
            listObs[i][j] =2
        if listObs[i][j] == 'can':
            listObs[i][j] =3
        if listObs[i][j] == 'play':
             listObs[i][j] =4
        if listObs[i][j] == 'eat':
            listObs[i][j] =5
        if listObs[i][j] == 'chess':
            listObs[i][j] =6
        if listObs[i][j] == 'food':
            listObs[i][j] =7



########################################
# start forward algrithm

store = [0 for x in range(0,numObs)]
for k in range(numObs):
    ## initialization
    for i in range(0,len(a)):
        a00 = pi[0] * b[0][listObs[k][0]]
        a01 = pi[1] * b[1][listObs[k][0]]
        a02 = pi[2] * b[2][listObs[k][0]]
        a03 = pi[3] * b[3][listObs[k][0]]

    # induction
    N= [a00,a01,a02,a03]
    for t in range(len(listObs[0])-1 ):
        X = [0 for x in range(0,4)]
        for i in range(0,4):
            X[i] = b[i][listObs[k][t+1]]*(N[0]*a[0][i]+N[1]*a[1][i] + N[2]* a[2][i] +N[3]*a[3][i])
        N = X


    ## termination

    
    for i in range(len(N)):
        store[k] += N[i]

    




##############################################

#starting Vertibi Algorithm:

# initialization:

for k in range(numObs):
    for i in range(0,len(a)):
        a00 = pi[0] * b[0][listObs[k][0]]
        a01 = pi[1] * b[1][listObs[k][0]]
        a02 = pi[2] * b[2][listObs[k][0]]
        a03 = pi[3] * b[3][listObs[k][0]]

 # Recursion
    N= [a00,a01,a02,a03]

    fi = [[0 for x in range(0,4)] for y in range(len(listObs[k]))]
    for t in range(len(listObs[k])-1 ):
        X = [0 for x in range(0,4)]
        for i in range(0,4):
            X[i] = max(N[0]*a[0][i],N[1]*a[1][i],N[2]* a[2][i],N[3]*a[3][i])
            if N[0]*a[0][i]==N[1]*a[1][i]==N[2]* a[2][i] ==N[3]*a[3][i]:
                fi[t+1][i] = -1
            elif  X[i] == N[0]*a[0][i]:
                fi[t+1][i] = 0
            elif X[i] == N[1]*a[1][i]:
                fi[t+1][i] = 1
            elif X[i] == N[2]*a[2][i]:
                fi[t+1][i] = 2
            elif  X[i] == N[3]*a[3][i]:
                fi[t+1][i] = 3
          
            X[i] = X[i] * b[i][listObs[k][t+1]]
        N = X
    qt = max(N)
    if qt == N[0]:
        qt =0
    if qt ==N[1]:
        qt = 1
    if qt ==N[2]:
        qt = 2
    if qt == N[3]:
        qt = 3

##    BackTracking
    Q = [ 0 for x in range(0,len(listObs[k]))]
    Q[0] = qt
    P = [ 0 for x in range(0,len(listObs[k]))]
    for t in range(0,len(listObs[k])-1):
        Q[1]=fi[t+1][Q[0]]
    for i in range(len(Q)):
        P[i] =Q[len(Q)-i-1]

##   Print out the answer
    O = [ 0 for x in range(0,len(listObs[k]))]
    for i in range(len(O)):
        O[i] = states[P[i]]
    print store[k],
    for i in range(len(listObs[k])):
        if store[k] != 0:
            print O[i]+" ",
    print("")
        






    

















