# PhotoEditor
Python image processing tool

# Demo
![photoeditor](https://user-images.githubusercontent.com/48859041/119507518-dc6a2a80-bda9-11eb-82e8-544b56949295.gif)

# Requirements
* Python 3.8
* numpy
* opencv-python
* opencv-contrib-python
* pillow
* scipy.interpolate
* TkinterDnD2
* tkdnd2.8

# Environment
* Windows10

# Usage
How to use the processing tool

## Convert

Drag a source image into the left canvas from outside, then drag the source image into the right canvas.

#### *Save* 
 
 * Input width and height.
 * Click [Save] button to save the image on the right canvas, then a file dialog box will appear.

#### *Sepia*
 
 * Check [Light], [Contrast] and [Noise] boxes if needed.
 * Click [Sepia] button to make the image on the right canvas sepia. 

#### *Gray*

 * Click [gray] button to make the image on the right canvas gray.

#### *Anime*

 * Click [Anime] button to make the image on the right canvas like animation.

#### *Pixel*

 * Click [Pixel] button to make the image on the right canvas like pixel art.

#### *Change mode*

 * Change scale and angle if needed.
 * Every time [Change mode] button is clicked, the image on the right canvas will be converted.

#### *Skew*

 * Check [X] or [Y].
 * Click [Skew] button to make the image on the right canvas skewed.


## Composite

Select or make a mask image on the left canvas. Drag two source images from outsite the canvas and the mask image from the left canvas into the right canvas, then a composite image will be displayed on the right canvas.

#### *Save* 

 * Input width and height.
 * Click [Save] button to save the image on the right canvas, then a file dialog box will appear.

#### *Clear*

 * Click [Clear] button to delete the image on the right canvas.

#### *Change mask images*

 * Click [Change] button to select a mask image.

#### *Create mask images*

 * Check [Oval] or [Rectangle].
 * Right click and drag to draw a oval or rectangle on the image on the left canvas.
 * If [Corners] is checked, right click at the points where you like on the image on the left canvas.
 * Click [Reset] button to delete the shape drawn on the image.
 * Click [Create] button to create and display a mask image on the left canvas.

#### *Crop*

 * Check [Oval] or [Rectangle].
 * Right click and drag to draw a oval or rectangle on the image on the left canvas.
 * If [Corners] is checked, right click at the points where you like on the image in the left canvas.
 * Click [Reset] button to delete the shape drawn on the image.
 * Click [Crop] button to create and display a cropped image on the left canvas.
 * Drag the cropped image into the right canvas to save.


## Connect

Drag source images into the left canvas from outside, then drag them into the right canvas to connect. The connected images can be dragged into the left canvas to use as a souce image.

#### *Save* 

 * Input width and height.
 * Click [Save] button to save the image on the right canvas, then a file dialog box will appear.

#### *Repeat*

 * Input the number of rows and columns.
 * Click [Repeat] button to make the image on the right canvas repeated.

#### *Connect*

 * Drag source images from the left canvas to the right canvas.
 * Select [Vertical] or [Horizontal].
 * Click [Connect] button to make the images dragged into the right canvas connected.
 * Click [Reset] button to delete the image on the right canvas.

#### *Change*

 * Click [Change] button to select a source image from the images dragged into the left canvas.

#### *Clear*

 * Click [Clear] button to delete all of the imaged dragged into the left canvas.


## Pixelate

Drag a source image into the left canvas from outside, then drag the source image into the right canvas.

#### *Save* 

 * Input width and height.
 * Click [Save] button to save the image on the right canvas, then a file dialog box will appear.

#### *Entire*

 * Check 0.1, 0.05 or 0.025.
 * Click [Entire] button to make the image on the right canvas entirely pixelated.

#### *Area*

 * Check 0.1, 0.05 or 0.025.
 * Right click and drag to draw a rectangle on the image on the right canvas.
 * Click [Area] button to pixelate the area in the drawn rectangle.

#### *Detect*

 * Click [Face Detect] button to pixelate faces in the image on the right canvas.
 * Click [Eye Detect] button to pixelate eyes in the image on the right canvas. 
 * If faild to detect, adjust scaleFactor and minNeighbors.

#### *Make animated GIF*

 * Click [Run GIF] button to make an animated GIF and run it one time on the right canvas.
 * Click [Save GIF] button to make and save an animated GIF. Open the saved file to run the animation Infinitely.

#### *Compare*

 * Click [Compare] button to compare the images on the left and right canvases. Rectangles will be drawn at where difference is detected in the image on the righ canvas. 









  
