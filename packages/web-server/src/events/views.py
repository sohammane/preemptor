from django.contrib.auth.decorators import login_required
from django.db.models import Min, Max, Sum, Count, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from datetime import datetime

from .models import Event
from . import utils


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
@login_required
def get_meta(request):
    base_queryset = Event.objects.filter(user__institution=request.user.institution)

    if request.GET.get("user__full_name"):
        base_queryset = base_queryset.filter(
            user__first_name__icontains=request.GET.get("user__full_name")
        ) | base_queryset.filter(
            user__last_name__icontains=request.GET.get("user__full_name")
        )
    if request.GET.get("status"):
        base_queryset = base_queryset.filter(status=request.GET.get("status"))
    if request.GET.get("created_at__gte"):
        base_queryset = base_queryset.filter(
            created_at__gte=request.GET.get("created_at__gte")
        )
    if request.GET.get("created_at__lte"):
        base_queryset = base_queryset.filter(
            created_at__lte=request.GET.get("created_at__lte")
        )

    agg = base_queryset.aggregate(
        created_at_min=Min("created_at"),
        created_at_max=Max("created_at"),
        total=Count("id"),
        pending=Count("id", filter=Q(status=Event.EVENT_PENDING)),
        in_analysis=Count("id", filter=Q(status=Event.EVENT_ANALYSIS)),
        closed=Count("id", filter=Q(status=Event.EVENT_CLOSED)),
        today_events=Count("id", filter=Q(created_at__gte=datetime.today().date())),
        closed_today=Count(
            "id",
            filter=Q(
                updated_at__gte=datetime.today().date(), status=Event.EVENT_CLOSED,
            ),
        ),
        oldest_in_analysis=Min("created_at", filter=Q(status=Event.EVENT_ANALYSIS)),
    )
    datediff_today = (
        (datetime.today().date() - agg["created_at_min"].date()).days
        if agg["created_at_min"]
        else 1
    )
    datediff_analysis = (
        (datetime.today().date() - agg["oldest_in_analysis"].date()).days
        if agg["oldest_in_analysis"]
        else 1
    )

    return Response(
        {
            "total_events": agg["total"],
            "pending_events": agg["pending"],
            "in_analysis_events": agg["in_analysis"],
            "closed_events": agg["closed"],
            "daily_avg_events": (agg["total"] or 0)
            / (datediff_today if datediff_today > 0 else 1),
            "today_events": agg["today_events"],
            "first_event_days_ago": datediff_analysis,
            "closed_events_today": agg["closed_today"],
        }
    )


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
def notify(request):
    utils.cron_notify()
    return Response(status=status.HTTP_200_OK)

