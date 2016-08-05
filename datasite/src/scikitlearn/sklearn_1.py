#-*- coding:utf-8 -*-

'''
@author: wulin
'''

#加载libSVM格式数据
from sklearn.datasets import load_svmlight_file
t_x, t_y = load_svmlight_file('filename')

#线性逻辑回归
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(C = 10, Penalty = '12', tol = 0.0001)
train_x = None 
train_y = None
train_s = lr.fit(train_x, train_y).score(train_x, train_y)
test_x = None
test_y = None
test_s = lr.score(test_x, test_y)

#交叉验证
from sklearn import cross_validation
c_train_x, c_test_x, c_train_y, c_test_y = cross_validation.train_test_split(
            t_x, t_y, test_size = 0.5, random_state = 'seed_i')
lr.fit(c_train_x, c_train_y)
lr.score(c_test_x, c_test_y, sample_weight = None)

#GridSearch
from sklearn.grid_search import GridSearchCV
tuned_parameters =[{'penalty': ['l1'], 'tol': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                    {'penalty': ['l2'], 'tol':[1e-3, 1e-4], 'C': [1, 10, 100, 1000]}]
clf =GridSearchCV(LogisticRegression(), tuned_parameters, cv=5, scoring=['precision','recall'])
print(clf.best_estimator_)

#matplotlib绘制学习曲线
from sklearn.learning_curve import learning_curve, validation_curve
# rain_sizes, train_scores, test_scores = learning_curve(
#         estimator, X, y, cv=cv, n_jobs=n_jobs,train_sizes=train_sizes)
# train_scores, test_scores =validation_curve(
#         estimator, X, y, param_name,param_range,
#         cv, scoring, n_jobs)







