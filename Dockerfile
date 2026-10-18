FROM python:3.11.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN pip install --no-cache-dir uv==0.11.28 && uv sync --locked --no-editable
COPY tests ./tests
RUN groupadd --gid 10001 runner && useradd --uid 10001 --gid 10001 --no-create-home runner
USER 10001:10001
CMD ["/app/.venv/bin/python", "-m", "pytest", "-p", "no:cacheprovider"]
