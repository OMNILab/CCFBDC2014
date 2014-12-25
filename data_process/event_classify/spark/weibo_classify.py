# -*- coding: utf-8 -*- 

import sys
import time
import math
import fileinput
from operator import add
from pyspark import SparkContext
from pyspark.mllib.util import MLUtils
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint

# 微博分类

def preprocess():
	from gensim import corpora, models, similarities
	A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
	A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
	B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
	C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
	C2 = ["砍","刀","匕首","刺","捅","杀"]
	event_map = {}
	for line in fileinput.input("classified_news.txt"):
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
	file1 = open("tag_pos_t_lable_group_comp_4.seg.txt","w")
	for line in fileinput.input("t_lable_group_comp_4.sort.seg.txt"):
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
	fileinput.close()
	file1.close()
	texts = [[word for word in document.lower().split()] for document in documents]
	dictionary = corpora.Dictionary(texts)
	print len(dictionary.token2id)
	corpus = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]
	file_event = open("corpus_tfidf_event.txt","w")
	file_weibo = open("corpus_tfidf_weibo.txt","w")
	c = 0
	for doc in corpus_tfidf:
		if c < len(event_map.keys()):
			file_event.write(str(event_map[c]["cls"])+"\t"+str(event_map[c]["stime"])+"\t"+"\t".join([str(item[0])+" "+str(item[1]) for item in doc])+"\n")
		else:
			file_weibo.write(str(weibo[c-len(event_map.keys())]["cls"])+"\t"+str(weibo[c-len(event_map.keys())]["day"])+"\t"+weibo[c-len(event_map.keys())]["cid"]+"\t"+weibo[c-len(event_map.keys())]["content"]+"\t"+"\t".join([str(item[0])+" "+str(item[1]) for item in doc])+"\n")
		c += 1
	file_event.close()
	file_weibo.close()

def cos(a, b):
	try:
		return sum([sa*sb if pa == pb else 0 for (pa,sa) in a for (pb,sb) in b])/math.sqrt(sum([sa**2 for (pa,sa) in a])*sum([sb**2 for (pb,sb) in b]))
	except:
		return 0

def extract(line):
	part = line.strip().split("\t")
	cls, day, cid, content, doc = part[0], int(part[1]), part[2], part[3], [(int(item.split(" ")[0]), float(item.split(" ")[1])) for item in part[4:]]
	maxsim, assign = 0, -1
	for k, v in event_map.iteritems():
		if cls == v["cls"] and 0 <= day - v["stime"] <= 28:
			sim = cos(doc, v["feature"])
			if sim > maxsim:
				maxsim, assign = sim, k
	if maxsim >= 0.15:
		return (assign, str(assign)+"\t"+cls+"\t"+str(day)+"\t"+cid+"\t"+content)
	else:
		return (-1, "")

global event_map

if __name__ == "__main__":
	# preprocess()
	event_map = {}
	c = 0
	for line in fileinput.input("corpus_tfidf_event.txt"):
		part = line.strip().split("\t")
		event_map[c] = {"cls":part[0], "stime":int(part[1]), "feature":[(int(item.split(" ")[0]), float(item.split(" ")[1])) for item in part[2:]]}
		c += 1
	fileinput.close()
	sc = SparkContext('spark://namenode.omnilab.sjtu.edu.cn:7077',appName="Extract")
	lines = sc.textFile('hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/CCFtask/corpus_tfidf_weibo.txt', 1)
	counts = lines.map(lambda x : extract(x)) \
			.filter(lambda x : x[0]!=-1) \
			.sortByKey() \
			.map(lambda x : x[1])
	output = counts.saveAsTextFile("./CCFtask/classified_weibo")
