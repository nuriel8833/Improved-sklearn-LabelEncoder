# Improved sklearn LabelEncoder() 

## Introduction

This project was created after encountering a problem with scikit-learns LabelEncoder(). Their LabelEncoder() has a few problems and limits.

For example, trying to encode never before seen items in test set after fitting the train set:

```
from sklearn.preprocessing import LabelEncoder()

train = pd.Series(['a','c','d','e'])
test = pd.Series(['a','c','b','d','e','f'])

le = LabelEncoder()
le.fit(train)
le.transform(test)
```
```ValueError: y contains previously unseen labels: 'b'```

Doing the opposite, while may not cause an error if all labels in train appear in test , will result in data leakage:
```
from sklearn.preprocessing import LabelEncoder()

train = pd.Series(['a','c','d','e'])
test = pd.Series(['a','c','b','d','e','f'])

le = LabelEncoder()
le.fit(test)
le.transform(train)
```

And fitting and transforming both test and train independently will just cause wrong labeling:
```
from sklearn.preprocessing import LabelEncoder()

train = pd.Series(['a','c','d','e'])
test = pd.Series(['a','c','b','d','e','f'])

le = LabelEncoder()
train = le.fit_transform(train)
print(train)
```
```[0 1 2 3]```

```
test = le.fit_transform(test)
print(test)
```
```[0 2 1 3 4 5]```


Notice that scikit-learn's LabelEncoder() reorganizing the items alphabetically , therefore the encoding was completely wrong for the test set (c received the label 2 in test set while receiving the label 1 in train set). 

In this project, the problems above and more were corrected.


## Functions
--------------------------------------------------------------------------------------------------------------
### Attributes

#### .dict
The encodingdictionary of the encoder:
```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(test)
new_le.dict
```
```
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6}
```
#### .labels
The labels encoded by the encoder (or the labels in the encoding dict if some were added manually):
```
new_le.labels
```
```
['a', 'c', 'b', 'd', 'e', 'f']
```

### mapping(series, encodeddictionary = None , ignorenan = False)
Mapping the labels of a series and creating encoding dictionary.

* **series:**   Pandas Series , the series which should be mapped

* **encodeddictionary:**  Dictionary , default *None* - Insering premade encodes dictionary, if given the mapping will be done in addition to it. If none, creates encoding dictionary from scratch.

* **ignorenan:** bool , default *False* - Ignoring NaNs while encoding or not. If False , NaNs are always encoded as 0 (if not set otherwise with set_nan())

* **returns:**   Dictionary

```
train = pd.Series(['a','c','d','e'])
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(train)
```
```{'a': 1, 'c': 2, 'd': 3, 'e': 4}```

If we would like to use the dictionary of encodes of the train in the test mapping:
```
train = pd.Series(['a','c','d','e'])
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
train_dict = new_le.mapping(train)
new_le.mapping(test , train_dict)
```
```{'a': 1, 'c': 2, 'd': 3, 'e': 4, 'b': 5, 'f': 6}```

Notice how the labels that did not appear in train were just added to the end of the dict without reorganizing it alphabetically.


### encode(series, encodeddictionary)
Encoding series labels according to an encoding dictionary.

* **series:**  Pandas series , the series which needs to be encoded.

* **encodeddictionary:**  Dictionary - The dictionary containing encoding labels, can be manually created or with mapping() function.
* **returns:**   Pandas Series

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
test_dict = new_le.mapping(test)
new_le.encode(test , test_dict)
```

Output:

```
0    1
1    2
2    3
3    4
4    5
5    6
dtype: int64
```

With manually inserted dict:
```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
test_dict = {'a' : 10 , 'b' : 52 , 'c' : 71 , 'd' : 3 , 'e' : 49 , 'f' : 103}
new_le.encode(test , test_dict)
```
Output:
```
0     10
1     71
2     52
3      3
4     49
5    103
dtype: int64
```

If not all parameters appear in the mapping dict, the encoder just skips them without encoding:
```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
test_dict = {'a' : 10 , 'b' : 52 , 'c' : 71 , 'd' : 3}
new_le.encode(test , test_dict)
```

Output:
```
0    10
1    71
2    52
3     3
4     e
5     f
dtype: object
```


### decode(series, encodeddictionary)
Decoding series labels according to an encoding dictionary.

* **series:**  Pandas series , the series which needs to be decoded.

* **encodeddictionary:**  Dictionary - The dictionary containing encoding labels, can be manually created or with mapping() function. **It is highly recommended to use the same dictionary as encoding , wether created manually or with mapping() , otherwise wrong decoding will occur.**

* **returns:**   Pandas Series

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
test_dict = new_le.mapping(test)

enc_test = new_le.encode(test , test_dict)
enc_test
```
```
0    1
1    2
2    3
3    4
4    5
5    6
dtype: int64
```
```
dec_test = new_le.decode(enc_test , test_dict)
dec_test
```
```
0    a
1    c
2    b
3    d
4    e
5    f
dtype: object
```


