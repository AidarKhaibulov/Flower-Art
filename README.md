# Flower Art
Computer graphics artwork. It's raster graphics flower drawn by using Bézier curves in order to animate petals tearing off.

#HOW TO USE
Open flower.py file, download required modules and run the script. The resulting file will be saved with the name flower1.gif. There are several demo files named demo1 and demo2 which demonstrate artwork.

#More about work
Tearing petals off logic implemented by using Bézier curves and shifting&rotation matrix. Firstly two curves are drawn in the center, then they rotate to the desired angle and shift to the flower's center, after that the space between curves is filled. In each frame petals are shifted from the flower's center. Used Matplotlib and Numpy.
