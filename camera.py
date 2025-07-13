import cv2

import numpy as np

# Initialize an empty list to store results

results = [] #liste vide pour stocker les résultats

conversion_factor = 0.01009 #chaque pixel represente 0.1mm (pixel*conversion-factor)
error = 0 #0 pour suivre les erreurs

def non_max_suppression_fast(boxes, overlapThresh): #fonction pour supprimer les détections redondantes ou similaires.

    #Vérifie si la liste boxes est vide. Si elle est vide, retourne une liste vide, car il n'y a aucune détection à supprimer.
    if len(boxes) == 0: 

        return [] 
    
     #Initialise une liste vide pick pour stocker les indices des détections sélectionnées après la suppression non maximale.
    pick = []

    #Extraction des coordonnées x et y chaque boîte englobante à partir de la liste boxes
    x1 = boxes[:, 0] # Coordonnée x du coin supérieur gauche de chaque boîte

    y1 = boxes[:, 1] # Coordonnée y du coin supérieur gauche de chaque boîte

    x2 = boxes[:, 2] # Coordonnée x du coin inférieur droit de chaque boîte

    y2 = boxes[:, 3] # Coordonnée y du coin inférieur droit de chaque boîte

    area = (x2 - x1 + 1) * (y2 - y1 + 1) 

    idxs = np.argsort(y2) # Tri des indices des boîtes par leur coordonnée y2 en ordre croissant.(coin inférieur droit y) #aalech y2?

 
    # Boucle tant qu'il reste des indices de boîtes à traiter
    while len(idxs) > 0:

        last = len(idxs) - 1  # Dernier indice de la liste d'indices

        i = idxs[last] # Récupère l'indice de la dernière boîte (celle avec la plus grande coordonnée y2)

        pick.append(i) # Ajoute l'indice de la boîte à la liste de boîtes sélectionnées

        # Calcul des coordonnées des points d'intersection entre la boîte actuelle et les autres boîtes

        xx1 = np.maximum(x1[i], x1[idxs[:last]])

        yy1 = np.maximum(y1[i], y1[idxs[:last]])

        xx2 = np.minimum(x2[i], x2[idxs[:last]])

        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Calcul de la largeur et de la hauteur des boîtes d'intersection
        w = np.maximum(0, xx2 - xx1 + 1)

        h = np.maximum(0, yy2 - yy1 + 1)
        # Calcul de l'overlap (recouvrement) entre la boîte actuelle et les boîtes d'intersection
        overlap = (w * h) / area[idxs[:last]]
        # Suppression des indices des boîtes d'intersection qui ont un overlap supérieur à overlapThresh
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

 
    # Retourne les indices des boîtes sélectionnées après la suppression non maximale
    return boxes[pick].astype("int")

 

# Load the main image and the template files

image_path =r"C:\Users\iram trabelsi\Pictures\FF\screenshot_0.png"

template_path_center = r"C:\Users\iram trabelsi\Pictures\FF\center.jpeg"

template_path_button = r"C:\Users\iram trabelsi\Pictures\FF\button.png"

template_path_left = r"C:\Users\iram trabelsi\Pictures\FF\left.png"

template_path_right = r"C:\Users\iram trabelsi\Pictures\FF\right.png"

image = cv2.imread(image_path)

 

template_center = cv2.imread(template_path_center, cv2.IMREAD_COLOR)

template_button = cv2.imread(template_path_button, cv2.IMREAD_COLOR)

template_left = cv2.imread(template_path_left, cv2.IMREAD_COLOR)

template_right = cv2.imread(template_path_right, cv2.IMREAD_COLOR)

if image is None or template_center is None or template_button is None or template_left is None or template_right is None:

    print("Error: Unable to load image or template(s)")

