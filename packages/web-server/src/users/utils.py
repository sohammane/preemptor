from datetime import timedelta
from django.utils import timezone
from django.db.models import F, Q, Sum, Avg
from sessions.models import Session


def originality_score(user):
    agg = (
        Session.objects.exclude(ended_at__isnull=True)
        .filter(user=user)
        .annotate(duration=F("ended_at") - F("created_at"))  # datetime diff in seconds
        .aggregate(
            time_total=Sum("duration"),
            time_total_last_90d=Sum(
                "duration",
                filter=Q(created_at__gte=timezone.now() - timedelta(days=90)),
            ),
            time_above_70=Sum("duration", filter=Q(confidence__gte=0.7)),
            avg_confidence=Avg("confidence"),
        )
    )
    p1 = (
        agg["time_above_70"].total_seconds() / agg["time_total"].total_seconds()
        if agg["time_above_70"] and agg["time_total"]
        else 0
    )
    p2 = max(agg["avg_confidence"] or 0, 0)
    p3 = (
        min(int(agg["time_total_last_90d"].total_seconds() / (50 * 60)), 10)
        if agg["time_total_last_90d"]
        else 0
    ) / 10  # convert to 0 ~ 1 range

    return 0.6 * p1 + 0.3 * p2 + 0.1 * p3
