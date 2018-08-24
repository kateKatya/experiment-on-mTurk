from django.urls import path

from . import views

app_name = 'mcmcgraphs'

urlpatterns = [
    path('', views.index, name='index'),
    path('amt/', views.catch_amt, name='catch_amt'),
    path('instr/', views.instructions, name='instructions'),
    path('instructions/', views.show_instructions, name='show_instructions'),
    path('try/', views.trials, name='trials'),
    path('trials/', views.show_trials, name='show_trials'),
    path('vote/', views.vote, name='vote')
]

