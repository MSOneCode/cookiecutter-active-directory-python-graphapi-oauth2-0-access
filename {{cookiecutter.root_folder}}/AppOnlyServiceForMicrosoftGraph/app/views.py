"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest,HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from app.auth_helper import get_token
from app.task_helper import invoke
import json 

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if(request.session.has_key('access_token')):
        return HttpResponseRedirect('/connect')
    else:
        return render(
            request,
            'app/index.html'
        )

def connect(request):
    result = get_token()
    msg = 'There is something wrong, please check you have modified the configurations in "app/config.py"' if result.status_code==400 else 'Connect to Miscrosoft Graph successfully!'
    if result.status_code==200:
        request.session['access_token'] = result.json().get('access_token')
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'isConnected':'true',
            'msg':msg
        })
    )

def disconnect(request):
    del request.session['access_token']
    return render(
            request,
            'app/index.html'
        )

def users(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    if(request.session.has_key('access_token')):
        request_result = invoke(request.session['access_token'],'users',params={'$select':'accountEnabled,id,displayName,userPrincipalName'})
        users_list = json.loads(request_result.text)['value']
        return render(
            request,
            'app/users.html',
            context_instance = RequestContext(request,
            {
                'users_list':users_list
            })
        )
    else:
        return render(
            request,
            'app/index.html'
        )

def add_user(request):
    if(request.method=='POST'):
        data = request.POST
        request_result = invoke(request.session['access_token'],
                                'users/',
                                method='POST',
                                data={'displayName':data['displayName'],
                                      'mailNickname':data['mailNickname'],
                                      'userPrincipalName':data['userPrincipalName'],
                                      'passwordProfile':{'password':data['password'],
                                                         'forceChangePasswordNextSignIn':data['forcePasswordChangeOnNextLogin']
                                                         },
                                      'accountEnabled':data['accountenabled']
                                      }
                                )
        return render(
            request,
            'app/add_user_form.html',
            context_instance = RequestContext(request,
            {
                'isShowMsg':'true',
                'msg' : 'add successfully!' if request_result.status_code==204 else request_result.text
            })
        )
    else:
        return render(
            request,
            'app/add_user_form.html',
            context_instance = RequestContext(request,
            {
                'isShowMsg':'false'
            })
        )

def edit_user(request, value=None):
    if(request.method=='POST'):
        data = request.POST
        request_result = invoke(request.session['access_token'],
                                'users/'+value,
                                method='PATCH',
                                data={'displayName':data['displayName'],
                                      'userPrincipalName':data['userPrincipalName']
                                      }
                                )
        return render(
            request,
            'app/user_form.html',
            context_instance = RequestContext(request,
            {
                'isShowMsg':'true',
                'msg' : 'update successfully!' if request_result.status_code==204 else request_result.text
            })
        )
    else:
        request_result = invoke(request.session['access_token'],'users/'+value)
        user = json.loads(request_result.text)
        return render(
            request,
            'app/user_form.html',
            context_instance = RequestContext(request,
            {
                'isShowMsg':'false',
                'item' : user    
            })
        )

def del_user(request, value=None):
    request_result = invoke(request.session['access_token'],'users/'+value,method='DELETE')
    return render(
        request,
        'app/user_form.html',
        context_instance = RequestContext(request,
        {
            'isShowMsg':'true',
            'msg' : 'delete successfully!' if request_result.status_code==204 else request_result.text    
        })
    )