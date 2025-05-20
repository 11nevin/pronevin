from django.contrib import admin
from django.urls import path
from summary import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('userregistration', views.userregistration),
    path('login', views.login),
    path('userhome', views.userhome),
    path('adminhome', views.adminhome),
    path('videosummary', views.videosummary),
    path('textsummary', views.textsummary),
    path('user_video_history', views.user_video_history),
    path('user_profile', views.user_profile),
    path('deleteuserprofile', views.deleteuserprofile),
    path('admin_user', views.admin_user),
    path('admin_user_details', views.admin_user_details),
    path('admin_user_active', views.admin_user_active),
    path('admin_user_inactive', views.admin_user_inactive),
    path('user_feedback', views.user_feedback),
    path('admin_feedbacks', views.admin_feedbacks),
    path('user_premium', views.user_premium),
    path('admin_premium', views.admin_premium),
    path('admin_premium_delete', views.admin_premium_delete),
    path('news', views.newspage),
    path('likes', views.like),
    # NEW VOICE COMMAND ENDPOINTS
    path('voice_command/', views.voice_command, name='voice_command'),
    path('process_voice_command/', views.process_voice_command, name='process_voice_command'),
]
