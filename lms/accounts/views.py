from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import CustomUser,Employee,LeaveType,Leaves,Department
from .forms import EmployeeCreationForm,EmployeeChangeForm,LeavesCreationForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# Create your views here.

links = [
{'link':'navbar-dashboards','icon':'shop','color':'red', 'name':'Dashboard','active':False,'dropdown':True,
'dropdowns':
[{'link':'/','icon':'collection', 'name':'My dashboard','active':False}]
},

{'link':'navbar-examples','icon':'single-02','color':'green','name':'My Profile','active':False,'dropdown':True,
'dropdowns':
[{'link':'/accounts/update_profile/','icon':'atom', 'name':'update','active':False},
{'link':"/accounts/logout/",'icon':'user-run', 'name':'Logout','active':False}]
},

{'link':'navbar-components','icon':'send','color':'yellow', 'name':'Leaves','active':False,'dropdown':True,
'dropdowns':
[{'link':'/leaves/application/','icon':'active-40', 'name':'Apply','active':False},
{'link':'/leaves/history/','icon':'bullet-list-67', 'name':'History','active':False}
]
}
]
def numberOfDays(fromDate,toDate):
    from datetime import datetime
    date_format = "%m/%d/%Y"
    a = datetime.strptime(fromDate, date_format)
    b = datetime.strptime(toDate, date_format)
    delta = b - a
    return int(delta.days)

def numberOfWeeks(fromDate,toDate):
    return numberOfDays(fromDate,toDate)/7

def addDays(date,days):
    from datetime import timedelta
    from datetime import datetime
    date_format = "%m/%d/%Y"
    result = datetime.strptime(date, date_format) + timedelta(days=days)
    return result


from datetime import datetime
def dashboard(request):
    template_name = "accounts/dashboard.html"
    if request.user.is_authenticated:
        if request.user.is_superuser:
            leaves = Leaves.objects.all()
            args = {'user':request.user,
                'links':links,
                'object_list':leaves
                }
            return render(request,template_name,args)

        if request.user.is_staff:
            leaves = []
            department = Department.objects.filter(hod=request.user)
            if department:
                for each in department:
                    employee_for_staff = Employee.objects.get(department=each)
                    employee_leaves = Leaves.objects.filter(employee=employee_for_staff)
                    for i in employee_leaves:
                        leaves.append(i)
            own_leaves = Leaves.objects.filter(employee = request.user)
            for e in own_leaves:
                leaves.append(e)

            args = {'user':request.user,
                'links':links,
                'object_list':leaves
                }
            return render(request,template_name,args)
        else:
            my_leaves = []
            employee = request.user
            leaves = Leaves.objects.filter(employee=employee)


        
            running_leaves = Leaves.objects.filter(employee=request.user,status="Approved",started=True,paused=False,ended=False).order_by('date_approved')

        
            today = datetime.now().date()
            today = (today).strftime("%m/%d/%Y")

            for i in running_leaves:
                toDate = (i.toDate).strftime("%m/%d/%Y")
                days_remaining = numberOfDays(today,toDate)
                if days_remaining == 0:
                    i.ended = True
                i.days_remaining = days_remaining
                i.save()
                my_leaves.append(i)

            # Getting the latest approved leave
            try:
                approved = my_leaves[-1]
            except:
                approved = []
            # print(my_leaves)
            # print(approved.description)
            if approved:
                try:
                    leave_prog = round((approved.days_remaining/approved.days)*100,2)
        
                    # print('progress',leave_prog)
                except:
                    leave_prog = 0
                else:
                    if leave_prog <= 20.0:
                        status = "danger"
                        prog_status = "danger"
                    elif leave_prog > 20.0 and leave_prog <= 50.0:
                        status = "warning"
                        prog_status = "warning"
                    else:
                        status = "info"
                        prog_status = "success"

                args = {'user':request.user,
                'links':links,
                'object_list':leaves,
                'object':approved,
                'progress':int(leave_prog),
                'status':status,
                'prog_status':prog_status
                }
            else:
                args={'user':request.user,'links':links,'object_list':leaves}
            return render(request,template_name,args)
        
    else:
        args={'links':links}
        template_name = "registration/login.html"
        return render(request,template_name,args)
    args={'links':links}
    return render(request,template_name,args)

