
# coding: utf-8

# In[6]:

import numpy as np
import sympy as sy

#from sympy import poly
from sympy import Poly

#from sympy import residue

# useful ?
from sympy import *
#from sympy import simplify

# useful ?
# from fractions import gcd
from math import gcd


# from itertools import combinations

# from sympy.parsing.sympy_parser import parse_expr

# from sympy.tensor import IndexedBase, Idx

# useful ?
# from sympy.abc import x,y


# In[15]:




# In[13]:

class MyPol2:
    """
    class for bivariate polynomials

    Usage:
    MyPol2(P:list of lists)     such that  P[j][i]=P_{i,j}
    MyPol2(P:dict)              such that  P[(i,j)]=P_{i,j}
    MyPol2(Poly)                sympy.Poly  must be bivariate
    MyPol2(callable)            must be a function of 2 variables -> number, must be a polynomial
    
    
    """
    name="PolynomialBivariate"    
    
    def __init__(self,P):
        if isinstance(P,list):  # entry can be a list [[]] P[j][i]=P_{i,j}
            if len(P)==0: P=[[0]]
            self.coefs=P
        elif isinstance(P,dict):  # entry can be a dict  P[(i,j)]=P_{i,j}
            if len(P)==0: P={(0,0):0}
            self.make_tablefromdict(P)
        elif isinstance(P,Poly):
            x=sy.Symbol('x')
            y=sy.Symbol('y')
            Px = Poly(P,y).all_terms()
            Pl={}
            for px in Px:
                for monomial in Poly(px[1],x).all_terms():         # i,j,coeff
                    Pl[(monomial[0][0],px[0][0])]=monomial[1]
            self.make_tablefromdict(Pl)
            
        elif callable(P):        # entry can be a function  P=lambda x,y :  ...
            self.make_table(P)
        if len(self.coefs)==0:
            self.coefs=[[0]]
            
        # removes null coefficients beyond degree.
        self.simplifycoefsdeg()

        
    
    def __call__(self,x,y):
        S=self[0,0]
        for j,Cy in enumerate(self.coefs):
            for i,Cx in enumerate(Cy):
                if i+j>0:
                    S+=Cx*x**i*y**j
        return S
    
    def __getitem__(self,indx):
        i=indx[0]
        j=indx[1]
        if j>=len(self.coefs): return 0
        if i>=len(self.coefs[j]): return 0
        return self.coefs[j][i]
    
    def deg(self):
        dx,dy=0,0
        for j in range(len(self.coefs)):
            for i in range(len(self.coefs[j])):
                if self.coefs[j][i]!=0 and i>dx: dx=i
                if self.coefs[j][i]!=0 and j>dy: dy=j        
        return dx,dy
    
    def __repr__(self,xs='x',ys='y'):
        x=Symbol(xs)
        y=Symbol(ys)
        return str(self.__call__(x,y))
    
    def iszero(self):
        if len(self.coefs)==0: return True
        for j in range(len(self.coefs)):
            if len(self.coefs[j])>0:
                for c in self.coefs[j]:
                    if c!=0: return False
        return True

    def __ne__(self,autre):
        if isinstance(autre,int):
            if autre==0: return not self.iszero()            
        if isinstance(autre,MyPol2):
            if self.iszero() and autre.iszero(): return False
            dx,dy=self.deg()
            dx2,dy2=autre.deg()
            for j in range(max([dy,dy2])):
                for i in range(max([dx,dx2])):
                    if self[i,j]!=autre[i,j]: return True
            return False            
        return False

    def __eq__(self,autre):
        return not self!=autre

    
    def make_table(self,P):  # a partir d'une fonction
        x,y=sy.symbols('x y')
        Px = Poly(P(x,y),y).all_terms()
        T=[]
        for px in Px:
            Tx=[]
            for monomial in Poly(px[1],x).all_terms():
                Tx=[monomial[1]]+Tx
            T=[Tx]+T
        self.coefs=T
        
    def as_dict(self):
        D={}
        for j in range(len(self.coefs)):
            for i in range(len(self.coefs[j])):
                c=self.coefs[j][i]
                if c!=0:
                    D[(i,j)]=c
        return D
        
        
    def make_tablefromdict(self,P):
        PL=P.keys()
        dx=max([idx[0] for idx in PL])
        dy=max([idx[1] for idx in PL])
        T=[]
        for j in range(dy+1):
            T+=[[0]*(dx+1)]
        for IJ in PL:
            T[IJ[1]][IJ[0]]=P[IJ]
        self.coefs=T
                
        

    def simplifycoefsdeg(self):
        dx,dy=self.deg()
        self.coefs=self.coefs[:dy+1]
        for j in range(len(self.coefs)):
            self.coefs[j]=self.coefs[j][:dx+1]
        
    def __add__(self,autre):
        dx,dy=self.deg()
        dx2,dy2=autre.deg()
        d1=max(dx,dx2)+1
        d2=max(dy,dy2)+1
        T=[]
        #T=[[0]*d1]*d2
        for j in range(d1):
            Tj=[0]*d1
            for i in range(d2):
                Tj[i]=self[i,j]+autre[i,j]
            #T[j]=Tj
            T+=[Tj]
        return MyPol2(T)

    def __neg__(self):
        return self*(-1)
        
    def __sub__(self,autre):
        return self+(autre*(-1))

    def __pow__(self,n):
        if n==0: return MyPol2([[1]])
        if n==1: return MyPol2(self.coefs)
        if n>1: return self*self**(n-1)
        
        
    def __mul__(self,autre):
        if isinstance(autre,MyPol2):
            dx,dy=self.deg()
            dx2,dy2=autre.deg()
            T=[[0]*(dx+dx2+1)]*(dy+dy2+1)
            for jj in range(dy+dy2+1):
                Tj=[0]*(dx+dx2+1)
                for j in range(jj+1):
                    for ii in range(dx+dx2+1):
                        for i in range(ii+1):
                            Tj[ii]+=self[i,j]*autre[ii-i,jj-j]
                T[jj]=Tj
            return MyPol2(T)    
        else:
            dx,dy=self.deg()
            #T=[[0]*(dx+1)]*(dy+1)
            T=[]
            for j in range(dy+1):
                Tj=[0]*(dx+1)
                for i in range(dx+1):
                    Tj[i]=autre*self[i,j]
                #T[j]=Tj
                T+=[Tj]
            return MyPol2(T)    
        
    def diff(self,a,b):  # d/dx**a d/dy**b
        def fact(u,v):  # defines factorial
            if v<=u:return 1
            return v*fact(u,v-1)        
        dx,dy=self.deg()
        if b>dy or a>dx: return MyPol2([[0]])
        T=[[0]*(dx-a+1)]*(dy-b+1)
        for j in range(dy-b+1):
            Tj=[0]*(dx-a+1)
            for i in range(dx-a+1):
                Tj[i]=self[i+a,j+b]*fact(i,i+a)*fact(j,j+b)
            T[j]=Tj
        return MyPol2(T)    
            
    def subs(self,other):   # returns self(otherx(x,y),othery(x,y))
        otherx,othery=other
        return MyPol2(lambda x,y: self.__call__(otherx(x,y),othery(x,y)))
    
    
    def diffdiv(self,a,d='x'):  # d='x' ou 'y'   difference divisee (P(x+a,y)-P(x,y) )/a
        def fact(u,v):
            if v<=u:return 1
            return v*fact(u,v-1)        
        dx,dy=self.deg()
        T=[[0]*(dx+1)]*(dy+1)
        if d=='x':
            for j in range(dy+1):
                Tj=[0]*(dx+1)
                for i in range(dx+1):
                    for k in range(1,dx-i+1):
                        Tj[i]+=a**(k-1) * self[i+k,j]*fact(i+k,i)/fact(k,1)
                    T[j]=Tj
        elif d=='y':
            for j in range(dy+1):
                Tj=[0]*(dx+1)
                for k in range(1,dy-j+1):
                    for i in range(dx+1):
                        Tj[i]+=a**(k-1) * self[i,j+k]*fact(j+k,j)/fact(k,1)
                T[j]=Tj
        return MyPol2(T)    
        
    def Newton(self,recompute=False): 
        if not recompute:
            try:
                return self.newtonPol
            except:
                pass
        T=[]
        dx,dy=self.deg()
        for j in range(dy+1):
            for i in range(dx+1):
                if self[i,j]!=0: T+=[[i,j]]   
        if T==[]: T=[[0,0]]
        self.newtonPol = Newt(T)
        return self.newtonPol
    
    

    def discriminant(self):
        x,y=sy.symbols("x,y")
        # return sy.discriminant( Poly(Poly(self(x,y),x,y),y))
        # raise Exception(" *** Not ready yet")
        dx,dy=self.deg()
        dd=2*dy-1
        x,y=sy.symbols("x,y")
        LPx=[sum([self[i,j]*x**i  for i in range(dx+1)]) for j in range(dy+1)]
        M=sy.Matrix(np.zeros(dd**2).reshape(dd,dd))
        for j in range(dy-1):
            for i in range(dy+1):
                M[j,i+j]=LPx[i]
        for j in range(dy):
            for i in range(dy):
                M[j+dy-1,i+j]=(i+1)*LPx[i+1]
        return sy.Poly(M.det(),x)
        return M
    



