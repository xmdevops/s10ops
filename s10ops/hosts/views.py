#_*_coding:utf-8_*_

from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import models,task,json,utils
# Create your views here.

@login_required
def index(request):
    return render(request,'index.html')

@login_required
def hosts_index(request):
    return render(request,'hosts/dashboard.html')

@login_required
def assets_index(request):
    return render(request,'assets/dashboard.html')

@login_required
def monitor_index(request):
    return render(request,'monitor/dashboard.html')
@login_required
def acc_logout(request):
    logout(request)

    return  HttpResponseRedirect("/")


def acc_login(requeset):
    login_err = ''
    if requeset.method == 'POST':
        username = requeset.POST.get('email')
        password = requeset.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is not None:
            login(requeset,user)

            return HttpResponseRedirect('/')

        else:
            login_err = "Wrong username or password!"
    return  render(requeset,'login.html', {'login_err':login_err})


@login_required
def host_mgr(request):
    selected_gid = request.GET.get('selected_gid')#��host_mgr.html�л�ȡselected_gid��
    if selected_gid:    #����selected_gid��BindHostToUser������û���
        host_list = models.BindHostToUser.objects.filter(host_groups__id =selected_gid)
    else:   #���selected_gid�����ڣ���bind_hosts��ѡȡû���û�����û�
        host_list = request.user.bind_hosts.select_related()
    return render(request,"hosts/host_mgr.html",{'host_list':host_list})

@login_required
def multi_cmd(request):
    return render(request,"hosts/multi_cmd.html")

@login_required
def multi_file_transfer(request):
    return render(request,"hosts/multi_file_transfer.html")


@login_required
def submit_task(request):
    print request.POST

    tas_obj = task.Task(request)#����task.py�ķ���
    res = tas_obj.handle()
    return HttpResponse(json.dumps(res)) #�ֵ���Ҫ��json�½����res���������ֵ�

@login_required
def get_task_result(request):
    task_obj = task.Task(request)
    res = task_obj.get_task_result()
    print '--res--task--',res
    return HttpResponse(json.dumps(res,default=utils.json_date_handler))
    #json.dump(res,default)��ʾ��res�����ݰ����溯���ķ�ʽ����󷵻أ���Ϊjson������ʱ���ʽ�����Ե���д����

@csrf_exempt #csrf����
@login_required
def file_upload(request):
    filename = request.FILES['filename']
    print '-->',request.POST
    file_path = utils.handle_upload_file(request,filename)

    return HttpResponse(json.dumps({'uploaded_file_path':file_path}))