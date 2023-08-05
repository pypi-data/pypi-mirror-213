"""
Example document to provide a quick overwiev on how to use this package
"""

# Import the module

from SimpleShape import SimpleShape as sh # If installed with pip
# import SimpleShape as sh # If directly using SimpleShape.py document

# a) Create a Triangle and perform simple operations

My_triangle = sh.Triangle([[1,1],[3,1],[4,3]])
print(My_triangle)
print("Perimeter of this triangle is " + str(My_triangle.perimeter()))
print("Area of this triangle is " + str(My_triangle.area()))

# b) Check if two circles intersect

Circle_1 = sh.Circle(2) # Circle with r = 2 and center at (0,0)
Circle_2 = sh.Circle(3,(3,0.2)) # Circle with r = 3 and center at (3,0.2)

print("Do circles intersect: " + str((Circle_1.intersect(Circle_2))))


# c) Create a random ellipse and visualize it

My_Ellipse = sh.random_shape("Ellipse")
My_Ellipse.visualize()
