import xml.etree.ElementTree as ET
tree = ET.parse('0001-baomoi-articles.xml')
print(ET.tostring(tree, encoding='utf-8', method='text'))