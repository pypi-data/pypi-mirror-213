#!/usr/bin/env python
# coding: utf-8

#%% [markdown]

# # Module for partitions

# In[1]:


# print("IMPORT PARTITIONS")

# from ast import arg
# from os import error


from sympy import Rational
from sympy import Matrix
from sympy import symbols
from sympy import factorial
# from numpy import array

import sys
sys.path.append("../")
# from mathutils import factorial

# In[2]:


if __name__=="__main__":
    x,x0,x1,x2,x3,x4,x5,x6=symbols('x,x0,x1,x2,x3,x4,x5,x6')


# In[3]:


"""
Module to deal with partitions.

class Partitions


"""


# In[ ]:





# In[4]:


def prod(L):
    """
    product of a list
    custom implementation
    that makes sure that the result will be in the same class as the elements of the list
    """
    if len(L)==0:
        return 1
    P=L[0]
    for x in L[1:]:
        P*=x
    return P

# In[5]:

# def wraptolist(f):
#     """
#     wrapper
#     wraps a function that takes list
#     into function that can take a tuple of arguments
    
#     ex:
#     f([1,2,3])
#     f2=wraptolist(f)
#     f2(1,2,3)
    
#     """
#     def newf(*args):
        
#         if len(args)==0:
#             x=[]
#         if len(args)==1:
#             if isinstance(args[0],list):
#                 x=args[0]
#             elif isinstance(args[0],tuple):
#                 x=list(args[0])
#             else:
#                 x=[args[0]]
#         else:
#             x=list(args)
#         return f(x)
#     return newf       




# In[1]:




# In[1]:

def complementset(E1,E2):       
    """complement of E1 in E2"""
    return [e for e in E2 if e not in E1]


def subsets(E,k="all"):  
    """
    list of all subsets of E of size k, 
    all subsets if k="all"
    """
    if k=="all": 
        EE=[]
        for l in range(1,len(E)+1): 
            EE+=subsets(E,l)
        return EE
    if len(E)<k:
        return []
    if len(E)==k:
        return [E]
    if k==0:
        return [[]]
    if k==1:
        return [[e] for e in E]
    EE=subsets(E[1:],k-1)
    return [[E[0]]+e for e in EE]+subsets(E[1:],k)



def orderedsubsets(E,k):  
    """
    list of decompositions of E into k subsets,
    possibly empty, 
    and ordered
    """
    
    if k==0:
        return []
    if E==[]:
        return [[[]]*k]
    L=[]
    EE=orderedsubsets(E[1:],k)
    #print("EE="+str(EE))
    for e in EE:
        #print("e="+str(e))
        for l in range(k):
            #print("l="+str(l)+" e[:1]="+str(e[:1])+" , "+ str([[E[0]]+e[l]])+" , "+str(e[l+1:])  )
            L+=[e[:l]+[[E[0]]+e[l]]+e[l+1:]]
    return L

def subsetsinto(E,k,allowempty=True):
    """
    decomposition of E into k subsets
    """
    if k==1:
        if len(E)==0:
            if allowempty:
                return [[[]]]
            else:
                return []
        else:
            return [[E]]
    start=0
    LL=[]
    if not allowempty:
        start=1
    for n in range(start,len(E)+1):
        for s in subsets(E,n):
            for p in subsetsinto(complementset(s,E),k-1,allowempty):
                LL+=[[s]+p]
    return LL
    

def partitions(E,k="all"): 
    """ 
    all partitions of E into k parts. 
    all partitions if k="all"
    """
    if E==[]:
        return []
    if k==1:
        return [[E]]        
    if k=="all":
        L=[]
        for l in range(1,len(E)+1):
            L+=partitions(E,l)
        return L
    def addtolist(L,s):  # ajoute s a tous les elements de la liste L
        return [[s]+l for l in L]            
    # cherche les sous ensembles de E[1:] (on enleve E[0]), et on rajoutte l'ensemble vide 
    EE=[[]]+subsets(E[1:])            
    L=[]  # liste des solutions, d'abbord vide, on va la remplir
    for e in EE:
        ec=complementset(e,E[1:])  # complementaire, on a donc E= e+E[0]  U  ec            
        Lp=partitions(ec,k-1)            
        L+=addtolist(Lp,[E[0]]+e)
    return L


