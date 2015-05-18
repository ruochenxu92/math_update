import os
for i in range(11, 33):
	target = 'SuperQQSpider' + str(i) + '.py'
	cmd = 'cp SuperQQSpider1.py ' + target
	os.system(cmd)