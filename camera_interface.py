'''Interface to capture images with the camera and 
	upload them to the server
	'''

import urllib2
from poster.encode import multipart_encode

import Image
import ImageFont
import ImageDraw

from VideoCapture import Device

import numpy
import numpy.oldnumeric


def caption_image( cam_img, school_name, brkname ):
    # Initialize a blank image
    # Define wid,ht of image
    imgwid, imght = (640,560)
    img = Image.new("RGB",(imgwid,imght))
    # paste camera image into img
    img.paste(cam_img,(0,0))

    # add text
    drw = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("C:\WINDOWS\Fonts\ARIAL.TTF",20)

    # Use form below when we fix the font problem
    # drw.text ((10,imght-50),"Yo World",font=fnt)
    Text0 = "Robot: "+brkname+"         School: "+school_name
    drw.text((10,imght-70),Text0,font=fnt)
    Text1 = "Date: "+time.strftime("%a %m/%d/%y",time.localtime())+"      Time:"+time.strftime("%H:%M:%S",time.localtime())
    drw.text ((10,imght-50),Text1,font=fnt)

    return img

class CameraInterface(object):
    def __init__(self, base_url, school_name, nxt_name, device_number=0,image_filename="rovershot.jpg"):
        self.base_url = base_url
        self.school_name = school_name
        self.nxt_name = nxt_name
        self.device_number = device_number
        self.image_filename = image_filename
        self.camera = Device(devnum=device_number)

    def capture_image( self, image_filename = None, captioned = False ):
        if not image_filename:
            image_filename = self.image_filename
        cam_img = self.camera.getImage()
        if captioned:
            cam_img = caption_image( cam_img, self.school_name, self.nxt_name )
        cam_img.save( image_filename )

    #def capture_image( self, image_filename = None ):
        #if not image_filename:
            #image_filename = self.image_filename
        #cam_img = self.camera.getImage()
        #cam_img_captioned = caption_image( cam_img, self.school_name, self.nxt_name )
        #cam_img_captioned.save( image_filename )

    def upload_image( self ):
        # Upload 
        datagen, headers = multipart_encode({"uploadedfile": open(self.image_filename, "rb")})

        # Create the Request object
        request = urllib2.Request(self.base_url + "scripts/uploader.php", datagen, headers)
        # Actually do the request
        urllib2.urlopen(request).read()

    def capture_and_upload_image( self,captioned= False ):
        self.capture_image(captioned=captioned)
        self.upload_image()
        
        


_magic = [0.299, 0.587, 0.114]
_zero = [0, 0, 0]
_ident = [[1, 0, 0],
[0, 1, 0],
[0, 0, 1]]

# anaglyph methods from here:
# 

true_anaglyph = ([_magic, _zero, _zero], [_zero, _zero, _magic])
gray_anaglyph = ([_magic, _zero, _zero], [_zero, _magic, _magic])
color_anaglyph = ([_ident[0], _zero, _zero], [_zero, _ident[1], _ident[2]])
half_color_anaglyph = ([_magic, _zero, _zero], [_zero, _ident[1], _ident[2]])
optimized_anaglyph = ([[0, 0.7, 0.3], _zero, _zero], [_zero, _ident[1], _ident[2]])
methods = [true_anaglyph, gray_anaglyph, color_anaglyph, half_color_anaglyph, optimized_anaglyph]


def anaglyph_f(image1, image2, method=true_anaglyph):
    m1, m2 = [numpy.array(m).transpose() for m in method]
    im1, im2 = image_to_array(image1), image_to_array(image2)
    composite = numpy.oldnumeric.matrixmultiply(im1, m1) + numpy.oldnumeric.matrixmultiply(im2, m2)
    result = array_to_image(image1.mode, image1.size, composite)
    return result

def image_to_array(im):
    s = im.tostring()
    dim = len(im.getbands())
    return numpy.fromstring(s, dtype=numpy.uint8).reshape(len(s)/dim, dim)

def array_to_image(mode, size, a):
    return Image.fromstring(mode, size, a.reshape(len(a)*len(mode), 1).astype(numpy.oldnumeric.UnsignedInt8).tostring())



class Anaglyph(object):
    
    def __init__(self, image_left, image_right, output, base_url ):
        self.image_left = image_left
        self.image_right = image_right
        self.output = output
        self.base_url = base_url
        
    def create( self ):
        im1, im2 = Image.open(self.image_left), Image.open(self.image_right)
        anaglyph_f(im1, im2, half_color_anaglyph).save(self.output, quality=98)
       
    def upload( self ):
        datagen, headers = multipart_encode({"uploadedfile": open(self.output, "rb")})

        # Create the Request object
        request = urllib2.Request(self.base_url + "scripts/uploader.php", datagen, headers)
        # Actually do the request
        urllib2.urlopen(request).read()



