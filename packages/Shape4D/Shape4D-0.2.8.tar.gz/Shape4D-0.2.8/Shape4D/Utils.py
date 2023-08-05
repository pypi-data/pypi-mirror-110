# from __future__ import absolute_import
from matplotlib import path 
import numpy as np
from .Constant import get_eps,get_sig_figures

### Computation on the intersection of 3D Lines and 3D Polygons
'''
    All vertices follow the form of numpy.array(N,3)
'''
# Vectors

def Repmat(M,m,n):          # matlab alternative to broadcasting of Python
    return np.tile(M,(m,n)) 

def Array(x):
    return np.array(x)

def MatShape(v):
    ret = v.shape
    n = len(v)
    if len(ret) == 1:
        ret = (1,n)
    return ret
    
def Cross(u,v):
    return np.cross(u,v)

def Dot(u,v):
    return np.dot(u,v)

def Inv(Matrix):
    return np.linalg.inv(Matrix)

def Det(Matrix):
    return np.linalg.det(Matrix)

# Fast Version
def Length(v):
    return np.sqrt(v.dot(v))

def UnitVector(v): 
    return v/Length(v)   

def Mask(v,bSelected):
    """
    It returns an array made of elements selected ( bSelected == True ).
    """
    P = np.array(v)
    return P[bSelected]

# To check whether the two vectors are equal. If they are,  it returns True
def Equal(a,b):
    return np.all(Round(a)==Round(b))

def Round(x):
    return np.round(x, get_sig_figures())

def ScalarEqual(a,b):
    return Round(abs(a-b))<=get_eps()

def ScalarZero(x):
    return ScalarEqual(x,get_eps())

# Vertices 
def Vertices(x):
    return Array(x)

# Intersection point of two 3D Lines with theri own points and slopes.
# It returns, 
# (1)Array（P), intersection point; 
# (2)None, they are in parallel; 
# (3)‘Line’, they are one; 
# (4)None, they are different in 3D space. 

def LineXLine(P1,L1,P2,L2):
    # Normalize them
    L1  = UnitVector(np.array(L1))
    L2  = UnitVector(np.array(L2)) 
    C, D = Array(P1), Array(P2)
    CD = D - C
    e,f  = Array(L1), Array(L2)
    X = Cross(f,CD)
    Y = Cross(f,e)
    # To check if they are zeros
    if(np.linalg.norm(X) <= get_eps() and np.linalg.norm(Y)  <= get_eps()):
        return 'colinear'
    else:
        if((np.linalg.norm(Y)) <= get_eps() ):
            return None
        else  :
            Z = Dot(X,Y)
            sign = 1 if Z>0 else -1
            M = C + sign * Length(X)/Length(Y) * e
            if PointInLine(M,P1,L1)==False or PointInLine(M,P2,L2)==False:
                return None
            else:
                return M

# To check if the point P0 is on the 3D line(P,L), Ture/False
def PointInLine(P0,P,L):
    V0 = Array(P0)
    V  = Array(P)

    L1 = UnitVector( V0 - V)
    Lx = UnitVector(Array(L))
    if Equal(L1, Lx) or Equal(L1, (-1)*Lx):
        return True
    else:
        return False



# To check if  P is inside a segement(P1,P2), Ture/False
def PointInSegment(P,P1,P2):
    pos = np.vstack((P1, P2))
    pos = np.array([np.min(pos[ :, :], axis=0),
                    np.max(pos[ :, :], axis=0)])
    return np.all(P>=pos[0,:]) & np.all(P<=pos[1,:])


# 3D Polygons
'''
   Core concern : intersection. 
   That is, a line of slop (L) from a point (P0) is intercepted with a Polygon.
   The process is decoupled into two steps :
        (1) the line cross a plane;
        (2) their intersection point falls in the polygon, including the border.

           P0 =np.array((x0,y0,z0))
           L  = np.array((dx,dy,dz))
           Polygon = np.array(
                                [x1 y1 z1],
                                [x2 y2 z2],
                                ...
                                [xm ym zm])
'''
# Intersection of a segement (P1,P2) with a polygon
def SegmentXPolygon(P1,P2,polygon):
    L  = UnitVector(np.array(P2) - np.array(P1))
    P0 = P1

    Point = LineXPolygon(P0,L,polygon)

    if Point is None :
        return None
    else :
       if PointInSegment(Point,P1,P2):
           return Point
       else :
           return None

