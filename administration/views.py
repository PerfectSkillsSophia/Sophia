from django.shortcuts import render, redirect , HttpResponseRedirect 
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from assessments.models import *
from administration.models import *
from django.urls import reverse
from django.db.models import Q
from sophia import settings
from thefuzz import fuzz,process

@staff_member_required
@login_required(login_url='login')
def dashboard(request):
	assessment =allAssessment.objects
	video = videoAns.objects.all()[:5]
	return render(request, 'dashboard.html',{'assessment':assessment, 'video':video})

@staff_member_required
@login_required(login_url='login')
def allAnswer(request):
	url =settings. MEDIA_URL
	video = videoAns.objects.all()
	return render(request, 'all_submmision.html',{'video':video,'url':url})

@staff_member_required
@login_required(login_url='login')
def searchbar(request):
	query = request.GET.get('q')
	url =settings. MEDIA_URL
	if query:
		results = videoAns.objects.filter(Q(user_name__icontains=query) | Q(assessment_name__icontains=query))
	else:
		results = videoAns.objects.all()
	return render(request, 'all_submmision.html', {'results': results, 'query': query,'url':url})
	
	
@staff_member_required
@login_required(login_url='login')
def Add_assessment(request):
	if request.method == 'GET':
		ass_name = request.GET.get('ass_name')
		ass_dec = request.GET.get('ass_dec')
		new_ass = allAssessment()
		new_ass.assessmentName = ass_name
		new_ass.assessmentDes = ass_dec
		new_ass.save()
		return redirect('addassessment')
	return redirect('addassessment')

@staff_member_required
@login_required(login_url='login')
def add_assessment(request):
	return render(request,'add_assessments.html')


@staff_member_required
@login_required(login_url='login')
def view_assessments(request,ass_id):
	
	ass_id = ass_id
	assessment = allAssessment.objects.filter(assId=ass_id)
	allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:5]
	return render(request, 'assview.html',{'ques':allque,'ass':assessment})

@staff_member_required
@login_required(login_url='login')
def Add_question(request):	
		if request.method == 'GET':
			que = request.GET.get('que')
			ass_name = request.GET.get('ass')
			ass = allAssessment.objects.get(assessmentName = ass_name)
			ass_id = ass.assId
			new_que = Question()
			new_que.quostion = que
			new_que.assessment = ass
			new_que.save()
			return HttpResponseRedirect(reverse("view", args=(ass_id,)))
		return HttpResponseRedirect(reverse("view", args=(ass_id,)))
## ebb5f4cc42d841d0aa7369f975d9af42
def view_analysis (request,ansId):
	url =settings. MEDIA_URL
	result = videoAns.objects.filter(ansId=ansId)


	return render(request, "analysis.html",{"result":result,'url':url})
	

@staff_member_required
@login_required(login_url='login')
def generate_tras(request,ansId):
	ref_url = request.META.get('HTTP_REFERER')
	result = videoAns.objects.get(ansId=ansId)
	vf = result.videoAns.path
	import requests
	API_KEY="623cfea0aba24d8f981195bbc20d48e0"
	filename = vf

#Upload Module Begins
	def read_file(filename, chunk_size=5242880):
		with open(filename, 'rb') as _file:
			while True:
				data = _file.read(chunk_size)
				if not data:
					break
				yield data

	headers = {'authorization': API_KEY}
	response = requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(filename))

	json_str1=response.json()
#Upload Module Ends

#Submit Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript"
	json = {
    	"audio_url": json_str1["upload_url"]
	}

	response = requests.post(endpoint, json=json, headers=headers)

	json_str2=response.json()
#Submit Module Ends

#CheckStatus Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript/" + json_str2["id"]

	response = requests.get(endpoint, headers=headers)

	json_str3=response.json()

	while json_str3["status"]!="completed":
		response = requests.get(endpoint, headers=headers)
		json_str3=response.json()
#CheckStatus Module Ends
	result.trasnscript = json_str3["text"]
	result.save()
	messages.success(request, 'Transcript is generated Successfully.')
	return HttpResponseRedirect(ref_url)    		

def generate_result(request):
	if request.method == 'GET':
		ansId = request.GET.get('ansId')
		expected_answer=request.GET.get('expected_answer')
		s2 = expected_answer
		ref_url = request.META.get('HTTP_REFERER')
		answer=videoAns.objects.filter(ansId=ansId)
		for trans in answer:
			s1 = trans.trasnscript
	
		print(s2)
		print(s1)
		print(ansId)

		if fuzz.partial_token_sort_ratio(s1,s2)==100:
			Percent_ratio=100
		elif fuzz.partial_token_sort_ratio(s1,s2)!=100 and fuzz.token_sort_ratio(s1,s2)!=100 and fuzz.token_set_ratio(s1,s2)!=100 and fuzz.partial_ratio(s1,s2)!=100:
			Percent_ratio=max(fuzz.partial_token_sort_ratio(s1,s2),fuzz.token_sort_ratio(s1,s2),fuzz.token_set_ratio(s1,s2),fuzz.partial_ratio(s1,s2))
		else:
			Percent_ratio=((fuzz.partial_token_sort_ratio(s1,s2)+fuzz.token_sort_ratio(s1,s2)+fuzz.token_set_ratio(s1,s2)+fuzz.partial_ratio(s1,s2))/400)*100
		answer=videoAns.objects.get(ansId=ansId)
		answer.answer_accurecy=Percent_ratio
		print("Accuracy of Answer is: ",Percent_ratio,"%")
		print(type(int(Percent_ratio)))
		answer.save()

		return HttpResponseRedirect(ref_url)







    


	