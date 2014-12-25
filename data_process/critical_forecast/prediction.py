# encoding: utf-8

import csv
import fileinput

area = {0:"东北区",1:"西北区",2:"西南区",3:"华北区",4:"华东区",5:"华南区",6:"华中区",7:"港澳台"}
province = {0:"上海",1:"云南",2:"内蒙",3:"北京",4:"台湾",5:"吉林",6:"四川",7:"天津",8:"宁夏",9:"安徽",10:"山东",11:"山西",12:"广东",13:"广西",14:"新疆",15:"江苏",16:"江西",17:"河北",18:"河南",19:"浙江",20:"海南",21:"湖北",22:"湖南",23:"甘肃",24:"福建",25:"贵州",26:"辽宁",27:"重庆",28:"陕西",29:"青海",30:"香港",31:"黑龙江"}
input_file1 = "event_attributes-results_my.txt"
input_file2 = "holiday.txt"
max_offset, xlen = 1125, 28
pv_event, pv_index = {"全国":[]}, {"全国":[[] for i in xrange(max_offset/xlen+1)]}
for line in fileinput.input(input_file1):
	row = line.strip().split("\t")
	event_id, event_tag, day_offset, happen_province, happen_area = int(row[0]), int(row[1]), int(row[2]), row[15].replace("省","").replace("市","").replace("自治区","").replace("古",""), [1 if area[x]==row[14] else 0 for x in range(8)]
	start_offset, end_offset = int(row[2]), max(int(row[4]),int(row[5]))
	duration, duration_25, duration_50, duration_75 = max(int(row[6]),int(row[7])), max(int(row[8]),int(row[11])), max(int(row[9]),int(row[12])), max(int(row[10]),int(row[13]))
	holiday = 0
	news_cnt_num, media_total = int(row[23]) if row[23]!="NULL" else 0, int(row[35]) if row[35]!="NULL" else 0
	wb_cnt_num, wb_person_num, wb_loc_num = int(row[24]) if row[24]!="NULL" else 0, int(row[36]) if row[36]!="NULL" else 0, int(row[37]) if row[37]!="NULL" else 0
	province_gdp_ranking_2013, province_gdp_2013, avg_province_gdp_ranking_2013, avg_province_gdp_2013 = int(row[17]) if row[17]!="NULL" else 0, float(row[18].replace(",","")) if row[18]!="NULL" else 0, int(row[19]) if row[19]!="NULL" else 0, float(row[20]) if row[20]!="NULL" else 0
	province_pnum_2013, province_hanzu_ratio = float(row[21]) if row[21]!="NULL" else 0, 100-float(row[22]) if row[22]!="NULL" else 0
	comments_news, comments_weibo, quotes_news, quotes_weibo, attitudes_news, attitudes_weibo = int(row[25]) if row[25]!="NULL" else 0, int(row[26]) if row[26]!="NULL" else 0, int(row[27]) if row[27]!="NULL" else 0, int(row[28]) if row[28]!="NULL" else 0, int(row[29]) if row[29]!="NULL" else 0, int(row[30]) if row[30]!="NULL" else 0
	words_med_news, words_med_weibo, words_mean_news, words_mean_weibo = int(row[31]) if row[31]!="NULL" else 0, int(row[33]) if row[33]!="NULL" else 0, int(row[32]) if row[32]!="NULL" else 0, int(row[34]) if row[34]!="NULL" else 0
	pos_eval_news, pos_emo_news, pos_ntusd_news, neg_eval_news, neg_emo_news, neg_ntusd_news = int(row[38]), int(row[39]), int(row[40]), int(row[41]), int(row[42]), int(row[43])
	pos_eval_weibo, pos_emo_weibo, pos_ntusd_weibo, neg_eval_weibo, neg_emo_weibo, neg_ntusd_weibo = int(row[44]), int(row[45]), int(row[46]), int(row[47]), int(row[48]), int(row[49])
	if event_tag == 3 and happen_province != "NULL":
		if not pv_event.has_key(happen_province):
			pv_index[happen_province] = [[] for i in xrange(max_offset/xlen+1)]
			pv_event[happen_province] = []
		event_info = {}
		event_info.update({"event_id":event_id, "event_tag":event_tag, "day_offset":day_offset, "happen_province":happen_province, "happen_area":happen_area})
		event_info.update({"start_offset":start_offset, "end_offset":end_offset})
		event_info.update({"duration":duration, "duration_25":duration_25, "duration_50":duration_50, "duration_75":duration_75})
		event_info.update({"holiday":holiday})
		event_info.update({"news_cnt_num":news_cnt_num, "media_total":media_total})
		event_info.update({"wb_cnt_num":wb_cnt_num, "wb_person_num":wb_person_num, "wb_loc_num":wb_loc_num})
		event_info.update({"province_gdp_ranking_2013":province_gdp_ranking_2013, "province_gdp_2013":province_gdp_2013, "avg_province_gdp_ranking_2013":avg_province_gdp_ranking_2013, "avg_province_gdp_2013":avg_province_gdp_2013})
		event_info.update({"province_pnum_2013":province_pnum_2013, "province_hanzu_ratio":province_hanzu_ratio})
		event_info.update({"comments_news":comments_news, "comments_weibo":comments_weibo, "quotes_news":quotes_news, "quotes_weibo":quotes_weibo, "attitudes_news":attitudes_news, "attitudes_weibo":attitudes_weibo})
		event_info.update({"words_med_news":words_med_news, "words_med_weibo":words_med_weibo, "words_mean_news":words_mean_news, "words_mean_weibo":words_mean_weibo})
		event_info.update({"pos_eval_news":pos_eval_news, "pos_emo_news":pos_emo_news, "pos_ntusd_news":pos_ntusd_news, "neg_eval_news":neg_eval_news, "neg_emo_news":neg_emo_news, "neg_ntusd_news":neg_ntusd_news})
		# event_info.update({"pos_eval_weibo":pos_eval_weibo, "pos_emo_weibo":pos_emo_weibo, "pos_ntusd_weibo":pos_ntusd_weibo, "neg_eval_weibo":neg_eval_weibo, "neg_emo_weibo":neg_emo_weibo, "neg_ntusd_weibo":neg_ntusd_weibo})
		pv_index[happen_province][start_offset/xlen].append(len(pv_event[happen_province]))
		pv_event[happen_province].append(event_info)
		pv_index["全国"][start_offset/xlen].append(len(pv_event["全国"]))
		pv_event["全国"].append(event_info)

