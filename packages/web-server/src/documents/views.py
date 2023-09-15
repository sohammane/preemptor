from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from .models import Document
from .utils import check_similarities
from users.models import User


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@login_required
def similar_documents(request, pk):
    try:
        document = Document.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    _, matches = check_similarities(document)

    docs = []
    for doc_id, similarity in matches.items():
        doc = Document.objects.get(pk=doc_id)
        docs.append(
            {
                "id": doc.id,
                "name": doc.name,
                "author": doc.user.full_name,
                "score": similarity,
            }
        )

    return Response(docs)
