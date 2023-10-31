import sys, os
import cv2
def main():
    paths = ["images/left.jpeg", "images/center.jpeg", "images/right.jpeg"]
    imgs = []
    for p in paths:
        imgs.append(cv2.imread(p))
    success, output = cv2.Sticher_create().stitch(imgs)
    if not success:
        print("Not successful stitch")
        return
    cv2.imshow("final", output)
    cv2.waitKey(0)

    










if __name__ == '__main__':    
    main()
