# PhotoEditor
Python image processing tool

# Demo
![photoeditor](https://user-images.githubusercontent.com/48859041/119247159-4f18b180-bbc2-11eb-8133-98586aef2c57.gif)

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

### Convert

Drag a source image into the left canvas, then drag the image into the right canvas.

* Save 
  * Input width and height.
  * Click [Save] button, then a file dialog box will appear to save the image on the right canvas.

* Sepia
  * Check [Light], [Contrast] and [Noise] boxes if you like.
  * Click [Sepia] button to make the image on the right canvas sepia. 

* Gray
  * Click [gray] button to make the image on the right canvas gray.

* Anime
  * Click [Anime] button to make the image on the right canvas like animation.

* Pixel
  * Click [Pixel] button to make the image on the right canvas like pixel art.

* Change mode
  * Change scale and angle if you like.
  * Every time [Change mode] button is clicked, the image on the right canvas will be converted.

* Skew
  * Check [X] or [Y].
  * Click [Skew] button to make the image on the right canvas skewed.


### Composite

Select or make a mask image on the left canvas. Drag two source images from outsite the canvas and the mask image from the left canvas into the right canvas to display a composite image.

* Save 
  * Input width and height.
  * Click [Save] button, then a file dialog box will appear to save the image on the right canvas.

* Clear
  * Click [Clear] button to delete the image on the right canvas.

* Change mask images
  * Click [Change] button to select mask images.

* Create mask images
  * Check [Oval] or [Rectangle].
  * Right click and drag to draw a oval or rectangle on the image on the left canvas.
  * If [Corners] is checked, right click at the points where you like on the image on the left canvas.
  * Click [Reset] button to delete the shape drawn on the image.
  * Click [Create] button to display a mask image on the left canvas.

* Crop
  * Check [Oval] or [Rectangle].
  * Right click and drag to draw a oval or rectangle on the image on the left canvas.
  * If [Corners] is checked, right click at the points where you like on the image in the left canvas.
  * Click [Reset] button to delete the shape drawn on the image.
  * Click [Crop] button to display a cropped image in the left canvas.
  * Drag the cropped image into the right canvas to save.


### Connect

Drag source images into the left canvas from the outside, then drag them into the right canvas to connect. The connected images can be dragged into the left canvas to use as a souce image.

* Save 
  * Input width and height.
  * Click [Save] button, then a file dialog box will appear to save the image on the right canvas.

* Repeat
  * Input the number of rows and columns.
  * Click [Repeat] button to make the image on the right canvas repeated.

* Connect
  * Drag source images from the left canvas to the right canvas.
  * Select [Vertical] or [Horizontal].
  * Click [Connect] button to make the images dragged into the right canvas connected.
  * Click [Reset] button to delete the image on the right canvas.

* Change
  * Click [Change] button to select a source image from the images dragged into the left canvas.

* Clear
  * Click [Clear] button to delete all of the imaged dragged into the left canvas.


### Pixelate

Drag a source image into the left canvas, then drag the image into the right canvas.

* Save 
  * Input width and height.
  * Click [Save] button, then a file dialog box will appear to save the image on the right canvas.

* Entire
  * Check 0.1, 0.05 or 0.025.
  * Click [Entire] button to the image on the right canvas entirely pixelated.

* Area
  * Check 0.1, 0.05 or 0.025.
  * Right click and drag to draw rectangle on the image on the right canvas.
  * Click [Area] button to pixelate in the drawn rectangle.

* Detect
  * Click [Face Detect] button to pixelate faces in the image on the right canvas.
  * Click [Eye Detect] button to pixelate eyes in the image on the right canvas. 
  * If faild to detect, adjust scaleFactor and minNeighbors.

* Make animated GIF
  * Click [Run GIF] button to make an animated GIF and run it one time on the right canvas.
  * Click [Save GIF] button to make an animated GIF and save it. Open the saved file to run the animation Infinitely.

* Compare
  * Click [Compare] button to compare the images on the left and right canvases. Rectangles will be drawn at where difference is detected in the image on the righ canvas. 









  