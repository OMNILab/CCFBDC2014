#--coding: utf8 --
input_file1 = "./classified_weibo.txt"
input_file2"./classified_news.txt"
input_file3 = "./holiday.txt"
def find_max_and_min(A, p, r):
    if r - p <= 1:
        if A[p] < A[r]:
            return [A[p], A[r]]
        else:
            return [A[r], A[p]]
    # 分解
    q = p + (r - p) / 2
    (lmin, lmax) = find_max_and_min(A, p, q)
    (rmin, rmax) = find_max_and_min(A, q + 1, r)
    # 合并
    return [min(lmin, rmin), max(lmax, rmax)]
 
if __name__ == "__main__":
	f = open(input_file1,'r')
	matrix = [[] for row in range(2401)] 
	for lines in f.read().split('\n'):
		if(lines.split('\t')[0]):
			matrix[int(lines.split('\t')[0])].append(int(lines.split('\t')[2]))
			matrix[int(lines.split('\t')[0])] = find_max_and_min(matrix[int(lines.split('\t')[0])],0,len(matrix[int(lines.split('\t')[0])])-1)
		else:
			pass;

	f2 = open(input_file2,'r')
	for lines in f2.read().split('\n'):
		if(lines.split('\t')[0]):
			# print lines.split('\t')[0]
			matrix[int(lines.split('\t')[0])].append(int(lines.split('\t')[2]))
			matrix[int(lines.split('\t')[0])] = find_max_and_min(matrix[int(lines.split('\t')[0])],0,len(matrix[int(lines.split('\t')[0])])-1)
		else:
			pass;


	fw = open('ttl_result.txt','w')
	for i in range(2400):
		fw.write(str(i))
		fw.write('\t')
		if len(matrix[i]) == 0:
			fw.write('null'+'\t'+'null'+'\t')
		else:
			for j in matrix[i]:
				fw.write(str(j)+'\t')
		fw.write(str(int(matrix[i][1])-int(matrix[i][0])+1))
		fw.write('\n')
# event_holiday  
if __name__ == "__main__":
	f2 = open('./ttl_result_news.txt','r')#news:ttl_result_news.txt /weibo:ttl_result_weibo.txt
	k = 0
	matrix = [[] for row in range(2400)] 
	for lines in f2.read().split('\n'):
		if lines.split('\t')[1] == "null":
			pass
		else:
			f = open(input_file3,'r')
			for lines_holiday in f.read().split('\n'):
				length = len(lines_holiday.split('\t'))
				for i in range(1,length):
					# print lines
					if int(lines.split('\t')[1]) <= int(lines_holiday.split('\t')[i])+3 and int(lines.split('\t')[1]) >= int(lines_holiday.split('\t')[i])-3:
						matrix[k].append(lines_holiday.split('\t')[0])					
		k = k+1

	fw = open('holiday_result.txt','w')
	for i in range(2400):
		fw.write(str(i))
		fw.write('\t')
		if len(matrix[i]) == 0:
			pass
		else:
			# for j in matrix[i]:
			# 	fw.write(j+',')
			fw.write(','.join(matrix[i]))
		fw.write('\n')
#holiday_mod
if __name__ == "__main__":
	f = open(input_file3,'r')
	fw = open('holiday_mod.txt','w')
	for lines in f.read().split('\n'):
		fw.write(lines.split('\t')[0]+'\t')
		k = len (lines.split('\t'))
		print k
		for i in range(1,k):
			fw.write(str(549+int(lines.split('\t')[i]))+'\t')
		fw.write('\n')
#event_week
if __name__ == "__main__":
	f = open('./ttl_result.txt','r')
	matrix = []
	i = 0
	for lines in f.read().split('\n'):
		matrix.append(int(lines.split('\t')[1]) % 7)
		# print int(lines.split('\t')[2]) % 7
	fw = open ('week_result.txt','w')
	j = 0
	for k in matrix:
		fw.write(str(j))
		fw.write('\t')
		if k == 1:
			fw.write('Monday')
		elif k == 2:
			fw.write('Tuesday')
		elif k == 3:
			fw.write('Wednesday')
		elif k == 4:
			fw.write('Thursday')
		elif k == 5:
			fw.write('Friday')
		elif k == 6:
			fw.write('Saturday')
		elif k == 0:
			fw.write('Sunday')
		fw.write('\n')	
		j = j+1