#%%

########  ##          ###    ##    ## ########  ######  ##     ## ########  ##     ## ########
##     ## ##         ## ##   ###   ## ##       ##    ## ##     ## ##     ## ##     ## ##
##     ## ##        ##   ##  ####  ## ##       ##       ##     ## ##     ## ##     ## ##
########  ##       ##     ## ## ## ## ######   ##       ##     ## ########  ##     ## ######
##        ##       ######### ##  #### ##       ##       ##     ## ##   ##    ##   ##  ##
##        ##       ##     ## ##   ### ##       ##    ## ##     ## ##    ##    ## ##   ##
##        ######## ##     ## ##    ## ########  ######   #######  ##     ##    ###    ########


class PlaneCurve(MyPol2):
            

    def branchpoints(self):
        x=sy.Symbol("x")
        Delta=self.discriminant()
        r = sy.roots(Delta)
        Lr={}
        i=0
        for a,m in r.items():
            an=sy.Symbol('a'+str(i))
            Lr[an]={'value':a,'multiplicity':m}
            i+=1
        return Lr
        
    def punctures(self,recompute=False):
        if not recompute:
            try:
                return self.list_punctures
            except:
                pass
        # raise NotImplementedError(" Newt.punctures ")
        newtonPol=self.Newton()
        bords=newtonPol.bords
        # L={}
        return [Puncture(b) for b in bords]
    
        nb=-1
        for b in bords:
            nb+=1
            p,q=b[0],b[1]
            name=sy.Symbol("puncture"+str(nb))
            degs = p[1]-q[1],q[0]-p[0]
            L[name]= {'segment':[p,q] , 'degrees':degs}
        self.list_punctures=L
        return self.list_punctures

    def BQ(self):
        x,y=symbols('x,y')
        xx,yy=symbols('xx,yy')
        dx,dy=self.deg()
        N=self.Newton()
        S=0
        
        
        
        # ancien
        
        for i in range(len(N.allpoints)-1):
            for j in range(i+1,len(N.allpoints)):
                p=N.allpoints[i]
                q=N.allpoints[j]
                r=[p[0],q[1]]
                s=[q[0],p[1]]
                sk=np.sign(s[0]-r[0])
                sl=np.sign(s[1]-r[1])
                
                if sk*sl != 0:
                    for k in range(1,abs(s[0]-r[0])):
                        for l in range(1,abs(s[1]-r[1])):
                            u=r[0]+k*sk
                            v=r[1]+l*sl
                            uu=s[0]-k*sk
                            vv=s[1]-l*sl
                            if N.is_interior(uu,vv) and not N.is_interior(u,v):
                                S+=k*l*self[p[0],p[1]]*self[q[0],q[1]]*(x**(u-1)*y**(v-1)*xx**(uu-1)*yy**(vv-1)+xx**(u-1)*yy**(v-1)*x**(uu-1)*y**(vv-1))
                            if not N.is_interior(uu,vv) and not N.is_interior(u,v):
                                S+=k*l*self[p[0],p[1]]*self[q[0],q[1]]*x**(u-1)*y**(v-1)*xx**(uu-1)*yy**(vv-1)
                                
        return Lambda((x,y,xx,yy),S)
        
        
    def Py(self):
        return self.diff(0,1)
    
    def KerB(self):  # in progress
        print(" *** Warning KerB() not  verified ***")
        Py=self.Py()
        Q=self.BQ()
        
        def B(x,y,xx,yy):
            return (self(x,yy)*self(xx,y)/(x-xx)**2/(y-yy)**2 - Q(x,y,xx,yy))/(Py(x,y)*Py(xx,yy))
        return B
        
        
        #def QB(x1,y1,x2,y2):
        #    return sum([sum([T[j][i](x2,y2)*x1**i*y1**j for i in range(2*dx+2)]) for j in range(dy)])

        def Bnum(x1,y1,x2,y2):
            QB=sum([sum([T[j][i](x1,y1)*x2**i*y2**j for i in range(2*dx+2)]) for j in range(dy)])
            return (x1-x2)**2*QB+Py(x2,y2)*(Py(x2,y1)+(x1-x2)*Pxy(x2,y1))

        def Bdenom(x1,y1,x2,y2):
            return (x1-x2)**2*Py(x2,y2)*Py(x1,y1)
        
        def B(x1,y1,x2,y2):
            return Bnum(x1,y1,x2,y2)/Bdenom(x1,y1,x2,y2)
        
        # le vrai B(x1,y1,x2,y2)=Bnum(x1,y1,x2,y2)/(x1-x2)**2 / Py(x1,y1) / Py(x2,y2)
        
        return B,Bnum,Bdenom

    def genus(self):
        # only algebraic genus at the moment
        # remains to take into account degeneracies of branchpoints
        return len(self.Newton().interior())

    def asymptoticPol(self,pct):
        assert isinstance(pct,Puncture)
        zeta=sy.Symbol("zeta")
        eta=sy.Symbol("eta")
        x,y=sy.symbols("x,y")
        dx,dy=pct.degrees()
        m=pct.intercept()
        Na = [p for p in self.Newton() if pct.sameline(p)]
        Namin=min([p[0] for p in Na]),min([p[1] for p in Na])
        x0=sy.Symbol("x0")
        y0=sy.Symbol("y0")

        if dx>0:
            x=zeta**(-dx)
        elif dx<0:
            x=x0+zeta**(-dx)
        elif dx==0:
            x=x0
        if dy>0:
            y=eta*zeta**(-dy)
        elif dy<0:
            y=y0+eta*zeta**(-dy)
        elif dy==0:
            y=y0
        P=sy.simplify(sum([self[p[0],p[1]]*x**p[0]*y**p[1] for p in Na])*zeta**m/eta**(Namin[1]))
        

        return P



    def times(self,*pcts):
        if len(pcts)==0:
            return self.times(*self.punctures())
        if len(pcts)>1:
            return {p: self.times(p) for p in pcts}
        pct=pcts[0]
        
        P=self.asymptoticPol(pct)



    def Poincareform(self,*ij):
        if len(ij)==0:
            raise ValueError
        if len(ij)==1:
            ij=ij[0]
        assert len(ij)==2
        i,j=ij[0],ij[1]
        assert i==int(i) and j==int(j)
        x,y=symbols('x','y')
        return Lambda((x,y),x**(int(i))*y**(int(j))/self.Py()(x,y))
        
                



