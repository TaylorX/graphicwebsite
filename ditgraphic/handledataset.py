import os
 
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

def paser_value_list(listName, data, column_size):

	listValue = [[str(0) for i in range(column_size) ] for j in range(len(listName)) ]

	mStr = ''
	column_size = column_size - 1
	count = 0
	for i, content in enumerate(data):
		mod = i%column_size
		if mod < column_size-1:
			mStr = mStr + content + ','
			if mod is 0:
				listValue[count][mod] = listName[count]
			listValue[count][mod+1] = content
		else:
			if i < len(data)-1:
				mStr = mStr + content
				listValue[count][mod+1] = content
				count+=1
			else:
				mStr = mStr + content
				listValue[count][mod+1] = content
				count+=1
	return mStr, listValue

def read_uploaded_csv_file(filename):

	f = open('static/data/'+filename,'r')
	
	list_title = []
	list_content = []
	column_size = ''
	for row in open('static/data/' + filename):
		row = f.readline()
		logLine = str(row);
		split_item = logLine.split('\n')
		for content in split_item:
			if content:
				temp = content.split(',')
				column_size = len(temp)
				for count, cc in enumerate(temp):
					if count == 0 and cc != '':
						list_title.append(cc)
					else:
						if cc:
							list_content.append(cc)

	return list_title, list_content, column_size

def read_uploaded_logcat_file(filename):

	f = open('static/data/' + filename,'r')
	list1 = []
	devicename = ''
	AppVersion = ''
	for row in open('static/data/' + filename):
		row = f.readline()
		logLine = str(row);

		if '[performance]' in logLine and 'autoFocus' not in logLine:
			list1.append(logLine)
		if 'DEVICE=D' in logLine:
			logLine = logLine.split('=')
			logLine = logLine[1].split('\r\n')
			devicename = 'Project:'+logLine[0]
		if 'printAppVersion=' in logLine:
			logLine = logLine.split('=')
			AppVersion = '	AppVersion:'+logLine[1]

	f.close()

	list2 = []
	countItem = 0
	countItemLine = 0
	sCountTag = True
	for logLine in list1:

		if 'launch time:' in logLine:
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

	listMean = [0 for x in range(countItemLine)]

	count_line_item = 0
	count_total_item = 1
	total = ''
	for logLine in list2:
		count_line_item+=1
		if count_line_item < countItemLine:
			total = total + logLine+","
			listMean[count_line_item-1] += int(logLine)
		else:
			if count_total_item < countItem:
				total = total + logLine+';'
				listMean[count_line_item-1] += int(logLine)
				count_total_item+=1
			else:
				total = total + logLine
				listMean[count_line_item-1] += int(logLine)
			count_line_item=0

	listMean[:] = [x / countItem for x in listMean]

	return total, listMean, devicename+AppVersion
