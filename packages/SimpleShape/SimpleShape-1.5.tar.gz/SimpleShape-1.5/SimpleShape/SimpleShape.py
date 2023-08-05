"""
Main document with definitions of classes, methods, and functions
"""

# Import libraries

import json
from math import pi, sqrt, sin, cos
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse as _Ellipse
import numpy as np

# Parent Class

class Geometry:
    """Parent class for creating geometric objects"""
    
    def __init__(self, coordinates):
        """Initialization of the object. Somewhat different for
        circle and ellipse"""
        self.type = self.__class__.__name__
        self.coordinates = coordinates

        for element in self.coordinates:
            if len(element) != 2:
                raise Warning("Provide 2 coordinates for each point")
    
    def __str__(self) -> str:
        """A string representation of the object"""
        return ("The coordinates of the " + self.type
                + " are " + str(self.coordinates))

    def perimeter(self) -> float:
        """Perimeter (circumference) of the object"""
        L = 0
        for i in range(len(self.coordinates)):
            L += sqrt((self.coordinates[i][0] - self.coordinates[i-1][0])**2
                      + (self.coordinates[i][1] - self.coordinates[i-1][1])**2)
        return L
    
    def area(self) -> float:
        """Area of object using shoelace formula"""
        s = 0
        for i in range(len(self.coordinates)):             
            s += (self.coordinates[i-1][0] * self.coordinates[i][1]
                  - self.coordinates[i][0] * self.coordinates[i-1][1])
        return abs(s/2)
            
    
    def intersect(self, other) -> bool:
        """Check if there is an intersection. This includes tangency"""
        if self.type in ('Triangle', 'Rectangle', 'Polygon'):
            if other.type in ('Triangle', 'Rectangle', 'Polygon'):
                for i in range(len(self.coordinates)):
                    for j in range(len(other.coordinates)):
                        if line_intersect(self.coordinates[i-1], 
                                          self.coordinates[i],
                            other.coordinates[j-1], other.coordinates[j]):
                            return True
                return False
            elif other.type == "Circle":
                for i in range(len(self.coordinates)):
                    if line_intersect_circle(self.coordinates[i-1],
                        self.coordinates[i], other.center, other.r):
                        return True
                return False
            
            elif other.type == "Ellipse":
                return "This feature has yet to be implemented"
            else:
                raise Warning("Invalid shape type for intersection check")
            
       
        elif self.type == "Circle":
            if other.type == "Circle":
                distance = sqrt((self.center[0] - other.center[0])**2
                                + (self.center[1] - other.center[1])**2)
                if distance > abs(self.r - other.r): 
                    return distance <= (self.r + other.r)
                return False
            elif other.type in ('Triangle', 'Rectangle', 'Polygon'):
                for i in range(len(other.coordinates)):
                    if line_intersect_circle(other.coordinates[i-1],
                        other.coordinates[i], self.center, self.r):
                        return True
                return False
            elif other.type == "Ellipse":
                return "This feature has yet to be implemented"
            else:
                raise Warning("Invalid shape type for intersection check")

    
        elif self.type == 'Ellipse':
            return "This feature has yet to be implemented"
        else:
            raise Warning("Invalid shape type for intersection check")
            
    
    def visualize(self) -> None:
        """Visualize the object using Matplotlib module"""
        X = np.array(self.coordinates)
        plt.figure()
        plt.scatter(X[:, 0], X[:, 1], s = 20)
        t1 = plt.Polygon(X[:,:])
        plt.gca().add_patch(t1)
        plt.show()

# Child classes (Triangle, Rectangle, Polygon, Circle, Ellipse)

class Triangle(Geometry):
    
    def __init__(self, coordinates):
        super().__init__(coordinates)

        a = self.coordinates[0]
        b = self.coordinates[1]
        c = self.coordinates[2]

        if (len(self.coordinates) != 3):
            raise Warning("Provide a 3x2 array or tuple")
        if parallel(a,b,b,c):
            raise Warning("Not a triangle. Try again") 
        if (a in (b, c) or b == c):
            raise Warning("Not a triangle. Try again")
    
