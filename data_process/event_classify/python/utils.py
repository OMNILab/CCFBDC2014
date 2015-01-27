# -*- coding: utf-8 -*-
def cos(a, b):
	import math
	try:
		return sum([sa*sb if pa == pb else 0 for (pa,sa) in a for (pb,sb) in b])/math.sqrt(sum([sa**2 for (pa,sa) in a])*sum([sb**2 for (pb,sb) in b]))
	except:
		return 0