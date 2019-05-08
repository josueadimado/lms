from django.contrib import admin
from .models import Department,Leaves,LeaveType,CustomUser,Employee
from django.contrib.auth.admin import UserAdmin
from .forms import LeavesChangeForm,LeavesCreationForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from datetime import datetime

def approve(modeladmin, request, queryset):
    queryset.update(status="Approved")
approve.short_description = "Mark selected requests as approved"

def disapprove(modeladmin, request, queryset):
    queryset.update(status="Disapproved")
disapprove.short_description = "Mark selected requests as disapproved"

def pend(modeladmin, request, queryset):
    queryset.update(status="Pending")
pend.short_description = "Mark selected requests as pending"

def numberOfDays(fromDate,toDate):
    from datetime import datetime
    date_format = "%m/%d/%Y"
    a = datetime.strptime(fromDate, date_format)
    b = datetime.strptime(toDate, date_format)
    delta = b - a
    return int(delta.days)

def numberOfWeeks(fromDate,toDate):
    return numberOfDays(fromDate,toDate)/7

class LeaveAdmin(admin.ModelAdmin):
    add_form = LeavesCreationForm
    form = LeavesChangeForm
    model = Leaves
    # Defines the list of fields displayed on admin page
    list_display = ['description','leavetype', 'status']
    fields = ['description','leavetype', 'status','adminRemark','employee','fromDate','toDate','days','days_remaining','started','paused']
    #fields = ['username','email',  'password', 'date_joined', 'image_tag', 'user_img','reset_token','is_patron','last_login','is_active','is_staff']
    readonly_fields = ['days','days_remaining']
    # Enables editing other fields

    # fieldsets = LeaveAdmin.fieldsets + (
    #     ('Extra Fields', {'fields': ('user_img','is_patron','role','role_description','fav_color','is_helper','lessons_completed',)}),
    #  )

    actions = [approve,disapprove,pend]


    def save_model(self, request, obj, form, change):
        if obj.pk:
          old_obj = Leaves.objects.get(pk=obj.pk)
          old_status = old_obj.status
          old_desc = old_obj.description
          user = old_obj.employee
        #   new_status = form.cleaned_data['status']
        new_status = obj.status
        
        if old_status != new_status:
            # send email here   
            msg_plain = render_to_string(
                'accounts/email.txt', {'username':user.username,'description':old_desc,'status':new_status,'days_remaining':obj.days_remaining})
            msg_html = render_to_string('accounts/email.html', {'username':user.username,'description':old_desc,'status':new_status,'days_remaining':obj.days_remaining})
            subject = "{} Status {}".format(user.username,new_status)
            try:
                send_mail(subject,msg_plain,'gwcllms601@gmail.com',[user.email],html_message=msg_html,fail_silently=False,)
            except:
                messages.success(request, "Email could not be sent")
            else:
                messages.success(request, "Email sent")
        if obj.status == "Approved":
            obj.started = True
            today = datetime.now().date()
             # print("Today: ",today)
            fromDate = (today).strftime("%m/%d/%Y")
            toDate = (obj.toDate).strftime("%m/%d/%Y")
            obj.days_remaining = numberOfDays(fromDate,toDate)
            new_from_date = (obj.fromDate).strftime("%m/%d/%Y")
            obj.days = numberOfDays(new_from_date,toDate)

            

        # custom stuff here
        # print("change: ",change)
        # print("form: ",)
        # print('object status: ',old_obj.status)
        obj.save()

# Register your models here.
admin.site.register(Department)
admin.site.register(Leaves,LeaveAdmin)
admin.site.register(LeaveType)
admin.site.register(CustomUser)
admin.site.register(Employee)