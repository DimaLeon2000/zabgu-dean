from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import datetime


def print_marks(request):
    wb = Workbook()
    dest_filename = 'marks'+str(datetime.date.today())+'.xlsx'

    ws1 = wb.active
    ws1.title = "оценки"
    ws1['A1'] = 'Студент'
    ws1['B1'] = 'Группа'
    ws1['C1'] = '№ Сессии'
    ws1['D1'] = 'Предмет'
    ws1['E1'] = 'Дата начала'
    ws1['F1'] = 'Дата окончания'
    ws1['G1'] = 'Оценка'
    marks = Mark.objects.filter(score=0) or []
    column_widths = []
    for i in marks:
        ws1.append([i.session.student.surname + ' ' + i.session.student.firstname[0:1] + '.' + i.session.student.lastname[0:1] + '.',
                    i.session.student.group.__str__(),
                    i.session_id,
                    i.subject.name,
                    i.session.startdate.strftime("%d.%m.%Y"),
                    i.session.enddate.strftime("%d.%m.%Y"),
                    i.score])

    wb.save(filename = 'files/media/'+dest_filename)
    return redirect(f'/media/{dest_filename}')


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
    #  marksPiv = pivot(marks, 'subject__name', 'session', 'score')
    return render(request, 'app/index.html', {'Specialty': specialties, 'Group': groups, 'Student': students})


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


def get_marks_specialty_zeroes(request, id_spec):
    marks = Mark.objects.filter(session__student__group__specialty_id=id_spec, score=0) or []
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


def get_marks_specialty_sorted(request, id_spec, sorting):
    marks = Mark.objects.filter(session__student__group__specialty_id=id_spec).order_by(sorting) or []
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


def get_marks_specialty_zeroes_sorted(request, id_spec, sorting):
    marks = Mark.objects.filter(session__student__group__specialty_id=id_spec, score=0).order_by(sorting) or []
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


def get_marks_group_zeroes(request, id_group):
    marks = Mark.objects.filter(session__student__group_id=id_group, score=0) or []
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


def get_marks_group_sorted(request, id_group, sorting):
    marks = Mark.objects.filter(session__student__group_id=id_group).order_by(sorting) or []
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


def get_marks_group_zeroes_sorted(request, id_group, sorting):
    marks = Mark.objects.filter(session__student__group_id=id_group, score=0).order_by(sorting) or []
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


def get_marks_student_zeroes(request, id_student):
    marks = Mark.objects.filter(session__student_id=id_student, score=0) or []
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


def get_marks_student_sorted(request, id_student, sorting):
    marks = Mark.objects.filter(session__student_id=id_student).order_by(sorting) or []
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


def get_marks_student_zeroes_sorted(request, id_student, sorting):
    marks = Mark.objects.filter(session__student_id=id_student, score=0).order_by(sorting) or []
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


class MarkViewSetZeroes(ModelViewSet):
    queryset = Mark.objects.filter(score=0) or []
    serializer_class = MarkSerializer
    http_method_names = ['get', ]


class MarkViewSetSorted(ModelViewSet):
    queryset = Mark.objects.all() or []
    serializer_class = MarkSerializer
    http_method_names = ['get', ]
    def list(self, request, *args, **kwargs):
        sorting = request.query_params.get('sorting', None)
        if sorting is not None:
            data = self.get_queryset().order_by(sorting)
            serialized_data = self.get_serializer(data, many=True)
            return Response(serialized_data.data)

        return super(MarkViewSetSorted, self).list(request, *args, **kwargs)


class MarkViewSetZeroesSorted(ModelViewSet):
    queryset = Mark.objects.filter(score=0) or []
    serializer_class = MarkSerializer
    http_method_names = ['get', ]
    def list(self, request, *args, **kwargs):
        sorting = request.query_params.get('sorting', None)
        if sorting is not None:
            data = self.get_queryset().order_by(sorting).filter(score=0)
            serialized_data = self.get_serializer(data, many=True)
            return Response(serialized_data.data)

        return super(MarkViewSetSorted, self).list(request, *args, **kwargs)
