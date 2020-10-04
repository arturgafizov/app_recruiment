"""app_recruitment_new URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from recruitment.views import custom_handler404, custom_handler500
from recruitment.views import MainView, VacanciesView, SpecialtyView, CardCompanyView, VacancyView, SentApplicationView
from recruitment.views import MyLoginView, MySignupView, MycompanyView, CompanyOutView, CompanyCreateView
from recruitment.views import VacancyEditView, MyresumeView, VacancyUpdateView, SearchView, ResumeEditView, SentView
from recruitment.views import CompanyVacancyView, ListVacanciesView, AboutUsView, ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('mycompany/vacancies/', VacanciesView.as_view()),
    path('mycompany/vacancies/vacancy_edit/', VacancyEditView.as_view()),
    path('mycompany/vacancies/<int:vacancy_update>/', VacancyUpdateView.as_view()),
    path('vacancies/<str:code>/', SpecialtyView.as_view()),
    path('list_vacancies', ListVacanciesView.as_view()),
    path('company_vacancies/<int:company_id>', CompanyVacancyView.as_view()),
    path('company/<int:company_id>/', CardCompanyView.as_view()),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view()),
    path('vacancies/<int:vacancy_id>/send', SentApplicationView.as_view()),
    path('mycompany/mycompany', CompanyOutView.as_view()),
    path('mycompany/company_create/', CompanyCreateView.as_view()),
    path('mycompany/', MycompanyView.as_view()),
    path('mycompany/myresume/', MyresumeView.as_view()),
    path('mycompany/myresume/resume_edit', ResumeEditView.as_view()),
    path('sent', SentView.as_view()),
    path('profile', ProfileView.as_view()),
    path('about_us', AboutUsView.as_view()),
    path('search/', SearchView.as_view()),
    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view()),
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
