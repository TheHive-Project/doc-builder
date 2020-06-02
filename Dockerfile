FROM python:3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./build /
 
COPY entrypoint.sh /usr/local/bin/

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