### isnan()
Checks if NaNs were encoded

* **returns:**   Bool , 'True' if NaNs were encoded and 'False' if not



### set_value(label , value)
Setting a specific value to a specific encoded label manually. **A mapping dictionary must be first created before using this function!**
If a value was already reserved to another label in the dictionary , the value is set to the new label and the old label will get a new value (highest that is not used).

* **label:**  label to change the encoding of

* **value:**  Integer , the value encoded for the label

* **returns:**   None

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(test)
```
```
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6}
```
```
new_le.set_value('a' , 8)
```
```
'Label a and its encoded value 8 were successfully added!'
```
```
new_le.dict
```
```
{'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6, 'a': 8}
```
```
new_le.set_value('a' , 3)
```
```
'3 was already the encode of b, now b is encoded as 9
'Label a and its encoded value 3 were successfully added!'
```
```
new_le.dict
```
```
{'c': 2, 'd': 4, 'e': 5, 'f': 6, 'b': 9, 'a': 3}
```


### ignore_nans(value)
Should NaNs be encoded or ignored.

* **value:**  Bool , if 'True' , NaNs will be ignored and not encoded , if 'False' (default when creating the encoder) , NaNs will be encoded (default encoding is 0 , else set with set_nan()


### set_nan(value)
Similar to set_value() , just for NaN. Setting a specific value to encode a NaN. **A mapping dictionary must be first created before using this function!**
If a value was already reserved to another label in the dictionary , the value is set to the new label and the old label will get a new value (highest that is not used).

* **value:**  Integer , the value encoded for the label NaN

* **returns:**   None



### add_label(label , value)
Adding a new label with a specific value to the encoding dictionary. **A mapping dictionary must be first created before using this function!**
If a value was already reserved to another label in the dictionary , the value is set to the new label and the old label will get a new value (highest that is not used).

* **label:**  new label to add the encoding of

* **value:**  Integer , the value encoded for the label

* **returns:**   None

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(test)
```
```
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6}
```
```
new_le.add_label('g' , 9)
```
```
'Label g and its encoded value 7 were successfully added!'
```
```
new_le.dict
```
```
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}
```
```
new_le.set_value('g' , 3)
```
```
3 was already the encode of b, now b is encoded as 7
'Label g and its encoded value 3 were successfully added!'
```
```
new_le.dict
```
```
{'a': 1, 'c': 2, 'd': 4, 'e': 5, 'f': 6, 'b': 7, 'g': 3}
```

If trying to add a label already in dict:
```
new_le.set_value('a' , 3)
```
```
Exception: This label was already encoded , use set_value() to set a different encode or remove_value() to remove it
```


### remove_label(label)
Removing a label from the encoding dictionary. **A mapping dictionary must be first created before using this function!**

* **label:**  new label to add the encoding of

* **returns:**   None

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(test)
```
```
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6}
```
```
new_le.remove_label('a')
```
```
'Label a and its encoded value 1 were successfully removed!'
```
```
new_le.dict
```
```
{'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7}
```


### summary()
Summarizing all data about the encoder

* **returns:**   None

```
test = pd.Series(['a','c','b','d','e','f'])

new_le = LabelEncoder()
new_le.mapping(test)
new_le.summary()
```
```
===============[Encoder Summary]===============
Encoding Dictionary: 
{'a': 1, 'c': 2, 'b': 3, 'd': 4, 'e': 5, 'f': 6}
-----------------------------------------------
Labels:
 ['a', 'c', 'b', 'd', 'e', 'f']
-----------------------------------------------
Total number of unique labels: 6
NaNs found: False
The encoder does encode NaNs
===============================================
```



## Credits
--------------------------------------------------------------------------------------------------------------
If you encounter an issue or a bug or just have a question feel free to email me: nuriel8833@gmail.com

All Rights Reserved © 2022 
