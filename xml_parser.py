from lxml import etree

file_path = '21 02 010103.xml'
##context = etree.iterparse(file_path, events=('start','end'))
##context = etree.iterparse(file_path, tag='Parcel')
##for event, element in context:
##    print(element.tag, element.text)

tree = etree.parse(file_path)
elements = [x for x in tree.xpath('//*') if x.tag.endswith('Parcel')]
for i in elements:
    print(i)
