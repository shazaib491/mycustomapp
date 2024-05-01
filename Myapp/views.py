from django.contrib  import messages
from django.shortcuts import render , redirect
from django.http import HttpResponse
from Myapp.models import Mecaps
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User , auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

@csrf_exempt
def register(request):
    # return HttpResponse('Welcome mere grahak')
    if request.method == 'POST':
        print('\n\n',request.POST,'\n\n')
        u = request.POST['user']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email  = request.POST['em']
        password = request.POST['pass']
        
        newuser = User.objects.create_user(username=u,first_name=fname,last_name=lname,email=email,password=password)
        newuser.save()
        
        return redirect('register')
    return render(request,'register.html')

@csrf_exempt
def login_request(request):
    if request.method == "POST":
        Username = request.POST.get('user')
        Password = request.POST.get('pass')
        U =authenticate(request,username=Username,password=Password)
        if U is not None:
            login(request,U)
            # request.session['username'] = user.username
            return redirect('/data')
        else:
            messages.error(request,'Invalid Username or password')
            
            print('\n\n invalid \n\n')
    return render(request,'register.html')        

def logout_request(request):
    # del request.session['username']
    logout(request)
    return redirect('home')

@csrf_exempt 
def home(request):
    # print('AL-Amir')
    # return HttpResponse('AL-AMIR ')
    # return render(request,'home.html')
    
    return render(request,'home.html') 



@login_required
def about(request):
    a = 10
    b = 12
    c = a+b
    return render (request,'about.html',{'Name':'Abu Quatada' ,'c':c})    

@login_required
def data(request):
    emp = Mecaps.objects.all() 
    print(emp)   
    Emp = []
    for e in emp:
        d = e.__dict__
        del(d['_state'])
        Emp.append(d)

    return render(request,'data.html',{'emp':Emp})

@csrf_exempt
@login_required
def insert(request):
    if request.method == 'POST':
        No = request.POST['no']
        Name = request.POST['name']
        Course  = request.POST['course']
        Contact = request.POST['contact']
        City = request.POST['city']
        objEmp = Mecaps(No,Name,Course,Contact,City)
        objEmp.save()
        return render(request,'insert.html') 

    return render(request,'insert.html') 

def delete(request ,id):
    emp = Mecaps.objects.get(s_no=id)
    emp.delete()
    return redirect('/data')  

@csrf_exempt

def update(request ,ID):
    
    if request.method == 'POST':
        No = request.POST['no']
        Name = request.POST['name']
        Course  = request.POST['course']
        Contact = request.POST['contact']
        City = request.POST['city']
        objEmp = Mecaps.objects.filter(s_no=ID).update(s_no=No,s_name=Name,
        course_name=Course,contact_no=Contact,city=City)
        
        return redirect('/data')    

    emp= Mecaps.objects.get(s_no=ID)  
    A = (emp.__dict__)
    # del(A['_state'])
    print('\n\n',A,'\n\n\'')
    return  render(request,'update.html',{'A':A})  
 