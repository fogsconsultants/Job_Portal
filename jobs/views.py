from django.shortcuts import render,redirect, get_object_or_404
from jobs.models import Jobs,Sectors, Applications
from jobs.forms import JobForm, ApplicationStatusForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
# Create your views here.

def allJobs(request,sector=None):
    all_sectors=Sectors.objects.all()
    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    if sector:
        job_posts=Jobs.objects.filter(sector__id=sector, is_active=True)
    else:
        job_posts=Jobs.objects.filter(is_active=True).order_by('-post_date')
    if query:
        job_posts = job_posts.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(sector__name__icontains=query))
    if location:
        job_posts = job_posts.filter(location__icontains=location)
    paginator = Paginator(job_posts, 9)
    jobs = paginator.get_page(request.GET.get("page"))
    featured_jobs = Jobs.objects.filter(is_active=True).order_by("-post_date")[:3]
    return render(request,"all-jobs.html",{'jobs':jobs,"sectors":all_sectors, "query": query, "location": location, "total_jobs": paginator.count, "featured_jobs": featured_jobs})
   
@login_required(login_url="login")
def jobDetail(request,job_id):
    job=get_object_or_404(Jobs, id=job_id, is_active=True)
    has_applied = request.user.is_authenticated and Applications.objects.filter(user=request.user, job=job).exists()
    return render(request,"job-detail.html",{"job":job, "has_applied": has_applied})
 

@user_passes_test(lambda user: user.is_staff, login_url="login")
def addJob(request):
    if request.method == "POST":
        form=JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.author = request.user
            job.save()
            messages.success(request, "Your job has been published.")
            return redirect("job_detail", job.id)
    else:
        form=JobForm()
    return render(request,"add-jobs.html",{"form":form})

@user_passes_test(lambda user: user.is_staff, login_url="login")
def updateJob(request,job_id):
    job=get_object_or_404(Jobs, id=job_id)
    if request.method=="POST":
        form=JobForm(request.POST,instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job details updated.")
            return redirect("job_detail",job_id)
    else:
        form=JobForm(instance=job)
    return render(request,"update-job.html",{"form":form})

@login_required(login_url="login")
def dashboard(request):
    applications = Applications.objects.filter(user=request.user).select_related("job", "job__sector").order_by("-date")
    posted_jobs = Jobs.objects.all().prefetch_related("applications_set").order_by("-post_date") if request.user.is_staff else Jobs.objects.none()
    return render(request, "dashboard.html", {"applications": applications, "posted_jobs": posted_jobs})

@user_passes_test(lambda user: user.is_staff, login_url="login")
def closeJob(request, job_id):
    if request.method != "POST":
        return redirect("dashboard")
    job = get_object_or_404(Jobs, id=job_id)
    job.is_active = not job.is_active
    job.save(update_fields=["is_active"])
    messages.success(request, f"Job {'reopened' if job.is_active else 'closed'} successfully.")
    return redirect("dashboard")

@user_passes_test(lambda user: user.is_staff, login_url="login")
def deleteJob(request, job_id):
    if request.method != "POST":
        return redirect("dashboard")
    job = get_object_or_404(Jobs, id=job_id)
    title = job.title
    job.delete()
    messages.success(request, f'“{title}” has been deleted.')
    return redirect("dashboard")

@user_passes_test(lambda user: user.is_staff, login_url="login")
def applicants(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)
    applications = Applications.objects.filter(job=job).select_related("user").order_by("-date")
    return render(request, "applicants.html", {"job": job, "applications": applications, "status_choices": ApplicationStatusForm().fields["status"].choices})

@user_passes_test(lambda user: user.is_staff, login_url="login")
def updateApplicationStatus(request, application_id):
    if request.method != "POST":
        return redirect("dashboard")
    application = get_object_or_404(Applications, id=application_id)
    form = ApplicationStatusForm(request.POST)
    if form.is_valid():
        application.status = form.cleaned_data["status"]
        application.save(update_fields=["status"])
        messages.success(request, "Applicant status updated.")
    else:
        messages.error(request, "Please select a valid application status.")
    return redirect("applicants", job_id=application.job_id)

def about(request):
    return render(request, "about.html")

def resources(request):
    return render(request, "resources.html")

def signIn(request):
    if request.method=="POST":
        email=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=email,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("all_jobs")
        else:
            messages.error(request,"Invalid username or password")
            return redirect("login")
    return render(request,"login.html")

def signUp(request):
    if request.method=="POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        if not first_name or not last_name or not email or not password:
            messages.error(request, "Please complete every required field.")
            return redirect("register")
        if password != confirm_password:
            messages.error(request, "Passwords must match.")
            return redirect("register")
        if len(password) < 8:
            messages.error(request, "Your password must be at least 8 characters.")
            return redirect("register")
        if User.objects.filter(username=email).exists():
            messages.info(request,"User already exists")
            return redirect("login")
        else:
            user=User.objects.create_user(username=email,first_name=first_name,
                                    last_name=last_name,password=password)
            user.save()
            messages.success(request,"Welcome to JobPortal. Please login to continue")
            return redirect("login")
    return render(request,"register.html")


def Logout(request):
    auth.logout(request)
    return redirect("all_jobs")

@login_required(login_url="login")
def applyJob(request, job_id):
    if request.method != "POST":
        return redirect("job_detail", job_id=job_id)
    job = get_object_or_404(Jobs, id=job_id, is_active=True)
    _, created = Applications.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, "Your application has been submitted.")
    else:
        messages.info(request, "You have already applied for this position.")
    return redirect("job_detail", job_id=job_id)
