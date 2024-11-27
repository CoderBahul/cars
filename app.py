import os
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pydub.playback
from pydub import AudioSegment
import tempfile
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from dotenv import load_dotenv
import google.generativeai as genai

# Set ffmpeg path explicitly if necessary
AudioSegment.ffmpeg = "E:/Gemini/ffmpeg/bin/ffmpeg.exe"

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the conversational model
chat_model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# Helper Functions
def text_to_speech(text):
    """Convert text to speech and play it instantly."""
    if not text.strip():
        return
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        audio = AudioSegment.from_file(temp_audio.name)
        fast_audio = audio.speedup(playback_speed=1.3)
        pydub.playback.play(fast_audio)

def speech_to_text():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening for your query...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio)
            return query
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand. Please try again."
        except sr.RequestError:
            return "Error with the speech recognition service."

def detect_wakeword():
    """Continuously listen for the wake word 'Wake Up'."""
    recognizer = sr.Recognizer()
    st.info("Listening for the wake word 'Wake Up'...")
    with sr.Microphone() as source:
        while True:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                query = recognizer.recognize_google(audio)
                if "WAKE UP" in query.upper():
                    st.success("Wake word detected: 'Wake Up'")
                    return True
            except sr.UnknownValueError:
                # Continue listening
                pass
            except sr.RequestError:
                st.error("Microphone or recognition service error.")
                break
    return False

def get_pdf_text(pdf_docs):
    """Extract text from uploaded PDFs."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    """Split text into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return splitter.split_text(text)

def create_vector_store(text_chunks):
    """Create a vector store from text chunks."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def query_pdf(question):
    """Query the processed PDF data."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings)
    docs = vector_store.similarity_search(question)

    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    If the answer is not available in the context, say, "I couldn't find the answer in the provided PDF."
    
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(chat_model, chain_type="stuff", prompt=prompt)

    response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
    return response.get("output_text", "Sorry, I couldn't find an answer.")

def general_chatbot_response(query):
    """Handle general chat queries."""
    try:
        response = chat_model.predict(query)
        return response
    except Exception as e:
        return f"Sorry, an error occurred: {e}"

# Main App
def main():
    st.set_page_config(page_title="Chat with PDF and AI", layout="wide")
    st.title("Two-in-One Bot: PDFBot & ChatGPT Clone")
    
    bot_type = st.sidebar.radio("Choose Bot", ["PDFBot", "ChatGPT Clone"], index=0)
    voice_chat_active = False  # Start with manual typing by default

    if bot_type == "PDFBot":
        st.subheader("PDFBot: Ask Questions from Uploaded PDFs")
        pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True)

        if st.button("Process PDFs"):
            with st.spinner("Processing..."):
                if pdf_docs:
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    create_vector_store(text_chunks)
                    st.success("PDFs processed successfully! You can now ask questions.")
                else:
                    st.error("Please upload at least one PDF.")

        question = st.text_input("Ask a Question from the PDFs:")
        if question:
            with st.spinner("Thinking..."):
                answer = query_pdf(question)
                st.write("Response:", answer)

        if detect_wakeword():
            st.info("Voice chat activated. Speak your query.")
            voice_question = speech_to_text()
            if voice_question:
                with st.spinner("Thinking..."):
                    answer = query_pdf(voice_question)
                    st.write("Response:", answer)
                    text_to_speech(answer)

    elif bot_type == "ChatGPT Clone":
        st.subheader("ChatGPT Clone: Ask Anything!")
        query = st.text_input("Ask your question here:")
        if query:
            with st.spinner("Thinking..."):
                answer = general_chatbot_response(query)
                st.write("Response:", answer)

        if detect_wakeword():
            st.info("Voice chat activated. Speak your query.")
            voice_query = speech_to_text()
            if voice_query:
                with st.spinner("Thinking..."):
                    answer = general_chatbot_response(voice_query)
                    st.write("Response:", answer)
                    text_to_speech(answer)

if __name__ == "__main__":
    main()
