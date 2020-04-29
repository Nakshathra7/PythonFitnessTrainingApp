#python3 -m pip install flask;
#python3 -m pip install flask_session;
#pip3 uninstall Werkzeug
#pip3 install Werkzeug==0.16.0


from flask import Flask
from flask import render_template
from flask import request,session, redirect, url_for, escape,send_from_directory,make_response 

from member import memberList
from memberHealth import memberHealthList
from subscription import subscriptionList
from trainer import trainerList
from mealPlan import mealPlanList
from workoutPlan import workoutPlanList
from trainerMemberAssignment import trainerMemberAssignmentList

import pymysql, json, time

from flask_session import Session #Serverside Sessions

app = Flask(__name__,static_url_path='')

SESSION_TYPE = 'filesystem'

app.config.from_object(__name__)
Session(app)

@app.route('/set')
def set():
    session['time'] = time.time()
    return 'set'
    
@app.route('/get')
def get():
    return str(session['time'])

@app.route('/nothing')
def nothing():
    print('hi')
    return ''

@app.route('/basichttp')
def basichttp():
    if request.args.get('myvar') is not None:
        a = request.args.get('myvar')
        return 'your var:' + request.args.get('myvar')
    else:
        return 'myvar not set' 

@app.route('/')
def home():
    return render_template('test.html', title='Home', msg='Welcome!')

@app.route('/index')
def index():
    user = {'username': 'Anusuya'}
    items = [
        {'name':'Apple','price':2.34},
        {'name':'Orange','price':4.88},
        {'name':'Grape','price':2.44}
    ]
    return render_template('index.html', title='MyPage', user=user, items=items)
 
def checkSession():
    if 'active' in session.keys():
        timeSinceLastActive = time.time() - session['active']
        print(timeSinceLastActive)
        if timeSinceLastActive > 150:
            session['msg'] = 'Your Session has Timed Out.'
            return False
        else:
            session['active'] = time.time()
            return True
    else:
        return False
 
@app.route('/login', methods = ['GET','POST'])
def login():  
    if request.form.get('email') is not None and request.form.get('password') is not None:
        m = memberList()
        t = trainerList()
        mh = memberHealthList()
        if m.tryLogin(request.form.get('email'),request.form.get('password')):
            print("Login Ok")  
            session['user'] = m.data[0]
            print("memberinfo",session['user']['MemberID'])
            session['active'] = time.time()
            userinfo = 'Welcome to Fitness Training...!!!'    
            memberID = m.getCurrentID(request.form.get('email'),request.form.get('password'))
            memberName = m.getCurrentFieldName(memberID)
            #return redirect('main')
            mh.getReferntialID(memberID)
            mealPlanID = mh.data[0]['MealPlanID']
            workoutID = mh.data[0]['WorkoutID']
            return render_template('member/memberMain.html', title='Main Menu',msg=userinfo,memberByID=memberID,mealPlanID=mealPlanID,workoutID=workoutID,memberName=memberName)

        elif t.tryLogin(request.form.get('email'),request.form.get('password')):
            print("Login Ok") 
            session['user'] = t.data[0]
            print("trainerinfo",session['user']['TrainerID'])
            session['active'] = time.time()
            trainerinfo = 'Welcome to Fitness Training...!!!'   
            trainerID = t.getCurrentID(request.form.get('email'),request.form.get('password'))
            trainerName = t.getCurrentFieldName(trainerID)
            return render_template('trainer/trainerDashboard.html', title='Main Menu',msg=trainerinfo,trainerByID=trainerID,trainerName=trainerName)

        elif (request.form.get('email') == 'admin' and request.form.get('password') == 'admin'):
            print("Login Ok") 
            session['user'] = 'admin'
            session['active'] = time.time()
            userinfo = 'Hello Admin....! Welcome to Fitness Training'    
            #return redirect('main')
            return render_template('admin/adminMain.html', title='Main Menu',msg=userinfo)

        else:
            print("Login Failed...!!!") 
            return render_template('login.html', title='Login',msg='Incorrect Username or Password...!!!')
    else:
        if 'msg' not in session.keys() or session['msg'] is None:
            m = 'Type your email and password to continue.'
        else:
            m = session['msg']
            session['msg'] = None
        return render_template('login.html', title='Login', msg=m)

