import cv2
import os
import sys 

orig_img=cv2.imread(sys.argv[1])
gt_img=cv2.imread(sys.argv[2],0)
print(orig_img.shape)
print(gt_img.shape)

img_out=cv2.bitwise_and(orig_img,orig_img,mask=gt_img)

cv2.imshow('img',img_out)
cv2.waitKey(0)
cv2.destroyAllWindows()