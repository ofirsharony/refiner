import streamlit as st
import time  # Add time import for measuring execution time
from streamlit.components.v1 import html  # Import the HTML function
from refiner import refine, PROMPT  # Import business logic functions
from diff_formatter import create_html_diff

def set_page_config():
    st.set_page_config(layout="wide", page_title="Text Refiner", initial_sidebar_state="expanded")

    st.markdown(
        """
        <style>
        .main {
            max-width: 1200px;
            margin: auto;
        }
        .css-18e3th9 {
            padding-top: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_page_config()

st.markdown("## Text Refiner")

with st.form('my_form'):
    model = st.selectbox('Which OpenAI model should we use?', ('openai/gpt-4.1-nano','openai/gpt-5-nano', 'openai/gpt-4o-mini', 'openai/gpt-4o'))
    auto_generate = st.query_params.get("auto_generate", "false").lower() == "true"
    text = st.text_area("Input Text", value=st.query_params.get("text", "sounds like a plan, take it directly with john on Mon so he can allocate time properly?"), height=120)

    with st.expander("Prompt (Click to edit)", expanded=False):
        prompt = st.text_area('Edit Prompt:', value=PROMPT, height=120)

    submitted = st.form_submit_button('Generate')

    if submitted or auto_generate:
        with st.spinner('Refining your writing...'):
            # Start timing
            start_time = time.time()
            
            after_text = refine(prompt.format(text), model)
            
            # End timing and calculate duration
            end_time = time.time()
            execution_time = end_time - start_time

        # Display execution time
        st.success(f"✅ Text refined successfully with model {model} in {execution_time:.2f} seconds")

        # Render a styled HTML diff
        st.markdown("#### Before and After Comparison:")
        html(create_html_diff(text, after_text), height=500, scrolling=True)
