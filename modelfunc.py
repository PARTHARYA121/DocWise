import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
import regex as re

eye_mapping = {
    0: 'Normal',
    1: 'Cataract',
    2: 'Diabetes',
    3: 'Glaucoma',
    4: 'HyperTension',
    5: 'Myopia',
    6: 'Age',
    7: 'Other'
}

skin_mapping = {
    0: 'Atopic Dermatitis',
    1: 'Basal Cell Carcinoma (BCC)',
    2: 'Benign Keratosis-like Lesions (BKL)',
    3: 'Eczema',
    4: 'Melanocytic Nevi',
    5: 'Melanoma',
    6: 'Psoriasis pictures Lichen Planus and related diseases',
    7: 'Seborrheic Keratoses and other Benign Tumors',
    8: 'Tinea Ringworm Candidiasis and other Fungal Infections',
    9: 'Warts Molluscum and other Viral Infections'
}
class_labels = ['Normal', 'Lung Opacity', 'Viral Pneumonia']

def enhance_image(image):
    image = cv2.addWeighted(image, 1.5, image, -0.5, 0)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image = cv2.filter2D(image, -1, kernel)

    image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    value = image_hsv[:, :, 2]
    value = np.clip(value * 1.25, 0, 255)

    image_hsv[:, :, 2] = value
    image = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2RGB)

    return image

def preprocess_and_predict(image_path,model):

        # Load and preprocess the image
        image = load_img(image_path, target_size=(256,256))
        image = img_to_array(image)
        image = enhance_image(image)
        image = preprocess_input(image)
        image = np.expand_dims(image, axis=0)  # Add batch dimension
        

        prediction = model.predict(image) 
        predicted_class = np.argmax(prediction, axis=1)[0]
        result = class_labels[predicted_class]
        return result


def preprocess_and_predict_sk(image_path, model, model_name):
    # Load and preprocess the image
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = tf.keras.applications.vgg19.preprocess_input(image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    
    # Make a prediction
    prediction = model.predict(image)
    predicted_class = np.argmax(prediction, axis=1)[0]
    
    # Map prediction to the corresponding class name
    if model_name == 'eye':
        result = eye_mapping.get(predicted_class, 'Unknown')
    elif model_name == 'skin':
        result = skin_mapping.get(predicted_class, 'Unknown')
    else:
        result = 'Invalid model name'
    
    return result

def clean_response(response_text):
    # Remove Markdown formatting (e.g., **bold**)
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', response_text)
    return cleaned_text

def generate_response(user_input,model):
    # Define the role and context for the chatbot
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    cleaned_response = clean_response(response.text.strip())
    return cleaned_response