import json
from pathlib import Path

source = Path('/tmp/retentio-blackhole/scene.gltf')
out = Path('/home/ubuntu/webdev-static-assets/black-hole-model/scene-web.gltf')
data = json.loads(source.read_text())
urls = {
    'scene.bin': 'scene_af3acc69.bin',
    'textures/Planet_diffuse.png': 'Planet_diffuse_66264e15.png',
    'textures/black_hole_blackoutside_diffuse.png': 'black_hole_blackoutside_diffuse_40c3eb54.png',
    'textures/black_hole_blackoutside_specularGlossiness.png': 'black_hole_blackoutside_specularGlossiness_289da4f2.png',
    'textures/black_hole_light1_diffuse.png': 'black_hole_light1_diffuse_d74d885c.png',
    'textures/black_hole_light1_emissive.png': 'black_hole_light1_emissive_5c1b9706.png',
    'textures/black_hole_light2_diffuse.png': 'black_hole_light2_diffuse_650ab583.png',
    'textures/black_hole_light2_emissive.png': 'black_hole_light2_emissive_6f3ad96c.png',
    'textures/black_hole_light3_diffuse.png': 'black_hole_light3_diffuse_64065bd1.png',
    'textures/black_hole_light3_emissive.png': 'black_hole_light3_emissive_04a2999a.png',
    'textures/ring2_specularGlossiness.png': 'ring2_specularGlossiness_0476f946.png',
    'textures/ring_diffuse.png': 'ring_diffuse_09f7d892.png',
    'textures/ring_specularGlossiness.png': 'ring_specularGlossiness_a1e666bd.png',
}
for collection in ('buffers', 'images'):
    for item in data.get(collection, []):
        if item.get('uri') in urls:
            item['uri'] = urls[item['uri']]
out.write_text(json.dumps(data, separators=(',', ':')))
print(out)
