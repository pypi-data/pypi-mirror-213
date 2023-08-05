# The End is Never

A package to make an LLM talk with itself for eternity.

```python
from thendisnever.theend import isnever
isnever(
  model_name='Fredithefish/ScarletPajama-3B-HF', # Default LLM
  prompt='THE END IS NEVER THE END IS NEVER ', # Default prompt
  max_memory_ratio=0.25 # Default % of latest tokens to remember
)
```

## Notes

- For the default LLM (which you can change as shown above), you'll need at least:
  - ~ 6GB of free disk space
  - ~ 15GB of RAM
- When running `isnever()` for the first time, it will download the model and tokenizer from HuggingFace. This will take a while, but it only needs to be done once.
- If you want to use the CPU (not recommended because it's slow, but it works), make sure you have [PyTorch for CPU](https://pytorch.org/get-started/locally/) installed.

## Contributing

1. Install [poetry](https://python-poetry.org/docs/#installation) if necessary.
1. Create and setup the poetry environment:

    ```bash
    git clone https://github.com/andrewhinh/thendisnever.git
    cd thendisnever
    poetry shell
    poetry install
    ```

1. Make your changes, remembering to update in `pyproject.toml` the `version` in the `tool.poetry` section and the `tool.poetry.dependencies` section as necessary.

1. Build the package:

    ```bash
    poetry build
    ```

1. Add `TestPyPI` as a source:

    ```bash
    poetry config repositories.testpypi https://test.pypi.org/legacy/
    ```

1. Publish the package to `TestPyPI`:

    ```bash
    poetry publish -r testpypi
    ```

1. Test the package in a fresh environment:

    ```bash
    pip install --index-url https://test.pypi.org/simple/ --no-deps --upgrade thendisnever
    ```

1. Once confirmed to work, make a PR from a feature branch to main on GitHub.
1. Once PR is merged, [email me](ajhinh@gmail.com) to be added as a collaborator on PyPI.
1. Once added as a collaborator, publish the package to `PyPI`:
  
      ```bash
      poetry publish
      ```
