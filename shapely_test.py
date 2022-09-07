from shapely.geometry import Point,Polygon
from shapely._geometry import *
import numpy as np
from PIL import Image
import largestinteriorrectangle as lir

path='deb\\'

def to_poly(frame):
    a=4
    return Polygon([(frame[0]/a,frame[1]/a),(frame[0]/a,frame[3]/a),(frame[2]/a,frame[3]/a),(frame[2]/a,frame[1]/a)])

frame1=to_poly([200-20,10,200-150,110])
frame2=to_poly([10,10,70,60])
frame3=to_poly([10,80,70,150])
frame5=to_poly([80,70,120,90])
frame4=to_poly([20,20,81,81])
zoom=4
height=int(600/zoom)
width=int(700/zoom)

binarygrid=np.zeros((width,height),'bool')
di_frame=frame1
di_frame=frame1.difference(frame2)
di_frame=di_frame.difference(frame3)
di_frame=di_frame.difference(frame5)

'''
contourarray=[]
contours=get_rings(di_frame).tolist()
for i in range(len(contours[0].xy[0])):
    contourarray.append(get_point(contours,[i])[0].bounds[1:3])

contour=np.array(contourarray)
'''

for x in range(width):
    for y in range(height):
        if di_frame.intersects(Point(x,y)):
            binarygrid[x][y]=True

'''
lir提供的利用opencv查找多边形的功能，shapely-2.0a1支持用get_rings来获取多边形路径就用那个替代了
cv_grid=binarygrid.astype('uint8')*255
contours, _ =\
    cv.findContours(cv_grid,cv.RETR_TREE,cv.CHAIN_APPROX_NONE)
contour=contours[0][:,0,:]
'''
im1=Image.fromarray(binarygrid)
im1.save('frame.jpeg')

a=(lir.lir(binarygrid)).tolist()
a=[a[1],a[0],a[3]+a[1]-1,a[2]+a[0]-1]
a=list(map(lambda x:x*zoom,a))
print(a)

max_frame=to_poly(a)

binarygrid=np.zeros((width,height),'bool')
for x in range(width):
    for y in range(height):
        if max_frame.intersects(Point(x,y)):
            binarygrid[x][y]=True

im2=Image.fromarray(binarygrid)
im2.save('max.jpeg')

img=Image.blend(im1.convert('RGB'),im2.convert('RGB'),0.3)
img.save('blend.jpeg')

binarygrid=np.zeros((width,height),'bool')
for x in range(width):
    for y in range(height):
        if frame4.intersects(Point(x,y)):
            binarygrid[x][y]=True

im=Image.fromarray(binarygrid)
im.save('max_copy.jpeg')