# Admin Section Starts 

@app.route('/adminMain')  
def adminMain():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #userinfo = 'Hello, ' + session['user']
    adminInfo = 'Hello Admin. Welcome to Fitness Training...!!!'
    #session['user']['type'] == 'Member'
    #t = trainerList()
    return render_template('admin/adminMain.html', title='Main Menu',msg=adminInfo)

@app.route('/trainerMemberList')
def trainerMemberList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    m = memberList()
    t = trainerList()
    m.getByFieldName('MemberName')
    t.getByFieldName('TrainerName')
    print(m.data) 
    #return ''   
    return render_template('admin/trainerMemberList.html', title='Trainer Member Assignment List', members=m.data, trainers=t.data)
  
@app.route('/trainerMemberAssignment', methods = ['GET','POST'])
def trainerMemberAssignment():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    m = memberList()
    t = trainerList()
    memberID = m.getFieldID(request.form.get('MemberName'))
    trainerID = t.getFieldID(request.form.get('TrainerName'))

    m.getByFieldName('MemberName')
    t.getByFieldName('TrainerName')

    tm = trainerMemberAssignmentList()
    tm.set('TrainerID',trainerID)
    tm.set('MemberID',memberID)
    tm.add()
    if tm.getByField('MemberID',memberID) == 0:
        tm.insert() 
        print(tm.data) 
        return render_template('admin/savedtrainerMemberAssignment.html', title='Saved Trainer Member Assignment', member=m.data[0])
    else:
        msg = 'Member is Already Assigned to Trainer'
        return render_template('admin/trainerMemberList.html', title='Trainer Member Assignment List', members=m.data, trainers=t.data, msg=msg)

# @app.route('/editTrainerMemberAssignment', methods = ['GET','POST'])
# def editTrainerMemberAssignment():
#     if checkSession() == False: #check to make sure the user is logged in
#         return redirect('login')
#     tm = trainerMemberAssignmentList()
#     t.set('TrainerName',request.form.get('TrainerName'))
#     t.set('TrainerEmail',request.form.get('TrainerEmail'))
#     t.set('TrainerPassword',request.form.get('TrainerPassword'))
#     t.set('TrainerYrsOfExperience',request.form.get('TrainerYrsOfExperience'))
#     t.set('TrainerGender',request.form.get('TrainerGender'))
#     t.add() 
#     if t.verifyNew():
#         t.update()
#         return render_template('trainer/savedTrainer.html', title='Trainer Saved',  trainer=t.data[0])
#     else:
#         return render_template('trainer/editTrainerMemberAssignment.html', title='Trainer Not Saved',  trainer=t.data[0],msg=t.errList) 

# @app.route('/allTrainerMemberList')
# def allTrainerMemberList():
#     if checkSession() == False: #check to make sure the user is logged in
#         return redirect('login')
#     m = memberList()
#     t = trainerList()
#     tm = trainerMemberAssignmentList()
#     tm.getAll()
#     print(tm.data)
#     return render_template('admin/allTrainerMemberList.html', title='Trainer Member List', trainerMembers=tm.data)

# @app.route('/trainerMemberAssignmentByID') 
# def trainerMemberAssignmentByID():
#     if checkSession() == False: #check to make sure the user is logged in
#         return redirect('login')
#     tm = trainerMemberAssignmentList()
#     if request.args.get(tm.pk) is None:
#         return render_template('admin/trainerMemberError.html', msg='No TrainerMemberAssignment ID is given.')
    
#     tm.getByID(request.args.get(tm.pk))
#     if len(tm.data) <= 0:
#         return render_template('admin/trainerMemberError.html', msg='TrainerMemberAssignment ID does not exist')
#     print(tm.data)
#     return render_template('admin/editTrainerMemberAssignment.html', title='Trainer Member List', trainerMember=tm.data[0])

