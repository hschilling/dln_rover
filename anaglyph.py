'''anaglyph.py '''

# uses PIL from http://www.pythonware.com/
# and numpy from http://www.scipy.org/

from PIL import Image
import numpy
import numpy.oldnumeric

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

def anaglyph(image1, image2, method=true_anaglyph):
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

if __name__=='__main__':
    im1, im2 = Image.open("rovershot_L.jpg"), Image.open("rovershot_R.jpg")
    anaglyph(im1, im2, half_color_anaglyph).save('output.jpg', quality=98)

