# -*- coding: utf-8 -*-
import fileinput
import time
import fileinput
#from gensim import corpora, models, similarities

def cos(a, b):
	import math
	try:
		return sum([sa*sb if pa == pb else 0 for (pa,sa) in a for (pb,sb) in b])/math.sqrt(sum([sa**2 for (pa,sa) in a])*sum([sb**2 for (pb,sb) in b]))
	except:
		return 0
input_file = "./t_lable_group_comp_1.sort.seg.txt"
output_file1 = "./tag_pos_t_lable_group_comp_1.seg.txt"
output_file2 = "./tag_neg_t_lable_group_comp_1.seg.txt"
A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
C2 = ["砍","刀","匕首","刺","捅","杀"]
file1 = open(output_file1,"w")
file2 = open(output_file2,"w")
for line in fileinput.input(input_file):
	cid = line.strip().split("\t")[0][1:-1]
	day = (int(time.mktime(time.strptime(line.strip().split("\t")[1][1:-1],'%Y-%m-%d %H:%M:%S')))-int(time.mktime(time.strptime("2011-04-01 00:00:00",'%Y-%m-%d %H:%M:%S'))))/(24*3600)
	title = line.strip().split("\t")[4][1:-1].split(" ")
	content = line.strip().split("\t")[7][1:-1].split(" ")
	nr_map_t, ns_map_t = {}, {}
	for item in title:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])/3>=2:
			nr_map_t[item.split("/")[0]] = 1 if not nr_map_t.has_key(item.split("/")[0]) else nr_map_t[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])/3>=2:
			ns_map_t[item.split("/")[0]] = 1 if not ns_map_t.has_key(item.split("/")[0]) else ns_map_t[item.split("/")[0]]+1
	nr_map_c, ns_map_c = {}, {}
	for item in content:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])/3>=2:
			nr_map_c[item.split("/")[0]] = 1 if not nr_map_c.has_key(item.split("/")[0]) else nr_map_c[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])/3>=2:
			ns_map_c[item.split("/")[0]] = 1 if not ns_map_c.has_key(item.split("/")[0]) else ns_map_c[item.split("/")[0]]+1
	title_orig = "".join([item.split("/")[0] for item in title])
	s1 = sum([1 if w in title_orig else 0 for w in A1])
	s2 = sum([1 if w in title_orig else 0 for w in A2])
	s3 = sum([1 if w in title_orig else 0 for w in B1])
	s4 = sum([1 if w in title_orig else 0 for w in C1])
	s5 = sum([1 if w in title_orig else 0 for w in C2])
	tag = 0
	if s1 >= 1 and s2 >= 1:
		tag = 1
	if s3 >= 1:
		tag = 2
	if s4 >= 1 and s5 >= 1:
		tag = 3
	if tag != 0:
		# print tag, title_orig
		# print " ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in nr_map_c.iteritems()])
		# print " ".join([k+":"+str(v) for k,v in ns_map_c.iteritems()])
		file1.write(cid+"\t"+str(tag)+"\t"+str(day)+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_c.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_c.iteritems()])+"\""+"\t"+title_orig+"\n")
	else:
		file2.write(line)
fileinput.close()
file1.close()
file2.close()
