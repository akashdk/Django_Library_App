from django.conf.urls import url
from . import views
from django.conf.urls import  url, include


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
  	url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
  	url(r'^login/$', views.Login, name='login'),
  	url(r'^logout/$', views.Logout ,name = 'logout'),
  	url(r'^register/$', views.register ,name = 'register'),  	
]