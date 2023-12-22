from django.shortcuts import render, redirect
from PlacementPredictionApp.models import *
import sweetify
import random
import base64
import json
import smtplib
from email.message import EmailMessage
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix

import os



# Create your views here.
def index(request):
    return render(request,'index.html')

def Login(request):
    if request.method == 'POST':
        UserID = request.POST["username"]
        Password = request.POST["password"]
        Flag=0
        Performances=PerformanceUpdate.objects.all().values()
        for perform in Performances:
            id=perform['userId']
            if perform['flag']==0:
                Flag+=1
        if UserID =="admin" and Password =="admin":
            sweetify.success(request, 'Success', text='Successfully Login ')
            return render(request,'College/home.html',{'Flag':Flag})
        else:
            sweetify.error(request, 'Opps', text='Invalid Credentials', persistent='OK')
            return render(request,'index.html')

def Logout(request):
    return render(request,'index.html')

def StudentManage(request):
    Dataset=[]
    StudentData=Student.objects.all().values()
    Dataset.extend(StudentData)
    Flag=0
    Performances=PerformanceUpdate.objects.all().values()
    for perform in Performances:
        id=perform['userId']
        if perform['flag']==0:
            Flag+=1
    return render(request,'College/StudentManage.html',{'Student':Dataset,'Flag':Flag})


def SaveStudent(request): 
    if request.method=='POST':
        Dataset=[]
        Name=request.POST['name']
        username=request.POST['username']
        Phone=request.POST['phone']
        Email=request.POST['email']
        Address=request.POST['address']
        Age=request.POST['age']
        gender=request.POST['gender']
        year=request.POST['year']
        fathername=request.POST['fathername']
        branch=request.POST['branch']
        sem=request.POST['sem']
        Image_File = request.FILES['images'].read()
     
        filename = "Student-"+str(random.randint(1000000000, 9999999999))+".jpg"

        if Student.objects.filter(contact=Phone).exists():
            sweetify.error(request, 'Error', text='Duplicate phone number')
        elif Student.objects.filter(email=Email).exists():
            sweetify.error(request, 'Error', text='Duplicate email')
        elif Student.objects.filter(username=username).exists():
            sweetify.error(request, 'Error', text='Duplicate username')
        else:
            with open('Media/Student/'+filename, 'wb') as f:
                 f.write(Image_File)
            
            data=Student(name=Name,contact=Phone,email=Email,address=Address,age=Age,username=username,Image=filename,gender=gender,fatherName=fathername,branch=branch,Semister=sem,year=year,password="")
            data.save()
            sweetify.success(request, 'Added', text='Successfully Added ', persistent='OK')
    
    StudentData=Student.objects.all().values()
    Dataset.extend(StudentData)
    Flag=0
    Performances=PerformanceUpdate.objects.all().values()
    for perform in Performances:
        id=perform['userId']
        if perform['flag']==0:
            Flag+=1
    return render(request,'College/StudentManage.html',{'Student':Dataset,'Flag':Flag})

def UpdateButton(request):
     if request.method == 'GET':
        print('reached')
        Id = request.GET["Id"]
        flag = request.GET["flag"]
        print(Id,flag)
        Student.objects.filter(id=Id).update(is_enabled=flag)
    
     return HttpResponse(Id)

def StudentLoginpage(request):
    return render(request,'Student/login.html')

def StudentRegister(request):
    return render(request,'Student/Register.html')

def Createaccount(request):
    if request.method=='POST':
        Name=request.POST['name']
        username=request.POST['user']
        email=request.POST['email']
        
        if Student.objects.filter(name=Name,username=username,email=email,is_register=0).exists():
            password = username+"@"+str(random.randint(1000, 9999))
            SendEmail(email,password,username)
            Student.objects.filter(username=username).update(is_register=1,password=password)
            # sweetify.success(request, 'Added', text='Please check your email for login credentials ', persistent='OK')
            return render(request,'Student/Register.html', {'success':'Please check your email for login credentials'})
        elif Student.objects.filter(name=Name,username=username,email=email,is_register=1).exists():
            return render(request,'Student/Register.html',{'error':'Already Registered'})

        else:
            # sweetify.error(request, 'Error', text='Invalid credentials')
            return render(request,'Student/Register.html',{'error':'Invalid credentials'})

