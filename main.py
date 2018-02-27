from xml_parser import RRxml
from settings import Settings
from xml2dxf import RRxml2dxf, merge_dxfs
from pprint import pprint
import ezdxf

settings = Settings()

# dxf_files = []
# for file in settings.xml_list:
#     print(file)
#     xml_file = RRxml(file, settings)
#     pprint(xml_file.blocks)
#     pprint(xml_file.parcels)
#     RRxml2dxf(xml_file, settings).save_dxf()

merge_dxfs(settings)
