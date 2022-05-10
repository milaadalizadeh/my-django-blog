from django import template
from ..models import Category
from django.db.models import Count, Q
from ..models import Article, Category                             #باید 2 تا خانه برگردیم تا به پوشه مورد نظر یعنی مدل برسیم
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType

register = template.Library()
@register.simple_tag
def title():
    return "وبلاگ جنگویی"




@register.inclusion_tag("myblog/partials/category_navbar.html")
def category_navbar():
    return {
    "category": Category.objects.filter(status=True),
    }


@register.inclusion_tag("myblog/partials/sidebar.html")
def popular_articles():
    last_month = datetime.today() - timedelta(days=30)
    return {
    "articles":  Article.objects.published().annotate(count=Count('hits', filter=Q(articlehit__created__gt=last_month))).order_by('-count', '-publish')[:5],
    "title":'مقالات پر بازدید ماه'
    }


@register.inclusion_tag("myblog/partials/sidebar.html")
def hot_articles():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='myblog', model='article').id
    return {
    "articles":  Article.objects.published().annotate(count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))).order_by('-count', '-publish')[:5],
    "title":'مقالات داغ ماه'
    }






@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):                                             #esme linki k mikhahim ma ra be anja bebarad masalan createview ya jaye dige//// content= matnik tuye link migirim maslan afzudan magalat edit magalat va ..........
    return{
        "request": request,
        "link_name": link_name,
        "link": 'Accounts:{}'.format(link_name),
        "content": content,
        "classes": classes,
    }