def update_leave(request,pk):
    if request.user.is_authenticated:
        if request.method =="GET":
            leavestypes = LeaveType.objects.all()
            types = []
            ids = []
            for each in leavestypes:
                types.append(each.leavetype)
                ids.append(each.id)
            all_leaves=zip(types,ids)
            template_name = "accounts/leave_history.html"
            args = {'user':request.user,'links':links,'all_leaves':all_leaves}
            return render(request,template_name,args)
        else:
            user = request.user
            try:
                fromDate = datetime.strptime(request.POST['fromDate'],'%m/%d/%Y')
                toDate = datetime.strptime(request.POST['toDate'],'%m/%d/%Y')#.strftime('%Y-%m-%d')

                leavetype = request.POST['leavetype']
                leavetype = LeaveType.objects.get(id=int(leavetype))
                description = request.POST['description']
                leave = Leaves.objects.get(id=pk)
                if leave.status == "Approved":
                    messages.warning(request, "This leave has already been approved")
                    return redirect('/leaves/history/{}/'.format(pk))
                
                myfromDate = fromDate.strftime('%m/%d/%Y')
                mytoDate = toDate.strftime('%m/%d/%Y')  
                days = numberOfDays(myfromDate,mytoDate)
                print(days)

                leave.days = days
                leave.toDate = toDate
                leave.fromDate = fromDate
                leave.description = description
                leave.leavetype = leavetype
                leave.employee = user
            
                leave.status = "Pending"

            except Exception as e:
                messages.error(request, "There was an error updating")
                return redirect('/leaves/history/{}/'.format(pk))
            else:
                leave.save()
                messages.success(request, "Successfully updated")
                return redirect('/leaves/history/')
    else:
        template_name = "registration/login.html"
        args = {'user':Employee.objects.get(username=request.user.username),'links':links}
        return render(request,template_name,args)




def update_profile(request):
    if request.user.is_authenticated:
        if request.method =="GET":
            template_name = "accounts/update_profile.html"
            try:
                employee = Employee.objects.get(username=request.user.username)
            except:
                employee = CustomUser.objects.get(username=request.user.username)
            args = {'user':employee,'links':links}
            return render(request,template_name,args)
        else:
            user = request.user
            try:
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                username = request.POST['username']

                city = request.POST['city']
                address = request.POST['address']
                country = request.POST['country']

                country_code = request.POST['country_code']
                marital_status = request.POST['marital_status']
                gender = request.POST['gender']

                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                
                user.city = city
                user.country = country
                user.country_code = country_code

                user.marital_status = marital_status
                user.gender = gender
                user.username = username
            except:
                messages.error(request, "Please Check your form")
                return redirect('update')
            else:
                user.save()

                messages.success(request, "Successfully updated")
                return redirect('update')
    else:
     
        template_name = "registration/login.html"
        args = {'user':Employee.objects.get(username=request.user.username),'links':links}
        return render(request,template_name,args)

def email_verification(request, email_token=""):
    
    template_name = 'registration/login.html'
    
    try:
    	user = Employee.objects.get(email_token=email_token)
    except:
        messages.warning(request, "Please you provided a wrong token.")
        return redirect('login')
    else:
        user.email_confirmed = 1
        user.is_active = True
        user.is_staff = True
        user.save()
        
        messages.success(request, "Thanks for verifying your email.Login Now")
        return redirect("login")#HttpResponse(user)
    args = {}
    return render(request, template_name, args)

    