else:

    template_center_gray = cv2.cvtColor(template_center, cv2.COLOR_BGR2GRAY)

    template_button_gray = cv2.cvtColor(template_button, cv2.COLOR_BGR2GRAY)

    template_left_gray = cv2.cvtColor(template_left, cv2.COLOR_BGR2GRAY)

    template_right_gray = cv2.cvtColor(template_right, cv2.COLOR_BGR2GRAY)

   
    #matchtemplate et cv2.TM_CCOEFF_NORMED : deux méthodes de correspondance de modèles
    result_center = cv2.matchTemplate(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), template_center_gray, cv2.TM_CCOEFF_NORMED)

    result_button = cv2.matchTemplate(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), template_button_gray, cv2.TM_CCOEFF_NORMED)

    result_left = cv2.matchTemplate(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), template_left_gray, cv2.TM_CCOEFF_NORMED)

    result_right = cv2.matchTemplate(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), template_right_gray, cv2.TM_CCOEFF_NORMED)

   

    threshold_center = 0.72

    threshold_button = 0.66

    threshold_left = 0.6

    threshold_right = 0.6

   

   
     #np.where : pour trouver les positions dans la matrice de résultats 
    loc_center = np.where(result_center >= threshold_center)

    loc_button = np.where(result_button >= threshold_button)

    loc_left = np.where(result_left >= threshold_left)

    loc_right = np.where(result_right >= threshold_right)

   
    # listes vides pour stocker les coordonnées des rectangles englobants des objets détectés pour chaque modèle
    rectangles_center = []

    rectangles_button = []

    rectangles_left = []

    rectangles_right = []

   

    # à travers les positions des correspondances de chaque modèle : boucle commence pour créer des rectangles englobants autour de chaque correspondance

    for pt in zip(*loc_center[::-1]): #prend les coordonnées x et y des correspondances (stockées dans loc_center) et les agrège en paires (x, y).

        rectangles_center.append([pt[0], pt[1], pt[0] + template_center_gray.shape[1], pt[1] + template_center_gray.shape[0]]) # pt[0] coordonnée x du coin inférieur droit du rectangle : calculé : la largeur du modèle de centre + x de la position de la correspondance. pt[1] coordonées y e ajoutat la hauteur

 

    for pt in zip(*loc_button[::-1]):

        rectangles_button.append([pt[0], pt[1], pt[0] + template_button_gray.shape[1], pt[1] + template_button_gray.shape[0]])

       

       

    for pt in zip(*loc_left[::-1]):

        rectangles_left.append([pt[0], pt[1], pt[0] + template_left_gray.shape[1], pt[1] + template_left_gray.shape[0]])

       

    for pt in zip(*loc_right[::-1]):

        rectangles_right.append([pt[0], pt[1], pt[0] + template_right_gray.shape[1], pt[1] + template_left_gray.shape[0]])

       
    #Les coordonnées des rectangles englobants sont ajoutées aux listes precedentes  
    rectangles_center = np.array(rectangles_center)

    rectangles_button = np.array(rectangles_button)

    rectangles_left = np.array(rectangles_left)

    rectangles_right= np.array(rectangles_right)

   

    # appliquer non_max_suppression_fast pour avoir les détections finales après élimination des détections redondantes ou très similaires(accepter:inf de 0.3)

    refined_rectangles_center = non_max_suppression_fast(rectangles_center, 0.3)  # Experiment with this value

    refined_rectangles_button = non_max_suppression_fast(rectangles_button, 0.3)  # Experiment with this value

    refined_rectangles_left = non_max_suppression_fast(rectangles_left, 0.3)  # Experiment with this value

    refined_rectangles_right = non_max_suppression_fast(rectangles_right, 0.3)  # Experiment with this value

   
    for idx, (x1, y1, w, h) in enumerate(refined_rectangles_button): #idx est l'indice de l'itération actuelle,(x1, y1, w, h) sont les coordonnées et dimensions du rectangle englobant actuel.

       # Draw the line and display its y1-coordinate

       line_y = y1 + 100
                              
       line_x = x1 + 650
       #ligne horizontal % au rectangle du button
       cv2.line(image, (x1, line_y+10), (x1 + 1300, line_y+10), (255, 0, 0), 2) 
       print(f"SP Y-Difference: {x1}")
       # midland button line , ligne vertical du button
       
       cv2.line(image, (x1+650, y1+100), (x1+650, y1-1020), (255, 0, 0), 2)

       #cv2.putText(image, f" {idx + 1} Line X-coordinate: {line_x}", (0, 1000 + 30 * idx), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

       #cv2.putText(image, f" {idx + 1} Line Y-coordinate: {line_y}", (0, 1100 + 30 * idx), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

       

       # Calculate and display the difference between the line y-coordinate and each point's y-coordinate

       for sp_idx, (x, y, w, h) in enumerate(refined_rectangles_center): #sp_idx : cooredonnées de spring

         center_x = x + 50 

         center_y = y + 25                                           
         spring_name = f"SP{sp_idx + 1}"  # Index starts from 1
        # Draw a rectangle on the image
         #cv2.rectangle(image, (x, y), (x+50, y+25), (255, 255, 255), 1)
         y_difference =abs( (line_y - center_y  )* conversion_factor)
         x_difference = abs((line_x - center_x  )* conversion_factor)
         
        # Check the problem in the value Y direction 
         if 0 <= y_difference <= 2:  
           if abs(y_difference-1.7)<= 0.5: 
           
             color = (0, 255, 0)  # Green color for values between 1 and 2
             cv2.putText(image, f"SP {sp_idx + 1}:  x ={y_difference}", (2800, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 0
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
           elif abs(y_difference-1.7) > 0.5 :
             color =   (0, 0, 255)
             cv2.putText(image, f"SP {sp_idx + 1}:  x ={y_difference}", (2800, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 1
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
             cv2.rectangle(image, (x, y), (x+100, y+190), (0, 0, 255), 2)
         elif 2 < y_difference <= 5:

           if abs(y_difference-4.45)<= 0.5 :
           
             color = (0, 255, 0)  # Green color for values between 1 and 2
             cv2.putText(image, f"SP {sp_idx + 1}:  x ={y_difference}", (2800, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 0
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
           elif abs(y_difference-4.45) > 0.1 :
             color =   (0, 0, 255)
             cv2.putText(image, f"SP {sp_idx + 1}:  x ={y_difference}", (2800, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA) 
             error = 1
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
             cv2.rectangle(image, (x, y), (x+100, y+190), (0, 0, 255), 2)
        
        # Check the problem in the value X direction 
         if 0 <= x_difference <= 2: #same here , aalech les valeurs hedhom?
           if abs(x_difference-1.25)<= 0.5:
           
             color = (0, 255, 0)  # Green color for values between 1 and 2
             cv2.putText(image, f"SP {sp_idx + 1}:  y ={x_difference}", (0, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 0
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
           elif abs(x_difference-1.25) > 0.1 :
             color =   (0, 0, 255)
             cv2.putText(image, f"SP {sp_idx + 1}:  y ={x_difference}", (0, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 1
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
             cv2.rectangle(image, (x, y), (x+100, y+190), (0, 0, 255), 2)
         elif 2 < x_difference <= 5:

           if abs(x_difference-3.75)<= 0.5 :
           
             color = (0, 255, 0)  # Green color for values between 1 and 2
             cv2.putText(image, f"SP {sp_idx + 1}:  y ={x_difference}", (0, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 0
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)
           elif abs(x_difference-3.75) > 0.5:
             color =   (0, 0, 255)
             cv2.putText(image, f"SP {sp_idx + 1}:  y ={x_difference}", (0, 120 * sp_idx +1000), cv2.FONT_HERSHEY_SIMPLEX, 4, color,3, cv2.LINE_AA)
             error = 1
             cv2.putText(image, spring_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2, cv2.LINE_AA)  
             cv2.rectangle(image, (x, y), (x+100, y+190), (0, 0, 255), 2)        
      
         

         print(f"SP {sp_idx + 1} to Button {idx + 1} Y-Difference: {y_difference}")
         #print(f"SP {sp_idx + 1} to Button {idx + 1} X-Difference: {x_difference}")
              # Add the name of the spring along with the index near the spring

         

         #cv2.putText(image, spring_name, (1500, 2000), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

         
         
        
       # Store information for each rectangle




 

# Display the x and y coordinates on the left side of the screen

    #ajout du circle dans le centre des rectangles 
    for idx, (x, y, w, h) in enumerate(refined_rectangles_center):

      cv2.circle(image, (x + 50, y + 25), 3, (0, 0, 255), 5)

      center_x = x + 50 // 2

      center_y = y + 25 // 2

      # Add the name of the spring along with the index near the spring

      spring_name = f"SP{idx + 1}"  # Index starts from 1 , 
      
      

      #cv2.putText(image, f"SP {idx + 1}: X={center_x}, Y={center_y}", (10, 50 * idx + 600), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the original size image with rectangles
    cv2.putText(image, 'STARZ ELECTRONICS', (170, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3, cv2.LINE_AA)
    cv2.putText(image, 'AUTOMATIC VISION SYSTEM', (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 3, cv2.LINE_AA)
    #cv2.putText(image, f'Number of centers: {len(refined_rectangles_center)}', (0, 2000), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    #cv2.putText(image, f'Number of buttons: {len(refined_rectangles_button)}', (0, 2050), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    #cv2.putText(image, f'Number of left: {len(refined_rectangles_button)}', (0, 2100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

    #cv2.putText(image, f'Number of right: {len(refined_rectangles_left)}', (0, 2150), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

   
    #cv2.circle(image, (2059, 2066), 3, (0, 0, 255), 5)
    cv2.namedWindow('Matching Result', cv2.WINDOW_NORMAL)  # Create a window that can be resized by the user

    cv2.imshow('Matching Result', image)  # Display the image in this window

    cv2.waitKey(0)

    cv2.destroyAllWindows()

