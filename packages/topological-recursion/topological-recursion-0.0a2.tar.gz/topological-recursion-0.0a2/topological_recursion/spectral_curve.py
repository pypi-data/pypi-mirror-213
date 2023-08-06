r"""
Spectral curves with 1 branch point

The general form of such spectral curve

.. MATH::

    x = z^2+x0
    y = z - 1/2 \sum_k t_{2k+3} z^{2k+1} 
    B = dz1 dz2 / (z1-z2)**2

where the input data is either Times t_k or function y(z)
"""

import numbers
from sympy import *

from .partitions import partint
from .intersection_numbers import INwithTimes


half = Rational(1,2)

def is_integer(n):
    try:
        return int(n)==n
    except:
        return False

def is_number(n):
    if isinstance(n,int) or isinstance(n,float) or isinstance(n,complex):
        return True
    return False


# %%

class SpCurveTimes:
    """
    Class for times usable by SpCurves
    
    Use subclasses of this class
    
    Any subclass must have:
    - a __getitem__() method 
    - a __contains__() method    
    - a property t
    - a method y()

    """

    name="Times"
    
    
    def __init__(self):
        pass
        # self.initialize(*args,**kargs)        

    def initialize(self,*args,**kargs):
        raise NotImplemented(" ** must use a subclass")
    
    def __repr__(self):
        s=self.__class__.name+"()"
        return s
    
    @staticmethod
    def MirzakhaniTimes():
        return MirzakhaniTimes()

    @staticmethod
    def Mirzakhani():
        return MirzakhaniTimes()
    
    @staticmethod
    def WeilPetersson():
        return MirzakhaniTimes()

    @staticmethod
    def WP():
        return MirzakhaniTimes()
    
    @staticmethod
    def from_formula(*args,**kargs):
        """
        argument : f: function k -> t[k]
        
        example:
        t = SpCurveTimes.from_formula(lambda k: factorial(k))
        t[4] -> 24
        
        """
        return TimesfromFormula(*args,**kargs)

    @staticmethod
    def from_Dict(*args,**kargs):         
        """
        argument : dict
        
        example:
        t = SpCurveTimes.from_Dict({3:8,5:7})
        t[3] -> 8
        t[5] -> 7
        9 in t -> False
        
        """
        return TimesfromDict(*args,**kargs)

    @staticmethod
    def from_y(*args,**kargs):         
        """
        argument : function y(z)
        
        example:
        t = SpCurveTimes.from_y(lambda z: 3*z - z**3)
        t[3] -> -4
        t[5] -> 2
        9 in t -> False
        
        """
        return Timesfromy(*args,**kargs)


#%%


class Timesdict(SpCurveTimes):
    """
    subclass of SpCurveTimes.
    Class for times usable by SpCurves
    
    Use subclasses of this class
    
    Any subclass must have:
    - a property t
    - a method y()

    optional: redefining
    - the __getitem__() method 
    - the __contains__() method    

    """

    def __init__(self, *args, **kargs):
        super().__init__()


    def __getitem__(self,k):
        if k in self.t:
            return self.t[k]
        else:
            return 0
    
    def __repr__(self):
        return self.__class__.name+"("+str(self.t)+")"

    def update(self,D):
        self.t.update(D)
        
    def __setitem__(self,k,v):
        self.update({k:v})
    
    def __contains__(self,k):
        return k in self.t

    def keys(self):
        return self.t.keys()
    def values(self):
        return self.t.values()
    def items(self):
        return self.t.items()

    def __iter__(self):
        return iter(self.t)

    def __len__(self):
        return len(self.t)
    
#%%

class TimesfromDict(Timesdict):
    """
    Class for times usable by SpCurves
    subclass of SpCurveTimes.Timesdict

    t is a dict
        
    """    
    def __init__(self, s={}, **kargs):
        super().__init__()
        self.initialize(s)
    
    def initialize(self,s):
        assert isinstance(s,dict) or isinstance(s,Timesdict)
        self.t={k:s[k] for k in s}
        self.y=self.createy()
            
    def createy(self):
        z=Symbol('z')
        return Lambda((z),z-half*sum([self.t[k]*z**(k-2) for k in self.t]))






#%%

