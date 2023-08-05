# lgpd_xml
## 1 - pip Install
```
pip install lgpdXml
```
## 2 - example replace value
```
#library
from lgpdXml import *

#text
xml = '''<name>john</name><uf>rn</uf><city>natal</city><age>31</age>'''

#call class
text = lgpdXml(xml)

#replace using tag
newText = text.replace('<city>','natal','</city>','parnamirim')

#result
print(newText)
```
## 3 - example find value of tag
```
#library
from lgpdXml import *

#text
xml = '''<name>john</name><uf>rn</uf><city>natal</city><age>31</age>'''

#call class
text = lgpdXml(xml)

#find using tag
searchVal = text.find('<uf>','</uf>')

#result
print(searchVal)
```