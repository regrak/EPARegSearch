import urllib2
import re
import os
import csv


#def getregs(chapter):
#	target = "https://www.gpo.gov/fdsys/pkg/CFR-2016-title40-vol" + str(chapter) + "/html/CFR-2016-title40-vol" + str(chapter) + ".htm"
#	return urllib2.urlopen(target).read()

#for i in range(1, 38):
#	file = open(str(i)+".txt", 'w')
#	file.write(getregs(i))
#	file.close()

def makepartlink(numchapter, numpart):
	return "https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=&SID=0d738f4009e14b04bd075a630bcc1d20&mc=true&n=sp40." + numchapter + "." + numpart + ".b&r=SUBPART&ty=HTML#se40." + numchapter + "." + numpart + "_1" + str(subsection)

def partlink(chapnum, partnum):
	chapnum, partnum = str(chapnum), str(partnum)
	return "https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=&SID=beb0ac4effa006b7d7cffcf88b9c1684&mc=true&n=pt40." + str(chapnum) + "." + str(partnum) + "&r=PART&ty=HTML"

def subseclink(chapnum, secnum):
	chapnum, secnum = str(chapnum), str(secnum)
	partnum = secnum.split(".")[0]
	subnum = secnum.split(".")[1]
	return "https://www.ecfr.gov/cgi-bin/retrieveECFR?gp=&SID=beb0ac4effa006b7d7cffcf88b9c1684&mc=true&n=pt40." + chapnum + "." + partnum + "&r=PART&ty=HTML#se40." + chapnum + "." + partnum + "_1" + subnum

print(subseclink("18", "75.1"))

def newsearchregs(term):
	os.chdir("/home/gabriel/Documents/Summer17/EPA/SearchRegs/Chapters")
	results = []
	for i in range(1,38):
		text = open(str(i) + ".txt", 'r').read()
		partre = re.compile("PART [0-9]+_[^a-z]*?" + term.upper() + "[^-]*", re.DOTALL)
		partdivs = [p for p in partre.finditer(text)]
		if partdivs:
			for result in partdivs:
				m = re.compile("[0-9]+").search(result.group())
				partnumber = m.group()
				partcontent = result.group()[m.span()[1] + 1:]
				partcontent.replace("\n", " ")
				results.append(["Part", partnumber, partcontent, partlink(i, partnumber)])
		subsecre = re.compile(">\nSec\. [0-9]+\.[0-9]+[\sA-Za-z0-9,\n]*?" + term + "[\sA-Za-z0-9,\n:]*", re.DOTALL)
		subsecdivs  = [s for s in subsecre.finditer(text)]
		if subsecdivs:
			for result in subsecdivs:
				m = re.compile("[\.0-9]{2,}").search(result.group())
				partnum = m.group()
				partcontent = result.group()[m.span()[1]:]
				partcontent.replace("\n", " ")
				results.append(["Subsection", partnum, partcontent, subseclink(i, partnum)])
	print(results)
	return results
		#First do parts, then subsections with most instances.
	
def resultscsv(term, destinationpath):
	rowrows = newsearchregs(term)
	if not rowrows:
		return None
	f =  open(destinationpath + "/" + term + ".csv", 'w')
	writer = csv.writer(f)
	writer.writerow(["Main Part or Subsection?", "Number of part or subsection", "Full Line of Result", "Link to Result"])
	writer.writerows(rowrows)

def makechemexamples():
	with open("/home/gabriel/Documents/Summer17/EPA/SearchRegs/chemlist.csv") as f:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			chem = row[1]
			print(chem)
			if len(chem.split()) < 2:
				try:
					resultscsv(chem, "/home/gabriel/Documents/Summer17/EPA/SearchRegs/ExampleSearches")
				except:
					continue

resultscsv("emission", "/home/gabriel/Documents/Summer17/EPA/SearchRegs/ExampleSearches")



