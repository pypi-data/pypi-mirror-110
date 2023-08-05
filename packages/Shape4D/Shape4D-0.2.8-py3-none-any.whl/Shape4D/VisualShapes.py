import numpy as np
import matplotlib._color_data as mcd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
import matplotlib.pylab as plt

from .Utils import UnitVector, PolygonNormal, SegmentXPolygon, PointInLine,PointInPolygon, GetU
from .Utils import Equal, PointInSegment
from .Shapes import regularPolygon, createShape
from .Shapes import add_col # as arange_col  # add_third_col
from .Shapes import move as change
from .Constant import get_eps,get_sig_figures

### 3D View Function of a Geometry 
#
#  Its plotting follows the strategy of pyny3D
#  Liqun He, 2020/10/27
#

class Plotable(object):
### Initialization
    fig   = None
    ax    = None

    """
    It adds the Plotable in matplotlib to a geometry.
    
    Global methods defined here:
        `plot`
        `get_centroid`
        `copy`
        `save`
        `restore`
    
    Local methods needed in subclasses:
        `get_instance()`      returns the working object to be plotted
        `iplot()`             for plotting specific data 
        `set_view_domain()`   getting its specific view range
        
    """
    def __init__(self):
        self.backup = None
        self.facecolor ='xkcd:beige'
        self.edgecolor ='olive'
        self.color     ='darkgreen'  # for Point/Segement/Line/Polyline
        self.linewidth = 1
        self.linestyles="solid"
        self.alpha     = 1
        self.marker    ='o'

### the framework for plotting
    def set_ax(self, ax):
        self.__class__.ax = ax

    def get_ax(self):
        return self.__class__.ax

    def draw_origin(self):
        ax = self.get_ax()
        if ax is None :
            return

        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        zmin, zmax = ax.get_zlim()

        # Make the grid
        x = [xmin, xmin, xmin]
        y = [ymin, ymin, ymin]
        z = [0,0,0]   #[zmin, zmin, zmin]
        
        
        # Make the direction data for the arrows
        u = [1,0,0]
        v = [0,1,0]
        w = [0,0,1]
        
        ax.quiver(x, y, z, u, v, w, length=0.2, normalize=True)

    def show(self, elev= 10.0, azim = 122.0):
        ax = self.get_ax()
        if  ax is None :
            return

        ax.view_init(elev, azim)
        plt.show()
        return ax

    def add_plot(self, shape, style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'},
                       hideAxes=False, **kwargs):

        if not isinstance(shape, Plotable):
            return None

        return shape.plot(style = style, ax = self.get_ax(), 
            hideAxes=hideAxes,**kwargs)


    def plot(self, style = {'facecolor':'default','edgecolor':'default','linewidth':'default','alpha':'default'}, ax = None, 
                   hideAxes = False, **kwargs):
        """
        3D visualization with the following parameters, 
        Inputs:
         1) style :
              style = {'facecolor','edgecolor','linewidth','alpha','node','nodemarker','nodecolor'}
              It matters differently for line and polygon 
                = (edge color, line width, alpha) for segement, line, polyline and Ray
                = (face color, edge color, alpha) for polygon
                = ( node, node color, node marker) for point
         2) ax: 
              None : to plot the current plot in a new figure
              ax :   to plot the current plot in the "ax" (mplot3d.Axes3D) 

         3) hideAxes : hide axes or not

        Outputs:
              plt, ax
              
        Note :
            plt.show() finally lets all plots visible
        """

        bOverlapping = True     # adding multiple geometries
        if ax is None: 
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            self.__class__.ax = ax
            bOverlapping = False

        # fetch the instance of a geometry
        # instance = self.__class__(**self.get_seed())
        instance = self.get_instance()

        # instance's domain 
        domain = instance.get_domain()

        bound = np.max(domain[1]-domain[0])
        centroid = instance.get_centroid()
        pos = np.vstack((centroid-bound/2, centroid+bound/2))
        pos[0,2] = domain[0,2]
        pos[1,2] = pos[0,2] + bound
        
        # Overlap the existing plots 
        if bOverlapping :
            old_pos = np.array([ax.get_xbound(),
                                ax.get_ybound(),
                                ax.get_zbound()]).T
            pos = np.dstack((pos, old_pos))
            pos = np.array([np.min(pos[0, :, :], axis=1),
                            np.max(pos[1, :, :], axis=1)])


        # Plot instance
        if 'facecolor' not in style : style['facecolor'] = 'default' 
        if 'edgecolor' not in style : style['edgecolor'] = 'default' 
        if 'linewidth' not in style : style['linewidth'] = 'default' 
        if 'alpha'     not in style : style['alpha']     = 'default' 


        if style['facecolor'] == 'default' : style['facecolor'] = self.facecolor
        if style['edgecolor'] == 'default' : style['edgecolor'] = self.edgecolor
        if style['linewidth'] == 'default' : style['linewidth'] = self.linewidth
        if style['alpha']     == 'default' : style['alpha']     = self.alpha    

        instance.iplot(style = style, ax = ax, **kwargs)

        # Axis limits
        ax.set_xlim3d(left  =pos[0,0], right=pos[1,0])
        ax.set_ylim3d(bottom=pos[0,1], top  =pos[1,1])
        ax.set_zlim3d(bottom=pos[0,2], top  =pos[1,2])

        if hideAxes :
            ax.set_axis_off()
            self.draw_origin()

        else :
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')

        return ax

            
    def center_plot3d(self):
        """
        Help function for a derived class to manage cascade representation
        of multiple geometries, by keeping the aspect ratio 
        in a 3D representation.
        
        ax : 
            mplot3d.Axes3D for the management.

        return value: None
        """
        ax = self.get_ax()
        if not ax : return

        # Domain
        domain = self.get_domain()
        bound = np.max(domain[1]-domain[0])
        centroid = self.get_centroid()
        pos = np.vstack((centroid-bound/2, centroid+bound/2))

        # Axis limits
        ax.set_xlim3d(left=pos[0,0], right=pos[1,0])
        ax.set_ylim3d(bottom=pos[0,1], top=pos[1,1])
        ax.set_zlim3d(bottom=pos[0,2], top=pos[1,2])

        return Plotable.plt

    def get_centroid(self):
        """
        The centroid refers to the center of the circumscribed
        paralellepiped, not its mass center.
        
        it returns a ndarray of (x, y, z).
        
        """
        return self.get_domain().mean(axis=0)

