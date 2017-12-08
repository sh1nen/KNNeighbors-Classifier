# KNNeighbors-Classifier

It's a really simple classifier which abstracts from using libraries used for faster artificial intelligence development 
available in Python such as sklearn, scipy etc. It only uses those libraries for better results representation such as confusion matrix.  

## Installing
There is no need to install anything except python 3.2 and above along with tools such pip for package managment.
There are three libs required which need to be install before running script on your local machine, just type in your console:
```
pip install <name_of_the_lib>
```
for following libs:
* numpy
* scipy
* sklearn

## Running the script
Running script is also not really a rocket science, just type:
```
py kNeighbours.py <file-name> <normalize>
```
where params passed to script are :
* file-name - name of the file from which data will be read, there are 2 data files initially
* normalize - pass 1 if you want to normalize your input data to [0-1] (highly recommended for wines set when going for better classification %) or 0 when if you want to keep it unnormalized.

for example:
```
py kNeighbours.py wine.data 1
```

it will run classifier against wine.data dataset and before performing cross-validation and predictioning it will normalize data to [0-1] values to avoid overfitting.

## Built With
* python 3.7
