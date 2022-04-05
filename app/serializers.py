from rest_framework import serializers
from .models import *


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'name', 'shortname')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'specialty', 'regyear')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'firstname', 'surname', 'lastname', 'group')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'student', 'startdate', 'enddate')


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name')


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'session', 'subject', 'score', 'student', 'group', 'startdate', 'enddate')

    subject = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    startdate = serializers.SerializerMethodField()
    enddate = serializers.SerializerMethodField()

    def get_subject(self, obj):
        return obj.subject.name

    def get_student(self, obj):
        return obj.session.student.surname + ' ' + obj.session.student.firstname[
                                                   0:1] + '.' + obj.session.student.lastname[0:1] + '.'
    def get_group(self, obj):
        return obj.session.student.group.__str__()

    def get_startdate(self, obj):
        return obj.session.startdate.strftime("%d.%m.%Y")

    def get_enddate(self, obj):
        return obj.session.enddate.strftime("%d.%m.%Y")