for k,v in pv_index.iteritems():
	print k,len(pv_event[k]),v
print len(pv_event["全国"])

holiday = [0 for i in xrange(max_offset/xlen+1)]
for line in fileinput.input(input_file2):
	for d in [int(i)/xlen for i in line.strip().split("\t")[1:]]:
		if 0 <= d <= max_offset/xlen:
			holiday[d] += 1
fileinput.close()

tp_feature, sp_feature, md_feature, st_feature, cnt = {}, {}, {}, {}, {}
for k,v in pv_index.iteritems():
	if k != "全国":
		tp_feature[k], sp_feature[k], md_feature[k], st_feature[k], cnt[k] = [], [], [], [], []
		for i in range(1,len(v)):
			cnt[k].append(len(v[i]))
			'''
			上期时间特征
			'''
			# 前N(N=1)个事件的时距
			last = reduce(lambda x,y:x+y,v[0:i])
			last = last[0] if len(last)!=0 else -1
			since_last_province = i*xlen - (pv_event[k][last]["start_offset"] if last>=0 else 0)
			last = reduce(lambda x,y:x+y,pv_index["全国"][0:i])
			last = last[0] if len(last)!=0 else -1
			since_last_china = i*xlen - (pv_event["全国"][last]["start_offset"] if last>=0 else 0)
			# 上期事件发生数
			happen_last_province = len(v[i-1])
			happen_last_china = len(pv_index["全国"][i-1])
			# 历史平均发生数
			happen_avg_province = float(sum([len(x) for x in v[0:i]]))/i
			feature_temporal = [since_last_province,since_last_china,happen_last_province,happen_last_china,happen_avg_province]
			tp_feature[k].append(feature_temporal)
			'''
			上期空间特征
			'''
			feature_spatial = []
			slice_feature_sum = [0]*40
			for e in pv_index["全国"][i-1]:
				happen_province_vec, happen_area_vec = [1 if province[m]==pv_event["全国"][e]["happen_province"] else 0 for m in xrange(32)], pv_event["全国"][e]["happen_area"]
				china_feature = []
				china_feature.extend(happen_province_vec)
				china_feature.extend(happen_area_vec)
				slice_feature_sum = [x+y for x,y in zip(slice_feature_sum,china_feature)]
			slice_feature_avg = [round(float(x)/len(v[i-1]),2) if len(v[i-1])!=0 else 0 for x in slice_feature_sum]
			feature_spatial.extend(slice_feature_sum)
			feature_spatial.extend(slice_feature_avg)
			sp_feature[k].append(feature_spatial)
			'''
			上期媒体特征
			'''
			feature_media = []
			# 本省
			slice_feature_sum = [0]*25
			for e in v[i-1]:
				event_feature = [pv_event[k][e][key] for key in ["duration","duration_25","duration_50","duration_75",\
																"news_cnt_num","media_total",\
																"wb_cnt_num","wb_person_num","wb_loc_num",\
																"comments_news","comments_weibo","quotes_news","quotes_weibo","attitudes_news","attitudes_weibo",\
																"words_med_news","words_med_weibo","words_mean_news","words_mean_weibo",\
																"pos_eval_news","pos_emo_news","pos_ntusd_news","neg_eval_news","neg_emo_news","neg_ntusd_news",\
																# "pos_eval_weibo","pos_emo_weibo","pos_ntusd_weibo","neg_eval_weibo","neg_emo_weibo","neg_ntusd_weibo"\
																]]
				# print len(event_feature)
				slice_feature_sum = [x+y for x,y in zip(slice_feature_sum,event_feature)]
			slice_feature_avg = [round(float(x)/len(v[i-1]),2) if len(v[i-1])!=0 else 0 for x in slice_feature_sum]
			feature_media.extend(slice_feature_sum)
			feature_media.extend(slice_feature_avg)
			# 全国
			slice_feature_sum = [0]*25
			for e in pv_index["全国"][i-1]:
				event_feature = [pv_event["全国"][e][key] for key in ["duration","duration_25","duration_50","duration_75",\
																	"news_cnt_num","media_total",\
																	"wb_cnt_num","wb_person_num","wb_loc_num",\
																	"comments_news","comments_weibo","quotes_news","quotes_weibo","attitudes_news","attitudes_weibo",\
																	"words_med_news","words_med_weibo","words_mean_news","words_mean_weibo",\
																	"pos_eval_news","pos_emo_news","pos_ntusd_news","neg_eval_news","neg_emo_news","neg_ntusd_news",\
																	# "pos_eval_weibo","pos_emo_weibo","pos_ntusd_weibo","neg_eval_weibo","neg_emo_weibo","neg_ntusd_weibo"\
																	]]
				# print len(event_feature)
				slice_feature_sum = [x+y for x,y in zip(slice_feature_sum,event_feature)]
			slice_feature_avg = [round(float(x)/len(v[i-1]),2) if len(v[i-1])!=0 else 0 for x in slice_feature_sum]
			feature_media.extend(slice_feature_sum)
			feature_media.extend(slice_feature_avg)
			md_feature[k].append(feature_media)
			'''
			本期时空特征
			'''
			feature_spatial_temporal = []
			tfeature = [holiday[i]]
			sfeature = [pv_event[k][0][key] for key in ["province_gdp_ranking_2013","province_gdp_2013","avg_province_gdp_ranking_2013","avg_province_gdp_2013",\
														"province_pnum_2013","province_hanzu_ratio"]]
			feature_spatial_temporal.extend(tfeature)
			feature_spatial_temporal.extend(sfeature)
			st_feature[k].append(feature_spatial_temporal)

