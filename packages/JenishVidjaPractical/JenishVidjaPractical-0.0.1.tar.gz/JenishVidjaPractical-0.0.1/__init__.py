def practical4(prac4):
    return prac4

prac4 = ('''Hello!
            import pandas as pd
            import numpy as np
            df=pd.read_csv("C:\\Users\\hmnai\\6citytsp.csv",header=None)
            mat=df.to_numpy()
            v=[]
            x=int(input("STARTING POINT:-"))
            s=[]
            s.append(x)
            for i in range(6):
                 v.append(i)
            m=x
            path=0
            p=0
            for i in range(5):
             minp=np.inf
                 for j in v:
                     if j not in s:
                        if j!=m:
                             if mat[m][j]<=minp:
                 minp=mat[m][j]
                 p=j
                 s.append(p)
                 m=p
                path+=minp 
path+=mat[m][x]
print(path)
STARTING POINT:-4
1248
#Brute Force Approach
import pandas as pd
import numpy as np
from itertools import permutations
df=pd.read_csv("6citytsp.csv",header=None)
mat=df.to_numpy()
v=[]
s=0
for i in range(6):
 if i!=s:
 v.append(i)
next_per=permutations(v)
min_path=np.inf
for i in next_per:
 k=s
 cur_path=0
 for j in i:
 cur_path+=mat[k][j]
 k=j
 cur_path+=mat[k][s]
 min_path=min(min_path,cur_path)
print("CHEAPEST PATH:-",min_path)
''')
