from .partitions import *
from .divisor import Divisor

from sympy import symbols,Symbol
# from sympy import init_printing

from pickle import load as pickleload
from pickle import dump as pickledump

from sympy import *



dbfactorial = factorial2
half = Rational(1,2)
hbar = Symbol('hbar')



def prod(L):
    # redefine the product, otherwise doesn't work for certain classes instances
    if len(L)==0:
        return 1
    if len(L)==1:
        return L[0]
    p=L[0]
    for x in L[1:]:
        p*=x
    return p





# def parts2(D):
#     # splits D into 2 parts in all possible ways
#     if len(D)==0:
#         return [[[],[]]]
#     if len(D)==1:
#         return [[D,[]],[[],D]]
#     D1=parts2(D[1:])
#     L=[]
#     for p in D1:
#         L+=[[[D[0]]+p[0],p[1]],[p[0],[D[0]]+p[1]]]
#     return L

#%%

class IntersectionNumber:
    r"""
    IN=IntersectionNumber([load=True],[autosave=True],[filename="default"])
    load = True : reloads from the saved file
    autosave = True : writes into the file, each time a new intersection number is computed
    filename = if we eant to give another file than the default

    Usage:
    IN(3,[3,3,2,2])  -> Rational

    (method of computation: string equations + Euler + cut&join)

    IN.known() -> dict by genus of those that are known
                    g: maximal n

    IN.tau(3,[3,3,2,2]) -> expression with Tau symbols
        -> tau3**2 \tau2**2 

    IN.latex(3,[3,3,2,2]) -> string LaTeX
        -> "\left<\tau{3}^{2}\tau{2}^{2}\right>_{3}"                

    """
    def __init__(self,load=True,autosave=True,filename="default"):
        
        self.L={0:{(0,0,0):1}}
        if load:
            if filename=="default":
                import os
                self.filename = os.path.join(os.path.dirname(__file__),"intersectionnumbersall.p")
            else:
                self.filename=filename
        self.autosave=autosave
        if load:
            self.load()

    def __repr__(self):
        s="IntersectionNumbers, "
        s+=f"already known up to genus g={max([g for g in self.L])}, n={max([max([len(k) for k in self.L[g]]) for g in self.L])}"
        return s
        
    def load(self,filename="default"):
        if filename=="default":
            filename=self.filename
        ## print(f"Will load from {filename}")
        with open(filename, "rb" ) as file:
            L= pickleload(file )
            self.L=L
            file.close()

    def save(self,filename="default"):
        if filename=="default":
            filename=self.filename
        with open(filename, "wb" ) as file:
            pickledump( self.L, file )

        
    @staticmethod
    def shift(D,i):
        DD=[d for d in D]
        DD[i]+=-1
        return DD
        
    def setin(self,g,L,r):
        if isinstance(L,Partition):
            D=L.L
        else:
            D=list(L)
        DD=tuple(D)
        if g not in self.L:
            self.L[g]={}
        self.L[g][DD]=r
        if self.autosave:
            self.save()
        return r
        
    def __call__(self,g,L):
        if isinstance(L,Partition):
            D=L.L
        else:
            D=list(L)

        if len(D)==0: return 0
        if 3*g-3+len(D)!=sum(D): return 0

        D.sort()  # orders them
        
        for d in D:  # return 0 if some d is <0 or is not integer
            if int(d)!=d: return 0
            if d<0:
                return 0
            
        if g in self.L:
            if tuple(D) in self.L[g]:
                return self.L[g][tuple(D)]

            
        
        if g==0:  # case genus 0
            return self.setin(g,D,self.genus0(*D))
        if g==1:  # case genus 1
            if len(D)==1:
                if D[0]==1:
                    return Rational(1,24)
                else: return 0
        
        if D[0]==0:
            DD=D[1:]
            return self.setin(g,D,sum([self(g,IntersectionNumber.shift(DD,i)) for i in range(len(DD))]))
        
        if D[0]==1:
            return self.setin(g,D,self(g,D[1:])*(2*g-3+len(D)))
            
        # now all D[i]>=2
        S=0
        for a in range(D[0]-1):  # terms (g-1,n+1)
            b=D[0]-a-2
            S+=dbfactorial(2*a+1)*dbfactorial(2*b+1)*Rational(1,2)*self(g-1,[a,b]+D[1:])
            
        if len(D)>1:  # terms (0,2)+(g,n)
            for i in range(1,len(D)):
                S+=dbfactorial(2*D[i]+2*D[0]-1)*Rational(1,dbfactorial(2*D[i]-1))*self(g,[D[i]+D[0]-1]+D[1:i]+D[i+1:])
        
        LP=IntersectionNumber.parts2(D[1:])  # terms (h,I)+(g-h,J)
        for IJ in LP:
            I=IJ[0]
            J=IJ[1]
            for h in range(1,g):
                a=3*h-3+1+len(I)-sum(I)
                b=3*(g-h)-3+1+len(J)-sum(J)
                S+=dbfactorial(2*a+1)*dbfactorial(2*b+1)*self(h,[a]+I)*self(g-h,[b]+J)*Rational(1,2)                                                                    
        
        return self.setin(g,D,S*Rational(1,dbfactorial(2*D[0]+1)))
        



        
    def genus0(self,*D):
        n=len(D)
        if sum(D)!=n-3: return 0
        
        p=factorial(n-3)
        for d in D:
            p=Rational(p,factorial(d))
        return p


    @staticmethod
    def parts2(D):
        if len(D)==0:
            return [[[],[]]]
        if len(D)==1:
            return [[D,[]],[[],D]]
        D1=IntersectionNumber.parts2(D[1:])
        L=[]
        for p in D1:
            L+=[[[D[0]]+p[0],p[1]],[p[0],[D[0]]+p[1]]]
        return L
    
    def known(self):
        D={g:max([len(k) for k in self.L[g]]) for g in self.L}
        return D


    def tau(self,g,L):
        return INTau(g,L).symbol()

    def latex(self,g,L):
        return INTau(g,L).latex()


