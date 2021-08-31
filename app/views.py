from django.shortcuts import render, redirect, resolve_url
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . import models
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import random, time
from .decorators import only_admin_can_access

# External Functions

def is_problem_maker(user):
    for g in user.groups.all():
        if g.name == "Problem Maker":
            return True

    return False

def get_solved_problems(user):
    problems = []
    for p in models.ProblemSolved.objects.all():
        if p.user == user and p.problem.status == "Public" :
            problems.append(p.problem)

    return problems

def get_ranking():
    class Rank:
        def __init__(self, name, username, score, solve, tried):
            self.name = name
            self.score = score
            self.solve = solve
            self.tried = tried
            self.username = username
            if tried == 0:
                self.average = 0
            else:
                self.average = self.solve / self.tried
            self.rank = 0

        def __repr__(self):
            return f"{self.score}"

    ranks = []

    def get_solved_problem_count(i):
        solved = 0
        for p in models.ProblemSolved.objects.all():
            if p.user.username == i.user.username:
                solved += 1

        return solved

    def get_tried_problem_count(i):
        tried = models.ProblemTried.objects.filter(user=i.user).count()

        return tried

    def sort(L):
        for i in range(len(L)):
            for j in range(len(L)):
                if L[i].score > L[j].score:
                    L[i], L[j] = L[j], L[i] 
        
        return L[0]

    for i in models.InRank.objects.all():
        profile = models.Profile.objects.get(user=i.user)
        rank = Rank(profile.user.first_name, profile.user.username , profile.point, get_solved_problem_count(i),get_tried_problem_count(i)) 
        ranks.append(rank)

    highest = sort(ranks)

    group_rank = []
    rank_highest = highest.score

    def get_group(point):
        group = []
        for i in ranks:
            if i.score == point:
                group.append(i)
        return group

    for j in range(rank_highest+1):
        group_rank.append(get_group(rank_highest-j))

    reversed(group_rank)
    print(group_rank)
    final_rank = []

    for i in group_rank:
        for j in range(len(i)):
            for k in range(len(i)):
                if i[j].score < i[k].score:
                    i[j], i[k] = i[k], i[j]

    for i in group_rank:
        for j in i:
            final_rank.append(j)

    for i in range(len(final_rank)):   
        final_rank[i].rank = i+1

    return final_rank

def get_id(model_class,length:int):
    count = 0
    for i in model_class.objects.all():
        count += 1

    count += 1

    id = str(count)
    trailing = ""

    for i in range(length-(len(id))):
        trailing += "0"

    trailing += id

    return f"{trailing}"

def get_problems(category):
    problems = []
    for i in models.Problem.objects.all():
        if i.status == "Public" and i.problem_cat == category :
            problems.append(i)

    return problems

# Create your views here.

def home(request):
    profile = None
    problems = []
    for i in range(3):
        problems.append(random.choice(list(models.Problem.objects.all())))
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    return render(request, 'home.html',{'profile':profile,'problems':problems})

def about(request):
    members = models.ClubMember.objects.all()
    cont = {'members':members}
    return render(request,'about.html',cont) 

def problem_set(request):
    profile = None 
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)

    cont = {'profile':profile,'is_problem_maker':is_problem_maker(request.user)}

    return render(request, 'problemset.html',cont)

def topic_probelm_set(request, topic, num):
    profile = None
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    solved_problems = get_solved_problems(request.user)
    problems = []
    all_problems = get_problems(topic)[num*20:num+21]
    for i in all_problems:
        if i not in solved_problems:
            problems.append(i)
    problems = problems[num*20:num+21]
    next_page = num + 1
    prev_page = num - 1
    ranking = get_ranking()

    cont = {
        'profile':profile,
        'problems':problems,
        'unsolveds_count':len(problems),
        'topic':topic,
        'next_page':next_page,
        'prev_page':prev_page,
        'solveds':solved_problems,
        'solveds_count':len(solved_problems),
        'all':all_problems,
        'ranking':ranking
        }

    return render(request,"topic_problemset.html",cont)

@login_required(login_url="/user_login/")
def submission(request,status,problem,tried):
    return render(request,"submission.html", context={
        'p':problem,
        'status':status,
        'submission':tried,
    })


