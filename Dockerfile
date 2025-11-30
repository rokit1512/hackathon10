FROM python:3.9-slim
ENV VIRTUAL_ENV=/backend/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /
COPY . .
WORKDIR backend
RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
