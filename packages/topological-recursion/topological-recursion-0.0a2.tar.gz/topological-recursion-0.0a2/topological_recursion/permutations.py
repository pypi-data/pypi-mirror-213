

#%%

#%%

# from itertools import permutations
from operator import truediv
# from numpy import array as nparray
from numpy import zeros as npzeros
#%%

def wraptolist(f):
    """allows to call a function that would only take lists, to take also tupples"""
    def newf(*LL):
        if len(LL)==0:
            return f([])
        if len(LL)==1:
            if isinstance(LL[0],list):
                return f(LL[0])
            elif isinstance(LL[0],tuple):
                return f(list(LL[0]))
            else:
                return f([LL[0]])
        else:
            return f(list(LL))
    return newf

@wraptolist
def ppcm(L):
    """lowest common multiple"""
    if len(L)==0:
        return 1
    elif len(L)==1:
        return L[0]
    elif len(L)==2:
        return int(L[0]*L[1]/pgcd(L))
    else:
        return ppcm([ppcm(L[:1])]+L[2:])

@wraptolist
def pgcd(L):
    """largest common divisor"""
    if len(L)==0:
        return 1
    elif len(L)==1:
        return L[0]
    elif len(L)==2:
        if L[1]==1 or L[0]==1: return 1
        if L[1]==0:
            return L[0]
        if L[0]==0:
            return L[1]
        if L[1]==L[0]:
            return L[0]
        if L[1]>L[0]:
            r=L[1]% L[0]
            return pgcd(r,L[0])
        if L[0]>L[1]:
            r=L[0]% L[1]
            return pgcd(r,L[1])
    else:
        return pgcd([pgcd(L[:1])]+L[2:])
    

    


#%%
class Permutation:

    def __init__(self,*D,**kargs):
        if len(D)==0:
            raise ValueError
        if isinstance(D[0],Permutation):
            self.D={k:D[0][k] for k in D[0].keys()}
        elif isinstance(D[0],dict):
            self.D=D[0]
        elif isinstance(D[0],int): # Id(D[0])
            self.D={n:n for n in range(D[0])}
        elif isinstance(D[0],list):
            self.D={}
            for Di in D:
                self.D.update(Permutation.fromlist(Di))
        else:
            raise ValueError
        self.reprOptions={}
        if 'sep' in kargs:
            self.reprOptions['sep']=kargs['sep']
        else:
            self.reprOptions['sep']=" , "
    
    @staticmethod
    def fromlist(L):
        n=len(L)
        if n==0:
            return {}
        D={L[i-1]:L[i] for i in range(1,n)}
        D[L[n-1]]=L[0]
        return D


    def __len__(self):
        return len(self.D)

    def keys(self):
        return self.D.keys()

    @property
    def dict(self):
        return {a:self[a] for a in self.keys()}
    
    def __repr__(self):
        s=""
        for k in self.keys():
            if len(s)>0:
                s+=self.reprOptions['sep']
            s+=f"{k} -> {self.D[k]} "
        return "Permutation( "+s+" )"
    

    def __mul__(self,autre):
        a=Permutation(autre)
        for k in a.keys():
            a[k]=self[autre[k]]
        return a

    def __getitem__(self,k):
        return self.D[k]
    
    def __setitem__(self,k,v):
        self.D[k]=v

    def inv(self):
        return Permutation({self[k]:k for k in self.keys()})


    def inverse(self):
        return self.inv()

    def isId(self):
        for k in self.keys():
            if self[k]!=k:
                return False
        return True

    def _isperm(self):
        L=[]
        for k in self.keys():
            if self[k] not in L:
                L+=[self[k]]
        return len(L)==len(self)


    def __eq__(self, autre) -> bool:
        if isinstance(autre,int):
            if autre==1:
                return self.isId()
            else:
                raise ValueError
        return (autre*self.inv()).isId()
    
    def __call__(self,k):
        try:
            if k in self.keys():
                return self[k]
        except:
            pass
        try:
            if isinstance(k,int) and k>=0 and k<len(self):
                return self[list(self.keys())[k]]
        except:
            pass
        if isinstance(k,list):
            if self.subset(k):
                return [self[e] for e in k]
            if len(k)!=len(self):
                raise ValueError
            I=self.indices()
            return [k[I[i]] for i in range(len(self))]
        raise IndexError

    def subset(self,E):
        """tells if self can permute the elements of E """
        for e in E:
            if e not in self.keys():
                return False
        return True


    def cycles(self):
        def isinL(x,L):
            for LL in L:
                if x in LL:
                    return True
            return False
        L=[]
        for k in self.keys():
            if not isinL(k,L):
                LL=[]
                x=k
                while x not in LL:
                    LL+=[x]
                    x=self[x]
                L+=[LL]
        return [Permutation(LL) for LL in L]

    def conjugationClass(self):
        L=self.cycles()
        mu = [len(LL) for LL in L]
        return list(reversed(sorted(mu)))

    def conjugacyClass(self):
        return self.conjugationClass()

    def __pow__(self,n):
        if n==0:
            return Permutation({k:k for k in self.keys()})
        if n==1:
            return Permutation(self)
        if n<0:
            return (self.inv()).__pow__(-n)
        return self.__pow__(n-1)*self

    def indices(self):
        n=len(self)
        L=list(self.keys())
        newP={}
        for i,x in enumerate(L):
            j=L.index(self[x])
            newP[i]=j
        return Permutation(newP)

    def order(self):
        return ppcm(self.conjugacyClass())

    def matrix(self):
        n=len(self)
        PI=self.indices()
        M=npzeros(n*n,dtype=int).reshape((n,n))
        for i in PI.keys():
            M[i,PI[i]]=1
        return M

    @property
    def sign(self):
        c=self.conjugationClass()
        if (sum(c)-len(c))%2==0:
            return 1
        else:
            return -1

    def hasFixedPoint(self):
        for k in self.keys():
            if self[k]==k:
                return True
        return False


    @staticmethod
    def permutations(E,**kargs):
        L=allPermutations(E,**kargs)
        return [Permutation(p) for p in L]

    @staticmethod
    def Id(n):
        return Permutation({i:i for i in range(n)})

    @staticmethod
    def transposition(a,b,E=[]):
        if isinstance(E,int):
            E=range(E)
        if len(E)<2:
            E=[a,b]
        D={x:x for x in E}
        D[a]=b
        D[b]=a
        return Permutation(D)
    
    def __iter__(self):
        return PermutationIter(self)