# Admin Section Ends  

# Member Section Starts 

@app.route('/memberMain')  
def memberMain():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    #userinfo = 'Hello, ' + session['user']
    memberinfo = 'Welcome to Fitness Training...!!!'    
    memberID = session['user']['MemberID']
    #return redirect('main')
    m = memberList()
    mh = memberHealthList()
    mh.getReferntialID(memberID)
    memberName = m.getCurrentFieldName(memberID)
    mealPlanID = mh.data[0]['MealPlanID']
    workoutID = mh.data[0]['WorkoutID']
    return render_template('member/memberMain.html', title='Main Menu',msg=memberinfo,memberByID=memberID,mealPlanID=mealPlanID,workoutID=workoutID,memberName=memberName)

@app.route('/addMember', methods = ['GET','POST'])
def addMember():
    if request.form.get('MemberName') is None:
        m = memberList()
        m.set('MemberName','')
        m.set('MemberEmail','')
        m.set('MemberPassword','')
        m.set('MemberAddress','')
        m.add() 
        return render_template('member/addMember.html', title='New Member', member=m.data[0])

    else:
        m = memberList()
        m.set('MemberName',request.form.get('MemberName'))
        m.set('MemberEmail',request.form.get('MemberEmail'))
        m.set('MemberPassword',request.form.get('MemberPassword'))
        m.set('MemberAddress',request.form.get('MemberAddress'))
        m.add()
        if m.verifyNew(): 
            m.insert()
            memberID = m.getCurrentID(request.form.get('MemberEmail'),request.form.get('MemberPassword'))
            print(m.data)
            return render_template('member/savedMember.html', title='Saved Member', member=m.data[0], memberID=memberID)
        else:
            return render_template('member/addMember.html', title='Member Not Added', member=m.data[0], msg=m.errList)
 
@app.route('/editMember', methods = ['GET','POST'])
def editMember(): 
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    m = memberList()
    memberID = request.form.get('MemberID')
    m.set('MemberID',request.form.get('MemberID'))
    m.set('MemberName',request.form.get('MemberName'))
    m.set('MemberEmail',request.form.get('MemberEmail'))
    m.set('MemberPassword',request.form.get('MemberPassword'))
    m.set('MemberAddress',request.form.get('MemberAddress'))
    m.add()  
    if m.verifyNew():
        m.update()
        return render_template('member/saveEditMember.html', title='Member Saved',  member=m.data[0],memberID=memberID)
    else:
        return render_template('member/editMember.html', title='Member Not Saved',  member=m.data[0],msg=m.errList)

@app.route('/allMemberList')
def allMemberList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    m = memberList()
    m.getAll()
    print(m.data)
    return render_template('member/allMemberList.html', title='Member List', members=m.data)

@app.route('/memberByID')  
def memberByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    m = memberList()
    if request.args.get(m.pk) is None:
        return render_template('member/memberError.html', msg='No Member is given.')
    
    m.getByID(request.args.get(m.pk))
    if len(m.data) <= 0:
        return render_template('member/memberError.html', msg='Member ID does not exist')
    print(m.data) 
    return render_template('member/editMember.html', title='Member List', member=m.data[0])

# Member Section Ends 

# MemberHealth Section Starts