def partint(g,k): 
    """
    partitions of the integer g into k parts
    """    
    if g<0: 
        return []
    if k==1:
        return [[g]]
    if g==0:
        return [[0]*k]
    L=[]
    for h in range(g+1):
        Eg=partint(g-h,k-1)
        L+=[[h]+e for e in Eg]
    return L 


def listdistr(L,n):  
    """
    returns all lists of lengths n, 
    with the elements of L
    """
    if n==1:
        return [[p] for p in L]
    if n==0: return [[]]
    LL=listdistr(L,n-1)
    Lf=[]
    for p in L:
        Lf+=[[p]+l for l in LL]
    return Lf
    


# In[4]:

infos="""


if __name__=="__main__":
    
    E=['a','b','c','d']
    
    print complementset([5,7],E)
    
    print "\n partint: \n"
    
    print partint(5,1)
    print partint(5,2)
    print partint(5,3)
    
    print "\n partitions: \n"
    
    print partitions(E,1)
    print partitions(E,2)
    print partitions(E,3)
    print partitions(E,4)
    print partitions(E,5)
    
    print "\n subsets: \n"
    
    print subsets(E,0)
    print subsets(E,1)
    print subsets(E,2)
    print subsets(E,3)
    print subsets(E,4)
    print subsets(E,5)


    print "\n ordered subsets: \n"
    
    print orderedsubsets([],3)
    print orderedsubsets(['A'],3)
    
    print
    
    E2=['O','X']
    
    print orderedsubsets(E2,0)
    print orderedsubsets(E2,1)
    print orderedsubsets(E2,2)
    print orderedsubsets(E2,3)
    print orderedsubsets(E2,4)
    
    
    print
    
    print listdistr(['a','b','c'],2)
    
"""


# In[ ]:





#%%

def permutations(E):
    """
    permutations(E) -> permutations(range(E))
    E can be integer
    or E = list
    """
    if isinstance(E,int):
        return permutations(list(range(E)))
    if len(E)==0:
        return []
    if len(E)==1:
        return [[E[0]]]
    L=[]
    Lp=permutations(E[:-1])
    for p in Lp:
        for i in range(len(E)):
            L+=[p[:i]+[E[-1]]+p[i:]]
    
    return L
        
        

# In[6]:


#permutations(['a','b','c'])


# In[7]:

#class Partition

