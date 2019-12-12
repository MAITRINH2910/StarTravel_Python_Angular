import pandas as pd 
from sklearn.svm import SVC
import numpy as np
import pickle
# import sys
# city = sys.argv[1]
# print(city)

UNIT=300000

citys = ['Da Lat','Da Nang','Nha Trang','Ho Chi Minh','Ha Noi']
for city in citys:
    data = pd.read_csv('../src/data/train/'+city+'.csv')#.as_matrix()

    y_train = data['id']

    X_train = data.drop(columns=['id','city','name','img','address','link'])

    X_train['price'] = X_train['price']/UNIT
    X_train.insert(1,'price1',X_train['price'])
    X_train.insert(1,'price2',X_train['price'])
    X_train.insert(1,'price3',X_train['price'])
    X_train.insert(1,'price4',X_train['price'])
    X_train.insert(1,'price5',X_train['price'])
    # X_train.insert(0,'rating1',X_train['rating'])
    # X_train.insert(0,'rating2',X_train['rating'])
    # X_train.insert(0,'rating3',X_train['rating'])
    # print(X_train[:4])
    # for k in data.keys()[5:]:
    #     print(k)


    clf = SVC(kernel = 'linear', **kwargs)
    clf.fit(X_train,y_train)
    with open('../src/models/'+city+'.pickle', 'wb') as handle:
        pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

# X = [[2,2,2,2,2,2,1,0,0,1,1,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0]]
# p = np.array(clf.decision_function(X))
# print(np.argmax(p))

# # p = clf.predict_proba(X)
# # print(np.max(p[0]))
# # print(p[0][65])
# # y = clf.predict(X)
# # print('y',y)
# k = 10
# ind = np.argpartition(p[0], -k)[-k:]
# # # print(ind)
# print(y_train[ind])
