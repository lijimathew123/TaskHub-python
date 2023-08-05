
from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from .forms import TaskForm
from .forms import EmployeeRegistrationForm,EmployeeProfileForm,GroupForm,TaskForm,TaskNoteForm
from .models import Employee,Task,Group,Activity,TaskNote
from django.contrib.auth import logout
from django.db.models import Prefetch


def index(request):
    return render(request, 'index.html')


def register_employee(request):
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login_employee')
    else:
        form = EmployeeRegistrationForm()

    return render(request, 'register.html', {'form': form})



#login credentials
def login_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Retrieve the employee from the database based on the username
            employee = Employee.objects.get(username=username)

            # Compare the password with the one stored in the database
            if employee.password == password:
                # Set the employee ID in the session to mark as authenticated
                request.session['employee_id'] = employee.id

                # Redirect to the profile page
                return redirect('view_profile')
            else:
                # Passwords don't match, set an error message
                error_message = 'Invalid username or password'
        except Employee.DoesNotExist:
            # Employee with the given username doesn't exist, set an error message
            error_message = 'Invalid username or password'
    else:
        # GET request, initialize the error message
        error_message = ''

    return render(request, 'login.html', {'error_message': error_message})

# view profile section
def view_profile(request):
    if 'employee_id' in request.session:
        # Retrieve the employee object using the stored ID
        employee_id = request.session['employee_id']
        try:
            employee = Employee.objects.get(id=employee_id)
            return render(request, 'view_profile.html', {'employee': employee})
        except Employee.DoesNotExist:
            # Employee with the stored ID doesn't exist, redirect to login
            return redirect('login_employee')
    else:
        # Redirect to the login page if not authenticated
        return redirect('login_employee')


   
#update profile
def update_profile(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        # Redirect or show an error message if employee with given ID doesn't exist
        return redirect('view_profile')

    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST,request.FILES, instance=employee)

        if form.is_valid():
            form.save()

            # Create an activity for profile update
            activity = Activity(title='Profile Updated', description=f'{employee.name} updated their profile.')
            activity.save()

            return redirect('view_profile')
    else:
        form = EmployeeProfileForm(instance=employee)

    return render(request, 'update_profile.html', {'form': form, 'employee': employee})



#logout profile
def logout_employee(request):
    logout(request)
    return redirect('login_employee')



# view for create team for a project

def create_group(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == 'POST':
        form = GroupForm(request.POST)
        
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = employee  # Set the creator of the group
            group.save()

            # Create an activity for group creation
            activity = Activity(title='Group Created', description=f'A new group named {group.name} was created by {employee.name}.')
            activity.save()

            selected_developers = form.cleaned_data['developers']
            group.developers.set(selected_developers)
            group.save()

            return redirect('group_detail', group_id=group.id, employee_id=employee.id)

        else:
            print(form.errors)
    else:
        form = GroupForm()

    developers = Employee.objects.filter(role='Project Developer')

    # Calculate the availability status for each developer
    for developer in developers:
        tasks_in_progress = Task.objects.filter(assigned_to=developer, status__in=['In Progress', 'Started'])
        if tasks_in_progress.exists():
            developer.availability = 'Busy'
        else:
            developer.availability = 'Available'

    return render(request, 'create_group.html', {'form': form, 'developers': developers, 'employee': employee})





def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('task_list')  # Redirect to the task list page after successful task creation
    else:
        form = TaskForm()
    
    return render(request, 'create_task.html', {'form': form})


# display group items

def group_detail(request, group_id, employee_id):
    group = get_object_or_404(Group, id=group_id)
    employee = get_object_or_404(Employee, id=employee_id)
    developers = Employee.objects.filter(role='Project Developer')
    return render(request, 'group_detail.html', {'group': group, 'employee': employee,'developers':developers})


#delete current  group
def delete_group(request, group_id,employee_id):
    group = get_object_or_404(Group, id=group_id)
    
    employee = get_object_or_404(Employee, id=employee_id)
    # Create an activity for group deletion
    activity = Activity(title='Group Deleted', description=f'The group "{group.name}" was deleted by {employee.name}.')
    activity.save()

    group.delete()


    return redirect('view_profile')



#remove a member from a group
def remove_member(request, group_id, developer_id):
    group = get_object_or_404(Group, id=group_id)
    developer = get_object_or_404(Employee, id=developer_id)
    group.developers.remove(developer)
    return redirect('group_detail', group_id=group_id,employee_id=group.creator.id)


#add member to the group
def add_member(request, group_id,employee_id):
    if request.method == 'POST':
        group = get_object_or_404(Group, id=group_id)
        employee = get_object_or_404(Employee,id = employee_id)
        developer_id = request.POST.get('developer')
        if developer_id:
            developer = get_object_or_404(Employee, id=developer_id)
            group.developers.add(developer)

            # Create an activity for adding a member to the group
            activity = Activity(
                title='Member Added',
                description=f'{employee.name} added {developer.name} to the group "{group.name}".'
            )
            activity.save()

            return redirect('group_detail', group_id=group_id, employee_id=group.creator.id)

    return redirect('group_detail', group_id=group_id, employee_id=group.creator.id)


#Assign task by project manager
def assign_task(request,employee_id):
    project_manager = Employee.objects.get(id=employee_id)
    groups = Group.objects.all()
    developers = Employee.objects.filter(role='Project Developer')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            
            # Create an activity for assigning the task by the project manager
            group_name = task.group.name if task.group else "No Group"
            developer_name = task.assigned_to if task.assigned_to else "Unassigned"
            activity = Activity(
                title='Task Assigned',
                description=f'A new task "{task.title}" was assigned to {developer_name} in the group "{group_name}" by {project_manager.name}.'
            )
            activity.save()
            
           
            
            group_id = form.cleaned_data['group'].id
            return redirect('task_list', group_id=group_id,employee_id = employee_id)
        else:
            print(form.errors)
    else:
        form = TaskForm()

    return render(request, 'assign_task.html', {'form': form, 'groups': groups, 'developers': developers})



# list out task details of current group
def task_list(request, group_id,employee_id):
    group = get_object_or_404(Group, id=group_id)
    employee =get_object_or_404(Employee,id=employee_id)
    tasks = Task.objects.filter(group=group)

    return render(request, 'task_list.html', {'group': group, 'tasks': tasks,'employee':employee})


#edit task
from django.utils import timezone
def edit_task(request, task_id,employee_id):
    
    project_manager = Employee.objects.get(id=employee_id)
    developers = Employee.objects.filter(role='Project Developer')
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        

            # Create an activity for editing the task by the project manager
            group_name = task.group.name if task.group else "No Group"
            
            activity = Activity(
                title='Task Edited',
                description=f'Task "{task.title}" in the group "{group_name}" was edited by {project_manager.name}.',
                date=timezone.now()  # Set the activity creation date to the current time
            )
            activity.save()
            return redirect('task_list', group_id=task.group.id,employee_id=employee_id)
        else:
            print(form.errors)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'edit_task.html', {'form': form, 'task': task,'developers':developers})




