from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from .models import Notes,Homework
from youtubesearchpython import VideosSearch
from django.contrib.auth.decorators import login_required

from django.contrib.auth import logout as auth_logout


import  requests 
import wikipedia
from .forms import *

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')
@login_required
def notes_list(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, 
                title=request.POST['title'], 
                description=request.POST['description']
            )
            notes.save()
            
            messages.success(request, f'Notes added by {request.user.username} successfully!') 
            form = NotesForm()  # Clear the form after saving
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)
@login_required
def delete_note(request, pk):
    note = get_object_or_404(Notes, pk=pk)  # Retrieve the note or return 404 if not found
    note.delete()  # Call delete() on the retrieved note
    messages.success(request, 'Note successfully deleted.')
    return redirect('notes_list')

class NoteDetailView(generic.DetailView):
    model = Notes

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            # Handle the 'is_finished' checkbox more safely
            finished = request.POST.get('is_finished', 'off') == 'on'

            homeworks = Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request, f'Homework added by {request.user.username}!')
    else:
        form = HomeworkForm()

    homeworks = Homework.objects.filter(user=request.user)
    
    homework_done = len(homeworks) == 0

    context = {'homeworks': homeworks, 'homework_done': homework_done, 'form': form}
    return render(request, 'dashboard/homework.html', context)

@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
        messages.success(request, f'Home Work Is Still Pending!')

    else:
        homework.is_finished=True
        messages.success(request, f'Home Work Is Finished Now!')

    homework.save()

    return   redirect('homework')      

@login_required
def delete_homework(request,pk=None):
    homework=Homework.objects.get(id=pk).delete()
    messages.success(request, f'Home Work Deleted Success!')

    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                # Perform YouTube search
                video = VideosSearch(text, limit=10)
                result_list = []
                for i in video.result().get('result', []):
                    result_dictionary = {
                        'input': text,
                        'title': i.get('title'),
                        'duration': i.get('duration'),
                        'thumbnail': i.get('thumbnails')[0].get('url') if i.get('thumbnails') else '',
                        'channel': i.get('channel').get('name'),
                        'link': i.get('link'),
                        'views': i.get('viewCount').get('short'),
                        'published': i.get('publishedTime'),
                    }
                    desc = ''
                    if i.get('descriptionSnippet'):
                        for j in i['descriptionSnippet']:
                            desc += j['text']
                    result_dictionary['description'] = desc
                    result_list.append(result_dictionary)

                context = {'form': form, 'results': result_list}
                return render(request, 'dashboard/youtube.html', context)
            
            except Exception as e:
                # Catch and display the error message
                print(f"Error occurred: {e}")
                context = {'form': form, 'error_message': "An error occurred while fetching the videos. Please try again later."}
                return render(request, 'dashboard/youtube.html', context)

    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            finished = request.POST.get('is_finished') == 'on'  # Simplified way to handle checkbox

            todos = Todo(
                user=request.user,
                title=form.cleaned_data['title'],
                day=form.cleaned_data['day'],
                time=form.cleaned_data['time'],
                place=form.cleaned_data['place'],
                is_finished=finished
            )
            todos.save()
            messages.success(request, f'New Todo List Added by {request.user.username}')
            return redirect('todo')  # Redirect to avoid re-posting

    else:
        form = TodoForm()
    
    todo_list = Todo.objects.filter(user=request.user)
    todos_done = not todo_list.exists()  # Check if there are no todos
    
    context = {
        'todos': todo_list,
        'form': form,
        'todos_done': todos_done,
    }
    return render(request, 'dashboard/todo.html', context)
@login_required
def update_todo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished==True:
        todo.is_finished=False

    else:
        todo.is_finished=True
    todo.save()
    messages.info(request,f'This Todo {todo.title} Have Finished Well!!')
    return redirect('todo')    
