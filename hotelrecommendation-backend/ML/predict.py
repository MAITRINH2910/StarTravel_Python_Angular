from sklearn.svm import SVC
import pickle
import numpy as np
import config
# city = 'Da Nang'
# with open('data/list_of_pro_hotel_'+city+'.pickle', 'rb') as handle:
#     list_of_pro = pickle.load(handle)
# print(list_of_pro)

#0: rating
#1: price
def predict(city,pro_predict,k = 20):
    with open('models/'+city+'.pickle', 'rb') as handle:
        clf = pickle.load(handle)
    with open('data/list_of_pro_hotel_'+city+'.pickle', 'rb') as handle:
        list_of_pro = pickle.load(handle)
    
    X = [pro_predict[0],int(pro_predict[1]/config.UNIT_PRICE)]
    
    for i in range (5):
        X.append(X[1])

    for pro in list_of_pro:
        if pro in pro_predict:
            X.append(1)
        else:
            X.append(0)

    print(X)

    p = np.array(clf.decision_function([X]))

    ind = np.argpartition(p[0], -k)[-k:]

    y = []
    for i in ind:
        y.append((city+str(i)).replace(" ",""))
    return y

y = predict('Da Nang',[8.0,400000,'Poolside bar','Restaurants','Garden','Bar'])
print(y)