########     ###    ########  ######## #### ######## ####  #######  ##    ## 
##     ##   ## ##   ##     ##    ##     ##     ##     ##  ##     ## ###   ## 
##     ##  ##   ##  ##     ##    ##     ##     ##     ##  ##     ## ####  ## 
########  ##     ## ########     ##     ##     ##     ##  ##     ## ## ## ## 
##        ######### ##   ##      ##     ##     ##     ##  ##     ## ##  #### 
##        ##     ## ##    ##     ##     ##     ##     ##  ##     ## ##   ### 
##        ##     ## ##     ##    ##    ####    ##    ####  #######  ##    ## 
class Partition:
    
    def __init__(self,*lp):
        if len(lp)==0:
            self.L=[]
        elif len(lp)==1:
            if isinstance(lp[0],Partition):
                self.L=lp[0].L
            elif isinstance(lp[0],list):
                self.L=lp[0]
            elif isinstance(lp[0],tuple):
                self.L=list(lp[0])
            else:
                self.L=[lp[0]]
        else:
            self.L=list(lp)
        self.reorder()
        
    def reorder(self):
        self.L=sorted(self.L,reverse=True)
        # self.L.sort()
        # self.L.reverse()
        
    def __repr__(self):
        return str(self.L)
        
    def __getitem__(self,n):
        # if isinstance(n,tuple):
        #     if len(n)==2:
        #         return 
        if n>=len(self.L):
            return 0
        else:
            return self.L[n]
        
    def __len__(self):
        self.reorder()
        return len([i for i in range(len(self.L)) if self.L[i]>0])
    
    @property
    def length(self):
        return len(self)

    @property
    def weight(self):
        return sum(self.L)

    def __abs__(self):
        return self.weight
    
    @property
    def nrows(self):
        self.reorder()
        L=[]
        for i in range(self[0]+1):
            L+=[len([j for j in self.L if j==i])]
        return L
    
    @property
    def T(self):
        if self.weight==0:
            return Partition([])
        # nr=self.nrows
        L=[]
        for i in range(self[0]):
            L+=[len([j for j in self.L if j>i])]
        return Partition(L)
    
    @property
    def z(self):
        nr=self.nrows
        return prod([factorial(x) for x in nr])
        
    def Ferrer(self,*args,**kargs):
        args=list(args)
        if "french" in args:
            convention="french"
            args.remove("french")
        elif "english" in args:
            convention="english"
            args.remove("english")
        elif "russian" in args:
            convention="russian"
            args.remove("russian") 
        elif "convention" in kargs:
                convention=kargs["convention"]
        else:
            convention="english"
            
        if len(args)>0:
            if isinstance(args[0],str):
                c=args[0]
        else:
            c="\u258a"
            
        if convention=="russian":
            return self.Ferrerrussian()
        
        # convention="english",c="\u258a"): 
        # convention="french","english","russian"
        self.reorder()
        s=""
        lmax=self[0]
        for i in range(self.length):
            si=""
            for j in range(self[i]):
                si+=c
            for j in range(lmax-self[i]):
                si+=" "
            if convention=="english":
                s+=si+"\n"
            elif convention=="french":
                s=si+"\n"+s
        return s
    
    def __contains__(self,box):
        i,j=box
        if j<0 or j>self.length:
            return False
        if i<=0:
            return False
        if i>self[j]:
            return False
        return True
    
    def boxes(self):
        L=[]
        for j in range(self.length):
            for i in range(1,self[j]+1):
                L+=[(i,j)]
        return L
            
    def __gt__(self,autre):  # dominance
        S1,S2=0,0
        for i in range(max([self.length,autre.length])):
            S1+=self[i]
            S2+=autre[i]
            if S1<S2:
                return False
        return self != autre

    def __ge__(self,autre):  
        if self==autre:
            return True
        return self>autre

    def __le__(self,autre): 
        return autre>=self

    def __lt__(self,autre):  
        return autre>self

    def H(self,n=0):
        if n==0:
            N=len(self.L)
        else:
            if n<len(self.L):
                raise ValueError("")
            N=n
        return [self[i]-i+N-1 for i in range(N)]
    
    @property
    def dim(self):
        self.reorder()
        if self.weight<=1:
            return 1
        H=self.H()
        d=factorial(self.weight)
        for i in range(len(H)-1):
            for j in range(i+1,len(H)):
                d*=(H[i]-H[j])
        for i in range(len(H)):
            d*=Rational(1,factorial(H[i]))
        return d
        
    def particuleholes(self,p="p",h="h"):
        L=[]
        previous=0
        for j in range(self.length-1,-1,-1):
            for i in range(self[j]-previous):
                L+=[h]
            previous=self[j]
            L+=[p]
        part=[i for i,x in enumerate(L) if x==p]
        holes=[i for i,x in enumerate(L) if x==h]
        return part,holes

    def drawparticuleholes(self,p="\u25cf",h="\u25cb"):
        part,holes=self.particuleholes()
        L={}
        for a in part:
            L[a]=p
        for a in holes:
            L[a]=h
        s=""
        for i in range(len(part)+len(holes)):
            s+=L[i]
        return s

    def Msym(self,Lx,normalized=True):
        if len(Lx)<len(self):
            raise ValueError("Msym: data must have length larger to equal to the partition")
        M=0
        for sigma in permutations(Lx):
            M+=prod([sigma[i]**(self[i]) for i in range(len(Lx))])
        if normalized:
            z=Rational(1,self.z)
        else:z=1
        return M*z
    
    
    def schur(self,Lx):
        if len(Lx)<len(self):
            raise ValueError("Msym: data must have length larger to equal to the partition")
        H=self.H(len(Lx))
        M=Matrix([[x**(H[i]) for i in range(len(Lx))]for x in Lx])
        return det(M)
        
    
    def Psym(self,Lx):
        return prod([sum([x**self[i] for x in Lx]) for i in range(len(self))])

    def Esym(self,Lx):
        def e(k,Lx):
            if k==0: return 1
            if k==1: return sum(Lx)
            if len(Lx)<k:
                return 0
            return Lx[0]*e(k-1,Lx[1:])+e(k,Lx[1:])
        # return [ e(self[i],Lx) for i in range(len(self))]
        return prod([ e(self[i],Lx) for i in range(len(self))])

    def heights(self):
        part,holes=self.particuleholes()
        L={a:-1 for a in part}
        for a in holes:
            L[a]=1
        heights=[len(part)-1]
        for i in range(len(part)+len(holes)):
            heights+=[heights[-1]+L[i]]
        return heights



    def Ferrerrussian(self):
        h=self.heights()
        hmax=max(h)

        hlow=[self.length-i-1 for i in range(self.length)]+[i-self.length-1 for i in range(self.length,len(h))]
        #print(hlow)

        table=[]
        for j in range(hmax+2):
            tablej=[]
            for i in range(len(h)-1):
                tablej+=[" "]
            table+=[tablej]
        for i in range(len(h)-1):
            if h[i+1]-h[i]==1:
                table[h[i+1]+1][i]="/"  #"\u25e2"
                #table[h[i+1]+1][i]="\u25e2"
            elif h[i+1]-h[i]==-1:
                table[h[i]+1][i]="\\"  #"\u25e3"
                #table[h[i]+1][i]="\u25e3"
        for i in range(len(hlow)-1):
            if hlow[i+1]-hlow[i]==1:
                table[hlow[i+1]+1][i]="/"  #"\u25e4"
                #table[hlow[i+1]+1][i]="\u25e4"
            elif hlow[i+1]-hlow[i]==-1:
                table[hlow[i]+1][i]="\\"  #"\u25e5"
                #table[hlow[i]+1][i]="\u25e5"
        #for i in range(1,len(h)-2):
        #    for j in range(hlow[i]+2,h[i]):
        #        table[j+1][i-1]="O"


        s=""
        for j in range(len(table)-1,0,-1):
            for i in range(len(h)-1):
                s+=table[j][i]
            s+="\n"
        return s        

    def __iter__(self):
        return PartitionIter(self)

    def rows(self):
        return PartitionIter(self)
    
    def columns(self):
        return PartitionIter(self.T)

    def __eq__(self,autre):
        for k in range(max(len(self),len(autre))):
            if self[k]!=autre[k]:
                return False
        return True

    def __neq__(self,autre):
        return not self==autre

    def __iadd__(self,autre):
        p=Partition(autre)
        self.L+=p.L
        self.reorder()
        return self

    def __add__(self,autre):
        A=Partition(self)
        A+=autre
        return A

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def partitions(E,k=-1):
        # print(f"partitions {k} of ",E)
        if isinstance(E,int):
            return Partition.partitions(list(range(E)),k)
        if k==-1:
            L=[]
            for i in range(1,len(E)+1):
                L+=Partition.partitions(E,i)
            return L
        if k==0:
            return []
        if len(E)<k:
            return []
        if k==1:
            return [[E]]
        L=[]
        L1=Partition.partitions(E[1:],k-1)
        for p in L1:
            # print(p, " --> ",[[E[0]]]+p)
            L+=[[[E[0]]]+p]
        L1=Partition.partitions(E[1:],k)
        for p in L1:
            for i in range(k):
                newp=[[E[0]]+p[i]]
                for j in range(k):
                    # print(f"   p[{j}]  = ",p[j])
                    if j!=i:
                        newp+=[p[j]]
                # print(p,i, " --> ",newp)
                L+=[newp]
        return L

    @staticmethod
    def partitionsOfWeight(n,lmax="default",maxrow=-1,lessthan=-1):
        if n<0:
            return []
        if lmax=="default":
            lmax=n
        if isinstance(lessthan,int):
            if lessthan==-1:
                if maxrow>=0:
                    Lt=[maxrow]*lmax
                else:
                    Lt=[n]*lmax
            else:
                Lt=[lessthan]*lmax
        else:
            Lt=[l for l in lessthan]
            while len(Lt)<lmax:
                Lt+=[0]
        if maxrow==-1:
            maxrow=Lt[0]

        if n==0:
            return [Partition([])]
        if lmax<=0:
            return []
        if n==1:
            if Lt[0]>=1:
                return [Partition([1])]
            else:
                return []
        L=[]
        for k in range(1,min([Lt[0],maxrow])+1):
            try:
                newLt=[Lt[0]+Lt[1]-k]+Lt[2:]
            except:
                newLt=[Lt[0]-k]
            for i in range(1,len(newLt)):
                if newLt[i]>maxrow or newLt[i]>k:
                    newLt[i]=min(k,maxrow)
            Lk=Partition.partitionsOfWeight(n-k,lmax=lmax-1,maxrow=k,lessthan=newLt)
            for p in Lk:
                L+=[p+Partition([k])]
        return L

    def enumerate(self):
        return PartitionEnumIter(self)

    def clean(self):
        self.L = [l for l in self if l!=0]

