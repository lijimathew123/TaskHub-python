from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name = 'index'),
    path('register_employee/', views.register_employee, name='register_employee'),
    path('login_employee/',views.login_employee, name='login_employee'),
    path('profile/', views.view_profile, name='view_profile'),
    path('my_tasks/<int:employee_id>/',views.my_tasks, name='my_tasks'),
    path('update_task/<int:employee_id>/<int:task_id>/', views.update_task, name='update_task'),

    path('update_profile/<int:employee_id>/', views.update_profile, name='update_profile'),
    path('my_groups/<int:employee_id>/',views.my_groups, name='my_groups'),

    path('create_group/<int:employee_id>/', views.create_group, name='create_group'),
    path('group_detail/<int:group_id>/<int:employee_id>/', views.group_detail, name='group_detail'),
    path('delete_group/<int:group_id>/<int:employee_id>/', views.delete_group, name='delete_group'),
    path('remove_member/<int:group_id>/<int:developer_id>/', views.remove_member, name='remove_member'),
    path('add_member/<int:group_id>/<int:employee_id>/', views.add_member, name='add_member'),
    path('assign_task/<int:employee_id>/', views.assign_task, name='assign_task'),
    path('task_list/<int:group_id>/<int:employee_id>/', views.task_list, name='task_list'),
    path('edit_task/<int:task_id>/<int:employee_id>/', views.edit_task, name='edit_task'),
    #path('created_group',views.created_group, name='created_group'),
    path('view_group/<int:employee_id>/',views.view_group, name='view_group'),
    path('delete_member_from_grouplist/<int:group_id>/<int:developer_id>/<int:project_manager_id>/',views.delete_member_from_grouplist, name = 'delete_member_from_grouplist'),
    path('delete_group_from_list/<int:group_id>/<int:project_manager_id>/',views.delete_group_from_list, name='delete_group_from_list'),
    path('track_activity/<int:employee_id>/', views.track_activity, name ='track_activity'),
    path('view_project_developers',views.view_project_developers,name='view_project_developers'),
    path('delete_account/<int:employee_id>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_employee, name='logout_employee'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)