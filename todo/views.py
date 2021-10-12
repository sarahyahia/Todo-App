from django.shortcuts import render
from .forms import TodoForm
from .models import Todo
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse



def get_showing_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'complete':
            todos = Todo.objects.filter(is_completed=True)
        elif request.GET.get('filter') == 'incomplete':
            todos = Todo.objects.filter(is_completed=False)
    return todos



def index(request):
    todos= Todo.objects.all()
    completed = Todo.objects.filter(is_completed=True).count
    not_completed = Todo.objects.filter(is_completed=False).count
    context = { 'todos': get_showing_todos(request, todos),
                "all_count": todos.count,
                "completed": completed,
                "not_completed":not_completed,
            }
    return render(request, 'todo/index.html', context)



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
        
        todo.save()
        print(todo.id)
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))  # reverse because we don't know the id
    return render(request, 'todo/create-todo.html', context)



def todo_details(request,id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    return render(request, 'todo/todo-details.html', context)



def delete_todo(request,id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo,}
    
    if request.method == 'POST':
        todo.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request, 'todo/delete-todo.html', context)



def edit_todo(request,id):
    todo = get_object_or_404(Todo, pk=id)
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
        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))
    return render(request, 'todo/edit-todo.html', context)