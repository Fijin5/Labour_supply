from sqlite3 import dbapi2
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from LabourApp import dbconnection
from django.core.files.storage import FileSystemStorage
from datetime import datetime,date
import random,string

# Create your views here.
def home(request):
    return render(request,'home.html',{})
def login(request):
    if request.method=='POST':
        us=request.POST['usercode']
        ps=request.POST['pass']
        sql="SELECT * FROM `logindata` WHERE  username='"+us+"' and password='"+ps+"' "
        a=dbconnection.singlerow(sql)
        d=datetime.now()
        time=d.strftime("%H:%M:%S")
        dat=date.today()
        # sql1="INSERT INTO `loginstatus`(`Staff`, `Login_date`, `Login_Time`,`Status`) VALUES('"+us+"','"+str(dat)+"','"+time+"',0)"
        # dbconnection.addrow(sql1)
        # if a:
        #     request.session['usercode']=us
        #     if a[3]=='agency':
        #         return HttpResponseRedirect("http://127.0.0.1:8000/AgencyHome")
        #     elif a[3]=='admin':
        #         return HttpResponseRedirect("http://127.0.0.1:8000/AdminHome")
        #     elif a[3]=='user':
        #         return HttpResponseRedirect("http://127.0.0.1:8000/UserHome")
        #     elif a[3]=='police':
        #         return HttpResponseRedirect("http://127.0.0.1:8000/PoliceHome")
        # else:
        #     msg="invalid user or password"
        #     return render(request,'login.html',{'msg':msg})

        if a:
            request.session['usercode']=us
            if a[3]=='agency':
                sql1="INSERT INTO `loginstatus`( `personId`, `date_login`, `status`) VALUES ('"+us+"','"+str(dat)+"',0)"
                dbconnection.addrow(sql1)
                return HttpResponseRedirect("http://127.0.0.1:8000/AgencyHome")
            elif a[3]=='admin':
                sql1="INSERT INTO `loginstatus`( `personId`, `date_login`, `status`) VALUES ('"+us+"','"+str(dat)+"',0)"
                dbconnection.addrow(sql1)
                return HttpResponseRedirect("http://127.0.0.1:8000/AdminHome")
            elif a[3]=='user':
                sql1="INSERT INTO `loginstatus`( `personId`, `date_login`, `status`) VALUES ('"+us+"','"+str(dat)+"',0)"
                dbconnection.addrow(sql1)
                return HttpResponseRedirect("http://127.0.0.1:8000/UserHome")
            elif a[3]=='police':
                sql1="INSERT INTO `loginstatus`( `personId`, `date_login`, `status`) VALUES ('"+us+"','"+str(dat)+"',0)"
                dbconnection.addrow(sql1)
                return HttpResponseRedirect("http://127.0.0.1:8000/PoliceHome")
        else:
            msg="invalid user or password"
            return render(request,'login.html',{'msg':msg})
        
    return render(request,'login.html',{})
def logout(request):
    username=request.session['usercode']
    sql="select * from logindata where username='"+username+"' "
    data=dbconnection.singlerow(sql)
    d=datetime.now()
    time=d.strftime("%H:%M:%S")
    sql1="UPDATE `loginstatus` SET `Status`=1 where personId='"+username+"'and Status=0 "
    dbconnection.addrow(sql1)
    return HttpResponseRedirect("http://127.0.0.1:8000/login")
def AgencyReg(request):
    d=datetime.now()   
    dat=date.today()
    if request.POST.get('register'):
        AgencyName=request.POST['agency_name']
        RegNum=request.POST['reg_num']
        StateReg=request.POST['state_reg']
        Addr=request.POST['addr']
        City=request.POST['city']
        State=request.POST['state']
        Distri=request.POST['distri']
        Pin=request.POST['pin']
        ContPerson=request.POST['cont']
        PhoneNum=request.POST['phn']
        Uni_Ag_Code=request.POST['uni']
        Email=request.POST['email']
        Passw=request.POST['pasw']
        BankName=request.POST['bankname']
        BankAddr=request.POST['bankaddr']
        AcountNumber=request.POST['acuntnum']
        AgenName_Branch=request.POST['agnam_Branch']
        sq="SELECT * FROM logindata WHERE username='"+Uni_Ag_Code+"'"
        a=dbconnection.singlerow(sq)
        if a:
            return render(request,'UserReg.html',{'msg':'UserName Already Exist'})  
        else:
            sql="INSERT INTO `agency_details`(`Agency_Name`, `Reg_No`, `Date_Reg`, `State_Reg`, `Address`, `City`, `State`, `District`, `Pincode`, `Contact_Person`, `Phn_no`, `Email`, `Password`, `Uni_Agen_Code`,`Delete_Status`) VALUES('"+AgencyName+"','"+RegNum+"','"+str(dat)+"','"+StateReg+"','"+Addr+"','"+City+"','"+State+"','"+Distri+"','"+Pin+"','"+ContPerson+"','"+PhoneNum+"','"+Email+"','"+Passw+"','"+Uni_Ag_Code+"',0)"
            dbconnection.addrow(sql)
            sql="INSERT INTO `ag_bank_details`(`Bank_Name`, `Account_No`, `Branch_address`, `AgBranch_Name`,`Delete_Status`) VALUES ('"+BankName+"','"+AcountNumber+"','"+BankAddr+"','"+AgenName_Branch+"',0)" 
            dbconnection.addrow(sql)
            sql1="INSERT INTO `logindata`(`username`, `password`, `utype`) VALUES  ('"+Uni_Ag_Code+"','"+Passw+"','agency')"
            dbconnection.addrow(sql1)
    return render(request,'Admin/AgencyReg.html',{})