@app.route('/addMemberHealth', methods = ['GET','POST'])
def addMemberHealth():
    memberIDArg = request.args.get('MemberID')
    print("memberIDArg",memberIDArg)
    if request.form.get('MemberAge') is None:
        mh = memberHealthList()
        mh.set('MemberID',request.args.get('MemberID'))
        mh.set('MemberAge','')
        mh.set('MemberGender','')
        mh.set('MemberHeight','')
        mh.set('MemberWeight','')
        mh.set('MemberBMI','')
        mh.set('MemberProfession','')
        mh.set('MemberMedicalAilments','')
        mh.add() 
        return render_template('memberHealth/addMemberHealth.html', title='New Member Health', memberHealth=mh.data[0], memberID=memberIDArg)

    else:  
        mh = memberHealthList()
        print("memberIDArg2",memberIDArg)
        mh.set('MemberID',memberIDArg)
        mh.set('MemberAge',request.form.get('MemberAge'))
        mh.set('MemberGender',request.form.get('MemberGender'))
        mh.set('MemberHeight',request.form.get('MemberHeight'))
        mh.set('MemberWeight',request.form.get('MemberWeight'))
        mh.set('MemberBMI',request.form.get('MemberBMI'))
        mh.set('MemberProfession',request.form.get('MemberProfession'))
        mh.set('MemberMedicalAilments',request.form.get('MemberMedicalAilments'))
        mh.add() 
        if mh.verifyNew():
            mh.insert()
            print(mh.data)
            return render_template('memberHealth/savedMemberHealth.html', title='Saved Member Health', memberHealth=mh.data[0],memberID=memberIDArg)
        else:
            return render_template('memberHealth/addMemberHealth.html', title='Member Health Not Added', memberHealth=mh.data[0], msg=mh.errList)
 
@app.route('/editMemberHealth', methods = ['GET','POST'])
def editMemberHealth():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login') 
    mh = memberHealthList()
    memberIDArg = request.args.get('MemberID')
    mh.set('MemberID',memberIDArg)
    mh.set('MemberHealthRecordID',request.form.get('MemberHealthRecordID'))
    mh.set('MemberAge',request.form.get('MemberAge'))
    mh.set('MemberGender',request.form.get('MemberGender'))
    mh.set('MemberHeight',request.form.get('MemberHeight'))
    mh.set('MemberWeight',request.form.get('MemberWeight'))
    mh.set('MemberBMI',request.form.get('MemberBMI'))
    mh.set('MemberProfession',request.form.get('MemberProfession'))
    mh.set('MemberMedicalAilments',request.form.get('MemberMedicalAilments'))
    mh.add()   
    if mh.verifyNew():
        mh.update()
        #print(c.data) 
        #return ''
        return render_template('memberHealth/saveEditMemberHealth.html', title='Member Health Saved',  memberHealth=mh.data[0])
    else:
        return render_template('memberHealth/editMemberHealth.html', title='Mealth Health Not Saved',  memberHealth=mh.data[0],msg=mh.errList)

@app.route('/allMemberHealthList')
def allMemberHealthList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    mh = memberHealthList()
    mh.getAll()
    print(mh.data)
    #return ''
    return render_template('memberHealth/allMemberHealthList.html', title='Member Health List', memberHealths=mh.data)

@app.route('/memberHealthByID') 
def memberHealthByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    mh = memberHealthList()
    memberID = mh.getParentID(request.args.get('MemberID'))
    
    if request.args.get('MemberID') is None:
        return render_template('memberHealth/memberHealthError.html', msg='No Member Health is given.')
    
    mh.getByID(request.args.get('MemberID'))
    if len(mh.data) <= 0:
        return render_template('memberHealth/memberHealthError.html', msg='Member Health ID does not exist')
    print(mh.data)
    #return ''
    return render_template('memberHealth/editMemberHealth.html', title='Member Health List', memberHealth=mh.data[0],memberID=memberID)

# MemberHealth Section Ends

# Subscription Plan Section Starts

@app.route('/addSubscription', methods = ['GET','POST'])
def addSubscription():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    if request.form.get('SubscriptionName') is None:
        s = subscriptionList()
        s.set('SubscriptionName','')
        s.set('SubscriptionPrice','')
        s.set('SubscriptionType','')
        s.set('NoOfDaysSubscription','')
        s.add() 
        return render_template('subscribe/addSubscription.html', title='New Subscription', subscribe=s.data[0])

    else:
        s = subscriptionList()
        s.set('SubscriptionName',request.form.get('SubscriptionName'))
        s.set('SubscriptionPrice',request.form.get('SubscriptionPrice'))
        s.set('SubscriptionType',request.form.get('SubscriptionType'))
        s.set('NoOfDaysSubscription',request.form.get('NoOfDaysSubscription'))
        s.add() 
        if s.verifyNew():
            s.insert()
            print(s.data)
            return render_template('subscribe/savedSubscription.html', title='Saved Subscription', subscribe=s.data[0])
        else:
            return render_template('subscribe/addSubscription.html', title='Subscription Not Added', subscribe=s.data[0], msg=s.errList)

