from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_images')
    description = models.CharField(max_length=500)
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')

    def __str__(self) -> str:
        return f'{self.name} {self.id}'


class Specialty(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='MEDIA_SPECIALITY_IMAGE_DIR')

    def __str__(self) -> str:
        return f'{self.title} {self.code}'


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()

    def __str__(self) -> str:
        return f'{self.title} {self.specialty} {self.company} {self.salary_min} {self.salary_max} {self.id}'


class Application(models.Model):
    written_username = models.CharField(max_length=50)
    written_phone = models.CharField(max_length=11)
    written_cover_letter = models.CharField(max_length=500)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')


class Resume(models.Model):
    STATUS_CHOICES = (
        ('1', 'Не ищу работу'),
        ('2', 'Рассматриваю предложение'),
        ('3', 'Ищу работу'),
    )

    GRADE_CHOICES = (
        ('1', 'Стажер'),
        ('2', 'Джуниор'),
        ('3', 'Миддл'),
        ('4', 'Синьор'),
        ('5', 'Лид'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume')
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    salary = models.FloatField()
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES)
    edication = models.CharField(max_length=500)
    experience = models.CharField(max_length=500)
    portfolio = models.CharField(max_length=500)
