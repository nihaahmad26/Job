from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path("jobs", views.show_all),
    path("jobs/page", views.show_page),
    path("jobs/create", views.add_job),
    # path("users/<int:user_id>", views.count),
    path("jobs/<int:job_id>", views.show_one),
    path("jobs/<int:job_id>/update", views.update),
    path("jobs/<int:job_id>/delete", views.delete),
    path("favorite/<int:job_id>", views.favorite),
    path("unfavorite/<int:job_id>", views.unfavorite),
    path('logout', views.logout),
    path('success', views.success)
]