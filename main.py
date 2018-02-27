from xml_parser import convert_all_xml2dxf
from settings import Settings
from xml2dxf import merge_dxfs


settings = Settings()
convert_all_xml2dxf(settings)
merge_dxfs(settings)
