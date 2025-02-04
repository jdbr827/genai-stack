FROM langchain/langchain

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY call_parser.py .
COPY call_loader.py .
COPY loader.py .
COPY loaderUI.py .
COPY utils.py .
COPY chains.py .
COPY images ./images

EXPOSE 8502

HEALTHCHECK CMD curl --fail http://localhost:8502/health

ENV FLASK_APP=call_loader.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8502"]