def SendEmail(email,password,username):
    msg = EmailMessage()
    messageBody='USN: '+username+'\n\n'+'Password: '+password
    msg.set_content(messageBody)

    msg['Subject'] = 'Login Credentials'
    msg['From'] = "srinivassit123@gmail.com"
    msg['To'] = email

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("srinivassit123@gmail.com", "sudfvksokqinzogg")
    server.send_message(msg)
    server.quit()

def Studentlogin(request):
    if request.method=='POST':
      username=request.POST['username']
      password=request.POST['password']
      
      Data=Student.objects.filter(username=username,password=password).values()
      if not Data:
        return render(request,'Student/login.html',{'error':'Invalid user'})
      else:
        for data in Data:
            is_enabled=data['is_enabled']
            request.session['id']=data['id']
            if is_enabled==0:
              return render(request,'Student/login.html',{'error':'Please Contact admin'})
            else:
             return render(request,'Student/Home.html',{'username':username})

def StudentAccount(request):
    Dataset=[]
    id=request.session['id']
    StudentData=Student.objects.filter(id=id).values()
    Dataset.extend(StudentData)
    return render(request,'Student/Account.html',{'Student':Dataset})


def editAccount(request):
    if request.method=="GET":
         ids=request.GET['id']
         data=[]
         StudentData=Student.objects.all().filter(id=ids).values()
         data.extend(StudentData) 
    return HttpResponse(json.dumps(data), content_type="application/json") 


def updateAccount(request):
    if request.method=="POST":
        Name=request.POST['name']
        username=request.POST['username']
        Phone=request.POST['phone']
        Email=request.POST['email']
        Address=request.POST['address']
        Age=request.POST['age']
        gender=request.POST['gender']
        year=request.POST['year']
        fathername=request.POST['fathername']
        branch=request.POST['branch']
        sem=request.POST['sem']
        id=request.POST['id']
        Image=request.POST['img']
        
        
        if len(request.FILES) !=0:
            if len(request.FILES['images']) > 0:
                 with open('Media/Student/'+Image, 'wb') as f:
                    f.write(request.FILES['images'].read())
            else:
               print('Updated')    

        Student.objects.filter(id=id).update(name=Name,contact=Phone,email=Email,address=Address,age=Age,username=username,gender=gender,fatherName=fathername,branch=branch,Semister=sem,year=year)
        sweetify.success(request, 'Success', text='Successfully Updated ', persistent='OK')

    Dataset=[]
    id=request.session['id']
    StudentData=Student.objects.filter(id=id).values()
    Dataset.extend(StudentData)
    return render(request,'Student/Account.html',{'Student':Dataset})    

def Performances(request):
    Dataset=[]
    Flag=0
    Performances=PerformanceUpdate.objects.all().values()
    for perform in Performances:
        id=perform['userId']
        if perform['flag']==0:
            Flag+=1
    StudentData=Student.objects.all().values()
    Dataset.extend(StudentData)
    return render(request,'College/StudentPerformance.html',{'Student':Dataset,'Flag':Flag})

