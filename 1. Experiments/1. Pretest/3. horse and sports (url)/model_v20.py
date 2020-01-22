import sys, argparse, csv
import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from itertools import combinations
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold


useage = """
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
ex) model.py -t [ url| index| whois| all| test] -m [ rf| dt| svm| nb| knn] -c 0,2,4 --test 1/10 
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
"""
if len(sys.argv) == 1:
    print(useage)
    sys.exit()


parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, required=True, help='ex) [url | indx | whois | all]')
parser.add_argument('-c', required=False, help='col', type=str)
parser.add_argument('--test', type=str, required=False, default='1/4', help='test case')
parser.add_argument('-f', type=str, required=False, help='test file (csv)')
parser.add_argument('-m', type=str, required=True, help='algorithm')
parser.add_argument('-p', type=str,  help='test parameter')
args = parser.parse_args()

column = []
dataset = pd.DataFrame()
tmp_col = []

if args.t == 'url':
    csv_kra, csv_normal = 'kra_url_feature.csv', 'normal_url_feature.csv'
    if args.c:  column = ['hangul', 'number_len', 'special_chr_0', 'special_chr_1', 'in_dic', 'total_len']
elif args.t == 'index':
    csv_kra, csv_normal = 'kra_index_feature.csv', 'normal_index_feature.csv'
    if args.c:  column = ['source_len', 'hangul_num', 'input', 'submit', 'rediraction_1', 'rediraction_0', 'js_func',
                          'js_filename']
elif args.t == 'whois':
    csv_kra, csv_normal = 'kra_whois_feature.csv', 'normal_whois_feature.csv'
    if args.c:  column = ['ip', 'web_age', 'name', 'email']
elif args.t == 'all':
    if args.c:  column = ['hangul', 'number_len', 'special_chr_0', 'special_chr_1', 'in_dic', 'total_len', 'source_len',
                          'hangul_num',
                          'input',
                          'submit', 'rediraction_1', 'rediraction_0', 'js_func',
                          'js_filename', 'ip', 'web_age', 'name', 'email']
