from django.urls import path
from AppOne import views
app_name = 'AppOne'

urlpatterns = [
    path('',views.user_login,name='user_login'),
    path('register',views.register,name='register'),
    path('child_managment',views.child_managment,name='child_managment'),
    path('child_grades',views.child_grades,name='child_grades'),
    path('list_of_students',views.list_of_students,name='list_of_students'),
    path('raport',views.raport,name='raport'),
    path('start_page_parent',views.start_page_parent,name='start_page_parent'),
    path('start_page_teacher',views.start_page_teacher,name='start_page_teacher'),
    path('task_managment',views.task_managment,name='task_managment'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('student_marks/<int:pk>/',views.student_marks,name='student_marks'),
    path('edit_student_marks/<int:pk>/',views.edit_student_marks,name='edit_student_marks'),
]
