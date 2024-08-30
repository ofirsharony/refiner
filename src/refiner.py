import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from streamlit.components.v1 import html  # For rendering custom HTML
import difflib  # Importing difflib for text comparison

# Store your OpenAI key in env var OPENAI_API_KEY
# pip install openai langchain streamlit
# streamlit run refiner.py

PROMPT = '''Slightly improve the following text while preserving my writing style. Fix grammar mistakes, and keep my writing clean and make my intent clear. When I see the result, I want to quickly identify it as my own writing, with a few necessary fixes. Don't add pleasing text
---
Text: {} '''

openai_api_key = os.environ.get('OPENAI_API_KEY')
st.set_page_config(layout="centered", page_title="LLM stories generator")
st.markdown("## Refiner")
st.markdown("### Your Work Refiner")

def generate_response(input_text, model_name):
    chat = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)
    messages = [SystemMessage(content=input_text)]
    response = chat(messages)
    return response.content

def create_diff_html(before_text, after_text):
    """Generate styled HTML for comparing two texts side-by-side with differences highlighted."""
    # Split texts into words for better granularity
    before_words = before_text.split()
    after_words = after_text.split()

    # Initialize HTML containers for left and right text display
    left_html = ""
    right_html = ""

    # Generate diff using SequenceMatcher
    matcher = difflib.SequenceMatcher(None, before_words, after_words)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':  # Unchanged text
            left_html += ' '.join(before_words[i1:i2]) + ' '
            right_html += ' '.join(after_words[j1:j2]) + ' '
        elif tag == 'delete':  # Subtractions in red on the left
            left_html += f"<span style='color: red;'>{' '.join(before_words[i1:i2])}</span> "
        elif tag == 'insert':  # Additions in green on the right
            right_html += f"<span style='color: green;'>{' '.join(after_words[j1:j2])}</span> "
        elif tag == 'replace':  # Modifications in orange on light gray background on both sides
            left_html += f"<span style='color: orange; background-color: #f0e68c;'>{' '.join(before_words[i1:i2])}</span> "
            right_html += f"<span style='color: orange; background-color: #f0e68c;'>{' '.join(after_words[j1:j2])}</span> "

    # Combine HTML with side-by-side layout using CSS Grid
    combined_html = f"""
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4>Before</h4>
            {left_html}
        </div>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4>After</h4>
            {right_html}
        </div>
    </div>
    """
    return combined_html


with st.form('my_form'):
    open_ai_model = st.selectbox('Which OpenAI model should we use?', ('gpt-4o-mini', 'gpt-4o'))
    # Change to st.text_area for larger input size, allowing paragraphs
    text = st.text_area("Input Text", value="Consider this approach: ", height=150)
    prompt = st.text_area('Prompt:', value=PROMPT, height=220)
    submitted = st.form_submit_button('Generate')

    if submitted:
        with st.spinner('Generating LLM response...'):
            # Generate the response
            after_text = generate_response(prompt.format(text), open_ai_model)

            # Generate the styled diff HTML
            diff_html = create_diff_html(text, after_text)

            # Display the diff table in Streamlit using HTML
            st.markdown("### Before and After Comparison:")
            html(diff_html, height=500, scrolling=True)
