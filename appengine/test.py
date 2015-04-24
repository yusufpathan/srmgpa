#!/usr/bin/env python

import cgi
import re
from google.appengine.api import urlfetch

flag=1
form = cgi.FieldStorage() 
if(len(form.getlist("registerno"))==1):	
	if(len(form.getvalue("registerno"))==10):	
		regno = form.getvalue('registerno')
		dob = form.getvalue('dob')
		flag=0
grades = {'A+':10, 'A':9.5, 'A-':9, 'B+':8.5, 'B':8, 'B-':7.5, 'C+':7, 'C':6.5, 'C-':6, 'D':5, 'E':4, 'W':0, 'I':0, 'U':0}
if(flag==0):
#	url = "http://evarsity.srmuniv.ac.in/srmwebonline/exam/onlineResultInner.jsp?registerno=1081110009&iden=1&frmdate=1993-04-20
	url = "http://evarsity.srmuniv.ac.in/srmwebonline/exam/onlineResultInner.jsp?registerno="+regno+"&iden=1&frmdate="+dob
	result = urlfetch.fetch(url, deadline=10)
	result = result.content.upper()
	if(result.find("NOT AVAILABLE")!=-1):
		flag=2

print "Content-type:text/xml\r\n\r\n"	
def generateXML(data):
	data = re.findall(r'<TD.+</TD>', data)
	data = "".join(data)
	data = data.replace(' ALIGN="RIGHT"', '').replace(' ALIGN="CENTER"', '').replace(' CLASS="DYNACOLORTR1"', '').replace(" CLASS='DYNACOLORTR1' ", '').replace(' NOWRAP=""', '').replace(' STYLE="FONT-#SIZE: 15PX;', '').replace(' STYLE="FONT-SIZE: 15PX;"', '').replace(' WIDTH="5%"', '')
	data = re.sub(r'<TD><B>.*</B></TD>', '', data)
	data = data.replace('<TD></TD>', '').replace('<TD>', '')
	list1 = data.split('</TD>')
	list1 = list1[1:-1]
	counter = (len(list1)-7)/7
	mk = 7

	subject_c = []
	subject_n = []
	credits = []
	grade = []
	sem = str(2*(14-int(list1[3][3:5]))-1)
	i = total = divisor = 0

#Computing GPA
#GPA = sum(grade*credit)/sum(credit)
	while(i<counter):
		if(list1[7+((7*i)+2)]==sem):	
			total += float(grades[list1[7+((7*i)+6)]])*int(list1[7+((7*i)+5)])
			divisor += int(list1[7+((7*i)+5)])
			subject_c.append(list1[7+((7*i)+3)])	
			subject_n.append(list1[7+((7*i)+4)])	
			credits.append(str(list1[7+((7*i)+5)]))
			grade.append(str(grades[list1[7+((7*i)+6)]]))
		i+=1
#Generate XML file
	print '<result>'
	print '<name>'+list1[1]+'</name>'
	print '<regno>'+list1[3]+'</regno>'
	print '<branch>'+list1[5]+'</branch>'
	print '<subcodes>\n\t<subcode>'+'</subcode>\n\t<subcode>'.join(subject_c)+'</subcode>\n</subcodes>'
	print '<subjects>\n\t<subject>'+'</subject>\n\t<subject>'.join(subject_n)+'</subject>\n</subjects>'
	print '<creditlist>\n\t<credits>'+'</credits>\n\t<credits>'.join(credits)+'</credits>\n</creditlist>'
	print '<gradelist>\n\t<grade>'+'</grade>\n\t<grade>'.join(grade)+'</grade>\n</gradelist>'
	print '<totalcredits>'+str(divisor)+'</totalcredits>'
	print '<gpa>'+str(total/divisor)+'</gpa>'
	print '</result>'

if(flag==0):
	generateXML(result)
elif(flag==1):
	print '<result>\n\t<error>Enter Register No.</error>\n</result>'
else:
	print '<result>\n\t<error>Result is Not Available</error>\n</result>'