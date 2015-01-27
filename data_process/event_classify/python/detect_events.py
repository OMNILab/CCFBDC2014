# -*- coding: utf-8 -*-
import fileinput
import time

from gensim import corpora, models
import utils

input_file = "tag_pos_t_lable_group_comp_1.seg.txt"
output_file = "classified_news.txt"

# 事件划分
documents, news = [], []
c = 0
for line in fileinput.input(input_file):
	part = line.strip().split("\t")
	cid, cls, day = part[0], int(part[1]), int(part[2])
	title_nf = None if len(part[3][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[3][1:-1].split(" ")]
	title_ns = None if len(part[4][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[4][1:-1].split(" ")]
	content_nf = None if len(part[5][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[5][1:-1].split(" ")]
	content_ns = None if len(part[6][1:-1]) == 0 else [(item.split(":")[0], int(item.split(":")[-1])) for item in part[6][1:-1].split(" ")]
	title = part[-1]
	news.append([cls, day, cid+"\t"+title+"\t"+part[3]+"|"+part[4]+"|"+part[5]+"|"+part[6]])
	text, weight = [], 5
	if title_nf != None:
		for w in title_nf:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if title_ns != None:
		for w in title_ns:
			try:
				text.extend([w[0].decode("utf-8")]*w[1]*weight)
			except:
				continue
	if content_nf != None:
		for w in content_nf:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	if content_ns != None:
		for w in content_ns:
			try:
				text.extend([w[0].decode("utf-8")]*min(w[1],3))
			except:
				continue
	documents.append(" ".join(text).encode("utf-8"))
	c += 1
fileinput.close()

texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
print len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
event = {1:[],2:[],3:[]}
c = 0

for doc in corpus_tfidf:
	print c
	feature = doc
	maxsim, assign = 0, -1
	for e in xrange(len(event[news[c][0]])):
		if abs(event[news[c][0]][e]["stime"] - news[c][1]) <= 14:
			sim = utils.cos(event[news[c][0]][e]["feature"],feature)
			# print "---- ---- ----"
			# print event[news[c][0]][e]["title"][0], news[c][2], sim
			# print event[news[c][0]][e]["feature"], feature
			# print "---- ---- ----"
			if sim > maxsim:
				maxsim, assign = sim, e
	# print maxsim
	if maxsim >= 0.15:
		event[news[c][0]][assign]["title"].append(news[c][2])
		fmap = {}
		for (p,s) in event[news[c][0]][assign]["feature"]:
			fmap[p] = s
		for (p,s) in feature:
			fmap[p] = s if not fmap.has_key(p) else fmap[p]+s
		event[news[c][0]][assign]["feature"] = [(p,s) for p,s in fmap.iteritems()]
	else:
		event[news[c][0]].append({"stime":news[c][1],"feature":feature,"title":[news[c][2]]})
	c += 1

file = open(output_file,"w")
c = 0
for i in [1,2,3]:
	for e in event[i]:
		for t in e["title"]:
			file.write(str(c)+"\t"+str(i)+"\t"+str(e["stime"])+"\t"+t+"\n")
		c += 1
file.close()

documents = ["Shipment of gold damaged in a fire","Delivery of silver arrived in a silver truck","Shipment of gold arrived in a truck"]
texts = [[word for word in document.lower().split()] for document in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
	print doc