class CreateEmployeeView(ListView):
    form_class = EmployeeCreationForm
    #success_url = reverse_lazy('home')
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form_class
        args = {'form': form,"warning":"Provide a valid email",'links':links}
        #sendMail()

        return render(request,self.template_name,args)

    def post(self,request):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            #group = Group.objects.get(name='Employees')
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password1']
            # department = form.cleaned_data['department']
            
            user = self.form_valid(form)
            user.is_active = True
            user.is_staff = False
            user.save()
            try:
                user.employee_id = str(user.department.dept_code) + str(user.id)
                user.save()
            except Exception as e:
                messages.success(request, str(e))
                return redirect('register')
    	   
            # user = authenticate(username=username, password=password)
            # login(request, user)
            verfication_link = "/localhost:8000/accounts/email_verification/"+user.email_token+"/"
            msg_plain = render_to_string(
                'accounts/welcome.txt', {'username':user.username,'verification_link':verfication_link})
            msg_html = render_to_string('accounts/welcome.html', {'username':user.username,'verification_link':verfication_link})
            subject = "Welcome {}".format(user.username)
            try:
                send_mail(subject,
                msg_plain,'gwcllms601@gmail.com',
                [user.email],
                html_message=msg_html,
                fail_silently=False,)
            except Exception as e:
                messages.warning(request, str(e))

            else:
                messages.success(request,"Please check your email for verification")
            
            messages.success(request, "Congratulations, succesfully registered")
            return redirect('register')
        else:
            messages.error(request, "Please check your form for errors")
            return redirect('register')

        args = {'form': form,"warning":"Provide a valid email",'links':links}
        return render(request, self.template_name, args)


    def create_group(self,group_name):
        group = Group(name=group_name)
        group.save()

    def add_user_to_group(self,group_name,user_id):
        group = Group.objects.get(name=group_name)
        #users = CustomUser.objects.all()
        user = CustomUser.objects.get(pk=user_id)
        user.groups.add(group)        # user is now in the "group_name" group

    def is_member(self,user_id,group_name):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name=group_name).exists()

    def is_in_multiple_groups(self,user_id,list_of_groups):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name__in=list_of_groups).exists()

    def form_valid(self, form):
        user = form.save(commit=True)
        return user
    def get_context_data(self, **kwargs):
        context = super(CreateEmployeeView, self).get_context_data(**kwargs)
        context.update({'success': "We have sent you an email. Check for your secret key."})
        return context

class CreateLeaveView(ListView):
    form_class = LeavesCreationForm
    #success_url = reverse_lazy('home')
    template_name = 'accounts/apply.html'

    def get(self, request):
        if self.request.user.is_authenticated:
            form = self.form_class
            leavestypes = LeaveType.objects.all()
            types = []
            ids = []
            for each in leavestypes:
                types.append(each.leavetype)
                ids.append(each.id)
            all_leaves=zip(types,ids)
            today = datetime.now().date()
            # print("Today: ",today)
            fromDate = (today).strftime("%m/%d/%Y")
            toDate = addDays(fromDate,5)
            toDate = toDate.strftime("%m/%d/%Y")

            args = {'form': form, 'all_leaves': all_leaves,'links':links,'fromDate':fromDate,'toDate':toDate}
            return render(request,self.template_name,args)
        else:
            template_name = 'registration/login.html'
            args = {'links':links}
            return render(request,template_name,args)

    def post(self,request):
        if self.request.user.is_authenticated:
            form = self.form_class(request.POST,request.FILES)
            if form.is_valid():
                #group = Group.objects.get(name='Employees')
                # description = form.cleaned_data['description']
                try:
                    fromDate = request.POST['fromDate']#).strftime('%m/%d/%Y')
                    toDate = request.POST['toDate']#).strftime('%m/%d/%Y')
                    no_of_days = numberOfDays(fromDate,toDate)
                except Exception as e:
                    messages.error(request, str(e))
                    return redirect('application')

                user = self.request.user

                messages.success(request, "Successful, pending approval")
                leave = self.form_valid(form)
                leave.employee = user
                leave.status = 'Pending'
                leave.days = no_of_days
                leave.save()
                return redirect('application')
            else:
                messages.error(request, "Please check your form for errors")
                return redirect('application')
            args = {'form': form,'links':links}
            return render(request, self.template_name, args)
        else:
            template_name = 'registration/login.html'
            args = {'links':links}
            return render(request,template_name,args)


    def create_group(self,group_name):
        group = Group(name=group_name)
        group.save()

    def add_user_to_group(self,group_name,user_id):
        group = Group.objects.get(name=group_name)
        #users = CustomUser.objects.all()
        user = CustomUser.objects.get(pk=user_id)
        user.groups.add(group)        # user is now in the "group_name" group

    def is_member(self,user_id,group_name):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name=group_name).exists()

    def is_in_multiple_groups(self,user_id,list_of_groups):
        user = CustomUser.objects.get(pk=user_id)
        return user.groups.filter(name__in=list_of_groups).exists()

    def form_valid(self, form):
        user = form.save(commit=True)
        return user
    def get_context_data(self, **kwargs):
        context = super(CreateLeaveView, self).get_context_data(**kwargs)
        # context.update({'success': "We have sent you an email. Check for your secret key."})
        return context


