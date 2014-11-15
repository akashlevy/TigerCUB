# Import libraries
import requests
import re
import datetime, time
import xml.etree.ElementTree as xml
from courses.models import *


# Constants, URLs, paths
WEBFEED_URL = "http://etcweb.princeton.edu/webfeeds/courseofferings"
EVALUATION_URL = "https://reg-captiva.princeton.edu/chart/index.php"
NAMESPACE_URL = "http://as.oit.princeton.edu/xml/courseofferings-1_4"
TIME_FORMAT = "%I:%M %p"
DATE_FORMAT = "%Y-%m-%d"
DATA_PATH = "data.xml"


# Gets data from all terms
def getAllData():
    with open(DATA_PATH, "w") as dataFile:
        getData({"term": "all", "subject": "all"})


# Gets current term data
def getCurrentData():
    with open(DATA_PATH, "w") as dataFile:
        getData({"subject": "all"})


# Generic data retriever
def getData(inputParams):
    with open(DATA_PATH, "w") as dataFile:
        dataFile.write(requests.get(WEBFEED_URL, params=inputParams).text.encode("utf8"))


# Loads data from data file into database
def loadData():
    # Read data from data file
    with open(DATA_PATH) as dataFile:
        data = dataFile.read()

    # Remove the namespace
    data = re.sub(' xmlns="[^"]+"', "", data, count=1)

    # Parse xml into tree
    root = xml.fromstring(data)

    # Get all terms
    for termElement in root.findall("term"):
        term = Term()
        term.code = int(termElement.find("code").text)
        term.suffix = termElement.find("suffix").text
        term.name = termElement.find("name").text
        term.calName = termElement.find("cal_name").text
        term.regName = termElement.find("reg_name").text
        term.startDate = datetime.datetime.strptime(termElement.find("start_date").text, DATE_FORMAT)
        term.endDate = datetime.datetime.strptime(termElement.find("end_date").text, DATE_FORMAT)
        print "Term " + str(term.code) # DEBUG
        
        for subjectElement in termElement.find("subjects").findall("subject"):
            # Get subject data
            subject = Subject()
            subject.code = subjectElement.find("code").text
            subject.name = subjectElement.find("name").text
            subject.deptCode = subjectElement.find("dept_code").text
            subject.dept = subjectElement.find("dept").text

            for courseElement in subjectElement.find("courses").findall("course"):
                # Get course data
                course = Course()
                course.guid = int(courseElement.find("guid").text)
                course.courseID = int(courseElement.find("course_id").text)
                course.catalogNumber = courseElement.find("catalog_number").text
                course.title = courseElement.find("title").text
                if course.title is None:
                    continue
                
                print str(course.courseID) + ": " + subject.code + " " + course.catalogNumber # DEBUG

                # Get course detail
                detailElement = courseElement.find("detail")
                detail = Detail()
                detail.startDate = datetime.datetime.strptime(detailElement.find("start_date").text, DATE_FORMAT)
                detail.endDate = datetime.datetime.strptime(detailElement.find("end_date").text, DATE_FORMAT)
                detail.track = detailElement.find("track").text
                detail.description = detailElement.find("description").text
                if detail.description == None:
                    detail.description = ""
                course.detail = detail

                # Get instructors
                for instructorElement in courseElement.find("instructors").findall("instructor"):
                    instructor = Instructor()
                    instructor.emplid = instructorElement.find("emplid").text
                    instructor.firstName = instructorElement.find("first_name").text
                    instructor.lastName = instructorElement.find("last_name").text
                    instructor.fullName = instructorElement.find("full_name").text
                    course.instructors.extend([instructor])

                # Get crosslistings
                if courseElement.find("crosslistings") is not None:
                    for crosslistingElement in courseElement.find("crosslistings").findall("crosslisting"):
                        crosslisting = Crosslisting()
                        crosslisting.subject = crosslistingElement.find("subject").text
                        crosslisting.catalogNumber = crosslistingElement.find("catalog_number").text
                        course.crosslistings.extend([crosslisting])

                # Get classes
                for classElement in courseElement.find("classes").findall("class"):
                    _class = Class()
                    _class.classNumber = int(classElement.find("class_number").text)
                    _class.section = classElement.find("section").text
                    _class.status = classElement.find("status").text
                    _class.typeName = classElement.find("type_name").text
                    _class.capacity = int(classElement.find("capacity").text)
                    _class.enrollment = int(classElement.find("enrollment").text)

                    # Get schedule
                    scheduleElement = classElement.find("schedule")
                    schedule = Schedule()
                    if scheduleElement is not None:
                        schedule.startDate = datetime.datetime.strptime(scheduleElement.find("start_date").text, DATE_FORMAT)
                        schedule.endDate = datetime.datetime.strptime(scheduleElement.find("end_date").text, DATE_FORMAT)

                        # Get meetings
                        for meetingElement in scheduleElement.find("meetings").findall("meeting"):
                            meeting = Meeting()
                            meeting.meetingNumber = int(meetingElement.find("meeting_number").text)
                            meeting.startTime = datetime.datetime.strptime(meetingElement.find("start_time").text, TIME_FORMAT)
                            meeting.endTime = datetime.datetime.strptime(meetingElement.find("end_time").text, TIME_FORMAT)
                            try:
                                meeting.room = meetingElement.find("room").text
                            except AttributeError:
                                meeting.room = ""

                            # Get days a class meets
                            for dayElement in meetingElement.find("days").findall("day"):
                                meeting.days.extend([dayElement.text])

                            # Get building a class meets in
                            buildingElement = meetingElement.find("building")
                            building = Building()
                            try:
                                building.buildingCode = buildingElement.find("building_code").text
                                building.locationCode = buildingElement.find("location_code").text
                                building.name = buildingElement.find("name").text
                                building.shortName = buildingElement.find("short_name").text
                                meeting.building = building
                            except AttributeError:
                                building.buildingCode = ""
                                building.locationCode = ""
                                building.name = ""
                                building.shortName = ""

                            schedule.meetings.extend([meeting])
                        _class.schedule = schedule
                    course.classes.extend([_class])
                subject.courses.extend([course])
            term.subjects.extend([subject])
        term.save()