def UserReg(request):
    d=datetime.now()   
    dat=date.today()
    if request.POST.get('register'):
        UserName=request.POST['name']
        Addr=request.POST['addr']
        PhnNum=request.POST['phn']
        Photo=request.FILES['photo']
        fs=FileSystemStorage()
        fn=fs.save('LabourApp/static/upload/'+Photo.name,Photo)
        Email=request.POST['email']
        Passw=request.POST['pasw']
        Usercode=request.POST['usercode']
        sq="SELECT * FROM logindata WHERE username='"+Usercode+"'"
        a=dbconnection.singlerow(sq)
        if a:
            return render(request,'UserReg.html',{'msg':'UserName Already Exist'})  
        else:
            sql="INSERT INTO `user_details`(`User_Name`, `Address`, `Phn_Num`, `Email`, `User_code`, `Password`, `Photo`, `Delete_Status`) VALUES ('"+UserName+"','"+Addr+"','"+PhnNum+"','"+Email+"','"+Usercode+"','"+Passw+"','"+Photo.name+"',0)"
            dbconnection.addrow(sql)
            sql="INSERT INTO `logindata`(`username`, `password`, `utype`) VALUES  ('"+Usercode+"','"+Passw+"','user')"
            dbconnection.addrow(sql)
    return render(request,'UserReg.html',{})   

def LabourReg(request):
    d=datetime.now()   
    dat=date.today()
    username=request.session['usercode']
    if request.method=='POST':
        LabourName=request.POST['name']
        LabourCode=request.POST['labourcode']
        dob=request.POST['dob']
        Addr=request.POST['address']
        City=request.POST['city']
        State=request.POST['state']
        Distri=request.POST['district']
        Pin=request.POST['pin']  
        PhoneNum=request.POST['phn']
        Aadhar=request.POST['aadhar']
        Photo=request.FILES['photo']
        fs=FileSystemStorage()
        fn=fs.save('LabourApp/static/upload/'+Photo.name,Photo)
        sq="SELECT * FROM labour_details WHERE Labour_code='"+LabourCode+"'"
        a=dbconnection.singlerow(sq)
        if a:
            return render(request,'Agency/LabourReg.html',{'msg':'UserName Already Exist'})  
        else:
            sql="INSERT INTO `labour_details`(`Labour_Name`, `Labour_code`, `date_reg`, `DOB`, `Address`, `City`, `State`, `District`, `Pincode`, `Phn_no`, `AdhharNumber`, `photo`, `AvailStatus`, `Delete_Status`, `status`, `AddAgency`) VALUES   ('"+LabourName+"','"+LabourCode+"','"+str(dat)+"','"+dob+"','"+Addr+"','"+City+"','"+State+"','"+Distri+"','"+Pin+"','"+PhoneNum+"','"+Aadhar+"','"+Photo.name+"',0,0,0,'"+username+"')"
            dbconnection.addrow(sql)
    return render(request,'Agency/LabourReg.html',{})  
def AgencyDetails(request):
    sql="SELECT * FROM  `Agency_details` "
    agen=dbconnection.allrow(sql)
    return render(request,'Admin/Agencydetails.html',{'agen':agen})
def Labourdetails(request):
    rid=request.GET['aid']
    sql="SELECT * FROM  `Labour_details` WHERE AddAgency='"+rid+"' "
    lab=dbconnection.allrow(sql)
    return render(request,'Admin/LabourDetails.html',{'lab':lab})
def LabourVeri(request):
    sql1="select * from `labour_details` where status=0"
    lab=dbconnection.allrow(sql1)
    return render(request,'Police/LabourVeri.html',{'lab':lab})
def LabourAccept(request):
    sql1="select * from `labour_details` where status=0"
    lab=dbconnection.allrow(sql1)
    LabId=request.GET['Lid']
    sql1="UPDATE `labour_details` SET status=1 where Labid='"+LabId+"'"
    dbconnection.addrow(sql1)
    return render(request,'Police/LabourVeri.html',{'lab':lab})
# def LabourReject(request):
#     return render(request,'LabourVeri.html',{})

def PostRequire(request):
    Usercode=request.session['usercode']
    sql="SELECT * FROM `user_details` WHERE User_code='"+Usercode+"' "
    user=dbconnection.singlerow(sql)
    sql2="SELECT * FROM Agency_details"
    ag=dbconnection.allrow(sql2)
    d=datetime.now()   
    dat=date.today()
    # sql="select *from requirements ORDER BY req_id DESC LIMIT 1"
    # req=dbconnection.singlerow(sql)
    # if request.method=='POST':
    if request.POST.get('register'):    
        Agency=request.POST['age']
        UserCode=request.POST['usercode']
        City=request.POST['city']
        District=request.POST['district']
        Require=request.POST['require']
        Worksite=request.POST['worksite']
        Workers=request.POST['workers']
        FromDate=request.POST['from_date'] 
        ToDate=request.POST['to_date'] 
        Amt=request.POST['amt'] 
        sql="INSERT INTO `requirements`(`Agency`, `UserCode`, `Date_req`, `Requirement`, `WorkSite`, `District`, `City`, `No_of_Labourer`, `From_Date`, `To_Date`, `Amt`, `RegStatus`, `AcceptStatus`, `AssignStatus`) VALUES ('"+Agency+"','"+UserCode+"','"+str(dat)+"','"+Require+"','"+Worksite+"','"+District+"','"+City+"','"+Workers+"','"+FromDate+"','"+ToDate+"','"+Amt+"',0,'0',0)"
        dbconnection.addrow(sql)
        sql="select *from requirements ORDER BY req_id DESC LIMIT 1"
        req=dbconnection.singlerow(sql)
        sql1="select DATEDIFF( To_date, From_date)  from requirements ORDER BY req_Id DESC LIMIT 1"
        data1=dbconnection.singlerow(sql1)
        tot=data1[0]*req[8]*req[11]
        
        return render(request,'User/PostRequire.html',{'user':user,'ag':ag,'req':req,'tot':tot})
    elif request.POST.get('Accept'):
        sql="select *from requirements ORDER BY req_id DESC LIMIT 1"
        req=dbconnection.singlerow(sql) 
        sql="UPDATE `requirements` SET `RegStatus`=1,AcceptStatus='requested' where Req_id='"+str(req[0])+"'"
        dbconnection.addrow(sql)
        
        return render(request,'User/PostRequire.html',{'user':user,'ag':ag,'req':req})
        # return HttpResponseRedirect("http://127.0.0.1:8000/PostRequire")
    
    return render(request,'User/PostRequire.html',{'user':user,'ag':ag})
