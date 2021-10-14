from django.shortcuts import render, redirect
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def get_showing_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'complete':
            todos = Todo.objects.filter(is_completed=True)
        elif request.GET.get('filter') == 'incomplete':
            todos = Todo.objects.filter(is_completed=False)
    return todos


@login_required
def index(request):
    todos= Todo.objects.filter(owner= request.user)
    completed = Todo.objects.filter(is_completed=True).count
    not_completed = Todo.objects.filter(is_completed=False).count
    context = { 'todos': get_showing_todos(request, todos),
                "all_count": todos.count,
                "completed": completed,
                "not_completed":not_completed,
            }
    return render(request, 'todo/index.html', context)


@login_required
def create_todo(request):
    form = TodoForm()
    context = {'form': form}
    if request.method == 'POST':
        title        = request.POST.get('title')
        description  = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        todo = Todo()
        todo.title        = title
        todo.description  = description
        todo.is_completed = True if is_completed=="on" else False
        todo.owner = request.user
        
        todo.save()
        messages.add_message(request, messages.SUCCESS, 'Task was created successfully')
        
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))  # reverse because we don't know the id
    return render(request, 'todo/create-todo.html', context)


@login_required
def todo_details(request,id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.owner != request.user:
        return redirect(reverse('home'))
    context = {'todo': todo}
    return render(request, 'todo/todo-details.html', context)


@login_required
def delete_todo(request,id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.owner != request.user:
        return redirect(reverse('home'))
    context = {'todo': todo,}
    
    if request.method == 'POST':
        todo.delete()
        messages.add_message(request, messages.SUCCESS, 'Task was deleted successfully')
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'todo/delete-todo.html', context)


@login_required
def edit_todo(request,id):
    todo = get_object_or_404(Todo, pk=id)
    if todo.owner != request.user:
        return redirect(reverse('home'))
    form = TodoForm(instance = todo)
    context = {'todo': todo, 'form': form}

    if request.method == 'POST':
        title        = request.POST.get('title')
        description  = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)
        
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        
        todo.save()
        messages.add_message(request, messages.SUCCESS, 'Task was edited successfully')
        
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    return render(request, 'todo/edit-todo.html', context)