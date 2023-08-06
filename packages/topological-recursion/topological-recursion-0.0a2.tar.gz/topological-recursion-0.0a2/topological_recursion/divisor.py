# coding: utf-8

from . import partitions as part


class Divisor:
    """
    Divisor({point:weight})

    """
    
    def __init__(self,D={}):  # un dict 
        if isinstance(D,Divisor):
            self.D=D.D
        elif isinstance(D,dict):
            self.D=D
        else:
            self.D={D:1}
        
    def __repr__(self):
        if len(self.D)==0:
            return "0"
        s=""
        debut=True
        for p in self.D:
            a=self.D[p]
            if a<0:
                s+=str(a)+"."+str(p)
            elif a>0 and debut:
                s+=str(a)+"."+str(p)
            elif a>0 and not debut:
                s+="+"+str(a)+"."+str(p)
            debut=False
        return s
    
    def __getitem__(self,p):
        if p in self.D:
            return self.D[p]
        else:
            return 0
        
    def cleanzeros(self):
        for p in self.D:
            if self[p]==0:
                del self.D[p]
        
    def __len__(self):
        return len(self.D)
    
    @property
    def degree(self):
        return sum([self.D[p] for p in self.D])
    
    @property
    def pts(self):
        return [k for k in self.D.keys()]

    @property
    def supp(self):
        return self.pts

    def copy(self):
        DD={p:self.D[p] for p in self.D}
        return Divisor(DD)
        
    def __iadd__(self,autre):
        if autre==0:
            return self
        for p in autre.D:
            if p in self.D:
                self.D[p]+=autre[p]
            else:
                self.D[p]=autre[p]
        return self

    def __add__(self,autre):
        DD=self.copy()
        DD+=autre
        return DD

    def __imul__(self,autre):
        for p in self.D:
            self.D[p]*=autre
        return self
    
    def __mul__(self,autre):
        DD=self.copy()
        DD*=autre
        return DD

    def __rmul__(self,autre):
        return self*autre

    def __isub__(self,autre):
        if autre==0:
            return self
        return self.__iadd__(-autre)
    def __sub__(self,autre):
        if autre==0:
            return self.copy()
        return self.__add__(-autre)

    def __neg__(self):
        DD=self.copy()
        DD*=-1
        return DD
    
    def iszero(self):
        for p in self.D:
            if self[p]!=0:
                return False
        return True

    def __eq__(self,autre):
        if isinstance(autre,int) or isinstance(autre,float):
            if autre==0:
                return self.iszero()
            else:
                return False
        if isinstance(autre,Divisor):
            return (self-autre).iszero()
        raise ValueError

    def __neq__(self,autre):
        return not self==autre

    def ispositive(self):
        for p in self.D:
            if self[p]<0:
                return False
        return True

    def __ge__(self,autre):
        return (self-autre).ispositive()
    def __gt__(self,autre):
        return self>=autre and self!=autre
    def __le__(self,autre):
        return (autre-self).ispositive()
    def __lt__(self,autre):
        return self<=autre and self!=autre

    def mapto(self,f,n=1):
        """
        ???
        """
        L=part.listdistr(self.pts,n)
        S=0
        for l in L:
            S+=part.product([self.D[k] for k in l])*f(*l)
        return S

    def __iter__(self):
        return DivisorIter(self)
            
            
class DivisorIter:
    def __init__(self,D):
        self.D=D
        self.n=-1
    def __iter__(self):
        self.n=-1
        return self
    def __next__(self):
        self.n+=1
        if self.n>=len(self.D):
            raise StopIteration
        return self.D.supp[self.n]
        
# %%

# %%


if __name__=="__main__":
    print("\nDemo : Divisor\n")
    
    print("*  D=Divisor({'a':1,'b':2})")
    D=Divisor({'a':1,'b':2})
    print("*  print(D)")
    print(D)
    print("*  -D")
    print(-D)
    print("*  2*D")
    print(2*D)
    print("*  len(D)")
    print(len(D))
    print("*  D.supp    ( = support)")
    print(D.supp)
    print("*  D.degree   ( = degrees )")
    print(D.degree)
    print("*  D>=0")
    print(D>=0)
    print("*  D>0")
    print(D>0)
    print("*  D==0")
    print(D==0)
    print("*  D!=0")
    print(D!=0)

    print("*  for p in D:print(p,D[p])")
    for p in D:
        print("*    print(p,D[p])")
        print(p,D[p])
        
# %%