def SavePerformance(request):
    if request.method=="POST":
        sslc=request.POST['sslc']
        Studentid=request.POST['name']
        puc=request.POST['puc']
        be_cgpa=request.POST['becgpa']
        deploma=request.POST['deploma']
        be_percentage=request.POST['BE_PERCENTAGE']
        backlog=request.POST['Backlogs']
        cocubes_total=request.POST['Cocubes']
        aptitude=request.POST['APTITUDE']
        english=request.POST['ENGLISH']
        quantitative=request.POST['QUANTITATIVE']
        compuer_fundamental=request.POST['Computer']
        analytical=request.POST['ANALYTICAL']
        coding=request.POST['CODING']
        domain=request.POST['DOMAIN']
        written_english=request.POST['writtenEnglish']

        if Performance.objects.filter(StudentId=Studentid).exists():
            sweetify.error(request, 'Opps..', text='Duplicate Record', persistent='OK') 
        else:
            data=Performance(StudentId=Studentid,Sslc=sslc,Puc=puc,Be_cgpa=be_cgpa,Deploma=deploma,Be_percentage=be_percentage,Backlog=backlog,Cocubes_total=cocubes_total,Aptitude=aptitude,English=english,Quantitative=quantitative,Compuer_fundamental=compuer_fundamental,Analytical=analytical,Coding=coding,Domain=domain,Written_english=written_english)
            data.save()
            sweetify.success(request, 'Added', text='Successfully Added ', persistent='OK') 
     
    Dataset=[]
    StudentData=Student.objects.all().values()
    Dataset.extend(StudentData)
    Flag=0
    Performances=PerformanceUpdate.objects.all().values()
    for perform in Performances:
        id=perform['userId']
        if perform['flag']==0:
            Flag+=1
    return render(request,'College/StudentPerformance.html',{'Student':Dataset,'Flag':Flag})


def StudentPerformance(request):
    if not request.session.has_key('id'):
        return redirect('/StudentLoginpage/')
    id=request.session['id']
    Dataset=[]
    response = {}
    performanceList = []
    
    isFinalStudent = 0
    student_data = Student.objects.get(id=id)
    if not student_data == None:
        isFinalStudent = 1 if int(student_data.Semister) > 4 else 0

    Performances=Performance.objects.filter(StudentId=id).values()
    Dataset.extend(Performances)

    if len(Dataset) > 0:
        # Performance Data
        performanceList.append({"isEdit": 0, "title": "SSLC", "key": "Sslc", "value": Dataset[0]['Sslc']})
        performanceList.append({"isEdit": 0, "title": "PUC", "key": "Puc", "value": Dataset[0]['Puc']})
        performanceList.append({"isEdit": 0, "title": "BE CGPA", "key": "Be_cgpa", "value": Dataset[0]['Be_cgpa']})
        performanceList.append({"isEdit": 0, "title": "Diploma", "key": "Deploma", "value": Dataset[0]['Deploma']})
        performanceList.append({"isEdit": 0, "title": "BE Percentage", "key": "Be_percentage", "value": Dataset[0]['Be_percentage']})
        performanceList.append({"isEdit": 0, "title": "Backlog", "key": "Backlog", "value": Dataset[0]['Backlog']})
        performanceList.append({"isEdit": 1, "title": "Aptitude", "key": "Aptitude", "value": Dataset[0]['Aptitude']})
        performanceList.append({"isEdit": 1, "title": "English", "key": "English", "value": Dataset[0]['English']})
        performanceList.append({"isEdit": 1, "title": "Quantitative", "key": "Quantitative", "value": Dataset[0]['Quantitative']})
        performanceList.append({"isEdit": 1, "title": "Computer Fundamental", "key": "Compuer_fundamental", "value": Dataset[0]['Compuer_fundamental']})
        performanceList.append({"isEdit": 1, "title": "Analytical", "key": "Analytical", "value": Dataset[0]['Analytical']})
        performanceList.append({"isEdit": 1, "title": "Coding", "key": "Coding", "value": Dataset[0]['Coding']})
        performanceList.append({"isEdit": 1, "title": "Domain", "key": "Domain", "value": Dataset[0]['Domain']})
        performanceList.append({"isEdit": 1, "title": "Written English", "key": "Written_english", "value": Dataset[0]['Written_english']})
        performanceList.append({"isEdit": 1, "title": "Cocubes Total", "key": "Cocubes_total", "value": Dataset[0]['Cocubes_total']})

        response = {
            "id": Dataset[0]['id'],
            "student_id": Dataset[0]['StudentId'],
            "performance_list": performanceList,
            "is_final_student": isFinalStudent
        }

    return render(request,'Student/Performance.html', response)

