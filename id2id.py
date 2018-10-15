#!/usr/bin/python
import sys,getopt
import urllib
import xml.sax
import xml.sax.handler
import pprint
import logging

version = '''
================================================================================================================================
./db2db.py  help document
	
	version:1.0
	author:zhangjiankun

 this python script can convert different ids between ensembl transcript id and RefSeq mRNA accession

option:
	--help/-h: display help information
	--input/-i: r(RefSeq mRNA accession) or e(Ensembl transcript id) input type
	--values/-v: NMXXXX,NMXXXX... or ENSTXXXX,ENSTXXXX...
	-f: the input file
	--output file:id2id_result.txt

for example:
	./db2db.py -i r -v 'NM_145554,NM_001081382' 
	./db2db.py -i r -f /home/user/tese_id.txt
================================================================================================================================'''

class XMLHandlerE(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
		self.InputValue = ""
		self.RefSeqmRNAAccession = ""
		self.array = []
	def startElement(self,tag,attributes):
		self.CurrentData = tag
		if tag == "item":
			pass
	def characters(self,content):
		if self.CurrentData == "InputValue":
			self.InputValue = content
		elif self.CurrentData == "RefSeqmRNAAccession":
			self.RefSeqmRNAAccession = content
	def endElement(self,tag):
		if self.CurrentData == "InputValue":
			self.array.append(self.InputValue)
		elif self.CurrentData == "RefSeqmRNAAccession":
			self.array.append(self.RefSeqmRNAAccession)
		self.CurrentData = ""
	def getresult(self):
		return self.array

class XMLHandlerR(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.CurrentData = ""
                self.InputValue = ""
                self.EnsemblTranscriptId = ""
		self.array = []
     	def startElement(self,tag,attributes):
                self.CurrentData = tag
                if tag == "item":
                        pass
        def characters(self,content):
                if self.CurrentData == "InputValue":
                        self.InputValue = content
                elif self.CurrentData == "EnsemblTranscriptID":
                        self.EnsemblTranscriptID = content
        def endElement(self,tag):
		if self.CurrentData == "InputValue":
                        self.array.append(self.InputValue)
                elif self.CurrentData == "EnsemblTranscriptID":
                        self.array.append(self.EnsemblTranscriptID)
                self.CurrentData = ""
	def getresult(self):
                return self.array

def main(argv):
	logging.basicConfig(level=logging.INFO,format="%(asctime)s %(message)s")
	logging.info("Start")
	inputid = ''
	inputtype = ''
	inputfile = ''
	try:  
		opts, args = getopt.getopt(argv, "hi:v:f:t", ["help","input","value","file","type"])  
	except getopt.GetoptError:  
		sys.exit(2)
	for o,a in opts:
		if o in ("-h","--help"):
			print version
			sys.exit()
		elif o in ("-input","-i"):
			inputtype = a
		elif o in ("--value","-v"):
			inputid = a
		elif o in ("--file","-f"):
			inputfile = a
		else:
			logging.warning("wrong option occurs")
			sys.exit(2)

	if inputfile:
		with open(inputfile,"r") as f:
			inputvalue = f.readlines()
			value = []
			for i in inputvalue:
				value.append(i.strip("\n"))
			seq = ","
			inputid = seq.join(value)
			print inputid
	else:
		pass

	if inputtype == "r":
		logging.info("wait a minute")
		url = 'https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?method=db2db&format=row&input=refseqmrnaaccession&inputValues='+inputid+'&outputs=ensembltranscriptid'
		u = urllib.urlopen(url)
		response = u.read()
		xh = XMLHandlerR()
		xml.sax.parseString(response,xh)
		data = xh.getresult()
		with open("id2id_result.txt","w") as f:
			f.write("RefSeq_mRNA_accession\tEnsemblTrancriptID\n")
			for n in range(len(data)-1):
				if n%2 == 0:
					string = str(data[n+1]).split("//")
					for nn in string:
						f.write(str(data[n])+"\t"+nn+"\n")
				else:
					pass
		logging.info("DONE please check output file 'id2id_result.txt'")
	elif inputtype == "e":
		print "please wait a minute"
		url = 'https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?method=db2db&format=row&input=ensembltranscriptid&inputValues='+inputid+'&outputs=refseqmrnaaccession'
		u = urllib.urlopen(url)
                response = u.read()
                xh = XMLHandlerE()
                xml.sax.parseString(response,xh)
		data = xh.getresult()
		with open("id2id_result.txt","w") as f:
                        f.write("EnsemblTrancriptID\tRefSeq_mRNA_accession\n")
                        for n in range(len(data)-1):
                                if n%2 == 0:
                                        string = str(data[n+1]).split("//")
                                        for nn in string:
                                                f.write(str(data[n])+"\t"+nn+"\n")
                                else:
                                        pass
		logging.info("DONE please check output file 'id2id_result.txt'")

	else:
		pass

if __name__ == "__main__":
	main(sys.argv[1:])
