from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

from assessments.models import videoAns,Feedback
from administration.models import allAssessment

# Create your views here.


@login_required(login_url='login')
def welcomeScreen(request,ass_name):
    global slug 
    slug = ass_name
    return render(request, 'welcomscreen.html')

## View For Enter link for Assessment link.
@login_required(login_url='login')
def afterlogin(request):
	return render(request,'assessment_link.html')

@login_required(login_url='login')
def answer(request):
    ass_name = slug
    assname = ass_name
    allque = allAssessment.objects.get(assessmentName=ass_name).question_set.all()
    return render(request, 'answer.html', {'question':allque , 'assname':assname} )


@login_required(login_url='login')
def fileUpload(request):

    if request.method == 'POST':
        
        fileName = request.user
        video = request.FILES.get('data')
        assessment_name = request.POST.get('ass_name')

        videoAns.objects.create(
            user_name=fileName,
            assessment_name=assessment_name,
            videoAns=video,)

        return redirect(request.path)

@login_required(login_url='login')
def feedback(request):
    if request.method == 'POST':
        feedback_type = request.POST.get('feedback_type')
        feedback = Feedback(user=request.user, feedback_type=feedback_type)
        feedback.save()
        return redirect('thankyou')

    return render(request, 'feedback.html')

@login_required(login_url='login')
def thankyou(request):
    return render(request,'thankyou.html')




