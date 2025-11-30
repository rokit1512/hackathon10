FROM python:3.9-slim
WORKDIR /
COPY . .
WORKDIR backend
RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