# def RegAccept(request):
#     rid=request.GET['Lid']
#     sql="UPDATE `requirements` SET `RegStatus`=1 where Req_id='"+rid+"'"
#     dbconnection.addrow(sql)
    # return HttpResponseRedirect('http://127.0.0.1:8000/PostRequire')
def SearchLabour(request):
    sql="SELECT * FROM `labour_details`where status=1"
    lab=dbconnection.allrow(sql)
    return render(request,'Admin/SearchLabour.html',{'lab':lab})
def SearchLabour2(request):
    rid=request.GET['aid']
    sql="SELECT * FROM labour_details Where Labid='"+rid+"' "
    Lab=dbconnection.singlerow(sql)
    return render(request,'Admin/SearchLabour2.html',{'Lab':Lab})
def UserRequest(request): 
    sql="SELECT *,user_details.user_name FROM `requirements` INNER JOIN Agency_details ON requirements.Agency=Agency_details.Uni_Agen_code  INNER JOIN user_details ON requirements.UserCode=user_details.user_code  where RegStatus=1"
    req=dbconnection.allrow(sql)
    return render(request,'Admin/UserRequest.html',{'req':req})
def AssignLabour(request):
    username=request.session['usercode']
    # sql="SELECT * FROM `requirements`"
    # req=dbconnection.allrow(sql)
    # sql="SELECT requirements.Req_id,user_details.Photo, requirements.UserCode, user_details.User_Name,user_details.Phn_Num,requirements.Requirement,requirements.WorkSite,requirements.No_of_Labourer,requirements.From_date,requirements.To_date,DATEDIFF( requirements.To_date, From_date),requirements.AcceptStatus FROM requirements INNER JOIN user_details ON requirements.UserCode=user_details.User_code where AssignStatus=0 and RegStatus=1 and Agency='"+username+"'"
    sql="SELECT requirements.Req_id,user_details.Photo, requirements.UserCode, user_details.User_Name,user_details.Phn_Num,requirements.Requirement,requirements.WorkSite,requirements.No_of_Labourer,requirements.From_date,requirements.To_date,DATEDIFF( requirements.To_date, From_date),requirements.AcceptStatus FROM requirements INNER JOIN user_details ON requirements.UserCode=user_details.User_code where  RegStatus=1 and Agency='"+username+"'"

    req=dbconnection.allrow(sql)
    # if request.POST.get('Accept'):
    #     sql="SELECT requirements.Req_id,user_details.Photo, requirements.UserCode, user_details.User_Name,user_details.Phn_Num,requirements.Requirement,requirements.WorkSite,requirements.No_of_Labourer,requirements.From_date,requirements.To_date,DATEDIFF( requirements.To_date, From_date)FROM requirements INNER JOIN user_details ON requirements.UserCode=user_details.User_code where AssignStatus=0 and RegStatus=1 and Agency='"+username+"'"
    #     req=dbconnection.allrow(sql)
    #     sql="UPDATE `requirements` SET AcceptStatus=1 where Req_id='"+str(req[0])+"'"
    #     dbconnection.addrow(sql)
    return render(request,'Agency/AssignLabour.html',{'req':req})
def ReqAccept(request):
    username=request.session['usercode']
    rid=request.GET['aid']
    sql="UPDATE `requirements` SET AcceptStatus='Accepted' where Req_id='"+rid+"'"
    dbconnection.addrow(sql)
    return HttpResponseRedirect('http://127.0.0.1:8000/AssignLabour')
def ReqReject(request):
    rid=request.GET['aid']
    sql="UPDATE `requirements` SET AcceptStatus='Pending' where Req_id='"+rid+"'"
    dbconnection.addrow(sql)
    return HttpResponseRedirect('http://127.0.0.1:8000/AssignLabour')
