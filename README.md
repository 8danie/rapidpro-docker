# 🐳 RapidPro Docker

[![tag](https://img.shields.io/github/tag/nyaruka/rapidpro-docker.svg)](https://github.com/nyaruka/rapidpro-docker/releases)
[![Build Status](https://github.com/nyaruka/rapidpro-docker/workflows/CI/badge.svg)](https://github.com/nyaruka/rapidpro-docker/actions?query=workflow%3ACI)

Docker compose for stable release versions of RapidPro.

Includes:
 - RapidPro webapp and celery worker ([License](https://github.com/nyaruka/rapidpro/blob/main/LICENSE))
 - Mailroom ([License](https://github.com/nyaruka/mailroom/blob/main/LICENSE))
 - Courier ([License](https://github.com/nyaruka/courier/blob/main/LICENSE))
 - Indexer ([License](https://github.com/nyaruka/rp-indexer/blob/main/LICENSE))
 - nginx
 - PostgreSQL (postgis)
 - Elasticsearch
 - Valkey
 - DynamoDB local
 - Minio (S3 emulator)

These example containers are for development purposes only and are *not intended for production deployments*.

## Usage

```
docker compose up -d
```

The webapp will then be accessible at [http://localhost](http://localhost) and you will be able to create 
a test workspace at [http://localhost/org/signup](http://localhost/org/signup).
