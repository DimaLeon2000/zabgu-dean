from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


def indexView(request):
    specialties = Specialty.objects.all()
    # Выборка группы из специальности
    # spec_input = request.GET.get('spec-input')
    # groups = []
    groups = Group.objects.all()
    # if spec_input:
    #     groups = Group.objects.filter(specialty_id=spec_input)
    # Выборка студентов из группы
    # group_input = request.GET.get('group-input')
    # students = []
    students = Student.objects.all()
    # students = Student.objects.all()
    # if group_input:
    #     students = Student.objects.filter(group_id=group_input)

    #  groups = Group.objects.all()
    #  students = Student.objects.all()
    marks = Mark.objects.all()
    #  marksPiv = pivot(marks, 'subject__name', 'session', 'score')
    return render(request, 'app/index.html', {'Specialty': specialties, 'Group': groups, 'Student': students, 'Mark': marks})


def get_groups(request, id_spec):
    groups = Group.objects.filter(specialty_id=id_spec) or []
    result = []
    for i in groups:
        result.append({
        'id': i.id,
        'name': i.name,
    })
    return JsonResponse({'result': result})


def get_students_spec(request, id_spec):
    students = Student.objects.filter(group__specialty_id=id_spec) or []
    result = []
    for i in students:
        result.append({
        'id': i.id,
        'firstname': i.firstname,
        'lastname': i.lastname,
        'surname': i.surname,
    })
    return JsonResponse({'result': result})


def get_students_group(request, id_group):
    students = Student.objects.filter(group_id=id_group) or []
    result = []
    for i in students:
        result.append({
        'id': i.id,
        'firstname': i.firstname,
        'lastname': i.lastname,
        'surname': i.surname,
    })
    return JsonResponse({'result': result})

def get_marks_specialty(request, id_spec):
    marks = Mark.objects.filter(session__student__group__specialty_id=id_spec) or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})

def get_marks_specialty_sorted(request, id_spec):
    marks = Mark.objects.filter(session__student__group__specialty_id=id_spec).order_by('score') or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})

def get_marks_group(request, id_group):
    marks = Mark.objects.filter(session__student__group_id=id_group) or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})

def get_marks_group_sorted(request, id_group):
    marks = Mark.objects.filter(session__student__group_id=id_group).order_by('score') or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})

def get_marks_student(request, id_student):
    marks = Mark.objects.filter(session__student_id=id_student) or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})


def get_marks_student_sorted(request, id_student):
    marks = Mark.objects.filter(session__student_id=id_student).order_by('score') or []
    result = []
    for i in marks:
        result.append({
        'id': i.id,
        'session': i.session_id,
        'student_id': i.session.student_id,
        'student_name': i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
        'subject_id': i.subject.id,
        'subject_name': i.subject.name,
        'group': i.session.student.group.__str__(),
        'startdate': i.session.startdate.strftime("%d.%m.%Y"),
        'enddate': i.session.enddate.strftime("%d.%m.%Y"),
        'score': i.score,
    })
    return JsonResponse({'result': result})


class SpecialtyViewSet(ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    http_method_names = ['get', ]


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get', ]


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    http_method_names = ['get', ]


class SessionViewSet(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    http_method_names = ['get', ]


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    http_method_names = ['get', ]


class MarkViewSet(ModelViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkSerializer
    http_method_names = ['get', ]


class MarkViewSetSorted(ModelViewSet):
    queryset = Mark.objects.order_by('score') or []
    serializer_class = MarkSerializer
    http_method_names = ['get', ]