### root methods for any geometry : `copy`, `save`, `restore`
    def copy(self):
        """
        a help function for deepcopy of its entire instance.
        """
        import copy
        return self.__class__(**copy.deepcopy(self.get_seed()))
        
    def save(self):
        """
        It saves a deepcopy of the current state of the instance. 
        restore() will return this copy.
        """
        self.backup = self.copy()
        
    def restore(self):
        """
        it returns last saved version of this object.
        """
        if self.backup is not None:
            return self.backup
        else:
            raise ValueError('No backup previously saved.')


### Classes for Point, Segement, Line, PolyLine, and Polygon, 
#     as well as Ray variant of PolyLine for solar ray tracking.

class Point(Plotable):
### Initilization
    def __init__(self, *args):
        self.set_point(*args)
        super().__init__()

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def __repr__(self):
        return "Point({}, {}, {})".format(
                self.x,
                self.y,
                self.z)

    def __eq__(self, other):
        # return self.x == other.x and self.y == other.y and self.z == other.z
        return isinstance(other, type(self)) and self.close_to(other)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __rmul__(self, c):
        return Point(c * self.x, c * self.y, c * self.z)

    def __mul__(self, c):
        return self.__rmul__(c)

    def __getitem__(self, item):
        """return one of x,y,z"""
        return (self.x, self.y, self.z)[item]

    def __setitem__(self, item, value):
        """set one of x,y,z of a Point"""
        setattr(self, "xyz"[item], value)

    @property
    def coordinates(self):
        return np.array([self.x, self.y, self.z])

    @coordinates.setter
    def coordinates(self, *args):
        self.set_point(*args)

    def set_point(self,*args):
        if len(args) == 1:
            # for initialisation by Vector 
            coords = args[0]
            if len(coords)==3 :
                self.x, self.y, self.z = coords[0],coords[1],coords[2]
            
            elif len(coords)==2 :
                self.x, self.y, self.z = coords[0],coords[1],0.0
            
            else:
                raise ValueError("Point() needs 2 or 3 values")
        else :
            self.x = args[0]
            self.y = args[1]
            if len(args) == 3 :
                self.z = args[2]
            else :
                self.z = 0

    def close_to(self, that):
        return self.distance_to(that) < get_eps()

    def distance_to(self, that):
        dx = self.x - that.x
        dy = self.y - that.y
        dz = self.z - that.z
        sqrDist = dx * dx + dy * dy  + dz * dz
        return np.sqrt(sqrDist)
        
    def move(self, offset):
        if isinstance(offset,list) or isinstance(offset,tuple) or isinstance(offset,np.array) :
            self.x += offset[0]
            self.y += offset[1]
            self.z += offset[2]
            return Point(self.x,self.y,self.z)
        else:
            raise NotImplementedError("move(offset) : offset must be (dx,dy,dz)")

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax, **kwargs):
        # defaul setting

        color  = style['color']  if 'color' in style else self.color  
        marker = style['marker'] if 'marker'in style else self.marker  
        alpha  = style['alpha']  if 'alpha' in style else self.alpha  

        if ax is None:
            ax = self.get_ax()

        ax.scatter(self.x, self.y, self.z, alpha=alpha, c=color, marker=marker)

    def get_domain(self) :
        ax = self.get_ax()
        # np.array([ax.get_xbound(),ax.get_ybound(), ax.gey_zbound()])
        xlower, xupper = ax.get_xbound()
        width = xupper - xlower
        if self.x <= xlower or self.x >= xupper: 
            xlower = self.x - 0.5*width
            xupper = self.x + 0.5*width

        ylower, yupper = ax.get_ybound()
        width = yupper - ylower
        if self.y <= ylower or self.y >= yupper : 
            ylower = self.y - 0.5*width
            yupper = self.y + 0.5*width

        zlower, zupper = ax.get_zbound()
        width = zupper - zlower
        if self.z <= zlower or self.z >= zupper: 
            zlower = self.z - 0.5*width
            zupper = self.z + 0.5*width

        domain = np.array([(xlower,xupper ), 
                           (ylower,yupper ),
                           (zlower,zupper )])
        return domain.T

