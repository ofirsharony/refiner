import streamlit as st
from streamlit.components.v1 import html  # Import the HTML function
from refiner import generate_llm_response, create_diff_html, PROMPT  # Import business logic functions

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

    query_params = st.experimental_get_query_params()
    auto_generate = query_params.get("auto_generate", ["false"])[0].lower() == "true"
    text = st.text_area("Input Text", value=query_params.get("text", ["sounds like a plan, take it directly with yosef on Sun so he can allocate time properly?"])[0], height=120)

    with st.expander("Prompt (Click to edit)", expanded=False):
        prompt = st.text_area('Edit Prompt:', value=PROMPT, height=120)

    submitted = st.form_submit_button('Generate')

    if submitted or auto_generate:
        with st.spinner('Generating LLM response...'):

            after_text = generate_llm_response(prompt.format(text), open_ai_model)

            # Generate the styled diff HTML
            diff_html = create_diff_html(text, after_text)

            # Display the diff table in Streamlit using HTML
            st.markdown("#### Before and After Comparison:")
            html(diff_html, height=500, scrolling=True)  # This line works now