def INwithTimes(g,L,t={}):
    r"""
    t must be a dictionary, or any object with a method __getitem__() and a method __contains__().
    In other words, one can do t[k]  and      
    t[k] -> value  (int, float, complex, symbol, expression,...)
    k in t -> True or False
    
    """
    n=len(L)
    assert 2*g-2+n>0
    mmax=3*g-3+n-sum(L)
    if mmax<0:
        return 0
    Lt={}
    for k in range(mmax+1):
        if 2*k+3 in t:
            if t[2*k+3]!=0:
                Lt.update({2*k+3:t[2*k+3]})
    # print("Lt = ",Lt)
    if len(Lt)==0:
        return Rational(1,2**(2*g-2+n))*IN(g,L)
    assert 1 not in Lt
    if 3 in Lt:
        t3=Lt[3]
        # Lt={k:Lt[k] for k in Lt if k!=3}
        return 2**(2*g-2+n)*(2-t3)**(2-2*g-n)*INwithTimes(g,L,t={k:2*Lt[k]/(2-t3) for k in Lt if k!=3})        
    # assert 3 not in Lt
    A=0
    for m in range(mmax+1):
        # print(mmax,m)
        if m>0:
            LLk=partint(mmax,m)
        else:
            LLk=[[]]
        for Lk in LLk:
            # print("Lk=",Lk)
            Ltt=1
            try:
                for k in Lk:
                    Ltt*=Rational(dbfactorial(2*k+1),1)*Lt[2*k+3]
                    
            except:
                Ltt=0
            # print("Ltt=",Ltt)
            if Ltt!=0:        
                r = IN(g,L+[k+1 for k in Lk])
                # print(r)
                if r!=0:
                    r*=prod([dbfactorial(2*d-1) for d in L])
                    r*=Rational(1,factorial(m)*2**m)
                    r*=Ltt
                    A+=r
    A*=Rational(1,2**(2*g-2+n))
    return A

