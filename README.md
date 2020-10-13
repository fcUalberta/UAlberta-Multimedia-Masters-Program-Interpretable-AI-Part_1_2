# Interpretable AI: Image Classification with Improved Visual Attention

This repository contains source code for Part 1 & 2 of our project which is based on improving Activation based techniques

## About
In this research, we implemented latest ABM Techniques on VGG16 classifier and also on state-of-the-art classifier InceptionV3 and Xception and compared its results. We also performed 3 experiments to improve the saliency map by Activation based methods(ABM) such as Grad-CAM, Grad-CAM++, Smooth Grad-CAM++ by using a novel combination with Backpropagation method called as Integrated Gradients

P.S: The main source code for Part1_CamOnDiffClassifiers and Part2_NovelCombination is added as a jupyter notebook for ease of visualization of results. Each cell takes few minutes to run. 

Part 1:
- New implementation of Grad-CAM Grad-CAM++ & Smooth Grad-CAM++ in VGG16
- Extending the above techniques for Xception & InceptionV3

Part 2: 
- Novel Combination of Integrated Gradients and CAM techniques on VGG16


## Project Structure

![GitHub Logo](/FinalResults/part2_struc.png)

## Hardware Requirements
1. Google Colab with 25 GB RAM
1. GPU is not mandatory

## Software Requirements
- Refer requirements.txt

## How to run this application?

1. Create environment with requirements.txt
1. Make sure you have hardware requirements 
1. Download the folder
1. Open code/Part1_CamOnDiffClassifiers.ipynb to run Part 1 or code/Part2_NovelCombination.ipynb to run Part 2
1. If running on Google Colab, upload this project, mount your Google drive by uncommenting the first cell
1. Change the base directory to reflect your local file structure
1. Run each cell in sequential order

## Results of Experiment

### Part 1 : Visualizing Grad-CAM, Grad-CAM++ , Smooth Grad-CAM++ on various classifiers

![GitHub Logo](/FinalResults/1.1.jpg)
![GitHub Logo](/FinalResults/1.2.jpg)
![GitHub Logo](/FinalResults/1.3.jpg)

### Part 2 : Novel Combination of above CAM techniques with Integrated Gradients 

#### Experiment 1: Direct Combination
![GitHub Logo](/FinalResults/2.1.jpg)

#### Experiment 2: Indirect Combination
![GitHub Logo](/FinalResults/2.2.jpg)


### Reference Papers:
- Grad-CAM https://arxiv.org/abs/1610.02391
- Grad-CAM ++ https://arxiv.org/abs/1710.11063
- Smooth Grad-CAM ++ https://arxiv.org/abs/1908.01224
- Integrated Gradients https://arxiv.org/abs/1703.01365

### References kernels:
- https://github.com/adityac94/Grad_CAM_plus_plus
- https://github.com/totti0223/gradcamplusplus
- https://github.com/yiskw713/SmoothGradCAMplusplus
- Integrated Gradients implemented from https://github.com/ankurtaly/Integrated-Gradients
