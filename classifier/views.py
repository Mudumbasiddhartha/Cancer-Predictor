from django.shortcuts import render


import csv
from io import StringIO
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt



def home(request):
    
    if request.method == "GET":
        return render(request, 'classifier/home.html', context={'title':"Classification","read ":-1})
   
    
    excel_file=request.FILES["train_file"]
    csv_file=request.FILES["test_file"]
    
    df=pd.ExcelFile(excel_file)
    
    plot_div,result= decision_tree(excel_file,csv_file)
    return render(request, 'classifier/home.html', context={'plot_div':plot_div, 'title':"Results",'read':result})

def handle_csv_data(csv_file):
    reader=csv.reader(csv_file)
    mydict = {rows[0]:rows[1] for rows in reader}
    return list(reader)

def decision_tree(filename,test):
    datas =pd.ExcelFile(filename)
    # read Affected sheet into df1
    df1 = datas.parse('Affected')
    file_data = test.read().decode("utf-8")
    test=pd.read_csv(StringIO(file_data))
    df1['affected']='yes'
    df1['affected'].astype('category')
    df2= datas.parse('not affected')
    df2['affected']='no'
    df2['affected'].astype('category')

    df=pd.concat([df1,df2],axis=0, ignore_index=True)
    train = df.sample(frac=1).reset_index(drop=True)
    #shuffle the dataframe
    #reading test data into a dataframe
    
    # drop File Name from test
    test = test.drop(['File Name'], axis=1)
    # drop Unnamed: 1 from test
    test.drop(['Unnamed: 1'],axis=1,inplace=True)
    test = test.dropna(axis=1)
  
    # drop WBC_convex_area from train
    train = train.drop(['WBC_convex_area'], axis=1)
    # change WBC_area to Area
    train = train.rename(columns={'WBC_area': 'Area'})
    # drop equivalent_diameter from test
    test = test.drop(['equivalent_diameter'], axis=1)
    # rename orient_wbc to orientation in train
    train = train.rename(columns={'orient_wbc': 'orientation'})
    # rename majoraxis in train to MajorAxisLength
    train = train.rename(columns={'majoraxis': 'MajorAxisLength'})
    # rename minoraxis in train to MinorAxisLength
    train = train.rename(columns={'minoraxis': 'MinorAxisLength'})
    # drop WBC_peri from train
    train = train.drop(['WBC_peri'], axis=1)
    # rename peri_nuc to Perimeter in train
    train = train.rename(columns={'peri_nuc': 'Perimeter'})
    # drop MinIntensity  MeanIntensity  MaxIntensity from test
    test = test.drop(['MinIntensity', 'MeanIntensity', 'MaxIntensity'], axis=1)
    # drop ecc_wbc	solidity_wbc	nuc_area	nuc_ratio	round_nuc	ecc_nuc	solidity_nuc	convex_area_nuc	avg_cyt_re	avg_cyt_gr	avg_cyt_bl	entropy_cyt	minoraxis_nuc	majoraxis_nuc	axismeanratio from train
    train = train.drop(['ecc_wbc', 'solidity_wbc', 'nuc_area', 'nuc_ratio', 'round_nuc', 'ecc_nuc', 'solidity_nuc', 'convex_area_nuc',
                    'avg_cyt_re', 'avg_cyt_gr', 'avg_cyt_bl', 'entropy_cyt', 'minoraxis_nuc', 'majoraxis_nuc', 'axismeanratio'], axis=1)

   
    # make the columns in train and test in same order
    train = train[['Area', 'orientation', 'MajorAxisLength',
                'MinorAxisLength', 'Perimeter', 'affected']]
    test = test[['Area', 'orientation', 'MajorAxisLength',
                'MinorAxisLength', 'Perimeter']]
  
    # Area orientation MajorAxisLength MinorAxisLength   Perimeter MILength+MALength convert to float32
    train['Area'] = train['Area'].astype('float32')
    train['orientation'] = train['orientation'].astype('float32')
    train['MajorAxisLength'] = train['MajorAxisLength'].astype('float32')
    train['MinorAxisLength'] = train['MinorAxisLength'].astype('float32')
    train['Perimeter'] = train['Perimeter'].astype('float32')
    # change affected to category type 
    train['affected'] = train['affected'].astype('category')



    from sklearn.tree import DecisionTreeClassifier
    from sklearn import tree

    # split the twt laraining data into 70% train and 30% test
    from sklearn.model_selection import train_test_split

    traintree, testtree = train_test_split(train, test_size=0.2,random_state=42)
    # encode yes to 1 and no to 0
    traintree['affected'] = traintree['affected'].map({'yes': 1, 'no': 0})
    testtree['affected'] = testtree['affected'].map({'yes': 1, 'no': 0})
    

    features = list(traintree.columns[:])
    features.remove('affected')
    x=traintree[features]
    
    y=traintree['affected']
    dtree = DecisionTreeClassifier()
    dtree = dtree.fit(x, y)
    

    # plot the roc curve
    from sklearn.metrics import roc_curve, auc
    # predict for testree
    y_pred = dtree.predict(testtree[features])
  
    fpr, tpr, thresholds = roc_curve(testtree['affected'], y_pred) 
    roc_auc = auc(fpr, tpr)
    fig=plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC curve')
    plt.legend(loc="lower right")

    # predict for test set
    lis = list(dtree.predict(test))

    yes =lis.count("yes")
    no = lis.count("no")
    # plt.show()
    result =0

    if(yes>no):
        result = 1
    else:
        result = 0
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data,result
