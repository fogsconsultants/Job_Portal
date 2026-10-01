from django.urls import path
from jobs import views

urlpatterns=[
    path("",views.allJobs,name="all_jobs"),
    path("jobs-by-category/<int:sector>",views.allJobs,name="jobs_by_category"),
    path("job-detail/<int:job_id>",views.jobDetail,name="job_detail"),
    path("add-job/",views.addJob,name="add_job"),
    path("update-job/<int:job_id>/",views.updateJob,name="update_job"),
    path('apply-job/<int:job_id>/',views.applyJob,name="apply_job"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('close-job/<int:job_id>/', views.closeJob, name="close_job"),
    path('delete-job/<int:job_id>/', views.deleteJob, name="delete_job"),
    path('job/<int:job_id>/applicants/', views.applicants, name="applicants"),
    path('application/<int:application_id>/status/', views.updateApplicationStatus, name="update_application_status"),
    path('about/', views.about, name="about"),
    path('resources/', views.resources, name="resources"),
    path("login/",views.signIn,name="login"),
    path("register/",views.signUp,name="register"),
    path("logout/",views.Logout,name="logout")
]
