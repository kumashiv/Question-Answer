
from django.urls import path

from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.index, name = 'index'),



    path('question/<int:question_id>/', views.QuestionDetail, name = 'question-detail'),
    path('question/create/', views.QuestionCreate.as_view(), name='question-create'),

    path('question/<int:question_id>/update', views.QuestionUpdate.as_view(), name = 'question-update'),
    path('question/<int:question_id>/delete', views.QuestionDelete.as_view(), name = 'question-delete'),

    path('question/<int:question_id>/save-comment/', views.save_comment, name = 'save-comment'),
    # path('save-comment/', views.save_comment, name = 'save-comment'),


    path('question/<int:question_id>/save-like/', views.save_like, name = 'save-like'),

    path('account', views.account, name = 'account'),

    path('main/', views.QuestionListView.as_view(), name = 'main-view'),
]
