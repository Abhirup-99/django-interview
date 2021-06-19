from typing import Dict, Optional, Tuple, Any, List, TypedDict
from django.db import transaction
from .models import Interviewee, Interview, Interviewer


class interviewData(TypedDict):
    email: List[str]
    starttime: int
    endtime: int


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
        if not interviews.exists:
            return (
                {
                    "status": "failure",
                    "reason": "interviewees has a meeting scheduled already",
                },
                400,
            )

        interviewId = str(starttime) + email[0]
        for interviewee in interviewees:
            newInterview = Interview(
                interviewee=interviewee,
                interviewer=interviewer,
                starttime=starttime,
                endtime=endtime,
                interviewId=interviewId,
            )
            newInterview.save()
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
