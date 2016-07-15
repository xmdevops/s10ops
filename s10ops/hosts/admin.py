#_*_coding:utf-8_*_
from django.contrib import admin

import auth_admin
# Register your models here.
import models
#��models.pyд�ı�ע�ᵽadmin�ʹ��ҳ��̨���Թ������ݿ�
class HostAdmin(admin.ModelAdmin):#ʹע��ı���ҳ�������ʾ��ϸ����Ϣ
    list_editable = ('hostname','ip_addr')#���Ա༭
    list_display = ('hostname','ip_addr','port','idc','system_type','enabled')#��ʾ������
    search_fields = ('hostname','ip_addr')#��������������
    list_filter = ('idc','system_type')#���Թ��˵�����
class HostUserAdmin(admin.ModelAdmin):
    list_display = ('auth_type','username','password')

class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host','host_user','get_groups')#'get_groups'���Լ�����ģ���models��
    filter_horizontal = ('host_groups',)#��ѡ������ʱ��ˮƽ������һ����Ϣ��
admin.site.register(models.UserProfile,auth_admin.UserProfileAdmin)
admin.site.register(models.Host,HostAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUser,HostUserAdmin)
admin.site.register(models.BindHostToUser,BindHostToUserAdmin)
admin.site.register(models.IDC)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)