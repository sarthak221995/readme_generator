# CrewAI README Generator

🚀 An AI-powered tool that generates comprehensive README files for GitHub repositories using CrewAI and Google Gemini.

## Features

- **AI-Powered Analysis**: Uses CrewAI agents to analyze GitHub repositories
- **Comprehensive Documentation**: Generates complete README files with all essential sections
- **Multiple LLM Support**: Works with Google Gemini, OpenAI GPT, and Anthropic Claude
- **CLI Interface**: Easy-to-use command-line interface
- **Customizable Output**: Configure badges, table of contents, and more
- **Rich Terminal UI**: Beautiful terminal interface with progress indicators

## Installation

```bash
pip install crewai-readme-generator
```

## Quick Start

1. Set your API key:
```bash
export GOOGLE_API_KEY=your_google_api_key
```

2. Generate a README:
```bash
readme-gen https://github.com/owner/repository
```

## Usage

### Basic Usage
```bash
# Generate README for a repository
readme-gen https://github.com/microsoft/vscode

# Use different model
readme-gen https://github.com/owner/repo --model gpt-4o-mini
```

### Advanced Options
```bash
# Disable badges and table of contents
readme-gen https://github.com/owner/repo --no-badges --no-toc

# Enable verbose output
readme-gen https://github.com/owner/repo --verbose

# Analyze repository without generating README
readme-gen analyze https://github.com/owner/repo
```

### Configuration
```bash
# Check current configuration
readme-gen config
```

## Programmatic Usage

```python
from readme_generator import ReadmeGenerator, Config

# Create configuration
config = Config(
    model_name="gemini/gemini-2.0-flash-exp",
    include_badges=True,
    include_toc=True
)

# Generate README
generator = ReadmeGenerator(config)
readme_content = generator.generate("https://github.com/owner/repo")
```

## Supported LLMs

- **Google Gemini** (Default): `gemini/gemini-2.0-flash-exp`
- **OpenAI GPT**: `gpt-4o-mini`, `gpt-4`
- **Anthropic Claude**: `claude-3-sonnet-20240229`
- **Local LLMs**: via Ollama

## Environment Variables

- `GOOGLE_API_KEY`: Google Gemini API key
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GITHUB_TOKEN`: GitHub token (optional, for higher rate limits)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.