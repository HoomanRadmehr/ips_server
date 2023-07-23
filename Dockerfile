FROM nexus:443/netpardaz/ubuntu-python3:20.04

USER root
COPY . ./app
WORKDIR /app
RUN apt-get update; apt install -y libpq-dev; pip install --index-url http://10.27.95.5:8081/repository/pypi-all/simple --trusted-host 10.27.95.5 --no-cache-dir -r requirements.txt
EXPOSE 8000
RUN python3 -m pip install -U pip
