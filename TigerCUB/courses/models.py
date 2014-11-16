import datetime, time
from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django.contrib.auth.models import User

tags = ["Language", "Science", "Engineering", "Politics", "Visual Arts", "Interdisciplinary", "Cultural"]

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=50)
    netid = models.CharField(max_length=50)
    year = models.IntegerField(max_length=50)
    major = EmbeddedModelField("Subject")
    coursesTaken = DictField("Course")
    preferenceTags = ListField()
    def __unicode__(self):
        return name

class Certificate(models.Model):
    courseCategories = EmbeddedModelField("CourseCategory")
    notes = models.TextField()

class CourseCategory(models.Model):
    courses = ListField(EmbeddedModelField("Course"))
    numberNeeded = models.IntegerField()

class Term(models.Model):
    code = models.IntegerField() #Registrar's numeric code, like '1114' for Spring 2011
    suffix = models.CharField(max_length=6) #Blackboard coursename suffix, like 'S2011'
    name = models.CharField(max_length=7) #Short name, like 'S10-11'
    calName = models.CharField(max_length=11) #Calender-style long name, like 'Spring 2011'
    regName = models.CharField(max_length=10) #Registrar's long name, like '10-11 Spr'
    startDate = models.DateField()
    endDate = models.DateField()
    subjects = ListField(EmbeddedModelField("Subject"))
    def __unicode__(self):
        return self.name

class Subject(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    deptCode = models.CharField(max_length=3)
    dept = models.CharField(max_length=100)
    courses = ListField(EmbeddedModelField("Course"))
    def __unicode__(self):
        return self.name

class Course(models.Model):
    guid = models.IntegerField()
    courseID = models.IntegerField()
    catalogNumber = models.CharField(max_length=3)
    title = models.CharField(max_length=300)
    detail = EmbeddedModelField("Detail")
    instructors = ListField(EmbeddedModelField("Instructor"))
    crosslistings = ListField(EmbeddedModelField("Crosslisting"))
    classes = ListField(EmbeddedModelField("Class"))
    def getRegistrarURL():
        pass
    def getEvaluationURL():
        pass
    def __unicode__(self):
        return self.title

class Detail(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    track = models.CharField(max_length=10)
    description = models.TextField()
    def __unicode___(self):
        return self.description
    
class Instructor(models.Model):
    emplid = models.CharField(max_length=9)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    fullName = models.CharField(max_length=100)
    def __unicode__(self):
        return self.fullName

class Crosslisting(models.Model):
    subject = models.CharField(max_length=3)
    catalogNumber = models.CharField(max_length=7)
    def __unicode__(self):
        return self.subject + u" " + self.catalog

class Class(models.Model):
    classNumber = models.IntegerField()
    section = models.CharField(max_length=7)
    status = models.CharField(max_length=25)
    typeName = models.CharField(max_length=25)
    capacity = models.IntegerField()
    enrollment = models.IntegerField()
    schedule = EmbeddedModelField("Schedule", null=True)
    def __unicode__(self):
        return self.section
    
class Schedule(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    meetings = ListField(EmbeddedModelField("Meeting"))
    def __unicode__(self):
        return str(self.startDate) + " - " + str(self.endDate)

class Meeting(models.Model):
    meetingNumber = models.IntegerField()
    startTime = models.TimeField()
    endTime = models.TimeField()
    room = models.CharField(max_length=25)
    buildings = ListField(EmbeddedModelField("Building"))
    days = ListField()
    def __unicode__(self):
        return self.days + u" " + unicode(self.startTime) + u" - " + unicode(self.endTime)
  
class Building(models.Model):
    buildingCode = models.CharField(max_length=5)
    locationCode = models.CharField(max_length=4)
    name = models.CharField(max_length=100)
    shortName = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name
