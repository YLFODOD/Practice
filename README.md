# Toolshop · Playwright (Python) + GitHub Actions

Practice target: https://practicesoftwaretesting.com (API: https://api.practicesoftwaretesting.com)

## Local setup (uv)

```bash
uv sync                                   # creates .venv from uv.lock (Python 3.13 via .python-version)
uv run playwright install                 # browsers (add --with-deps on Linux)
cp .env.example .env                      # test credentials for local runs
```

## Run

```bash
uv run pytest                             # all tests, headless chromium
uv run pytest --headed --slowmo 300       # watch it
uv run pytest -m smoke                    # by marker: smoke | api | e2e
uv run pytest --browser firefox -n auto   # other browser, parallel
uv run playwright codegen https://practicesoftwaretesting.com
uv run playwright show-trace test-results/<test>/trace.zip
```

## Adding a package

```bash
uv add --dev <package>                    # updates pyproject.toml AND uv.lock — commit both
```

CI runs `uv sync --locked`, which fails if `uv.lock` is out of date with `pyproject.toml`.

## GitHub setup

Repository → Settings → Secrets and variables → Actions → add
`TEST_USER_EMAIL` and `TEST_USER_PASSWORD`.

> Toolshop locks accounts after repeated failed logins, and the demo
> accounts are shared. Never test wrong passwords against a real demo account.
