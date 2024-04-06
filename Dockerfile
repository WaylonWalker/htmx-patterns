FROM python:3.11

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
COPY htmx_patterns/__about__.py ./htmx_patterns/__about__.py
COPY htmx_patterns/__init__.py ./htmx_patterns/__init__.py
COPY README.md .

RUN uv pip install --system .
COPY . .

EXPOSE 5000

RUN uv pip install --system --no-deps .
ENV TZ=America/Chicago
ENV ENV=production
# CMD ['htmx-patterns', 'api', 'run']
CMD htmx-patterns api run