class Timesfromy(Timesdict):
    """
    Class for times usable by SpCurves
    subclass of SpCurveTimes.Timesdict

    y is a function (callable)
        
    """    

    def __init__(self, y):
        super().__init__()
        self.initialize(y)
        
    def initialize(self,*args,**kargs):
        if len(args)==1:
            assert callable(args[0])
            self.y=args[0]
            self.t=self.createt()
        elif len(args)>1:
            raise ValueError
        else:
            z=Symbol('z')
            self.y=Lambda((z),z)
            self.t={}

    def createt(self):
        z=Symbol('z')
        p=Poly(self.y(z),z)
        lM=p.all_monoms()
        lc=p.all_coeffs()
        t={3:2}
        for i in range(len(lM)):
            if lc[i]!=0:
                k=lM[i][0]+2
                t.update({k:-2*lc[i]})
                if k==3:
                    t[k]+=2
        if 3 in t:
            if t[3]==0:
                del t[3]
        
        return t
        
        

    # def __getitem__(self,k):
    #     if k in self.t:
    #         return self.t[k]
    #     else:
    #         return 0

    # def __contains__(self,k):
    #     return (k in self.t and self[k]!=0)

#%%


class TimesfromFormula(Timesdict):
    
    def __init__(self, f,y=None):
        super().__init__()
        self.initialize(f,y)
    
    def initialize(self,f,y=None):
        assert callable(f)
        self.formula=f
        try:
            assert callable(y)
            self.y=y
        except:
            def fy(z):
                return " y not defined for this family of times "
                # raise NotImplementedError(" y not defined for this family of times ")                
            self.y = fy

    def __repr__(self):
        s=self.__class__.name
        try:
            n=Symbol('n')
            t=self.formula(n)
            sf=f"( formula n -> {t} )"
        except:
            sf=f"( formula n -> function(n) )"
        s+=sf
        return s

    def __getitem__(self,k):
        assert is_integer(k) and k>=0
        return self.formula(k)
    
    def __contains__(self,k):
        return is_integer(k) and k>=0
    
    
        
#%%

def Times(t={}):
    if isinstance(t,dict):
        return TimesfromDict(t)
    if callable(t):
        try:
            z=Symbol('z')
            p=Poly(self.y(z),z)
            return Timesfromy(t)
        except:
            raise NotImplementedError(" not yet ready. TODO: implement times from a series of z")
    if isinstance(t,Timesdict):
        return t.__class__(t.t)
    if isinstance(t,str):
        if t in SpCurveTimes.__dict__:
            return getattr(SpCurveTimes,t)()
        
    raise TypeError



#%%

def convertKappaTimesToTimes(t):
    r"""
    recall that
    $$ e^{\sum_k \hat t_k \kappa_k} = e^{\frac12 \sum_k t_{2k+1} (2k-1)!! \tau_k } $$
    with the relation
    $$ e^{-\sum_k \hat t_k u^{-k}} = 1 - \frac12 \sum_k (2k+1)!! t_{2k+3} u^{-k} $$
    """
    def f(k):
        if k%2==0:
            return 0
        if k<=3:
            return 0
        kk=int((k-3)/2)        
        S=0
        for mu in  allpartitions(kk):
            S+=prod([-t[mui] for mui in mu])*Rational(1,mu.z)
        S*=Rational(-2,dbfactorial(2*kk+1))
        return S
    return TimesfromFormula(f)

def convertTimesToKappaTimes(t):
    r"""
    recall that
    $$ e^{\sum_k \hat t_k \kappa_k} = e^{\frac12 \sum_k t_{2k+1} (2k-1)!! \tau_k } $$
    with the relation
    $$ e^{-\sum_k \hat t_k u^{-k}} = 1 - \frac12 \sum_k (2k+1)!! t_{2k+3} u^{-k} $$
    """
    def f(k):
        assert k>0
        S=0
        for j in range(1,k+1):            
            S+=sum([prod([dbfactorial(2*pi+1)*t[2*pi+3] for pi in p]) for p in partint(k,j)])*Rational(1,j*2**j)
        return S            
    return TimesfromFormula(f)


#%%
    

class MirzakhaniTimes(SpCurveTimes):
    name="MirzakhaniTimes"
    
    def initialize(self,*args,**kargs):
        pass

    def __getitem__(self,k):
        if k==3:
            return 0
        if k%2==0:
            return 0
        if k<3:
            return 0
        return Rational(2**(k-2)*(-1)**(int((k+1)/2)),factorial(k-2))*pi**(k-3)
    
    def __contains__(self,k):
        return k%2==1 and k>=3
    
    @property
    def y(self):
        z=Symbol("z")
        return Lambda((z),sin(2*pi*z)/(2*pi))
    

