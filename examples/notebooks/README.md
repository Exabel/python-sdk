# Notebook examples

[prediction_models.ipynb](prediction_models.ipynb) lists and inspects prediction
models, reads run history, and optionally copies a model and starts a run.

## Run it

Install from the checkout, since the examples use methods that are not in the
current PyPI release:

```bash
uv sync
```

Set a credential, either EXABEL_ACCESS_TOKEN for a user access token or
EXABEL_API_KEY for an API key. Paste it when the shell waits for input:

```bash
read -rs EXABEL_ACCESS_TOKEN && export EXABEL_ACCESS_TOKEN
```

Launch from the same shell:

```bash
uv run --with jupyterlab jupyter lab examples/notebooks/prediction_models.ipynb
```

Run the cells in order. Reads work with the default settings; set
RUN_WRITE_EXAMPLES to True to also create a model copy and start a run. The
public API cannot delete models, so remove copies in the Exabel app.

Outputs are committed so the notebook can be read on GitHub. Review them before
committing a re-executed notebook, as the nbstripout hook does not redact.
