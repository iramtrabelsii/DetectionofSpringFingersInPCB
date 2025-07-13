import cv2
import os
import numpy as np
from math import hypot
from pypylon import pylon



# Specify the directory to save screenshots
save_directory = r"C:\Users\iram trabelsi\Pictures\FF"

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    
    if grabResult.GrabSucceeded():
        # Access the image data
        image = converter.Convert(grabResult)
        img = image.GetArray()
        flipped_img = cv2.flip(img, 90)
        #TITLE TEXT

   
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # press 'ESC' to exit
         break
        elif k == ord('s'):  # Press 's' to save screenshot
            
            screenshot_filename = os.path.join(save_directory, f"screenshot_{0}.png")
            cv2.imwrite(screenshot_filename, img)
            print(f"Screenshot saved as {screenshot_filename}")

# Releasing the resource    
camera.StopGrabbing()
cv2.destroyAllWindows()


