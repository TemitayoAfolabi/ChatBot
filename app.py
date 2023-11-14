from flask import Flask, render_template, request, redirect, url_for, session
import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key) # Sanity check FsCOF

app = Flask(__name__)

#Home page route iZvvgch
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chatbot", methods=["POST"])
def chatbot(): 
    # Get user input from form
    user_input = request.form["message"]
    # Get chatbot response from OpenAI
    prompt = f"Q: {user_input}\nA:"
    chat_history = []
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\nUser", " \nChatbot", " AI:"]
    )
    # Store chatbot response in variable
    chatbot_response = response["choices"][0]["text"]

    #Add user input and chatbot response to chat history
    chat_history.append(f"User: {user_input}\nChatbot: {chatbot_response}")

    # Render chatbot response in template
    return render_template("index.html", user_input=user_input, chatbot_response=chatbot_response)

#Run app
if __name__ == "__main__":
    app.run(debug=True)