#%%
            
            
def Fgn(g,Lz,t={}):
    r"""
    g =  genus = positive integer
    Lz = [z1,z2,...,zn]
    each zi is either a value, or a symbol, or a divisor 
    example:
    Fgn(0,[z,z,z,z],t={5:t5})
    
    zz=Divisor({z:1,z2:-1})
    Fgn(0,[zz,zz,zz,zz],t={5:t5})
    
    """
    n=len(Lz)
    for i,z in enumerate(Lz):
        if isinstance(z,Divisor) or isinstance(z,dict):            
            S=0
            for p in z:
                S+=z[p]*Fgn(g,Lz[:i]+[p]+Lz[i+1:],t=t)
            return S
    S=0
    for d in range(3*g-3+n+1):
        for L in partint(d,n):
            S+=INwithTimes(g,L,t=t)*prod([Lz[i]**(-(2*L[i]+1)) for i in range(n)])
    return S    
    



# %%

# def Schi(chi,z,t={}):
#     assert chi>0
#     S=0
#     for g in range(int((chi-1)/2)+2):
#         n=chi-2*g+2
#         assert n>0
#         S+=Fgn(g,[z]*n,t=t)*Rational(1,factorial(n))
#     return S

# def Schi(chi,z,t={}):
#     assert chi>0
#     S=0
#     for g in range(int((chi-1)/2)+2):
#         n=chi-2*g+2
#         assert n>0
#         S=0
#         for d in range(3*g-3+n+1):
#             # print(g,n,d)
#             Ld=partint(d,n)
#             # print(Ld)
#             S+=sum([INwithTimes(g,L,t=t) for L in Ld])*z**(-(2*d+n))*Rational(1,factorial(n))
#     return S

# #%%

# def S1chi(chi,z,t={}):
#     assert chi>0
#     S=0
#     for g in range(int((chi-1)/2)+2):
#         n=chi-2*g+2
#         assert n>0
#         S=0
#         for d in range(3*g-3+n+1):
#             # print(g,n,d)
#             if n>1:
#                 Ld=partint(d,n-1)
#             else:
#                 if d==0:
#                     Ld=[[]]
#                 else:
#                     Ld=[]
#             # print(Ld)
#             # for L in Ld:
#                 # print(L+[0])                
#             S+=sum([INwithTimes(g,L+[0],t=t) for L in Ld])*z**(-(2*d+n-1))*Rational(1,factorial(n-1))
#     return -S




#%%

class INTau:
    r"""
    class to display intersection numbers in Witten's notation    
    
    INTau(4,[4,3,2]) ->     tau2*tau3*tau4

    INTau(4,[4,3,2],output="latex) ->     \left<\tau{4}\tau{3}\tau{2}\right>_{4}
    INTau(4,[4,3,2],mode="latex) ->     \left<\tau{4}\tau{3}\tau{2}\right>_{4}

    INTau.mode = "symbol" or "latex"    
    """
    
    
    mode="symbol"

    def __init__(self,g,L,**kargs):
        self.g=g
        if isinstance(L,Partition):
            self.L=L.L
        else:
            self.L=L
        self.mode="symbol"
        if 'mode' in kargs:
            if kargs['mode'].lower() in ['symbol','latex']:
                self.mode=kargs['mode']
        elif 'output' in kargs:
            if kargs['output'].lower() in ['symbol','latex']:
                self.mode=kargs['output']
        # self.mode="latex"

    def __repr__(self):
        if self.mode=="latex":
            return self.latex()

        else:
            return str(self.symbol())

    def latex(self):
        s=r"\left<"
        D=self.asdict()
        for l in D:
            p=D[l]
            if p==1:
                s+=r"\tau{"+str(l)+"}"
            elif p>1:
                s+=r"\tau{"+str(l)+"}^{"+str(p)+"}"
            else:
                pass
        
        s+=r"\right>_{"+str(self.g)+"}"
        return s

    def symbol(self):
        r=1
        D=self.asdict()
        for d in D:
            r*=Symbol("tau"+str(d))**(D[d])
        return r


    def asdict(self):
        D={}
        for l in self.L:
            if l in D:
                D[l]+=1
            else:
                D[l]=1
        return D
    
    def __dict__(self):
        return self.asdict()


