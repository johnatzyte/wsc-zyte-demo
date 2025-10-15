# Scrapy Project

This project uses [Scrapy](https://scrapy.org/) for web scraping. It leverages the `web-poet` library to create page object classes, which define how to extract data from webpages in a structured and reusable way. The `scrapy-poet` package provides the integration between `web-poet` and Scrapy.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

1.  Create a virtual environment and install the required packages:

    ```bash
    uv sync
    ```

2.  Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

To Run the Spider

```bash
scrapy crawl products
```

## Testing

Tests for page object classes use test fixtures stored in the `fixtures/` directory, following the `web-poet` convention. These fixtures allow for testing extraction logic without making live network requests.