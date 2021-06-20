from django.db.models.query import FlatValuesListIterable, RawQuerySet
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from . import models
from . import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
import random

# External Functions

def is_problem_maker(user):
    for g in user.groups.all():
        if g.name == "Problem Maker":
            return True

    return False

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

    return f"#{trailing}"

# Create your views here.

def home(request):
    profile = None
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    return render(request, 'home.html',{'profile':profile})

def about(request):
    return render(request,'about.html') 

def problem_set(request):
    profile = None 
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)

    cont = {'profile':profile,'is_problem_maker':is_problem_maker(request.user)}

    return render(request, 'problemset.html',cont)

def topic_probelm_set(request, topic):
    profile = None
    if request.user.is_authenticated:
        profile = models.Profile.objects.get(user=request.user)
    problems = models.Problem.objects.filter(problem_cat=topic)
    return render(request,"topic_problemset.html",{'profile':profile,'problems':problems,'topic':topic})

@login_required(login_url="/user_login/")
def submission(request,status,problem,tried):
    return render(request,"submission.html", context={
        'p':problem,
        'status':status,
        'submission':tried,
    })

def problem(request,pk):
    problem = models.Problem.objects.get(pk=pk)
    first_solve = "None"
    if not problem.first_solve == "None":
        first_solve = User.objects.get(username=problem.first_solve).first_name

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
                if problem.tried.count() <= 1:
                    problem.first_solve = request.user.username
                    print(request.user.username, " first solved it")
                    problem.save()
                return submission(request,"Correct",problem,tried)
            return submission(request,"Wrong",problem,tried)

        if already_solved() or already_tried():
            return HttpResponse("Already Solved")
    
    cont = {'problem':problem,'solved':already_solved(), 'first_solve_username': problem.first_solve ,'first_solve':first_solve}
    
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
        
        return redirect(f"/topic_problems/{problem.problem_cat}/#problem-{problem.id}")

    return render(request, 'add_problem.html',cont)


def profile(request):
    def get_solved_problem_count(topic=None):
        solved = 0
        for p in models.ProblemSolved.objects.all():
            if p.user.username == request.user.username:
                solved += 1

        return solved

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

    print(get_math_progress(),get_physics_progress())

    cont = {
        'profile':models.Profile.objects.get(user=request.user),
        'progress':get_progress(),
        'math_progress': get_math_progress(),
        'physics_progress': get_physics_progress(),
        'solved':get_solved_problem_count(),
        'math_solved': get_math_solved_problem_count(),
        'physics_solved': get_physics_solved_problem_count(),
        'total_problems':get_total_problems(),
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
            if username[0] != "#":
                username = "#"+username 

            user = authenticate(username=username,password=password)

            if user is not None:
                login(request,user)

            return redirect('tmc:home')
        
        return render(request,'login.html')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("tmc:home")
    else:
        return redirect("tmc:user_login")

def leaderboard(request):
    class Rank:
        def __init__(self, name, score, solve, tried):
            self.name = name
            self.score = score
            self.solve = solve
            self.tried = tried
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
        rank = Rank(profile.user.username, profile.point, get_solved_problem_count(i),get_tried_problem_count(i)) 
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
        print("P",j)
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

    cont = {'ranks':final_rank, 'highest':highest}
    return render(request, 'leaderboard.html',cont)

def user_registration(request):
    if request.user.is_authenticated:
        return redirect("tmc:home")
    else:
        if request.method == "POST":
            def get_tmc_id():
                return get_id(User,6)

            print(get_tmc_id())

            email = request.POST['email']
            pswd = request.POST['password']
            f_name = request.POST['first_name']
            l_name = request.POST['last_name']
            username = get_tmc_id()
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

            user = authenticate(username=username,password=pswd)

            if user is not None:
                login(request, user)

            return redirect("tmc:profile")
            
        return render(request, 'registration.html')