# Intersection of a segement (x1,y1),(x2,y2) with a 2D line.
# It returns :
# (1) Array（P), intersecting point;
# (2) None, No intersection;
# (3) ‘Line’, the segment if part of the line
def LineXSegment2D(P0,L,x1,y1,x2,y2):
    P1,L1,P2=(x1,y1),(x1-x2,y1-y2),(x2,y2)
    L1  = UnitVector(np.array(L1))
    if np.linalg.norm(L1) <= get_eps():
        return None
    else:
        P=LineXLine(P0,L,P1,L1)  
        if P is None:
            return None
        elif P == 'colinear':
            return P
        else:
            if PointInSegment(P,P1,P2): 
                return P
            else:
                return None

# Intersection of line with polygon in 2D space.
# It returns a pair of values as follow,
#(1) P1，None : one intersection point
#(2) None，None : no intersection
#(3) P1，P2 : two intersection points
def LineXPolygon2D(P0,L,Polygon):
    L=UnitVector(L) 
    n = len(Polygon)
    IS = 0
    P1=None
    P2=None
    for i in range(n):
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]
        P = LineXSegment2D(P0,L,x1,y1,x2,y2)  # to check its intersection with each edge of the polygon
        if P is None :
            pass
        elif P == 'colinear':                       # the edge is part of line
            P1,P2=(x1,y1),(x2,y2)
            return P1,P2
        else:
            if P1 is None:
                P1=P
            elif np.linalg.norm(P-P1) <= get_eps():
                pass  
            else:
                P2=P
                return P1,P2

       
    if P1 is None :
        return None,None
    else:
        return P1,None

# In 3D space, intersection of a line with a polygon
# It return a pair of follwoing values ,
# (1) P1, the intersection point;
# (2) None, no intersection;
# (3) 'colinear', plus a warning message on console: there are two points of intersection
def LineXPolygon(P0,L,Polygon):
    n = PolygonNormal(Polygon)          # [dx,dy,dz] 
    R0 = np.array(Polygon[0,:])          # [x,y,z]
    Point = LineXPlane(P0,L,R0,n)          # intersection of line with plane

    if Point is None:
        return None
    if Point == 'colinear':                # If the line lies in the plane, it goes into 2D space
        PL=P0+L
        P03D,Polygon3D,U,R0=D3ToD2(P0,Polygon)                      ##从三维矩阵变成二维
        PL3D,Polygon3D,U,R0=D3ToD2(PL,Polygon)
        Polygon2D = Polygon3D[:,0:2]
        L3D=P03D-PL3D
        P02D=P03D[0:2]
        L2D= L3D[0:2]
        P1,P2=LineXPolygon2D(P02D,L2D,Polygon2D)
        if P1 is None and P2 is None:
            return None
        elif P2 is None:
            P1=D2toD3Point(P1,U,R0)
            return P1
        else:
            P1=D2toD3Point(P1,U,R0)
            P2=D2toD3Point(P2,U,R0)
            print('intesection leaves a segment of ',np.around(P1, decimals=3, out=None),np.around(P2, decimals=3, out=None))
            return 'colinear', P1, P2
    if PointInPolygon(Point,Polygon) :
        return Point
    else :
        return None

# Intersection of a 3D line with a 3D plane
# It returns
# (1) P1
# (2) None
# (3)‘Line’, the line is one the plane

def LineXPlane(P0,L,R0,n):
    L = UnitVector(L) 
    n_dot_L = Dot(n,L)
    dP = R0 - P0                         # [dx,dy,dz]

    if ScalarZero(n_dot_L):
        if ScalarZero(Dot(dP,dP)) or ScalarZero(Dot(dP,n)):
            return 'colinear'
        else:
            return None

    x  = Dot(n,dP)/n_dot_L
    P  = P0 + x*L                         # [x,y,z]
    return P


