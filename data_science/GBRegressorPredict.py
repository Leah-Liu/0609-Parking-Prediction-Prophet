'''Gradient Boosting Regressor'''
from sklearn.ensemble import GradientBoostingRegressor

import unicodecsv
from datetime import datetime as dt
import datetime
with open('train_new.csv','rb') as f:
	reader = unicodecsv.DictReader(f)
	rawTrain = list(reader)

X = []
y = []
for row in rawTrain:
	'''
	curDate = dt.strptime(row['time'], '%Y-%m-%d %H:%M:%S')
	temp = [curDate.year, curDate.month, curDate.day, curDate.hour]
	'''
	temp = [ int(row['year']), int(row['month']), int(row['day']), int(row['hour']), bool(row['weekend']) ]
	X.append(temp)
	occupancy = int(row['occupancy'])
	y.append(occupancy)


clf = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, \
		max_depth=1, random_state=0, loss='ls').fit(X, y)

'''new input: from -> to'''
start = dt(2015,11,1,0,0,0)
end = dt(2016,1,31,23,0,0)
X = []
while start<=end:
	temp = [start.year, start.month, start.day, start.hour, start.weekday()>=5]
	start = start + datetime.timedelta(hours=1)
	X.append(temp)


'''
predict part
'''
ans = clf.predict(X)

predictAns =[]
for i in range(len(X)):
	#curDate = dt.strptime(rawTest[i]['time'],'%Y-%m-%d %H:%M:%S')
	temp = {'time':dt(X[i][0],X[i][1],X[i][2],X[i][3],0,0), 'occupancy':int(ans[i])}
	predictAns.append(temp)
#print predictAns

''' output predict as csv file '''
keys = predictAns[0].keys()
with open('predict_GB.csv','wb') as f:
	writer = unicodecsv.DictWriter(f,keys)
	writer.writeheader()
	writer.writerows(predictAns)
