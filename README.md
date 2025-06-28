# readme_generator

> **AI-powered README creation for your repositories.**  
> Generate detailed, professional README.md files automatically using state-of-the-art Large Language Models. Use via a web UI or command-line tool.

![Build Status](https://img.shields.io/github/workflow/status/sarthak221995/readme_generator/CI)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/github/license/sarthak221995/readme_generator)
![Docker Image](https://img.shields.io/badge/docker-ready-blue)

---

**Table of Contents**

- [Overview](#overview)
- [Features](#features)
- [Screenshots & Demos](#screenshots--demos)
- [Installation](#installation)
  - [System Requirements](#system-requirements)
  - [Standalone Installation](#standalone-installation)
  - [Docker Deployment](#docker-deployment)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Web Application](#web-application)
  - [Command-Line Interface](#command-line-interface)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)
- [Credits & Acknowledgments](#credits--acknowledgments)
- [Contact](#contact)
- [Links](#links)

---

## Overview

**`readme_generator`** is an automated tool for generating comprehensive, high-quality README.md files for GitHub repositories by leveraging advanced AI models (OpenAI or Google Generative AI) through CrewAI orchestration.  
It is the perfect solution for individuals or teams seeking to quickly bootstrap, improve, or standardize repository documentation with minimal manual effort.

- Analyze any public repository by its URL and receive a detailed README draft.
- Choose from popular LLM providers (OpenAI/GPT-4, Gemini, etc.).
- Use as a web service or a versatile command-line tool.

---

## Features

- **Automated README.md Authoring:**  
  Generate clean, project-tailored README files using LLMs in seconds.

- **Web and CLI Interfaces:**  
  Submit a repo URL via browser or terminal, and get documentation back instantly.

- **Multiple AI Providers:**  
  Seamlessly switch between OpenAI and Google Gemini models.

- **Background Processing:**  
  The web UI provides live progress updates; download your new README when ready.

- **Docker-ready:**  
  Effortless deployment for instant local or production use.

- **Custom Templates:**  
  Easily extensible for future customization of README style.

- **Secure Configuration:**  
  Safeguard all API keys and model configs via a `.env` file.

---

## Screenshots & Demos

<!-- Uncomment and replace with actual images when available
![Web UI screenshot](docs/web-ui.png)
-->

- **Web UI:**
  - Paste a repository URL
  - Click "Generate"
  - Wait for the progress bar and download the final README

- **CLI:**
  - One-command README generation straight to your console or a file

_See [Demo Video](https://readme-generator-916940205758.europe-west1.run.app/)

---

## Installation

### System Requirements

- Python 3.8 or newer
- pip (Python package installer)
- **At least one** valid LLM API key (OpenAI or Google Generative AI)
- (Optional, but recommended) Docker

---

### Standalone Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/sarthak221995/readme_generator.git
   cd readme_generator
   ```

2. **Set up a virtual environment and install dependencies:**

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Configure your environment:**

   Create a `.env` file in the project root. At minimum, include your LLM API key:

   ```env
   # For Google Gemini
   GOOGLE_API_KEY=your_google_api_key_here
   model_name=gemini/gemini-2.0-flash

   # Or, for OpenAI
   # OPENAI_API_KEY=your_openai_api_key_here
   # model_name=gpt-4-1106-preview
   ```
   (See [Configuration](#configuration) for full details.)

4. **Run via CLI or start the web server:**

   ```sh
   # Command-Line
   python -m readme_generator.cli --repo-url https://github.com/example/repo

   # OR start the Web Application
   python app.py
   ```

---

### Docker Deployment

Build and run as a containerized service (no local Python setup required):

#### Command-Line Tool (CLI):

```sh
docker build -t readme-gen .
docker run --env-file .env readme-gen python -m readme_generator.cli --repo-url https://github.com/example/repo
```

#### Web Application:

```sh
docker build -f Dockerfile.web -t readme-gen-web .
docker run -p 5000:5000 --env-file .env readme-gen-web
```

_Note: Both images support `.env` configuration for secure secrets handling._

---

## Configuration

All AI credentials, model selection, and environment parameters are managed via environment variables (in a `.env` file or your OS environment):

| Variable           | Purpose                                         | Example Value                        |
|--------------------|-------------------------------------------------|--------------------------------------|
| `GOOGLE_API_KEY`   | API key for Google Generative AI (Gemini)       | `AIzaSyD...`                         |
| `OPENAI_API_KEY`   | API key for OpenAI models                       | `sk-...`                             |
| `model_name`       | Identifier for target LLM (provider-dependent)  | `gpt-4-1106-preview` or `gemini/gemini-2.0-flash` |

**To switch models/providers:**  
- Set only one provider's key (`GOOGLE_API_KEY` *or* `OPENAI_API_KEY`) and update `model_name` accordingly.

---

## Usage

### Web Application

1. **Start the server:**
   ```sh
   python app.py
   ```
   (or via Docker, as above)

2. **Navigate to:**  
   [http://localhost:5000](http://localhost:5000)

3. **Submit Repository URL:**  
   - Enter a public GitHub repository URL.
   - Click “Generate README”.

4. **Processing:**  
   - Status/progress updates are displayed during AI analysis.

5. **Result:**  
   - Download the generated README file on completion.

---

### Command-Line Interface

#### Quick Usage

```sh
readme-gen --repo-url "https://github.com/user/project"
# or, equivalently
crewai-readme --repo-url "https://github.com/user/project"
```

#### Common Options

| Option               | Description                                         | Example                                |
|----------------------|-----------------------------------------------------|----------------------------------------|
| `--repo-url`         | **(Required)** Target repository GitHub HTTPS URL   | `https://github.com/user/project`      |
| `--output`           | Path to save README file (optional; defaults to stdout) | `--output ./README.generated.md`       |
| `--model`            | Override LLM model (optional)                       | `--model gpt-4-1106-preview`           |
| `--provider`         | Explicit provider selection (optional)              | `--provider openai` or `google`        |

#### Example

```sh
readme-gen --repo-url "https://github.com/pallets/flask" --output flask_README.md
```

#### Output

```
[INFO] Analyzing repository...
[INFO] Selecting LLM: gemini/gemini-2.0-flash (Google AI)
[INFO] Drafting README sections...
[✓] README written to flask_README.md
```

---

#### Configuration Options

- To use different LLM models, update your `.env` as described.
- If no `--output` is specified, the README content prints to the console.

---

## API Documentation

`readme_generator` offers both CLI and Web UI. For integration at a deeper level, the main packages/classes include:

### Main Modules

- **`core.py`**
  - `generate_readme(repo_url: str, model: str, provider: str) -> str`
    - **Parameters:**
      - `repo_url`: URL of the target public GitHub repository.
      - `model`: (optional) LLM model name (e.g., "gpt-4-1106-preview").
      - `provider`: (optional) LLM provider ("openai" or "google").
    - **Returns:**  
      - String containing the full generated README markdown.

- **`cli.py`**
  - CLI entrypoint (as `readme-gen` or `crewai-readme`)
  - Uses [Click](https://click.palletsprojects.com/) for arguments and provides progress/error output.

- **Flask endpoints (`app.py`):**
  - `POST /generate` — Start README creation
  - `GET /progress/<task_id>` — Poll background job progress
  - `GET /download/<task_id>` — Download completed README

### Usage Example (Python):

```python
from readme_generator.core import generate_readme

markdown = generate_readme(
    repo_url="https://github.com/user/project",
    model="gpt-4-1106-preview",
    provider="openai"
)
print(markdown)
```

---

## Development

### Setup

1. Clone and enter the repository directory.
2. Install dependencies:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Optionally, install in editable mode for CLI:
   ```sh
   pip install -e .
   ```
4. Prepare your `.env` with the relevant API keys.

### Running Tests

- Test suite is managed via `pytest` (ensure it is installed) or `unittest`.
- To run all tests:
  ```sh
  pytest tests/
  ```
  or
  ```sh
  python -m unittest discover tests
  ```

### Build (Package Distribution)

```sh
python setup.py sdist bdist_wheel
```

#### Development Dependencies

Core requirements are listed in `requirements.txt`.  
For code formatting and linting, consider installing:

- [`black`](https://black.readthedocs.io/en/stable/) — automatic Python code formatter
- [`flake8`](https://flake8.pycqa.org/en/latest/) — linting
- [`pytest`](https://docs.pytest.org/en/7.0.x/) — for running tests

---

## Contributing

Contributions are welcome! To get started:

1. **Fork** this repository.
2. **Clone** your fork and set up the environment as above.
3. **Create a new branch** for your feature or bugfix:
   ```sh
   git checkout -b feature/your-feature
   ```
4. **Follow coding standards:**
   - Use [PEP8](https://pep8.org/) conventions.
   - Format code with `black` before submitting.
5. **Test** your changes before pushing.
6. **Submit a Pull Request:**  
   - Include a clear, concise description of your changes.
   - Reference relevant issues, if applicable.

### Reporting Issues

- Use the [GitHub Issues](https://github.com/sarthak221995/readme_generator/issues) page to report bugs, suggest features, or request enhancements.
- Please include reproduction steps, expected behavior, and your environment details.

---

## License

Distributed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software under the terms of the MIT license.

---

## Credits & Acknowledgments

- [Sarthak Jain (@sarthak221995)](https://github.com/sarthak221995) — Creator & Maintainer
- Powered by [CrewAI](https://github.com/joaomdmoura/crewai), [OpenAI](https://openai.com/), and [Google Generative AI](https://ai.google/discover/gemini/)
- Thanks to the contributors and the open source ecosystem, including Flask and Click

---

## Contact

- GitHub: [@sarthak221995](https://github.com/sarthak221995)
- Email: sarthak221995@gmail.com
- Project Discussions: [GitHub Discussions](https://github.com/sarthak221995/readme_generator/discussions)

---

## Links

- **Project Repo:** [https://github.com/sarthak221995/readme_generator](https://github.com/sarthak221995/readme_generator)
- **CrewAI:** [https://github.com/joaomdmoura/crewai](https://github.com/joaomdmoura/crewai)
- **Documentation:** (Coming soon)
- **Report Issues:** [Issue Tracker](https://github.com/sarthak221995/readme_generator/issues)

---

> **_Save time. Increase quality. Let AI power your documentation!_**
```
