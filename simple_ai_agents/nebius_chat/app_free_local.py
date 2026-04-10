import json
import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

st.set_page_config(page_title="Local AI Chat", page_icon="🧠", layout="wide")


class LocalStudioChat:
    def __init__(self):
        self.models = {
            "Llama 3.1 8B": "llama3.1:8b",
            "Qwen 2.5 7B": "qwen2.5:7b",
            "Phi 4 Mini": "phi4:mini",
        }
        self.conversation_history = []
        self.custom_instruction = "You are a helpful AI assistant."

    def send_message(
        self,
        message,
        model="llama3.1:8b",
        temperature=0.6,
        max_tokens=2048,
        top_p=0.95,
    ):
        try:
            llm = ChatOllama(
                model=model,
                temperature=temperature,
                num_predict=max_tokens,
                top_p=top_p,
            )

            prompt_parts = []
            if self.custom_instruction:
                prompt_parts.append(f"System: {self.custom_instruction}")
            for entry in self.conversation_history[-5:]:
                prompt_parts.append(f"User: {entry['user']}")
                prompt_parts.append(f"Assistant: {entry['assistant']}")
            prompt_parts.append(f"User: {message}")
            prompt_parts.append("Assistant:")

            prompt = "\n\n".join(prompt_parts)
            assistant_response = llm.invoke(prompt).content.strip()
            conversation_entry = {
                "timestamp": datetime.now().isoformat(),
                "user": message,
                "assistant": assistant_response,
                "model": model,
                "temperature": temperature,
            }
            self.conversation_history.append(conversation_entry)
            return assistant_response, None
        except Exception as e:
            return None, f"Error: {str(e)}"

    def set_custom_instruction(self, instruction):
        self.custom_instruction = instruction

    def clear_conversation(self):
        self.conversation_history = []

    def export_conversation(self):
        if not self.conversation_history:
            return None, None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"local_conversation_{timestamp}.json"
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "custom_instruction": self.custom_instruction,
            "conversation": self.conversation_history,
        }
        return filename, json.dumps(export_data, indent=2)


user_input = st.chat_input("Ask your question.")


def main():
    st.title("Local AI Studio Chat")

    if "local_chat" not in st.session_state:
        st.session_state.local_chat = LocalStudioChat()

    chat = st.session_state.local_chat

    with st.sidebar:
        st.header("Configuration")
        st.caption("This free path uses Ollama running on your machine.")

        selected_model = st.selectbox("Choose Local Model", list(chat.models.keys()))
        model_id = chat.models[selected_model]

        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
        top_p = st.slider("Top-p", 0.1, 1.0, 1.0, 0.1)
        max_tokens = st.slider("Max Tokens", 128, 4096, 1024, 128)

        preset_instructions = {
            "Default": "You are a helpful AI assistant.",
            "Creative Writer": "You are a creative writing assistant.",
            "Business Assistant": "You are a professional business assistant.",
            "Language Tutor": "You are a language learning tutor.",
            "Technical Expert": "You are a technical expert.",
        }
        selected_preset = st.selectbox("Quick Presets", list(preset_instructions.keys()))
        if st.button("Apply Preset"):
            chat.set_custom_instruction(preset_instructions[selected_preset])
            st.rerun()

        if chat.conversation_history:
            if st.button("Export Conversation"):
                filename, content = chat.export_conversation()
                if content:
                    st.download_button("Download Chat", content, file_name=filename, mime="application/json")

        if st.button("Clear Chat"):
            chat.clear_conversation()
            st.rerun()

        st.divider()
        st.caption("Image generation was removed from this free local path. Use a separate local image stack if needed.")

    for entry in chat.conversation_history:
        with st.chat_message("user"):
            st.markdown(entry["user"])
        with st.chat_message("assistant"):
            st.markdown(entry["assistant"])

    if user_input and user_input.strip():
        with st.chat_message("user"):
            st.markdown(user_input.strip())
        with st.chat_message("assistant"):
            with st.spinner("Local model is thinking..."):
                response, error = chat.send_message(
                    user_input.strip(),
                    model=model_id,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                )
                if response:
                    st.markdown(response)
                else:
                    st.error(error)


if __name__ == "__main__":
    main()