#%%

class LambdaDiv:
    r""" 
    turns a function Lambda((vars),expression)
    into a function that can take divisors as variables
    
    Usage:
    use the same syntax as Lambda  (imported from sympy)

    Example: 
       
    f=Lambda((z),sin(z))
    f(z) -> sin(z)
    f({z1:a,z2:b}) -> ERROR
    
    g=LambdaDiv((z),sin(z))
    g(z) -> sin(z)
    g({z1:a,z2:b}) -> a*sin(z1)+b*sin(z2)
    
    """
    def __init__(self,Lz,expr):
        self.Lz=Lz
        self.expr=expr
    
    def __repr__(self):
        return str(Lambda(self.Lz,self.expr))
    
    def __call__(self,*zz):
        Lz=list(zz)
        for i,z in enumerate(Lz):
            if isinstance(z,Divisor) or isinstance(z,dict):
                return sum([z[p]*self(*(Lz[:i]+[p]+Lz[i+1:])) for p in z])
        
        f=Lambda(self.Lz,self.expr)
        return f(*zz)
        
    

#%%
class SpCurve:
    r"""
    Spectral curves with 1 branch point
    x = z^2 + x0
    y = z - 1/2 \sum_k t_{2k+3} z^{2k+1}
    B = dz1 dz2 / (z1-z2)^2
    
    Usage:
    SpCurve(y=function , **options)
    or
    SpCurve(t=Times() , **options)
    
    options : 
    x = function   ( must be   lambda z:z**2+x0 )
    name = str
    
     
    
    
    """
    name="SpCurve"
    hbar=Symbol("hbar")
    
    def __init__(self,*args,**kargs):
        hbar=self.__class__.hbar
        z,z1,z2=symbols("z,z1,z2")
        self.x=Lambda((z),z*z)
        self.y=Lambda((z),z)
        self.B=Lambda((z1,z2),1/(z1-z2)**2)
        self.t=TimesfromDict({})
        self._Fgn_cached={}
        self._Wgn_cached={}
        
        if 't' in kargs:
            args=[kargs['t']]+list(args)
        if 'y' in kargs:
            args=[kargs['y']]+list(args)
            self.y=kargs['y']
        
        if len(args)==1:
            arg=args[0]
            if isinstance(arg,SpCurveTimes):
                self.t=arg
                self.y=self.t.y
            elif isinstance(arg,dict):
                self.t=TimesfromDict(arg)        
                self.y=self.t.y
            elif callable(arg):
                self.t=Timesfromy(arg)        
                self.y=Lambda((z),arg(z))
            else:
                raise ValueError()
        elif len(args)>1:
            raise ValueError()
        
        if 'x' in kargs:
            self.x=kargs['x']
            assert callable(self.x)
            z=Symbol('z')
            assert self.x(z).diff(z)==2*z, " In this class x(z) must be x(z) = z**2 + constant"
            
        if 'name' in kargs:
            self.name=kargs['name']
        else:
            self.name=""
            
        if 'B' in kargs:
            raise NotImplementedError(" only B=(z1-z2)**(-2) allowed in this class")
        if 'BP' in kargs:
            raise NotImplementedError(" only BP z=0  allowed in this class")

    def PolynomialEquation(self):
        x,y,z=symbols('x,y,z')
        return Lambda((x,y),y**2-expand((self.y(z)**2).subs({z:(x-self.x0)**half})))
    
    def __repr__(self):
        z,z1,z2=symbols("z,z1,z2")
        s=self.__class__.name
        s+="(\n"
        if self.name!="":
            s+=self.name+"\n"
        s+=f"  x(z) = {self.x(z)}\n"
        s+=f"  y(z) = {self.y(z)}\n"
        s+=f"  B(z1,z2) = {self.B(z1,z2)}\n"
        s+="  BP: z=0,  inv: z -> -z\n"
        s+="   )"
        return s
    
    @property
    def x0(self):
        return self.x(0)

    
    def Wgn(self,g,n):
        r"""
        EXAMPLES::

            sage: from topological_recursion.spectral_curve import SpCurve
            sage: S = SpCurve()
            sage: S.Wgn(2,1)
            Lambda(z0, -1/(1024*z0**10))
        """
        if not isinstance(g, numbers.Integral) or not isinstance(n, numbers.Integral):
            raise TypeError('g and n must be integers')
        g = int(g)
        n = int(n)
        if g < 0 or n <= 0:
            raise ValueError('g must be positive and n non-negative')

        if (g,n)==(0,1):
            z=Symbol('z')
            return Lambda((z),self.y(z)*2*z)        
        elif (g,n)==(0,2):
            return self.B        
        if (g,n) in self._Wgn_cached:
            return self._Wgn_cached[(g,n)]
        else:
            self._computeWgn(g,n)
            return self._Wgn_cached[(g,n)]

    def Fgn(self,g,n):
        if n==0:
            return self.Fg(g)
        assert isinstance(g,int)
        assert isinstance(n,int)
        assert g>=0
        assert n>=0
        if (g,n)==(0,1):
            z=Symbol('z')
            return Lambda((z),integrate(self.Wgn(0,1)(z),z))            
            raise NotImplementedError
            return Lambda((z),self.y(z)*2*z)        
        elif (g,n)==(0,2):
            z1,z2=symbols('z1,z2')
            # def f(z1,z2):
            #     return ln((z1**(-half)+z2**(-half))*half)
            def f(z1,z2):
                return -ln((z1+z2)/(2*z1**(half)*z2**(half)))
            return LambdaDiv((z1,z2),f(z1,z2))
            
            # raise NotImplementedError
            # return self.B        
        if (g,n) in self._Fgn_cached:
            return self._Fgn_cached[(g,n)]
        else:
            self._computeWgn(g,n)
            return self._Fgn_cached[(g,n)]

    def _computeWgn(self,g,n):
        assert isinstance(g,int)
        assert isinstance(n,int)
        assert g>=0
        assert n>=0
        Lz=tuple([Symbol("z"+str(i)) for i in range(n)])
        # for i,z in enumerate(Lz):
        #     if isinstance(z,Divisor) or isinstance(z,dict):            
        #         S=0
        #         for p in z:
        #             S+=z[p]*Fgn(g,Lz[:i]+[p]+Lz[i+1:],t=t)
        #         return S
        SF=0
        SW=0
        for d in range(3*g-3+n+1):
            for L in partint(d,n):
                SF+=INwithTimes(g,L,t=self.t)*prod([Lz[i]**(-(2*L[i]+1)) for i in range(n)])
                SW+=INwithTimes(g,L,t=self.t)*prod([Lz[i]**(-(2*L[i]+2))*(-(2*L[i]+1)) for i in range(n)])
        self._Wgn_cached[(g,n)]=Lambda(Lz,SW)
        self._Fgn_cached[(g,n)]=LambdaDiv(Lz,SF)
        

    def Fg(self,g):
        assert isinstance(g,int)
        assert g>=0
        if g==0:
            return self.F0()
        if g==1:
            return self.F1()
        z=Symbol('z')
        S=self.Fgn(g,1)(z)*self.y(z)*2*z
        r=series(S*z,z,0,1)
        r=r.removeO().subs({z:oo})
        return r*Rational(1,2*g-2)
    
    def F0(self):
        try:
            if len(self.t)>0:
                kmax=max([k for k in self.t])
            else:
                kmax=0
            if kmax>0:
                return half*sum([ self.Acycleoo(k)*self.Bcycleoo(k) for k in range(1,kmax+1)])                
            else:
                return 0
                
        except:
            raise NotImplemented(" not implemented for this class of Spectral Curves")
        
    def F1(self):
        return -Rational(1,24)*ln(1-self.t[3]*half)


    def F(self,order):
        gmax = int((order+1)/2)
        F=sum([self.Fg(g)*hbar**(2*g-2) for g in range(gmax+1)])+O(hbar**order)
        return F
        
    # def Schi(self,chi):
    #     assert is_integer(chi)
    #     assert chi>0
    #     # hbar=self.__class__.hbar
    #     z=Symbol('z')
    #     S=0
    #     for g in range(int((chi-1)/2)+2):
    #         n=chi-2*g+2
    #         # assert n>0
    #         for d in range(3*g-3+n+1):
    #             # print(g,n,d)
    #             Ld=partint(d,n)
    #             # print(Ld)
    #             S+=sum([INwithTimes(g,L,t=self.t) for L in Ld])*z**(-(2*d+n))*Rational(1,factorial(n))
    #     return Lambda((z),S)


    def Schi(self,chi):
        assert is_integer(chi)
        assert chi>0        
        def f(z):            
            if isinstance(z,Divisor) or isinstance(z,dict):
                Lz={p:z[p] for p in z}
            else:
                Lz={z:1}
            S=0
            for g in range(int((chi-1)/2)+2):
                n=chi-2*g+2
                S+=self.Fgn(g,n)(*([Lz]*n))*Rational(1,factorial(n))
            return S
        return f        

    def S1chi(self,chi):
        assert is_integer(chi)
        assert chi>0
        hbar=self.__class__.hbar
        z=Symbol('z')
        S=0
        for g in range(int((chi-1)/2)+2):
            n=chi-2*g+2
            assert n>0
            for d in range(3*g-3+n+1):
                # print(g,n,d)
                if n>1:
                    Ld=partint(d,n-1)
                else:
                    if d==0:
                        Ld=[[]]
                    else:
                        Ld=[]
                # print(Ld)
                # for L in Ld:
                    # print(L+[0])                
                S+=sum([INwithTimes(g,L+[0],t=self.t) for L in Ld])*z**(-(2*d+n-1))*Rational(1,factorial(n-1))
        return Lambda((z),-S)

    def lnpsi(self,order=2,stable=False):
        assert isinstance(order,int)
        hbar=self.__class__.hbar
        z=Symbol('z')
        S=0
        if not stable:
            S+=hbar**(-1)*self.Fgn(0,1)(z)
            S+=-half*ln(z)
        for chi in range(1,order):
            S+=self.Schi(chi)(z)*hbar**(chi)
        S+=O(hbar**order)
        return Lambda((z),S)

    def matrixPsi(self,order=2):
        assert isinstance(order,int)
        z=Symbol('z')
        hbar=self.__class__.hbar
        r=self._r(order)
        F01=self.Fgn(0,1)
        S=Lambda((z),expand(series(exp(self.lnpsi(order,stable=True)(z)),hbar,0,order)))
        T=Matrix([[exp(hbar**(-1)*F01(z))*S(z),0],[0,exp(hbar**(-1)*F01(-z))*S(-z)]])
        V=Matrix([[1,I],[I*r(z),-r(-z)]])*(2*z)**(-half)
        M=V*T
        return Lambda((z),M)        
        
        

    def _r(self,order=2):
        assert isinstance(order,int)
        assert order >0
        z=Symbol('z')
        hbar=self.__class__.hbar
        r=z
        for chi in range(1,order):
            r+=self.S1chi(chi)(z)*hbar**chi
        r+=O(hbar**(order))
        # r=Lambda((z),z+sum([self.S1chi(chi)(z)*hbar**chi  for chi in range(1,order)])+O(hbar**(order)))
        return Lambda((z),r)
    
    def matrixM(self,order=3):
        assert isinstance(order,int)
        hbar=self.__class__.hbar
        z=Symbol('z')
        # y=Lambda((z),z-half*sum([t[k]*z**(k-2) for k in t]))
        r=self._r(order)
        # r=Lambda((z),z+sum([self.S1chi(chi)(z)*hbar**chi  for chi in range(1,order)])+O(hbar**(order)))
        rm=series(r(z)-r(-z),hbar,0,order)
        s=expand(series(1/rm,hbar,0,order))
        return Lambda((z),Matrix([[expand(-r(-z)*s),s],[expand(-s*r(z)*r(-z)),expand(s*r(z))]]))

    def matrixD1(self,order=3):
        assert isinstance(order,int)
        hbar=self.__class__.hbar
        z=Symbol('z')
        # y=Lambda((z),z-half*sum([t[k]*z**(k-2) for k in t]))
        r=self._r(order)
        # r=Lambda((z),z+sum([self.S1chi(chi)(z)*hbar**chi  for chi in range(1,order)])+O(hbar**(order)))
        rm=series(r(z)-r(-z),hbar,0,order)
        s=expand(series(1/rm,hbar,0,order))
        # return rm,s
        A=series((r(z)+r(-z))*s,hbar,0,order)
        C=series(-2*r(z)*r(-z)*s,hbar,0,order)
        D= Matrix([[-A,2*s],[C,A]])
        return Lambda((z),D)


    def matrixD(self,order=3):
        assert isinstance(order,int)
        t=self.t
        y=self.y
        hbar=self.__class__.hbar
        z=Symbol('z')
        x=Symbol('x')
        x0=self.x0
        # x0=expand(self.x(z)-z**2)
        dd1=self.matrixD1(order)(z)
        dd0=[]
        for i in range(2):
            dd0i=[]
            for j in range(2):
                d1=dd1[i,j].removeO()
                d=series(d1*y(z),z,0,0).removeO()
                r=expand(d1*y(z)-d)
                r=r.subs({z:(x-x0)**half})                                
                dd0i+=[r+O(hbar**order)]
            dd0+=[dd0i]
        
        
        return Lambda((x),Matrix(dd0))
    
    def Acycleoo(self,k,omega="default"):
        k=int(k)
        assert k>=0
        z=Symbol('z')
        if omega=="default":
            omega=Lambda((z),self.y(z)*2*z)
        return series(z**(-k+1)*(self.x(z)/z**2)**(-k*half)*omega(z),z,oo,1 ).coeff(z,0)
        
    def Bcycleoo(self,k,omega="default"):
        k=int(k)
        assert k>0
        z=Symbol('z')
        if omega=="default":
            omega=Lambda((z),self.y(z)*2*z)
        return series(Rational(1,k)*z**(k+1)*(self.x(z)/z**2)**(k*half)*omega(z),z,oo,1 ).coeff(z,0)
        
    @property
    def KPtimes(self):
        return TimesfromFormula(lambda k:self.Acycleoo(k))
        