#%%


# def matrixD1(order=2,t={}):
#     z=Symbol('z')
#     # y=Lambda((z),z-half*sum([t[k]*z**(k-2) for k in t]))
#     r=Lambda((z),z+sum([S1chi(chi,z,t=t)*hbar**chi  for chi in range(1,order)])+O(hbar**(order)))
#     rm=series(r(z)-r(-z),hbar,0,order)
#     s=expand(series(1/rm,hbar,0,order))
#     # return rm,s
#     A=series((r(z)+r(-z))*s,hbar,0,order)
#     C=series(-2*r(z)*r(-z)*s,hbar,0,order)
#     D= Matrix([[-A,2*s],[C,A]])
#     return D


# def matrixD(order,y=lambda z:z,t={}):
#     assert callable(y),"y must be a function"
#     z=Symbol('z')
#     # x=Symbol('x')
#     """
#     must use:
#     y = Lambda((z),z - 1/2 \sum_k t_k z^{k-2})
    
#     """
#     dd1=matrixD1(order,t=t)
#     dd0=[]
#     for i in range(2):
#         dd0i=[]
#         for j in range(2):
#             d1=dd1[i,j].removeO()
#             d=series(d1*y(z),z,0,0).removeO()
#             r=expand(d1*y(z)-d)
#             dd0i+=[r+O(hbar**order)]
#         dd0+=[dd0i]
#     return Matrix(dd0)


    
# %%


# class MirzakhaniTimes:
    
#     def __init__(self):
#         self.pi=Symbol('pi')
#         pass
    
#     def __getitem__(self,k):
#         if k==3:
#             return 0
#         if k%2==0:
#             return 0
#         if k<3:
#             return 0
#         return Rational(2**(k-2)*(-1)**(int((k+1)/2)),factorial(k-2))*self.pi**(k-3)
    
#     def __contains__(self,k):
#         return k%2==1 and k>=3
    
    
# %%

######## ########  ####    ###    ##        ######
   ##    ##     ##  ##    ## ##   ##       ##    ##
   ##    ##     ##  ##   ##   ##  ##       ##
   ##    ########   ##  ##     ## ##        ######
   ##    ##   ##    ##  ######### ##             ##
   ##    ##    ##   ##  ##     ## ##       ##    ##
   ##    ##     ## #### ##     ## ########  ######

#%%

try:
    import os
    filename = os.path.join(os.path.dirname(__file__),"intersectionnumbers.p")
    IN=IntersectionNumber(filename=filename)
    ## print(f" Successfully loaded known IN ( IntersectionNumber() )  from {filename}\n")
except:
    IN=IntersectionNumber(load=False,autosave=False)
    ## print(" *** could not load the file ")
    ## print(" Successfully created a new empty IN ( IntersectionNumber() )\n")
    
# %%

# %%


if __name__=="__main__":
    z,z0,z1,z2,z3,z4,z5,z6,z7,z8,z9=symbols("z,z0,z1,z2,z3,z4,z5,z6,z7,z8,z9")
    t3,t5,t7,t8,t9,t11=symbols("t3,t5,t7,t8,t9,t11")
    tt={5:t5,7:t7,9:t9}

# if __name__=="__main__":
#     tM=MirzakhaniTimes()
    
    
    

#%%

if __name__=="__main__":
    print("Examples of use:\n")
    print()
    
    print("Type:")
    print('print(f" < {INTau(g,L)} >_{g} = {IN(g,L)} ") ')
    print()
        
    g,L=0,[2,1,0,0,0,0]
    print(f" g,L = {g},{L}  -->")
    print(f" < {INTau(g,L)} >_{g} = {IN(g,L)} \n")

    g,L=1,[2,1,0]
    print(f" g,L = {g},{L}  -->")
    print(f" < {INTau(g,L)} >_{g} = {IN(g,L)} \n")

    g,L=2,[4,1,1]
    print(f" g,L = {g},{L}  -->")
    print(f" < {INTau(g,L)} >_{g} = {IN(g,L)} \n")


# %%
