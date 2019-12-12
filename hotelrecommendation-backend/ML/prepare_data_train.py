import pickle
import os 
import pandas as pd

citys = ['Ho Chi Minh',
        'Da Nang',
        'Ha Noi',
        'Nha Trang',
        'Da Lat']

# import sys
# city = sys.argv[1]
# print(city)
for city in citys:
    print(city)
    with open('../src/data/raw_data_hotel_'+city+'.pickle', 'rb') as handle:
        data_hotel = pickle.load(handle)
    with open('../src/data/list_of_pro_hotel_'+city+'.pickle', 'rb') as handle:
        list_of_pro = pickle.load(handle)

    print(len(data_hotel))

    data = []
    list_address = []

    for hotel in data_hotel:
        if data_hotel[hotel]['address'] in list_address:
            print(data_hotel[hotel]['address'])
            continue
        list_address.append(data_hotel[hotel]['address'])
        
        tmp = [hotel,city,data_hotel[hotel]['name'],data_hotel[hotel]['link'],data_hotel[hotel]['img'],data_hotel[hotel]['address'],data_hotel[hotel]['rating'],data_hotel[hotel]['price']]
        for pro in list_of_pro:
            if pro in data_hotel[hotel]['properties']:
                tmp.append(1)
            else:
                tmp.append(0)
        data.append(tmp)

    properties = ['id','city','name','link','img','address','rating','price']
    for p in list_of_pro:
        properties.append(p)

    df = pd.DataFrame(data)
    df.to_csv('../src/data/train/'+city+'.csv',encoding='utf-8-sig',index = False,header = properties)