@app.route('/editSubscription', methods = ['GET','POST'])
def editSubscription():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    s = subscriptionList()
    s.set('SubscriptionID',request.form.get('SubscriptionID'))
    s.set('SubscriptionName',request.form.get('SubscriptionName'))
    s.set('SubscriptionPrice',request.form.get('SubscriptionPrice'))
    s.set('SubscriptionType',request.form.get('SubscriptionType'))
    s.set('NoOfDaysSubscription',request.form.get('NoOfDaysSubscription'))
    s.add()   
    if s.verifyNew():
        s.update()
        return render_template('subscribe/savedSubscription.html', title='Subscription Saved',  subscribe=s.data[0])
    else:
        return render_template('subscribe/editSubscription.html', title='Subscription Not Saved',  subscribe=s.data[0],msg=s.errList)
    

@app.route('/allSubscriptionList')
def allSubscriptionList(): 
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    s = subscriptionList() 
    s.getAll()
    print(s.data)
    #return ''
    return render_template('subscribe/allSubscriptionList.html', title='Subscription List', subscribes=s.data)

@app.route('/subscriptionByID') 
def subscriptionByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    s = subscriptionList()
    if request.args.get(s.pk) is None:
        return render_template('subscribe/subscriptionError.html', msg='No Subscription is given.')
    
    s.getByID(request.args.get(s.pk))
    if len(s.data) <= 0:
        return render_template('subscribe/subscriptionError.html', msg='Subscription ID does not exist')
    print(s.data)
    #return ''
    return render_template('subscribe/editSubscription.html', title='Subscription List', subscribe=s.data[0])

@app.route('/deleteSubscription',methods = ['GET', 'POST'])
def deleteSubscription():
    if checkSession() == False: 
        return redirect('login')
    print("cid:",request.form.get('SubscriptionID')) 
    s = subscriptionList()
    s.deleteByID(request.form.get('SubscriptionID'))
    return render_template('subscribe/deleteSubscription.html', title='Subscription Deleted',  msg='Subscription Deleted.')

@app.route('/viewMemberSubscription')
def viewMemberSubscription(): 
    memberIDArg = request.args.get('MemberID')
    s = subscriptionList() 
    s.getAll()
    print(s.data)
    return render_template('subscribe/viewMemberSubscription.html', title='Subscription List', subscribes=s.data,memberID=memberIDArg)

@app.route('/addMemberSubscription', methods = ['GET','POST'])
def addMemberSubscription():
    memberIDArg = request.args.get('MemberID') 
    mh = memberHealthList()
    
    subscribeID = request.form.get('SubscriptionID')

    mh.updateReferenceField(subscribeID,memberIDArg)
    
    return render_template('subscribe/addMemberSubscription.html', title='Added Member Subscription')

# Subscription Plan Section Ends

# Trainer Section Starts

@app.route('/trainerMain')  
def trainerMain():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    t = trainerList()
    trainerinfo = 'Welcome to Fitness Training...!!!'
    trainerID = session['user']['TrainerID']
    trainerName = t.getCurrentFieldName(trainerID)
    t = trainerList()
    return render_template('trainer/trainerDashboard.html', title='Main Menu',msg=trainerinfo,trainerByID=trainerID,trainerName=trainerName)

