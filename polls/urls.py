from django.urls import path
from . import views
from .views import QuestionCreateView, QuestionUpdateView, QuestionDeleteView,QuestionDetailView, PollsListView


urlpatterns = [
    path('', PollsListView.as_view(), name="list"),
    path('update/<slug:pk>/', QuestionUpdateView.as_view(), name="polls-update"),
    path('newquestion/', QuestionCreateView.as_view(), name='polls-create'),
    path('delete/<slug:pk>/', QuestionDeleteView.as_view(), name="polls-delete"),
    path('detail/<int:question_id>/', QuestionDetailView, name="polls-detail"),
    path('userposts/<int:id>/', views.user_detail, name="users-detail"),
    path('vote/<int:id>/', views.vote, name="polls-vote"),
]
