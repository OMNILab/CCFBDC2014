# -*- coding: utf-8 -*-
import fileinput
import time
from utils import cos

from gensim import corpora, models

input_file1 = "classified_news.txt"
input_file2 = "t_lable_group_comp_4.sort.seg.txt"
output_file1 = "tag_pos_t_lable_group_comp_4.seg.txt"
output_file2 = "tag_neg_t_lable_group_comp_4.seg.txt"
output_file3 = "classified_weibo.txt"

# 微博分类
import time
import fileinput
A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
C2 = ["砍","刀","匕首","刺","捅","杀"]
event_map = {}
for line in fileinput.input(input_file1):
	part = line.strip().split("\t")
	event, cls, day = int(part[0]), int(part[1]), int(part[2])
	nr_t = None if len(part[5].split("|")[0][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[0][1:-1].split(" ")]
	ns_t = None if len(part[5].split("|")[1][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[1][1:-1].split(" ")]
	nr_c = None if len(part[5].split("|")[2][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[2][1:-1].split(" ")]
	ns_c = None if len(part[5].split("|")[3][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5].split("|")[3][1:-1].split(" ")]
	text, weight = [], 5
	if nr_t != None:
		for w in nr_t:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if ns_t != None:
		for w in ns_t:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if nr_c != None:
		for w in nr_c:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if ns_c != None:
		for w in ns_c:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if not event_map.has_key(event):
		event_map[event] = {"cls":cls,"stime":day,"text":text}
	else:
		event_map[event]["text"].extend(text)
fileinput.close()

documents = []
for k, v in event_map.iteritems():
	documents.append(" ".join(v["text"]).encode("utf-8"))

weibo = []
file1 = open(output_file1,"w")
file2 = open(output_file2,"w")

for line in fileinput.input(input_file2):
	cid = line.strip().split("\t")[0][1:-1]
	day = (int(time.mktime(time.strptime(line.strip().split("\t")[1][1:-1],'%Y-%m-%d %H:%M:%S')))-int(time.mktime(time.strptime("2011-04-01 00:00:00",'%Y-%m-%d %H:%M:%S'))))/(24*3600)
	content = line.strip().split("\t")[5][1:-1].split(" ")
	nr_map_t, ns_map_t = {}, {}
	for item in content:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"]:
			nr_map_t[item.split("/")[0]] = 1 if not nr_map_t.has_key(item.split("/")[0]) else nr_map_t[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"]:
			ns_map_t[item.split("/")[0]] = 1 if not ns_map_t.has_key(item.split("/")[0]) else ns_map_t[item.split("/")[0]]+1
	text = []
	for k,v in nr_map_t.iteritems():
		try:
			text.extend([k.decode("utf-8")]*v)
		except:
			continue
	for k,v in ns_map_t.iteritems():
		try:
			text.extend([k.decode("utf-8")]*v)
		except:
			continue
	content_orig = "".join([item.split("/")[0] for item in content])
	s1 = sum([1 if w in content_orig else 0 for w in A1])
	s2 = sum([1 if w in content_orig else 0 for w in A2])
	s3 = sum([1 if w in content_orig else 0 for w in B1])
	s4 = sum([1 if w in content_orig else 0 for w in C1])
	s5 = sum([1 if w in content_orig else 0 for w in C2])
	cls = 0
	if s1 >= 1 and s2 >= 1:
		cls = 1
	if s3 >= 1:
		cls = 2
	if s4 >= 1 and s5 >= 1:
		cls = 3
	if cls != 0:
		documents.append(" ".join(text).encode("utf-8"))
		weibo.append({"cid":cid,"cls":cls,"day":day,"content":content_orig})
		file1.write(cid+"\t"+str(cls)+"\t"+str(day)+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])+"\""+"\t"+content_orig+"\n")
	else:
		file2.write(line)
fileinput.close()
file1.close()
file2.close()

# Do classifying
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
print len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
file = open(output_file3,"w")
c = 0
for doc in corpus_tfidf:
	print c
	if c < len(event_map.keys()):
		event_map[c]["feature"] = doc
	else:
		maxsim, assign = 0, -1
		for k, v in event_map.iteritems():
			if weibo[c-len(event_map.keys())]["cls"] == v["cls"] and 0 <= weibo[c-len(event_map.keys())]["day"] - v["stime"] <= 28:
				sim = cos(v["feature"],doc)
				if sim > maxsim:
					maxsim, assign = sim, k
		if maxsim >= 0.15:
			file.write(str(assign)+"\t"+str(weibo[c-len(event_map.keys())]["cls"])+"\t"+str(weibo[c-len(event_map.keys())]["day"])+"\t"+weibo[c-len(event_map.keys())]["cid"]+"\t"+weibo[c-len(event_map.keys())]["content"]+"\n")
	c += 1
file.close()
