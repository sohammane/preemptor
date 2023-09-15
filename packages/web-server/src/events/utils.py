from django.db.models import Count, Q

from notifications.services import mail
from users.models import User
from .models import Event


def cron_notify():
    pendings_qs = (
        Event.objects.values("user__institution")
        .annotate(
            pending=Count("user__institution", filter=Q(status=Event.EVENT_PENDING))
        )
        .order_by()
    )
    pending_institutions = {
        ps["user__institution"]: ps["pending"] for ps in pendings_qs
    }
    supervisors = User.objects.filter(
        institution__in=pending_institutions.keys(), role=User.ROLE_SUPERVISOR,
    )
    for supervisor in supervisors:
        if pending_institutions[supervisor.institution.id] > 0:
            mail(
                supervisor.full_name,
                supervisor.email,
                {
                    "title": "There are pending ocurrences",
                    "subject": "Pending student ocurrences",
                    "body": """
                        There are {} pending ocurrences from {} students on Preemptor. 
                        You may see more details and review them by clicking the button below.
                        """.format(
                        pending_institutions[supervisor.institution.id],
                        supervisor.institution.name,
                    ),
                    "cta_text": "Review Ocurrences",
                    "cta_url": "https://app.preemptor.ai/events",
                },
            )
