FROM python:3.10-slim-bullseye

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python setup.py sdist bdist_wheel
RUN pip install dist/hyperborea-*-py3-none-any.whl
RUN python -m pytest tests

CMD ["gunicorn", "app:app", "--workers", "2", "--threads", "2", "-b", "0.0.0.0:8000"]
