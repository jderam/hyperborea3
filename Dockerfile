FROM python:3.10-slim-bullseye

WORKDIR /app
COPY . .

RUN pip install -U pip
RUN pip install -r requirements_dev.txt
RUN python -m build
RUN pip install dist/hyperborea3-*-py3-none-any.whl

CMD ["uvicorn", "main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000"]