#%%


######## ########  ####    ###    ##        ######
   ##    ##     ##  ##    ## ##   ##       ##    ##
   ##    ##     ##  ##   ##   ##  ##       ##
   ##    ########   ##  ##     ## ##        ######
   ##    ##   ##    ##  ######### ##             ##
   ##    ##    ##   ##  ##     ## ##       ##    ##
   ##    ##     ## #### ##     ## ########  ######


#%%
        
if __name__=="__main__":
    x=Symbol('x')
    z=Symbol('z')
    z0,z1,z2,z3,z4,z5=symbols('z0,z1,z2,z3,z4,z5')
    t3,t5,t7,t9=symbols('t3,t5,t7,t9')
    hbar=SpCurve.hbar
        

#%%
if __name__=="__main__":
    St=SpCurve(Times({5:t5,7:t7}))
    print(St)
    print("W21 : ")
    print(St.Wgn(2,1)(z))


# %%

if __name__=="__main__":
    # SWP=SpCurve(MirzakhaniTimes())
    SWP=SpCurve(Times("Mirzakhani"),name="Mirzakhani")
    print(SWP)
    print("W21 : ")
    print(SWP.Wgn(2,1)(z))



# %%

if __name__=="__main__":
    u=Symbol('u')
    z=Symbol('z')
    SP1=SpCurve(x=Lambda((z),z*z-2*u),y=Lambda((z),z**3-3*u*z),name="Painleve1")
    print(SP1)
    print("W21 : ")
    print(SP1.Wgn(2,1)(z))