def problem(request,pk):
    start_time  = time.time()
    problem = models.Problem.objects.get(pk=pk)
    first_solve = "None"
    if not problem.first_solve == "None":
        try:
            first_solve = User.objects.get(username=problem.first_solve).first_name
        except:
            problem.first_solve = 'None'
            problem.save()

    more_problems = []
    all_problems = models.Problem.objects.all()
    total_problems = len(list(models.Problem.objects.all()))
    attempts = 0

    while len(more_problems) <= 5:
        attempts += 1
        more_problem = random.choice(list(all_problems))
        if more_problem not in more_problems:
            more_problems.append(more_problem)
        if attempts == total_problems:
            break

    # while True:
    #     if len(more_problems) <= 5:
    #         more_problem = random.choice(list(models.Problem.objects.all()))
    #         if more_problem not in more_problems:
    #             more_problems.append(more_problem)
    #     else: 
    #         break


    def already_solved():
        for p in models.ProblemSolved.objects.all():
            if p.problem == problem and p.user.username == request.user.username:
                return True
        
    def already_tried():
        for p in models.ProblemTried.objects.all():
            if p.problem == problem and p.user.username == request.user.username:
                return True

    def in_rank():
        for r in models.InRank.objects.all():
            if r.user == request.user:
                return True
        
        return False

    if request.method == "POST":
        tried = models.ProblemTried()
        tried.problem = problem
        tried.user = request.user
        answer = float(request.POST["answer"])
        tried.ans = answer
        tried.save()
        if not already_solved():
            if problem.answer == answer:
                solved = models.ProblemSolved()
                solved.user = request.user
                solved.problem = problem
                solved.save()
                profile = models.Profile.objects.get(user=request.user)
                profile.point = profile.point + problem.point
                profile.save()
                if not in_rank() and  profile.point > 15:
                    push_to_rank = models.InRank()
                    push_to_rank.user = request.user 
                    push_to_rank.save()
                if problem.first_solve == 'None':
                    problem.first_solve = request.user.username
                    problem.save()
                return submission(request,"Correct",problem,tried)
            return submission(request,"Wrong",problem,tried)

        if already_solved() or already_tried():
            return HttpResponse("Already Solved")
    
    cont = {'problem':problem,'solved':already_solved(), 'first_solve_username': problem.first_solve ,'first_solve':first_solve, 'more_problems':more_problems}
    print(time.time() - start_time )
    return render(request, 'problem.html',cont)

@login_required(login_url="/user_login/")
def add_problem(request):
    form = forms.Problem

    cont = {'form':form}

    if request.method == "POST":
        form = forms.Problem(request.POST)
        if form.is_valid():
            form.save()
        tags = request.POST['tags'].split(",")
        problem = models.Problem.objects.last()
        problem.problem_maker = request.user.username
        for t in tags:
            tag = models.ProblemTag()
            tag.name = t
            tag.problem = problem
            tag.save()
        
        return redirect(f"/admin_panel/problems/")

    return render(request, 'add_problem.html',cont)