def AssignLabour1(request):
    username=request.session['usercode']
    # sql="SELECT * FROM labour_details "
    # lab=dbconnection.allrow(sql)
    rid=request.GET['aid']
    if request.POST.get('check'):
        workdate=request.POST['dat']
        sql="SELECT * FROM labour_details WHERE NOT EXISTS(SELECT * FROM labour_assign WHERE labour_details.labour_code = labour_assign.labourer_code and labour_assign.Date_Work='"+workdate+"')and status=1 and AddAgency='"+username+"'"
        # sql="select Labour_name,Labour_code from labour_details where not exists(select * from labour_assign Where labour_details.labour_code=labour_assign.Labourer_code)"
        lab=dbconnection.allrow(sql)
        # sql2="SELECT * FROM Labour_assign"
        # ass=dbconnection.allrow(sql2)
        # rid=request.GET['aid']
        # sql="SELECT * FROM requirements WHERE Req_id='"+rid+"'"
        # req=dbconnection.singlerow(sql)
        # worksite=req[5]
        # # fromdate=req[8]
        # # todate=req[9]
        # require=req[4]
        # user=req[2]
        return render(request,'Agency/AssignLabour1.html',{'lab':lab})
    if request.POST.get('assign'):
        
        rid=request.GET['aid']
        sql="SELECT * FROM requirements WHERE Req_id='"+rid+"'"
        req=dbconnection.singlerow(sql)
        worksite=req[5]
        # # fromdate=req[8]
        # # todate=req[9]
        require=req[4]
        user=req[2]
        workdate=request.POST['dat']
        labr=request.POST.getlist('lab')
        for i in labr:
            sql="INSERT INTO `labour_assign`(`Date_Work`, `Labourer_code`, `Worksites`, `Requirement`, `User_code`, `AddBy`) VALUES  ('"+str(workdate)+"','"+i+"','"+worksite+"','"+require+"','"+user+"','"+username+"')"
            dbconnection.addrow(sql)
            # sql1="UPDATE `labour_details` SET AvailStatus=0 where Labour_code='"+i+"'"
            # dbconnection.addrow(sql1)
            sql1="UPDATE `requirements` SET AssignStatus=1 where Req_id='"+rid+"'"
            dbconnection.addrow(sql1)
            # sql="INSERT INTO `labour_assign`(`Work_Id`, `Worksites`, `From_Date`, `To_date`, `LabourCode`, `requirements`, `UserId`, `AssignStatus`, `agency`) VALUES"
        return render(request,'Agency/AssignLabour1.html',{'req':req})
    # sql="SELECT labour_details.Labour_Name,labour_assign.WorkSite,labour_assign.From_date,labour_assign.To_date FROM labour_assign INNER JOIN labour_details ON labour_assign.LabourId=labour_details.Labour_Name"
    # lab=dbconnection.allrow(sql)
    return render(request,'Agency/AssignLabour1.html',{})
def LabAssignDetails(request):
    # rid=request.GET['aid']
    # uid=request.GET['bid']
    # reid=request.GET['cid']
    # # did=request.GET['aid']
    # sql="SELECT distinct date_work from Labour_assign Where User_Code='"+uid+"'and requirement='"+reid+"'"
    # data=dbconnection.allrow(sql)
    rid=request.GET['aid']
    uid=request.GET['bid']
    reid=request.GET['cid']
    # did=request.GET['aid']
    sql="SELECT distinct date_work from Labour_assign Where User_Code='"+uid+"'and requirement='"+reid+"'"
    data=dbconnection.allrow(sql)
    return render(request,'Agency/LabourAssignDetails.html',{'data':data})
def Labour(request):
    rid=request.GET['aid']
    sql="select Labourer_code from labour_assign where date_work='"+rid+"'"
    data1=dbconnection.allrow(sql)
    return render(request,'Agency/LabourAssignDetails.html',{'data1':data1,'rid':rid})

def SearchSite(request):
    username=request.session['usercode']
    sql="SELECT * FROM requirements WHERE AcceptStatus='Accepted' and Agency='"+username+"'"
    data=dbconnection.allrow(sql)
    if request.method=='POST':
        Site=request.POST['sit']
        sql="SELECT requirements.worksite,requirements.Requirement,labour_assign.Labourer_Code,labour_details.Labour_Name,requirements.No_of_Labourer FROM requirements INNER JOIN labour_assign ON requirements.worksite=labour_assign.Worksites INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code  WHERE Requirement='"+Site+"' ORDER BY Date_Work"
        # sql="SELECT * FROM labour_assign WHERE Requirement='"+Site+"'"
        sql="SELECT labour_assign.requirement,labour_assign.worksites,labour_details.labour_name,labour_assign.Labourer_code,labour_assign.Date_Work FROM labour_assign INNER JOIN labour_details ON labour_assign.Labourer_code=labour_details.labour_code WHERE requirement='"+Site+"'"
        site=dbconnection.allrow(sql)
        return render(request,'Agency/SearchSite.html',{'data':data,'site':site})
    return render(request,'Agency/SearchSite.html',{'data':data})
def SearchStaff(request):
    username=request.session['usercode']
    sql="SELECT * FROM  labour_details WHERE status=1 and AddAgency='"+username+"'"
    data=dbconnection.allrow(sql)
    if request.method=='POST':
        Lab=request.POST['lab']
        # sql="SELECT * FROM labour_assign WHERE Labourer_code='"+Lab+"'"
        sql="SELECT labour_assign.requirement,labour_assign.worksites,labour_details.labour_name,labour_assign.Labourer_code,labour_details.State,labour_details.District,labour_details.City,labour_assign.Date_Work FROM labour_assign INNER JOIN labour_details ON labour_assign.Labourer_code=labour_details.labour_code WHERE Labourer_code='"+Lab+"'"
        staff=dbconnection.allrow(sql)
        return render(request,'Agency/SearchStaff.html',{'data':data,'staff':staff})
    return render(request,'Agency/SearchStaff.html',{'data':data})   

def AgLabourdetails(request):
    username=request.session['usercode']
    sql="SELECT * FROM  `Labour_details` WHERE AddAgency='"+username+"'and status=1 "
    lab=dbconnection.allrow(sql)
    return render(request,'Agency/Labourdetails.html',{'lab':lab})
def AdTrackLabour(request):
    sql="SELECT * FROM Labour_details where status=1"
    data=dbconnection.allrow(sql)
    if request.POST.get('labr'):
        lab=request.POST['lab']
        # sql="SELECT * FROM labour_assign"
        sql1="SELECT * FROM labour_details Where Labour_code='"+lab+"'"
        track=dbconnection.singlerow(sql1)
        sql2="SELECT labour_assign.worksites,labour_assign.Date_Work,labour_assign.requirement,User_details.User_Name,User_details.User_Code FROM labour_assign INNER JOIN User_details ON labour_assign.User_Code=User_details.User_code WHERE Labourer_Code='"+lab+"'   "
        track1=dbconnection.allrow(sql2)

        return render(request,'Admin/TrackLabour.html',{'track':track,'track1':track1,'data':data})
    return render(request,'Admin/TrackLabour.html',{'data':data})