class Segment(Plotable):  # segment
### Initialization
    """
      It run across both P1 and P2
    """
    def __init__(self, *points):

        if len(points) == 1:
            if len(*points) < 2 :
                raise ValueError("Segment must have at least 2 points.")

        self.p1 = self.set_point(points[0])
        self.p2 = self.set_point(points[1])
 
        super().__init__()

    def __str__(self):
        return f"{self.P1} -> {self.P2}"

    def __repr__(self):
        # type: () -> str
        class_name = type(self).__name__
        return f"{class_name}({self.P1}, {self.P2})"

    def __eq__(self, other):
        if isinstance(other,Segment):
            return  other.p1 == self.p1 and self.p2 == other.p2
        else:
            return False

    def __hash__(self):
        return hash(
        round(self.P1[0],get_sig_figures()),
        round(self.P2[1],get_sig_figures()),
        round(self.P1[0] * self.P2[1] - self.P1[1] * self.P2[0], get_sig_figures()))

    def __contains__(self, other):
        """Checks if a point on the line of segment"""
        if isinstance(other, Segment):
            return None 

        P0 = other
        if isinstance(other,Point):
            P0 = other.coordinates

        return PointInSegment(P0,self.P1,self.P2)

    def set_point(self,x):
        if isinstance(x,Point):
            p = x
        else :
            p = Point(*x)

        return p

    @property
    def P1(self):
        return self.p1.coordinates
 
    @property
    def P2(self):
        return self.p2.coordinates

    @P1.setter
    def P1(self, xyz):
        self.p1 = self.set_point(xyz)

    @P2.setter
    def P2(self, xyz):
        self.p2 = self.set_point(xyz)

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def iplot(self, style, ax,**kwargs):
        color     = style['color']     if 'color'     in style else self.color
        linewidth = style['linewidth'] if 'linewidth' in style else self.linewidth 
        alpha     = style['alpha']     if 'alpha'     in style else self.alpha

        # import mpl_toolkits.mplot3d as mplot3d
        xs = self.p1.x, self.p2.x 
        ys = self.p1.y, self.p2.y
        zs = self.p1.z, self.p2.z
        # line = mplot3d.art3d.Line3D(xs, ys, zs)
        vertices = list(zip(xs, ys, zs))
        line = Line3DCollection([vertices],colors=color,linewidths=linewidth, alpha=alpha)

        if ax is None:
            ax = self.get_ax()

        ax.add_collection3d(line)

    def get_domain(self):
        points = np.array([(self.p1.x,self.p1.y,self.p1.z), 
                           (self.p2.x,self.p2.y,self.p2.z)])
        return np.array([points.min(axis=0),points.max(axis=0)])

### Functions
    def midpoint(self):
        P = self.p1 + self.p2
        return 0.5*P

    def length(self):
        d = self.p2 - self.p1
        d = np.array([d.x,d.y,d.z]) 
        return np.sqrt(d.dot(d))

    def direction(self):
        return UnitVector(self.P2 - self.P1)

class Line(Segment):  # drawn as a special triangle, making full use of polygon shading in matplotlib.
    def __init__(self, *points):
        super().__init__(*points)
        
    def iplot(self, style, ax, **kwargs):

        color     = style['color']     if 'color'     in style else self.color
        linewidth = style['linewidth'] if 'linewidth' in style else self.linewidth 
        alpha     = style['alpha']     if 'alpha'     in style else self.alpha
        node      = style['node']      if 'node'      in style else 'invisible'
        nodecolor = style['nodecolor'] if 'nodecolor' in style else 'r'
        marker    = style['marker']    if 'marker'    in style else 'o'

        p = self.midpoint()

        xs = self.p1.x, p.x, self.p2.x 
        ys = self.p1.y, p.y, self.p2.y
        zs = self.p1.z, p.z, self.p2.z

        vertices = list(zip(xs,ys,zs))
     
        line = Poly3DCollection([vertices],edgecolors=color,linewidths=linewidth, alpha=alpha)

        if ax is None:
            ax = self.get_ax()

        ax.add_collection3d(line)

        if node is 'visible':
            ax.scatter(self.p1.x, self.p1.y, self.p1.z, alpha=alpha, c=nodecolor, marker=marker)
            ax.scatter(self.p2.x, self.p2.y, self.p2.z, alpha=alpha, c=nodecolor, marker=marker)

