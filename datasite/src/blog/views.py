# from django.shortcuts import render

from django.template import loader, Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect  
from blog.models import Author, Article  
from django.shortcuts import render_to_response
  
def authorList(request):
    author_list = Author.objects.all()
#     template = loader.get_template('author_list.html')
#     context = Context({'author_list' : author_list})
#     return HttpResponse(template.render(context))
    return render_to_response('author_list.html', 
        {'author_list' : author_list}, context_instance=RequestContext(request))

def articleList(request):
    article_list = Article.objects.all()
#     template = loader.get_template('article_list.html')
#     context = Context({'article_list' : article_list})
#     return HttpResponse(template.render(context))
    return render_to_response('article_list.html', 
        {'article_list' : article_list}, context_instance=RequestContext(request))

def article(request, aid):
    print 'article_id %s' %aid
    article = Article.objects.get(id = aid)
    print article.__dict__
#     template = loader.get_template('article.html')
#     context = Context({'article' : article})
#     return HttpResponse(template.render(context))
    return render_to_response('article.html', 
        {'article' : article}, context_instance=RequestContext(request))

def articleUpdate(request, aid):
    article = Article.objects.get(id = aid)
    if request.POST.has_key('title'):
        article.title =  request.POST['title']
    if request.POST.has_key('content'):
        article.content = request.POST['content']
    article.save()
    return HttpResponseRedirect('/blog/')
#     article_list = Article.objects.all()
#     template = loader.get_template('article_list.html')
#     context = RequestContext(request, {'article_list' : article_list})
#     return HttpResponse(template.render(context))
#     return render_to_response('article_list.html',
#         {'article_list' : article_list}, context_instance=RequestContext(request))
    
def articleDelete(request, aid):
    print 'article_id %s' %aid
    article = Article.objects.get(id = aid)
    article.delete()
    return HttpResponseRedirect('/blog/')

    