#%%
        
# class Puncture:

########  ##     ## ##    ##  ######  ######## ##     ## ########  ########
##     ## ##     ## ###   ## ##    ##    ##    ##     ## ##     ## ##
##     ## ##     ## ####  ## ##          ##    ##     ## ##     ## ##
########  ##     ## ## ## ## ##          ##    ##     ## ########  ######
##        ##     ## ##  #### ##          ##    ##     ## ##   ##   ##
##        ##     ## ##   ### ##    ##    ##    ##     ## ##    ##  ##
##         #######  ##    ##  ######     ##     #######  ##     ## ########

class PunctureNewton:
    """
    Class for punctures coming from a Newton Polygon
    
    Usage:
    
    instantiate:
    p = PunctureNewton(p1,p2,[name])
    
    p.degrees() -> dx,dy
    p.intercept() -> m such that the line (p1,p2) is  i*dx+j*dy=m
    
    
    
    """
    
    
    name="Puncture"
    symbol="alpha"
    nb=0
    
    def __init__(self,*p,name="",**kargs):
        if len(p)==1:
            p=p[0]
        assert len(p)==2
        self.p1=p[0]
        self.p2=p[1]
        self.name=self._makename(name)

    def _makename(self,name=""):
        if name=="":
            name=self.__class__.symbol+str(self.__class__.nb)
            self.__class__.nb+=1
        return name

    def __repr__(self):
        s=self.__class__.name
        s+=f"({self.name})"
        return s
    
    def degrees(self):
        return self.p1[1]-self.p2[1],self.p2[0]-self.p1[0]        

    def intercept(self):
        dx,dy=self.degrees()
        return self.p1[0]*dx+self.p1[1]*dy
    
    def line(self):
        dx,dy=self.degrees()
        m=self.intercept()
        return lambda i,j:i*dx+j*dy-m

    def sameline(self,p):
        dx,dy=self.degrees()
        m=self.intercept()
        return p[0]*dx+p[1]*dy-m==0
        
    def assymptotic(self,pol):        
        
        raise NotImplementedError


        
# In[3]:

##    ## ######## ##      ## ########
###   ## ##       ##  ##  ##    ##
####  ## ##       ##  ##  ##    ##
## ## ## ######   ##  ##  ##    ##
##  #### ##       ##  ##  ##    ##
##   ### ##       ##  ##  ##    ##
##    ## ########  ###  ###     ##