elif args.t == 'test':
    column = ['hangul', 'number_len', 'special_chr_0', 'special_chr_1', 'in_dic', 'total_len', 'source_len',
              'hangul_num',
              'input',
              'submit', 'rediraction_1', 'rediraction_0', 'js_func',
              'js_filename', 'ip', 'web_age', 'name', 'email']

    s1 = pd.DataFrame(pd.read_csv('kra_url_feature.csv'))
    s2 = pd.DataFrame(pd.read_csv('kra_index_feature.csv'))
    s3 = pd.DataFrame(pd.read_csv('kra_whois_feature.csv'))
    kra_data = pd.concat([s1.hangul, s1.number_len, s1.special_chr_0, s1.special_chr_1, s1.in_dic,
                          s1.total_len, s2.source_len, s2.hangul_num, s2.input, s2.submit,
                          s2.rediraction_1, s2.rediraction_0, s2.js_func, s2.js_filename, s3.ip, s3.web_age,
                          s3.name, s3.email, s1.site], axis=1).reset_index(drop=True)
    kra_data = kra_data.dropna()

    s1 = pd.DataFrame(pd.read_csv('normal_url_feature.csv'))
    s2 = pd.DataFrame(pd.read_csv('normal_index_feature.csv'))
    s3 = pd.DataFrame(pd.read_csv('normal_whois_feature.csv'))
    normal_data = pd.concat([s1.hangul, s1.number_len, s1.special_chr_0, s1.special_chr_1, s1.in_dic,
                             s1.total_len, s2.source_len, s2.hangul_num, s2.input, s2.submit,
                             s2.rediraction_1, s2.rediraction_0, s2.js_func, s2.js_filename, s3.ip, s3.web_age,
                             s3.name, s3.email, s1.site], axis=1).reset_index(drop=True)
    normal_data = normal_data.dropna()
    dataset = pd.concat([kra_data, normal_data])

    for x in range(2, len(column)):
        comb = list(combinations(column, x))
        for b in comb:
            cc = ''
            asdf = pd.DataFrame()
            for i in b:
                cc += " " + i
                asdf = pd.concat([asdf, dataset[i]], axis=1)
            asdf = pd.concat([asdf, dataset['site']], axis=1)
            x = asdf.iloc[:, :-1].values
            y = asdf.iloc[:, -1].values


            if args.m =='all':
                for mm in ['rf', 'dt', 'svm','nb', 'knn']:
                    if mm == 'rf':
                        model = RandomForestClassifier(n_estimators=300,
                                                    bootstrap=True,
                                                    max_features='sqrt', n_jobs=2, random_state=1)
                    elif mm == 'dt':
                        model = DecisionTreeClassifier(max_depth=10, random_state=1)
                    elif mm == 'svm':
                        model = SVC(kernel='linear', C=1.0, random_state=1)
                    elif mm == 'nb':
                        model = GaussianNB()
                    elif mm == 'knn':
                        model = KNeighborsClassifier(n_neighbors=5)
                    
                    if args.f:
                        xTrain, yTrain = x, y
                        pdd = pd.DataFrame(pd.read_csv(args.f))
                        xTest = pdd.iloc[:, :-1].values
                        yTest = pdd.iloc[:, -1].values
                    else:
                        xTrain, xTest, yTrain, yTest = train_test_split(x, y,
                                test_size=int(args.test.split('/')[0]) / int(
                                    args.test.split('/')[1]),
                                random_state=1)

                    if mm == 'svm':
                        sc = StandardScaler()
                        sc.fit(xTrain)
                        xTrain = sc.transform(xTrain)
                        xTest = sc.transform(xTest)
                    model.fit(xTrain, yTrain)

                    model_predictions = model.predict(xTest)
                    acc = accuracy_score(yTest, model_predictions)
                    recall = recall_score(yTest, model_predictions)
                    precision_score(yTest, model_predictions)
                    f1 = precision_score(yTest, model_predictions)

                    CM = confusion_matrix(yTest, model_predictions)
                    TN = CM[0][0]
                    FN = CM[1][0]
                    TP = CM[1][1]
                    FP = CM[0][1]
                    with open('test_result.csv', 'a') as f:
                        wr = csv.writer(f)
                        wr.writerow([args.m, cc, acc, recall, prec, (acc + recall + prec), TN, TP, FN, FP])
                        print(mm, cc,recall , prec, acc, f1, TN, TP, FN, FP)

            
            elif args.m == 'rf':
                model = RandomForestClassifier(n_estimators=300,
                                            bootstrap=True,
                                            max_features='sqrt', n_jobs=2, random_state=1)
            elif args.m == 'dt':
                model = DecisionTreeClassifier(max_depth=10, random_state=1)
            elif args.m == 'svm':
                model = SVC(kernel='linear', C=1.0, random_state=1)

            elif args.m == 'nb':
                model = GaussianNB()
            elif args.m == 'knn':
                model = KNeighborsClassifier(n_neighbors=5)    

            if args.f:
                xTrain, yTrain = x, y
                pdd = pd.DataFrame(pd.read_csv(args.f))
                xTest = pdd.iloc[:, :-1].values
                yTest = pdd.iloc[:, -1].values
                xTrain, yTrain = x, y
                pdd = pd.DataFrame(pd.read_csv(args.f))
                full = pd.DataFrame()
                cc2=''
                for i in b:
                    cc2 += " " + i
                    full = pd.concat([full, pdd[i]], axis=1)
                full = pd.concat([full, pdd['site']], axis=1)
                xTest = full.iloc[:, :-1].values
                yTest = full.iloc[:, -1].values
            else:
                xTrain, xTest, yTrain, yTest = train_test_split(x, y,
                        test_size=int(args.test.split('/')[0]) / int(
                            args.test.split('/')[1]),
                        random_state=1)

            if args.m == 'svm':
                sc = StandardScaler()
                sc.fit(xTrain)
                xTrain = sc.transform(xTrain)
                xTest = sc.transform(xTest)
            model.fit(xTrain, yTrain)

            model_predictions = model.predict(xTest)
            acc = accuracy_score(yTest, model_predictions)
            recall = recall_score(yTest, model_predictions)
            precision_score(yTest, model_predictions)
            f1 = precision_score(yTest, model_predictions)

            CM = confusion_matrix(yTest, model_predictions)
            TN = CM[0][0]
            FN = CM[1][0]
            TP = CM[1][1]
            FP = CM[0][1]
            with open('test_result.csv', 'a') as f:
                wr = csv.writer(f)
                wr.writerow([args.m, cc, acc, recall, prec, (acc + recall + prec), TN, TP, FN, FP])
                print(args.m, cc,recall , prec, acc, f1, TN, TP, FN, FP)
    sys.exit()

else:
    print(useage)
    sys.exit()

