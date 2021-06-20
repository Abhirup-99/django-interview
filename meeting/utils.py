import os
from typing import Dict, List, Optional, Tuple, TypedDict

from django.db import transaction
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Interview, Interviewee, Interviewer


class interviewData(TypedDict):
    email: List[str]
    starttime: int
    endtime: int
    interviewId: str


def sendEmail(emails: List[str]) -> None:
    message = Mail(
        from_email="abhiruppalmethodist@gmail.com",
        to_emails=emails,
        subject="Interview",
        html_content="Interview is scheduled.",
    )
    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        pass


def addInterviews(submitData: interviewData) -> Tuple[Dict[str, str], int]:
    email = submitData["email"]
    starttime = submitData["starttime"]
    endtime = submitData["endtime"]
    assert email is not None
    assert endtime is not None
    assert starttime is not None
    with transaction.atomic():
        interviewees = Interviewee.objects.select_for_update().filter(email__in=email)
        if len(interviewees) != len(email):
            return ({"status": "failure", "reason": "user email not found"}, 400)
        interviews = (
            Interview.objects.filter(interviewee__in=interviewees.values_list("id"))
            .filter(
                starttime__gt=starttime,
                starttime__lt=endtime,
            )
            .filter(
                starttime__lt=starttime,
                endtime__gt=starttime,
            )
        )
        interviewer = Interviewer.objects.get(pk=1)
        if interviews.exists and len(interviews) > 0:
            return (
                {
                    "status": "failure",
                    "reason": "interviewees has a meeting scheduled already",
                },
                400,
            )

        interviewId = (
            submitData["interviewId"]
            if submitData.get("interviewId")
            else str(starttime) + email[0]
        )
        for interviewee in interviewees:
            newInterview = Interview(
                interviewee=interviewee,
                interviewer=interviewer,
                starttime=starttime,
                endtime=endtime,
                interviewId=interviewId,
            )
            newInterview.save()
        sendEmail(email)
        return ({"status": "success", "interviewId": interviewId}, 200)


def dataChecks(submitData: interviewData) -> Optional[Tuple[Dict[str, str], int]]:
    if submitData["endtime"] <= submitData["starttime"]:
        return ({"status": "failure", "reason": "bad time range"}, 400)
    submitData["email"] = list(set(submitData["email"]))
    if len(submitData["email"]) < 2:
        return (
            {"status": "failure", "reason": "at least 2 participants required"},
            400,
        )
    return None