def AgTrackLabour(request):
    username=request.session['usercode']
    sql="select * from logindata  where username='"+username+"' "
    data=dbconnection.singlerow(sql)
    sql="SELECT * FROM Labour_details WHERE AddAgency='"+username+"' and  status=1"
    data=dbconnection.allrow(sql)
    if request.POST.get('labr'):
        lab=request.POST['lab']
        # sql="SELECT * FROM labour_assign"
        sql="SELECT labour_assign.Labourer_Code,labour_details.labour_name,labour_assign.worksites,labour_assign.Date_work,labour_assign.requirement FROM labour_assign INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code WHERE Labourer_Code='"+lab+"' "
        track=dbconnection.allrow(sql)
        return render(request,'Agency/TrackLabour.html',{'track':track,'data':data})
    return render(request,'Agency/TrackLabour.html',{'data':data})
def ViewAssignLab(request):
    username=request.session['usercode']
    # sql="select * from logindata  where username='"+username+"' "
    # data=dbconnection.singlerow(sql)
    sql1="select * from requirements where UserCode='"+username+"'"
    data1=dbconnection.allrow(sql1)
    if request.POST.get('requ'):
        req=request.POST['req']
        dat=request.POST['dat']
        sql=" SELECT labour_details.Labour_Name,labour_details.Labour_code,Labour_details.Address,labour_details.DOB,labour_details.photo,Agency_Details.Agency_Name,Agency_Details.Address,Agency_Details.Contact_person,Agency_Details.Phn_no,Agency_Details.District,Agency_Details.Email FROM  labour_assign INNER JOIN Agency_details ON labour_assign.AddBy=Agency_details.Uni_Agen_Code INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code WHERE  labour_assign.User_code='"+username+"' and labour_assign.requirement='"+req+"' and labour_assign.Date_Work='"+dat+"' "
        ass=dbconnection.allrow(sql)

    # sql1="SELECT labour_assign.Requirement,labour_details.Labour_name,labour_assign.Labourer_Code,requirements.From_Date,requirements.To_Date,requirements.WorkSite FROM requirements INNER JOIN labour_assign ON requirements.UserCode=labour_assign.User_code INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code  WHERE UserCOde='"+username+"'"
        # sql2="SELECT * FROM labour_assign WHERE User_code='"+username+"' and requirement='"+req+"' and Date_Work='"+dat+"'"
        # sql2="SELECT labour_assign.Requirement,labour_assign.Date_work,labour_assign.worksites,labour_details.Labour_name,labour_assign.AddBy FROm labour_assign INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code WHERE  labour_assign.User_code='"+username+"' and labour_assign.requirement='"+req+"' and labour_assign.Date_Work='"+dat+"' " 
        # ass=dbconnection.allrow(sql2)
        return render(request,'User/ViewAssignLab.html',{'ass':ass,'data1':data1})
    return render(request,'User/ViewAssignLab.html',{'data1':data1})
def Payment(request):
    username=request.session['usercode']
    sql="SELECT *   FROM payment_user WHERE PaymentStatus=0 and User_id='"+username+"'"
    pay=dbconnection.allrow(sql)
    return render(request,'User/Payment.html',{'pay':pay})
def Payment2(request):
    username=request.session['usercode']
    rid=request.GET['aid']
    d=datetime.now()   
    dat=date.today()
    # sql="SELECT *   FROM payment_user WHERE PaymentStatus=0"
    sql="UPDATE `payment_user` SET PaymentStatus=1 ,Date='"+str(dat)+"' where Pay_id='"+rid+"'"
    dbconnection.addrow(sql)
    return render(request,'User/Payment.html',{})
def PayStatus(request):
    username=request.session['usercode']
    sql="SELECT *,requirements.UserCode,requirements.Agency FROM user_details INNER JOIN requirements ON user_details.User_Code=requirements.UserCode WHERE requirements.Agency='"+username+"'"
    user=dbconnection.allrow(sql)
    return render(request,'Agency/PayStatus.html',{'user':user})

def PayStatus2(request):
    username=request.session['usercode']
    rid=request.GET['aid']
    sql="SELECT * FROM payment_user WHERE User_Id='"+rid+"' and paymentstatus=1"
    payuser=dbconnection.allrow(sql)
    sql1="SELECT * FROM user_details WHERE User_Code='"+rid+"'"
    user=dbconnection.singlerow(sql1)
    sql2="SELECt * FROM agency_details WHERE Uni_Agen_Code='"+username+"' "
    agen=dbconnection.singlerow(sql2)
    return render(request,'Agency/PayStatus2.html',{'payuser':payuser,'agen':agen,'user':user})

def UserAmount1(request):
    username=request.session['usercode']
    sql="SELECT * ,user_details.user_Name FROM requirements  INNER JOIN User_details ON requirements.UserCode=User_details.User_code WHERE Agency='"+username+"'and AcceptStatus='Accepted' and AmountStatus=0"
    req=dbconnection.allrow(sql)
   
    # sql1="SELECT requirements.Requirement,labour_details.Labour_name,labour_details.Labour_Code,requirements.From_Date,requirements.To_Date,requirements.WorkSite FROM requirements INNER JOIN labour_assign ON requirements.UserCode=labour_assign.User_code INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code  WHERE Agency='"+username+"'"
    # sql1="SELECT user_details.User_Name,requirements.UserCode,requirements.Requirement,requirements.worksite,requirements.From_date,requirements.To_date,requirements.No_of_labourer FROM requirements INNER JOIN User_details ON requirements.UserCode=User_details.User_code WHERE Agency='"+username+"'"
    # req=dbconnection.allrow(sql1)
    # sql1="select DATEDIFF( To_date, From_date) from requirements"
    # days=dbconnection.singlerow(sql1)
    return render(request,'Agency/AssignUserAmount.html',{'req':req})
