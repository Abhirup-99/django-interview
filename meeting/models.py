from django.db import models


class Interviewee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class Interviewer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

class Interview(models.Model):
    interviewee = models.ForeignKey(Interviewee, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    starttime = models.PositiveIntegerField()
    endtime = models.PositiveIntegerField()
    interviewId = models.CharField(max_length=200)