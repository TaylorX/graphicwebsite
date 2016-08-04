from django.shortcuts import render

from django.template import loader, Context

def index(request):
    return render(request,"index.html",{'title_name':'Graphics Generator'})

def execution_time(request):
    return render(request,"execution_time.html",{'test':'test'})

def post_data(request):
    if request.method == "POST":
    	if 'analysis_data' in request.POST and request.POST['analysis_data']:
            ready_to_analysis_data = request.POST['analysis_data']
            return render(request,"execution_time.html",{'info':'done','analysis_data':ready_to_analysis_data})
    else:
		return render(request,"index.html",{'info':'error'})