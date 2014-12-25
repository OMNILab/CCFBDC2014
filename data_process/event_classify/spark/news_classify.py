# -*- coding: utf-8 -*- 

import sys
import time
import math
from operator import add
from pyspark import SparkContext
from pyspark.mllib.util import MLUtils
from pyspark.mllib.tree import DecisionTree
from pyspark.mllib.regression import LabeledPoint

# 新闻分类

def extract(line):
	A1 = ["公交","车辆","巴士","交通","乘坐","车厢","车窗","驾驶员","司机","乘客"]
	A2 = ["爆炸","炸弹","起火","大火","燃烧","自燃"]
	B1 = ["暴力","恐怖","暴徒","袭击","击毙","自杀式"]
	C1 = ["校园","学校","高校","名校","校内","校外","小学","中学","初中","高中","大学","学生","同学","教师","老师","师生","幼儿园"]
	C2 = ["砍","刀","匕首","刺","捅","杀"]
	cid = line.strip().split("\t")[0][1:-1]
	day = (int(time.mktime(time.strptime(line.strip().split("\t")[1][1:-1],'%Y-%m-%d %H:%M:%S')))-int(time.mktime(time.strptime("2011-04-01 00:00:00",'%Y-%m-%d %H:%M:%S'))))/(24*3600)
	title = line.strip().split("\t")[4][1:-1].split(" ")
	content = line.strip().split("\t")[7][1:-1].split(" ")
	nr_map_t, ns_map_t = {}, {}
	for item in title:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])>=2:
			nr_map_t[item.split("/")[0]] = 1 if not nr_map_t.has_key(item.split("/")[0]) else nr_map_t[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])>=2:
			ns_map_t[item.split("/")[0]] = 1 if not ns_map_t.has_key(item.split("/")[0]) else ns_map_t[item.split("/")[0]]+1
	nr_map_c, ns_map_c = {}, {}
	for item in content:
		if len(item.split("/")) == 2 and item.split("/")[1] in ["nr","nr1","nr2","nrj","nrf"] and len(item.split("/")[0])>=2:
			nr_map_c[item.split("/")[0]] = 1 if not nr_map_c.has_key(item.split("/")[0]) else nr_map_c[item.split("/")[0]]+1
		if len(item.split("/")) == 2 and item.split("/")[1] in ["ns","nsf"] and len(item.split("/")[0])>=2:
			ns_map_c[item.split("/")[0]] = 1 if not ns_map_c.has_key(item.split("/")[0]) else ns_map_c[item.split("/")[0]]+1
	title_orig = "".join([item.split("/")[0] for item in title])
	s1 = sum([1 if w.decode('utf-8') in title_orig else 0 for w in A1])
	s2 = sum([1 if w.decode('utf-8') in title_orig else 0 for w in A2])
	s3 = sum([1 if w.decode('utf-8') in title_orig else 0 for w in B1])
	s4 = sum([1 if w.decode('utf-8') in title_orig else 0 for w in C1])
	s5 = sum([1 if w.decode('utf-8') in title_orig else 0 for w in C2])
	tag = 0
	if s1 >= 1 and s2 >= 1:
		tag = 1
	if s3 >= 1:
		tag = 2
	if s4 >= 1 and s5 >= 1:
		tag = 3
	if tag != 0:
		return (day, cid+"\t"+str(tag)+"\t"+str(day)+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_t.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in nr_map_c.iteritems()])+"\""+"\t"+"\""+" ".join([k+":"+str(v) for k,v in ns_map_c.iteritems()])+"\""+"\t"+title_orig)
	else:
		return (-1, "")

if __name__ == "__main__":
	sc = SparkContext('spark://namenode.omnilab.sjtu.edu.cn:7077',appName="Extract")
	lines = sc.textFile('hdfs://namenode.omnilab.sjtu.edu.cn/user/qiangsiwei/CCFtask/t_lable_group_comp_1.sort.seg.txt', 1)
	counts = lines.map(lambda x : extract(x)) \
			.filter(lambda x : x[0]!=-1) \
			.sortByKey() \
			.map(lambda x : x[1])
	output = counts.saveAsTextFile("./CCFtask/tag_pos_t_lable_group_comp_1")