class Polyline(Plotable):
### Initialization
    def __init__(self, start, *points):
        
        vertices = []
        vertices.append(start)

        for each in points :
            vertices.append(each)

        self.vertices = vertices     # an array of [x,y,z]
        self.lines = []              # a list of Line() created by two Point()

        if len(self.vertices)> 1:
            v1 = self.vertices[0]
            for v2 in self.vertices[1:]:
                line = Line(v1,v2)
                self.lines.append(line)
                v1 = v2        

        super().__init__()

    def __str__(self):
        s = f"There are nodes of {len(self.vertices)}.\n"
        s += str(self.vertices[0])
        for point in self.vertices[0:-1]:
            if s:
                s += " -> "
            s += str(point)

        return s

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, item):
        """return one of lines"""
        return self.lines[item]

    def __setitem__(self, item, value):
        """set one of Line """
        # setattr(self, "xyz"[item], value)
        print(f"item : {item}, value : {value}")

    def __hash__(self):
        return hash(tuple(sorted(self.vertices, key=lambda p: p.x)))

    @property
    def P1(self):
        return self.vertices[0]
 
    @property
    def P2(self):
        return self.vertices[-1]

    @P1.setter
    def P1(self, xyz):
        self.vertices[0] = xyz

    @P2.setter
    def P2(self, xyz):
        self.vertices[-1] = xyz

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def get_domain(self):
        """
        :returns: opposite corners of the bounding prism for this object.
        :       ndarray([min], [max])
        """
        # Min/max along the column
        vertices = np.array(self.vertices)
        return np.array([vertices.min(axis=0),  # min (x,y,z)
                         vertices.max(axis=0)]) # max (x,y,z)

    def iplot(self, style, ax,**kwargs):
        # style = {'node':'invisible','edgecolor':'default', ...}
        #                 'visible'               'gradient'
        # for 'gradient' 
        default_colors = ['darkgoldenrod', 'goldenrod','gold','khaki','darkkhahi','olive','oilvedrab','darkolivedrab','beige']
        colors = []

        bColors = 0 
        if style.get('color') is 'gradient' :
            bColors = 1

        if 'colors' in style :
            bColors = 2
            colors = style['colors']

        i=0
        for line in self.lines:

            if bColors == 1 :
                style['color'] = default_colors[i]
                i += 1
                i = i % len(default_colors)

            elif bColors == 2 :
                style['color'] = colors[i]
                i += 1
                i = i % len(colors)

            line.iplot(style, ax,**kwargs)

### Funcions
    def broken_by(self,v):
        if v is None:
            return None
        if isinstance(v,Point):
            v = v.coordinates

        if len(self.vertices) == 1:
            self.append(v)
            return 2

        elif len(self.vertices) >= 2:
            V,i = np.array(v),0
            P1  = np.array(self.vertices[0])
            for p2 in self.vertices[1:] :
    
                if Equal(V,P1) :
                    return None 

                P2 = np.array(p2)
                if PointInSegment(V,P1,P2):
                    if Equal(V,P2) :
                        return None 
    
                    self.insert_at(i+1,v)
                    return i+1
                i += 1
                P1 = P2

    def append(self, v):
        v1 = self.vertices[-1]
        v2 = v
        self.vertices.append(v)
        self.lines.append(Line(v1,v2))

    def insert_at(self,i,v):
        if i >= len(self.vertices):
            self.append(v)

        elif i == 0 :
            self.vertices.insert(0,v)
            v0 = self.vertices[0]
            v1 = self.vertices[1]
            self.lines.insert(0, Line(v0,v1))

        else:
            v0 = self.vertices[i-1]
            v1 = v
            v2 = self.vertices[i]
            self.vertices.insert(i,v)

            self.lines.pop(i-1)
            self.lines.insert(i-1, Line(v0,v1))
            self.lines.insert(i,Line(v1,v2))

    def intercept(self, polygon):
        if isinstance(polygon,Polygon):
            return polygon.intercept(self)
        else:
            return None

