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
  * [Background](#Background)  
  * [Dataset](#Dataset)  
  * [Model](#Model)  
  * [Training and Results](#Training%20and%20Results)
  * [Files in the repository](#Files%20in%20the%20repository)


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


## Training The Model
We trained our models with Adam and a learning rate schezualer. Ther were a few training scemes and compaired the results. The schemes included changing the number of input frames to the model (5 RGB frame or 15 RGB frames), changing the input data augmentation (noising/ not noisng the frames, changing frames between ephochs, reordering frames in the input). We also changed the kind and depth of the input models (resnet50, resnet18, vgg16,vgg19). 

We trained the models with mse loss between the predicted score and the real score. In order to ease the learning process, and to improve our understanding of the results we standartize the IMDN score labels.
We also used l2 regularization.
The best model was VGG16. It's final test score (on the normilized data) is 0.76. Since the labels are stundertize, the naive guess gives a score of 1. This is a 25% improvement.
The leaning curve of this model is:

<p align="center">
<img src="./README images/VggTraining.png" height="400" > </p>


