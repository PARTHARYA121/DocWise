from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import google.generativeai as genai
import re

# Load environment variables from .env file
load_dotenv()

# Configure genai with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def clean_response(response_text):
    # Remove Markdown formatting (e.g., **bold**)
    cleaned_text = re.sub(r'\*\*(.*?)\*\*', r'\1', response_text)
    return cleaned_text

def generate_response(user_input):
    # Define the role and context for the chatbot
    role_instruction = (
        "You are a medical chatbot. Your purpose is to provide medical advice, "
        "answer health-related questions, and help users understand their symptoms. "
        "If the user asks questions that are not related to medical topics, politely decline to answer."
    )
    response = model.generate_content(f"{role_instruction}\n\nUser: {user_input}\nChatbot:")
    cleaned_response = clean_response(response.text.strip())
    return cleaned_response

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
            response_text = generate_response(user_input)
            conversation += f"\nChatbot: {response_text}"
    
    return render_template("index.html", conversation=conversation, user_input=user_input)

if __name__ == "__main__":
    app.run(port="4000",debug=True)
