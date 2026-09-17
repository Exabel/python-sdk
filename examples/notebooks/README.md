# Notebook examples

Open [prediction_models.ipynb](prediction_models.ipynb) to list and inspect models,
read run history and outcomes, and optionally copy a model, update its description,
and start a run.

## Setup

Use a checkout containing the prediction model API additions. Install from the
checkout because these examples use methods that are not in the current PyPI release.
From the repository root, run:

```bash
uv sync
```

Set either EXABEL_ACCESS_TOKEN to a user access token or EXABEL_API_KEY to an API key.
Set only one credential. The following
reads it without echoing it or putting its value in shell history. Paste the token
after the first command and press Enter:

```bash
read -rs EXABEL_ACCESS_TOKEN
export EXABEL_ACCESS_TOKEN
uv run --with jupyterlab jupyter lab examples/notebooks/prediction_models.ipynb
```

For an API key, substitute EXABEL_API_KEY in the read and export commands. If the
credential is already in an untracked .env file at the repository root, launch with:

```bash
uv run --env-file .env --with jupyterlab jupyter lab examples/notebooks/prediction_models.ipynb
```

API keys use the customer's service account and can access models in folders shared
with that account. The optional write examples require permission to create models
and run them. Configuration writability describes supported settings, not permissions.

Run cells in order. Reads work with the default settings. Set RUN_WRITE_EXAMPLES
to True only to create a copy and start a run. Re-executing the creation cell creates
another model. Runs use compute and do not activate automatically.

The public API does not support deleting prediction models. Delete example copies
in the Exabel app when finished.

## Saved outputs

The notebook includes illustrative outputs so it can be read on GitHub. Running it
against Exabel replaces those examples with the credential's accessible data.

The nbstripout pre-commit hook strips outputs by default. This example opts in to
preserving outputs with `keep_output: true` in notebook metadata. Execution counts
and cell IDs are preserved; transient execution metadata is removed.

Install the hooks with `prek install`. Before committing a re-executed notebook,
review every output and replace private data with illustrative values. The hook
does not redact secrets. Keep credentials out of cells and saved outputs.