@app.route('/addTrainer', methods = ['GET','POST'])
def addTrainer():
    if request.form.get('TrainerName') is None:
        t = trainerList()
        t.set('TrainerName','')
        t.set('TrainerEmail','')
        t.set('TrainerPassword','')
        t.set('TrainerYrsOfExperience','')
        t.set('TrainerGender','')
        t.add() 
        return render_template('trainer/addTrainer.html', title='New Trainer', trainer=t.data[0])

    else:
        t = trainerList()
        t.set('TrainerName',request.form.get('TrainerName'))
        t.set('TrainerEmail',request.form.get('TrainerEmail'))
        t.set('TrainerPassword',request.form.get('TrainerPassword'))
        t.set('TrainerYrsOfExperience',request.form.get('TrainerYrsOfExperience'))
        t.set('TrainerGender',request.form.get('TrainerGender'))
        t.add() 
        if t.verifyNew():
            t.insert()
            print(t.data)
            return render_template('trainer/savedTrainer.html', title='Saved Trainer', trainer=t.data[0])
        else:
            return render_template('trainer/addTrainer.html', title='Trainer Not Added', trainer=t.data[0], msg=t.errList)

@app.route('/editTrainer', methods = ['GET','POST'])
def editTrainer():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    t = trainerList()
    t.set('TrainerID',request.form.get('TrainerID'))
    t.set('TrainerName',request.form.get('TrainerName'))
    t.set('TrainerEmail',request.form.get('TrainerEmail'))
    t.set('TrainerPassword',request.form.get('TrainerPassword'))
    t.set('TrainerYrsOfExperience',request.form.get('TrainerYrsOfExperience'))
    t.set('TrainerGender',request.form.get('TrainerGender'))
    t.add() 
    if t.verifyNew():
        t.update()
        return render_template('trainer/saveEditTrainer.html', title='Trainer Saved', trainer=t.data[0])
    else:
        return render_template('trainer/editTrainer.html', title='Trainer Not Saved', trainer=t.data[0],msg=t.errList) 

@app.route('/allTrainerList')
def allTrainerList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    t = trainerList()
    t.getAll()
    print(t.data)
    return render_template('trainer/allTrainerList.html', title='Trainer List', trainers=t.data)

@app.route('/trainerByID') 
def trainerByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    t = trainerList()
    if request.args.get(t.pk) is None:
        return render_template('trainer/trainerError.html', msg='No Trainer is given.')
    
    t.getByID(request.args.get(t.pk))
    if len(t.data) <= 0:
        return render_template('trainer/trainerError.html', msg='Trainer ID does not exist')
    print(t.data)
    return render_template('trainer/editTrainer.html', title='Trainer List', trainer=t.data[0])

@app.route('/getMealWorkoutPlan', methods = ['GET','POST'])
def getMealWorkoutPlan():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    meal = mealPlanList()
    w = workoutPlanList()
    memberIDArg = request.args.get('MemberID')
    meal.getByFieldName('MealPlanName')
    w.getByFieldName('WorkoutName')

    return render_template('trainer/getMealWorkoutPlan.html', title='Assign Meal Workout Plan', mealPlanName=meal.data,workoutName=w.data,memberID=memberIDArg)

@app.route('/assignMealWorkoutPlan', methods = ['GET','POST'])
def assignMealWorkoutPlan():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    meal = mealPlanList()
    w = workoutPlanList()
    memberID = request.form.get('MemberID')

    mealPlanID = meal.getFieldID(request.form.get('MealPlanName'))
    workoutID = w.getFieldID(request.form.get('WorkoutName'))

    mh = memberHealthList()
    mh.updateSpecificField(mealPlanID,workoutID,memberID)
    
    return render_template('trainer/assignMealWorkoutPlan.html', title='Saved Trainer Member Assignment')
  
@app.route('/trainerAssignedMemberList')
def trainerAssignedMemberList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    tm = trainerMemberAssignmentList()
    mh = memberHealthList()
    trainerID = session['user']['TrainerID']
    print("trainerID",trainerID)
    tm.getAssignedID(trainerID)
    print("getAssignedID",tm.data) 

    trainerAssignedMember = []
    for members in tm.data:
        mh.getByID(members['MemberID'])
        trainerAssignedMember.append(mh.data)
    print("trainerAssignedMember",trainerAssignedMember) 
    return render_template('trainer/trainerAssignedMemberList.html', title='Trainer Assigned Member List', members=tm.data,trainerAssignedMember=trainerAssignedMember)
 
# Trainer Section Ends

# Meal Plan Section Starts

