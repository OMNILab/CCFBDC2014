# -*- coding: utf-8 -*-  
import sys
import os
import math

#读写文件接口函数文件函数
def read_write_file(rfname,wfname,resource_files):
	readf = open(rfname,'r')
	writef = open(wfname,'w')
	for line in readf:
		#add other functions to deal with each line
		result_line = location_extr(line.strip(),resource_files)
		writef.write(result_line + '\n')
	writef.close()
	readf.close()

#由值查主键，输入一个单词，如果查到返回主键名称，没有返回0
def value_to_key(value,resourcef_name):
	readf = open(resourcef_name)
	result = 0
	for line in readf:
		line_split = line.split('\t')
		key = line_split[0]
		values = line_split[1]
		if values.find(value)==-1:
			continue
		else:
			result = key
			break
	readf.close()
	return result


#地点提取函数，先在标题里面找，如果没有再在内容里面找，从频次高的到频次低的找，找到即标注地点，输出“地区、省、市”这样格式的信息
def location_extr(record,resource_files):
	record_split = record.split('\t')
	event_id = record_split[0]
	title_loc = record_split[1].strip('"')
	content_loc = record_split[2].strip('"')
	basic_info = event_id + '\t'
	
	line_rslt = event_id + '' + '' + ''
	province = ''
	area = ''

	title_loc_dealed = content_loc_match(title_loc,resource_files)
	if title_loc_dealed!=0:
		return basic_info + title_loc_dealed
	content_loc_dealed = content_loc_match(content_loc,resource_files)
	if content_loc_dealed!=0:
		return basic_info + content_loc_dealed

	return line_rslt

#内容与地点库匹配函数
def content_loc_match(content_loc,resource_files):
	resource_files_split = resource_files.split('\t')
	prov_city_map = resource_files_split[0]
	area_prov_map = resource_files_split[1]

	if content_loc!='':
		content_loc_split = content_loc.split(' ')
		#map the cities
		for num in range(len(content_loc_split)):
			content_city_name = content_loc_split[num].split(':')[0]
			province = value_to_key(content_city_name,prov_city_map)
			if(province!=0):
				area = value_to_key(province,area_prov_map)
				if content_city_name.find("市")==-1:
					content_city_name = content_city_name + "市"
				line_rslt = area + '\t' + province + '\t' + content_city_name
				return line_rslt
		#if there arenn't cities, map provinces
		for num in range(len(content_loc_split)):
			content_province_name = content_loc_split[num].split(':')[0]
			area = value_to_key(content_province_name,area_prov_map)
			if(area!=0):
				line_rslt = area + '\t' + content_province_name
				return line_rslt
	return 0
