from xml_parser import convert_all_xml2dxf
from settings import Settings
from xml2dxf import merge_dxfs
from dxf_intersect import MyDxfFile


settings = Settings()
# convert_all_xml2dxf(settings)
# merge_dxfs(settings)
my_dxf_file = MyDxfFile(settings)
checked_parcels = my_dxf_file.check()
with open(settings.settings['my_dxf_check_path'], 'w') as file:
    for parcel in checked_parcels:
        print(parcel, file=file)