class LeaveListView(ListView):
    model = Leaves
    template_name = "accounts/history.html"
    def get_context_data(self, **kwargs):
        context = super(LeaveListView, self).get_context_data(**kwargs)
        context['links']=links
        return context
    def get_queryset(self):
        # my_obj = Lesson.objects.get(title="Getting Started")
        employee = self.request.user
        return Leaves.objects.filter(employee=employee)

class LeaveDetailView(DetailView):
    model = Leaves
    template_name = "accounts/history_detail.html"
    def get_context_data(self, **kwargs):
        context = super(LeaveDetailView, self).get_context_data(**kwargs)
        context['links']=links
        leavestypes = LeaveType.objects.all()
        types = []
        ids = []
        for each in leavestypes:
            types.append(each.leavetype)
            ids.append(each.id)
        all_leaves=zip(types,ids)
        context['all_leaves'] = all_leaves
        return context

    def get_queryset(self):
            return Leaves.objects.all()


def reset_password(request, reset_token):
    form_class = EmployeeChangeForm
    # success_url = reverse_lazy('home')
    template_name = 'accounts/reset_password.html'
    form = form_class
    if request.method == "GET":
        args = {'form': form,"warning":"You provided a wrong token",'reset_token':reset_token}
        try:
            user = Employee.objects.get(reset_token=reset_token)
        except:
	        return render(request, template_name, args)
        else:
            args = {'form': form,"warning":"Please enter a new password",'reset_token':reset_token}
            return render(request, template_name, args)

    if request.method == "POST":
        args = {'form': form,"warning":"You provided a wrong token, please use correct token",'reset_token':reset_token}
        try:
	        user = CustomUser.objects.get(reset_token=reset_token)
        except:
            return render(request, template_name, args)
        else:
            user.set_password(request.POST['password1'])
            user.reset_token = ""
            user.save()
	    	#user = authenticate(username=user.username, password=user.password)
            #login(request, user)
            messages.success(request, "Hi, Your password has been reset, login now.")
            return redirect('login')
        args = {'form': form,"warning":"Please make sure the password obeys the listed rules"}
        return render(request, template_name, args)
    return render(request, template_name, args)

import json
from Jake.lib.parser import Parser
from Jake.lib.tokenizer import *
from Jake.lib.models import Message
import time


