from django.db import models
from django.contrib import admin


class Specialty(models.Model):
    class Meta:
        verbose_name = 'Специальность'
        verbose_name_plural = 'Все специальности'
    name = models.CharField(verbose_name='Наименование', max_length=60)
    shortname = models.CharField(verbose_name='Наименование (краткое)', max_length=10)
    def __str__(self):
        return self.name + ' (' + self.shortname + ')'


class Group(models.Model):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Все группы'
    name = models.CharField(verbose_name='Наименование', max_length=20)
    specialty = models.ForeignKey(Specialty, verbose_name='Специальность', on_delete=models.CASCADE)
    regyear = models.PositiveIntegerField(verbose_name='Год регистрации')

    def __str__(self):
        return self.name


class Student(models.Model):
    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Все студенты'
    firstname = models.CharField(verbose_name='Имя', max_length=30)
    surname = models.CharField(verbose_name='Фамилия', max_length=30)
    lastname = models.CharField(verbose_name='Отчество', max_length=30, null=True)
    group = models.ForeignKey(Group, verbose_name='Группа', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.surname + ' ' + self.firstname[0:1] + '.' + self.lastname[0:1] + '.'


class Session(models.Model):
    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Все сессии'
    student = models.ForeignKey(Student, verbose_name='Студент', on_delete=models.SET_NULL, null=True)
    startdate = models.DateField(verbose_name='Дата начала сессии')
    enddate = models.DateField(verbose_name='Дата конца сессии', null=True, blank=True)
    def __str__(self):
        return str(self.student) + ': Сессия (' + str(self.startdate) + ' - ' + str(self.enddate) + ')'


class Subject(models.Model):
    class Meta:
        verbose_name = 'Учебный предмет'
        verbose_name_plural = 'Все учебные предметы'
    name = models.CharField(verbose_name='Наименование', max_length=255)
    def __str__(self):
        return self.name


class Mark(models.Model):
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Все оценки'
    session = models.ForeignKey(Session, verbose_name='Сессия', on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, verbose_name='Предмет', on_delete=models.SET_NULL, null=True)
    score = models.PositiveSmallIntegerField(verbose_name='Оценка')
    def __str__(self):
        return str(self.session) + ': ' + str(self.subject) + ' (' + str(self.score) + ')'


#  admin.site.register(Specialty)
#  admin.site.register(Group)
#  admin.site.register(Student)
#  admin.site.register(Session)
#  admin.site.register(Subject)
#  admin.site.register(Mark)
