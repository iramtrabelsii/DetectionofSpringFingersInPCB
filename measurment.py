import cv2
import numpy as np
from math import hypot #bibliothèque mathématique pour calculer l'hypoténuse
from pypylon import pylon #bib pour  la gestion de la caméra

points = []
distances = []
start_point = None
enable_measurement = True  # Flag to enable/disable measurements
selected_axis = None  # Variable to store the selected axis ('x' or 'y')

def calculate_distance(point1, point2, conversion_factor):
    distance_pixels = np.linalg.norm(np.array(point2) - np.array(point1)) #calculer l'hypoténuse (racine de x au carre + y au carre)
    distance_mm = distance_pixels * conversion_factor
    return distance_mm

def draw_distances(image, distances, selected_axis):
    # Display whether 'x' or 'y' was selected at the top
    axis_text = f"Selected Axis: {selected_axis}"
    cv2.putText(image, axis_text, (50, 900), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2, cv2.LINE_AA)

    for i in range(len(distances)):
        dist_text = f"{distances[i]:.2f} mm"
        
        cv2.putText(image, 'Distance', (650, 1300), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, dist_text, (600, 1500 + i * 150), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 2,
                    cv2.LINE_AA)


def delete_last_distance():
    global distances, img
    if distances:
        distances.pop() # utilisée pour supprimer le dernier élément de la liste distance 
        img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)  # Reset the image, nettoyer l'image précédente des lignes de mesure.
        draw_distances(img, distances, selected_axis)  # Redraw distances on the updated image
        cv2.imshow('title', img)

def click_event(event, x, y, flags, param):
    global points, distances, img, start_point, enable_measurement, selected_axis # La fonction utilise les variables globales Cela signifie qu'elle peut accéder et modifier ces variables définies en dehors de la fonction
    if enable_measurement:
        if event == cv2.EVENT_LBUTTONDOWN: #vérifie si l'événement est un clic gauche de la souris.
            if start_point is None: #cela signifie qu'aucun point de départ n'a encore été défini
                start_point = (x, y) #? mafhmthch yaani ken maatinch lpoint thenya yaaml cercle sghyra felpoint linzelna aaliha?
                cv2.circle(img, start_point, 5, (0, 0, 255), -1)
            else:
                end_point = (x, y)
                if selected_axis == 'x':
                    end_point = (x, start_point[1])  # Keep the y-coordinate constant for 'x' axis #mouvement sur x
                elif selected_axis == 'y':
                    end_point = (start_point[0], y)  # Keep the x-coordinate constant for 'y' axis #mouvement sur y

                points.extend([start_point, end_point])

                # Assuming a conversion factor of 1 pixel = 0.1 millimeters
                conversion_factor = 0.010079025  # Change this based on your image's scale

                # Calculate and add distance to the list
                distance = calculate_distance(start_point, end_point, conversion_factor)
                distances.append(distance)

                # Draw distances directly on the image with larger font
                draw_distances(img, distances, selected_axis)

                # Draw a line between the points
                cv2.line(img, start_point, end_point, (255, 0, 0), 2)

                # Draw both start and end points with different markers
                cv2.circle(img, start_point, 5, (0, 0, 255), -1)
                cv2.circle(img, end_point, 5, (0, 255, 0), -1)

                # Clear start_point for the next measurement
                start_point = None

                # Display the updated image
                cv2.imshow('title', img)

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
        flipped_img = cv2.flip(img, 90) # pour effectuer une opération de retournement (ou miroir) de l'image 
        #TITLE TEXT
        cv2.putText(img,'STARZ ELECTRONICS',(50,100),cv2.FONT_HERSHEY_SIMPLEX, 4,(255,255,255),2,cv2.LINE_AA)
         
        cv2.putText(img, 'Press "d" key to delete last mesurement ', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, 'Press "m" key to disable or enable manual mode ', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, 'Press "e" or "Exit" to close window  ', (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img, 'Press "x" to select X axis  ', (100, 500), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA) 
        cv2.putText(img, 'Press "y" to select Y axis  ', (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
        if enable_measurement:
         #PCB RECTANGLE
         cv2.rectangle(img, (1398, 930), (2698, 2070), (255,0,0), 2)
        
         #PCB AXIS RECTANGLE
         cv2.rectangle(img, (2048  , 1500), (2698, 2070), (255,0,0), 2)
         cv2.rectangle(img, (1398, 930), (2048, 1500), (255,0,0), 2)
        
         #SPRING 6 RECTANGLE
         cv2.rectangle(img, (1623, 1790), (1723, 1550), (255,0,0), 2)
         cv2.circle(img, (1673,1630), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF6',(1473,1630),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
         #SPRING 5 RECTANGLE
         cv2.rectangle(img, (1623, 2070), (1723, 1830), (255,0,0), 2)
         cv2.circle(img, (1673,1910), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF5',(1623,2148),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
         #SPRING 4 RECTANGLE
         cv2.rectangle(img, (1873, 2070), (1973, 1830), (255,0,0), 2)
         cv2.circle(img, (1923,1910), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF4',(1900,2148),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
         #SPRING 3 RECTANGLE
         cv2.rectangle(img, (2123,2070), (2223, 1830), (255,0,0), 2)
         cv2.circle(img, (2173,1910), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF3',(2153,2148),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
         #SPRING 2 RECTANGLE
         cv2.rectangle(img, (2373, 2070), (2473, 1830), (255,0,0), 2)
         cv2.circle(img, (2423,1910), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF2',(2400,2148),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
        
         #SPRING 1 RECTANGLE
         cv2.rectangle(img, (2373, 1790), (2473, 1550), (255,0,0), 2)
         cv2.circle(img, (2423,1630), 5, (0, 0, 255), 2)
         cv2.putText(img,'SPF1',(2523,1630),cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

        # Display the distances on the image
        draw_distances(img, distances, selected_axis)

        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        
        # Set the callback function for mouse events
        cv2.setMouseCallback('title', click_event)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # press 'ESC' to exit
            break
        elif k == ord('d'):  # press 'd' to delete the last measured distance
            delete_last_distance()
        elif k == ord('m'):  # press 'm' to toggle measurement on/off
            enable_measurement = not enable_measurement
        elif k == ord('e'):  # press 'e' to exit and close the window
            break  # Break out of the loop to exit the application
        elif k == ord('x'):  # press 'x' to select x-axis
            selected_axis = 'x'
        elif k == ord('y'):  # press 'y' to select y-axis
            selected_axis = 'y'

# Releasing the resource    
camera.StopGrabbing()
cv2.destroyAllWindows()


