import streamlit as st
import os
import tempfile
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from gtts import gTTS

st.set_page_config(page_title="Jarvis Omni-Modal OS", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; color: #00ffcc; font-family: 'Courier New', Courier, monospace; }
    h1, h2, h3 { color: #00ffcc !important; text-shadow: 0px 0px 10px #00ffcc; }
    .stAudio { border: 2px solid #00ffcc; border-radius: 10px; box-shadow: 0px 0px 15px #00ffcc; }
    .stTextArea textarea, .stChatInput input { background-color: #111111 !important; color: #ffffff !important; border: 1px solid #00ffcc !important; }
    /* Custom Download Button */
    .stDownloadButton button { border: 1px solid #00ffcc; color: #00ffcc; background-color: transparent; }
    .stDownloadButton button:hover { background-color: #00ffcc; color: #000000; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Jarvis: Omni-Modal Operating System")
st.markdown("*Advanced AI Assistant equipped with Speech Recognition, Audio Synthesis, and LLM Reasoning.*")

# --- SECURE API KEY HANDLING ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.environ.get("GROQ_API_KEY")

with st.sidebar:
    st.header("🎛️ Select Protocol")
    # THE FIX: Upgraded the name to sound much cooler!
    app_mode = st.radio("Active Interface:", [
        "📁 Audio Intelligence Protocol", 
        "🗣️ Real-Time Voice (Jarvis)",
        "💬 Omni-Agent Chat"
    ])
    st.divider()
    st.caption("Status: Online 🟢")
    st.caption("Core: Groq LPU + Llama-3")

if api_key:
    client = Groq(api_key=api_key)
    llm = ChatGroq(temperature=0, model_name="qwen/qwen3.8-27b")
    
    # ---------------------------------------------------------
    # MODE 1 & 2: AUDIO PROCESSING
    # ---------------------------------------------------------
    if app_mode in ["📁 Audio Intelligence Protocol", "🗣️ Real-Time Voice (Jarvis)"]:
        audio_data = None
        if app_mode == "📁 Audio Intelligence Protocol":
            st.subheader("Upload Audio Data (MP3/WAV)")
            audio_data = st.file_uploader("Drop audio file for deep analysis", type=["mp3", "wav", "m4a"])
        else:
            st.subheader("Voice Interface Active")
            st.info("Click the microphone, speak your query, and click stop to transmit.")
            audio_data = st.audio_input("Transmit Audio")

        if audio_data is not None:
            st.audio(audio_data)
            if st.button("🚀 Execute Protocol"):
                with st.spinner("Processing audio transmission..."):
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                        tmp_file.write(audio_data.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        with open(tmp_file_path, "rb") as file:
                            transcription = client.audio.transcriptions.create(
                                file=(tmp_file_path, file.read()),
                                model="whisper-large-v3",
                                response_format="text",
                            )
                        
                        st.success("Audio Decoded!")
                        with st.expander("📝 View Raw Transcript"):
                            st.write(transcription)
                        
                        with st.spinner("Synthesizing response..."):
                            if app_mode == "📁 Audio Intelligence Protocol":
                                prompt = PromptTemplate.from_template("""
                                You are an elite Executive Assistant. Read the transcript and extract the key points.
                                TRANSCRIPT: {transcript}
                                Provide:
                                1. A one-sentence summary.
                                2. A bulleted list of Action Items.
                                """)
                            else:
                                prompt = PromptTemplate.from_template("""
                                You are Jarvis, a highly intelligent, concise AI assistant. 
                                The user just spoke to you and said: "{transcript}"
                                Answer their question or respond directly and concisely. Do not use emojis.
                                """)
                                
                            chain = prompt | llm
                            response = chain.invoke({"transcript": transcription})
                        
                        st.subheader("🎯 System Output:")
                        st.info(response.content)
                        
                        if app_mode == "📁 Audio Intelligence Protocol":
                            st.download_button(
                                label="📥 Download Intelligence Report",
                                data=response.content,
                                file_name="Jarvis_Audio_Intelligence_Report.txt",
                                mime="text/plain"
                            )
                        
                        if app_mode == "🗣️ Real-Time Voice (Jarvis)":
                            with st.spinner("Generating voice reply..."):
                                # NEW: Clean the Markdown symbols so Jarvis doesn't read them out loud!
                                clean_text = response.content.replace("*", "").replace("#", "").replace("_", "")
                                tts = gTTS(clean_text, lang='en')
                                tts.save("reply.mp3")
                                st.audio("reply.mp3", format="audio/mp3", autoplay=True)

                    except Exception as e:
                        st.error(f"Audio processing failed. Please try speaking clearer or uploading a valid file. Error: {e}")
                    finally:
                        os.remove(tmp_file_path)

    # ---------------------------------------------------------
    # MODE 3: TEXT CHAT WITH MEMORY
    # ---------------------------------------------------------
    elif app_mode == "💬 Omni-Agent Chat":
        st.subheader("Terminal Chat Interface")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage(content="You are Jarvis, an advanced AI operating system. Be helpful, concise, and professional.")
            ]

        for msg in st.session_state.messages:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)
            elif isinstance(msg, AIMessage):
                with st.chat_message("assistant", avatar="🤖"):
                    st.write(msg.content)

        user_input = st.chat_input("Type your command here...")
        
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            st.session_state.messages.append(HumanMessage(content=user_input))
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Processing..."):
                    response = llm.invoke(st.session_state.messages)
                    st.write(response.content)
            st.session_state.messages.append(AIMessage(content=response.content))

else:
    st.error("CRITICAL ERROR: API Key not found in environment secrets.")
