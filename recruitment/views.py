import operator
import datetime
from django.views.generic import ListView
from functools import reduce
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_extensions import auth

from recruitment.models import Specialty
from recruitment.models import Company
from recruitment.models import Vacancy
from recruitment.models import Application
from recruitment.models import Resume
from recruitment.forms import ApplicationForm
from recruitment.forms import CompanyForm
from recruitment.forms import VacancyForm
from recruitment.forms import ResumeForm
from recruitment.forms import SignUpForm
from recruitment.forms import UserProfileForm
# Create your views here.


class MainView(View):
    def get(self, request):
        current_user = request.user

        context = {'specialties': Specialty.objects.all(),
                   'companies': Company.objects.all(),
                   'vacancies': Vacancy.objects.all(),
                   'current_user': current_user,
                   }
        return render(
            request, 'index.html', context=context
        )


class VacanciesView(View):
    def get(self, request,  *args, **kwargs):
        my_company = Company.objects.filter(owner_id=request.user.id).first()
        my_vacancies = my_company.vacancies.all()

        context = {
            'vacancies': Vacancy.objects.all(),
            'companies': Company.objects.all(),
            'my_vacancies': my_vacancies,
                  }

        if not my_company:
            return render(
                    request, 'recruitment/vacancy_out.html', context=context
                )

        return render(
                request, 'recruitment/vacancies.html', context=context
            )

    def post(self, request, *args, **kwargs):
        applications = Application.objects.all()

        context = {
            'vacancies': Vacancy.objects.all(),
            'companies': Company.objects.all(),
            'applications': applications,
                   }

        return render(
                request, 'recruitment/vacancies.html', context=context
            )


class ListVacanciesView(ListView):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        paginator = Paginator(vacancies, 5)
        page = self.request.GET.get('page')
        try:
            vacancies = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            vacancies = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            vacancies = paginator.page(paginator.num_pages)


        context = {
            'all_vacancies': Vacancy.objects.all(),
            'vacancies': vacancies,
            }

        return render(
                request, 'recruitment/list_vacancies.html', context=context
            )


class CompanyVacancyView(View):
    def get(self, request, company_id: int, *args, **kwargs):
        cur_company = Company.objects.filter(id=company_id).first()
        cur_vacancies = Vacancy.objects.filter(company__id=company_id).all()

        context = {
            'cur_company': cur_company,
            'cur_vacancies': cur_vacancies,
                  }

        return render(
                request, 'recruitment/company_vacancies.html', context=context
            )


class SpecialtyView(ListView):
    def get(self, request, code: str):
        cur_specialty = Vacancy.objects.filter(specialty__code=code).first()
        special_vacancies = Vacancy.objects.filter(specialty__code=code).all()
        if not cur_specialty:
            raise Http404
        paginator = Paginator(special_vacancies, 2)
        page = self.request.GET.get('page')
        try:
            special_vacancies = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            special_vacancies = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            special_vacancies = paginator.page(paginator.num_pages)

        context = {
            'all_specialties': Vacancy.objects.filter(specialty__code=code).all(),
            'specialties': Specialty.objects.all(),
            'vacancies': Vacancy.objects.all(),
            'cur_specialty': cur_specialty,
            'special_vacancies': special_vacancies,
        }

        return render(
            request, 'recruitment/specialty.html', context=context
        )


class CardCompanyView(View):
    def get(self, request, company_id: int):
        company = get_object_or_404(Company, id=company_id)
        vacancies = Vacancy.objects.filter(company__name=company.name).all()

        context = {
            'company': company,
            'vacancies': vacancies,
        }
        return render(
            request, 'recruitment/company.html', context=context
        )