if args.t == 'all':
    s1 = pd.DataFrame(pd.read_csv('kra_url_feature.csv'))
    s2 = pd.DataFrame(pd.read_csv('kra_index_feature.csv'))
    s3 = pd.DataFrame(pd.read_csv('kra_whois_feature.csv'))
    kra_data = pd.concat([s1.hangul, s1.number_len, s1.special_chr_0, s1.special_chr_1, s1.in_dic,
                          s1.total_len, s2.source_len, s2.hangul_num, s2.input, s2.submit,
                          s2.rediraction_1, s2.rediraction_0, s2.js_func, s2.js_filename, s3.ip, s3.web_age,
                          s3.name, s3.email, s1.site], axis=1).reset_index(drop=True)
    kra_data = kra_data.dropna()

    s1 = pd.DataFrame(pd.read_csv('normal_url_feature.csv'))
    s2 = pd.DataFrame(pd.read_csv('normal_index_feature.csv'))
    s3 = pd.DataFrame(pd.read_csv('normal_whois_feature.csv'))
    normal_data = pd.concat([s1.hangul, s1.number_len, s1.special_chr_0, s1.special_chr_1, s1.in_dic,
                             s1.total_len, s2.source_len, s2.hangul_num, s2.input, s2.submit,
                             s2.rediraction_1, s2.rediraction_0, s2.js_func, s2.js_filename, s3.ip, s3.web_age,
                             s3.name, s3.email, s1.site], axis=1).reset_index(drop=True)
    normal_data = normal_data.dropna()
    dataset = pd.concat([kra_data, normal_data])
else:
    s1 = pd.DataFrame(pd.read_csv(csv_kra))
    s2 = pd.DataFrame(pd.read_csv(csv_normal))

if not args.c and args.t == 'all':
    x = dataset.iloc[:, :-1].values
    y = dataset.iloc[:, -1].values
elif args.c and args.t == 'all':
    for a in args.c.split(','):
        tmp_col.append(a)
    new_dataset = pd.DataFrame()
    for b in tmp_col:
        new_dataset = pd.concat([new_dataset, dataset[column[int(b)]]], axis=1)
    new_dataset = pd.concat([new_dataset, dataset['site']], axis=1)

    x = new_dataset.iloc[:, :-1].values
    y = new_dataset.iloc[:, -1].values
elif args.c:
    for a in args.c.split(','):
        tmp_col.append(a)
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    for b in tmp_col:
        df1 = pd.concat([df1, s1[column[int(b)]]], axis=1)
        df2 = pd.concat([df2, s2[column[int(b)]]], axis=1)
    dataset = pd.concat([df1, df2])

    if len(tmp_col) == 1:
        x = dataset.iloc[:, :].values
    else:
        x = dataset.iloc[:, :-1].values
    y = pd.concat([s1, s2]).iloc[:, -1].values
elif args.t=='url' or args.t=='index' or args.t=='whois':
    x = pd.concat([s1, s2]).iloc[:, 1:-1].values
    y = pd.concat([s1, s2]).iloc[:, -1].values
else:
    x = pd.concat([s1, s2]).iloc[:, :-1].values
    y = pd.concat([s1, s2]).iloc[:, -1].values


if args.m == 'rf':
    model = RandomForestClassifier(n_estimators=300,
                                   bootstrap=True,
                                   max_features='sqrt', n_jobs=2, random_state=1)
elif args.m == 'dt':
    model = DecisionTreeClassifier(max_depth=10, random_state=1)
elif args.m == 'svm':
    model = SVC(kernel='linear', C=1.0, random_state=1)
elif args.m == 'nb':
    model = GaussianNB()
elif args.m == 'knn':
    model = KNeighborsClassifier(n_neighbors=1)
elif args.m == 'all':
    for mm in ['rf', 'dt', 'svm','nb' ,'knn']:
        cv = StratifiedKFold(n_splits=5, random_state=123, shuffle=True)
        acc,recall,prec,f1,TN,TP,FP,FN = 0,0,0,0,0,0,0,0
        for (train, test), i in zip(cv.split(x, y), range(5)):
            if mm == 'rf':
                model = RandomForestClassifier(n_estimators=300,
                                                bootstrap=True,
                                                max_features='sqrt', n_jobs=2, random_state=1)
            elif mm == 'dt':
                model = DecisionTreeClassifier(max_depth=10, random_state=1)
            elif mm == 'svm':
                model = SVC(kernel='linear', C=1.0, random_state=1)
            elif mm == 'nb':
                model = GaussianNB()
            elif mm == 'knn':
                model = KNeighborsClassifier(n_neighbors=5)
            if mm == 'svm':
                sc = StandardScaler()
                sc.fit(x[train])
                x[train] = sc.transform(x[train])
                x[test] = sc.transform(x[test])
            model.fit(x[train], y[train])
            model_predictions = model.predict(x[test])
            acc += accuracy_score(y[test], model_predictions)
            recall += recall_score(y[test], model_predictions)
            prec += precision_score(y[test], model_predictions)
            f1 += f1_score(y[test], model_predictions)
            CM = confusion_matrix(y[test], model_predictions)
            TN += CM[0][0]
            FN += CM[1][0]
            TP += CM[1][1]
            FP += CM[0][1]
            if i==4:
                print('target : \t', args.t, '\tmodel : \t', mm)
                print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
                print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
                print('accuracy : \t', acc/5)
                print('recall : \t', recall/5)
                print('precision : \t', prec/5)
                print('f1 : \t\t', f1/5)
                print('')
    sys.exit()