class Ray(Plotable):
### Initialization
    plot_style = None
    """
      It starts from P0 and runs in a direction of L(dx,dy,dz)
    """
    def __init__(self, P0, L):
        self.P0 = P0
        self.L  = L
        super().__init__()

    def __str__(self):
        return f"From {self.P0.P}, it runs in the direction of {self.L}"

    def __repr__(self):
        # type: () -> str
        class_name = type(self).__name__
        return f"{class_name}({self.P0}, {self.L})"

    def __eq__(self, other):
        return self.P0 == other.P0 and self.L == other.L

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def get_domain(self):
        ax = self.get_ax()
        xlower, xupper = ax.get_xbound()
        width = xupper - xlower
        if self.P0.x <= xlower : 
            xlower = self.P0.x - 0.5*width
            xupper = self.P0.x - 0.5*width
        if self.P0.x >= xupper :
            xlower = self.P0.x + 0.5*width 
            xupper = self.P0.x + 0.5*width

        ylower, yupper = ax.get_ybound()
        width = yupper - ylower
        if self.P0.y <= ylower : 
            ylower = self.P0.y - 0.5*width
            yupper = self.P0.y - 0.5*width
        if self.P0.y >= yupper : 
            ylower = self.P0.y + 0.5*width
            yupper = self.P0.y + 0.5*width

        zlower, zupper = ax.get_zbound()
        width = zupper - zlower
        if self.P0.z <= zlower : 
            zlower = self.P0.z - 0.5*width
            zupper = self.P0.z - 0.5*width
        if self.P0.z >= zupper :
            zlower = self.P0.z + 0.5*width 
            zupper = self.P0.z + 0.5*width

        domain = np.array([(xlower,xupper), (ylower,yupper), (zlower,zupper)])
        return domain.T

    def iplot(self, style, ax,**kwargs):
        if not kwargs :
            mode = "line"

        color     = style['color']     if 'color'    in style else self.color
        linewidth = style['linewidth'] if 'linewidth'in style else self.linewidth
        alpha     = style['alpha']     if 'alpha'    in style else self.alpha

        if ax is None:
            ax = self.get_ax()

        if mode == 'quiver':
            (x,y,z,u,v,w,length) = self.__set_plotable_data(mode)
            ax.quiver(x, y, z, u, v, w, length=length)
        else :
            vertices =  self.__get_plotable_line(mode)
            line = Line3DCollection([vertices],colors=color,linewidths=linewidth, alpha=alpha)
            ax.add_collection3d(line)

    def __get_plotable_line(self, mode):
        """
            returns: mplot3d.art3d.Line3DCollection
        """    
        # ray direction
        ax = self.get_ax()

        u = self.L[0]
        v = self.L[1]
        w = self.L[2]

        xmin,xmax = ax.get_xbound()
        ymin,ymax = ax.get_ybound()
        zmin,zmax = ax.get_zbound()

        x = xmin if u < 0 else xmax
        y = ymin if v < 0 else ymax 
        z = zmin if w < 0 else zmax  

        x = x if u != 0 else 0.0
        y = y if v != 0 else 0.0 
        z = z if w != 0 else 0.0 

        if mode == "quiver" :
            '''
               A ray is represented by a quiver from P0 to an edge of the figure.
            '''
            line = Line(self.P0,Point(x,y,z))
            length = line.length()
            ret = (self.P0.x,self.P0.y,self.P0.z,u,v,w,length)

        else :
            '''
               A ray is represented by a line from P0 to an edge of the figure.
            '''
            xs = self.P0.x, x
            ys = self.P0.y, y
            zs = self.P0.z, z
                
            vertices = list(zip(xs, ys, zs))
            ret = vertices

        return ret

class Polygon(Plotable):
### Initialization
    plot_style = None
    """
    A visible 3D polygon.
    It is iterable , and when indexed, it returns the vertices.
    
    The polygon's vertices are a ndarray of 3D points 
          np.array(N, 2 or 3) for (xyz or xy).

    It requires a open loop, the first point != the end point.

    NOTE:: In future, this object can be locked for calculation once,  
    for a rapid rendering.
    """
    verify = True
    def __init__(self, points, **kwargs):
        
        # Input errors
        if len(points) < 3:
            raise ValueError("Polygon must have at least three vertices.")

        if type(points) != np.ndarray:
           points = np.array(points)
                
        # Adapt 2D/3D
        if points.shape[1] == 2:
            # from Shapes import add_col
            points = np.hstack((points, add_col(points.shape[0])*0))

        elif points.shape[1] != 3:
            raise ValueError('VisualGeom.Polygon needs 2 or 3 coords '+\
                             '(columns) at least')

        # Basic processing
        self.vertices = points
        self.p = self.vertices[0]
        self.n = PolygonNormal(self.vertices)
        
        # Optional processing
        self.path = None
        self.parametric = None
        self.shapely = None
        
        # Parameters
        self.locked = False
        self.domain = None
        self.area = None
                

        super().__init__()

    def __str__(self):
        s = ""
        for point in self.vertices:
            if s:
                s += " -> "
            s += str(point)
        return s

    def __hash__(self):
        return hash(tuple(sorted(self.vertices, key=lambda p: p.x)))

    def __iter__(self): return iter(self.vertices)

    def __getitem__(self, key): return self.vertices[key]
        
    def lock(self):
        """
        It locks some polygons for calculation, 
        by using ``self.domain`` and ``self.path`` 

        ***warning***: Unnecessary locks can slow down the calculation.
        """
        if not self.locked:
            self.path = self.get_path()
            self.domain = self.get_domain()
            self.locked = True

    def to_2d(self):
        """
        To calculate the local coordinates of vertices.
        """

        # Create the matrix from global to local systems
        U = self.getU()
        # U = self.matrix()  # in future
        
        # Local coordiantes
        dR = self.vertices - self[0]   # The first vertice as the origin
        r = np.dot(U, dR.T).T
        r[np.isclose(r, 0.0)] = 0.0
        
        # print(r.shape)
        return Polygon(r[:, :2])
        
    def plot2d(self, style = ('wheat', 'yellowgreen', 1)):
        """
        It plots the 2D Polygon
        
        Inputs 
           1)style = color, edge_color, alpha ):
               (1)      color: 'default', matplotlib color for polygon
               (2) edge_color : 'k'     , matplotlib color for edge
        :      (3)       alpha:  1,      pacity, float
        :  2) ret: If True, the function returns the figure, so as to add 
                 more elements to the plot or to modify it.
        
        Output: 
          None or axes(matplotlib axes)
        """
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
        (color,edge_color,alpha) = style
        path = self.to_2d().get_path()
        domain = self.to_2d().get_domain()[:, :2]

        if color is 'default': color = 'yellowgreen'

        # Plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.add_patch(patches.PathPatch(path, facecolor=color, lw=1, 
                                       edgecolor=edge_color, alpha=alpha))
        ax.set_xlim(domain[0,0],domain[1,0])
        ax.set_ylim(domain[0,1], domain[1,1])

        return plt,ax

