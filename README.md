# AI-Agent

A command-line AI coding agent powered by Gemini 2.5 Flash. Give it a task in plain English and it will explore the codebase, read and write files, and run Python scripts to complete it — asking the model in a loop until it produces a final answer.

## How it works

1. Your prompt is sent to Gemini along with a set of tool definitions
2. The model decides which tools to call (list files, read files, write files, run scripts)
3. Tool results are fed back into the conversation and the model is called again
4. This repeats for up to 20 turns until the model gives a final text answer

All tool calls are sandboxed to the `./calculator` directory.

## Setup

```bash
# Install dependencies
uv sync

# Add your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env
```

## Usage

```bash
python main.py "your task here"
python main.py --verbose "your task here"
```

**Example:**
```bash
python main.py "fix the bug in calculator.py"
```

## Project structure

```
main.py              # entry point — agentic loop and model calls
prompts.py           # system prompt given to the model
config.py            # shared constants (e.g. MAX_CHARS for file reads)
functions/
  call_function.py   # dispatches model tool calls to the right function
  validate_path.py   # path validation and sandbox enforcement
  get_files_info.py  # tool: list files in a directory
  get_file_content.py # tool: read a file's contents
  run_python_file.py # tool: execute a Python script
  write_file.py      # tool: write or overwrite a file
calculator/          # sandboxed working directory the agent operates on
```