@login_required
def delete_todo(request,pk=None):
    todo=Todo.objects.filter(id=pk).delete()
    messages.info(request,f'Todo Have Deleted Success!!')
    return redirect('todo')


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            try:
                # Perform Books search
                url = f"https://www.googleapis.com/books/v1/volumes?q={text}"
                r = requests.get(url)
                r.raise_for_status()  # Raise an exception for HTTP errors
                answer = r.json()
                result_list = []

                for item in answer.get('items', [])[:10]:
                    volume_info = item.get('volumeInfo', {})
                    result_dictionary = {
                        'title': volume_info.get('title', 'N/A'),
                        'subtitle': volume_info.get('subtitle', 'N/A'),
                        'description': volume_info.get('description', 'N/A'),
                        'count': volume_info.get('pageCount', 'N/A'),
                        'categories': volume_info.get('categories', []),
                        'rating': volume_info.get('averageRating', 'N/A'),
                        'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'N/A'),
                        'preview': volume_info.get('previewLink', 'N/A'),
                    }
                    
                    result_list.append(result_dictionary)

                context = {'form': form, 'results': result_list}
                return render(request, 'dashboard/books.html', context)
            
            except requests.RequestException as e:
                # Catch and display the error message
                print(f"Error occurred: {e}")
                context = {'form': form, 'error_message': "An error occurred while fetching the books. Please try again later."}
                return render(request, 'dashboard/books.html', context)

    else:
        form = DashboardForm()

    context = {'form': form}
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text', '')  # Use get() with a default value
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{text}"
        
        try:
            # Make the API request
            r = requests.get(url)
            r.raise_for_status()  # Raise an error for HTTP request failures
            answer = r.json()
            
            # Extract data from the JSON response
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0].get('example', 'No example available')
            synonyms = answer[0]['meanings'][0]['definitions'][0].get('synonyms', 'No synonyms available')
            
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,  
                'example': example,
                'synonyms': synonyms
            }
        except (requests.exceptions.RequestException, KeyError, IndexError) as e:
            # Handle exceptions and provide a user-friendly message
            context = {
                'form': form,
                'input': text,
                'error': 'An error occurred while fetching the data. Please try again.'
            }
            # Log the error message if needed (for debugging)
            print(f"Error: {e}")

        return render(request, 'dashboard/dictionary.html', context)
    
    else:
        form = DashboardForm()
        context = {'form': form}

    return render(request, 'dashboard/dictionary.html', context)



def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST.get('text')
        
        if text:
            try:
                # Search Wikipedia and get a list of results
                search_results = wikipedia.search(text, results=10)  # Fetch up to 10 results
                
                articles = []
                for result in search_results:
                    try:
                        page = wikipedia.page(result)
                        image_url = page.images[0] if page.images else None
                        articles.append({
                            'title': page.title,
                            'link': page.url,
                            'details': page.summary,
                            'image_url': image_url
                        })
                    except wikipedia.PageError:
                        continue  # Skip any pages that result in a PageError
                
                context = {
                    'form': form,
                    'articles': articles  # Pass the list of articles to the template
                }
            except Exception as e:
                context = {
                    'form': form,
                    'error': str(e)
                }
        else:
            context = {
                'form': form,
                'error': 'Please enter a search term.'
            }
        
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
        return render(request, 'dashboard/wiki.html', context)
    

def conversion(request):
    if request.method == 'POST':
        form = ConversionForm()
        measurement_type = request.POST['measurement']
        
        if measurement_type == 'length':
            measurement_form = ConversionLengthForm()
        elif measurement_type == 'mass':
            measurement_form = ConversionMassForm()
        else:
            # Add other measurement forms here
            measurement_form = None

        context = {
            'form': form,
            'm_form': measurement_form,
            'input': True
        }

        if 'input' in request.POST:
            first = request.POST['measure1']
            second = request.POST['measure2']
            input_value = request.POST['input']
            answer = None

            if input_value and int(input_value) >= 0:
                if measurement_type == 'length':
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {int(input_value) * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {int(input_value) / 3} yard'
                elif measurement_type == 'mass':
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
                # Add other conversion logic here

            context['answer'] = answer

    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }

    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')  # Redirect after successful registration
    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/register.html', context)
@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False  

    if len(todos)==0:
       todos_done=True
    else:
       todos_done=False  

    context={
        'homeworks':homeworks,
        'todos':todos,
       'homework_done':homework_done,
       'todos_done':todos_done,
    }        

    return render(request,'dashboard/profile.html',context)

@login_required
def logout(request):
    auth_logout(request)  # Kill the session
    return render(request, 'dashboard/logout.html')  # Redirect to logout page