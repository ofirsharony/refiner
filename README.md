
# Text refiner

Refines your text, while preserving your style.

# Example

![Alt text](./resources/llm_stories_generator.png?raw=true "single question template")

## Running modes

* Replace your text in place
* Open the text in full diff mode to observe changes
## Run Locally

Clone the project

```bash
  git clone https://github.com/ofirsharony/refiner.git
```

Go to the project directory, to the desired template, e.g

```bash
  cd refiner/src
```

Install dependencies, by either 'pip install -r requirements.txt' or directly via

```bash
  pip install openai langchain streamlit diff-match-patch
```

Make sure your OpenAI key is defined as environment var 
```bash
  export OPENAI_API_KEY=sk-XXXX
```

Run it!

```bash
  streamlit run app.py
```

## Contributing

Contributions are always welcome!

## License

You are free to do whatever you'd like, including copying, modifying and distributing, without any need for attribution.

