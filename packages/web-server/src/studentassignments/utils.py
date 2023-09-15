from notifications.services import mail
from users.models import User
from assignments.models import Assignment
from .serializers import StudentAssignmentSerializer
from .models import StudentAssignment


def create_studentassignment(data):
    # check if student assignment already exists
    # this handles the case where a user is present in multiple clazzes that were assigned
    try:
        user = User.objects.get(pk=data["user"])
    except:
        user = data["user"]
    try:
        assignment = Assignment.objects.get(pk=data["assignment"])
    except:
        assignment = data["assignment"]

    try:
        studentassignment = StudentAssignment.objects.get(
            assignment=assignment, user=user
        )
        # if no exception was raised, return this serializer
        return StudentAssignmentSerializer(
            studentassignment
        )  # TODO add serializer context
    except StudentAssignment.DoesNotExist:
        pass

    serializer = StudentAssignmentSerializer(data=data)  # TODO add serializer context
    serializer.is_valid(raise_exception=True)
    studentassignment = serializer.save()

    try:
        student = studentassignment.user
        assignment = studentassignment.assignment
        mail(
            student.first_name,
            student.email,
            params={
                "title": "New Assignment Available",
                "body": "A new assignment is available for you to complete. Click the button below to check it out.",
                "cta_text": "Open Assignment",
                "cta_url": "https://app.preemptor.ai/assignment/{}".format(
                    assignment.id
                ),
            },
        )
    except Exception as e:
        print(e)

    return serializer

