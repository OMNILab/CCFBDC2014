# -*- coding: utf-8 -*-  
import feature_spatial as mf_el

resource_dir="./"
file_read_from = resource_dir + "event_loc.txt"
file_write_to = resource_dir + "event_loc_result.txt"

province_city_map = resource_dir + "province_city_map.txt"
area_province_map = resource_dir + "area_province_map.txt"
resource_files = province_city_map + '\t' + area_province_map

mf_el.read_write_file(file_read_from,file_write_to,resource_files)