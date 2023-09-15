from rest_framework import viewsets, permissions

from . import serializers
from . import models


class VoucherViewSet(viewsets.ModelViewSet):
    """ViewSet for the Voucher class"""

    queryset = models.Voucher.objects.all()
    serializer_class = serializers.VoucherSerializer
    permission_classes = []

    def get_queryset(self):
        if self.request.GET.get("code"):
            return models.Voucher.objects.filter(code=self.request.GET.get("code"))
        return models.Voucher.objects.all()