# transformation from 3D to 2D
def D3ToD2(Point,Polygon):
    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    P  = Array(Point)
    r = U@(R - R0).T  # @ is for vector times matrix
    p = U@(P - R0).T
    xy=p.T
    vertices3D = r.T
    vertices2D = r.T[:,0:2]
    return xy,vertices3D,U,R0

# transformation from 2D to 3D : polygon
def D2toD3Polygon(Polygon,U,R0):
    r=Polygon.T
    U=np.mat(U)
    U=U.I
    R=(U@r).T+R0
    return R

# transformation from 2D to 3D : Point
def D2toD3Point(Point,U,R0):
    Point3D=np.array([[Point[0]],[Point[1]],[0]])
    p=Point3D
    U=np.mat(U)
    U=U.I
    R=(U@p).T+R0
    return R

# To check if a single point lies in a polygon, True/False
def PointInPolygon(Point,Polygon):
    p,vertices3D,U,R0=D3ToD2(Point,Polygon)
    z=p[2]
    vertices2D = vertices3D[:,0:2]
    if ScalarZero(z) :                  # In local 2D coordiates, if z = 0 , the point is in the plane
        xy = p[0:2]   # first two columns 
        return PointInPolygon2D(xy[0], xy[1], vertices2D)
    else :
        return False

# To check if many points lie in a polygon, True/False
def PointsInPolygon(Points,Polygon):
    Points = np.array(Points)

    # set it unitary
    j=0
    if Points.ndim == 1:
        return PointInPolygon(Points,Polygon)
    elif Points.ndim ==3:
        j=1
        dimen = Points.shape
        a=dimen[0]
        b=dimen[1]
        Points = Points.reshape(int(a*b),3)

    U  = GetU(Polygon)
    R  = Array(Polygon)
    R0 = Array(Polygon[0,:])
    Ps = Array(Points)
    r  = U@(R - R0).T
    p  = U@(Ps - R0).T
    n  = len(p[0])                   # to check is z == 0
    ret = np.array(list(False for i in range(n)))

    for i in range(n):
        if ScalarZero(p[2,i]):
            ret[i] = True

    xy = (p[0:2]).T   # first two columns 
    vertices2D = r.T[:,0:2]
    if j == 1:
        ret = ret.reshape(a,b)
        xy = xy.reshape(a,b,2)
    ret = ret*PointsInPolygon2D(xy, vertices2D)
    return ret

# multiple points in a polygon : variant method 0
def PointsInPolygon0(Points,Polygon):
    Points = np.array(Points)
    ret=[]
    if Points.ndim ==2:
        for i,point in enumerate(Points):
            ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        return ret
    elif Points.ndim ==3:
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret.append(PointInPolygon(point,Polygon))
        ret=np.array(ret)
        ret = ret.reshape(i+1,j+1)
        return ret
    else:
        return None

# multiple points in a polygon : variant method 1
def PointsInPolygon1(Points,Polygon):
    Points = np.array(Points)
    if Points.ndim ==2:
        n=len(Points)
        ret = np.array(list(False for i in range(n)))
        for i,point in enumerate(Points):
            ret[i]=(PointInPolygon(point,Polygon))
        return ret
    elif Points.ndim ==3:
        n=len(Points)
        m=len(Points[0])
        ret = np.array(list(False for i in range(n*m)))
        ret = ret.reshape(n,m)
        for i,points in enumerate(Points):
            for j,point in enumerate(points):
                ret[i,j]=(PointInPolygon(point,Polygon))
        return ret
    else:
        return None


