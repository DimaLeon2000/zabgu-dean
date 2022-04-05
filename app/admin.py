from django.contrib import admin
from app.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(Specialty)
class SpecialtyAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'shortname')
    list_display_links = ('id', 'name', 'shortname')


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'specialty', 'regyear')
    list_display_links = ('id', 'name', 'specialty', 'regyear')


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'firstname', 'surname', 'lastname', 'group')
    list_display_links = ('id', 'firstname', 'surname', 'lastname', 'group')


@admin.register(Session)
class SessionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'student', 'startdate', 'enddate')
    list_display_links = ('id', 'student', 'startdate', 'enddate')


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(Mark)
class MarkAdmin(ImportExportModelAdmin):
    list_display = ('id', 'session', 'subject', 'score')
    list_display_links = ('id', 'session', 'subject', 'score')
