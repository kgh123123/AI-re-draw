from tensorflow.keras.applications import inception_v3  # <-- 이 부분이 반드시 포함되어야 합니다
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.random import normal
import numpy as np
import cv2
from transformers import CLIPProcessor, CLIPModel
import torch

# Load pre-trained models
inc_model = inception_v3.InceptionV3(weights='imagenet', include_top=False)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

#Function - Preprocess an image
def preprocess_img(img_path):
    img = load_img(img_path, target_size=(299, 299))  # InceptionV3 expects 299x299 images
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = x / 127.5 - 1.  # Normalize pixel values to range [-1, 1]
    #Scales the pixel intensity range from 0 - 255 to a range centered around 0
    #Positive values: Brighter pixels
    #Negative values: Darker pixels
    return x

#Function - Generate image noise
def generate_noise(shape):
    return normal(shape=shape, mean=0, stddev=1).numpy()


# Function - Generate a virtual image
def virtual_image(base_img_path, text_prompt, iterations=10):
    base_img = preprocess_img(base_img_path)
    virtual_img = generate_noise(base_img.shape)
    inputs = processor(text=text_prompt, return_tensors='pt')
    
    with torch.no_grad():
        text_features = model.get_text_features(**inputs).squeeze().numpy()  # (512,)
    
    for i in range(iterations):
        virtual_features = inc_model.predict(virtual_img)  # Shape: (1, 8, 8, 2048)
        virtual_features = np.mean(virtual_features, axis=(1, 2))  # Reduce to (1, 2048)
        virtual_features = virtual_features.squeeze()  # Shape: (2048,)
        
        # Calculate the loss function
        loss = np.dot(text_features, virtual_features)  # Dot product for alignment
        grad_des = np.gradient(loss)  # Calculate gradient
        virtual_img += grad_des * 0.1  # Update the virtual image

    # De-process the virtual image
    virtual_img[:, :, 0] += 1.
    virtual_img[:, :, 1] += 1.
    virtual_img[:, :, 2] += 1.
    virtual_img *= 127.5
    virtual_img = np.clip(virtual_img, 0, 255).astype('uint8')

    # Combine virtual image with the original one
    base_img = cv2.imread(base_img_path)
    virtual_img = cv2.resize(virtual_img, (base_img.shape[1], base_img.shape[0]))
    alpha = 0.5
    blended_img = cv2.addWeighted(base_img, alpha, virtual_img, 1 - alpha, 0)
    return blended_img


#Main
base_img1 = "imgs/lion.png"  # Path of the file
text_prompt1 = input("a scary lion")
virtual = virtual_image(base_img1, text_prompt1, iterations=20)
cv2.imwrite("imgs/generated_image.jpg", virtual)
print("Image has been generated and saved as 'generated_image.jpg' ")
#Done