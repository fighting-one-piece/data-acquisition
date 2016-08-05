#-*- coding:utf-8 -*-

'''
@author: wulin
'''

from sklearn import linear_model
X = [[0,0], [1,1], [2,2]]
y = [0, 1, 2]
lr = linear_model.LogisticRegression()
lr.fit(X, y)
print lr.coef_
print lr.intercept_
print lr.predict([[3,3]])
print lr.decision_function(X)
print lr.score(X, y)
print lr.get_params()
print lr.set_params(fit_intercept = False)


