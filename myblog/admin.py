from django.contrib import admin
from .models import Article, Category, IPAddress
from django.utils.translation import ngettext

# Register your models here.

@admin.action(description='انتشار مقالات انتخاب شده')                      #azafe kardane jomle va egdam be gesmate action ha
def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
#    modeladmin.message_user(request,
#            '%d story was successfully marked as published.',
#            '%d stories were successfully marked as published.',
#            updated,
#          %updated, messages.SUCCESS)


@admin.action(description='پیشنویس کردن مقالات انتخاب شده')
def make_draft(modeladmin, request, queryset):
    queryset.update(status='d')



class CategoryAdmin(admin.ModelAdmin):      #yani admin az model.admin ersbari kone
      list_display = ('position','title','slug','parent','status')      #bularida gorsadir asli onvanin kanarida
      list_filter = (['status'])                    #bar asase bular filter elir
      search_fields = ('title','slug')                  #bularin ichin gedir search elir
      prepopulated_fields = {'slug': ('title',)}     #slug ro mire az ro title khodesh misaze

                                                #vase moratabsazi
admin.site.register(Category,CategoryAdmin)  # bayad payin tarin bashe va alave bar article bagie claaaaassss haram behesh add konim


class ArticleAdmin(admin.ModelAdmin):      #yani admin az model.admin ersbari kone
      list_display = ('title','thumbnail_tag','slug','author','publish','is_special','status','category_to_str')      #bularida gorsadir asli onvanin kanarida
      list_filter = ('publish','status','author')                    #bar asase bular filter elir
      search_fields = ('title','description')                  #bularin ichin gedir search elir
      prepopulated_fields = {'slug': ('title',)}     #slug ro mire az ro title khodesh misaze
      ordering = ['-status','-publish',]             #vase moratabsazi

      actions = [make_published, make_draft]

admin.site.register(Article,ArticleAdmin)  # bayad payin tarin bashe va alave bar article bagie claaaaassss haram behesh add konim
admin.site.register(IPAddress)
