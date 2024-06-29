from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os
from tensorflow.keras.models import load_model
from modelfunc import preprocess_and_predict,preprocess_and_predict_sk,clean_response,generate_response

# Ensure the 'models' directory exists
os.makedirs('models', exist_ok=True)

# URLs to your models on Hugging Face
urls = {
    'Pneumonia': 'https://huggingface.co/ShlokArora2709/DocWise/blob/main/Pneumonia.keras',
    'EyeDisease': 'https://huggingface.co/ShlokArora2709/DocWise/blob/main/EyeDisease.h5',
    'Skin': 'https://huggingface.co/ShlokArora2709/DocWise/blob/main/Skin.keras'
}

def download_model(url, file_name):
    if not os.path.exists(file_name):
        print(f'Downloading {file_name}...')
        response = requests.get(url)
        response.raise_for_status()
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f'{file_name} downloaded successfully.')

for name, url in urls.items():
    file_name = os.path.join('models', f'{name}.keras' if 'keras' in url else f'{name}.h5')
    download_model(url, file_name)

Pneumonia= load_model("models\Pneumonia.keras")
Eye=load_model("models\EyeDisease.h5")
Skin=load_model("models\Skin.keras")

load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

bot_model = genai.GenerativeModel('gemini-pro')



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if "conversation" not in request.form:
        conversation = ""
    else:
        conversation = request.form["conversation"]
        
    user_input = ""
    if request.method == "POST":
        user_input = request.form["user_input"]
        if user_input:
            conversation += f"\nYou: {user_input}"
            response_text = generate_response(user_input,bot_model)
            conversation += f"\nChatbot: {response_text}"
    
    return render_template("index.html", conversation=conversation, user_input=user_input)

if __name__ == "__main__":
    app.run(port="4000",debug=True)