### Custom get_instance()/iplot()/get_domain()
    def get_instance(self): return self

    def seed2pyny(self, seed):
        return Polygon(**seed)

    def get_domain(self):
        """
        :returns: opposite vertices of the bounding prism for this object.
        :       ndarray([min], [max])
        """
        if self.domain is None:
            # Min/max along the column
            return np.array([self.vertices.min(axis=0),  # min (x,y,z)
                             self.vertices.max(axis=0)]) # max (x,y,z)
        return self.domain

    def iplot(self, style, ax, **kwargs):

        plotable3d = self.__get_plotable_data()

        facecolor = self.facecolor  
        edgecolor = self.edgecolor  
        linewidth = self.linewidth  
        alpha     = self.alpha      

        if 'facecolor' in style : facecolor = style['facecolor'] 
        if 'edgecolor' in style : edgecolor = style['edgecolor'] 
        if 'linewidth' in style : linewidth = style['linewidth'] 
        if 'alpha'     in style : alpha     = style['alpha']     

        for polygon in plotable3d:
            polygon.set_facecolor(facecolor)
            polygon.set_edgecolor(edgecolor)
            polygon.set_linewidth(linewidth)
            polygon.set_alpha(alpha)
            ax.add_collection3d(polygon)
    
    def __get_plotable_data(self):
        """
        :returns: matplotlib Poly3DCollection
        :rtype: mpl_toolkits.mplot3d
        """
        # import mpl_toolkits.mplot3d as mplot3d
        # return [mplot3d.art3d.Poly3DCollection([self.vertices])]
        return [Poly3DCollection([self.vertices])]

### Functions for geometry calculation
    def get_seed(self):
        """
        get the dict information  required by Polygon.as its arguments
        For Polygon(points)
        it returns arguments in dicttionary form :
                   {"points": vertices} 
        """
        return {'points': self.vertices}

    def intercept(self,segment) :
        if isinstance(segment, Segment) or isinstance(segment, Polyline):
            P1, P2 = segment.P1, segment.P2

        else :
            return None

        P = SegmentXPolygon(P1,P2,self.vertices)
        if P is None :
            return None
        else :
            return Point(P)
        

    def __contains__(self, other):
        if isinstance(other, Point):
            return PointInPolygon(other.coordinates,self.vertices)         # in polygon
           # return abs(other.V * self.n - self.p.V * self.n) < const.get_eps()  # in plane
        else:
            raise NotImplementedError("")
        
        # elif isinstance(other, Line):
        #     return Point(other.sv) in self and self.parallel(other)
        # elif other.class_level > self.class_level:
        #     return other.in_(self)
   # def contains(self, points, edge=True):
 
    #     P = self.to_2d( points )
    #     polygon = self.to_2d().get_path()
    #     return PointInPolygon2D(P[0],P[1],polygon.vertices[:,:2])

        # radius = 1e-10 if edge else -1e-10
        # return self.to_2d().get_path().contains_points(P[:, :2], radius=radius)
       

    def get_parametric(self, check=True, tolerance=0.001):
        """
        Calculates the parametric equation of the plane that contains 
        the polygon. The output has the form np.array([a, b, c, d]) 
        for:

        .. math::
            a*x + b*y + c*z + d = 0
        
        Inputs:
         check : whether or not the vertices are in the plane with *tolerance*.
         tolerance: float
        
        NOTE that this method automatically stores the solution to avoid calculation
                  more than once.
        """
        if self.parametric is None: 
            
            # Plane calculation
            a, b, c = np.cross(self.vertices[2,:]-self.vertices[0,:],
                               self.vertices[1,:]-self.vertices[0,:])
            d = -np.dot(np.array([a, b, c]), self.vertices[2, :])
            self.parametric = np.array([a, b, c, d])
                
            # Point belonging verification
            if check:
                if self.vertices.shape[0] > 3:
                    if np.min(np.abs(self.vertices[3:,0]*a+
                                     self.vertices[3:,1]*b+
                                     self.vertices[3:,2]*c+
                                     d)) > tolerance:
                        raise ValueError('Polygon not plane: \n'+\
                                         str(self.vertices))
        return self.parametric
        
    def get_path(self):
        """
        :returns: matplotlib.path.Path object for the z=0 projection of 
            this polygon.
        """
        if self.path == None:
            from matplotlib import path
            
            return path.Path(self.vertices[:, :2]) # z=0 projection!
        return self.path

    def get_area(self):
        """
        :returns: The area of the polygon.
        """
        if self.area is None:
            self.area = self.to_2d().get_shapely().area
        return self.area

