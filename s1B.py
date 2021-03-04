#TODO: Ask for input of angle from user input
#TODO: Rotate object correctly, without cropping the image or changing dimensions
#TODO: Save files in respective folders in both .nrrd and .tif format in correct name and location


import os
import time
import tifffile as tiff
import numpy as np
import imutils
import cv2
import math
from skimage.transform import rotate
from skimage import io
from scipy import ndimage
import SimpleITK as sitk
start = time.time()
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/test/'


# angle in degrees
def rotate_image(mat, angle):
    #height, width = mat.shape[1], mat.shape[2]
    height, width  = mat.shape
    print(height, width)
    image_center = (width / 2, height / 2)
    print(image_center)
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1)
    print(rotation_mat)
    radians = math.radians(angle)
    sin = math.sin(radians)
    cos = math.cos(radians)
    bound_w = int((height * abs(sin)) + (width * abs(cos)))
    bound_h = int((height * abs(cos)) + (width * abs(sin)))
    print(bound_h, bound_w)

    rotation_mat[0, 2] += ((bound_w / 2) - image_center[0])
    rotation_mat[1, 2] += ((bound_h / 2) - image_center[1])

    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h), flags=cv2.INTER_LANCZOS4)
    return rotated_mat


def rotateAndScale(img, angle):
    scaleFactor = 0.5
    (oldY, oldX, ) = img.shape
    #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
    M = cv2.getRotationMatrix2D(center=(oldX/2,oldY/2), angle=angle, scale=scaleFactor) #rotate about center of image.

    #choose a new image size.
    newX,newY = oldX*scaleFactor,oldY*scaleFactor
    #include this if you want to prevent corners being cut off
    r = np.deg2rad(angle)
    newX,newY = (abs(np.sin(r)*newY) + abs(np.cos(r)*newX),abs(np.sin(r)*newX) + abs(np.cos(r)*newY))

    #the warpAffine function call, below, basically works like this:
    # 1. apply the M transformation on each pixel of the original image
    # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

    #So I will find the translation that moves the result to the center of that region.
    (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
    M[0,2] += tx #third column of matrix holds translation, which takes effect after rotation.
    M[1,2] += ty

    rotatedImg = cv2.warpAffine(img, M, dsize=(int(newX),int(newY)))
    return rotatedImg


theta = float(input('Enter the angle by which image to be rotated:'))


def _rotate(i, angle):
    return rotate(i, -angle, preserve_range=True)


def _r(src, angle, scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    rangle = np.deg2rad(angle)  # angle in radians
    # now calculate new image width and height
    nw = (abs(np.sin(rangle)*h) + abs(np.cos(rangle)*w))*scale
    nh = (abs(np.cos(rangle)*h) + abs(np.sin(rangle)*w))*scale
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    rotated_mat = cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)
    return rotated_mat

for item in os.listdir(data_path):
    if item.endswith(".tif"):
        print(item)
        #image = tiff.imread(os.path.join(data_path, file)).astype('uint8')
        #image = tiff.imread(os.path.join(data_path, item))
        image = cv2.imread(os.path.join(data_path, item))
        #rotated_image = rotate_image(image, theta)
        #rotated_image = rotateAndScale(image, theta)
        rotated_image = _r(image, theta)
        #print(type(rotated_image))
        #rotated_image = _rotate(image, theta)
        #rotated_image = imutils.rotate_bound(image, theta)
        tiff.imwrite(os.path.join(data_path, f"rotated_{item}"), rotated_image)

        #image = io.imread(os.path.join(data_path, item))
        #rotated = ndimage.rotate(image, angle=theta, mode='nearest')

        #i = sitk.ReadImage(os.path.join(data_path, item))
        #print(i)
        #print(i.GetDirection())
        #tiff.imwrite(os.path.join(data_path, f"rotated_{item}"), rotated)


end = time.time()

print(end - start , 'secs')