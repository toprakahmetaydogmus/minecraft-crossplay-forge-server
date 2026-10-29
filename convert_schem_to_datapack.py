# -*- coding: utf-8 -*-
import os
import sys
import json
import nbtlib
from nbtlib.tag import Compound, List, Int, Byte, String

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMATICS_DIR = os.path.join(BASE_DIR, "schematics")
LUXURY_VILLA_FILE = os.path.join(SCHEMATICS_DIR, "luxury-villa.schem")

# 1. Datapack mcfunction
datapack_dir = os.path.join(BASE_DIR, "world", "datapacks", "custom_structures")
func_dir = os.path.join(datapack_dir, "data", "custom", "functions")
os.makedirs(func_dir, exist_ok=True)

pack_meta = {
    "pack": {
        "pack_format": 15,
        "description": "Custom Schematics Fast Builder"
    }
}
with open(os.path.join(datapack_dir, "pack.mcmeta"), "w", encoding="utf-8") as f:
    json.dump(pack_meta, f, indent=2)

from schematics_manager import parse_schematic_to_commands
w, h, l, solid, cmds = parse_schematic_to_commands(LUXURY_VILLA_FILE, center_origin=True)

mcfunction_path = os.path.join(func_dir, "luxury_villa.mcfunction")
with open(mcfunction_path, "w", encoding="utf-8") as f:
    for c in cmds:
        line = c.replace("execute at {p} run ", "")
        f.write(line + "\n")
    f.write('playsound minecraft:ui.toast.challenge_complete master @s ~ ~ ~ 1 1\n')
    f.write('title @s actionbar {"text":"🏰 Luxury Villa Başarıyla İnşa Edildi!","color":"green","bold":true}\n')

print(f"Generated datapack function: {mcfunction_path} ({len(cmds)} commands)")

# 2. Native Minecraft Structure NBT in world/generated/minecraft/structures/luxury-villa.nbt
struct_dir = os.path.join(BASE_DIR, "world", "generated", "minecraft", "structures")
os.makedirs(struct_dir, exist_ok=True)

# Parse Sponge schem to native Structure NBT
schem = nbtlib.load(LUXURY_VILLA_FILE)
s_obj = schem.get('Schematic', schem) if 'Schematic' in schem else schem
raw_bd = s_obj.get('BlockData', [])
bd = [int(b) & 0xff for b in raw_bd]

varints = []
i, total_len = 0, len(bd)
while i < total_len:
    v, s = 0, 0
    while True:
        b = bd[i]; i += 1; v |= (b & 0x7f) << s; s += 7
        if (b & 0x80) == 0: break
    varints.append(v)

palette_dict = s_obj.get('Palette', {})
id_to_state = {int(v): k for k, v in palette_dict.items()}

# Build palette and blocks list for native structure NBT
native_palette = []
state_to_idx = {}

native_blocks = []

for y in range(h):
    for z in range(l):
        for x in range(w):
            idx = (y * l + z) * w + x
            if idx < len(varints):
                st = id_to_state.get(varints[idx], 'minecraft:air')
                if not st.startswith('minecraft:'):
                    st = 'minecraft:' + st
                st = st.replace('pale_oak', 'dark_oak')
                
                # Parse block name and properties
                if '[' in st and st.endswith(']'):
                    bname, props_str = st[:-1].split('[', 1)
                    props = {}
                    for p in props_str.split(','):
                        if '=' in p:
                            pk, pv = p.split('=', 1)
                            props[pk] = String(pv)
                else:
                    bname = st
                    props = {}
                
                full_sig = st
                if full_sig not in state_to_idx:
                    state_to_idx[full_sig] = len(native_palette)
                    tag = Compound({"Name": String(bname)})
                    if props:
                        tag["Properties"] = Compound(props)
                    native_palette.append(tag)
                
                state_idx = state_to_idx[full_sig]
                native_blocks.append(Compound({
                    "pos": List[Int]([Int(x), Int(y), Int(z)]),
                    "state": Int(state_idx)
                }))

structure_file = nbtlib.File({
    "": Compound({
        "DataVersion": Int(3465),
        "size": List[Int]([Int(w), Int(h), Int(l)]),
        "entities": List[Compound]([]),
        "palette": List[Compound](native_palette),
        "blocks": List[Compound](native_blocks)
    })
})

out_nbt_path = os.path.join(struct_dir, "luxury-villa.nbt")
structure_file.save(out_nbt_path, gzipped=True)
print(f"Generated native Minecraft Structure NBT: {out_nbt_path}")