# file = open("data/feature_extracted_my.txt","w")
# for k,v in pv_index.iteritems():
# 	if k!="全国":
# 		for i in xrange(max_offset/xlen):
# 			file.write(k+"\t"+str(i)+"\t"+str(cnt[k][i])+"\t"+"\t".join([str(round(x,3)) for x in tp_feature[k][i]])+"\t"+"\t".join([str(round(x,3)) for x in sp_feature[k][i]])+"\t"+"\t".join([str(round(x,3)) for x in md_feature[k][i]])+"\t"+"\t".join([str(round(x,3)) for x in st_feature[k][i]])+"\n")
# file.close()

import numpy as np
from sklearn import svm
from sklearn import tree
from sklearn import feature_selection
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import LeaveOneOut
from sklearn.cross_validation import KFold
from sklearn import pipeline
from sklearn import ensemble
from sklearn import linear_model
from sklearn import preprocessing

# 0.61760 0.93635
# 0.56271 0.82666
# 0.53125 0.77180
# 0.53125 0.77116

#### routine 1 ####

rec1, rec2 = [], []
for t in xrange(100):
	X, y1, y2 = [], [], []
	for k,v in pv_index.iteritems():
		if k!="全国":
			for i in xrange(max_offset/xlen-4):
				feature = []
				feature.extend(tp_feature[k][i])
				feature.extend(sp_feature[k][i])
				feature.extend(md_feature[k][i])
				feature.extend(st_feature[k][i])
				X.append(feature)
				y1.append(0 if cnt[k][i] == 0 else 1)
				y2.append(cnt[k][i])
	# clf1 = pipeline.Pipeline([
	# 	('feature_selection', linear_model.LogisticRegression(penalty='l1')),
	# 	# ('feature_selection', LinearSVC(penalty="l1",dual=False)),
	# 	# ('classification', tree.DecisionTreeClassifier())
	# 	# ('classification', ExtraTreesClassifier())
	# 	# ('classification', RandomForestClassifier())
	# 	('classification', GradientBoostingClassifier())
	# 	])
	clf1 = GradientBoostingClassifier()
	clf2 = tree.DecisionTreeRegressor()
	clf1 = clf1.fit(X, y1)
	clf2 = clf2.fit(X, y2)
	total, right, mse = 0, 0, []
	for k,v in pv_index.iteritems():
		if k!="全国":
			for i in range(max_offset/xlen-4, max_offset/xlen-1):
				feature = []
				feature.extend(tp_feature[k][i])
				feature.extend(sp_feature[k][i])
				feature.extend(md_feature[k][i])
				feature.extend(st_feature[k][i])
				hp = 0 if cnt[k][i] == 0 else 1
				if clf1.predict(feature)[0] == hp:
					right += 1
				mse.append(abs(clf2.predict(feature)[0]-cnt[k][i]))
				total += 1
	print t, float(right)/total, float(sum(mse))/len(mse)
	rec1.append(float(right)/total)
	rec2.append(float(sum(mse))/len(mse))
