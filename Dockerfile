FROM node:22-alpine
WORKDIR /
COPY . .
WORKDIR backend
RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
