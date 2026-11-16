
# Text refiner

Refines your text, while preserving your style.

Select text in any app, and refine it in place or review suggested changes with a click of a button.

Combines LLM with Automator - select text you've written in any app and make grammar adjustments in place, or open full diff app to review changes.
The app supports both interactive use (via Streamlit UI) and API requests (via FastAPI), and combines them with Automator.

## Features

- **Text Refinement**: Uses a language model (default: gpt-5.4-mini) to improve input text while preserving the user's writing style.
- **Diff Visualization**: Shows side-by-side comparison between original and refined text with changes highlighted.
- **API Mode**: Supports `curl` requests to the FastAPI endpoint for automated text refinement.
- **Shortcut from any app**: Run from any text input app (Slack, Gmail, Sublime, etc.) to edit in place or review changes

## Running modes

* Replace your text in place
* Open the text in full diff mode to observe changes

## Installation

1. **Clone the Repository**:

```bash
  git clone https://github.com/ofirsharony/refiner.git
  cd refiner/src
```

2. **Set Up a Virtual Environment** (optional):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `.env\Scriptsctivate`
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

The app calls the OpenAI API. Export your key:
```bash
  export OPENAI_API_KEY=sk-XXXX
```
To use another OpenAI-compatible provider (Ollama, Groq, Gemini, a company gateway), change `base_url` and `api_key_env` in `config.json`.

Behind a TLS-inspecting proxy, set `SSL_CERT_FILE` to the proxy's CA bundle.

## Configuration

**Update Configuration**:

The prompt for text refinement is stored in `config.json`. You can modify this file to change the prompt or other settings.

**Example `config.json`**:
   ```json
   {
     "prompt" : "Refine the following text without altering my writing style. Correct grammar mistakes and keep the writing concise and clear. I should immediately recognize it as my own work, but with essential improvements. Text: {}",
     "base_url": "https://api.openai.com/v1",
     "api_key_env": "OPENAI_API_KEY",
     "model": "gpt-5.4-mini",
     "models": ["gpt-5.4-mini", "gpt-5.4-nano", "gpt-4.1-mini"]
   }
   ```


## Running the Application

### 1. Start the Streamlit App for Interactive Use:

Run the following command to start the Streamlit UI:

```bash
streamlit run app.py --server.port 8504
```

Port 8504 matches `Automations/review_diff.sh`.

This will open the app in your default web browser where you can input text and see the refinements.

### 2. Start the FastAPI Server for API Use:

Run the FastAPI server using `uvicorn`:

```bash
uvicorn api:app --host 0.0.0.0 --port 8005
```

This will start the API server on `http://localhost:8005`. Use the `/generate_get` endpoint to refine text via API.


### Example `curl` Request:

```bash
curl -s "http://localhost:8005/generate_get?text=Your_custom_input_text&model=gpt-5.4-nano"
```

### Tests and model benchmark

```bash
pip install -r requirements-dev.txt
python -m pytest            # unit tests, no network calls
python benchmark.py         # times every model in config.json "models" on real calls
python benchmark.py gpt-5.4-nano gpt-4.1-mini
```

### 3. Set shortcuts to run by selecting input text from any app

In order to create Automator actions that activates both API mode and APP mode via shortcuts, see [Automations](https://github.com/ofirsharony/refiner/tree/main/src/Automations) folder

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.