elif args.m == 'rf_test':
    if args.c and args.f:
        new_dataset = pd.DataFrame()
        for b in tmp_col:
            new_dataset = pd.concat([new_dataset, dataset[column[int(b)]]], axis=1)
        new_dataset = pd.concat([new_dataset, dataset['site']], axis=1)
        x = new_dataset.iloc[:, :-1].values
        y = new_dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        new_tmp = pd.DataFrame()
        for b in tmp_col:
            new_tmp = pd.concat([new_tmp, pd.DataFrame(pd.read_csv(args.f))[column[int(b)]]], axis=1)
        xTest = new_tmp.iloc[:, :].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr = 0
    elif not args.c and args.f:
        x=dataset.iloc[:, :-1].values
        y=dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        xTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, :-1].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr=0
    elif not args.c and not args.f:
        xTrain, xTest, yTrain, yTest = train_test_split(x, y,test_size=int(args.test.split('/')[0]) / int(args.test.split('/')[1]),random_state=1)
        tmpscr=0
    if args.p:
        pp = args.p.split(',')
        x=int(pp[0])
        y=int(pp[1])
    else:
        x,y=1,5000

    for x in range(x, y, 1):
        print('n_estimators =', x)
        model = RandomForestClassifier(n_estimators=x,
                                       bootstrap=True,
                                       max_features='sqrt', n_jobs=2, random_state=1)
        model.fit(xTrain, yTrain)

        model_predictions = model.predict(xTest)
        acc = accuracy_score(yTest, model_predictions)
        recall = recall_score(yTest, model_predictions)
        precision_score(yTest, model_predictions)
        f1 = precision_score(yTest, model_predictions)
        CM = confusion_matrix(yTest, model_predictions)
        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]

        if tmp_col:
            tmpstr = ''
            for a in tmp_col:
                tmpstr += column[int(a)] + ', '
            print('column : \t', tmpstr)
        if tmpscr < f1:
            tmpscr = f1
            print('TN : \t%s\tTP : \t%s' % (TN, TP))
            print('FN : \t%s\tFP : \t%s' % (FN, FP))
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('accuracy : \t', acc)
            print('recall : \t', recall)
            print('precision : \t', prec)
            print('f1 : \t\t', f1)
    sys.exit()
elif args.m == 'dt_test':
    if args.c and args.f:
        new_dataset = pd.DataFrame()
        for b in tmp_col:
            new_dataset = pd.concat([new_dataset, dataset[column[int(b)]]], axis=1)
        new_dataset = pd.concat([new_dataset, dataset['site']], axis=1)
        x = new_dataset.iloc[:, :-1].values
        y = new_dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        new_tmp = pd.DataFrame()
        for b in tmp_col:
            new_tmp = pd.concat([new_tmp, pd.DataFrame(pd.read_csv(args.f))[column[int(b)]]], axis=1)
        xTest = new_tmp.iloc[:, :].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr = 0
    elif not args.c and args.f:

        x=dataset.iloc[:, :-1].values
        y=dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        xTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, :-1].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr=0
    elif not args.c and not args.f:
        xTrain, xTest, yTrain, yTest = train_test_split(x, y,test_size=int(args.test.split('/')[0]) / int(args.test.split('/')[1]),random_state=1)
        tmpscr=0
    if args.p:
        pp = args.p.split(',')
        x=int(pp[0])
        y=int(pp[1])
    else:
        x,y=1,5000
    for x in range(x, y, 1):
        print('max_depth =', x)
        model = DecisionTreeClassifier(max_depth=x, random_state=1)
        model.fit(xTrain, yTrain)

        model_predictions = model.predict(xTest)
        acc = accuracy_score(yTest, model_predictions)
        recall = recall_score(yTest, model_predictions)
        prec = precision_score(yTest, model_predictions)
        f1 = f1_score(yTest, model_predictions)
        CM = confusion_matrix(yTest, model_predictions)
        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]
        if tmp_col:
            tmpstr = ''
            for a in tmp_col:
                tmpstr += column[int(a)] + ', '
            print('column : \t', tmpstr)
        if tmpscr < f1:
            tmpscr = f1
            print('TN : \t%s\tTP : \t%s' % (TN, TP))
            print('FN : \t%s\tFP : \t%s' % (FN, FP))
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('accuracy : \t', acc)
            print('recall : \t', recall)
            print('precision : \t', prec)
            print('f1 : \t\t', f1)
    sys.exit()
