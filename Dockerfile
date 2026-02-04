FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv pip install --system -r pyproject.toml

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