print sum(rec1)/len(rec1), sum(rec2)/len(rec2)

#### routine 2 ####

# X, y1, y2 = [], [], []
# for k,v in pv_index.iteritems():
# 	if k!="全国":
# 		for i in xrange(max_offset/xlen):
# 			feature = []
# 			feature.extend(tp_feature[k][i])
# 			feature.extend(sp_feature[k][i])
# 			feature.extend(md_feature[k][i])
# 			feature.extend(st_feature[k][i])
# 			X.append(feature)
# 			y1.append(0 if cnt[k][i] == 0 else 1)
# 			y2.append(cnt[k][i])
# total, right, mse = 0, 0, []
# X, y1, y2 = np.array(X), np.array(y1), np.array(y2)

# loo = LeaveOneOut(len(X))
# for train, test in loo:
# 	clf1 = pipeline.Pipeline([
# 		('feature_selection', linear_model.LogisticRegression(penalty='l1')),
# 		# ('feature_selection', LinearSVC(penalty="l1",dual=False)),
# 		('classification', tree.DecisionTreeClassifier())
# 		# ('classification', ExtraTreesClassifier())
# 		# ('classification', RandomForestClassifier())
# 		# ('classification', GradientBoostingClassifier())
# 		])
# 	# clf1 = GradientBoostingClassifier()
# 	clf2 = tree.DecisionTreeRegressor()
# 	clf1 = clf1.fit(X[train], y1[train])
# 	clf2 = clf2.fit(X[train], y2[train])
# 	r1 = clf1.predict(X[test])[0]
# 	r2 = clf2.predict(X[test])[0]
# 	if r1 == y1[test]:
# 		right += 1
# 	mse.append(abs(r2-y2[test]))
# 	total += 1
# 	print r1,y1[test],r2,y2[test]
# print float(right)/total, sum(mse)/len(mse)

