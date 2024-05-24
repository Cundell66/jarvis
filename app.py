import os
# from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from text2speech import tts
from flask import render_template, Flask, request
import jinja_partials
import uuid

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Create a ChatGroq instance with temperature=0 and the Groq API key
chat = ChatGroq(temperature=0.5, groq_api_key=groq_api_key, model_name="llama3-70b-8192")

# Create a Flask app instance
app = Flask(__name__)

# Register Jinja partials with the Flask app
jinja_partials.register_extensions(app)

# Define the system and human messages for the chat prompt
system = "You are a helpful and friendly personal assistant. You provide advice and suggestions and where necessary use follow up questions."
human = "{input}"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", system
        ), 
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", human),
    ]
)
chat_history = ChatMessageHistory()

# Define the home route (GET request)
@app.route("/", methods=["GET"])
def home():
    # Render the index.html template
    return render_template("index.html")

# Define the translate route (POST request)
@app.route("/", methods=["POST"])
def conversation():
    # Get the user input from the form
    input = request.form.get("query")
    
    # Create a chat chain with the prompt and chat instance
    chain = prompt | chat
    
    chain_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: chat_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    # Invoke the chat chain with the user input
    response = chain_history.invoke({"input": input},
                                    {"configurable": {"session_id": "unused"}},
                                ).content
    
    # Convert the response to speech using text-to-speech
    sound_file = tts(response)
    
    # Generate a unique ID for the response
    unique_id = str(uuid.uuid4())
    
    # Render the index.html template with the response, sound file, and unique ID
    return render_template("index.html", response=response, sound_file=sound_file, unique_id=unique_id)
