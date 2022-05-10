from django.urls import path
from . import views
from django.contrib import admin
from . import models
from .views import (
post, category, ArticleList, AuthorList, ArticlePreview, SearchList
)  #dar halate avale view byad myblog ro dar inja import mikardim
app_name='myblog'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ArticleList.as_view(),name='myblog'),
    path('page/<int:page>', ArticleList.as_view(),name='myblog'),
    path('post/<slug:slug>',views.post,name='post'),
    path('preview/<int:pk>', ArticlePreview.as_view(),name='preview'),
    path('category/<slug:slug>',views.category,name='category'),
    path('category/<slug:slug>/page/<int:page>',views.category,name='category'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name='author'),
    path('search/', SearchList.as_view(), name='search'),
    path('search/page/<int:page>', SearchList.as_view(), name='search'),


#    path('ghaleb',include('Accounts.urls')),
]
