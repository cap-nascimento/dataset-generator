import urllib.request
#import requests as req
import json

links = ['https://www.metal-archives.com/band/view/id/',
		 'https://www.metal-archives.com/band/discography/id/%s/tab/all']

def band_model():
	band_obj = {
		"name" : "",
		"country" : "",
		"countryLocation" : "",
		"status": "",
		"formationYear" : 0,
		"genre" : "",
		"lyricalThemes" : "",
		"currentLabel" : "",
		#"yearsActive" : "",
		"discography" : []
	}
	return band_obj

def discography_model():
	discography_obj = {
		"title" : "",
		"type" : "",
		"year" : 0,
		"tracklist": []
	}
	return discography_obj

def band_data(id):
	req = urllib.request.Request(links[0]+str(id),
			headers={'User-Agent' : 'Magic Browser'})
	band_data = ""
	try:
		con = urllib.request.urlopen(req)
		content = con.read().decode('utf-8')
		split1 = content.split('band_info')
		split2 = split1[1].split('#band_tab_discography')
		band_data = split2[0]
	except:
		return "{}"
	return band_data

def band_discography(id):
	req = urllib.request.Request(links[1]%str(id),
			headers={'User-Agent' : 'Magic Browser'})
	band_discography = ""
	try:
		con = urllib.request.urlopen(req)
		band_discography = con.read().decode('utf-8')
	except:
		return "{}"
	return band_discography

def album_data(link):
	req = urllib.request.Request(link,
		headers={'User-Agent' : 'Magic Browser'})
	album_data = ""
	try:
		con = urllib.request.urlopen(req)
		album_data = con.read().decode('utf-8')
	except:
		return "{}"
	return album_data

def get_string1(s):
	spl = s.split('</a>')
	spl = spl[0].split('>')
	return spl[len(spl)-1]

def get_string2(s):
	spl = s.split('<dd')
	spl = spl[1].split('</dd>')
	spl = spl[0].split('>')
	return spl[1]

def get_string3(s):
	spl = s.split('>')
	return spl[1]

def get_link(s):
	spl = s.split('href="')
	spl = spl[1].split('"')
	return spl[0]

def isNum(x):
	if(len(x) == 4):
		for i in range(4):
			if(x[i] < '0' or x[i] > '9'):
				return False
		return True
	return False


def format_band_data(content):
	#print(content)
	if(content == "{}"): return "{}"
	arr = content.split("<dt>")
	#print(arr)
	band = band_model()
	band['name'] = get_string1(arr[0])

	for i in range(1, len(arr)):
		if(arr[i][0:17] == 'Country of origin'):
			band['country'] = get_string1(arr[i])
		if(arr[i][0:8] == 'Location'):
			band['countryLocation'] = get_string2(arr[i])
		if(arr[i][0:6] == 'Status'):
			band['status'] = get_string2(arr[i])
		if(arr[i][0:9] == 'Formed in'):
			yearFormation = get_string2(arr[i])
			if isNum(yearFormation):
				band['formationYear'] = int(yearFormation)
			else:
				band['formationYear'] = -1
		if(arr[i][0:5] == 'Genre'):
			band['genre'] = get_string2(arr[i])
		if(arr[i][0:14] == 'Lyrical themes'):
			band['lyricalThemes'] = get_string2(arr[i])
		if(arr[i][0:13] == 'Current label'):
			no_label = get_string2(arr[i])
			if(no_label == 'Unsigned/independent'):
				band['currentLabel'] = no_label
			else:
				band['currentLabel'] = get_string1(arr[i])
		# if(arr[i][0:12] == 'Years active'):
		# 	print(arr[i])
		# 	spl = arr[i].split('-')
		# 	years = []
		# 	for j in range(len(spl)):
		# 		for k in range(len(spl[j])):
		# 			if((spl[j][k] >= '0' and spl[j][k] <= '9')):
		# 				years.append(spl[j][k:k+5])
		# 				break
		# 			if((spl[j][k:k+7] == 'present')):
		# 				years.append('present')
		# 				break

		# 	j = 0
		# 	s = ""
		# 	print(years)
		# 	while j < len(years):
		# 		s += years[j] + '-' + years[j+1] + ' '
		# 		j += 2
		# 	band['yearsActive'] = ''
	#print(arr)
	return band

def format_album_data(content):
	arr = content.split("wrapWords")
	tracks = []
	for i in range(1, len(arr)):
		spl = arr[i].split('>')
		spl = spl[1].split('<')
		tracks.append(spl[0].replace('\n', ''))
	return tracks

def format_band_discography(content, band):
	if(content == "{}"): return "{}"
	arr = content.split('<a')
	#print(content)
	for i in range(1, len(arr)):
		cd = discography_model()
		spl = arr[i].split('</td>')
		if(len(spl) >= 3):
			cd['title'] = get_string3(spl[0]).replace('</a', '')
			cd['type'] = get_string3(spl[1])
			cd['year'] = int(get_string3(spl[2]))
			tracks = format_album_data(album_data(get_link(spl[0])))
			for track in tracks:
				cd['tracklist'].append(track);
			band['discography'].append(cd)
	return band

first = 130084
last = 3540409485
arq = open("output.json", "a")
for i in range(last, first, -1):
	print("Parseando banda...")
	band = format_band_data(band_data(i))
	if(band != "{}"):
		band = format_band_discography(band_discography(i), band)
		arq.write(json.dumps(band, ensure_ascii=False) + '\n')
		print(band)
	#arq.write(json.dumps(band, ensure_ascii=False) + '\n')
# band = format_band_data(band_data(446))
# if(band != "{}"):
# 	band = format_band_discography(band_discography(446), band)
# print(band)
# arq.write(json.dumps(band, ensure_ascii=False))
