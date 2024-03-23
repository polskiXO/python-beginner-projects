# NatLang2Latex

## Setup

Either use the devcontainer included, or have `poetry` installed. Navigate to the root of the project and run

```terminal
poetry install
```

Then obtain a Google API key, create a `.env` file and fill it in based on the example in `.env.example`. If you want to contribute, you can also run the following set of commands.

```terminal
poetry install --with dev
poetry run pre-commit install
```

## Tests

Run tests with

```terminal
pytest projects/NatLang2Latex
```
