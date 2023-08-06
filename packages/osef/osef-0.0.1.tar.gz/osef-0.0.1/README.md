# OSEF library

Library containing utilities to read and parse a live or recorded stream from an 
Outsight Augmented Lidar Box (ALB). The stream is in the **OSEF** format (**O**utsight **SE**rialization **F**ormat): 
it's an Outsight-defined serialisation binary format used to encode data streaming out of the ALB. 
It is based on *TLV-encoding*.

Full documentation: https://docs.outsight.ai/

## Installation
Install from PyPi using pip:
```bash
pip install osef
``` 
## Usage
Open and parse an osef file or stream: 
```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

file = osef.parser.open_osef(osef_path)
tlv_iterator = osef.parser.get_tlv_iterator(file)
for index, tlv in tlv_iterator:
    tree = osef.parser.build_tree(tlv)
    frame_dict = osef.parser.parse_to_dict(tree)
    tracked_objects = frame_dict["timestamped_frame"]["scan_frame"]["tracked_objects"]
file.close()
```

A shorter version:
```python
import osef

osef_path = "path/to/my/file.osef"
# or osef_path="tcp://192.168.2.2:11120"

frame_iterator = osef.parser.parse(osef_path)
for frame_dict in frame_iterator:
    tracked_objects = frame_dict["timestamped_frame"]["scan_frame"]["tracked_objects"]
```

See more examples:
https://gitlab.com/outsight-public/alb-software-package
