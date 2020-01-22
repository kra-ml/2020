import sys, argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold



if len(sys.argv) == 1:
    sys.exit()

parser = argparse.ArgumentParser()
parser.add_argument('-t', type=str, required=True, help='ex) [label_ngram | label | ngram]')
parser.add_argument('-m', type=str, required=True, help='algorithm')
args = parser.parse_args()



if args.t == 'label_ngram':
    s1 = pd.read_csv('label_ngram.csv')
elif args.t == 'label':
    s1 = pd.read_csv('only_label.csv')
elif args.t == 'ngram':
    s1 = pd.read_csv('only_ngram.csv')
elif args.t == 'full_label_ngram':
    s1 = pd.read_csv('full_label_ngram.csv')
elif args.t == 'full_label':
    s1 = pd.read_csv('full_label.csv')
elif args.t == 'full':
    s1 = pd.read_csv('full_url.csv')

x = s1.iloc[:, 1:-1].values
y = s1.iloc[:, -1].values

cv = StratifiedKFold(n_splits=5, random_state=123, shuffle=True)
acc,recall,prec,f1,TN,TP,FP,FN = 0,0,0,0,0,0,0,0
for (train, test), i in zip(cv.split(x, y), range(5)):
    if args.m == 'rf':
        model = RandomForestClassifier(n_estimators=300,
                                    bootstrap=True,
                                    max_features='sqrt', n_jobs=2, random_state=1)
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
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
            print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
            print('accuracy : \t', acc/5)
            print('recall : \t', recall/5)
            print('precision : \t', prec/5)
            print('f1 : \t\t', f1/5)
    elif args.m == 'dt':
        model = DecisionTreeClassifier(max_depth=10, random_state=1)
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
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
            print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
            print('accuracy : \t', acc/5)
            print('recall : \t', recall/5)
            print('precision : \t', prec/5)
            print('f1 : \t\t', f1/5)
    elif args.m == 'svm':
        sc = StandardScaler()
        sc.fit(x[train])
        x[train] = sc.transform(x[train])
        x[test] = sc.transform(x[test])
        model = SVC(kernel='linear', C=1.0, random_state=1)
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
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
            print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
            print('accuracy : \t', acc/5)
            print('recall : \t', recall/5)
            print('precision : \t', prec/5)
            print('f1 : \t\t', f1/5)
    elif args.m == 'nb':
        model = GaussianNB()
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
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
            print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
            print('accuracy : \t', acc/5)
            print('recall : \t', recall/5)
            print('precision : \t', prec/5)
            print('f1 : \t\t', f1/5)
    elif args.m == 'knn':
        model = KNeighborsClassifier(n_neighbors=1)
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
            print('target : \t', args.t, '\tmodel : \t', args.m)
            print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
            print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
            print('accuracy : \t', acc/5)
            print('recall : \t', recall/5)
            print('precision : \t', prec/5)
            print('f1 : \t\t', f1/5)
if args.m == 'all':

    for mm in ['rf', 'dt', 'svm', 'nb', 'knn']:
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
                xTrain = sc.transform(x[train])
                xTest = sc.transform(x[test])
            
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
                print('target : \t', args.t, '\tmodel : \t', mm)
                print('TN : \t%s\tTP : \t%s' % (TP/5, FN/5))
                print('FN : \t%s\tFP : \t%s' % (FP/5, TN/5))
                print('accuracy : \t', acc/5)
                print('recall : \t', recall/5)
                print('precision : \t', prec/5)
                print('f1 : \t\t', f1/5)


