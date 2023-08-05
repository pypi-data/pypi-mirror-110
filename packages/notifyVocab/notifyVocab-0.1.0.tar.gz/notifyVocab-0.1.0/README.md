# notifyVocab

- _pip/pip3 install notifyVocab_

a small library that notifies you of a new word and its meaning every time you run it

**you can also use task schedular(for windows) to notify you with a new word (inorder to increase you vocabulary while you are working on desktop)**

Developed by Mohammad.Tayyib (c) 2021

## Examples of How To Use

importing it and calling the function (its that simple!!)

```python
from notification import notifyVocab

notifyVocab()

```

**you can also pass the _timeout_(int) as an arguement so that notification may live for more time**

```python
from notification import notifyVocab

timeout = 15 #default 10s
notifyVocab(timeout)

```