class VacancyView(View):
    def get(self, request, vacancy_id: int):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            raise Http404

        application_form = ApplicationForm()
        if application_form.is_valid():
            application_form.save()
        context = {
            'vacancy': vacancy,
            'application_form': application_form,
        }
        return render(
            request, 'recruitment/vacancy.html', context=context
        )

    def post(self, request, vacancy_id: int, *args, **kwargs):
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            application = application_form.save(commit=False)
            application.user = request.user
            application.vacancy = Vacancy.objects.filter(id=vacancy_id).first()
            application_form.save()

        context = {
            'application_form': application_form,
        }
        return render(
                   request, 'recruitment/sent.html', context=context
                )

        if not application_form.is_valid():
            application_form.save()

        context = {
            'application_form': application_form,
            'application_form.errors': application_form.errors,
        }

        return render(
                request, 'recruitment/vacancy.html', context=context
            )


class VacancyUpdateView(View):
    def get(self, request, vacancy_update: int):
        specialties = Specialty.objects.all()
        all_applications = Application.objects.all()
        current_vacancy = vacancy_update
        vacancy_form = VacancyForm()
        if vacancy_form.is_valid():
            vacancy_form.save()
        application_form = ApplicationForm()
        if application_form.is_valid():
            application_form.save()
        applications = Application.objects.all()
        paginator = Paginator(applications, 5)
        page = self.request.GET.get('page')
        try:
            applications = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            applications = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            applications = paginator.page(paginator.num_pages)

        context = {
            'vacancy_form': vacancy_form,
            'all_applications': all_applications,
            'specialties': specialties,
            'current_vacancy': current_vacancy,
            'application_form': application_form,
            'vacancies': Vacancy.objects.all(),
            'applications': applications,
        }

        return render(
            request, 'recruitment/vacancy_update.html', context=context
        )

    def post(self, request, vacancy_update: int):
        vacancy = Vacancy.objects.get(id=vacancy_update)
        vacancy_form = VacancyForm(request.POST, instance=vacancy)


        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.published_at = datetime.date.today()
            vacancy_form.save()

        context = {
            'vacancy_form': vacancy_form,
        }

        return render(
            request, 'recruitment/vacancy_update.html', context=context
        )

        if not vacancy_form.is_valid():
            vacancy_form.save()

        context = {
            'vacancy_form': vacancy_form,
            'vacancy_form.errors': vacancy_form.errors,
        }

        return render(
            request, 'recruitment/vacancy_update.html', context=context
        )


class VacancyEditView(View):
    def get(self, request):
        current_user = request.user
        specialties = Specialty.objects.all()
        applications = Application.objects.all()
        vacancy_form = VacancyForm()
        if vacancy_form.is_valid():
            vacancy_form.save()

        context = {
            'vacancy_form': vacancy_form,
            'current_user': current_user,
            'applications': applications,
            'specialties': specialties,
        }

        return render(
            request, 'recruitment/vacancy_edit.html', context=context
        )

    def post(self, request):
        vacancy_form = VacancyForm(request.POST)
        if vacancy_form.is_valid():
            vacancy = vacancy_form.save(commit=False)
            vacancy.company = Company.objects.filter(owner_id=request.user.id).first()
            vacancy.published_at = datetime.date.today()
            vacancy.save()

        context = {
            'vacancy_form': vacancy_form,
        }

        return render(
            request, 'recruitment/vacancy_edit.html', context=context
        )

        if not vacancy_form.is_valid():
            vacancy_form.save()

        context = {
            'vacancy_form': vacancy_form,
            'vacancy_form.errors': vacancy_form.errors,
        }

        return render(
            request, 'recruitment/vacancy_edit.html', context=context
        )


class CompanyOutView(View):
    def get(self, request):
        current_user = request.user
        company_form = CompanyForm()
        if company_form.is_valid():
            company_form.save()

        context = {
            'companies': Company.objects.all(),
            'company_form': company_form,
            'current_user': current_user,
        }

        return render(
            request, 'recruitment/company_out.html', context=context
        )


class CompanyCreateView(View):
    def get(self, request):
        company_form = CompanyForm()
        if company_form.is_valid():
            company_form.save()

        context = {
            'company_form': company_form,
        }

        return render(
            request, 'recruitment/company_create.html', context=context
        )

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner_id=request.user.id).first()
        company_form = CompanyForm(request.POST, request.FILES, instance=company)

        if company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            if not company:
                company.save()
            else:
                company_form.save()

        context = {
            'company_form': company_form
        }

        return render(
            request, 'recruitment/company_create.html', context=context
        )

        if not company_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company_form.save()

        context = {
            'company_form': company_form,
            'company_form.errors': company_form.errors,
        }

        return render(
            request, 'recruitment/company_create.html', context=context
        )