# multiple points in a polygon : 2D space only
def PointsInPolygon2D(Points,Polygon,Method='Custom'):
    from functools import reduce
    from operator import mul

    Vertices = Points
    if type(Points) is not np.array:
        Vertices = Array(Points)

    # Single Point
    # 1) input as np.array([7,8]), shape =(2,)
    if len(Vertices.shape) == 1 :
        x0 = Vertices[0]
        y0 = Vertices[1]
        ##print(x0,y0,Polygon)
        ret = PointInPolygon2D(x0,y0,Polygon) 
        return ret

    # 2) input as np.array([(7,8)]), shape = (1,2)
    elif (len(Vertices.shape) == 2 and Vertices.shape[0] == 1) : 
        x0 = Vertices[0][0]
        y0 = Vertices[0][1]
        ret = PointInPolygon2D(x0,y0,Polygon)
        return ret

    # Multiple Points
    shape = np.shape(Vertices)    #  0,...,n-1
    matrix_shape = shape[0:-1]  #  0,...,n-2, excluding shape[-1]
    n = reduce(mul, matrix_shape, 1)   #  how many points
    Points_array = Vertices.reshape(n,shape[-1])  # 1D array of (x,y,z).

    key_str = Method.lower()
    
    if key_str == 'custom':
        ret = _PointsInPolygon2D_Custom(Points_array,Polygon)
    elif key_str == 'matplotlib':
        ret = _PointsInPolygon2D_Matplotlib(Points_array, Polygon)

    return ret.reshape(matrix_shape)

# help functions 
def _PointsInPolygon2D_Custom(Points,Polygon):

    n = len(Points)
    ret = np.array(list(False for i in range(n)))
    for i in range(n):
        x0,y0  = Points[i]
        ret[i] = PointInPolygon2D(x0,y0,Polygon)   
    return ret

def _PointsInPolygon2D_Matplotlib(Points,Polygon):
    row = len(Polygon)   # row = N, Polygon = N x 2   
    
    # Inside
    edge = path.Path([(Polygon[i,0],Polygon[i,1]) for i in range(row)])
    ret  = edge.contains_points(Points)    
    
    # print(ret)
    # On edge
    if not all(ret) :        
        n = len(Points)
        for i in range(0,row):
            j = (i+1)%row 
            x1,y1 = Polygon[i]
            x2,y2 = Polygon[j]
            dy = y2-y1
            dx = x2-x1
           
            for k in range(n):
                if ret[k] :
                    continue          
                
                x0,y0 = Points[k]
                if not ScalarZero(dy):
                    if min(y1,y2) <= y0 and y0 <= max(y1,y2) :                        
                        x = x1 + (y0-y1)*dx/dy   # any slant line, including vertical line
                        if ScalarEqual(x,x0) :
                            ret[k] = True
                            
                elif not ScalarZero(dx):    # horizontal line
                    if min(x1,x2) <= x0 and x0 <= max(x1,x2) :
                        if ScalarEqual(y1,y0):
                            ret[k] = True
                                     
    # inside + on Edge
    return ret

# a 2D point inside a 2D polygon, it return True/False
def PointInPolygon2D(x0,y0,Polygon):
    """
       return value :
         True,  (XO,YO) IS LOCATED BOTH IN Polygon and ON EDGE
         False, (XO,YO) FAILS TO DO SO
    """
    if type(x0) is np.ndarray or type(y0) is np.ndarray :
        raise ValueError(f"PointInPolygon2D(x0,y0,Polygon)\n"
            "x0,y0 need be scalar value, but be given array.")

    n = len(Polygon)
    IS = 0
    for i in range(n):
        x1,y1 = Polygon[i]
        x2,y2 = Polygon[(i+1)%n]
        I = PointInSegment2D(x0,y0,x1,y1,x2,y2)
        # print(f" {loc[I]} of line = ({x1},{y1}) - ({x2},{y2})  ")
        if I == 1 :    
            IS += 1    #  x0 < x_predicted
        elif I == 2 :  # on edge
            return True
        
    ret = IS%2
    if ret == 1 :
        return True
    else:
        return False

    """
    Starting from a point P0, a ray goes to the right.
        INTERSECTION ?
            ret=O  NO  ( no any intersection with edges )
            ret=1  YES ( There is one intersection point, P0 is internal.) 
            ret=2  YES ( P0 is ON EDGE ) 
    """
    # ymin < y0 < ymax 