class Newt():              # classe des polytopes de Newton
    name="NewtonPol"
    
    def __init__(self,points=[[0,0]],*kargs):       
        self.allpoints=[]                   # defini par une liste de points
        for p in points:                      # on verifie que chaque element de la liste est bien un point entier, 
            if p not in self.allpoints: # et n'est pas en double
                assert len(p)==2 
                assert isinstance(p[0],int) and isinstance(p[1],int)
                self.allpoints+=[p]
                        
        self.Cstar=False
        if 'C*' or 'Cstar' in kargs: self.Cstar=True

    def __repr__(self):
        return self.__class__.name+"( "+ str(self.allpoints)+" )"
   
    def __str__(self):
        return str(self.allpoints)
        
    def __add__(self,other):                      # pour additioner 2 polytopes, on joint leur listes de points
        points=[p for p in self.allpoints]
        for p in other.allpoints:
            if p not in points:
                points+=[p]        
        return Newt(points)

    def __contains__(self,indx):
        i=indx[0]
        j=indx[1]
        return [i,j] in self.allpoints

    def __iter__(self):
        return iter(self.allpoints)
        
    # def __getitem__(self,indx):
    #     i=indx[0]
    #     j=indx[1]
    #     return [i,j] in self.allpoints

    def _addvector(self,v):                      # pour additioner un polytope et un vecteur entier, on decale le polytope par ce vecteur entier
        """ returns the .allpoints shiftted  by  v = (vx,vy) """
        assert len(v)==2
        assert isinstance(v[0],int) and isinstance(v[1],int)
        return [[p[0]+v[0],p[1]+v[1]] for p in self.allpoints]

    
    def boundingBox(self):                              # le rectangle minimal contenant le polytope
        xM=max([p[0] for p in self.allpoints])
        yM=max([p[1] for p in self.allpoints])
        xm=min([p[0] for p in self.allpoints])
        ym=min([p[1] for p in self.allpoints])
        return xM,yM,xm,ym
                            
    def sorted(self):                             # ordonne les points du polytope dans l'ordre lexicographique, ligne puis colonne
        points=self.allpoints
        xmax,ymax,xmin,ymin=self.boundingBox()
        sortedpoints=sorted(points, key=lambda p: p[0]*ymax+p[1])
        return sortedpoints
    
    def To_Table(self,occupied=True,empty=False):                          # met le polytope dans une grille rectangle de taille donnee par self.max
        points=self.allpoints                    # True si un point est occupe, False si il ne l'est pas. 
        xmax,ymax,xmin,ymin=self.boundingBox()
        T = [[empty]*(xmax-xmin+1) for i in range(0,ymax-ymin+1)]
        for p in points:
            T[p[1]-ymin][p[0]-xmin]=occupied
        return T

    
    def print_Newton(self,full=" x ",empty=" . "):    # trace le polytope
        xmax,ymax,xmin,ymin=self.boundingBox()            # produit une str
        Newtprint=""
        for i in reversed(range(ymax-ymin+1)):
            Newtpi=""
            for j in range(xmax-xmin+1):
                if [j,i] in self.allpoints: Newtpi+=full
                else: Newtpi+=empty
            Newtpi+="\n"
            Newtprint+=Newtpi
        return Newtprint


    


    def print_Newton_int(self,cbord=" * ",cempty=" . ",cinterior=" o "):
        xmax,ymax,xmin,ymin=self.boundingBox()
        bord = self.bord()
        interior=self.interior()
        Newtprint=""
        for i in reversed(range(ymax-ymin+1)):
            Newtpi=""
            for j in range(xmax-xmin+1):
                if [j,i] in bord: Newtpi+=cbord
                else:
                    if [j,i] in interior: Newtpi+=cinterior
                    else: Newtpi+=cempty
            Newtpi+="\n"
            Newtprint+=Newtpi
        return Newtprint

    def print_Newton_kind(self,cbord=" * ",cempty=" . ",cinterior=" o "):
        xmax,ymax,xmin,ymin=self.boundingBox()
        first = self.firstkind()
        second = self.secondkind()
        third = self.thirdkind()
        Newtprint=""
        for i in reversed(range(ymax-ymin+1)):
            Newtpi=""
            for j in range(xmax-xmin+1):
                if [j,i] in first: Newtpi+=" 1 "
                else:
                    if [j,i] in second: Newtpi+=" 2 "
                    else: 
                        if [j,i] in third: Newtpi+=" 3 "
                        else: Newtpi+=cempty
            Newtpi+="\n"
            Newtprint+=Newtpi
        return Newtprint                
    
    def bord(self):        # trouve le bord du polytope        
        
        if len(self.allpoints)<=2: return self.allpoints  # si il y a 0,1 ou 2 points, le bord est trivial, egal au polytope lui meme
        
        def distanceptsegment(p1,p2,p3):  # distance d'un point p1 a une droite orientee p2->p3  ,  >0 si a gauche, <0 si a droite
            return (p1[0]-p2[0])*(p1[1]-p3[1])-(p1[1]-p2[1])*(p1[0]-p3[0])
        
        xmax,ymax,xmin,ymin=self.boundingBox()
        
        # on met initialement 1 point dans le bord: 
        pt0=[xmin,ymin]
        for p in self.allpoints:
            if p[0]==xmin and p[1]>pt0[1]: pt0=p      # le plus haut de la 1ere colone  
        bord=[pt0]
        
        # on initialise
        pt1=pt0        
#        print("initialization pt0="+str(pt0))
        fini=False

        while not fini:           # tant qu'on est pas revenu au point de depart
#            print("boucle pt1="+str(pt1))
            ptmax=self.allpoints[0]              # on initialise la recherche avec ptmax  le premier point possible
            if ptmax==pt1: ptmax=self.allpoints[1]  # different de pt1

#            print("           ptmax="+str(ptmax))
            for pt3 in self.allpoints:                   # on va alors regarder tous les points pt3 sauf pt1 et ptmax
                if pt3!= pt1 and pt3!= ptmax:
                    m=distanceptsegment(pt3,pt1,ptmax)          # si pt3 est a gauche du segment (pt1,ptmax)
#                    print("           pt3="+str(pt3)+"  ,  m="+str(m))
                    if m>0:                                #   le pt le plus a gauche est mis a pt3,
                        ptmax=pt3                                  
#            print("           ptmax="+str(ptmax))

            if ptmax[1]==ymin and self.Cstar==False: fini=True
            if ptmax!=pt0:
                bord+=[ptmax]                           # ptmax est donc le plus a gauche trouvé, on l'ajoute au bord
                pt1=ptmax                               # on recommence la boucle en partant de ptmax qui devient le nouveau pt1
            if ptmax==pt0: fini=True
#        print("bord="+str(bord))
        
        # on rajoute les pts entiers sur les segments
        bordtotal=[]
        if self.Cstar: krange=range(len(bord))
        else: krange=range(len(bord)-1)
            
        for k in krange:
            p=bord[k]
            pnext=bord[(k+1) % len(bord)]

            if pnext[1]-p[1]==0 : 
                steps=abs(pnext[0]-p[0])
                stepy=0
                stepx=(pnext[0]-p[0])/steps
            else:
                if pnext[0]-p[0]==0 : 
                    steps=abs(pnext[1]-p[1])
                    stepx=0
                    stepy=(pnext[1]-p[1])/steps
                else: 
                    steps= abs(gcd(pnext[1]-p[1],pnext[0]-p[0]))
                    stepx=(pnext[0]-p[0])/steps
                    stepy=(pnext[1]-p[1])/steps

