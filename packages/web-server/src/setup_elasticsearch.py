from elasticsearch import Elasticsearch
import os

es = Elasticsearch([{"host": os.environ.get("ELASTICSEARCH_HOST")}])

es.indices.create(
    index=os.environ.get("FACE_EMBEDDING_INDEX"),
    body={
        "mappings": {
            "properties": {
                "embedding": {"type": "dense_vector", "dims": 512},
                "user_id": {"type": "integer"},
                "datetime_created": {"type": "date", "format": "epoch_millis"},
            }
        }
    },
    ignore=400,
)
es.indices.create(
    index=os.environ.get("VOICE_EMBEDDING_INDEX"),
    body={
        "mappings": {
            "properties": {
                "embedding": {"type": "dense_vector", "dims": 512},
                "user_id": {"type": "integer"},
                "datetime_created": {"type": "date", "format": "epoch_millis"},
            }
        }
    },
    ignore=400,
)
es.indices.create(
    index=os.environ.get("TEXT_EMBEDDING_INDEX"),
    body={
        "mappings": {
            "properties": {
                "embedding": {"type": "dense_vector", "dims": 768},
                "user_id": {"type": "integer"},
                "document_id": {"type": "integer"},
                "raw_text": {"type": "text"},
                "datetime_created": {"type": "date", "format": "epoch_millis"},
            }
        }
    },
    ignore=400,
)

print("Elasticsearch is set up")
