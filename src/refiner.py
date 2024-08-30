import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from streamlit.components.v1 import html  # For rendering custom HTML
from diff_match_patch import diff_match_patch

# Store your OpenAI key in env var OPENAI_API_KEY
# pip install openai langchain streamlit
# streamlit run refiner.py

PROMPT = '''Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements.
Text: {} '''

openai_api_key = os.environ.get('OPENAI_API_KEY')

st.set_page_config(layout="wide", page_title="Text Refiner", initial_sidebar_state="expanded")

# CSS to set a custom width for the main content and reduce padding at the top
st.markdown(
    """
    <style>
    .main {
        max-width: 1200px;  /* Adjust this value for desired width */
        margin: auto;  /* Centers the content */
    }
    .css-18e3th9 {  /* Adjust top padding to bring content closer to the top */
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("## Text Refiner")

def generate_response(input_text, model_name):
    chat = ChatOpenAI(temperature=0.3, openai_api_key=openai_api_key, model_name=model_name)
    messages = [SystemMessage(content=input_text)]
    response = chat(messages)
    return response.content.replace("You are trained on data up to October 2023.", "")

def create_diff_html(before_text, after_text):
    """Generate styled HTML for comparing two texts side-by-side with differences highlighted using diff-match-patch."""

    # Initialize the diff_match_patch object
    dmp = diff_match_patch()

    # Compute the diff
    diffs = dmp.diff_main(before_text, after_text)
    dmp.diff_cleanupSemantic(diffs)  # Clean up the diff to be more human-readable

    # Initialize HTML containers for left (before) and right (after) text display
    left_html = ""
    right_html = ""

    # Build separate HTML for "before" and "after" using the diff data
    for op, data in diffs:
        if op == -1:  # Deletion in "before" (red)
            left_html += f"<span style='color: red;'>{data}</span>"
            right_html += ""  # No addition on the right side for deletions
        elif op == 1:  # Addition in "after" (green)
            left_html += ""  # No deletion on the left side for additions
            right_html += f"<span style='color: green;'>{data}</span>"
        elif op == 0:  # No change (unchanged text)
            left_html += f"{data}"
            right_html += f"{data}"

    # Combine HTML with side-by-side layout using CSS Grid and add grey background for headers
    combined_html = f"""
    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px;'>Before</h4>
            <div>{left_html}</div>
        </div>
        <div style='font-family: Arial, sans-serif; padding: 10px; border: 1px solid #ddd;'>
            <h4 style='background-color: #f0f0f0; padding: 10px;'>After</h4>
            <div>{right_html}</div>
        </div>
    </div>
    """
    return combined_html

with st.form('my_form'):
    open_ai_model = st.selectbox('Which OpenAI model should we use?', ('gpt-4o-mini', 'gpt-4o'))
    # Change to st.text_area for larger input size, allowing paragraphs
    text = st.text_area("Input Text", value="sounds like a plan, take it directly with yosef on Sun so he can allocate time properly?",
                        height=120)

    with st.expander("Prompt (Click to edit)", expanded=False):
        prompt = st.text_area('Edit Prompt:', value=PROMPT, height=120)
    submitted = st.form_submit_button('Generate')

    if submitted:
        with st.spinner('Generating LLM response...'):
            # Generate the response
            after_text = generate_response(prompt.format(text), open_ai_model)

            # Generate the styled diff HTML
            diff_html = create_diff_html(text, after_text)

            # Display the diff table in Streamlit using HTML
            st.markdown("#### Before and After Comparison:")
            html(diff_html, height=500, scrolling=True)
