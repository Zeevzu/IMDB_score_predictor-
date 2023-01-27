# Predicting IMDB score from movie’s trailer
<p align="center">
<img src="https://static.amazon.jobs/teams/53/images/IMDb_Header_Page.jpg?1501027252" height="200" > </p>

In this project we attempt to use a Pre-trained model to predict from selected frames of a trailer, it's IMDB score.
We use Transfer-Learning by performing additional training on a pre-trained network, using the new dataset, to achieve this task.
The creation of this unique Dataset was made by scraping from the internet the trailers MP4 files and sampling frames from them.
This is a class project as part of EE046211 - Deep Learning course @ Technion.

<p align="center">
    Eran Mann: <a href="https://github.com/EranMann1">GitHub</a>
  <br>
    Ze'ev Zukerman:  <a href="https://github.com/Zeevzu">GitHub</a>
  </p>

Link to the Drive with the Project - <p align="center">
    <a href="https://drive.google.com/drive/folders/1ecvNFD-mHsSIs7fCg59mDQ6GgTRbyr9m?usp=share_link">Project Drive</a>
</p>

## Agenda
  * [I Just Want to Run The Code](#I%20Just%20Want%20to%20Run%20The%20Code)
  * [Background](#Background)  
  * [Dataset](#Dataset)  
  * [Model](#Model)  
  * [Training And Results](#Training-And-Results)
  * [Files in the repository](#Files-in-the-repository)


## Background

As mentioned previously, the goal of the project is to obtain the IMDB score of a movie, based on it's trailer, As showed in the following block diagram.
<p align="center">
<img src="./README images/Block Diagram wanted.png" height="300" > </p>

The main constraints we made for this project is reasonable traning and inference time. Those constraints guided us to be more creative with the input of our model.
To have reasonable traning and inference time we used a pre-trained DNN model, also we assumed that video as an input will cause a huge input layer with big redundancy between following frames, as result we chose to sample randomly meaningful frames from the trailer and to have small amount of frames as the input to the model. So the actuall block diagram of our project is as follows.
<p align="center">
<img src="./README images/Block Diagram Actual.png" height="300" > </p>

## Dataset
For the movie scores dataset we used - <p align="center">
    <a href="https://www.kaggle.com/code/saurav9786/imdb-score-prediction-for-movies/data"> IMDB Movies Dataset </a></p>
For the trailers themselvs we used the excel file found under  directory excels, which connect movie title with it's trailer youtube url. This excel is quite old, so some of the urls there dont exist anymore.

As mentioned above, the model input is a few random frames from the trailer. The problem with that is that maney movie frames are not informative. Some frames containe companey logo, text, fade away between two other frames, etc...

<p align="center">
<img src="./README images/bad frames.PNG" height="500" > </p>

To combat that we used a preproceccing algorithm before choosing the "random" frames. For each trailer we sample a 100 frames, and for each frame we compute the mean and the variance. Than we deleate the frames with exceptianly low mean or variance compaired to the rest of the frames. Low mean coralates with black frames, and low std coralates with uniform frames (such as text on a uniform background).
After that we sample random frames from the remaining frame pool.





## Model
As mentioned in the Background section, We worked with pre-trained Deep Neural Networks. The architectures we chose were - Resnet50, Resnet18 and VGG16. To all of those models we updated the input layer and the first 2D convolution layer to get 15 input channels. Also we added a linear output layer with 1 output because we use the network for regression task.
As we can see in the next section, the architecture which achieved the best results was the VGG16, with the following updated architecture as showed below.
<p align="center">
<img src="./README images/VGG16.png" height="400" > </p>


## Training And Results
We trained our models with Adam and a learning rate schezualer. Ther were a few training scemes and compaired the results. The schemes included changing the number of input frames to the model (5 RGB frame or 15 RGB frames), changing the input data augmentation (noising/ not noisng the frames, changing frames between ephochs, reordering frames in the input). We also changed the kind and depth of the input models (resnet50, resnet18, vgg16,vgg19). 

We trained the models with mse loss between the predicted score and the real score. In order to ease the learning process, and to improve our understanding of the results we standartize the IMDN score labels.
We also used l2 regularization.
The best model was VGG16. It's final test score (on the normilized data) is 0.76. Since the labels are stundertize, the naive guess gives a score of 1. This is a 25% improvement.
The leaning curve of this model is:

<p align="center">
<img src="./README images/VggTraining.png" height="400" > </p>

## Files in the repository
### excels
In the excels directory there are two excels files from wich we get the dataset. In the "movies_metadata.csv" file there is the movir title, year of publication. IMDB score, genere, director, etc...
In the "ml-youtube.csv" file there is a connection between movie title, and youtube url. The excel is old so some of the video trailers there are either non existed or private. to get to the actual url the prefix "https://www.youtube.com/watch?v=" is needed before the writen url.
### Images
The "images" directory containe the frames of the trailers. For each movie there will be a folder with frames from its trailer: "\imgaes\{movie title}\{num}.jpg". The images are after filtering of bad frame (completely dark frames, frames with mainly text, etc...). There are between 50 to 100 frames per trailer.
what presented in this repository is very few trailers in order to not have to much data.
### dataset
In this folder there is a file in the pickle format that contain a dataset one can simply load to train a model with
### code
In thif folder we have all of the code files needed to scrape the internet, preprocess the data, and train a model. Most of the code is writen in google colab (.ipynb files), and the rest in pure python (.py files). Here we present a in depth analasys of the code. In the next section we present a short description of haw to run the project.
#### scrape_from_internet.ipynb
This file download frames from the trailer in order to create the training dataset. It reads the excels, and create a list of movie titles, the scores, and their respective youtube url. The it shuffles the list (in order to not have some kind of movie bias), and donload 2000 trailers in the following way:
First we download a trailer
Then we take a 100 random frames from it and deleate the trailer (it takes a lot of memories).
Out of this frames we take the statistics of the frames mean and std. We deleate the frames whos mean or std is in 20'th percentile (lowest mean and lowest std).
This ensure to deleate frames that are not informative.
We save the remaining frames in "\imgaes\{movie title}\{num}.jpg".

#### CreateDatasetFromImages.ipynb
This file usses the downloaded frames and creates a numpy dataset of the frames and the scores. The dataset is a list of movies, each movie contain 15 frames from the trailer, and its score. The 15 frames are stores as a 45 channels picture (15 frames, each one has RGB channels). The dataset is saved in a file names Dataset.

#### trainModel.ipynb
This file train the model. here the user have a lot of controll. you controll the pretrained model (resnt vs vgg and the model depth). You controll the the augmentations done on the model. You controll the optimizer and scedualer parameters. You controll the input size. each section of the notebook is explained in the text above. If you run it with no changes at all, it will use the defult parameters.