@csrf_exempt
def PerformUpdateRequest(request):
    if request.method=="POST":
        print('reached')
        Id=request.POST['id']
        Field=request.POST['Field']
        field_key=request.POST['field_key']
        field_value=request.POST['field_value']
        if PerformanceUpdate.objects.filter(Field=Field,userId=Id,flag=0).exists():
            # sweetify.error(request, 'Opps..', text='Please Contact admin', persistent='OK')
            res='Please Contact admin'
        else:    
            PerformanceUpdate(Field=Field,userId=Id,field_key=field_key,field_value=field_value).save() 
            # sweetify.success(request, 'Sucess', text='Update request Successfully sent' , persistent='OK') 
            res='Update request Successfully sent'
    
    return HttpResponse(res)


@csrf_exempt
def UpdatePerform(request):
    if request.method=="POST":
        Id=request.POST['id']
        Field=request.POST['Field']
        values=request.POST['val']
        key=request.POST['key']

        Data=PerformanceUpdate.objects.filter(Field=Field,userId=Id).values()
        if len(Data) > 0:
            Performid=Data[0]['id']
            PerformanceUpdate(id=Performid).delete()
        p = Performance.objects.get(StudentId=Id)
        setattr(p, key, values) # f.foo=bar
        p.save()

        res='Success' 
    return HttpResponse(res)

def UpdateRequests(request):
    Dataset=[]
    Dta=[]
    Flag=0
    # id=request.session['id']
    Performances=PerformanceUpdate.objects.all().values()
    for perform in Performances:
        id=perform['userId']
        if perform['flag']==0:
            Flag+=1
        Data=Student.objects.filter(id=id).values()
        Name=Data[0]['name']
        Phone=Data[0]['contact']
        Branch=Data[0]['branch']
        res={
            'student_id': Data[0]['id'],
            'name':Name,
            'contact':Phone,
            'Branch':Branch,
            'flag':perform['flag'],
            'Field':perform['Field'],
            'field_key': perform['field_key'],
            'field_value': perform['field_value'],
            'count':Flag,
            'id':perform['id'],

        }
        Dta.append(res)

        

    Dataset.extend(Dta)
    return render(request,'College/PerformUpdateRequest.html',{'Performance':Dataset,'Flag':Flag})

@csrf_exempt
def ApproveRequest(request):  
    # if request.method == 'GET':
    #     print('reached')
    #     Id = request.GET["Id"]
    #     flag = request.GET["flag"]
    #     print(Id,flag)
    #     PerformanceUpdate.objects.filter(id=Id).update(flag=flag)
    if request.method=="POST":
        student_id=request.POST['student_id']
        perform_id=request.POST['perform_id']
        field=request.POST['field']
        key=request.POST['key']
        value=request.POST['value']

        Data=PerformanceUpdate.objects.filter(Field=field,userId=student_id).values()
        Performid=Data[0]['id']
        PerformanceUpdate(id=Performid).delete()

        p = Performance.objects.get(StudentId=student_id)
        setattr(p, key, value) # f.foo=bar
        p.save()

        res='Success' 
    return HttpResponse(res)
    # return HttpResponse(Id)     