class PartitionIter:
    def __init__(self,P):
        self.P=P
        self.n=-1
    def __iter__(self):
        self.n=-1
        return self
    def __next__(self):
        self.n+=1
        if self.n>=len(self.P):
            raise StopIteration
        return self.P.L[self.n]

class PartitionEnumIter:
    def __init__(self,P):
        self.P=P
        self.n=-1
    def __iter__(self):
        self.n=-1
        return self
    def __next__(self):
        self.n+=1
        if self.n>=len(self.P):
            raise StopIteration
        return self.n,self.P.L[self.n]

# In[8]:

#%%

class BoxPartition:

    def __init__(self,P,x,y,content="default"):
        self.P=P
        self.x=x
        self.y=y
        if content=="default":
            self.content=self.x-self.y
        else:
            self.content=content

    def __repr__(self):
        return f" ({self.x},{self.y})"

    @property
    def arm(self):
        return self.P[y]-self.x

    @property
    def leg(self):
        return self.P.T[x]-self.y 

    def hook(self):
        return self.arm+self.leg+1




#%%



def allpartitions(n,rowmax="default"): 
    # n = weight = number of boxes
    if rowmax=="default":
        rowmax=n
    if n==0:
        return [Partition([])]
    if n==1:
        if rowmax>=1:
            return [Partition([1])]
        else:
            return []
    LL=[]
    for i in range(1,min(n,rowmax)+1):
        L=allpartitions(n-i,i)
        LL+=[ Partition([i]+p.L) for p in L]
    return LL
        
    
    
    