class MycompanyView(View):
    def get(self, request):
        current_user = request.user
        company = Company.objects.filter(owner_id=current_user.id).first()
        company_form = CompanyForm()
        if company_form.is_valid():
            company_form.save()

        context = {
            'companies': Company.objects.all(),
            'current_user': current_user,
            'company_form': company_form,
        }

        if not company:
            return render(
                request, 'recruitment/company_out.html', context=context
            )

        return render(
                request, 'recruitment/company_create.html', context=context
            )

    def post(self, request):
        company_form = CompanyForm(request.POST)
        if company_form.is_valid():
            company_form.save()

        context = {
            'company_form': company_form
        }

        return render(
            request, 'recruitment/company_create.html', context=context
        )

        if not company_form.is_valid():
            company_form.save()

        context = {
            'company_form': company_form,
            'company_form.errors': company_form.errors,
        }

        return render(
            request, 'recruitment/company_create.html', context=context
        )


class SentApplicationView(View):
    def get(self, request, vacancy_id: int):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()

        context = {
            'vacancy': vacancy
        }
        return render(
            request, 'recruitment/sent.html', context=context
        )


class MyresumeView(View):
    def get(self, request):
        user_id = Resume.objects.filter(user_id=request.user.id).first()

        if not user_id:
            return render(
                    request, 'recruitment/resume_create.html'
                )
            if not resume_form.is_valid():
                resume_form.save()
            context = {
                'resume_form.errors': resume_form.errors,
            }
            return render(
                request, 'recruitment/resume_create.html', context
            )

        return render(
                request, 'recruitment/resume_edit.html'
                )


class ResumeEditView(View):
    def get(self, request):
        resume_form = ResumeForm()
        if resume_form.is_valid():
            resume_form.save()

        context = {
            'resume_form': resume_form,
            'specialties': Specialty.objects.all(),
        }
        return render(
                request, 'recruitment/resume_edit.html', context=context
            )

    def post(self, request):
        resume = Resume.objects.filter(user_id=request.user.id).first()
        resume_form = ResumeForm(request.POST, instance=resume)
        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            if not resume:
                resume.save()
            else:
                resume_form.save()

        context = {
                'resume_form': resume_form,
                'specialties': Specialty.objects.all(),
        }
        return render(
            request, 'recruitment/resume_edit.html', context=context
            )

        if not resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user

        context = {
            'resume_form': resume_form,
            'specialties': Specialty.objects.all(),
            'resume_form.errors': resume_form.errors,
        }
        return render(
                request, 'recruitment/resume_edit.html', context=context
            )


class SearchView(ListView):
    model = Vacancy
    template_name = 'recruitment/search.html'
    paginate_by = 10
    ordering = ['-published_at']

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('s')

        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(skills__icontains=q) for q in query_list))
            )
        return result


class SentView(View):
    def get(self, request):

        return render(
                    request, 'recruitment/sent.html'
                )

    def post(self, request, *args, **kwargs):

        return render(
                    request, 'recruitment/sent.html'
                )


class ProfileView(View):
    def get(self, request):
        form = UserProfileForm
        context = {
            'form': form,
        }
        return render(
            request, 'recruitment/profile.html', context=context
        )

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        print(request.POST)
        print(form.errors)
        context = {
            'form': form,
            'form.errors': form.errors,
        }

        return render(
            request, 'recruitment/profile.html', context=context
        )


class AboutUsView(View):
    def get(self, request):
        return render(
            request, 'recruitment/about_us.html'
        )


def custom_handler404(request, exception=None):
    return HttpResponseNotFound('Ой, кажется запроссили не существующию страницу!')


def custom_handler500(request):
    return HttpResponseServerError('Server error')


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/'
    template_name = 'recruitment/signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'recruitment/login.html'
