from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views import generic
from .models import User
import pandas as pd
from django.contrib import messages
import pywhatkit , time

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
   
def home(request): 
    return redirect('/profile') #profile
 
def signin(request):
    if request.user.is_authenticated:
         return redirect('/profile') #profile

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile') #profile
        else:
            msg = 'Error Login'
            form = AuthenticationForm(request.POST)
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

class profile(generic.ListView):
    template_name = 'profile.html'
    context_object_name = 'contact_list'

    def get_queryset(self):
       return User.objects.order_by('-id')
    
def signout(request):
    logout(request)
    return redirect('/')

def import_excel(request):
    return render(request, 'upload.html')  

def Export_excel(request):
    if request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'): 
          try:          
            df = pd.read_excel(excel_file)
            name = df['name']
            name_array = name.tolist()
            number = df['number']
            number_array = number.tolist()
            # number is duplicates or not findout
            myset = set(number_array)
            if len(number_array) == len(myset):
                print()  
            else:           
                return render(request, 'upload.html',{'error_message':' excel data  Number is duplicates' })              
            for i in number_array: 
                 vari = str(i)                 
                 if len(vari) == 10:
                     print()          
                 try:                
                     integer_number = int(i)
                     if integer_number == int(i):
                         print()
                     else:
                        return render(request, 'upload.html',{'error_message':' Number is not a number check you number' })                                                                               
                 except Exception as error:
                     return render(request, 'upload.html',{'error_message': 'check your excel data '})
            try:
                for i,j in zip(name_array,number_array):                                   
                    user = User.objects.filter(number=j).first()
                    if user:                       
                        continue              
                    else:           
                        varrible = User.objects.create(name=i,number=j)                   
                return redirect("/profile")  
            except Exception as error:
                return render(request, 'upload.html',{'error_message': 'This Number {} Is Already In The Data Base , Plese Remove This Number In Your Excel'.format(error)})                
          except Exception as error:
               return render(request, 'upload.html',{'error_message': 'Check your excel sheet input , set and mention name , number , message'}) 
        else:
            return render(request, 'upload.html', {'error_message': 'Invalid file format. Please upload an Excel file.'})
    else:
        return render(request, 'upload.html')  
    
def add_user(request):
    return render(request, 'contact_add.html')    
     
def add_user_method(request):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['number']        
        try:        
           User.objects.create(name=name, number=number)
        except Exception as error:
           return render(request, 'contact_add.html',{'error_message': 'this number is already in you database'})       
        return redirect("/profile") # http:127.0.0.1:8000/image_send
    # return render(request, 'signup.html')

def edit(request):
    if request.method == 'POST':
        id = request.POST['edit']
    member = User.objects.get(id=id)
    return render(request, 'edit.html',{'member':member})  

def edit_store(request):
    if request.method == "POST":
        id = request.POST['id']
    try:        
        phone = User.objects.get(id=id)
        new_name = request.POST.get('newname', None)
        new_number = request.POST.get('newnumber', None)
        if new_name:
            phone.name = new_name
        if new_number:
            phone.number = new_number
        try:
           try:    
              phone.save()
           except Exception as error:
              return render(request, 'edit.html',{'error_message': 'number is not a ten digit'})  
        except Exception as error:
           return render(request, 'edit.html',{'error_message': 'this number is already in you database'})    
        messages.success(request, "Updated successfully")
        return redirect("/profile")  # http:127.0.0.1:8000/image_send
    except User.DoesNotExist:
        messages.success(request, " Update does not exist with ID %s" % id)
        return redirect("/profile") # http:127.0.0.1:8000/image_send
  
def delete(request):
    if request.method == 'POST':
        id = request.POST['delete']    
    try:
       member = User.objects.get(id=id)
       member.delete()
       return redirect("/profile")
    except Exception as er:
        return redirect("/profile")
    
def upload_excel(request):
    return render(request, 'whatsapp_message.html')    

def message_send(request):
    if request.method == 'POST':
        Message = request.POST['message_text']
        Number_input = User.objects.all()
        sussess_message ='Message has been send success fully '
        error_message ='Message has been send fully check you number once'
        i=0
        try:
            if (Number_input[i] != ""):
                print()
        except Exception as err:
            return render(request, 'whatsapp_message.html',{'error_message':'add number in your db'})    
        for item in Number_input:
            array = item.number              
            try:                                          
                pywhatkit.sendwhatmsg_instantly('+91{}'.format(array),Message,20,tab_close=True)                                           
            except Exception as e:
                pywhatkit.sendwhatmsg_instantly('+91{}'.format(array),Message,35,tab_close=True)
                time.sleep(10)                                                                            
        return render(request, 'whatsapp_message.html',{'error_msg':sussess_message})   

    return render(request, 'whatsapp_message.html',{'error_message':error_message}) 

def image_send(request):
    if request.method == 'POST' and request.FILES['img']:
        upload_image = request.FILES['img']
        caption = request.POST['caption']
        Number_input = User.objects.all()
        sussess_message2 ='image has been send success fully '
        error_message2 ='wrong input check you image or phone numbers'
        i=0
        try:
            if (Number_input[i] != ""):
                print()
        except Exception as err:
            return render(request, 'whatsapp_message.html',{'error_message':'add number in your db'})   
        for item in Number_input:
            array = item.number 
            try:
                pywhatkit.sendwhats_image('+91{}'.format(array),upload_image,caption,20,tab_close=True)
                
            except Exception as ew:
                pywhatkit.sendwhats_image('+91{}'.format(array),upload_image,caption,35,tab_close=True)
                time.sleep(10)    
        return render(request, 'whatsapp_message.html',{'error_msg':sussess_message2})
    return render(request, 'whatsapp_message.html',{'error_message':error_message2})

def sendmsg_to_excel(request):
      return render(request, 'uploaded.html')

def senddata(request):
    if request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
          try:
            df = pd.read_excel(excel_file)
            number = df['number']
            number_array = number.tolist()
            message = df['message']
            message_array = message.tolist()
            myset = set(number_array)
            if len(number_array) == len(myset):
                print()
            else:
                return render(request, 'uploaded.html',{'error_message':' excel data  Number is duplicates' })
            for i in number_array:
                 vari = str(i)
                 if len(vari) == 10:
                     print()
                 try:
                     integer_number = int(i)
                     if integer_number == int(i):
                        print()
                     else:
                        return render(request, 'uploaded.html',{'error_message':' Number is not a number check you number' })
                 except Exception as error:
                     return render(request, 'uploaded.html',{'error_message': 'check your excel data '})
            for i,j in zip(number_array,message_array):
                try:
                    pywhatkit.sendwhatmsg_instantly('+91{}'.format(i),j,20,tab_close=True )
                    
                except Exception as er:
                    pywhatkit.sendwhatmsg_instantly('+91{}'.format(i),j,35,tab_close=True)
                    time.sleep(10)
            return redirect("/profile")
          except Exception as error:
               return render(request, 'uploaded.html',{'error_message': 'Check your excel sheet input , set and mention name , number , message'})
        else:
            return render(request, 'uploaded.html', {'error_message': 'Invalid file format. Please upload an Excel file.'})
    else:
        return render(request, 'uploaded.html')
    