#            print("k="+str(k)+", p="+str(p)+", pnext="+str(pnext))
#            print("steps="+str(steps)+", stepx="+str(stepx)+", stepy="+str(stepy))
            
            if steps>0:
                for j in range(steps):
                    bordtotal+=[[int(p[0]+j*stepx),int(p[1]+j*stepy)]]
    #                print("j="+str(j)+" , "+str([p[0]+j*stepx,p[1]+j*stepy]))
        if not self.Cstar: bordtotal+=[bord[len(bord)-1]]
        
        
        return bordtotal

    @property
    def bords(self):
        L=self.bord()
        return [[L[i],L[i+1]] for i in range(-1,len(L)-1)]
        return self.bord()
    
    
    def interior(self):
        xmax,ymax,xmin,ymin=self.boundingBox()
        bord=self.bord()
        Newtint=[]
        
        if self.Cstar: jrange=range(ymin,ymax+1)
        else: jrange=range(ymin+1,ymax+1)
        if self.Cstar: irange=range(xmin,xmax+1)
        else: irange=range(xmin+1,xmax+1)
        if self.Cstar: kmax=len(bord)
        else: kmax=len(bord)-1
        
        for j in jrange:
            for i in irange:
                k=0
                ok=True
                while ok and k<kmax:
                    b1=bord[k]
                    b2=bord[(k+1) % len(bord)]
                    ok=((j-b1[1])*(b2[0]-b1[0])-(i-b1[0])*(b2[1]-b1[1])<0)
                    k+=1
                    
                if ok: Newtint+=[[i,j]]
        return Newtint

            
    

    
    def firstkind(self):
        No=self.interior()
        liste=[]
        for p in No:
            if p[0]>0 and p[1]>0:
                liste+=[[p[0]-1,p[1]-1]]
        return liste

    def thirdkind(self):
        bord=self.bord()
        liste=[]
        for p in bord:
            if p[0]>0 and p[1]>0:
                liste+=[[p[0]-1,p[1]-1]]
        return liste
    
    def secondkind(self):
        bord=self.bord()
        No=self.interior()
        bNo=No+bord
        liste=[]
        for p in self.allpoints:
            if [p[0]+1,p[1]+1] not in bNo:
                liste+=[p]
        return liste
        
        

    
    def formalpoly(self,letter="P"):
        x,y=sy.symbols("x,y")
        P=Poly(0,x,y)
        # P=MyPol2(Poly(0,x,y))
        for point in self.allpoints:
            i=point[0]
            j=point[1]
            sij=letter+str(i)+str(j)
        #            sij="P["+str(i)+"]["+str(j)+"]"
            Pij=sy.Symbol(sij,integer=True)
            P+=Poly(Pij* x**i * y**j ,x,y)
            pass
        return P
    
    
    def frompoly(self,P):
        raise Exception(" ***  method `Newt.frompoly`  not yet ready ")
        L=P.all_terms()
                
        pass

    def plot(self,L=[],marker="o",color="black",ax="default"):
        if ax=="default":
            ax=plt.gca()
        if L==[]:
            L=self.allpoints
        for p in L:
            ax.plot([p[0]],[p[1]],marker,color=color)
        
    def plotBord(self,color="black",ax="default"):
        if ax=="default":
            ax=plt.gca()
        bord=self.bord()
        for i in range(len(bord)):
            p=bord[i-1]
            q=bord[i]
            ax.plot([p[0],q[0]],[p[1],q[1]],color=color)


    def is_splitting(self,p1,p3):  # dit si la droite passant par p1,p3  coupe le polytope 
        """
        returns:
        True,p1,p3  if the line cuts the polygon
        False,p1,p3 if the polygon is at the left
        False,p3,p1 if the polygon is at the right
        or
        False,p1,p3 if the polygon is entirely on the line (p1,p3)
        """
        def si(x):
            if x>0: return 1
            if x<0: return -1
            return 0
        T=map(lambda p2: si((p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])) ,self.allpoints)
        if 1 in T and -1 in T: return True,p1,p3
        if 1 in T : return False,p1,p3   # le polytope est a droite
        if -1 in T : return False,p3,p1   # le polytope est a gauche
        return False,p1,p3   # le polytope est une ligne
        
    def is_bord(self,i,j):
        """ 
        returns True if (i,j) is a boundary point otherwise False
        """
        for b in self.bord():
            if b[0]==i and b[1]==j: return True
        return False
    
    def is_interior(self,i,j):
        """ 
        returns True if (i,j) is an interior point otherwise False
        """
        xmax,ymax,xmin,ymin=self.boundingBox()
        if i>xmax or i<xmin: return False
        if j>ymax or j<ymin: return False
        for b in self.bords:
            p1,p3=b[0],b[1]
            if (i-p1[0])*(p3[1]-p1[1])-(j-p1[1])*(p3[0]-p1[0]) <=0: return False    
        return True


    def kind(self,*indx):
        if len(indx)==2:
            i,j=indx[0],indx[1]
            if self.is_bord(i+1,j+1): return 3
            if self.is_interior(i+1,j+1): return 1
            return 2
        if len(indx)==1:
            k=indx[0]
            if k==3:
                if self.Cstar:
                    return [[b[0][0]-1,b[0][1]-1] for b in self.bords]
                return [[b[0][0]-1,b[0][1]-1] for b in self.bords if b[0][0]>0 and b[0][1]>0]
                
            elif k==2:
                return [p for p in self.allpoints if self.kind(p[0]+1,p[1]+1)==2]
            
            elif k==1:
                Lk=[]
                xmax,ymax,xmin,ymin=self.boundingBox()
                for i in range(xmin,xmax+1):
                    for j in range(ymin,ymax+1):
                        if self.kind(i,j)==1:
                            Lk+=[[i,j]]
                return Lk
            else:
                raise ValueError(" *** use  .kind(1,2,3) or .kind(i,j) ")
    

    def convexhull(self):
        Lp=self.allpoints
        if len(Lp)<=2:
            return Lp
        pminmax={}                            # dict: pour chaque x pminmax[x] = [y+,y-]
        for p in Lp:
            if p[0] not in pminmax:
                pminmax[p[0]]=[p[1],p[1]]
            else:
                if p[1]>max(pminmax[p[0]]):
                    pminmax[p[0]][-1]=p[1]
                elif p[1]<min(pminmax[p[0]]):
                    pminmax[p[0]][0]=p[1]
        ptsup=[]
        ptinf=[]
        for x in pminmax:                         # ptsup = liste des [x,y+]
            y=pminmax[x][1]
            ptsup+=[[x,y]]
        for x in pminmax:                         # ptinf = liste des [x,y-]  dans l'ordre des x decroissants
            y=pminmax[x][0]
            ptinf=[[x,y]]+ptinf

        if ptinf[0]==ptsup[-1]:                   # enleve les points comptes 2 fois
            del ptinf[0]
        if ptinf[-1]==ptsup[0]:
            del ptinf[-1]

        ptsup+=ptinf                              # et fait une seule liste
        #OK=True
        i=1
        while i<len(ptsup)-1:                      # enleve les point interieurs
            p0=ptsup[i-1]
            p=ptsup[i]
            p1=ptsup[i+1]
            if (p1[1]-p0[1])*(p[0]-p0[0])-(p1[0]-p0[0])*(p[1]-p0[1])>0:
                del ptsup[i]
                if i>1:
                    i+=-1
            else:
                i+=1
            #if i>=len(ptsup)-1:
            #    OK=False
        
        i=0                          # rajoutte tous les points du bords a coordonnees entieres
        while i<len(ptsup)-1:
            x,y=ptsup[i]
            x1,y1=ptsup[i+1]
            k=gcd(abs(x1-x),abs(y1-y))
            if k!=1:
                for j in range(1,k):
                    ptsup.insert(i+1,[int(x+j*(x1-x)/k),int(y+j*(y1-y)/k)])
                    i+=1
            i+=1

        
        return ptsup
        
    

    @staticmethod
    def Grid(n,m,alpha=0.3,color="grey",ax="default"):
        """

        Makes a pyplot.ax  Grid of size  n x m

        """
        if isinstance(n,list):
            nmin,n=n[0],n[1]
        else:
            nmin=0
        if isinstance(m,list):
            mmin,m=m[0],m[1]
        else:
            mmin=0
        if ax=="default":
            ax=plt.gca()
        ax.set_xlim([nmin-0.5,n+0.5])
        ax.set_ylim([mmin-0.5,m+0.5])
        ax.set_aspect('equal', adjustable='box')
        # ax.set_axis_off()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        for line in range(int(mmin),int(m+1)):
            ax.plot([nmin-0.2,n+1],[line,line],color=color,alpha=alpha)
        for col in range(int(nmin),int(n+1)):
            ax.plot([col,col],[mmin-0.2,m+1],color=color,alpha=alpha)
        

    @staticmethod
    def plotdroite(p1,p2,**options):
        """
        p1=(x1,y1) , p2=(x2,y2)
        
        plots the line passing through p1,p2
        
        
        """
        ax=plt.gca()
        xl,yl=ax.get_xlim(),ax.get_ylim()
        if p1[0]==p2[0]:
            return plt.plot([p1[0],p1[0]],[yl[0],yl[1]],**options)
        a=(p2[1]-p1[1])/(p2[0]-p1[0])
        def D(x):
            return a*(x-p1[0])+p1[1]
        return plt.plot([xl[0],xl[1]],[D(xl[0]),D(xl[1])],**options)


    @staticmethod
    def plotsegment(p1,p2,**options):
        """
        p1=(x1,y1) , p2=(x2,y2)
        
        plots the segment [p1,p2]
                
        """
        ax=plt.gca()
        return ax.plt([p1[0],p2[0]],[p1[1],p2[1]],**options)
            
    @staticmethod
    def plotdemiplan(p1,p2,**options):
        import matplotlib as mpl
        ax=plt.gca()
        xl,yl=ax.get_xlim(),ax.get_ylim()
        if p1[0]==p2[0]:
            if p2[1]<p1[1]:
                region=[[p1[0],yl[0]],[p1[0],yl[1]],[xl[1],yl[1]],[xl[1],yl[0]]]
            else:
                region=[[p1[0],yl[0]],[p1[0],yl[1]],[xl[0],yl[1]],[xl[0],yl[0]]]
        else:
            a=(p2[1]-p1[1])/(p2[0]-p1[0])
            b=p1[1]-a*p1[0]
            def is_inside(p):
                x,y=p[0],p[1]
                if y-a*x-b<0:
                    return False
                if y<yl[0] or y>yl[1]: return False
                if x<xl[0] or x>xl[1]: return False
                return True
            def bndpt(p):
                x,y=p[0],p[1]
                if x==xl[0] or x==xl[1]:
                    return True
                if y==yl[0] or y==yl[1]:
                    return True
                if a*x+b==y:
                    return True
                return False
            def reorder(L):
                i=0
                while i<len(L)-1:
                    p1,p2=L[i-1],L[i]
                    if not bndpt([(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]):
                        L[i+1],L[i]=L[i],L[i+1]
                        # i=0
                    else:
                        i+=1
                return L


            L=[]
            for i in [0,1]:
                for j in [0,1]:
                    p=[xl[i],yl[j]]
                    if is_inside(p):
                        L+=[p]
            for i in [0,1]:
                x=xl[i]
                p=[x,a*x+b]
                if is_inside(p):
                    L+=[p]
                if a !=0:
                    y=yl[i]
                    p=[(y-b)/a,y]
                    if is_inside(p):
                        L+=[p]
            region=reorder(L)
        # print(region)
        pol=mpl.patches.Polygon(region,closed=True,facecolor="yellow",**options)
        return plt.gca().add_patch(pol)


    
    @staticmethod
    def Newtfrompol(P,x,y):
        L=[]
        LQ=[]
        dy=len(Poly(P,y).all_coeffs())
        for j,A in enumerate(Poly(P,y).all_coeffs()):
            dx=len(Poly(A,x).all_coeffs())
            LA=[]
            for i,B in enumerate(Poly(A,x).all_coeffs()):
                LA=[B]+LA
                L+=[(dx-1-i,dy-1-j)]
            LQ=[LA]+LQ
        return L


    
    
#%%%

 #######  ##       ########
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
##     ## ##       ##     ##
 #######  ######## ########



# class Newtold():              # classe des polytopes de Newton
    
#     def __init__(self,points=[[0,0]],*kargs):       
#         self.allpoints=[]                   # defini par une liste de points
#         try:
#             for p in points:                      # on verifie que chaque element de la liste est bien un point entier, 
#                 if p not in self.allpoints:        # et n'est pas en double
#                     if isinstance(p, list):
#                         if len(p)==2:
#                             if isinstance(p[0],int) and isinstance(p[1],int):
#                                 self.allpoints+=[p]
                            
#         except:
#             pass
#         self.Cstar=False                            # si Cstar, on ne met pas le point [0,0], sinon on le met
#         if 'C*' in kargs or 'Cstar' in kargs: 
#             self.Cstar=True
#         else:
#             if [0,0] not in self.allpoints:
#                 self.allpoints=[[0,0]]+self.allpoints

#         self.boundingBox=self.boundingBox()
#         self.bords=self.computebords()
#         self.interior=self.computeinterior()
        

   
#     def __str__(self):
#         return str(self.allpoints)

#     def __add__(self,vector):
#         if self.Cstar:
#             return Newt([[p[0]+vector[0],p[1]+vector[1]] for p in self.allpoints],'C*')
#         else: return Newt([[p[0]+vector[0],p[1]+vector[1]] for p in self.allpoints if p[0]+vector[0]>=0 and p[1]+vector[1]>=0])

#     def __mul__(self,factor):
#         if isinstance(factor,int):
#             if self.Cstar:
#                 return Newt([[p[0]*factor,p[1]*factor] for p in self.allpoints],'C*')
#             else:
#                 if factor>=0:
#                     return Newt([[p[0]*factor,p[1]*factor] for p in self.allpoints])
        
    
#     def max(self):                              # le rectangle minimal contenant le polytope
#         xM=max([p[0] for p in self.allpoints])
#         yM=max([p[1] for p in self.allpoints])
#         xm=min([p[0] for p in self.allpoints])
#         ym=min([p[1] for p in self.allpoints])
#         return xM,yM,xm,ym
    
#     def __max__(self):
#         return self.boundingBox()
                            
#     def sort(self):                             # ordonne les points du polytope dans l'ordre lexicographique, ligne puis colonne
#         points=self.allpoints
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         sortedpoints=sorted(points, key=lambda p: p[0]*ymax+p[1])
#         return sortedpoints
    
#     def To_Table(self):                          # met le polytope dans une grille rectangle de taille donnee par self.max
#         points=self.allpoints                    # True si un point est occupe, False si il ne l'est pas. 
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         T = [[False]*(xmax-xmin+1) for i in range(0,ymax-ymin+1)]
#         for p in points:
#             T[p[1]-ymin][p[0]-xmin]=True
#         return T

#     def __getitem__(self,indx):
#         i=indx[0]
#         j=indx[1]
#         return [i,j] in self.allpoints
    

#     def is_splitting(self,p1,p3):  # dit si la droite passant par p1,p3  coupe le polytope 
#         def si(x):
#             if x>0: return 1
#             if x<0: return -1
#             return 0
#         T=map(lambda p2: si((p2[0]-p1[0])*(p3[1]-p1[1])-(p2[1]-p1[1])*(p3[0]-p1[0])) ,self.allpoints)
#         if 1 in T and -1 in T: return True,p1,p3
#         if 1 in T : return False,p1,p3   # le polytope est a droite
#         if -1 in T : return False,p3,p1   # le polytope est a gauche
#         return False,p1,p3   # le polytope est une ligne
        
#     def computebords(self):
#         Lc=self.convexhull()
#         Lc+=[Lc[0]]
#         return [[Lc[i],Lc[i+1]] for i in range(len(Lc)-1)]
        
    
#     def is_bord(self,i,j):
#         for b in self.bords:
#             if b[0][0]==i and b[0][1]==j: return True
#         return False
    
#     def is_interior(self,i,j):
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         if i>xmax or i<xmin: return False
#         if j>ymax or j<ymin: return False
#         for b in self.bords:
#             p1,p3=b[0],b[1]
#             if (i-p1[0])*(p3[1]-p1[1])-(j-p1[1])*(p3[0]-p1[0]) <=0: return False    
#         return True
    
#     def computeinterior(self):
#         Lk=[]
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         for i in range(xmin,xmax+1):
#             for j in range(ymin,ymax+1):
#                 if self.is_interior(i,j):
#                     Lk+=[[i,j]]
#         return Lk
    
    
#     def kind(self,*indx):
#         if len(indx)==2:
#             i,j=indx[0],indx[1]
#             if self.is_bord(i+1,j+1): return 3
#             if self.is_interior(i+1,j+1): return 1
#             return 2
#         if len(indx)==1:
#             k=indx[0]
#             if k==3:
#                 if self.Cstar:
#                     return [[b[0][0]-1,b[0][1]-1] for b in self.bords]
#                 return [[b[0][0]-1,b[0][1]-1] for b in self.bords if b[0][0]>0 and b[0][1]>0]
                
#             if k==2:
#                 return [p for p in self.allpoints if self.kind(p[0]+1,p[1]+1)==2]
            
#             if k==1:
#                 Lk=[]
#                 xmax,ymax,xmin,ymin=self.boundingBox()
#                 for i in range(xmin,xmax+1):
#                     for j in range(ymin,ymax+1):
#                         if self.kind(i,j)==1:
#                             Lk+=[[i,j]]
#                 return Lk
    
    
#     def print_Newton(self,full=" x ",empty=" . "):    # trace le polytope
#         xmax,ymax,xmin,ymin=self.boundingBox()            # produit une str
#         Newtprint=""
#         for i in reversed(range(ymax-ymin+1)):
#             Newtpi=""
#             for j in range(xmax-xmin+1):
#                 if [j,i] in self.allpoints: Newtpi+=full
#                 else: Newtpi+=empty
#             Newtpi+="\n"
#             Newtprint+=Newtpi
#         return Newtprint
            
    
    
    
    
    
#     def print_Newton_int(self,cbord=" * ",cempty=" . ",cinterior=" o "):
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         #bord = self.bord()
#         #interior=self.interior()
#         Newtprint=""
#         for i in reversed(range(ymax-ymin+1)):
#             Newtpi=""
#             for j in range(xmax-xmin+1):
#                 if self.is_bord(j,i): Newtpi+=cbord
#                 else:
#                     if self.is_interior(j,i): Newtpi+=cinterior
#                     else: Newtpi+=cempty
#             Newtpi+="\n"
#             Newtprint+=Newtpi
#         return Newtprint

#     def print_Newton_kind(self,cbord=" * ",cempty=" . ",cinterior=" o "):
#         xmax,ymax,xmin,ymin=self.boundingBox()
#         first = self.kind(1)
#         second = self.kind(2)
#         third = self.kind(3)
#         Newtprint=""
#         for i in reversed(range(ymax-ymin+1)):
#             Newtpi=""
#             for j in range(xmax-xmin+1):
#                 if [j,i] in first: Newtpi+=" 1 "
#                 else:
#                     if [j,i] in second: Newtpi+=" 2 "
#                     else: 
#                         if [j,i] in third: Newtpi+=" 3 "
#                         else: Newtpi+=cempty
#             Newtpi+="\n"
#             Newtprint+=Newtpi
#         return Newtprint

    
        

    
#     def formalpoly(self,letter="P"):
#         P=Pol(Poly(0,x,y))
#         for point in self.allpoints:
#             i=point[0]
#             j=point[1]
#             sij=letter+str(i)+str(j)
# #            sij="P["+str(i)+"]["+str(j)+"]"
#             Pij=sy.symbols(sij)
#             P+=Poly(Pij* x**i * y**j ,x,y)
#             pass
#         return P
    
    
#     def frompoly(self,P):
        
#         L=P.all_terms()
        
        
#         pass
    
#     @staticmethod
#     def Newtfrompol(P,x,y):
#         L=[]
#         LQ=[]
#         dy=len(Poly(P,y).all_coeffs())
#         for j,A in enumerate(Poly(P,y).all_coeffs()):
#             dx=len(Poly(A,x).all_coeffs())
#             LA=[]
#             for i,B in enumerate(Poly(A,x).all_coeffs()):
#                 LA=[B]+LA
#                 L+=[(dx-1-i,dy-1-j)]
#             LQ=[LA]+LQ
#         return L


#     def convexhull(self):
#         Lp=self.allpoints
#         if len(Lp)<=2:
#             return Lp
#         pminmax={}                            # dict: pour chaque x pminmax[x] = [y+,y-]
#         for p in Lp:
#             if p[0] not in pminmax:
#                 pminmax[p[0]]=[p[1],p[1]]
#             else:
#                 if p[1]>max(pminmax[p[0]]):
#                     pminmax[p[0]][-1]=p[1]
#                 elif p[1]<min(pminmax[p[0]]):
#                     pminmax[p[0]][0]=p[1]
#         ptsup=[]
#         ptinf=[]
#         for x in pminmax:                         # ptsup = liste des [x,y+]
#             y=pminmax[x][1]
#             ptsup+=[[x,y]]
#         for x in pminmax:                         # ptinf = liste des [x,y-]  dans l'ordre des x decroissants
#             y=pminmax[x][0]
#             ptinf=[[x,y]]+ptinf

#         if ptinf[0]==ptsup[-1]:                   # enleve les points comptes 2 fois
#             del ptinf[0]
#         if ptinf[-1]==ptsup[0]:
#             del ptinf[-1]

#         ptsup+=ptinf                              # et fait une seule liste
#         #OK=True
#         i=1
#         while i<len(ptsup)-1:                      # enleve les point interieurs
#             p0=ptsup[i-1]
#             p=ptsup[i]
#             p1=ptsup[i+1]
#             if (p1[1]-p0[1])*(p[0]-p0[0])-(p1[0]-p0[0])*(p[1]-p0[1])>0:
#                 del ptsup[i]
#                 if i>1:
#                     i+=-1
#             else:
#                 i+=1
#             #if i>=len(ptsup)-1:
#             #    OK=False
        
#         i=0                          # rajoutte tous les points du bords a coordonnees entieres
#         while i<len(ptsup)-1:
#             x,y=ptsup[i]
#             x1,y1=ptsup[i+1]
#             k=gcd(abs(x1-x),abs(y1-y))
#             if k!=1:
#                 for j in range(1,k):
#                     ptsup.insert(i+1,[x+j*(x1-x)/k,y+j*(y1-y)/k])
#                     i+=1
#             i+=1

        
#         return ptsup
        


# In[3]:

######## ########  ####    ###    ##        ######
   ##    ##     ##  ##    ## ##   ##       ##    ##
   ##    ##     ##  ##   ##   ##  ##       ##
   ##    ########   ##  ##     ## ##        ######
   ##    ##   ##    ##  ######### ##             ##
   ##    ##    ##   ##  ##     ## ##       ##    ##
   ##    ##     ## #### ##     ## ########  ######


# In[19]:

# if __name__=="__main__":    # Exemple elliptic curve
#     g2,g3=symbols('g2,g3')
#     x,y,xx,yy=symbols('x,y,xx,yy')
#     P1=MyPol2(Lambda((x,y),y**2-4*x**3-g2*x-g3))
#     N=P1.Newton()
#     print(P1)
#     print('degres : ', P1.deg())
#     print(P1.Newton().print_Newton())
#     print(N.print_Newton_int())
    
#     Q1=P1.BQ()
    
#     print(Q1(x,y,xx,yy))


# In[14]:

#%%
if __name__=="__main__":    
    import matplotlib.pyplot as plt

#%%


if __name__=="__main__":    # Exemple
    N1=Newt([[0,0],[0,6],[1,6],[4,5],[5,4],[6,3],[7,1],[7,0],[4,3],[1,4],[2,5]])




# In[15]:

if __name__=="__main__":
    
    Newt.Grid(8,7)
    N1.plot(color="red",marker="o")
    N1.plotBord(color="green")
    N1.plot(N1.interior(),color="blue",marker=".")
    N1.plot(N1.bord(),color="orange",marker=".")


# In[15]:

if __name__=="__main__":

    Newt.Grid(8,7)
    N1.plot(color="red")
    N1.plotBord(color="green")
    N1.plot(N1.firstkind(),color="blue")
    N1.plot(N1.thirdkind(),color="orange",marker="D")






# In[ ]:

if __name__=="__main__":
    print(N1.print_Newton())
    print(N1.To_Table(1,0))
    print(N1.To_Table('x','.'))

    print(N1.print_Newton_int())
    print(N1.print_Newton_kind())

# %%

if __name__=="__main__":
    print(N1.bord())
    print(N1.interior())
    print(N1.firstkind())
    print(N1.secondkind())
    print(N1.thirdkind())

    
#%%

if __name__=="__main__":
    N2=Newt([[0,0],[0,3],[5,0],[2,2]])
    P2=N2.formalpoly()
    print(P2)
    MP2=MyPol2(P2)
    print(MP2)

#%%

if __name__=="__main__":
    C=PlaneCurve(P2)
    Q2=C.BQ()
    print(Q2)
    print()
    x1,y1,x2,y2=sy.symbols("x1,y1,x2,y2")
    print(Q2(x1,y1,x2,y2))


#%%

if __name__=="__main__":
    B2=C.KerB()
    x1,y1,x2,y2=sy.symbols("x1,y1,x2,y2")
    print(B2(x1,y1,x2,y2))

#%%

if __name__=="__main__":
    print(N1.kind(1,0))
    print(N1.kind(6,0))
    print(N1.kind(6,1))



# %%

if __name__=="__main__":
    print(N1.kind(1))
    print(N1.kind(2))
    print(N1.kind(3))



# %%


if __name__=="__main__":

    plt.figure(figsize=(5,4))
    Newt.Grid(8,8)

    N=Newt([[0,0],[0,6],[1,6],[4,5],[5,4],[6,3],[7,1],[7,0],[4,3],[1,4],[2,5],[1,3],[5,1]])
    N.plotBord(color="green")
    N.plot(color="r")

    plt.plot([1,5,1,1],[3,1,1,3],"-b")
    plt.plot([2],[2],"D",color="purple")
    plt.plot([3],[2],"D",color="purple")

    # Newt.plotdroite([1,6],[4,5])


    # Newt.plotdemiplan([1,6],[4,5],alpha=0.2)

    L=[p for p in N.bord() if not ((p[0]<N.boundingBox()[0] and p[1]==0) or (p[1]<N.boundingBox()[1] and p[0]==0) )]
    for i in range(len(L)-1):
        Newt.plotdroite(L[i],L[i+1])
        Newt.plotdemiplan(L[i],L[i+1],alpha=0.2)


# plt.savefig(savepath+"triangles.png")

# %%
