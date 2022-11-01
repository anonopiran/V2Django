import sys
from pathlib import Path

v2ray_proto_path = (Path(__file__).parent / "v2ray_proto").__str__()
if v2ray_proto_path not in sys.path:
    sys.path.append(v2ray_proto_path)
