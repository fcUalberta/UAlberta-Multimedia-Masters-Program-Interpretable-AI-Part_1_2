# -*- coding: utf-8 -*-
"""CAM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uYrXrDxUGU5mQls4X6BGH_a76gTT89Um

Implementing All the Class Activation Techniques as Classes
"""

# Checking tensorflow version to make sure it is between 1.13 and 1.15
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
print(tf.__version__)

from scipy.ndimage.interpolation import zoom
import numpy as np
import keras.backend as K

class GradCAM():
    """ 
    Implements the Gradient of Class Activation Mapping(CAM)
    
    """

    def __init__(self,model,target_layer, prediction,H=224,W=224):
        """
        Initializing variables for the class GradCAM
        
        Args:
            model: Classifier on which CAM is generated 
            target_layer: Target convolutional layer to be visualized
            prediction : Prediction w.r.t input
            H,W: Height and width of input image
        """
        self.model = model
        self.target_layer = target_layer
        self.prediction = prediction
        self.H = H
        self.W = W    

    def __call__(self, x):
        """
        Invokes the gradCAM function to generate CAM
        
        Args:
            x: input image. shape =>(1, 3, H, W)
        
        Return:
            cam: class activation mappings of the predicted class shown as heatmap
        """
        cam = self.getGradCAM(x)
        return cam
        
    def getGradCAM(self, image):
        '''
        Finds the cam by calculating the linear combination of activations
        
        Args:        
        image: test image that needs to be classified
        
        Returns:
        cam: class activation map.  shape=> (1, 1, H, W)
        '''
        class_score = self.model.output[0, self.prediction]
        conv_layer_output = self.model.get_layer(self.target_layer).output
        grads = K.gradients(class_score, conv_layer_output)[0]
        gradient_function = K.function([self.model.input], [conv_layer_output, grads])

        output, grads_val = gradient_function([image])
        output, grads_val = output[0, :], grads_val[0, :, :, :]
        
        weights = np.mean(grads_val, axis=(0, 1))
        
        # Linear combination of activations
        cam = np.dot(output, weights)

        # Passing through ReLU
        cam = np.maximum(cam, 0)
        cam = zoom(cam,self.H/cam.shape[0])
        cam = cam / cam.max()
        
        return cam

from skimage.transform import resize
class GradCAMPlusPlus():
    """ 
    Implements the Improved version of Gradient of Class Activation Mapping(CAM) ++
    
    """

    def __init__(self,model,target_layer,prediction,H=224,W=224):
        """
        Initializing variables for the class GradCAMPlusPlus
        
        Args:
            model: Classifier on which CAM is generated 
            target_layer: Target convolutional layer to be visualized
            prediction : Prediction w.r.t input
            H,W: Height and width of input image
        """
        self.model = model
        self.target_layer = target_layer
        self.prediction = prediction
        self.H = H
        self.W = W
        
      
    def __call__(self, x):
        """
        Invokes the gradCAMPlusPlus function to generate CAM
        
        Args:
            x: input image. shape =>(1, 3, H, W)
        
        Return:
            cam: class activation mappings of the predicted class shown as heatmap
        """
        cam = self.getGradCAMPlusPlus(x)

        return cam

    def getGradCAMPlusPlus(self, image):
        '''
        Finds the cam by calculating the linear combination of activations
        
        Args:        
        image: test image that needs to be classified
        
        Returns:
        cam: class activation map.  shape=> (1, 1, H, W)
        '''
        class_score = self.model.output[0, self.prediction]
        conv_layer_output = self.model.get_layer(self.target_layer).output
        grads = K.gradients(class_score, conv_layer_output)[0]
       
        # Finding first, second and third derivative of gradients respectively        
        first_derivative = K.exp(class_score)*grads
        second_derivative = K.exp(class_score)*grads*grads
        third_derivative = K.exp(class_score)*grads*grads*grads
        
        gradient_function = K.function([self.model.input], [class_score,first_derivative,\
                            second_derivative,third_derivative, conv_layer_output, grads])
        
        class_score, conv_first_grad, conv_second_grad,conv_third_grad, conv_layer_output, grads_val = gradient_function([image])
        
        global_sum = np.sum(conv_layer_output[0].reshape((-1,conv_first_grad[0].shape[2])), axis=0)
         
        alpha_num = conv_second_grad[0]
        alpha_denom = conv_second_grad[0]*2.0 + conv_third_grad[0]*global_sum.reshape((1,1,conv_first_grad[0].shape[2]))
        alpha_denom = np.where(alpha_denom != 0.0, alpha_denom, np.ones(alpha_denom.shape))
        alphas = alpha_num/alpha_denom

        weights = np.maximum(conv_first_grad[0], 0.0)
        
        alphas_thresholding = np.where(weights, alphas, 0.0)

        alpha_normalization_constant = np.sum(np.sum(alphas_thresholding, axis=0),axis=0)
        alpha_normalization_constant_processed = np.where(alpha_normalization_constant != 0.0, alpha_normalization_constant, np.ones(alpha_normalization_constant.shape))

        alphas /= alpha_normalization_constant_processed.reshape((1,1,conv_first_grad[0].shape[2]))
        
        deep_linearization_weights = np.sum((weights*alphas).reshape((-1,conv_first_grad[0].shape[2])),axis=0)
        
        grad_CAM_map = np.sum(deep_linearization_weights*conv_layer_output[0], axis=2)

            
        # Passing through ReLU
        cam = np.maximum(grad_CAM_map, 0)
        cam = zoom(cam,self.H/cam.shape[0])
        cam = cam / np.max(cam) # scale 0 to 1.0    
        
        return cam

from keras.layers import GaussianNoise
class SmoothGradCAMPlusPlus(GradCAMPlusPlus):
    """ Implements Smooth Grad CAM Plus Plus """

    def __init__(self, model, target_layer, prediction, n_samples=25, stdev_spread=0.15):
        """
        Args:
            model: Classifier on which CAM is generated 
            target_layer: Target convolutional layer to be visualized
            prediction : Prediction w.r.t input
            n_sample: the number of samples
            stdev_spread: standard deviationß
        """

        self.model = model
        self.target_layer = target_layer
        self.n_samples = n_samples
        self.stdev_spread = stdev_spread
        self.prediction = prediction
        super().__init__(self.model,self.target_layer,self.prediction)

    def __call__(self, x):
        """
        Args:
            x: input image. shape =>(1, 3, H, W)
        Return:
            cam: class activation mappings of predicted classes
        """
        cam = self.getSmoothGradCAMPP(x)

        return cam
    
    def getSmoothGradCAMPP(self,x):
        """
        Args:
            x: input image. shape =>(1, 3, H, W)
        Return:
            Total_cams: mean of class activation mappings of n_samples
        """

        stdev = self.stdev_spread / (x.max() - x.min())
        
        std_tensor = np.ones_like(x) * stdev
                
        for i in range(self.n_samples):
            x_with_noise = K.random_normal(shape = (x.shape), mean=x,stddev=std_tensor)
            smg_cam = super().getGradCAMPlusPlus(x_with_noise)
            #smg_cam = cam(GradCAMPlusPlus,self.model,self.target_layer,self.prediction,x_with_noise)

            if i == 0:
                total_cams = smg_cam.copy()
            else:
                total_cams += smg_cam

        total_cams /= self.n_samples
        
        return total_cams