def UserAmount2(request):
    
    username=request.session['usercode']
    rid=request.GET['aid']

    sql="SELECT * ,user_details.user_Name FROM requirements  INNER JOIN User_details ON requirements.UserCode=User_details.User_code WHERE Agency='"+username+"'and AcceptStatus='Accepted' and AmountStatus=0"
    req=dbconnection.allrow(sql)
    d=datetime.now()   
    dat=date.today()
    sql="SELECT * FROM requirements WHERE Req_Id='"+rid+"'"
    requ=dbconnection.singlerow(sql)
    sql1="select DATEDIFF( To_date, From_date) from requirements where Req_Id='"+rid+"'"
    days=dbconnection.singlerow(sql1)
    Payment=requ[8]*requ[11]*days[0]
    # tot=data1[0]*req[8]*req[11]
    sql1="INSERT INTO `payment_user`( `Date`, `User_Id`, `Requirement`, `Total_No`, `Days`, `Payment`, `Agency`, `PaymentStatus`) VALUES ('"+str(dat)+"','"+str(requ[2])+"','"+str(requ[4])+"','"+str(requ[8])+"','"+str(days[0])+"','"+str(Payment)+"','"+username+"',0)"
    dbconnection.addrow(sql1)
    sql2="UPDATE requirements SET AssignStatus=1 WHERE Req_Id='"+rid+"' "
    dbconnection.addrow(sql2)
    return render(request,'Agency/AssignUserAmount.html',{'days':days,'req':req})
def Attendence1(request):
    username=request.session['usercode']
    sql="SELECT * FROM labour_assign where AddBy='"+username+"' and AtenStatus=0 "
    # sql="SELECT DISTINCT Date_WORK,WorkSites,Requirement FROM labour_assign"
    req=dbconnection.allrow(sql)
    return render(request,'Agency/attendence.html',{'req':req})

def Attendence2(request):
    rid=request.GET['aid']
    username=request.session['usercode']
    # sql="SELECT * FROM requirements WHERE Agency='"+username+"' AND Requirement='"+rid+"'"
    # data=dbconnection.singlerow(sql)
    sql="SELECT * FROM labour_assign WHERE Assign_id='"+rid+"'"
    lab=dbconnection.allrow(sql)
    
    lab1=dbconnection.singlerow(sql)
    workdate=lab1[1]
    worksite=request.GET['cid']
    user=request.GET['did']
    if request.method=='POST':
        labr=request.POST.getlist('lab')
        for i in labr:
            sql="INSERT INTO `attendence`(`Work_date`, `Requirement`, `LabourId`, `UserId`, `AttendBy`) VALUES('"+str(workdate)+"','"+worksite+"','"+i+"','"+user+"','"+username+"')"
            dbconnection.addrow(sql)
            sql1="UPDATE `labour_assign` SET Atenstatus=1 where Labourer_code='"+i+"'"
            dbconnection.addrow(sql1)
        return HttpResponseRedirect("http://127.0.0.1:8000/Attendence1")   
    return render(request,'Agency/Attendence2.html',{'lab':lab,'workdate':workdate})

def LabourSalary1(request):
    username=request.session['usercode']

    sql="SELECT * FROM attendence WHERE AttendBy='"+username+"' and SalaryStatus=0 "
    # sql="SELECT attendence.Work_date,attendence.requirement,attendence.labourId,labour_details.photo FROM attendence INNER JOIN labour_details ON attendence.labourId=labour_details.Labour_code where attendby='"+username+"'"
    req=dbconnection.allrow(sql)
    return render(request,'Agency/LabourSalary1.html',{'req':req})
def LabourSalary2(request):
    rid=request.GET['aid']
    
    username=request.session['usercode']
    sql="SELECT * FROM attendence WHERE  atten_id='"+rid+"'"
    lab=dbconnection.singlerow(sql)
    user=lab[4]
    if request.method=='POST':
        dat=request.POST['dat']
        labr=request.POST['labr']
        work=request.POST['work']
        salary=request.POST['sal']
        sql="INSERT INTO `salary_labour`(`Labourer_Id`, `Sal_date`, `UserCode`, `Worksite`, `Salary`, `AttendBy`) VALUES('"+labr+"','"+dat+"','"+user+"','"+work+"','"+salary+"','"+username+"')"
        dbconnection.addrow(sql)
        sql1="UPDATE attendence SET SalaryStatus=1 WHERE LabourId='"+labr+"'"
        dbconnection.addrow(sql1)
        return HttpResponseRedirect("http://127.0.0.1:8000/LabourSalary1")
    return render(request,'Agency/LabourSalary2.html',{'lab':lab})
# def LabPaymentHis(request):
#     username=request.session['usercode']
#     sql="SELECT * FROM  `Agency_details` "
#     agen=dbconnection.allrow(sql)
#     if request.POST.get('ag'):
#         agen=request.POST['agen']
#         # sql="SELECT * FROM `salary_labour` WHERE AttendBy='"+agen+"'"
#         sql="SELECT * , labour_details.Labour_name FROM `salary_labour` INNER JOIN labour_details ON salary_labour.Labourer_id=labour_details.labour_code WHERE AttendBy='"+agen+"' "
#         labpay=dbconnection.allrow(sql)
#         return render(request,'Admin/LabPaymentHis.html',{'labpay':labpay,'agen':agen})
#     return render(request,'Admin/LabPaymentHis.html',{'agen':agen})
def LabPaymentHis(request):
    # sql="SELECT * FROM  `Agency_details` "
    # agen=dbconnection.allrow(sql)
    sql="SELECT salary_labour.Sal_date,salary_labour.Worksite, salary_labour.Salary,labour_details.Labour_name,labour_details.Photo,Agency_details.Agency_Name,User_details.User_Name FROM `salary_labour` INNER JOIN labour_details ON salary_labour.Labourer_id=labour_details.labour_code INNER JOIN agency_details ON salary_labour.AttendBy=Agency_details.Uni_Agen_Code INNER JOIN User_details ON salary_labour.UserCode=User_details.User_Code "
    labpay=dbconnection.allrow(sql)
    return render(request,'Admin/LabPaymentHis.html',{'labpay':labpay})