#view for my task details by project developer
def my_tasks(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        tasks = Task.objects.filter(assigned_to=employee)

        return render(request, 'my_task.html', {'employee': employee, 'tasks': tasks})
    except Employee.DoesNotExist:
        return redirect('login_employee')


     
#view my groups by project developer
def my_groups(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        groups = Group.objects.filter(developers=employee)
        return render(request, 'my_group.html', {'employee': employee, 'groups': groups})
    except Employee.DoesNotExist:
        # Employee with the given ID doesn't exist
        return redirect('login_employee')
    

    
#update task status view from the side of  project developer
def update_task(request, employee_id, task_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        task = Task.objects.get(id=task_id)

        if request.method == 'POST':
            status = request.POST.get('status')

            # Update the task status
            task.status = status
            task.save()

            return redirect('my_tasks', employee_id=employee_id)

        return render(request, 'update_task.html', {'employee': employee,'task': task})
    except (Employee.DoesNotExist, Task.DoesNotExist):
        return redirect('login_employee')


#project manager see his group details



def view_group(request, employee_id):
    try:
        project_manager = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return HttpResponse("Invalid Employee ID")

    groups = Group.objects.filter(creator=project_manager).order_by('-created_at')

    # Prefetch related developers and tasks to reduce database queries
    groups = groups.prefetch_related(
        Prefetch('developers', queryset=Employee.objects.filter(role='Project Developer')),
        Prefetch('developers__task_set', queryset=Task.objects.filter(group__creator=project_manager))
    )

    return render(request, 'view_group.html', {'groups': groups, 'project_manager': project_manager})


def delete_group_from_list(request, group_id, project_manager_id):
    group = get_object_or_404(Group, id=group_id)
    employee = Employee.objects.get(id=project_manager_id)
    
    # Create an activity for group deletion
    activity = Activity(title='Group Deleted', description=f'The group "{group.name}" was deleted by {employee.name}.')
    activity.save()

    group.delete()
    return redirect('view_group', employee_id=project_manager_id)


def delete_member_from_grouplist(request, group_id, developer_id, project_manager_id):
    group = get_object_or_404(Group, id=group_id)
    developer = get_object_or_404(Employee, id=developer_id)
    employee = Employee.objects.get(id=project_manager_id)

    group.developers.remove(developer)
    
    # Create an activity for removing a member from the group
    activity = Activity(
        title='Member Removed',
        description=f'{developer.name} ({developer.email}) was removed from the group "{group.name}" by {employee.name}.'
    )
    activity.save()

    return redirect('view_group', employee_id=project_manager_id)



   
#track activity of project manager
def track_activity(request, employee_id):
    try:
        project_manager = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        # Redirect or show an error message if employee with given ID doesn't exist
        return redirect('view_profile')

    # Get activities related to the project manager
    activities = Activity.objects.filter(description__contains=project_manager.name).order_by('-date')

    return render(request, 'track_activity.html', {'activities': activities})

#view all members in the system
def view_project_developers(request):
    employee = Employee.objects.all()
    return render(request, 'view_project_developers.html', {'employee': employee})

# Delete my account 
def delete_account(request, employee_id):
    
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
       
        employee.delete()

        
        return redirect('index')  # Replace 'home' with the name of the URL pattern for the homepage.

    
    return render(request, 'index.html')


def add_task_note(request, employee_id, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        note_text = request.POST.get('note')
        TaskNote.objects.create(task=task, note=note_text)
        return redirect('my_tasks', employee_id=employee_id)

def view_task_notes(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        notes = TaskNote.objects.filter(task=task).order_by('-id')
    except Task.DoesNotExist:
        # Handle the case when the task with the given ID does not exist
        return redirect('task_list', employee_id=15)  # Change 15 to your desired employee ID

    return render(request, 'view_task_notes.html', {'task': task, 'notes': notes})


def view_team_member_note(request, group_id):
    group = Group.objects.get(id=group_id)
    team_members = group.developers.all()
    return render(request, 'view_team_member_note.html', {'group': group, 'team_members': team_members})