class StartChat:
    # Asks user for input
    def __init__(self,):
        #self.command = input("Waiting for your input> ")
        self.name = "Jake"

    def take2nd(self,elem):
        return elem[1]

    def matcher(self,array, snt):
        # setting up lists
        ind = []
        all =[]
        final_dict = {'0':0}
        # looping through words in a sentence
        # and matching against what we have
        for word in snt:
            for index,i in enumerate(array):
                if word in i:
                    """ we append any match's index to ind list"""
                    ind.append(index)

        #print(ind)
        dic = {}
        """ we now create a dictionary of the indices so as to eliminate duplicates """
        for i in ind:
            dic['{}'.format(i)]=i
        #print(dic)
        """ we loop through the dictionary items and update
        the dictionary with their number of occurences """
        for key,val in dic.items():
            dic[key]=(ind.count(val))
            """ we add their occurences to a list from
            which we later get the max """
            all.append((ind.count(val)))
        if all:
            high = max(all)
            for key,val in dic.items():
                    if val == high:
                        our_sentence = array[int(key)]
            # Calculating number of words gotten right
            ratio = high/(len(snt)*1.0)
            #print("Ratio: ",ratio)
            if ratio >= 0.5:
                """ we once again go back to our dictionary(updated) and
                fetch the key
                that has the max value """
                final_dict[our_sentence]=ratio
                return final_dict
                # for key,val in dic.items():
                #     if val == high:
                #         return array[int(key)]
            else:
                return
        else:
            return

    def my_searcher(self,all_from_db,user):
        my_dict = {}
        for index,each in enumerate(all_from_db):
            ratio = self.ratio_match(user,each)
            if ratio >= .5:
                #my_dict.clear()
                my_dict[each]=ratio
        return my_dict


    def ratio_match(self,user,existing):
        from difflib import SequenceMatcher as sm
        return sm(None,user,existing).ratio()

    def my_matcher(self, all_msgs,new_msg,bot_ratio=0.5):
        my_dict = {'0':0}
        for index,each_msg in enumerate(all_msgs):
            ratio = self.ratio_match(new_msg,each_msg)
            if ratio > bot_ratio and ratio > list(my_dict.values())[0]:
                my_dict.clear()
                my_dict[each_msg]=ratio
        return my_dict


    def get_specific(self,tokens,robot_name,bot_ratio):
        robot_name=robot_name.lower()
        """Getting all existing questions"""
        all_obj = Message.objects.filter(name=robot_name)
        all_msgs = []
        for each in all_obj:
            all_msgs.append(each.message)
        """Using our matcher function to get the closest match"""
        closest = self.my_matcher(all_msgs,tokens,bot_ratio)
        if list(closest.keys())[0] == '0':
            res = []
        else:
            matched = list(closest.keys())[0]
            all_matched_from_db = Message.objects.filter(message=str(matched),name=robot_name)
            # print("All from database:", all )
            res = []
            if len(all_matched_from_db) == 1:
                category = all_matched_from_db[0].category
                if category != "unanswered":
                    msgs_from_cat = Message.objects.filter(category=category,name=robot_name)
                    for i in msgs_from_cat:
                        res.append(i.response)
                else:
                    res = []
            elif len(all_matched_from_db)>1:
                for i in all_matched_from_db:
                    if i.category != "unanswered":
                        res.append(i.response)
            else:
                res = []
        return res


    def start(self,userinput,robot_name):
        """Tokenization of input from user to strip unnecessary punctuations"""
        tokens = Tokenizer().tokenize(userinput)
        res = []
        """Tokenization returns a list of chunks of words, we put them together here"""
        checker = ""
        for index,i in enumerate(tokens):
            if len(tokens)<2:
                checker +=i+""
            else:
                if not index == len(tokens)-1:
                    checker += i + " "
                else:
                    checker += i + ""

        checker = checker.lower()
        company = "pywe"
	
	""" Below, the bot_ratio=0.6 will determine how close what a user types has to be
	with what we have in our database in order to conclude that is what the user wants to say.
	For example, if we have 'hello, how are you?' in our database and a user comes to 
	type 'how are you', the function called get_specific() will go to the database and fetch
	all our existing questions and compare them with what the user types, all the questions
	from the database that are as close to the one the user typed as much as 0.6 or 60% will qulaify
	to be part of what the user typed, but the one which has the highest percentage among these
	will be chosen. If they are more than one, one of them will randomly be chosen.
	comparing 'hello, how are you?' to 'how are you' should return about 0.7586206896551724 match:
	This is done by the python function defined here:
	def ratio_match(user_input,existing):
        	from difflib import SequenceMatcher as sm
        	return sm(None,user,existing).ratio()
	and that is about 76% match rate. Therefore the previosly recorded answer for the question:
	'helllo, how are you?' can also be given to the question 'how are you'
	"""
        res = self.get_specific(tokens=checker,robot_name=robot_name,bot_ratio=0.6)
        return Parser().parse(res=res,snt=tokens,company=company,robot_name=robot_name)

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def process(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    message = json_data["message"]
    robot = "pywebot"
    output = StartChat().start(message,robot)
    output_msg = output[0]
    data = {'response': output_msg,'status code':200,'robot_name':robot}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


