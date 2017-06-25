from django.shortcuts import render, get_object_or_404
from django.utils import timezone 
import datetime
# Create your views here.
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from locallibrary import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm



def Login(request):
    next = request.GET.get('next','/catalog/books/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "registration/login.html", {'redirect_to': next})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/registor_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "registration/reg.html", {'user_form' : user_form} )




@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)




@login_required
def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
        
    # Render the HTML template index.html with the data in the context variable
    num_authors=Author.objects.count()  # The 'all()' is implied by default.
    
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors,
            'num_visits':num_visits}, # num_visits appended
    )







@method_decorator(login_required, name='dispatch')
class BookListView(generic.ListView):
        model = Book
      #  context_object_name = 'book_list'   # your own name for the list as a template variable



        def get_queryset(self):
            return Book.objects.all() # Get 5 books containing the title war
        def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
            context = super(BookListView, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
            context['some_data'] = 'This is just some data'
            return context
@method_decorator(login_required, name='dispatch')

class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request,pk):
        try:
            book_id=Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Book does not exist")

    #book_id=get_object_or_404(Book, pk=pk)
    
        return render(
        request,
        'catalog/book_detail.html',
        context={'book':book_id,}
    )

















