from django.urls import path
from app import views
from .views import CourseListAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
  path('', views.home, name='home'),
  path('course-detail/<int:id>', views.course_detail, name='course_detail'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('courses/', views.course, name='course'),
  path('courses/<slug:data>', views.course, name='course_semister'),
  path('about/', views.about, name='about'),
  
  path('accounts/login/', views.Login_view.as_view(), name='login'),
  path('register/', views.Register.as_view(), name='register'),
  path('logout/', views.custom_logout, name='logout'),
  path('api/courses/', CourseListAPIView.as_view(), name='course-list-api'),
  path( 'password-change/', auth_views.PasswordChangeView.as_view( template_name='password_change.html', success_url='/password-change/done/'),name='password_change'),
    path( 'password-change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html' ),name='password_change_done' ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)