import json

from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .models import Interview
from .utils import addInterviews, dataChecks


@require_GET
def indexView(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")


@require_GET
def readInterviewsView(request: HttpRequest) -> HttpResponse:
    allInterviews = Interview.objects.all().select_related("interviewee")
    return render(request, "interviews.html", context={"allInterviews": allInterviews})


@require_GET
def getInterviewView(request: HttpRequest) -> JsonResponse:
    interviewId = request.GET.get("interviewId")
    interview = Interview.objects.filter(interviewId=interviewId).select_related(
        "interviewee"
    )
    return JsonResponse({"interview": interview})


@require_POST
def updateInterview(request: HttpRequest) -> JsonResponse:
    interviewId = request.GET.get("interviewId")
    submitData = json.loads(request.body)
    dataError = dataChecks(submitData)
    if dataError:
        return JsonResponse(dataError[0], status=dataError[1])
    else:
        submitData["email"] = list(set(submitData["email"]))
        interview = Interview.objects.filter(interviewId=interviewId)
        if interview.exists:
            interview.delete()
            res, code = addInterviews(submitData)
            return JsonResponse(res, status=code)
        else:
            return JsonResponse({"status": "failure", "reason": "wrong id"}, status=400)


@require_POST
def submitFormView(request: HttpRequest) -> JsonResponse:
    submitData = json.loads(request.body)
    dataError = dataChecks(submitData)
    if dataError:
        return JsonResponse(dataError[0], status=dataError[1])
    res, code = addInterviews(submitData)
    return JsonResponse(res, status=code)