@only_admin_can_access
def edit_problem(request, pk):

    problem = models.Problem.objects.get(pk=pk)
    form = forms.Problem(instance=problem)

    cont = {'form':form}

    if request.method == "POST":
        form = forms.Problem(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            return redirect("/admin_panel/problems/")
    return render(request, 'edit_problem.html', cont)

def get_user_ranking(user):
    ranks = get_ranking()
    rank = "none"
    for i in ranks:
        if i.username == user.username:
            rank = i.rank
            break

    return rank

def profile(request):
    def get_solved_problem_count(topic=None):
        solved = 0
        for p in models.ProblemSolved.objects.all():
            if p.user.username == request.user.username:
                solved += 1

        return solved

    def get_total_submissions_count():
        tried = len(list(models.ProblemTried.objects.filter(user=request.user)))

        return tried

    def get_total_problem_tried_count():
        problems = []
        tried = list(models.ProblemTried.objects.filter(user=request.user))
        for i in tried:
            if i.problem not in problems:
                problems.append(i.problem)

        return len(problems)

    def get_math_solved_problem_count():
        solved = 0
        for p in models.ProblemSolved.objects.all():
            if p.user.username == request.user.username and p.problem.problem_cat == "Math":
                solved += 1

        return solved

    def get_physics_solved_problem_count():
        solved = 0
        for p in models.ProblemSolved.objects.all():
            if p.user.username == request.user.username and p.problem.problem_cat == "Physics":
                solved += 1

        return solved

    def get_total_problems():
        return models.Problem.objects.count()

    def get_total_math_problems():
        count = 0
        for p in models.Problem.objects.all():
            if p.problem_cat == "Math":
                count += 1

        return count
    def get_total_physics_problems():
        count = 0
        for p in models.Problem.objects.all():
            if p.problem_cat == "Physcis":
                count += 1

        return count

    def get_progress():
        try:
            problems = get_total_problems()
            solved = get_solved_problem_count()

            return f'{((solved/problems) * 100):.2f}'
        except ZeroDivisionError: 
            return 0
    
    def get_math_progress():
        try:
            problems = get_total_math_problems()
            solved = get_math_solved_problem_count()

            return f'{((solved/problems) * 100):.2f}'
        except ZeroDivisionError: 
            return 0

    def get_physics_progress():
        try:
            problems = get_total_physics_problems()
            solved = get_physics_solved_problem_count()

            return f'{((solved/problems) * 100):.2f}'
        except ZeroDivisionError: 
            return 0
        


    rank = get_user_ranking(request.user)

    cont = {
        'profile':models.Profile.objects.get(user=request.user),
        'problem_tried': get_total_submissions_count(),
        'progress':get_progress(),
        'problems_tried': get_total_problem_tried_count(),
        'math_progress': get_math_progress(),
        'physics_progress': get_physics_progress(),
        'solved':get_solved_problem_count(),
        'math_solved': get_math_solved_problem_count(),
        'physics_solved': get_physics_solved_problem_count(),
        'total_problems':get_total_problems(),
        'rank': rank,
        }

    return render(request,'profile.html',cont)

def other_profile(request,username):
    cont = {'name': User.objects.get(username=username).username }

    return render(request,'other_profile.html',cont)

def user_login(request):
    if request.user.is_authenticated:
        return redirect("tmc:home")
    else:

        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            if len(username) != 6:
                length = len(username)
                new_name = ""
                for i in range(0,6-length):
                    new_name += "0"
                new_name += username
                username = new_name
            if username[0] == "#":
                username = username[1:] 

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)
            else:
                messages.error(request,'The given username or the password is incorrect. Try again, or click on \'Forgot Psssword\'')
                return render(request,'login.html')

            return redirect('tmc:profile')
        
        return render(request,'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("tmc:home")
    else:
        return redirect("tmc:user_login")

def leaderboard(request):
    final_rank = get_ranking()
    cont = {'ranks':final_rank,}
    return render(request, 'leaderboard.html',cont)

def user_registration(request):
    if request.user.is_authenticated:
        return redirect("tmc:home")
    else:
        if request.method == "POST":
            def get_tmc_id():
                return get_id(User,6)

            print(get_tmc_id())

            problem = None
            email = request.POST['email']
            pswd = request.POST['password']
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            username = get_tmc_id()

            if len(f_name) == 0 or len(l_name) == 0:
                messages.error(request, "First name or last name can't be empty")
                problem = True
            if len(pswd) < 6:
                messages.error(request, 'The password must contain at least 6 characters')
                problem = True

            if problem:
                return render(request, 'registration.html')

            new_user = User.objects.create_user(
                username, email, pswd
            )
            new_user.first_name = f_name
            new_user.last_name = l_name
            new_user.save()

            profile = models.Profile()
            profile.user = new_user
            profile.point = 0
            profile.save()

            messages.success(request, f'Registered successfully. Your TMC ID is {username}')

            user = authenticate(username=username,password=pswd)

            if user is not None:
                login(request, user)

            return redirect("tmc:profile")
            
        return render(request, 'registration.html')

def create_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0,9))

    return int(otp)

