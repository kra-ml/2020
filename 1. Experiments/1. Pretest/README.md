# [Using only URL group features]

## 1. Only illegal horse racing

[General]
URL     14633

[Illegal]
URL     3517

Command) python model_v20.py -t url -m [rf | svm | knn | nb| dt | all]



## 2. Only illegal sports toto

[General]
URL     14633

[Illegal]
URL     4818

Command) python model_v20.py -t url -m [rf | svm | knn | nb| dt | all]



## 3. Mix of illegal horse racing and sports toto

[General]
URL     14633

[Illegal]
URL     8335

Command) python model_v20.py -t url -m [rf | svm | knn | nb| dt | all]




# [Using all features]

## 1. Only horse racing (URL, INDEX, WHOIS group) 
ratio 5(general):1(illegal)

[General]
URL     14633
INDEX   14633
WHOIS   14633

[Illegal]
URL     2843
INDEX   2843
WHOIS   2843

Command) python model_v20.py -t [url | index | whois | all] -m [rf | svm | knn | nb| dt | all]



## 2. Only horse racing (URL, INDEX, WHOIS group) 
ratio 1(general):1(illegal

[General]
URL     12000
INDEX   3000
WHOIS   3000

[Illegal]
URL     2843
INDEX   2843
WHOIS   2843

Command) python model_v20 -t [url | index | whois | all] -m [rf | svm | knn | nb| dt | all]

