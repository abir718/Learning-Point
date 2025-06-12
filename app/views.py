from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Course, CourseEnrollment,Class_video, Semsiter_Even_odd,Website_logo, Slider_model
from .serializers import CourseSerializer
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import UserSession
import datetime
from django.contrib.sessions.models import Session
from django_user_agents.utils import get_user_agent
from django.utils.timezone import now
from .models import UserSession, LoginLog 

# Create your views here.

def home(request):
    course = Course.objects.all()[:3]
    print(course)
    slider = Slider_model.objects.all()
    print(slider)
    return render(request, 'index.html', {'slider': slider, 'courses': course})

from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Course, CourseEnrollment, Class_video

def course_detail(request, id):
    today = timezone.now()
    enrolled = False

    if request.user.is_authenticated:
        user = request.user
        val = CourseEnrollment.objects.filter(user=user, course__id=id).first()
        
        if val is None:
            enrolled = False
        else:
            print(f"Today: {today}")
            print(f"Expired on: {val.expired_on}")
            if val.expired_on >= today:
                enrolled = True
            else:
                val.is_active = False
                val.save()
                enrolled = False

    course = get_object_or_404(Course, id=id)
    video = Class_video.objects.filter(course=course)

    return render(request, 'course-details.html', {
        'course': course,
        'enrolled': enrolled,
        'video': video
    })

def dashboard(request):
    return render(request, 'dashboard.html')

def course(request,data=None):
    if data is None:
        all = Course.objects.all()
    else:
        all = Course.objects.filter(semister=str(data))
    Even_odd = Semsiter_Even_odd.objects.all().first()
    return render(request, 'courses.html', {'all': all,"data":data, 'Even_odd': Even_odd})



def about(request):
    return render(request, 'about-us.html')

def footer(request):
    return render(request, 'footer.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not full_name or not email or not password or not confirm_password:
            return render(request, 'register.html', {'error': 'All fields are required.'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already taken.'})
        
        if len(password) < 8:
            return render(request, 'register.html', {'error': 'Password must be at least 8 characters long.'})
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error': 'Email already registered.'})

        user = User(username=username, first_name=full_name, email=email)
        user.set_password(password)
        user.save()

        return render(request, 'register.html', {'success': 'Registration successful.'})

class Login_view(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'Username and password are required.'})

        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()

        if user is None or not user.check_password(password):
            return render(request, 'login.html', {'error': 'Invalid username or password.'})

        try:
            user_session = UserSession.objects.get(user=user)
            session_exists = Session.objects.filter(session_key=user_session.session_key).exists()

            if session_exists:
                return render(request, 'login.html', {'error': 'Already logged in on another device.'})
            else:
                login(request, user)
                user_session.session_key = request.session.session_key
                user_session.save()
        except UserSession.DoesNotExist:
            login(request, user)
            UserSession.objects.create(user=user, session_key=request.session.session_key)

        # Track device and log info
        user_agent = get_user_agent(request)
        device_type = 'Mobile' if user_agent.is_mobile else 'Tablet' if user_agent.is_tablet else 'PC'
        os = user_agent.os.family
        browser = user_agent.browser.family
        ip = self.get_client_ip(request)

        # Optional: Save to LoginLog
        LoginLog.objects.create(
            user=user,
            ip_address=ip,
            device_type=device_type,
            os=os,
            browser=browser,
        )

        return redirect('home')

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
def custom_logout(request):
    logout(request)
    return redirect('login')

class CourseListAPIView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)