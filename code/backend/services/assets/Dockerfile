# services/assets/Dockerfile

############################################
# 1) Builder: install all Python deps
############################################
FROM python:3.11-slim AS builder
WORKDIR /app

# 1a) System build tools (for any packages with C extensions)

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*

# 1) Install all PyPI packages
COPY ./services/assets/docker-requirements.txt ./requirements.txt

# 2) Copy in your libraries
COPY ./libraries/ ./libraries/

# 3) Install the local libs by hand, in dependency order
RUN pip install --no-cache-dir -e libraries/myExceptions[docker] \
                             -e libraries/myAws[docker] \
                             -e libraries/myHttp[docker] \
                             -e libraries/myEncryption[docker] \
                             -e libraries/myOrm[docker] \
                             -e libraries/myDependencies[docker]


RUN pip install --no-cache-dir -r requirements.txt

############################################
# 2) Final: lean runtime image
############################################
FROM python:3.11-slim
WORKDIR /app

# bring in installed packages & console scripts
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/                   /usr/local/bin/

# copy your service code
COPY ./services/assets/ .

# copy the libraries folder (so editable installs will resolve)
COPY --from=builder /app/libraries/ ./libraries/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

CMD ["python3", "main.py"]