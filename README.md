# partial_deannotation_in_an_image

## Data Description
The dataset can be downloaded from [here](https://github.com/akaiketech/internship-assignment-cv/tree/main/Dataset). The file will contain 2 folder train and
test and a submission file.<br>
The train folder contains 3 images
- original_image : Original Base Image without annotation
- fully_annotated : Fully annotated Image
- partially_annotated : Partially annotated Image
The test folder will have 2 images.<br>
- original_image : Original Base Image without annotation
- fully_annotated : Fully annotated Image
Assumptions<br>
You can assume the following in the image:
- There will be only two annotations per image
- There will be one dog and a cat in the image
- The annotation of the cat should be retained in the partially annotated image


## Problem Statement

The objective of this assignment is to develop a solution using image processing techniques to partially de-annotate an image, given an original image and a fully annotated image. The solution should be able to de-annotate the image partially without re-annotating the original image. The assignment will also provide a set of sample images containing original, fully annotated, and partially annotated images for testing and evaluation purposes.The solution should be able to identify and remove specific annotations from the fully annotated image while preserving the underlying information of the original image. The partially de-annotated image should not contain any unwanted annotations or distortions that may affect its interpretation. Additionally, the solution should be able to generalize to different types of images and annotations, and should be efficient and scalable for processing large datasets.<br>

** Annotation of original images partially will not be considered as a solution.
You’re not allowed to use any Object Detection model on the images.

## Solution
The Solution is in the partial_annotated.py file as a function. If the path for original_image, fully_annotated_image and partially_annotated_image (to save the result in a location with image.jpg at the end of the location) is given, the output will be stored in a path provided in the partially_annotated_image.<br>
<br>
To see the below process in the steps given below see the [de-annotation of dog and keep cat annotation.ipynb] file. It will give the better visulation of the process and filters applied.
### Steps
- Loaded the original image and fully annotated image using opencv.
- Applied **Gray Scale** to both the images to futher process the image.
- **Resized an fully annotated image** to the size of original image.
- **Subtracted the numpy array of original image from the fully annotated 
image.**
- **Applied Gaussian Blur** to the subtracted image.
- **Applied Canny Edge Detection** to the blurred image
- From the resulting image of the canny edge detection, **used Hough lines
method to find the edges of the bounding boxes.**
- The edge lines are drawn into the new black image.
- Drawn the lines around the edges of the image containing the lines.
- Now, applied Gray scale again to the image containing line.
- **Applied Adaptive Threshold to the gray scaled to line image** to obtain 
the rectangles.
- In these rectangles one some rectangles contain dog.
- So used contour and opencv’s rectangle to draw rectangle to each of the 
contour rectangles.
- Got the axes of all the rectangle.
- Parallely the **model.pickle file in trained to identify the ‘Dog’ or ‘Cat’.**
- With axes of every rectangle, looped through every rectangle to find the 
rectangles with the ‘Dog’ in it.
- In axes which is found to be the ‘Dog’, found the rectangle with 
maximum area.
- **Finally, the axes found to be dog is cropped from the original image in 
BGR and put in the Fully Annotated Image to get the Partially 
Annotated Image.**










