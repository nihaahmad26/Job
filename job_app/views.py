from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect ('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request,e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/jobs')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        logged_in_user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_jobs': Job.objects.all(),
            'my_fav': Job.objects.filter(Q(creator=logged_in_user) | Q(favorited_by = logged_in_user)),
            'not_my_fav': Job.objects.exclude(Q(creator=logged_in_user) | Q(favorited_by = logged_in_user)),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'show_all.html', context)

def show_page(request):
    return render(request,"add_job.html")

def add_job(request):
    if request.method=="GET":
        return redirect("/jobs/page")
        # return render(request,"add_quote.html")
    else:
        print(request.POST)
        errors = Job.objects.job_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/jobs/page')
        else:
            user = User.objects.get(id=request.session["user_id"])
            job = Job.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            location = request.POST['location'],
            creator = user
        )
            user.favorited_jobs.add(job)
        
            return redirect("/jobs")

def show_one(request, job_id):
    context = {
        'job': Job.objects.get(id=job_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_one.html", context)

def update(request, job_id):
    if request.method=="GET":
        context = {
            'job' : Job.objects.get(id=job_id),
        }
        return render(request,"show_one.html", context)
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/jobs/{job_id}")
    else:
        job = Job.objects.get(id=job_id)
        job.title = request.POST['title']
        job.description = request.POST['description']
        job.location = request.POST['location']
        job.save()
        return redirect(f"/jobs")
    
def delete(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()

    return redirect('/jobs')

def favorite(request, job_id):
    user = User.objects.get(id=request.session["user_id"])
    job = Job.objects.get(id=job_id)
    user.favorited_jobs.add(job)

    return redirect(f'/jobs/{job_id}')

def unfavorite(request, job_id):
    user = User.objects.get(id=request.session["user_id"])
    job = Job.objects.get(id=job_id)
    user.favorited_jobs.remove(job)

    return redirect(f'/jobs/{job_id}')


def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    
    return render(request, 'success.html', context)


