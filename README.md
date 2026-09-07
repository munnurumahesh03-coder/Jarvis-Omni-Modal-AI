# 🤖 Jarvis: Omni-Modal AI Operating System

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg )](https://www.python.org/ )
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B.svg )](https://jarvis-omni-modal-ai-zulbdg7ncrtdwasjnpfse3.streamlit.app/ )
[![LangChain](https://img.shields.io/badge/LangChain-Framework-green.svg )](https://langchain.com/ )
[![Groq](https://img.shields.io/badge/Groq-LPU_Inference-f55036.svg )](https://groq.com/ )
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper_v3-white.svg )](https://openai.com/research/whisper )

### 🚀 Live Application: [Experience Jarvis Here]( )

## 📌 Executive Overview
Jarvis is a production-ready, Omni-Modal AI Assistant designed to bridge the gap between human speech and Large Language Model reasoning. Moving beyond standard text-based chatbots, this system processes unstructured audio data, performs real-time speech-to-text inference, and maintains stateful conversational memory. Built on top of Groq's ultra-low latency LPU architecture, the system seamlessly integrates OpenAI's Whisper model for hearing, Llama-3/Qwen for reasoning, and Google TTS for vocal synthesis.

## 🎛️ Core Protocols (Features)

### 1. 📁 Audio Intelligence Protocol (Batch Processing)

* **Business Use Case:** Enterprise meeting summarization, lecture transcription, and automated data extraction.
  
* **Functionality:** Users upload raw audio files (`.mp3`, `.wav`, `.m4a`). The system transcribes the audio and utilizes a strict LLM Executive Assistant prompt to extract a concise summary and a bulleted list of actionable items.
  
* **UX Feature:** Includes a one-click export to download the final intelligence report as a `.txt` file.


### 2. 🗣️ Real-Time Voice Interface

* **Business Use Case:** Hands-free, real-time AI interaction and accessibility.
  
* **Functionality:** Captures live microphone input directly via the browser. It transcribes the speech in milliseconds, processes the query through the LLM, and automatically synthesizes a vocal response using Text-to-Speech (TTS), playing it back to the user instantly.


### 3. 💬 Omni-Agent Chat
* **Business Use Case:** Deep reasoning, coding assistance, and contextual conversation.
  
* **Functionality:** A terminal-style chat interface equipped with LangChain `SystemMessage` and `HumanMessage` memory buffers. This allows the AI to maintain context and remember previous interactions throughout the entire session.


## 🧠 System Architecture Deep Dive

The application follows a strict, modular pipeline to handle multimodal data:

1. **Audio Ingestion:** Streamlit captures audio (either via file upload or WebRTC microphone input) and writes it to a secure, temporary binary file (`tempfile.NamedTemporaryFile`).
   
2. **Speech-to-Text (STT):** The binary file is transmitted to Groq's API, where the `whisper-large-v3` model performs zero-shot transcription.
  
3. **LLM Orchestration:** The transcribed text is injected into LangChain `PromptTemplates`. Depending on the active mode, it is either processed statelessly (for summarization) or appended to a `session_state` memory buffer (for chat).
   
4. **Text-to-Speech (TTS):** The LLM's text output is passed to `gTTS`, which generates an MP3 file on the fly. Streamlit's audio component is triggered with `autoplay=True` for immediate playback.


## ⚙️ Key Engineering Decisions

| Component | Technology Chosen | Engineering Rationale |
| :--- | :--- | :--- |
| **Inference Engine** | Groq LPU | Traditional GPUs cause noticeable lag in voice assistants. Groq's LPUs provide near-instantaneous token generation, crucial for real-time voice interactions. |
| **Orchestration** | LangChain | Provided the necessary abstractions for conversational memory (`AIMessage`, `HumanMessage`) and dynamic prompt routing. |
| **Frontend UI** | Streamlit + Custom CSS | Allowed for rapid Python-based deployment while utilizing injected CSS to create a custom, dark-mode cybernetic aesthetic. |


## 🛠️ Technical Challenges Overcome

* **Volatile Memory Management:** Streamlit reruns the entire script on every user interaction. To prevent the AI from forgetting the conversation, LangChain message histories were bound directly to Streamlit's `session_state`.
* **Audio File Handling:** Cloud deployments restrict direct file system access. This was solved by utilizing Python's `tempfile` library to create and destroy audio buffers dynamically, preventing memory leaks and storage overflow.
* **API Rate Limiting:** Mitigated Groq token limits during heavy memory-buffer chats by dynamically routing to higher-tier open-source models (`gpt-oss-120b`) for sustained conversations.


## 💻 Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Jarvis-Omni-Modal-AI.git
cd Jarvis-Omni-Modal-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API Keys
mkdir .streamlit
echo 'GROQ_API_KEY = "your_groq_api_key"' > .streamlit/secrets.toml

# 4. Launch the OS
streamlit run app.py
```
