#!/usr/bin/env python
#-*- coding: latin-1 -*-

##  flyby_photos_of_3D_planar_shape.py

##  This script generates a flyby collection of images as the camera
##  "flies" over a planar shape in the YZ-plane of the world (X,Y,Z)
##  frame.  Initially, the optic axis of the camera is aligned with
##  the world-Z axis.  However, before the flyby, you can orient the
##  the camera in any direction you wish and position it where you
##  want it.  Except for the Z-coordinate of the camera position, the
##  extrinsic and the intrinsic parameters of the camera remain
##  constant during the flyby.


import NonlinearLeastSquares
import ProjectiveCamera
import numpy
from PIL import Image                                                                                                               
from PIL import ImageDraw                                                                                                           
from PIL import ImageTk   
import tkinter as Tkinter                                                                                                       
from tkinter.constants import * 
import sys, os, glob

##  This directory is for storing the flyby images:
flyby_directory = 'flyby_images'

if os.path.exists(flyby_directory):
    files = glob.glob(flyby_directory + "/*")
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
        else:
            files = glob.glob(file + "/*")
            list(map(lambda x: os.remove(x), files))
else:
    os.mkdir(flyby_directory)

##  Initialize the camera
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


## The argument is the Z-offset for the planar shape.  Z-axis is the
## optic axis of the camera and Z-offset is distance between the image
## plane and closest point on the planar shape in its generic pose:
world_lines = camera.make_line_description_of_a_3D_planar_shape(200)
print("\n\nThe lines that define the planar shape: ", world_lines)

## Define the initial pose of the camera at the start of the flyby:
theta_x = 20.0
theta_y = 45.0
x_motion = 3000.0
y_motion = -100.0

camera.rotate_previously_initialized_camera_around_world_X_axis( theta_x)
camera.rotate_previously_initialized_camera_around_world_Y_axis( theta_y)
camera.translate_a_previously_initialized_camera((0.0,y_motion,0.0))
camera.translate_a_previously_initialized_camera((x_motion,0.0,0.0))

##  The world Z is the optic axis of the camera.  The flyby consist of
##  translating the camera in a direction that is parallel to world Z-axis
##  as its pointing angle is set as shown above.  Note that the camera
##  flies at the altitude that is set by the value of 'x_motion' shown
##  above:
flyby_displacements_in_Z_direction =  [i * 2000 for i  in range(10)]

##  Use the following index to name the saved images during the flyby:
save_fig_index = 0

##  With the pointing angle of the camera set as above and also with the
##  height of the camera set as above, now move the camera along a path
##  parallel to the World-Z axis and record images:
for z_disp in flyby_displacements_in_Z_direction:

    camera.translate_a_previously_initialized_camera((0.0,0.0,z_disp))

    ##  For each of the wold lines defined by a pair of end points, find
    ##  the corresponding image line as defined by its endpoint pixels
    ##  in the image plane:
    image_lines = []
    for line in world_lines:
        image_lines.append(camera.get_pixels_for_a_sequence_of_world_points(line))
    print("\n\nimage lines for planar shape: ", image_lines)    

    ##  IMPORTANT: Since the current script does not center the camera 
    ##             pointing angle toward the plane object in the YZ-plane,
    ##             the pixels are likely to be all over the image plane 
    ##             during the flyby. At the moment, for a given position of 
    ##             the camera during the flyby, I find the min and the max
    ##             of the image line endpoint coordinates in order to scale
    ##             and translate them so that they would be visible within
    ##             the camera image occupying roughly the same portion of the
    ##             camera image plane. THIS HAS THE FOLLOWING CONSEQUENCE: As
    ##             the camera becomes more and more distant from the stationary
    ##             object in the YZ-plane, the image rendered would only have the
    ##             correct perspective effects but its size would be misleading.

    ##             In a future version of the module, I am planning to 
    ##             incorporate other strategies for image "normalization" so that
    ##             the images displayed would include both size-scaling and
    ##             perspective effects.
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
    save_fig_name = flyby_directory + "/" + str(save_fig_index) + ".jpg"
    camera.displayImage(im, save_fig_name)
    save_fig_index += 1
    
