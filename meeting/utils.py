from django.db import transaction
from .models import Interviewee, Interview, Interviewer


def addInterviews(submitData):
    with transaction.atomic():
        interviewees = Interviewee.objects.select_for_update().filter(
            email__in=submitData.get("email")
        )
        if len(interviewees) != len(submitData.get("email")):
            return ({"status": "failure", "reason": "user email not found"}, 400)
        interviews = (
            Interview.objects.filter(interviewee__in=interviewees.values_list("id"))
            .filter(
                starttime__gt=submitData.get("starttime"),
                starttime__lt=submitData.get("endtime"),
            )
            .filter(
                starttime__lt=submitData.get("starttime"),
                endtime__gt=submitData.get("starttime"),
            )
        )
        interviewer = Interviewer.objects.get(pk=1)
        if not interviews.exists:
            return (
                {
                    "status": "failure",
                    "reason": "interviewees has a meeting scheduled already",
                },
                400,
            )
        interviewId = str(submitData.get("starttime")) + submitData.get("email")[0]
        for interviewee in interviewees:
            newInterview = Interview(
                interviewee=interviewee,
                interviewer=interviewer,
                starttime=submitData.get("starttime"),
                endtime=submitData.get("endtime"),
                interviewId=interviewId,
            )
            newInterview.save()
        return {"status": "success", "interviewId": interviewId}


def dataChecks(submitData):
    if submitData.get("endtime") <= submitData.get("starttime"):
        return ({"status": "failure", "reason": "bad time range"}, 400)
    submitData["email"] = list(set(submitData["email"]))
    if len(submitData.get("email")) < 2:
        return (
            {"status": "failure", "reason": "at least 2 participants required"},
            400,
        )