### Functions to manipulate the polygon
    def getU(self):
        return GetU(self.vertices)

    def matrix(self, points = []):  # to replace GetU

        # if points == None :
        #     points = self.vertices
        # The first vertice is the origin of the local system
        #      dR = points - self[0]

        if type(points) != np.ndarray:
            points = np.array(points)

        if not points.size :
            points = self.vertices

        # Create the matrix from local to global systems
        a = points[1]-points[0]
        a = a/np.linalg.norm(a)                # arbitrary first axis
        n = np.cross(a, points[-1] - points[0])
        n = n/np.linalg.norm(n)                # normal axis
        b = -np.cross(a, n)                    # Orthogonal to the others
        U = np.array([a, b, n])
        U[np.isclose(U, 0.0)] = 0.0
    
        return U

class Shape(Polygon):
    def __init__(self, shape=None,W=None,H=None,A=None,B=None,C=None,D=None, **kwargs):

        points = self.createVertices(shape,W,H,A,B,C,D,**kwargs)
        if type(points) is not np.ndarray :
            points = np.array(points)
        super(Shape, self).__init__(np.array(points))

        # from matplotlib import path
        # self.path = path.Path(self.vertices[:, 1:3]) # x=0 projection!

    def createVertices(self,shape,W,H,A,B,C,D, **kwargs):    
        vertices = np.array([])
        P0 = (0.0,0.0,0.0)
        reference_index = 0

        if not shape : return

        self.input_str = ""
        self.shapeName = shape.lower()
        # print(self.shapeName)
        if self.shapeName == 'regularpolygon' :
            n=3
            R=1
            # print(kwargs)
            for key, value in kwargs.items():
                key_str = key.lower()
                if key_str == 'r':
                    R = value
                elif key_str == 'n':
                    n = value
                elif key_str == 'center':
                            # Input errors
                    if len(value) != 3:
                        raise ValueError('Model.Shape needs x,y,z for a regular polygon center')
                    else :
                        P0 = value
                        # print(P0)

            vertices = regularPolygon(n,R,P0)
            input_str = f"'{shape}',n={n},R={R},center={P0}"

        elif self.shapeName == 'polygon' :

            for key, value in kwargs.items():
                key_str = key.lower()
                if key_str == 'vertices':
                    
                    # value = {'vertices':[(0,0),(1,0),(0.6,0.5)]}

                    if type(value) is list:
                        vertices = np.array(value)
                    elif type(value) is np.ndarray :
                        vertices = value
                    else :
                        raise ValueError('Model.Shape needs a list/np.array for a polygon')

                    # Adapt 2D/3D
                    if vertices.shape[1] == 2:
                         vertices = np.hstack((add_col(vertices.shape[0])*0, vertices))

                    P0 = tuple(vertices[reference_index])
                    input_str = f"'{shape}',{kwargs}"

        else :
            vertices = createShape(shape,W,H,A,B,C,D)
            P0 = tuple(vertices[reference_index])
            input_str = f"'{shape}',{W},{H},{A},{B},{C},{D}"
    
        # self.vertices = vertices    # working vertices
        self.P0 = P0         # reference point
        # the state of the polygon
        self.R = vertices   # initial values of vertices
        self.angles = [0.0,0.0]
        self.__input_str = input_str

        return vertices

    def __str__(self):
        return f"{len(self.vertices)} vertices :\n{self.vertices}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__input_str})"

    def __iter__(self): return iter(self.vertices)
    def __getitem__(self, key): return self.vertices[key]

    # change the object from the current position to a next one 
    # in terms of reference point,together with change in both angles
    # These changes in angle are around the global YZ
    def move(self, reference = None, to = (0,0,0), by = (0.0,0.0)):
        alpha = self.angles[0] + by[0]
        beta  = self.angles[1] + by[1]

        if not reference: P0 = self.P0
        else            : P0 = reference
        
        vertices = change(shape = self.R, reference = P0, to = to, by = (alpha, beta) )
        P0 = tuple(self.vertices[0])

        newPolygon = Shape(shape='Polygon',**{'vertices':vertices})
        newPolygon.P0 = P0
        newPolygon.angles = (alpha, beta)

        return newPolygon
 
    def get_instance(self):
        return self

    def get_argument_dict(self):
        return getArguments(self.shapeName)

#  end of class 

### test functions
def testPoints1():
    P = Point(0.5,0.5,0.5)
    ax = P.plot(style={'color':'r','marker':'o','alpha':0.5})
    P = Point(0.5,0.7,0.5)
    P.plot(ax=ax)
    P.show()

def testPoints2():
    P = Point(0.5,0.5,0.5)
    ax = P.plot(style={'color':'r','marker':'o','alpha':0.5})
    print(P.ax)
    P1 = Point(0.5,0.7,0.5)
    P.add_plot(P1)
    P.show()

def testPoints3():
    P = Point(0.5,0.5)
    P[2]=0.6
    print(P[0],P[1],P[2])

