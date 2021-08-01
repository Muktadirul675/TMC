from django.urls import path
from . import views
from TMC2 import settings
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tmc'

urlpatterns = [
    path('', views.home,name="home"),
    path('about/', views.about,name="about"),
    path('problemset/',views.problem_set,name="problem_set"),
    path('problemset/problem/<int:pk>/',views.problem,name="problem"),
    path('profile/',views.profile,name="profile"),
    path('profile/<str:username>/',views.other_profile,name="other_profile"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('topic_problems/<str:topic>/<int:num>/',views.topic_probelm_set,name="topic_problems"),
    path('problemset/problem/add_problem', views.add_problem, name="add_problem"),
    path('leaderboard/', views.leaderboard, name="leaderboard"),
    path('user_registration/', views.user_registration, name="user_registration"),
    path('forgot_password/<str:email>/<str:otp>/',views.forgot_password, name="forgot_password"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



