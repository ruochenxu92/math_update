import os
import sys
import django
from os.path import expanduser
home = expanduser('~')
path = os.path.abspath(home + '/testproject/testproject.settings')
sys.path.append(os.path.abspath(os.path.join(path, os.path.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testproject.settings")
django.setup()

import json
from task.models import cs499Item
import os, datetime
import codecs
_open_func_bak = open # Make a back up, just in case
open = codecs.open
import json
import ijson

def escape(str):
	return str.encode('ascii',errors='ignore')

json_file_path = home + '/superqq_spider/cs_update.json'
json_file = open(json_file_path, encoding='utf-8')
parser = ijson.parse(json_file)
j = {}
i = 0
for prefix, event, value in parser:
	if event == 'start_map':
		j = {}
	elif event == 'end_map':
		try:
			if len(cs499Item.objects.filter(title=j['title'])) == 0:
				cs = cs499Item(urllink=j['urllink'], pdflink=j['pdflink'], category=j['category'], authors=j['authors'],title=j['title'], subjects=j['subjects'], abstract=j['abstract'], date=j['date'])
				cs.save()
				print "successfully"
			else:
				print "duplicate"
		except Exception:
			print Exception
			print i
	else:
		if prefix == 'item.urllink':
			j['urllink'] = escape(value)
		if prefix == 'item.pdflink':
			j['pdflink'] = escape(value)
		if prefix == 'item.category':
			j['category'] = escape(value)
		if prefix == 'item.authors':
			j['authors'] = escape(value)
		if prefix == 'item.title':
			j['title'] = escape(value)
		if prefix == 'item.subjects':
			j['subjects'] = escape(value)
		if prefix == 'item.abstract':
			j['abstract'] = escape(value)
		if prefix == 'item.date':
			j['date'] = escape(value)
	i += 1


