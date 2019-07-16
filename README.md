# IB111 Projects
Repository for my projects made in the advanced group of the class IB111 - Basics of Programming.
In the file "Správa IB111.pdf" is a complete report (in Slovak) about the projects with analysis and graphs of the results.
There were three projects:
### 1. Simulation of a board game
- here I chose the "Pexeso" Game, where you have to find pairs of cards that you don't know the position of
- there are 3 types of strategy(more of a memory type): Random, Infinite, Finite (with memory type stack or queue)

### 2. Data handling and analyis
- I looked into the data of an online blank map test site(slepemapy.cz), which also uses Adaptive Learning
- input files had to be split becuase of the GitHub size limit - script won't work, has to rerun with changed values
- the main question was which continent do Czech and Slovak citizens know the best
- Nokia HereWeGo map API and `pycountry_convert` were used to fetch the continent on which certain location was, since this was not present in the dataset

### 3. Bitmap images
- one of our Professors made a genarator of punch tape images for studets to practice the conversion from binary to ASCII
- this Python script automates this process by using the `PIL` image library
