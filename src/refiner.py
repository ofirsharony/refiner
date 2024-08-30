import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage
)

# instructions
# Store your OpenAI key in env var OPENAI_API_KEY
# pip install openai langchain streamlit
# streamlit run single-question-llm.py

PROMPT = '''Slightly improve the following text while preserving my writing style. Fix grammar mistakes, and keep my writing clean and make my intent clear. When I see the result, I want to quickly identify it as my own writing, with a few necessary fixes. Don't add pleasing text
---
Text: {} '''

openai_api_key = os.environ.get('OPENAI_API_KEY')
st.set_page_config(layout="centered", page_title="LLM stories generator")
st.markdown("## Refiner")
st.markdown("### your work refiner")

def generate_response(input_text, model_name):
    chat = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)
    messages = [
        SystemMessage(content=input_text),
        # HumanMessage(content="Hi AI, how are you today?"),
        # AIMessage(content="I'm great thank you. How can I help you?"),
        # HumanMessage(content="I'd like to understand string theory.")
    ]

    return chat(messages)


with st.form('my_form'):
    open_ai_model = st.selectbox('Which OpenAI model should we use?', ('gpt-4o-mini', 'gpt-4o'))
    text = st.text_input("text", value="Consider this approach: ")
    prompt = st.text_area('Prompt:', value=PROMPT, height=220)
    submitted = st.form_submit_button('Generate')

    if submitted:
        with st.spinner('Generating LLM response...'):
            narrative = generate_response(prompt.format(text), open_ai_model)
            st.info(narrative.content)