def PoliceReg(request):
    d=datetime.now()   
    dat=date.today()
    username=request.session['usercode']
    if request.method=='POST':
        StationName=request.POST['name']
        Email=request.POST['email']
        Passw=request.POST['passw']
        PoliceCode=request.POST['policecode']
        PhoneNum=request.POST['phonenum']
        Addr=request.POST['address']
        sq="SELECT * FROM logindata WHERE username='"+PoliceCode+"'"
        a=dbconnection.singlerow(sq)
        if a:
            return render(request,'UserReg.html',{'msg':'UserName Already Exist'})  
        else:
            sql="INSERT INTO `police_details`(`StationName`, `Email`, `Police_code`,`Password`, `PhnNum`, `Address`) VALUES  ('"+StationName+"','"+Email+"','"+PoliceCode+"','"+Passw+"','"+PhoneNum+"','"+Addr+"')"
            dbconnection.addrow(sql)
            sql1="INSERT INTO `logindata`(`username`, `password`, `utype`) VALUES  ('"+PoliceCode+"','"+Passw+"','police')"
            dbconnection.addrow(sql1)
    return render(request,'Admin/PoliceReg.html',{})
def PoliceAgency(request):
    sql="SELECT * FROM agency_details"
    agen=dbconnection.allrow(sql)
    return render(request,'Police/SearchAgency.html',{'agen':agen})
def PoliceAgency2(request):
    rid=request.GET['aid']
    sql="SELECT * FROM agency_details where Agency_Id='"+rid+"'"
    agen=dbconnection.singlerow(sql)
    return render(request,'Police/SearchAgency2.html',{'agen':agen})  
def PoliceLabour(request):
    sql="SELECT * ,Agency_details.Agency_Name FROM labour_details  INNER JOIN Agency_details ON labour_details.AddAgency=Agency_details.Uni_Agen_code Where labour_details.Status=1" 
    Lab=dbconnection.allrow(sql)
    return render(request,'Police/SearchLabour.html',{'Lab':Lab}) 
  
def PoliceLabour2(request):
    rid=request.GET['aid']
    sql="SELECT * FROM labour_details Where Labid='"+rid+"' "
    Lab=dbconnection.singlerow(sql)
    return render(request,'Police/SearchLabour2.html',{'Lab':Lab})
def LabourWork(request):
    # sql="SELECT * ,agency_details.Agency_Name FROM labour_assign INNER JOIN agency_details ON labour_assign.AddBy=agency_details.Agency_Name INNER JOIN labour_details ON labour_assign.labourer_code=labour_details.labour_Name  "
    # # sql="SELECT * FROM labour_assign  "
    # work=dbconnection.allrow(sql)
    # return render(request,'Police/LabourWork.html',{'work':work})
    sql="SELECT * FROM Labour_details where status=1"
    data=dbconnection.allrow(sql)
    if request.POST.get('labr'):
        lab=request.POST['lab']
        # sql="SELECT * FROM labour_assign"
        sql="SELECT labour_assign.Labourer_Code,labour_details.labour_name,labour_assign.worksites,labour_assign.Date_Work,labour_assign.requirement FROM labour_assign INNER JOIN labour_details ON labour_assign.Labourer_Code=labour_details.Labour_code WHERE Labour_Code='"+lab+"'   "
        track=dbconnection.allrow(sql)
        return render(request,'Police/LabourWork.html',{'track':track,'data':data})
    return render(request,'Police/LabourWork.html',{'data':data})

def AssignStatus(request):
    username=request.session['usercode']
    sql="SELECT user_details.User_name,requirements.UserCode FROM  `Requirements`INNER JOIN user_details ON Requirements.usercode=user_details.user_code  WHERE Agency='"+username+"' and AcceptStatus='Accepted' "
    ass=dbconnection.allrow(sql)
    if request.method=="POST":
        User=request.POST['user']
        # sql="SELECT * FROM labour_assign WHERE user_code='"+User+"' "
        # ass=dbconnection.allrow(sql)
        # sql="SELECT * FROM labour_assign WHERE usr_code='"+User+"' GROUP BY Requirement and Worksites"
        sql="SELECT *, labour_details.labour_Name,labour_assign.labourer_code FROM labour_assign INNER JOIN labour_details ON labour_assign.labourer_code=labour_details.labour_code WHERE labour_assign.User_code='"+User+"' ORDER BY Date_Work"
        lab=dbconnection.allrow(sql)
        
        return render(request,'Agency/AssignmentStatus.html',{'ass':ass,'lab':lab})
    return render(request,'Agency/AssignmentStatus.html',{'ass':ass})
def PostComplaints(request):
    username=request.session['usercode']
    sql="SELECT * FROM  user_details Where user_code='"+username+"'"
    user=dbconnection.singlerow(sql)
    sql="SELECT * FROM Agency_details"
    agen=dbconnection.allrow(sql)
    dat=date.today()
    if request.method=='POST':
        sub=request.POST['sub']
        agen=request.POST['agen']
        comp=request.POST['comp']
        sql1="INSERT INTO `complaints`(`Comp_Date`, `UserId`, `ToAgency`, `subject`, `Complaints`) VALUES('"+str(dat)+"','"+username+"','"+agen+"','"+sub+"','"+comp+"')"
        dbconnection.addrow(sql1)
    return render(request,'User/PostComplaints.html',{'user':user,'agen':agen})