# for t in xrange(10):
# 	kf = KFold(32*40, n_folds=10)
# 	c = 0
# 	for train, test in kf:
# 		c += 1
# 		print t, c
# 		clf1 = pipeline.Pipeline([
# 			('feature_selection', linear_model.LogisticRegression(penalty='l1')),
# 			# ('feature_selection', LinearSVC(penalty="l1",dual=False)),
# 			# ('classification', tree.DecisionTreeClassifier())
# 			# ('classification', ExtraTreesClassifier())
# 			# ('classification', RandomForestClassifier())
# 			('classification', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0))
# 			])
# 		# clf1 = GradientBoostingClassifier()
# 		clf2 = tree.DecisionTreeRegressor()
# 		clf1 = clf1.fit(X[train], y1[train])
# 		clf2 = clf2.fit(X[train], y2[train])
# 		for one in test:
# 			r1 = clf1.predict(X[one])[0]
# 			r2 = clf2.predict(X[one])[0]
# 			if r1 == y1[one]:
# 				right += 1
# 			mse.append(abs(r2-y2[one]))
# 			total += 1
# 			# print r1,y1[one],r2,y2[one]
# 	print float(right)/total, sum(mse)/len(mse)

#### routine 3 ####

# rec1, rec2 = [], []
# for t in range(0,31):
# 	X, y1, y2 = [], [], []
# 	for k,v in pv_index.iteritems():
# 		if k!="全国":
# 			for i in range(t, t+6):
# 				feature = []
# 				feature.extend(tp_feature[k][i])
# 				feature.extend(sp_feature[k][i])
# 				feature.extend(md_feature[k][i])
# 				feature.extend(st_feature[k][i])
# 				# print "feature:", len(tp_feature[k][i]), len(sp_feature[k][i]), len(md_feature[k][i]), len(st_feature[k][i])
# 				X.append(feature)
# 				y1.append(0 if cnt[k][i] == 0 else 1)
# 				y2.append(cnt[k][i])
# 	clf1 = pipeline.Pipeline([
# 		('feature_selection', linear_model.LogisticRegression(penalty='l1')),
# 		# ('feature_selection', LinearSVC(penalty="l1",dual=False)),
# 		# ('classification', tree.DecisionTreeClassifier())
# 		# ('classification', ExtraTreesClassifier())
# 		# ('classification', RandomForestClassifier())
# 		('classification', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0))
# 		])
# 	# clf1 = GradientBoostingClassifier()
# 	clf2 = tree.DecisionTreeRegressor()
# 	clf1 = clf1.fit(X, y1)
# 	clf2 = clf2.fit(X, y2)
# 	total, right, mse = 0, 0, []
# 	for k,v in pv_index.iteritems():
# 		if k!="全国":
# 			for i in range(t+6, t+9):
# 				feature = []
# 				feature.extend(tp_feature[k][i])
# 				feature.extend(sp_feature[k][i])
# 				feature.extend(md_feature[k][i])
# 				feature.extend(st_feature[k][i])
# 				hp = 0 if cnt[k][i] == 0 else 1
# 				if clf1.predict(feature)[0] == hp:
# 					right += 1
# 				mse.append(abs(clf2.predict(feature)[0]-cnt[k][i]))
# 				total += 1
# 	print t, float(right)/total, float(sum(mse))/len(mse)
# 	rec1.append(float(right)/total)
# 	rec2.append(float(sum(mse))/len(mse))
# print sum(rec1)/len(rec1), sum(rec2)/len(rec2)