# In[ ]:





# In[9]:


if __name__=="__main__":
    mu=Partition([2,2])
    



    print(mu)

    print(mu.H())

    print(mu.dim)

    print(mu.Ferrer())
    print(mu.Ferrer("french"))
    print(mu.Ferrer("russian"))

    print(mu.T)

    print(len(mu))
    print(mu.length)
    print(mu.weight)

    print(mu.boxes())

    print((3,4) in mu)

    print((1,1) in mu)

    print(mu.nrows)

    print(mu.z)

    print(mu.Msym([x1,x2,x3]))

    nu=Partition([1,3])
    print(nu.Ferrer())



    print(nu.dim)

    print(nu.T.Ferrer())

    print(nu.T.Ferrer("o"))

    print(nu.T.Ferrer("french"))
    print(nu.T.Ferrer("o","french"))
    print(nu.Ferrer("russian"))

    print(nu>mu)

    print(Partition([7,3]).dim)
    print(Partition([7,3,0,0]).dim)

    print(Partition([8,8,6,4,4,2,1,0,0]).Ferrer())

    print(Partition([8,8,6,4,4,2,1,0,0]).Ferrer(convention="french"))


# In[10]:


if __name__=="__main__":
    nu=Partition([8,8,6,4,4,2,1,0,0])
    print(nu.H())

    print(nu.T.H())

    print([nu.H()[0]-x for x in nu.T.H()])

    print(nu.particuleholes())

    print(nu.drawparticuleholes())

    print(nu.drawparticuleholes("/","\\"))

    


# In[11]:


if __name__=="__main__":
    nu=Partition([3,1])
    print(nu.Ferrer("french"))
    print(nu.drawparticuleholes())
    print(nu.drawparticuleholes("x","."))
    print(nu.particuleholes())


    print(nu.Ferrer("french"))
    print(nu.drawparticuleholes())
    print(nu.heights())

    print(nu.Ferrer("russian"))


# In[12]:


class TableauSS(Partition):
    
    def __init__(self,lp):
        if isinstance(lp,Partition):
            lp=lp.L
        Partition.__init__(self,lp)
        self.table=[]*self.length
        for j in range(self.length):
            tj=[]
            for i in range(self[j]):
                tj+=[1]
            self.table+=[tj]
        
    def Young(self):
        s=""
        for line in self.table:
            for v in line:
                s+=" [{:2d}]".format(v)
            s+="\n"
        return s
            


# In[13]:


if __name__=="__main__":
    print("\u24aa")
    print("\u24c4")
    print("\u2460")
    print("\u2461")
    print("\u2462")
    print("\u246a")
    print("\u246b")
    print("\u2470")
    print("\u2473")



# In[14]:


if __name__=="__main__":
    T1=TableauSS([3,2,1])
    print(T1.Young())


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