def PostReview(request):
    username=request.session['usercode']
    sql="SELECT * FROM Agency_details"
    agen=dbconnection.allrow(sql)
    sql="SELECT * FROM  user_details Where user_code='"+username+"'"
    user=dbconnection.singlerow(sql)
    dat=date.today()
    if request.method=='POST':
        agen=request.POST['agen']
        rev=request.POST['rev']
        sql1="INSERT INTO `review`(`Re_Date`, `UserId`, `ToAgency`, `Review`) VALUES('"+str(dat)+"','"+username+"','"+agen+"','"+rev+"')"
        dbconnection.addrow(sql1)
    return render(request,'User/PostReview.html',{'user':user,'agen':agen})
def ViewReview(request):
    username=request.session['usercode']
    sql="SELECT *,user_details.User_name,user_details.photo FROM review INNER JOIN user_details ON review.UserId=user_details.User_code WHERE ToAgency='"+username+"'"
    rev=dbconnection.allrow(sql)
    return render(request,'Agency/Review.html',{'rev':rev})
def AdViewReview(request):
    username=request.session['usercode']
    sql="SELECT *,user_details.User_name,user_details.photo FROM review INNER JOIN user_details ON review.UserId=user_details.User_code"
    rev=dbconnection.allrow(sql)
    return render(request,'Admin/Review.html',{'rev':rev})
def PoliManageComp(request):
    username=request.session['usercode']
    sql="SELECT *,user_details.user_name FROM complaints INNER JOIN user_details ON complaints.UserId=user_details.User_code"
    comp=dbconnection.allrow(sql)
    return render(request,'Police/ManageComplaint.html',{'comp':comp})
def AdManageComp(request):
    username=request.session['usercode']
    sql="SELECT *,user_details.user_name FROM complaints INNER JOIN user_details ON complaints.UserId=user_details.User_code"
    comp=dbconnection.allrow(sql)
    return render(request,'Admin/ManageComplaint.html',{'comp':comp})
# def AdClient(request):
#     return render(request,'Admin/ClientPayment.html',{})
def AdClientPayment(request):
    username=request.session['usercode']
    sql2="SELECT * FROM agency_details WHERE Uni_Agen_Code='"+username+"'"
    agen=dbconnection.singlerow(sql2)
    # sql="SELECT * FROM payment_user"
    # payuser=dbconnection.allrow(sql)
    #
    sql="SELECT Agency_details.Agency_name,Agency_details.Address,user_details.User_name,user_details.Address,user_details.Email,user_details.Phn_num,Payment_user.Date,payment_user.requirement,payment_user.Total_no,payment_user.days,payment_user.Payment from payment_user INNER JOIN user_details ON payment_user.User_Id=user_details.User_code INNER JOIN Agency_details ON payment_user.Agency=Agency_details.Uni_agen_code Where payment_user.PaymentStatus=1"  
    # sql="SELECT *,requirements.UserCode,requirements.Agency FROM user_details INNER JOIN requirements ON user_details.User_Code=requirements.UserCode"
    # sql="SELECT *, User_details.user_name FROM payment_user INNER JOIN user_details ON payment_user.User_Id=user_details.User_code "
    payuser=dbconnection.allrow(sql)
    # SELECT payment_user.date,payment_user.Requirement,payment_user.Total_No,payment_user.Days,payment_user.Payment, User_details.user_name,user_deatils.Address,user_details.phn_num FROM payment_user INNER JOIN user_details ON payment_user.User_Id=user_details.User_code 
    # sql1="SELECT * FROM user_details"
    # user=dbconnection.singlerow(sql1)
    # sql2="SELECt * FROM agency_details"
    # agen=dbconnection.singlerow(sql2)
    # sql="SELECT *,user_details.user_name,agency_details.Agency_name FROM payment_user INNER JOIN user_details ON payment_user.User_Id=user_details.User_code INNER JOIN agency_details ON payment_user.Agency=Agency_details.Uni_agen_code "
    # sql="SELECT  payment_user.Date,payment_user.Requirement,payment_user.Total_No,payment_user.Days,User_details.User_name,user_details.Address,user_details.Email,agency_details.agency_name,Agency_details.Address FROM payment_user INNER JOIN user_details ON payment_user.User_Id=user_details.User_code INNER JOIN agency_details ON payment_user.Agency=agency_details.Uni_agen_code"
    # payuser=dbconnection.allrow(sql)
    return render(request,'Admin/ClientPayment.html',{'payuser':payuser,'agen':agen})
    
def UserDetails(request):
    rid=request.GET['aid']
    sql="SELECT * FROM user_details WHERE User_code='"+rid+"'"
    user=dbconnection.singlerow(sql)
    return render(request,'Admin/userdetails.html',{'user':user})
def AdminHome(request):
    return render(request,'Admin/AdminHome.html',{})
def AgencyHome(request):
    username=request.session['usercode']
    sql="SELECT Agency_details.agency_name FROM logindata INNER JOIN agency_details ON logindata.username=agency_details.Uni_Agen_Code"
    agen=dbconnection.singlerow(sql)
    return render(request,'Agency/AgencyHome.html',{'agen':agen[0]})
def PoliceHome(request):
    return render(request,'Police/PoliceHome.html',{})
def UserHome(request):
    sql="SELECT user_details.User_name FROM logindata INNER JOIN user_details ON logindata.username=user_details.user_code"
    user=dbconnection.singlerow(sql)
    return render(request,'User/UserHome.html',{'user':user[0]})
def hr(request):
    return render(request,'hr.html',{})
    
    