elif args.m == 'knn_test':
    if args.c and args.f:
        new_dataset = pd.DataFrame()
        for b in tmp_col:
            new_dataset = pd.concat([new_dataset, dataset[column[int(b)]]], axis=1)
        new_dataset = pd.concat([new_dataset, dataset['site']], axis=1)
        x = new_dataset.iloc[:, :-1].values
        y = new_dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        new_tmp = pd.DataFrame()
        for b in tmp_col:
            new_tmp = pd.concat([new_tmp, pd.DataFrame(pd.read_csv(args.f))[column[int(b)]]], axis=1)
        xTest = new_tmp.iloc[:, :].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr = 0
    elif not args.c and args.f:
        x=dataset.iloc[:, :-1].values
        y=dataset.iloc[:, -1].values
        xTrain, yTrain = x, y
        xTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, :-1].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
        tmpscr=0
    elif not args.c and not args.f:
        xTrain, xTest, yTrain, yTest = train_test_split(x, y,test_size=int(args.test.split('/')[0]) / int(args.test.split('/')[1]),random_state=1)
        tmpscr=0
    if args.p:
        pp = args.p.split(',')
        x=int(pp[0])
        y=int(pp[1])
    else:
        x,y=1,5000
    for x in range(x, y, 1):
        print('n_neighbors =', x)
        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(xTrain, yTrain)
        model_predictions = model.predict(xTest)
        acc = accuracy_score(yTest, model_predictions)
        recall = recall_score(yTest, model_predictions)
        precision_score(yTest, model_predictions)
        f1 = precision_score(yTest, model_predictions)
        CM = confusion_matrix(yTest, model_predictions)
        TN = CM[0][0]
        FN = CM[1][0]
        TP = CM[1][1]
        FP = CM[0][1]
        if tmp_col:
            tmpstr = ''
            for a in tmp_col:
                tmpstr += column[int(a)] + ', '
            print('column : \t', tmpstr)
        if tmpscr < f1:
            tmpscr = f1
            print('TN : \t%s\tTP : \t%s' % (TN, TP))
            print('FN : \t%s\tFP : \t%s' % (FN, FP))
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('accuracy : \t', acc)
            print('recall : \t', recall)
            print('precision : \t', prec)
            print('f1 : \t\t', f1)
    sys.exit()


if args.f:
    xTrain, yTrain = x, y
    if args.c:
        new_tmp = pd.DataFrame()
        for b in tmp_col:
            new_tmp = pd.concat([new_tmp, pd.DataFrame(pd.read_csv(args.f))[column[int(b)]]], axis=1)
        xTest = new_tmp.iloc[:, :].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values
    else:
        xTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, 1:-1].values
        yTest = pd.DataFrame(pd.read_csv(args.f)).iloc[:, -1].values


cv = StratifiedKFold(n_splits=5, random_state=123, shuffle=True)
acc,recall,prec,f1,TN,TP,FP,FN = 0,0,0,0,0,0,0,0
for (train, test), i in zip(cv.split(x, y), range(5)):
    if args.m =='svm':
        sc = StandardScaler()
        sc.fit(x[train])
        x[train] = sc.transform(x[train])
        x[test] = sc.transform(x[test])

    model.fit(x[train], y[train])
    model_predictions = model.predict(x[test])
    acc += accuracy_score(y[test], model_predictions)
    recall += recall_score(y[test], model_predictions)
    prec += precision_score(y[test], model_predictions)
    f1 += f1_score(y[test], model_predictions)
    CM = confusion_matrix(y[test], model_predictions)
    TN += CM[0][0]
    FN += CM[1][0]
    TP += CM[1][1]
    FP += CM[0][1]
    if i == 4:
        print('target : \t', args.t, '\tmodel : \t', args.m)
        print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
        print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
        print('accuracy : \t', acc/5)
        print('recall : \t', recall/5)
        print('precision : \t', prec/5)
        print('f1 : \t\t', f1/5)
    a, b = x[test].shape
    vv = np.hstack([x[test], model_predictions.reshape(a, 1)])

np.savetxt('model_' + args.t + '.csv', vv, delimiter=',', fmt='%d')