@app.route('/addMealPlan', methods = ['GET','POST'])
def addMealPlan():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    if request.form.get('MealPlanName') is None:
        meal = mealPlanList()
        meal.set('MealPlanName','')
        meal.set('MealPlanDescription','')
        meal.set('NoOfDaysMealPlan','')
        meal.add() 
        print("meal",meal.data)
        return render_template('mealPlan/addMealPlan.html', title='New Meal Plan', meals=meal.data[0])

    else:
        meal = mealPlanList()
        meal.set('MealPlanName',request.form.get('MealPlanName'))
        meal.set('MealPlanDescription',request.form.get('MealPlanDescription'))
        meal.set('NoOfDaysMealPlan',request.form.get('NoOfDaysMealPlan'))
        meal.add() 
        if meal.verifyNew():
            meal.insert()
            print("meal2",meal.data)
            return render_template('mealPlan/savedMealPlan.html', title='Saved Meal Plan', meals=meal.data[0])
        else:
            return render_template('mealPlan/addMealPlan.html', title='Meal Plan Not Added', meals=meal.data[0], msg=meals.errList)

@app.route('/editMealPlan', methods = ['GET','POST'])
def editMealPlan():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    meal = mealPlanList()
    meal.set('MealPlanID',request.form.get('MealPlanID'))
    meal.set('MealPlanName',request.form.get('MealPlanName'))
    meal.set('MealPlanDescription',request.form.get('MealPlanDescription'))
    meal.set('NoOfDaysMealPlan',request.form.get('NoOfDaysMealPlan'))
    meal.add() 
    if meal.verifyNew():
        meal.update()
        return render_template('mealPlan/savedMealPlan.html', title='Meal Plan Saved',  meals=meals.data[0])
    else:
        return render_template('mealPlan/editMealPlan.html', title='Meal Plan Not Saved',  meals=m.data[0],msg=meals.errList)


@app.route('/allMealPlanList')
def allMealPlanList():
    if checkSession() == False: #check to make sure the user is logged in  
        return redirect('login')
    meal = mealPlanList()
    meal.getAll()
    print(meal.data)
    return render_template('mealPlan/allMealPlanList.html', title='Meal Plan List', meals=meal.data)

@app.route('/mealPlanByID') 
def mealPlanByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    meal = mealPlanList()
    if request.args.get(meal.pk) is None:
        return render_template('mealPlan/mealPlanError.html', msg='No Meal Plan is given.')
    
    meal.getByID(request.args.get(meal.pk))
    if len(meal.data) <= 0:
        return render_template('mealPlan/mealPlanError.html', msg='Meal Plan ID does not exist')
    print(meal.data)
    return render_template('mealPlan/editMealPlan.html', title='Meal Plan List', meals=meal.data[0])

@app.route('/deleteMealPlan',methods = ['GET', 'POST'])
def deleteMealPlan():
    if checkSession() == False: 
        return redirect('login')
    print("MealPlanID:",request.form.get('MealPlanID')) 
    meal = mealPlanList()
    meal.deleteByID(request.form.get('MealPlanID'))
    return render_template('mealPlan/deleteMealPlan.html', title='Meal Plan Deleted',  msg='Meal Plan Deleted.')

@app.route('/memberMealPlanByID') 
def memberMealPlanByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    meal = mealPlanList()
    if request.args.get(meal.pk) is None:
        return render_template('mealPlan/mealPlanError.html', msg='No Meal Plan is given.')
    
    meal.getByID(request.args.get(meal.pk))
    if len(meal.data) <= 0:
        return render_template('mealPlan/mealPlanError.html', msg='Meal Plan does not exist')
    print(meal.data)
    return render_template('mealPlan/viewMemberMealPlan.html', title='Meal Plan List', meals=meal.data[0])

# Meal Plan Section Ends

# Workout Section Starts

