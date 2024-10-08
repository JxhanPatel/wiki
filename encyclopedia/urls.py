from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry_page, name="entry"),
    path("search/", views.search, name="search"),
    path("new", views.new, name="new"),
    path('wiki/<str:title>/edit/', views.edit, name='edit'),
    path("random", views.randomm, name="random"),
    path("wiki/<str:title>/delete/", views.delete_entry, name="delete")
]
