import streamlit as st
from streamlit.components.v1 import html  # Import the HTML function
from refiner import generate_llm_response, create_diff_html  # Import business logic functions

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
    open_ai_model = st.selectbox('Which OpenAI model should we use?', ('gpt-4o-mini', 'gpt-4o'))
    text = st.text_area("Input Text", value="sounds like a plan, take it directly with yosef on Sun so he can allocate time properly?", height=120)

    with st.expander("Prompt (Click to edit)", expanded=False):
        prompt = st.text_area('Edit Prompt:', value='''Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements. Text: {} ''', height=120)

    submitted = st.form_submit_button('Generate')

    if submitted:
        with st.spinner('Generating LLM response...'):

            after_text = generate_llm_response(prompt.format(text), open_ai_model)

            # Generate the styled diff HTML
            diff_html = create_diff_html(text, after_text)

            # Display the diff table in Streamlit using HTML
            st.markdown("#### Before and After Comparison:")
            html(diff_html, height=500, scrolling=True)  # This line works now
