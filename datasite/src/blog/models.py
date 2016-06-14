from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

class Author(models.Model):
    name = models.CharField(max_length = 80)
    age = models.IntegerField(blank = True, null = True)
    sex = models.CharField(max_length = 10)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    attach = models.FileField(upload_to = "datasite/blog/file/")
    pub_time = models.DateTimeField('PUB_TIME')
    author = models.ForeignKey(Author)
    
    def __unicode__(self):
        return self.title
    
class ArticleComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField('PUB_TIME')
    author = models.ForeignKey(Author)
    article = models.ForeignKey(Article)
    
    def __unicode__(self):
        return self.content
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'attach', 'pub_time') 
    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'email')

admin.site.register(Article, ArticleAdmin) 
admin.site.register(Author, AuthorAdmin)


    