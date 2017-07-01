#!/usr/bin/env python

import web_interface
import nxt_interface
import camera_interface
import dln_rover
   
def main():
	global robot
	
	#base_url = "http://web.grc.nasa.gov/explorers-robot/"
	base_url = "http://dlnrover.grc.nasa.gov/"
	print("Welcome to the NXT command interface.")
	school_name = raw_input("Enter name of School: ")
	if school_name == "":
		school_name = "NASA"
	
	nxt_name = raw_input("Enter name of NXT brick[NXT]: ")
	if nxt_name == "":
		nxt_name = "NXT"

	# Camera
	camera_right = camera_interface.CameraInterface(base_url,school_name,nxt_name,device_number=0,image_filename="rovershot_R.jpg")
	camera_left = camera_interface.CameraInterface(base_url,school_name,nxt_name,device_number=1,image_filename="rovershot_L.jpg")
	anaglyph = camera_interface.Anaglyph("rovershot_L.jpg","rovershot_R.jpg","rovershot.jpg",base_url)
	#camera_left = None
	#camera_right = None
	#anaglyph = None
	
	# Brick
	nxt = nxt_interface.NxtInterface(nxt_name)

	# Web
	web = web_interface.WebInterface(base_url)
	web.run(nxt,camera_left,camera_right,anaglyph,refresh_interval=1)
        
	nxt.teardown_brick_connection( )



if __name__ == "__main__":
	main()