class PermutationIter:
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
        return self.P[self.n]


#%%


def allPermutations(n,fixed=True):
    """
    allPermutations(n: int) -> list of all permutations of [0,...,n-1] 
    allPermutations(n: list) -> list of all permutations of L
    allPermutations(n, fixed=False) -> only permutations without fixed points
    """
    if isinstance(n,list):
        L=allPermutations(len(n),fixed)
        return [{n[k]:n[p[k]] for k in range(len(n))} for p in L]
    if not isinstance(n,int):
        raise TypeError
    if n<0:
        raise ValueError
    if n==0:
        return []
    if n==1:
        if fixed:
            return [{0:0}]
        else:
            return []
    L1=allPermutations(n-1,fixed=True)
    def hasfixedpt(d):
        for k in d:
            if d[k]==k:
                return True
        return False
    L=[]
    if fixed:
        for p in L1:
            newp={k:p[k] for k in p}
            newp.update({n-1:n-1})
            L+=[newp]


    for e in range(n-1):
        for p in L1:
            newp={k:p[k] for k in p}
            newp.update({n-1:p[e],e:n-1})
            if fixed or not hasfixedpt(newp):
                L+=[newp]
    return L

def cyclicPermutations(n):
    if isinstance(n,list):
        return [{n[i]:n[p[i]] for i in p} for p in cyclicPermutations(list(range(len(E))))]
    L1=allPermutations(n-1,fixed=True)
    L=[]
    for p in L1:
        v=list(p.values())+[n-1]
        L+=[Permutation(v).dict]
    return L



def subsets(E,size=-1,empty=True):
    """
    subsets(E) -> all subsets of E, including []
    subsets(E,empty=False) -> all subsets of E, except empty set
    subsets(E,n) -> all subsets of E of size n
    """
    if size<0:
        L=[]
        for s in range(len(E)+1):
            Ls=subsets(E,s,empty)
            for e in Ls:
                L+=[e]
        return L
    if size==0:
        if empty:
            return [[]]
        else:
            return []
    if size>len(E):
        return []
    if size==1:
        return [[e] for e in E]
    if size==len(E):
        return [E]
    L=subsets(E[:-1],size,True)
    L1=subsets(E[:-1],size-1,True)
    for p in L1:
        L+=[p+[E[-1]]]
    return L

    

# %%

if __name__=="__main__":
    a=Permutation({1:2,2:3,3:1})
    print("a = ",a)
    print("a**2 = ",a**2)
    print("a**3 = ",a**3)
    print("a**3 == 1  --> ",a**3==1)
    print("a.inv() = ",a.inv())

    b=Permutation([1,3],[2])
    print("b = ",b)
    print("a*b = ",a*b)
    print("b.cycles() = ")
    for k in b.cycles():
        print(k)
    print()
    print("a.conjugationClass() = ",a.conjugationClass())
    print("b.conjugationClass() = ",b.conjugationClass())


# %%
# %%
