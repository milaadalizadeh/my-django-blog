from django.views.generic import ListView , DetailView
from Accounts.models import User
from django.shortcuts import render ,get_object_or_404
from . import models
from .models import Article, Category
from django.core.paginator import Paginator
from Accounts.mixins import AuthorAccessMixin
from django.db.models import Q
# Create your views here.

#def myblog(request, page=1):
#    articles_list = Article.objects.published()
#    paginator = Paginator(articles_list, 5) # Show 25 contacts per page.
#    article= paginator.get_page(page)
#    context= {
#             'article': article
#    }                                           #az managere publish estefade kardim : article.objects.published
    #category=models.Category.objects.all()
#    return render(request,'myblog/index.html', context)
class ArticleList(ListView):
#    model = Article                                    #kolli hast va lazem nist
    queryset = Article.objects.published()
#    template_name = 'myblog/index.html'               #ya bayad vase template injuri adress bedim ya khodesh mire article_list.html ro mikhune
    context_object_name = 'article'   # ino khodam dadam ta majbut be taghyire article be page_obj nabasham
    paginate_by = 5


# Create your views here.
def post(request, slug):
    context={
         "article": get_object_or_404(Article, slug=slug, status='p'),           # ya benevisam Article.objects.published(), slug=slug ham mishe
    }
    article = get_object_or_404(Article, slug=slug, status='p')
    #article=models.Article.objects.all()

    ip_address = request.user.ip_address
    if ip_address not in article.hits.all():
        article.hits.add(ip_address)



    return render(request, 'myblog/post.html', context)

class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)
    template_name = 'myblog/post.html'



def category(request, slug, page=1):
    category= get_object_or_404(Category, slug=slug, status=True)
    article_list= category.article.published()
    paginator = Paginator(article_list, 4) # Show 25 contacts per page.
    article= paginator.get_page(page)
    context={
            'article': article,
            'category': category,
            'page_obj': article,
    }

    return render(request, 'myblog/category.html', context)


class AuthorList(ListView):
    paginate_by = 5
    template_name ='myblog/author_list.html'
    context_object_name = 'article'  # ino mesle list view balayi khodam dadam ta majbur be taghyire article be page_obj nabasham
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.article.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author']= author
        return context


class SearchList(ListView):
    paginate_by = 5
    template_name ='myblog/search_list.html'
    context_object_name = 'article'
    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))   #اول بدون کیو نوشته بودیم وجواب  یداد حالا چون میخواستیم جستجو در تایتل رو هم بهش اضافه کنم از کیو استفاده کردیم  وقبلشکیو رو امپورت کردم و علا مت پایپ به معنای یا هست

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search']= self.request.GET.get('q')
        return context
