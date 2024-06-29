from flask import Flask, request, render_template,jsonify
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

# Pneumonia= load_model("models\Pneumonia.keras")
# Eye=load_model("models\EyeDisease.h5")
# Skin=load_model("models\Skin.keras")

load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

bot_model = genai.GenerativeModel('gemini-pro')



app = Flask(__name__)

@app.route ("/chatbot", methods=["GET", "POST"])
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

@app.route('/') 
def home():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate credentials (you can check against a database or hard-coded values)
        if username == 'admin' and password == 'admin':
            # Successful login
            return 'Welcome, admin!'
        else:
            # Invalid credentials
            return 'Invalid username or password'

    # Display the login form
    return render_template('login.html')

@app.route('/prediction')
def image_recognition():
     if request.method == 'POST':
         image=request.files['image']
         if 'image'not in request.files:
             return jsonify({'error': 'no file'})
             
         if image.filename =='':
             return jsonify({'error': 'a error occured'})
         image.save('temp.jpg')
         image_path='temp.jpg'
          

         disease=request.form['disease']
         if disease =='lungs':
             pred1=preprocess_and_predict(image_path,Pneumonia)
         elif disease == 'skin':
             pred1=preprocess_and_predict_sk(image_path,Skin,disease)
         else: 
             pred1=preprocess_and_predict_sk(image_path,Eye,disease)

     return jsonify({'prediction':pred1})




     

if __name__ == "__main__":
    app.run(port="4000",debug=True)
