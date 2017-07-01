'''
This is the file that defines all the objects the
students will create and call methods on.

The methods, in turn, will send BlueTooth messages
to the NXT
'''
import nxt.locator
class Robot(object):
   '''The driving part of the rover'''

   def __init__(self, brick):
      self.brick = brick

   def timeDrive(self, direction, speed, time):
      time = time * 1000; #adjust for 1/1000ths of a second
      self.brick.send_command("btimeDrive %s %i %f " % (direction, speed, time))
      # Direction: forward, backward; Speed: 0-100%; Time: seconds
      
   def rotationDrive(self, direction, speed, degrees):
      self.brick.send_command("brotationDrive %s %i %f " % (direction, speed, degrees))
      # Direction: forward, backward; Speed: 0-100%; Rotations: rotations of motor
      
   def ultrasonicDrive(self, direction, speed, distance):
      self.brick.send_command("bultrasonicDrive %s %i %f " % (direction, speed, distance))
      # Direction: forward, backward; Speed: 0-100%; (centimeters)
      print "Message sent"
      
   def timeTurn(self, direction, speed, time):
      time = time * 1000;
      self.brick.send_command("btimeTurn %s %i %f " % (direction, speed, time))
      # Direction: leftTurn, RightTurn; Speed: 0-100%; Time: seconds
      
   def gyroTurn(self, direction, speed, heading):
      self.brick.send_command("bgyroTurn %s %i %f " % (direction, speed, heading))
      # Direction: leftTurn, rightTurn; Speed: 0-100%; Gyro
      
   def cameraHeading(self, speed, degrees):
      self.brick.send_command("bcameraHeading %s %i %f " % ("right", speed, degrees))
      
   