@csrf_exempt
def importStudents(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']
        recordCount = 0
        duplicateStudentCount = 0
        savedStudentCount = 0
        df = pd.read_excel(excel_file)

        for index, row in df.iterrows():
            student_name = row['Student Name']
            contact_no = row['Contact no']
            email_id = row['Email ID']
            address = row['Address']
            age = row['Age']
            username = row['USN']
            gender = row['Gender']
            father_name = row['Father Name']
            branch = row['Branch']
            semister = row['Semister']
            year = row['Year']
            recordCount += 1

            if Student.objects.filter(contact=contact_no).exists():
                duplicateStudentCount += 1
            elif Student.objects.filter(email=email_id).exists():
                duplicateStudentCount += 1
            elif Student.objects.filter(username=username).exists():
                duplicateStudentCount += 1
            else:
                data=Student(name=student_name,contact=contact_no,email=email_id,address=address,age=age,username=username,Image="",gender=gender,fatherName=father_name,branch=branch,Semister=semister,year=year,password="")
                data.save()
                savedStudentCount += 1
            
        print('Total Records: ', recordCount)
        print('Duplicate Students: ', duplicateStudentCount)
        print('Saved Students: ', savedStudentCount)

    return redirect('/StudentManage/')

def studentPrediction(request, id):
    performanceList = []
    student_data = Student.objects.get(id=id)
    performance_data=Performance.objects.filter(StudentId=id).values()

    performanceList.append(performance_data[0]['Sslc'])
    performanceList.append(performance_data[0]['Puc'])
    performanceList.append(performance_data[0]['Deploma'])
    performanceList.append(performance_data[0]['Be_cgpa'])
    performanceList.append(performance_data[0]['Be_percentage'])
    performanceList.append(performance_data[0]['Backlog'])
    performanceList.append(performance_data[0]['Cocubes_total'])
    performanceList.append(performance_data[0]['Aptitude'])
    performanceList.append(performance_data[0]['English'])
    performanceList.append(performance_data[0]['Quantitative'])
    performanceList.append(performance_data[0]['Analytical'])
    performanceList.append(performance_data[0]['Domain'])
    performanceList.append(performance_data[0]['Compuer_fundamental'])
    performanceList.append(performance_data[0]['Coding'])
    performanceList.append(performance_data[0]['Written_english'])
    
    print(performanceList)
    print(student_data.branch)

    dataset_file = ''
    if student_data.branch in ['Computer Science', 'Information Science', 'Eletrical', 'Electronics']:
        dataset_file = 'project_data_EC.csv'
    if student_data.branch in ['Aeronautical', 'Automobile']:
        dataset_file = 'AE.csv'
    if student_data.branch in ['Mechanical', 'Marine']:
        dataset_file = 'Dataset_MECH.csv'

    print(dataset_file)

    dataset=pd.read_csv(dataset_file)
    X=np.array(dataset.iloc[:,:-1])
    X=X.astype(dtype='int')
    Y=np.array(dataset.iloc[:,-1])
    # Y=Y.astype(dtype='str')
    Y=Y.reshape(-1,)
    # print(X)
    # print(Y)
    # print(Y.shape)
    X_train, X_test, y_train, y_test =train_test_split(X,Y,test_size=0.25,random_state=42)

    # print(X_train.shape)
    model_RR=RandomForestClassifier(n_estimators=100,criterion='entropy',)
    model_RR.fit(X_train,y_train)
    a = np.array(performanceList)
    # y_predicted_RR=model_RR.predict(performanceList)
    y_predicted_RR=model_RR.predict(a.reshape(1, -1))
    print(y_predicted_RR)

    result_list = y_predicted_RR[0].split('/')
    # confusion=confusion_matrix(y_test,y_predicted_RR)
    # print('Accuracy :')
    # print(accuracy_score(y_test,y_predicted_RR))

    # return redirect('/StudentPerformance/')
    return render(request, 'Student/prediction_result.html', {"result_list": result_list})

def improveSkill(request):
    return render(request, 'Student/improve_skill.html')

def preperationOne(request):
    return render(request, 'Student/preperation_one.html')
def preperationTwo(request):
    return render(request, 'Student/preperation_two.html')

def aboutCampus(request):
    company_data = []
    myfiles = [f for f in os.listdir('./media/Company/')]
    for file_name in myfiles:
        company_name = os.path.splitext(file_name)[0]
        company_data.append(
            {"company_name": company_name, "company_file": file_name}
        )
    return render(request, 'Student/about_campus.html', {"company_data": company_data})

