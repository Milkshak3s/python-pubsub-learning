# python-pubsub-learning
Practicing using google pubsub with python, and simulating that usage in circleci.  
Specifically interested in adding a message delay for intentionally delayed processing.

## Usage
```
echo "[gcp_creds]" > creds.json"
docker build . --tag psl:latest
docker run --env PUB_SUB_PROJECT= --env PUB_SUB_TOPIC= --env PUB_SUB_SUBSCRIPTION= psl:latest
```
