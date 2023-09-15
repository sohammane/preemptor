import json
import os
from datetime import datetime
import urllib3
import nltk
from nltk import tokenize
from elasticsearch import Elasticsearch

from .models import Document
from .serializers import DocumentSerializer
from users.models import User
from assignments.models import Assignment
from studentassignments.models import StudentAssignment

nltk.download("punkt")
es = Elasticsearch([{"host": os.environ.get("ELASTICSEARCH_HOST")}])


def create_document(data, user):
    studentassignment = None
    name = data["name"] if "name" in data else "Untitled Document"
    template_data = ""
    has_template = False

    if "assignment" in data:
        try:
            assignment = Assignment.objects.get(pk=data["assignment"])
        except:
            # django does not allow to check by type
            assignment = data["assignment"]

        print("assignment", assignment)
        name = assignment.name

        # this may be a response for an assignment, an studentassignment *must* already exist
        # the other case is that this is a template document
        if user.role == User.ROLE_STUDENT:
            studentassignment = StudentAssignment.objects.get(
                assignment=assignment.id, user=user.id
            )

            # check if a document for this assignment already exists
            try:
                # studentassignment suffices bc it is a key for (document, assignment, user)
                document = Document.objects.get(studentassignment=studentassignment)
                # if no exption was raised, return the existing document
                return DocumentSerializer(document)  # TODO add serializer context
            except:
                pass

        # fill in the template data if the professor created one
        try:
            template_doc = Document.objects.get(
                assignment=assignment.id, user__role=User.ROLE_PROFESSOR,
            )
            if template_doc:
                has_template = True
                template_data = template_doc.data
        except Exception as e:
            print(e)

    # if user's institution requires auth, this document must require it too
    if user.institution.has_facial_recognition:
        data["requires_face"] = True
    if user.institution.has_voice_recognition:
        data["requires_voice"] = True
    if user.institution.has_screen_invigilation:
        data["requires_screen"] = True

    data["user"] = user.id
    data["name"] = name
    data["data"] = template_data
    data["has_template"] = has_template
    data["studentassignment"] = studentassignment.id if studentassignment else None

    serializer = DocumentSerializer(data=data)  # TODO add serializer context
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return serializer


def register_document_embeddings(document):
    # delete existing embeddings for this document to avoid too much space usage
    query = {"query": {"match": {"document_id": document.id}}}
    res = es.delete_by_query(
        index=os.environ.get("TEXT_EMBEDDING_INDEX"), body=query, refresh=True
    )
    print(
        "Deleted existing embeddings for document {}: ".format(document.id),
        res["deleted"],
    )

    # transform text into sentences
    sentences = tokenize.sent_tokenize(document.raw_data)
    for sentence in sentences:
        # send text to encoder and receive embedding
        http = urllib3.PoolManager()
        serialized_data = http.request(
            "POST", os.environ.get("TEXT_SERVER"), fields={"text": sentence},
        )
        embedding = json.loads(serialized_data.data.decode("utf-8"))
        # save embedding to elasticsearch
        es_entry = {
            "embedding": embedding,
            "user_id": document.user.id,
            "document_id": document.id,
            "raw_text": sentence,
            "datetime_created": int(
                datetime.now().timestamp() * 1000
            ),  # datetime, in milliseconds since epoch
        }
        res = es.index(
            index=os.environ.get("TEXT_EMBEDDING_INDEX"), body=es_entry, refresh=True
        )
        if res["result"] != "created":
            del es_entry["embedding"]
            print(
                "Error saving embeddings. Payload: ", es_entry, "\nError: ", res,
            )

    print(
        "Sentence embeddings saved to elasticsearch. (document: {}, user: {})".format(
            document.id, document.user.id
        )
    )


def check_similarities(document):
    # transform text into sentences
    sentences = tokenize.sent_tokenize(document.raw_data)
    matches = []
    doc_matches = {}

    for sentence in sentences:
        # send text to encoder and receive embedding
        http = urllib3.PoolManager()
        serialized_data = http.request(
            "POST", os.environ.get("TEXT_SERVER"), fields={"text": sentence},
        )
        embedding = json.loads(serialized_data.data.decode("utf-8"))

        # check best matching sentences with elasticsearch
        query = {
            "_source": ["document_id", "user_id", "raw_text", "datetime_created"],
            "min_score": 1.9,
            "query": {
                "script_score": {
                    "query": {
                        "bool": {
                            "must_not": {
                                "bool": {
                                    "should": [
                                        {"match": {"document_id": document.id}},
                                        {"match": {"user_id": document.user.id}},
                                    ]
                                }
                            }
                        }
                    },
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": embedding},
                    },
                },
            },
        }
        res = es.search(
            body=query, index=os.environ.get("TEXT_EMBEDDING_INDEX"), size=5
        )  # limit top 5 results

        for hit in res["hits"]["hits"]:
            matches.append(
                {
                    "id": hit["_id"],
                    "document_id": hit["_source"]["document_id"],
                    "user_id": hit["_source"]["user_id"],
                    "score": hit["_score"],
                }
            )
            if hit["_source"]["document_id"] in doc_matches:
                doc_matches[hit["_source"]["document_id"]] += 1 / len(sentences)
            else:
                doc_matches[hit["_source"]["document_id"]] = 1 / len(sentences)

    # TODO calculate a better similarity score
    # consider len(sentence) and score too
    score = len(matches) / (len(sentences) or 1)

    return score, doc_matches
