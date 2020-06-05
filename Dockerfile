FROM python:3-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD build/ /usr/local/bin/
 
COPY entrypoint.sh /usr/local/bin

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
