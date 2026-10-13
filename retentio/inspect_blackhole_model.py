import json
from pathlib import Path
p=Path('/tmp/retentio-blackhole/scene.gltf')
data=json.loads(p.read_text())
print('meshes',len(data.get('meshes',[])))
print('nodes',len(data.get('nodes',[])))
print('materials',len(data.get('materials',[])))
print('animations',len(data.get('animations',[])))
for i,m in enumerate(data.get('meshes',[])):
    print(i, m.get('name'), len(m.get('primitives',[])), [x.get('material') for x in m.get('primitives',[])])
for i,n in enumerate(data.get('nodes',[])):
    if 'mesh' in n: print('node',i,n.get('name'),'mesh',n['mesh'],'scale',n.get('scale'),'rotation',n.get('rotation'))
