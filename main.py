# main settings class
from settings import Settings
# merges all dxfs
from xml2dxf import merge_dxfs
# MydxfFile.check() - checking for intersection
from dxf_intersect import MyDxfFile
# convert all xml to dxf
from xml_parser import convert_all_xml2dxf


settings = Settings()
# convert_all_xml2dxf(settings)
# merge_dxfs(settings)
MyDxfFile(settings).check()
convert_all_xml2dxf(settings)
merge_dxfs(settings)