def forgot_password(request,email,otp):
    if request.user.is_authenticated:
        return redirect("tmc:home")
    else:
        if request.method == "POST":
            if email == 'given' and otp != 'given':
                given_email = request.POST['email']
                for i in User.objects.all():
                    if i.email == given_email:
                        break
                else:
                    messages.error(request,'Given email isn\'t valid')
                    return render(request, 'forgot_password.html',{'step':1})
                otp = create_otp()
                print(otp)
                cont = {'step':2,'otp':otp,'given_email':given_email}
                return render(request, 'forgot_password.html',cont)
            if email != 'given' and otp == 'given':
                given_email = request.POST['given_email']
                given_otp = request.POST['given_otp']
                otp = request.POST['otp']
                if given_otp == otp:
                    cont = {'step':3,'given_email':given_email}
                    return render(request, 'forgot_password.html',cont)
            if email == 'given' and otp == 'given':
                password = request.POST['password']
                user = request.user
                user.password = password
                user.save()
                login(request,user)
                return redirect('tmc:home')
        cont = {'step':1}
        return render(request, 'forgot_password.html',cont)

# Admin Panel Views

@only_admin_can_access
def admin_panel_users(request):

    users = list(User.objects.all())

    cont = {'users':users}
    return render(request, 'admin_panel_users.html', cont)

def get_most_point_earned_by():
    user = None
    highest = 0
    for i in models.ProblemSolved.objects.all():
        profile = models.Profile.objects.get(user=i.user)
        if profile.point > highest:
            user = i.user
            highest = profile.point
    return (user, highest)

def get_most_problems_solved_by():
    user = None
    highest = 0
    for i in User.objects.all():
        count = len(list(models.ProblemSolved.objects.filter(user=i)))
        if count > highest:
            user = i
            highest = len(list(models.ProblemSolved.objects.filter(user=i)))

    point = models.Profile.objects.get(user=user).point

    return (user, highest,point)

def get_most_solved_problem():
    highest = 0
    problem = None
    for i in models.Problem.objects.all():
        if len(list(models.ProblemSolved.objects.filter(problem=i))) > highest:
            problem = i
            highest = len(list(models.ProblemSolved.objects.filter(problem=i)))

    return (problem, highest)

@only_admin_can_access
def admin_panel_problems(request):
    problems = list(models.Problem.objects.all())
    hidden_problems = []
    public_problems = []
    for i in models.Problem.objects.all():
        if i.status == "Hidden":
            hidden_problems.append(i)
        else:
            public_problems.append(i)
    most_problems_solved_by = get_most_problems_solved_by()
    most_solved_problem = get_most_solved_problem()
    most_point_earned = get_most_point_earned_by()
    cont = {
        'problems':problems,
        'total_problems': len(problems),
        'hidden_problems_count': len(hidden_problems),
        'public_problems_count': len(public_problems),
        'most_problems_solved_by':most_problems_solved_by[0],
        'most_problems_solved_by_count':most_problems_solved_by[1],
        'most_problems_solved_by_point': most_problems_solved_by[2],
        'most_solved_problem': most_solved_problem[0],
        'most_solved_problem_count': most_solved_problem[1],
        'most_point_earned': most_point_earned[0],
        'most_point_earned_point': most_point_earned[1]
     }
    return render(request, 'admin_panel_problems.html', cont)

@only_admin_can_access
def delete_problem(request,pk):
    problem = models.Problem.objects.get(pk=pk)
    problem.delete()

    return redirect("/admin_panel/problems/")

@only_admin_can_access
def admin_panel_club_members(request):
    members = models.ClubMember.objects.all()
    form = forms.ClubMember()

    if request.method == "POST":
        form = forms.ClubMember(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    cont = {'members':members, 'form':form}

    return render(request, 'admin_panel_club_members.html', cont)

def is_admin(user):
    for g in user.groups.all():
        if g.name == "admin":
            return True

    return False

def admin_login(request):
    cont = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            if is_admin(user):
                login(request,user)
                return redirect("/admin_panel/")
            else:
                messages.error(request,'The given credentials does not match to admin credentials!')
                return redirect("/login_as_admin/")  
        else:
            messages.error(request,'The given username or the password is incorrect. Try again')
            return redirect("/login_as_admin/")

    return render(request, 'admin_login.html', cont)

@only_admin_can_access
def admin_panel_club_member_details(request, pk):
    member = models.ClubMember.objects.get(pk=pk)
    cont = {'member':member}

    return render(request, 'admin_panel_club_member_details.html', cont)
