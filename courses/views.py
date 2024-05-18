from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .form import RegistrationForm , LoginForm , CourseForm , AddToRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Course, CourseSchedule ,Registration , Student ,Notification


def home(request):
    return render(request, 'home.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            student = Student(username=username, email=email, password=password)
            student.save()
            messages.success(request, "Sign up successful. You can now log in.")

            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']  
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)  
            if user is not None:
                login(request, user)
                return redirect('search')  
            else:
                messages.error(request, "Invalid email or password")
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def search_courses(request):
    query = request.GET.get('query', '')
    search_results = None
    if query:
        search_results = Course.objects.filter(
            course_code__icontains=query
        ) | Course.objects.filter(
            course_name__icontains=query
        ) | Course.objects.filter(
            instructor_name__icontains=query
        )
        
    search_details = ""
    if search_results:
        for result in search_results:
            search_details += f"Course Code: {result.course_code}\n"
            search_details += f"Course Name: {result.course_name}\n"
            search_details += f"Description: {result.description}\n"
            search_details += f"Instructor Name: {result.instructor_name}\n"
            search_details += f"Prerequisites: {result.prerequisites}\n"
            search_details += f"Capacity: {result.capacity}\n\n"

    return render(request, 'search.html', {'search_details': search_details})


def course_schedule(request):
    user_id=request.user.id
    courses = Course.objects.all()
    course_schedule = CourseSchedule.objects.all() 
    student = Student.objects.get(id=user_id)  
    registrations = Registration.objects.filter(student=student)
    
    course_data = []
    for registration in registrations:
        course = registration.course
        schedule = course_schedule.filter(course=course)
        course_data.append({'course': course, 'schedule': schedule})

    context = {
        'course_data': course_data
    }
    return render(request, 'schedule.html', context)



def course_details(request):
    user_id = request.user.id
    courses = Course.objects.all()
    course_schedule = CourseSchedule.objects.all() 
    completed_course_ids = Registration.objects.filter(student_id=user_id).values_list('course_id', flat=True)  
    course_data = []
    for course in courses:
        if completed_course_ids or course.prerequisites == "None":
            schedule = course_schedule.filter(course=course) 
            num_registered_students = Registration.objects.filter(course=course).count()
            capacity_fraction = f"{num_registered_students}/{course.capacity}"
            
            course_data.append({'course': course, 'schedule': schedule, 'capacity_fraction': capacity_fraction})

    context = {
        'course_data': course_data
    }
    return render(request, 'Regestration.html', context)


def add_to_registration(request):
    course_choices = Course.objects.all()  # Get all courses for the form
    if request.method == 'POST':
        form = AddToRegistrationForm(request.POST, course_choices=course_choices)
        if form.is_valid():
            selected_courses = form.cleaned_data['selected_courses']
            user_id = request.user.id
            try:
                for course in selected_courses:
                    num_registered_students = Registration.objects.filter(course=course).count()
                    capacity_fraction = course.capacity - num_registered_students
                    if not Registration.objects.filter(student_id=user_id, course=course).exists() and capacity_fraction != 0:
                        Registration.objects.create(student_id=user_id, course=course)
                        messages.success(request, f"Course {course.course_code} added successfully.")
                        # Trigger notification here
                        message = f"You have added a course to your registration."
                        Notification.objects.create(user=request.user, message=message)
                    else:
                        messages.error(request, f"Course {course.course_code} is already in your schedule.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            form = AddToRegistrationForm(course_choices=course_choices)
    return redirect('coursedetails')


def all_courses(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('courses')
    else:
        form = CourseForm()
    return render(request, 'add_course.html', {'form': form})

def delete_courses(request):
    if request.method == 'POST':
        selected_course_ids = request.POST.getlist('selected_courses')
        Course.objects.filter(course_code__in=selected_course_ids).delete()
    return redirect('courses')



# views.py

from django.http import JsonResponse
from .models import Notification

def get_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user)
        serialized_notifications = [{'message': notification.message} for notification in notifications]
        return JsonResponse(serialized_notifications, safe=False)
    else:
        return JsonResponse([], safe=False)  # Return empty array if user is not authenticated