# %%

if __name__=="__main__":
    t=SpCurveTimes.from_Dict({7:5})
    SP3=SpCurve(t,name="SpCurvefromDict_t")
    print(SP3)
    print("times : ")
    print(SP3.t)
    print("y : ")
    print(SP3.y)
    print("W21 : ")
    print(SP3.Wgn(2,1)(z))



# %%

if __name__=="__main__":
    t=SpCurveTimes.from_y(lambda z: -3*z+6*z**7)
    SP4=SpCurve(t,name="SpCurvefrom_y")
    print(SP4)
    print("times : ")
    print(SP4.t)
    print("y(z) : ")
    print(SP4.y(z))
    print("W21 : ")
    print(SP4.Wgn(2,1)(z))


# %%



# %%

if __name__=="__main__":
    t=SpCurveTimes.from_formula(lambda k: Rational(1,factorial(k)))
    SP5=SpCurve(t,name="SpCurvefrom_formula")
    print(SP5)
    print("times : ")
    print(SP5.t)
    print(f" t[3] = {SP5.t[3]}")
    print(f" t[5] = {SP5.t[5]}")
    print("y(z) : ")
    print(SP5.y(z))
    print("W21 : ")
    print(SP5.Wgn(2,1)(z))

# %%


if __name__=="__main__":
    n=Symbol('n')
    t=SpCurveTimes.from_formula(Lambda((n),factorial(n)))
    SP5=SpCurve(t,name="SpCurvefrom_formula")
    print(SP5)
    print("times : ")
    print(SP5.t)
    print(f" t[3] = {SP5.t[3]}")
    print(f" t[5] = {SP5.t[5]}")
    print("y(z) : ")
    print(SP5.y(z))


# %%
