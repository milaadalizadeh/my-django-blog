
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf.urls.static import static  #important and added from djangoproject sit for img static files
from django.conf import settings  #important and added from djangoproject sit for img static files
from . import views
from Accounts.views import Login, Register, activate
from payment.views import send_request, verify

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('',views.home,name='home'),
#    path('ghaleb/',include('ghaleb.urls')),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
#    path('emailVerification/<uidb64>/<token>', views.activate, name='emailActivate'),
    path('comment/', include('comment.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('',include('django.contrib.auth.urls')),               #میره از خود جنگو کد های لازم برای ورود خروج تنظیم رمز و ... برام  میاره
    path('',include('myblog.urls')),
    path('Accounts/',include('Accounts.urls')),
    path('request/', send_request, name='request'),
    path('verify/', verify , name='verify'),


]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
