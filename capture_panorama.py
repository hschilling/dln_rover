'''Capture images for panorama'''

#!/usr/bin/env python

import nxt_interface
import camera_interface
import time

def main():

        #base_url = "http://web.grc.nasa.gov/explorers-robot/"
        base_url = "http://dlnrover.grc.nasa.gov/"

        # Camera
        camera = camera_interface.CameraInterface(base_url,"","")

        # Brick
	nxt_name = raw_input("Enter name of NXT brick[NXT]: ")
	if nxt_name == "":
		nxt_name = "NXT"

        nxt = nxt_interface.NxtInterface(nxt_name)

        # Capture images while panning the camera in 
        # equal increments
        image_filename_format = "pancam%03d.jpg"
        num_images = 16
        angle_increment = 360.0/num_images
	angle = 0
        for i in range( num_images ):
                filename = image_filename_format % i
                nxt.send_command( "bcameraHeading right 10 %f" % angle)
		time.sleep(3)
		camera.capture_image(image_filename = filename )
		angle+=angle_increment
		#time.sleep(1)
        nxt.teardown_brick_connection( )
	


if __name__ == "__main__":
        main()