def PointInSegment2Dold(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ScalarEqual(min(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   
    #    if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) in the condition that all intersection occurs by the right
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            if not ScalarEqual(x1, x2) : # x1 != x2 :
                x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
                if  ScalarEqual(x0, x) :  # x0 == x :
                    return 2
                
                if x0 < x :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            
                return 0
            
            else:        # vertical line
                if ScalarEqual(x0,x1) :
                    return 2
                
                elif x0 < x1 :
                    if ScalarEqual(min(y1,y2) , y0):
                        return 0
                    else:
                        return 1            

                else :               # x0 > x1 :
                    return 0
               
        else:  # horizontal line
            if not ScalarEqual(y0 , y1) :
                return 0

            elif ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
    else:
        return 0

def PointInSegment2D(x0,y0,x1,y1,x2,y2):
    if ScalarEqual(max(y1,y2),y0) or ((max(y1,y2)>y0) & ( y0>min(y1,y2))):   
    #  if (max(y1,y2)>=y0) & ( y0>=min(y1,y2)) in the condition that all intersection occurs by the right
        if not ScalarEqual(y1 , y2) :   # y1 != y2 :
            x=x1+(y0-y1)*(x2-x1)/(y2-y1)   # predicted point
            if  ScalarEqual(x0, x) :  # x0 == x :
                return 2
            if x0 < x :
                return 1 
            return 0
               
        else:  # horizontal line
            if ScalarEqual(x1,x0) or ScalarEqual(x0,x2) or max(x1,x2)>x0 and x0>min(x1,x2) :  #  y1 == y0
                return 2
            return 0
    elif ScalarEqual(min(y1,y2) , y0):
        if ScalarEqual(min(y1,y2) , y1):
            if ScalarEqual(x1,x0):
                return 2
            else:
                return 0
        else:
            if ScalarEqual(x2,x0):
                return 2
            else:
                return 0
    else:
        return 0

# To obtain a normal unitary vector of a polygon
def PolygonNormal(v):
    """
       get a vector normal to the polygon 
       parameter : v
                     np.array(M,3)
    """
    #
    #   C = A x B 
    #
    A = v[1,:] - v[0,:]
    B = v[2,:] - v[1,:]
    C = Cross(A,B)
    
    return UnitVector(C)

# To obtain a transformation of a polygon from its 3D to 2D
def GetU(polygon):
    """
        Get transform matrix of a polyogn
            U = GetU(polygon)
        Parameter :
            polygon : vertices of np.array(M,3)
    """
    v = polygon 

    a = v[1,:] - v[0,:]
    b = v[2,:] - v[1,:]
    c = Cross(a,b)

    # show("a",a)
    # show("b",b)
    # show("c",c)

    #   unitary vectors 
    i = UnitVector(a)
    k = UnitVector(c)
    j = Cross(k,i)

    # show("i",i)
    # show("j",j)
    # show("k",k)

    U = np.vstack((i,j,k))

    # show('U',U)

    return U


# element-wise view factor
def fij(P1, P2, n1, n2, A2 ):
    '''
    P1,P2 : centers of two elements, np.array([x,y,z])
    n1,n2 : unit vectors of the two elements, np.array([x,y,z])
    A2 : the area.of receiving element
    '''
    dP = P1 - P2
    S  = np.sqrt(dP.dot(dP))
    
    V12 = P2 - P1
    V21 = P1 - P2
    d1 = V12.dot(n1)
    d2 = V21.dot(n2)
    
    f12 = d1*d2*A2/( np.pi* S*S*S*S)
    
    return f12


#
#  Demo how to use them
#
def test_PointsInPolygon2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]

    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(Points, polygon)
    print(ret)
    print(Points[ret])

def test_PointsInPath2D():
    P = [(7,8),(6.5,7.7),(10,5),(10,11),(7,13),(6,-1),(5,5),(10,10),(10,5),(5,10)]
    vertices = [(5,5),(5,10),(10,10),(10,5)]
    Points = np.array(P)
    polygon = np.array(vertices)
    ret = PointsInPolygon2D(P, polygon, Method = 'Matplotlib')
    print(ret)
    print(Points[ret])

def main():
    test_PointsInPolygon2D()
    test_PointsInPath2D()

if __name__ == '__main__':
    main()
