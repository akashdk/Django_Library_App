from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth.views import login,logout

# Use include() to add URLS from the catalog application and authentication system
from django.conf.urls import include


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]



urlpatterns += [
    url(r'^catalog/', include('catalog.urls')),
]


# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    url(r'^$', RedirectView.as_view(url='/catalog/', permanent=True)),
]




#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    url('^accounts/', include('catalog.urls')),

]