@app.route('/addWorkout', methods = ['GET','POST'])
def addWorkout():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    if request.form.get('WorkoutName') is None:
        w = workoutPlanList()
        w.set('WorkoutName','')
        w.set('WorkoutType','')
        w.set('WorkoutTimeTotalHours','')
        w.set('NoOfDaysWorkout','')
        w.add() 
        return render_template('workoutPlan/addWorkout.html', title='New Workout Plan', workout=w.data[0])

    else:
        w = workoutPlanList()
        w.set('WorkoutName',request.form.get('WorkoutName'))
        w.set('WorkoutType',request.form.get('WorkoutType'))
        w.set('WorkoutTimeTotalHours',request.form.get('WorkoutTimeTotalHours'))
        w.set('NoOfDaysWorkout',request.form.get('NoOfDaysWorkout'))
        w.add() 
        if w.verifyNew():
            w.insert()
            print(w.data)
            return render_template('workoutPlan/savedWorkout.html', title='Saved Workout Plan', workout=w.data[0])
        else:
            return render_template('workoutPlan/addWorkout.html', title='Workout Plan Not Added', workout=w.data[0], msg=w.errList)

@app.route('/editWorkout', methods = ['GET','POST'])
def editWorkout():
    if checkSession() == False: #check to make sure the user is logged in 
        return redirect('login')
    w = workoutPlanList()
    w.set('WorkoutID',request.form.get('WorkoutID'))
    w.set('WorkoutName',request.form.get('WorkoutName'))
    w.set('WorkoutType',request.form.get('WorkoutType'))
    w.set('WorkoutTimeTotalHours',request.form.get('WorkoutTimeTotalHours'))
    w.set('NoOfDaysWorkout',request.form.get('NoOfDaysWorkout'))
    w.add()
    if w.verifyNew():
        w.update()
        return render_template('workoutPlan/savedWorkout.html', title='Workout Plan Saved',  workout=w.data[0])
    else:
        return render_template('workoutPlan/editWorkout.html', title='Workout Plan Not Saved',  workout=w.data[0],msg=w.errList)

@app.route('/allWorkoutList')
def allWorkoutList():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    w = workoutPlanList()
    w.getAll()
    print(w.data)
    return render_template('workoutPlan/allWorkoutList.html', title='Workout Plan List', workouts=w.data)
 
@app.route('/workoutPlanByID') 
def workoutPlanByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    w = workoutPlanList()
    if request.args.get(w.pk) is None:
        return render_template('workoutPlan/workoutPlanError.html', msg='No Workout Plan is given.')
    
    w.getByID(request.args.get(w.pk))
    if len(w.data) <= 0:
        return render_template('workoutPlan/workoutPlanError.html', msg='Workout ID does not exist')
    print(w.data)
    return render_template('workoutPlan/editWorkout.html', title='Workout Plan List', workout=w.data[0])

@app.route('/deleteWorkout',methods = ['GET', 'POST'])
def deleteWorkout():
    if checkSession() == False: 
        return redirect('login')
    print("WorkoutID:",request.form.get('WorkoutID')) 
    w = workoutPlanList()
    w.deleteByID(request.form.get('WorkoutID'))
    return render_template('mealPlan/deleteWorkout.html', title='Workout Deleted',  msg='Workout Deleted.')

@app.route('/memberWorkoutPlanByID') 
def memberWorkoutPlanByID():
    if checkSession() == False: #check to make sure the user is logged in
        return redirect('login')
    w = workoutPlanList()
    if request.args.get(w.pk) is None:
        return render_template('workoutPlan/workoutPlanError.html', msg='No Workout Plan is given.')
    
    w.getByID(request.args.get(w.pk))
    if len(w.data) <= 0:
        return render_template('workoutPlan/workoutPlanError.html', msg='Workout does not exist')
    print(w.data)
    return render_template('workoutPlan/viewMemberWorkout.html', title='Workout Plan List', workout=w.data[0])

# Workout Section Ends

@app.route('/logout', methods = ['GET','POST']) 
def logout():
    del session['user']
    del session['active']
    return render_template('login.html', title='Login',msg='You have Logged Out...!!!')
    
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
   app.secret_key = '1234'
   app.run(host='127.0.0.1',debug=True)