class Rectangle(Geometry):
    """Insert points in clockwise or counter-clockwise direction"""
    def __init__(self, coordinates):
        super().__init__(coordinates)
        
        a = self.coordinates[0]
        b = self.coordinates[1]
        c = self.coordinates[2]
        d = self.coordinates[3]

        ab = (a[0] - b[0], a[1] - b[1])
        bc = (b[0] - c[0], b[1] - c[1])
        cd = (c[0] - d[0], c[1] - d[1])
        da = (d[0] - a[0], d[1] - a[1])
        
        ac = sqrt((a[0] - c[0])**2 + (a[1] - c[1])**2)
        bd = sqrt((b[0] - d[0])**2 + (b[1] - d[1])**2)

        eps = 1e-10
        
        if (len(self.coordinates) != 4):
            raise Warning("Provide a 4x2 array or tuple")
        if (abs(ab[0] + cd[0]) > eps or
            abs(bc[0] + da[0]) > eps or abs(ac - bd) > eps):
            raise Warning('Not a rectangle. Try again')
        if (abs(ab[1] + cd[1]) > eps or abs(bc[1] + da[1]) > eps):
            raise Warning('Not a rectangle. Try again')
        if a in (b, c, d):
            raise Warning("Not a rectangle. Try again")
            
class Polygon(Geometry):
    """Insert points in specific order"""
    def __init__(self, coordinates):
        super().__init__(coordinates)

        if len(self.coordinates) < 3:
            raise Warning("Provide a nx2 array or tuple, where n > 2")
        
        # Check for parallelism
        for i in range(len(self.coordinates)):
            if parallel(self.coordinates[i-1], self.coordinates[i],
                         self.coordinates[i-2], self.coordinates[i-1]):
                raise Warning("One of the edges in polygon is 180°. Try again")
            
        # Check if polygon is self intersecting
        self.is_intersected = 0
        for i in range(1, len(self.coordinates)):
            if self.is_intersected == 1: break
            for j in range(i-1):  # To not consider neighbours
                if line_intersect(self.coordinates[i-1], self.coordinates[i],
                             self.coordinates[j-1], self.coordinates[j]):
                    if i - j != len(self.coordinates) - 1:  # No neighbours
                        self.is_intersected = 1
                        print("This polygon is not a simple polygon. The result of area() method will presumably be incorrect")
                        break

       
                        
class Circle(Geometry):
    
    def __init__(self, r, center = (0,0)):
        self.type = self.__class__.__name__
        self.r = r
        self.center = center
        
        if r <= 0: raise Warning("Radius is 0 or less. Use another radius")
        if len(self.center) != 2:
            raise Warning("Use a center point with two dimensions")
    
    def __str__(self):
        return ("Circle with radius " + str(self.r) + " and center in "
                + str(self.center)) 

    def area(self):
        """pi * r**2"""
        return pi * self.r**2

    def perimeter(self):
        """2 * pi * r"""
        return 2 * pi * self.r
           
           
    def visualize(self):
        circle = plt.Circle(self.center, self.r)
        fig, ax = plt.subplots()
        ax.set_xlim((self.center[0] - 1.1 * self.r,
                     self.center[0] + self.r * 1.1))
        ax.set_ylim((self.center[1] - 1.1 * self.r,
                     self.center[1] + self.r * 1.1))
        ax.add_patch(circle)
        plt.show()

    
class Ellipse(Geometry):
    def __init__(self, width, height, f = 0, center = (0,0)):
        self.type = self.__class__.__name__
        self.width = width
        self.height = height
        self.f = f
        self.center = center

        if self.width <= 0:
            raise Warning("Width is 0 or less. Use another width")
        if self.height <= 0:
            raise Warning("Height is 0 or less. Use another height")
        if len(self.center) != 2:
            raise Warning("Use a center point with two dimensions")
        
    def __str__(self):
        return ("Ellipse with width = " + str(self.width) + ", height = "
                + str(self.height) + ", rotation of " + str(self.f)
                + "° and center at " + str(self.center)) 

    def area(self):
        """pi * width * height"""
        return pi * self.width * self.height

    def perimeter(self):
        """Approximate calculation using Ramanujan formula"""
        return pi * (3 * (self.width + self.height) - 
                     sqrt((3 * self.width + self.height)
                          * (self.width + 3 * self.height)))
           
    def visualize(self):
        fig, ax = plt.subplots()

        ax.axis('equal')
        ell = _Ellipse(xy=self.center, width=self.width, height=self.height,
                       angle=self.f, lw=4)
        
        ax.add_artist(ell)
        
        temp = max(self.width, self.height)
        ax.set_xlim((self.center[0] - 1.1 * temp,
                     self.center[0] + temp * 1.1))
        ax.set_ylim((self.center[1] - 1.1 * temp,
                     self.center[1] + temp * 1.1))
        
        plt.show()


# JSON functions

def to_json(object_list):
    """Convert the list of objects to JSON string using object attributes"""
    return json.dumps([obj.__dict__ for obj in object_list])
    
def save_shapes(json_data, filename):
    """Write JSON string to a .json file"""
    with open(filename, 'w') as outfile:
        outfile.write(json_data)
        
def load_shapes(filename):
    """Create JSON string from a .json file"""
    with open(filename, 'r') as file:
        json_data = json.load(file)
    return json_data 
        

