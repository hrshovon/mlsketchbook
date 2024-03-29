import cv2
import os
import sys 

def doseg(orig_path,gt_path):
    orig_img=cv2.imread(orig_path,cv2.IMREAD_UNCHANGED)
    gt_img=cv2.imread(gt_path,0)
    print(orig_img.shape)
    print(gt_img.shape)
    cv2.namedWindow("win",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("win",800,600)
    img_out=cv2.bitwise_and(orig_img,orig_img,mask=gt_img)

    cv2.imshow('win',img_out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

for item in os.listdir("images/op"):
    org_img=os.path.join('images','6',item)
    gt_img=os.path.join("images","op",item)
    doseg(org_img,gt_img)