def testSegment():
    P1 = Point(0.2,0.1,0.1)
    P2 = Point(0.8,0.5,0.8)
    L  = Segment(P1,P2)
    print(L)
    L.plot()
    L.show()

def testLine2():
    P1 = Point(0.2,0.1,0.1)
    P2 = Point(0.8,0.5,0.8)
    L  = Line(P1,P2)
    L.plot(style={'color':'r'})
    L.show()

def testRay1():
    P0 = Point(0.2,0.1,0.1)
    L  = [0.8,0.5,0.8]
    ray  = Ray(P0,L)
    ax   = ray.plot()
    # print(ax)
    ray.show()

def testRay2():
    P0 = Point(0.2,0.1,0.1)
    L  = [0.8,0.5,0.8]
    ray = Ray(P0,L)
    ax = ray.plot()
    ray.show()

def testPolygon1():
    x = [0.5,0.3,0.6,0.9,0.1]
    y = [0.1,0.9,0.3,0.4,0.8]
    z = [0.7,0.3,0.1,0.9,0.6]
    points = list(zip(x,y,z))
    poly = Polygon(points)
    poly.plot()
    poly.show()

def testPolygon2():
    x = [0.5,0.3,0.6,0.9,0.1]
    y = [0.1,0.9,0.3,0.4,0.8]
    z = [0.7,0.3,0.1,0.9,0.6]
    points = list(zip(x,y,z))
    poly = Polygon(points)
    poly.plot()
    poly.show()

def testPolyLine():
    pl = Polyline((0.5,0.3,0.6),(0.1,0.9,0.3),(0.7,0.3,0.9))
    pl.broken_by((0.1,0.9,0.6))
    pl.insert_at(1,(0.3,0.6,0.9))
    pl.plot()
    pl.show()

def testPolyLine():
    pl = Polyline((0.5,0.3,0.6),(0.1,0.9,0.3),(0.7,0.3,0.9))
    pl.broken_by((0.1,0.9,0.6))
    pl.insert_at(1,(0.3,0.6,0.9))
    pl.plot(style = {'colors':['darkorange','orange','gold','wheat'],'node':'visible'})
    pl.show(azim=110, elev=19)

def testAllShapes():
    W,H,A,B,C,D = 2.0,1.5, 1.0, 0.6, 0.2, 0.3
    shape1 = Shape('rectangle',W,H,A,B,C,D)
    shape2 = Shape('triangle' ,W,H,A,B,C,D)
    shape3 = Shape('fourSided',W,H,A,B,C,D)
    shape4 = Shape('fiveSided',W,H,A,B,C,D)
    shape5 = Shape('rectangleWithHole',W,H,A,B,C,D)

    shape1.plot(hideAxes=True)

    shape2 = shape2.move(to = (1,0,0))
    shape3 = shape3.move(to = (2,0,0))
    shape4 = shape4.move(to = (3,0,0))
    shape5 = shape5.move(to = (4,0,0))
    
    line = Polyline((0,1,0.5),(5,1,0.5))

    P2 = shape2.intercept(line)
    P3 = shape3.intercept(line)
    P4 = shape4.intercept(line)
    P5 = shape5.intercept(line)

    # print(P2,P3,P4,P5)
    
    line.broken_by(P2)
    line.broken_by(P3)
    line.broken_by(P4)
    line.broken_by(P5)

    # print(line)

    shape1.add_plot(shape2)
    shape1.add_plot(shape3)
    shape1.add_plot(shape4)
    shape1.add_plot(shape5)
    shape1.add_plot(line,style={'node':'visible','color':'gradient'})
    shape1.show(azim=-88, elev=7)

def ShapeXLine():
    W,H,A,B,C,D = 2.0,1.5, 1.0, 0.9, 0.5, 0.5
    shape = Shape('fourSided',W,H,A,B,C,D)

    shape = shape.move(to = (3,0,0))
    line = Polyline((1,1,0.5),(5,1,0.5))

    P = shape.intercept(line)

    line.broken_by(P)

    # print(line)
    shape.plot(hideAxes=True)
    shape.add_plot(line,style={'node':'visible','edgecolor':'gradient'})
    shape.show(azim=144, elev=-38)
 
def draw_logo():

    W,H = 2.0,1.5
    shape = Shape('rectangle',W,H)
    shape = shape.move(to = (2,0,0), by = (45,30))
    
    line = Polyline((0,0,0),(3,1.,2))
    P = shape.intercept(line)
    line.broken_by(P)
    
    shape.plot(hideAxes=True)
    shape.add_plot(line,style={'color':'b','node':'visible','edgecolor':'gradient'})
    shape.show(azim=-20, elev=3)


def main():

    # testPoints1()
    # testPoints2()
    # testPoints3()
    # testSegment()
    # testLine2()
    # testRay1()
    # testRay2()
    # testPolygon1()
    # testPolygon2()
    # testPolyLine()
    testAllShapes()
    # ShapeXLine()
    # draw_logo()


if __name__ == '__main__':
    main()
