import os
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response, render

from django.template import loader, Context

from django import template

def index(request):
    return render(request,"index.html",{'title_name':'DIT Chart Generator'})

def manual(request):
	if request.method == "POST":
		if 'analysis_data' in request.POST and request.POST['analysis_data']:
			ready_to_analysis_data = request.POST['analysis_data']

			mStr = ''
			for line in ready_to_analysis_data:
				# split_item = line.split("\n")
				mStr = mStr + line
				break
				# for content in split_item:
				# 	split_item = content.split(',')
				# 	mStr = split_item
				# 	mStr = mStr + split_item[0]

			return render(request,"execution_time_manual.html",{'analysis_data':mStr})
	else:
		return render(request,"index.html",{'info':'error'})

def upload_2(request):
    if request.method == 'POST':
    	file_ = request.FILES['file']
    	filename = str(request.FILES['file']);
        handle_uploaded_file(file_, filename)

        listName, listValue, temp = read_uploaded_csv_file(filename)

        return render(request,"execution_time_2.html", {'analysis_data_1':listName,'analysis_data_2':listValue})

    return HttpResponse("index.html", {'message':'Failed'})

def upload(request):
    if request.method == 'POST':
    	file_ = request.FILES['file']
    	filename = str(request.FILES['file']);
        handle_uploaded_file(file_, filename)

        # data = open('static/data/' + filename,'r')
        # return render(request,"execution_time.html", {'analysis_data':data.read()})
        
        data = read_uploaded_file(filename)
        return render(request,"execution_time.html", {'analysis_data':data})

    return HttpResponse("index.html", {'message':'Failed'})

def handle_uploaded_file(file, filename):
    if not os.path.exists('static/data/'):
        os.mkdir('static/data/')

    with open('static/data/' + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def paser_name_list(data):
	mStr = ''
	for i, content in enumerate(data,1):
		if i < len(data):
			mStr = mStr + content + ';'
		else:
			mStr = mStr + content
	return mStr

def paser_value_list(data, size):
	mStr = ''
	size = size - 1
	for i, content in enumerate(data):
		mod = i%size
		if mod < size-1:
			mStr = mStr + content + ','
		else:
			if i < len(data)-1:
				mStr = mStr + content + ';'
			else:
				mStr = mStr + content
	return mStr

def read_uploaded_csv_file(filename):

	f = open('static/data/'+filename,'r')
	
	list_title = []
	list_content = []
	column_size = ''
	temp = ''
	for row in open('static/data/' + filename):
		row = f.readline()
		logLine = str(row);
		split_item = logLine.split('\n')
		for content in split_item:
			split_item = content.split(',')
			column_size = len(split_item)
			temp = split_item
			for cc in split_item:
				if cc.isalpha():
					list_title.append(cc)
				else:
					if cc:
						list_content.append(cc)

	return paser_name_list(list_title), paser_value_list(list_content, column_size), temp

def read_uploaded_file(filename):

	f = open('static/data/' + filename,'r')
	list1 = []
	for row in open('static/data/' + filename):
		row = f.readline()
		logLine = str(row);

		if '[performance]' in logLine and 'autoFocus' not in logLine:
			list1.append(logLine)

	f.close()

	list2 = []
	countItem = 0
	countItemLine = 0
	sCountTag = True
	for logLine in list1:

		if 'Relaunch time:' in logLine:
			# print logLine
			if countItem > 0:
				sCountTag = False
			countItem += 1

		if sCountTag:
			countItemLine += 1

		splitlogLine = logLine.split(' ')
		for content in splitlogLine:
			if 'ms' in content:
				for time in content.split('ms.'):
					if time.isdigit():
						list2.append(time)

	# return countItem
	# return countItemLine

	count_line_item = 0
	count_total_item = 1
	total = ''
	for logLine in list2:
		count_line_item+=1
		if count_line_item < countItemLine:
			total = total + logLine+","
		else:
			if count_total_item < countItem:
				total = total + logLine+';'
				count_total_item+=1
			else:
				total = total + logLine
			count_line_item=0

	return total
