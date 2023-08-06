#!/usr/bin/env python
#-*- coding: latin-1 -*-

##  take_photo_of_3D_planar_shape.py

##  This script generates a photo of the virtual planar shape in the
##  YZ-plane of the world (X,Y,Z) coordinate frame.


import NonlinearLeastSquares
import ProjectiveCamera
import numpy
from PIL import Image                                                                                                               
from PIL import ImageDraw                                                                                                           
from PIL import ImageTk   
import tkinter as Tkinter                                                                                                       
from tkinter.constants import * 
import sys

cam_rotation = numpy.diag([1.0,1.0,1.0])
cam_rotation = numpy.asmatrix(cam_rotation)
cam_translation = numpy.matrix([0.0, 0.0, 0.0])
camera = ProjectiveCamera.ProjectiveCamera( 
                     camera_type = 'projective',
                     alpha_x = 1000.0,
                     alpha_y = 1000.0,
                     x0 = 300.0,
                     y0 = 250.0,
                     camera_rotation = cam_rotation,
                     camera_translation = cam_translation,
         )
camera.initialize()
camera.print_camera_matrix()

camera.print_camera_matrix()
theta_x = 20.0
theta_y = 45.0
x_motion = 3000.0
y_motion = -100.0
camera.rotate_previously_initialized_camera_around_world_X_axis( theta_x)
camera.rotate_previously_initialized_camera_around_world_Y_axis( theta_y)
camera.translate_a_previously_initialized_camera((0.0,y_motion,0.0))
camera.translate_a_previously_initialized_camera((x_motion,0.0,0.0))

## The argument is the Z-offset for the planar shape.  Z-axis is the optic axis of the camera and Z-offset is distance
## between the image plane and closest point on the planar shape in its generic pose:
#world_lines = camera.make_line_description_of_a_3D_planar_shape(500)

world_lines = camera.make_line_description_of_a_3D_planar_shape(200)

print("\n\ncuboid lines: ", world_lines)

image_lines = []
for line in world_lines:
#    print("line being projected: ", line)
    image_lines.append(camera.get_pixels_for_a_sequence_of_world_points(line))

print("\n\nimage lines for planar shape: ", image_lines)    

## for estimating the min and max bounds on the image plane pixels
all_pixels = []
for line in image_lines:
    all_pixels += line
x_min = min( [x for (x,_) in all_pixels] )
x_max = max( [x for (x,_) in all_pixels] )
y_min = min( [y for (_,y) in all_pixels] )
y_max = max( [y for (_,y) in all_pixels] )
print("\n\nx_min = %d   x_max = %d      y_min = %d   y_max = %d" % (x_min, x_max, y_min, y_max))

width,height = 256,256
margin = 25
scaled_image_lines = []
for line in image_lines:
    scaled_line = []
    for endpoint in line:
        x,y = endpoint
        scaled_x = int( ((x - x_min ) / (x_max - x_min)) * (width - 2*margin) ) + margin 
        scaled_y = int( ((y - y_min ) / (y_max - y_min)) * (height - 2*margin) )  + margin
        scaled_line.append( (scaled_x, scaled_y) )
    scaled_image_lines.append(scaled_line)

print("\n\nscaled image lines: ", scaled_image_lines)

im = Image.new( "1", (width,height), 0 )
draw = ImageDraw.Draw(im)
for line in scaled_image_lines:
    draw.line( (line[0][0], line[0][1], line[1][0], line[1][1]), fill=255)

camera.displayImage5(im, "Displaying Planar Shape")
    
