# Imports
import cv2
import keras
import numpy as np
import matplotlib
from matplotlib.pyplot import imshow
from matplotlib import pyplot as plt

def get_output_image(original_img_path, fully_annotated_image_path, partially_annotated_img_path):

    # Taking original image
    orig_img_c = cv2.imread(original_img_path)
    orig_img = cv2.cvtColor(orig_img_c, cv2.COLOR_BGR2GRAY)

    # Taking fully annotated image
    full_ann_img_c = cv2.imread(fully_annotated_image_path)
    full_ann_img = cv2.cvtColor(full_ann_img_c, cv2.COLOR_BGR2GRAY)

    # Getting size of original image
    size = orig_img.shape

    # Converting the size of full_ann_img_c to the size of ori_img_c (BRG Image)
    rs_full_ann_img_c = cv2.resize(full_ann_img_c, size)

    # Converting the size of full_ann_img to the size of ori_img (Gray Image)
    rs_full_ann_img = cv2.resize(full_ann_img, size)

    # Applying Gaussian Blur to the subtracted image of (fully_annotaed_image) - (original_image)
    fil_img = cv2.medianBlur(rs_full_ann_img - orig_img, 11)

    # Applying Canny Edge Detection the blurred image
    image_edges = cv2.Canny(fil_img, 100, 200)

    # Drawing the straight lines of the canny image to the seperate black image
    # Apply Hough Line Transform
    lines = cv2.HoughLines(image_edges, 1, np.pi / 180, 150)

    # Draw the lines on a blank image
    line_img = np.zeros((orig_img.shape[0], orig_img.shape[1], 3), dtype=np.uint8)
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Draw lines around the corners of the image

    ## Get the height and width of the image
    h, w = line_img.shape[:2]
    ## Define the four corners of the image
    top_left = (0, 0)
    top_right = (w - 1, 0)
    bottom_left = (0, h - 1)
    bottom_right = (w - 1, h - 1)
    ## Draw lines in the four corners
    cv2.line(line_img, top_left, bottom_left, (0, 0, 255), 2)
    cv2.line(line_img, top_left, top_right, (0, 0, 255), 2)
    cv2.line(line_img, top_right, bottom_right, (0, 0, 255), 2)
    cv2.line(line_img, bottom_left, bottom_right, (0, 0, 255), 2)

    # Applying Gray Scale to the line image
    line_img_g = cv2.cvtColor(line_img, cv2.COLOR_BGR2GRAY)

    # Applying threshold to the line image
    thresh = cv2.adaptiveThreshold(line_img_g, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find all the combination of rectangle's axes
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    axes = []
    for contour in contours:
        # Get the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Append the axes of the rectangle to the list
        axes.append((x, y, x + w, y + h))

        # Draw a rectangle around the contour
        cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # For every axes identifying whether it is a dog or not

    ## Importing pickle model to identify cat or dog
    CATEGORIES = ['Cat', 'Dog']
    def image(path):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        new_arr = cv2.resize(img, (60, 60))
        new_arr = np.array(new_arr)
        new_arr = new_arr.reshape(-1, 60, 60, 1)
        return new_arr
    model = keras.models.load_model("3x3x64-catvsdog.model")
    prediction = model.predict([image('axes.jpg')])
    ## Looping through all the rectangles to find the rectangles with dog
    dog_ax = []
    cat_ax = []
    op_img = rs_full_ann_img_c
    for ax in axes:
        x1, y1, x2, y2 = ax
        cv2.imwrite('aximg.jpg', orig_img_c[y1:y2, x1:x2])
        if CATEGORIES[prediction.argmax()] == 'Dog':
            dog_ax.append(ax)
        else:
            cat_ax.append(ax)

    if len(dog_ax) > 0:
        l = dog_ax
    else:
        l = cat_ax
    m_area = 0
    m_ar_dg_ax = l[0]
    for i in l:
        area = abs(i[2] - i[0]) * abs(i[3] - i[1])
        if area > m_area:
            m_area = area
            m_ar_dg_ax = i

    # Getting Partially annotated image from the fully annotated and reference image
    ## Dogs Annotation boundary axes
    x1, y1, x2, y2 = m_ar_dg_ax
    op_img = rs_full_ann_img_c
    op_img[y1:y2, x1:x2] = orig_img_c[y1:y2, x1:x2]

    # Saving the partially annotated image
    cv2.imwrite(partially_annotated_img_path, ot_img)


if __name__ == "__main__":
    original_image_path = input('Paste original image path: ')
    fully_annotated_image_path = input('Paste fully annotated image path: ')
    partially_annotated_img_path = input('Paste the partially annotated image path: ')
    get_output_image(original_image_path, fully_annotated_image_path, partially_annotated_img_path)