def from_json(json_data):
    """Create a list of objects from a JSON string"""
    object_list = []
    for element in json_data:
        if element['type'] == 'Triangle':
            object_list.append(Triangle(element['coordinates']))
        elif element['type'] == 'Rectangle':
            object_list.append(Rectangle(element['coordinates']))
        elif element['type'] == 'Polygon':
            object_list.append(Polygon(element['coordinates']))
        elif element['type'] == 'Circle':
            object_list.append(Circle(element['r'], element['center']))
        elif element['type'] == 'Ellipse':
            object_list.append(Ellipse(element['width'], element['height'],
                           element['f'], element['center']))
        else:
            print('Invalid JSON data. Will not be used to create an object')
    return object_list

# Other functions

def random_shape(shape = next(iter({"Rectangle", "Triangle",
                                    "Circle", "Ellipse", "Polygon"}))):
    
    if shape == "Triangle":
        return Triangle(np.random.uniform(-1000, 1000, (3,2)).tolist())
    elif shape == "Rectangle":
        [a, b] = np.random.uniform(-1000, 1000, 2)
        _min = min(a,b)
        _max = max(a,b)
        avg = (_min + _max)/2
        center = (avg, avg)
        f = 2 * pi * np.random.uniform(0,1)  # Radians
        P1, P2, P3, P4 = [_min,_min], [_max,_min], [_max,_max], [_min,_max]
        (P1, P2, P3, P4) = (rotate(P1, center, f), rotate(P2, center, f),
                            rotate(P3, center, f), rotate(P4, center, f))
        return Rectangle([P1, P2, P3, P4])
    elif shape == "Polygon":
        num = np.random.randint(3,100)	
        return Polygon(np.random.uniform(-1000, 1000, (num,2)).tolist())
    elif shape == "Circle":
        r = np.random.uniform(0.1, 1000)
        [x, y] = np.random.uniform(-1000, 1000, 2)
        return Circle(r,(x,y))
    elif shape =="Ellipse":
        [a, b] = np.random.uniform(0.1, 1000, 2)
        [x, y] = np.random.uniform(-1000, 1000, 2)
        f = 360 * np.random.uniform(0,1)
        return Ellipse(a, b, f, (x, y))
    else:
        raise ValueError("Invalid shape type for creating random shape")

# Rotate P1 around P2 for angle f in radians        

def rotate(P1, P2, f):
    
    x = cos(f) * (P1[0] - P2[0]) - sin(f) * (P1[1] - P2[1]) + P2[0]
    y = sin(f) * (P1[0] - P2[0]) + cos(f) * (P1[1] - P2[1]) + P2[1]
    return [x,y]



# From: https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

def line_intersect(A, B, C, D):
    
    def onSegment(p, q, r):
        if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
               (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False
      
    def orientation(p, q, r):

        val = ((float(q[1] - p[1]) * (r[0] - q[0]))
               - (float(q[0] - p[0]) * (r[1] - q[1])))
        if (val > 0):
            return 1
        elif (val < 0):
            return 2
        else:
            return 0
      
    
    o1 = orientation(A, B, C)
    o2 = orientation(A, B, D)
    o3 = orientation(C, D, A)
    o4 = orientation(C, D, B)

    if ((o1 != o2) and (o3 != o4)):
        return True
  
    if ((o1 == 0) and onSegment(A, C, B)):
        return True
  
    if ((o2 == 0) and onSegment(A, D, B)):
        return True
  
    if ((o3 == 0) and onSegment(C, A, D)):
        return True
  
    if ((o4 == 0) and onSegment(C, B, D)):
        return True
  
    return False


    

def parallel(A, B, C, D):
    
    if A[0] == B[0]:
        if A[1] == B[1]: return True
        else: return (True if C[0] == D[0] else False)
        
    if C[0] == D[0]: 
        if C[1] == D[1]: return True
        else: return (True if A[0] == B[0] else False)
        
    return (B[1] - A[1])/(B[0] - A[0]) == (D[1] - C[1])/(D[0] - C[0])

# From: https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
# (bobobobo answer)


def line_intersect_circle(A, B, C, r):
    d = (B[0] - A[0], B[1] - A[1])
    f = (A[0] - C[0], A[1] - C[1])

    a = d[0] * d[0] + d[1] * d[1]
    b = 2 * (f[0] * d[0] + f[1] * d[1])
    c = f[0] * f[0] + f[1] * f[1] - r * r
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return False
    else:
        discriminant = sqrt(discriminant)
        t1 = (-b - discriminant)/(2*a)
        t2 = (-b + discriminant)/(2*a)
        if t1 >= 0 and t1 <= 1:
            return True
        if t2 >= 0 and t2 <= 1:
            return True
        return False
