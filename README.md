# 🤖 Jarvis: Omni-Modal AI Operating System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg )](https://www.python.org/ )
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-FF4B4B.svg )](https://jarvis-omni-modal-ai-zulbdg7ncrtdwasjnpfse3.streamlit.app/ )
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED.svg )](https://www.docker.com/ )
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen.svg )](https://github.com/features/actions )

### 🚀 Live Application: [Experience Jarvis Here](https://jarvis-omni-modal-ai-zulbdg7ncrtdwasjnpfse3.streamlit.app/ )

## 📌 Overview
Jarvis is a real-time, multimodal AI assistant designed to replicate an enterprise-grade voice agent. It bridges the gap between unstructured audio data and actionable intelligence. The system is capable of transcribing live speech, maintaining stateful conversational memory, and synthesizing text-to-speech responses with ultra-low latency.

## 🏗️ System Architecture Deep Dive

The architecture is built on a three-stage pipeline: **Hearing, Thinking, and Speaking.**

1. **Hearing (Speech-to-Text):** Audio is captured via the Streamlit UI and routed to OpenAI's **Whisper** model. To achieve near-instantaneous transcription, inference is executed on **Groq's LPUs** (Language Processing Units) rather than traditional GPUs.
   
2. **Thinking (LLM & Memory):** The transcribed text is passed to **Llama-3 (120B)**. The conversational state is managed using **LangChain's Memory Buffers**, allowing the agent to retain context across multiple interactions rather than treating each prompt in isolation.
   
3. **Speaking (Text-to-Speech):** The LLM's text output is dynamically converted back into human speech using a REST API integration with **gTTS** (Google Text-to-Speech), completing the two-way multimodal loop.

## ⚙️ Key Engineering Decisions

| Component | Technology | Engineering Rationale |
| :--- | :--- | :--- |
| **Inference Engine** | Groq LPU | Provides sub-second latency for both Whisper and Llama-3, which is critical for real-time voice applications where delays break user immersion. |
| **Agent Framework** | LangChain | Simplifies the orchestration of prompt templates and session state memory, enabling true "Chatbot" functionality over simple Q&A. |
| **Deployment** | Docker & Streamlit | Containerizing the app ensures environment consistency across any machine, while Streamlit Cloud provides a rapid, accessible frontend for stakeholders. |

## 🐳 Run Locally via Docker (Recommended)

The application is fully containerized. You can pull and run the image directly from the GitHub Container Registry without installing Python dependencies.

```bash
# Pull the latest image
docker pull ghcr.io/munnurumahesh03-coder/jarvis-omni-modal-ai:latest

# Run the container on port 8501
docker run -p 8501:8501 ghcr.io/munnurumahesh03-coder/jarvis-omni-modal-ai:latest
```
*(Note: You will need to provide your own Groq API key in the UI once the app boots up).*

## 💻 Manual Local Installation

If you prefer to run the source code directly:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Jarvis-Omni-Modal-AI.git
cd Jarvis-Omni-Modal-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the OS
streamlit run app.py
```
