from django.db import models
from django.urls import reverse
from Accounts.models import User
from django.utils import timezone
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


#  my managers
class ArticleManager(models.Manager):                                          # vagti magaleyi ro draft mikardim bazam neshun midad hala ba in dastur va adamsh tu payin (objects=...) khodesh draft shode haro az safhe hazf mikone
    def published(self):
        return self.filter(status='p')

class CategoryManager(models.Manager):            #dige cat.children.all nminevisim bjash cat.children.active neveshtim                              # vagti magaleyi ro draft mikardim bazam neshun midad hala ba in dastur va adamsh tu payin (objects=...) khodesh draft shode haro az safhe hazf mikone
    def active(self):
        return self.filter(status=True)






# Create your models here.
class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name = 'آدرس آی پی')


class Category(models.Model):

    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name='children', verbose_name='زیردسته')                                #'self'khodesh parente khodeshe be khodesh foreign key mizanae,default be surate pishfarz category ha valed nadaran on_delet= models.CASCADE bashe yani ba pak shodane valed farzanda ham pak mishan SET.NULL bashe age khodemun khastim badan pak mikonim,
    title = models.CharField(max_length=200 , verbose_name = 'عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, verbose_name = "آدرس دسته بندی")
    status = models.BooleanField(default = True, verbose_name = "آیا میخواهید نمایش داده شود؟")
    position = models.IntegerField(verbose_name= 'پوزیشن')
    class Meta :
         verbose_name = "دسته بندی"
         verbose_name_plural = "دسته بندی ها"
         ordering = ['parent__id','position']
    def __str__(self):          #field haye article ro bar asase title neshoon mide|||||||||magic mothod str k bar asase reshte be ma neshun mide
          return self.title
    objects = CategoryManager()


class Article(models.Model):
    STATUS_CHOICES = (
       ('d', 'پیشنویس'),
       ('p', 'نوشته شده'),
       ('i', 'در حال بررسی'),    #investigation
       ('b', 'برگشت داده شده'),  #backed
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name ="article", verbose_name='نویسنده')
    title = models.CharField(max_length=200 , verbose_name = 'عنوان مقاله')
    slug = models.SlugField(max_length=100, unique=True, verbose_name = "آدرس مقاله")
    category = models.ManyToManyField(Category, verbose_name = 'دسته بندی', related_name= "article") # har esmimitvanad bashad hata 's' va ...
    description = models.TextField(verbose_name = "محتوا")
    thumbnail = models.ImageField(upload_to="images",verbose_name = "تصویر مقاله")
    publish = models.DateTimeField(default=timezone.now,verbose_name = "زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default = False, verbose_name = "مقاله ویژه")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name = "وضعیت")
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, through='ArticleHit', blank=True, related_name='hits',verbose_name='بازدید ها')

    class Meta :
         verbose_name = "مقاله"
         verbose_name_plural = "مقالات"
         ordering = ['-publish']
    def __str__(self):          #field haye article ro bar asase title neshoon mide reshteeee mikoone
        return self.title

    def get_absolute_url(self):
        return reverse("Accounts:home")

    #def category_published(self):                          # dar aval vagti in ro mineveshrim agar tik aya nomayesh dade shavad ro pak mikardim bazam nomayesh midad tag haro hala fagat unayi k statuseshun true bashe ro neshun mide na hamamro
    #    return self.category.filter(status=True)

    def thumbnail_tag(self):
        return format_html("<img width=100 height=75 style='border-radius: 10px' src='{}'>".format(self.thumbnail.url))              #braye neshan dadane aks thumbnail dar admin panel in kodo neveshtim ||| format_html k bala importesham kardim baraye bahs  haye amniyati bud
    thumbnail_tag.short_description = "عکس"
    def category_to_str(self):         #field haye article ro bar asase title neshoon mide|||||||||magic mothod str k bar asase reshte be ma neshun mide
        return ", ".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"

    objects = ArticleManager()


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
