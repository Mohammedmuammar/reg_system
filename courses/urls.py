# In urls.py

from django.urls import path
from .views import home,signup ,login_view ,search_courses,logout_view,course_details 
from .views import all_courses, course_schedule,add_to_registration , delete_courses ,add_course ,get_notifications

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('search/', search_courses, name='search'),
    path('logout/', logout_view, name='logout'),
    path('courses/', all_courses, name='courses'),
    path('course_schedule/', course_schedule, name='course_schedule'),
    path('coursedetails/', course_details, name='coursedetails'),
    path('add-to-registration/', add_to_registration, name='add_to_registration'),
    path('add-course/', add_course, name='add_course'),
    path('delete-courses/',delete_courses, name='delete_courses'),
    path('get-notifications/', get_notifications, name='get_notifications'),
    
]
