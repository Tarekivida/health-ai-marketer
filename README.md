# health-ai-marketer

**An end-to-end health article generation and AI-driven product marketing pipeline.**

## Table of Contents

1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Project Structure](#project-structure)  
   - [Agents](#agents)  
   - [Utilities](#utilities)  
   - [Entry Point](#entry-point)  
7. [Configuration](#configuration)  
8. [Development](#development)  
9. [Contributing](#contributing)  
10. [License](#license)  
11. [Contact](#contact)

## Introduction

`health-ai-marketer` is a proof-of-concept application demonstrating an automated pipeline for:
- Generating informative health and wellness articles using a Large Language Model (LLM).
- Extracting product and solution mentions from generated content.
- Researching real products on Newpharma via SearxNG.
- Scraping product details (title, price, description, reviews) with Selenium.
- Rewriting articles to inject AI-curated product recommendations for marketing and SEO.

## Features

- **AI-driven content generation**: Utilizes a configurable LLM backend via the `autogen` framework.
- **Structured product extraction**: Identifies products and categories within article text.
- **Automated product research**: Queries SearxNG to find relevant Newpharma listings.
- **Web scraping**: Employs Selenium WebDriver for detailed product data retrieval.
- **Content rewriting**: Integrates real product recommendations into articles for enhanced marketing impact.

## Prerequisites

- Python 3.8 or newer  
- [pipenv](https://pipenv.pypa.io/) or `virtualenv` for environment management  
- Google Chrome or Chromium installed  
- ChromeDriver matching your browser version  
- A running instance of [SearxNG](https://github.com/searxng/searxng) on `localhost:8080`  
- Access to an LLM backend configured in `utils/llm_config.py`
- Docker (Engine 20.10 or newer)
- Docker Compose (v2 or newer)
- Python Autogen framework and extensions (install via pip: autogen, autogen-agentchat, autogen-core, autogen-ext, autogenstudio)
- FastAPI
- Uvicorn (ASGI server)
- Jinja2 (templating engine)
 - python-multipart (required by FastAPI for form handling)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/health-ai-marketer.git
   cd health-ai-marketer
   ```
2. Create and activate a virtual environment:
   ```bash
   pip install pipenv
   pipenv install
   pipenv shell
   ```
   *Or with virtualenv:*
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Ensure ChromeDriver is in your PATH or set the `CHROMEDRIVER_PATH` environment variable.

4. Install Autogen packages:
   ```bash
   pip install autogen autogen-agentchat autogen-core autogen-ext autogenstudio
   ```

5. Install python-multipart:
   ```bash
   pip install python-multipart
   ```

6. (Optional) Configure environment variables as needed.

## Usage

Run the main pipeline script:
```bash
python3 main.py
```
Follow prompts to enter a health topic. The pipeline then:
1. Generates an article.  
2. Extracts products and solutions.  
3. Researches matching products on Newpharma.  
4. Scrapes product details.  
5. Rewrites the article with product recommendations.

Output markdown files are saved under `outputs/YYYYMMDD_HHMMSS/`.

### Web Interface

Launch the web UI:
```bash
uvicorn web.app:app --reload
```
Open your browser at `http://localhost:8000/` to access the interface for generating and viewing articles.

## Project Structure

```
health-ai-marketer/
├── agents/
│   ├── extraction.py
│   ├── product_research_agent.py
│   ├── product_scraper_agent.py
│   ├── marketing_content_specialist.py
│   ├── pharmacist_expert.py
│   └── pharmacist_reviewer.py
├── utils/
│   └── llm_config.py
├── main.py
├── requirements.txt
└── README.md
```

### Agents

- **pharmacist_expert**: Generates health articles via LLM.  
- **extraction**: Extracts product/solution mentions from text.  
- **product_research_agent**: Searches Newpharma for relevant product URLs.  
- **product_scraper_agent**: Scrapes detailed product info with Selenium.  
- **marketing_content_specialist**: Rewrites articles to integrate product recommendations.  
- **pharmacist_reviewer**: Optionally refines or reviews content via LLM.

### Utilities

- **utils/llm_config.py**: Centralized LLM endpoint/configuration.

### Entry Point

- **main.py**: Orchestrates the full end-to-end pipeline.

## Configuration

Update `utils/llm_config.py` with your LLM endpoint or API key.  
Configure environment variables as needed:
- `SEARXNG_URL` (default: `http://localhost:8080`)  
- `CHROMEDRIVER_PATH` if ChromeDriver isn’t in your PATH.

## Development

- Extend agents in the `agents/` directory.  
- Add tests under a new `tests/` directory.  
- Maintain code style: use `flake8` or `black`.

## Contributing

1. Fork the repo.  
2. Create a branch: `git checkout -b feature/YourFeature`.  
3. Commit: `git commit -m 'Add feature'`.  
4. Push: `git push origin feature/YourFeature`.  
5. Open a Pull Request describing your changes.

## License

Licensed under the MIT License. See `LICENSE` for details.

## Contact

Maintainer: Tarek  
GitHub: [Tarekivida](https://github.com/Tarekivida)