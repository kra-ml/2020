Usage
----

# 1. [Experiments]

## 1.1 [Pretest]

### 1.1.1. horse (url)

CMD) python model_v20.py -t url -m all


### 1.1.2. sports (url)

CMD) python model_v20.py -t url -m all



### 1.1.3. horse and sports (url)

CMD) python model_v20.py -t url -m all




## 1.2 [Test]

### 1.2.1. horse (url + index + whois) - ratio 1 vs 1

CMD) python model_v20.py -t all -m all



### 1.2.2. horse (label encoding + n gram) - ratio 1 vs 1

CMD) python model_v20.py -t label -m all

CMD) python model_v20.py -t ngram -m all

CMD) python model_v20.py -t label_ngram -m all

CMD) python model_v20.py -t full_label_ngram -m all







# 2. [Demo] Detection of Illegal Online Gambling Websites 

Run the web socket server(Already active) :

CMD) python server.py

<p>

<b>1. Download from github 'KRA_Extensions.zip'</b>

<p>

<b>2. Install Chrome extension and Run :</b>

- Unzip 'KRA_Extensions.zip'

- chrome://extensions ( Check the 'Developer mode' )

- Click the 'Load unpacked extension'

- Select the 'KRA_Extensions'(Unzipped folder) 

- Right click(Context Menu) the 'KRA_Extensions' and Select the 'Options'

- Run


ScreenShots
----
General site

![general](https://user-images.githubusercontent.com/55607802/71304118-8e5b3580-2405-11ea-9f2c-0f50427e9987.png)

<p>

Illegal site

![illegal](https://user-images.githubusercontent.com/55607802/71304091-feb58700-2404-11ea-9563-1ff6ceb13313.png)



# 3. [Misc]
## 3.1 [Feature collector]
## 3.2 [Word files]
