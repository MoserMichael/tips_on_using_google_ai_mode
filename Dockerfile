FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

RUN pip install --no-cache-dir markdownify
RUN pip install --no-cache-dir mistune

COPY conv.py .

CMD ["python", "conv.py"]

ENTRYPOINT ["python", "conv.py"]
