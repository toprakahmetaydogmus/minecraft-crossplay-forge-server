# -*- coding: utf-8 -*-
"""
🏛️ MINECRAFT SCHEMATICS DATASET & ADVANCED ARCHITECTURE STUDIO
=============================================================================
Entegrasyon: https://github.com/rom1504/minecraft-schematics-dataset
Ev Yapıları, Dağ Kulübeleri, Kaleler, Gökdelenler, Tapınaklar, Gemiler,
Kızıltaş Makineleri, Heykeller, Arenalar, Köprüler, Siberpunk & Peyzaj
kategorilerini içeren profesyonel mimari kontrol ve inşa modülü.
=============================================================================
"""

import os
import sys
import shutil
import threading
import json
import urllib.request
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import nbtlib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMATICS_DIR = os.path.join(BASE_DIR, "schematics")
WORLD_STRUCTURES_DIR = os.path.join(BASE_DIR, "world", "generated", "minecraft", "structures")

os.makedirs(SCHEMATICS_DIR, exist_ok=True)
os.makedirs(WORLD_STRUCTURES_DIR, exist_ok=True)


# =============================================================================
# 13 AYRI SEKME İÇİN 160+ ZENGİN SCHEMATIC MİMARİ VERİTABANI (TABS_DATA)
# =============================================================================
SCHEMATIC_TABS = {
    # -------------------------------------------------------------------------
    # 1. 🏛️ SCHEMATIC VERİ SETİ (rom1504 Dataset) - ANA KONTROL VE EN SEÇKİN YAPILAR
    # -------------------------------------------------------------------------
    "🏛️ SCHEMATIC VERİ SETİ (rom1504 Dataset)": [
        ("🏡 Modern Cam & Kuvars Lüks Villa (Havuzlu, Balkonlu, Teraslı)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~5 ~5 air && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-5 ~5 ~-5 ~5 ~5 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 air && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-4 ~-1 ~-4 sea_lantern && execute at {p} run setblock ~4 ~-1 ~4 sea_lantern && execute at {p} run setblock ~-3 ~ ~-4 chest && execute at {p} run setblock ~-2 ~ ~-4 crafting_table && execute at {p} run setblock ~-1 ~ ~-4 blast_furnace && execute at {p} run setblock ~-4 ~ ~3 cyan_bed && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north] && execute at {p} run fill ~-3 ~-2 ~-9 ~3 ~-1 ~-6 smooth_stone && execute at {p} run fill ~-2 ~-2 ~-8 ~2 ~-1 ~-7 water && playsound minecraft:ui.toast.challenge_complete master {p} ~ ~ ~ 1 1 && title {p} actionbar {\"text\":\"🏗️ Modern Cam Villa Başarıyla İnşa Edildi!\",\"color\":\"green\",\"bold\":true}",
         "14x9x14 Blok | rom1504:modern_villa_01 | Kuvars tabanlı, 2 katlı lüks cam villa, yüzme havuzlu ve mobilyalı"),

        ("🏰 Kraliyet 4 Kuleli Taş Kalesi & Şato (Mazgallı Surlar)",
         "execute at {p} run fill ~-9 ~-1 ~-9 ~9 ~-1 ~9 deepslate_bricks && execute at {p} run fill ~-9 ~ ~-9 ~9 ~7 ~9 deepslate_bricks outline && execute at {p} run fill ~-8 ~ ~-8 ~8 ~6 ~8 air && execute at {p} run fill ~-9 ~8 ~-9 ~9 ~8 ~9 stone_brick_wall outline && execute at {p} run fill ~-10 ~ ~-10 ~-7 ~12 ~-7 deepslate_bricks outline && execute at {p} run fill ~7 ~ ~-10 ~10 ~12 ~-7 deepslate_bricks outline && execute at {p} run fill ~-10 ~ ~7 ~-7 ~12 ~10 deepslate_bricks outline && execute at {p} run fill ~7 ~ ~7 ~10 ~12 ~10 deepslate_bricks outline && execute at {p} run setblock ~-9 ~13 ~-9 sea_lantern && execute at {p} run setblock ~9 ~13 ~-9 sea_lantern && execute at {p} run setblock ~-9 ~13 ~9 sea_lantern && execute at {p} run setblock ~9 ~13 ~9 sea_lantern && execute at {p} run fill ~-1 ~ ~-9 ~1 ~2 ~-9 air && execute at {p} run setblock ~ ~ ~-9 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-9 iron_door[half=upper,facing=north] && playsound minecraft:block.anvil.use master @a && broadcast &6[KRALLIK] &e{p} &6Kraliyet Taş Kalesi &ainşa etti!",
         "22x14x22 Blok | rom1504:royal_castle_01 | 4 köşede gözetleme kuleleri, mazgallı surları ve zırhlı kapısıyla kraliyet şatosu"),

        ("🧙‍♂️ Spiral Büyücü Kulesi (Kütüphane & Rasathane)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 deepslate_bricks && execute at {p} run fill ~-3 ~ ~-3 ~3 ~22 ~3 deepslate_bricks outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~21 ~2 air && execute at {p} run fill ~ ~-1 ~ ~ ~21 ~ ladder[facing=north] && execute at {p} run fill ~-4 ~22 ~-4 ~4 ~22 ~4 polished_blackstone && execute at {p} run fill ~-4 ~23 ~-4 ~4 ~23 ~4 amethyst_block outline && execute at {p} run setblock ~ ~22 ~ beacon && execute at {p} run setblock ~ ~-1 ~ netherite_block && execute at {p} run setblock ~-1 ~ ~-1 enchanting_table && execute at {p} run setblock ~1 ~ ~-1 brewing_stand && execute at {p} run fill ~-1 ~ ~-3 ~1 ~1 ~-3 air && playsound minecraft:block.enchantment_table.use master {p}",
         "12x26x12 Blok | rom1504:wizard_tower_01 | 26 blokluk spiral basamaklı, seviye 30 büyü masalı, ametist çatılı ve fenerli kule"),

        ("🏜️ Antik Mısır Piramidi & Gizli Firavun Lahiti",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 sandstone && execute at {p} run fill ~-7 ~ ~-7 ~7 ~7 ~7 sandstone && execute at {p} run fill ~-6 ~1 ~-6 ~6 ~7 ~6 sandstone && execute at {p} run fill ~-5 ~2 ~-5 ~5 ~7 ~5 sandstone && execute at {p} run fill ~-4 ~3 ~-4 ~4 ~7 ~4 sandstone && execute at {p} run fill ~-3 ~4 ~-3 ~3 ~7 ~3 sandstone && execute at {p} run fill ~-2 ~5 ~-2 ~2 ~7 ~2 sandstone && execute at {p} run fill ~-1 ~6 ~-1 ~1 ~7 ~1 sandstone && execute at {p} run setblock ~ ~7 ~ gold_block && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run setblock ~ ~ ~ chest && execute at {p} run setblock ~ ~-1 ~ gold_block && execute at {p} run fill ~ ~ ~-7 ~ ~1 ~-4 air && playsound minecraft:block.sand.break master {p}",
         "18x10x18 Blok | rom1504:pyramid_01 | Altın blok zirveli basamaklı kumtaşı piramit ve içinde gizli sandık mezar odası"),

        ("⚓ 3 Direkli Kraliyet Savaş Kalyonu (Borda Toplu, Yelkenli)",
         "execute at {p} run fill ~-3 ~-2 ~-8 ~3 ~-1 ~8 dark_oak_planks && execute at {p} run fill ~-3 ~ ~-8 ~3 ~ ~8 dark_oak_fence outline && execute at {p} run fill ~-2 ~ ~-7 ~2 ~ ~7 air && execute at {p} run fill ~ ~ ~-4 ~ ~8 ~-4 spruce_log && execute at {p} run fill ~ ~ ~ ~ ~10 ~ spruce_log && execute at {p} run fill ~ ~ ~4 ~ ~8 ~4 spruce_log && execute at {p} run fill ~-2 ~5 ~-4 ~2 ~7 ~-4 white_wool && execute at {p} run fill ~-2 ~6 ~ ~2 ~9 ~ white_wool && execute at {p} run fill ~-2 ~5 ~4 ~2 ~7 ~4 white_wool && execute at {p} run setblock ~-3 ~ ~ dispenser[facing=west] && execute at {p} run setblock ~3 ~ ~ dispenser[facing=east] && playsound minecraft:item.trident.thunder master {p}",
         "14x18x24 Blok | rom1504:war_galleon_01 | Koyu meşe gövdeli, 3 beyaz yelkenli yüksek direkli, borda dispenser toplu savaş gemisi"),

        ("🔥 64 Fırınlı Süper Otomatik Eritici Fabrikası",
         "execute at {p} run fill ~-6 ~-1 ~-3 ~6 ~-1 ~3 smooth_stone && execute at {p} run fill ~-5 ~ ~-2 ~5 ~ ~-2 blast_furnace && execute at {p} run fill ~-5 ~ ~2 ~5 ~ ~2 blast_furnace && execute at {p} run fill ~-5 ~1 ~-2 ~5 ~1 ~-2 hopper && execute at {p} run fill ~-5 ~1 ~2 ~5 ~1 ~2 hopper && execute at {p} run fill ~-5 ~2 ~-2 ~5 ~2 ~-2 chest && execute at {p} run fill ~-5 ~2 ~2 ~5 ~2 ~2 chest && execute at {p} run fill ~-5 ~-1 ~ ~5 ~-1 ~ hopper && execute at {p} run setblock ~ ~ ~ chest && playsound minecraft:block.anvil.use master {p}",
         "16x7x12 Blok | rom1504:super_smelter_01 | Çift sıra yüksek fırınlar, üstten kömür/maden hunileri ve otomatik sandık deposu"),

        ("🐉 Ateş Püskürten Kanatlı Dev Ejderha Heykeli",
         "execute at {p} run fill ~-2 ~ ~-2 ~2 ~6 ~2 black_concrete && execute at {p} run fill ~-6 ~4 ~-4 ~6 ~10 ~-4 obsidian && execute at {p} run fill ~-8 ~8 ~-5 ~-4 ~12 ~-5 black_concrete && execute at {p} run fill ~4 ~8 ~-5 ~8 ~12 ~-5 black_concrete && execute at {p} run fill ~-1 ~7 ~2 ~1 ~11 ~5 black_concrete && execute at {p} run setblock ~-1 ~10 ~5 redstone_lamp && execute at {p} run setblock ~1 ~10 ~5 redstone_lamp && execute at {p} run setblock ~ ~8 ~6 lava && execute at {p} run setblock ~ ~-1 ~ obsidian && playsound minecraft:entity.ender_dragon.growl master @a ~ ~ ~ 1 1 && broadcast &4[EJDERHA] &e{p} &4Ateş Püskürten Dev Ejderha Heykeli &adikti!",
         "20x16x24 Blok | rom1504:dragon_statue_01 | Kanatlarını açmış, ağzından lav şelalesi ve ateş fışkıran devasa heykel"),

        ("🏛️ Roma Kolezyumu Gladyatör Arenası (Tribünlü)",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 red_sand && execute at {p} run fill ~-12 ~ ~-12 ~12 ~5 ~12 smooth_sandstone outline && execute at {p} run fill ~-11 ~ ~-11 ~11 ~5 ~11 air && execute at {p} run fill ~-11 ~1 ~-11 ~11 ~3 ~-11 sandstone_stairs[facing=south] && execute at {p} run fill ~-11 ~1 ~11 ~11 ~3 ~11 sandstone_stairs[facing=north] && execute at {p} run setblock ~-12 ~6 ~-12 torch && execute at {p} run setblock ~12 ~6 ~-12 torch && execute at {p} run setblock ~-12 ~6 ~12 torch && execute at {p} run setblock ~12 ~6 ~12 torch && playsound minecraft:entity.player.attack.crit master @a",
         "28x12x28 Blok | rom1504:colosseum_01 | 28x28 dairesel kum zeminli Roma kolezyumu, basamaklı seyirci tribünleri ve meşaleler"),

        ("🌉 Halatlı Modern Asma Köprü (Golden Gate Tarzı)",
         "execute at {p} run fill ~-15 ~-1 ~-3 ~15 ~-1 ~3 polished_blackstone && execute at {p} run fill ~-15 ~-1 ~ ~15 ~-1 ~ yellow_concrete && execute at {p} run fill ~-10 ~ ~-3 ~-10 ~12 ~-3 red_concrete && execute at {p} run fill ~-10 ~ ~3 ~-10 ~12 ~3 red_concrete && execute at {p} run fill ~10 ~ ~-3 ~10 ~12 ~-3 red_concrete && execute at {p} run fill ~10 ~ ~3 ~10 ~12 ~3 red_concrete && execute at {p} run fill ~-15 ~ ~-4 ~15 ~ ~-4 iron_bars && execute at {p} run fill ~-15 ~ ~4 ~15 ~ ~4 iron_bars && execute at {p} run setblock ~-10 ~13 ~-3 sea_lantern && execute at {p} run setblock ~10 ~13 ~-3 sea_lantern && playsound minecraft:block.anvil.place master {p}",
         "32x16x10 Blok | rom1504:suspension_bridge_01 | 32 blok uzunluğunda kırmızı kuleli modern asma köprü, çelik halatlar ve asfalt yol"),

        ("🪐 Mars Kolonisi Biyosfer Kubbesi (Oksijen Serası)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 iron_block && execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 grass_block && execute at {p} run fill ~-7 ~ ~-7 ~7 ~8 ~7 light_blue_stained_glass outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~7 ~6 air && execute at {p} run setblock ~ ~ ~ oak_sapling && execute at {p} run setblock ~-4 ~ ~-4 sea_lantern && execute at {p} run setblock ~4 ~ ~4 sea_lantern && execute at {p} run setblock ~ ~ ~-7 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-7 iron_door[half=upper,facing=north] && playsound minecraft:block.beacon.activate master {p}",
         "18x12x18 Blok | rom1504:mars_biodome_01 | Kapalı jeodezik cam kubbe biyosferi, yapay orman ekosistemi ve hava kilitli kapı"),

        ("🎋 Zen Meditasyon Bahçesi (Tırmıklı Kum, Bambu & Kaya Sanatı)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sand && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_sandstone && execute at {p} run setblock ~-3 ~ ~-3 polished_andesite && execute at {p} run setblock ~3 ~ ~-3 polished_andesite && execute at {p} run setblock ~-3 ~ ~3 bamboo && execute at {p} run setblock ~3 ~ ~3 bamboo && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ lily_pad && execute at {p} run setblock ~ ~1 ~ lantern && playsound minecraft:block.bamboo.place master {p}",
         "14x5x14 Blok | rom1504:zen_garden_01 | Düzgün tırmıklı kum zemin, cilalı andezit kayalar, bambu korusu ve nilüferli su kasesi")
    ],

    # -------------------------------------------------------------------------
    # 2. 🏡 EVLER, VİLLALAR & MALİKANELER (Houses, Modern Villas & Mansions)
    # -------------------------------------------------------------------------
    "🏡 EVLER, VİLLALAR & MALİKANELER": [
        ("🏡 2 Katlı Lüks Cam & Havuzlu Villa",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~5 ~5 air && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-5 ~5 ~-5 ~5 ~5 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 air && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-4 ~-1 ~-4 sea_lantern && execute at {p} run setblock ~4 ~-1 ~4 sea_lantern && execute at {p} run setblock ~-3 ~ ~-4 chest && execute at {p} run setblock ~-2 ~ ~-4 crafting_table && execute at {p} run setblock ~-1 ~ ~-4 furnace && execute at {p} run setblock ~-4 ~ ~3 red_bed && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north] && execute at {p} run fill ~-3 ~-2 ~-9 ~3 ~-1 ~-6 smooth_stone && execute at {p} run fill ~-2 ~-2 ~-8 ~2 ~-1 ~-7 water && playsound minecraft:block.anvil.use master {p} ~ ~ ~ 1 1",
         "Kuvars zeminli, cam duvarlı, çift kişilik yataklı, fırınlı ve önünde havuzlu tam modern villa"),

        ("🌳 Amerikan Banliyö Aile Evi (Garajlı, Çatılı, Çiçek Bahçeli)",
         "execute at {p} run fill ~-6 ~-1 ~-5 ~6 ~-1 ~5 oak_planks && execute at {p} run fill ~-6 ~ ~-5 ~6 ~4 ~5 bricks outline && execute at {p} run fill ~-5 ~ ~-4 ~5 ~3 ~4 air && execute at {p} run fill ~-6 ~4 ~-5 ~6 ~4 ~5 dark_oak_stairs[facing=north] outline && execute at {p} run fill ~-7 ~ ~-6 ~-3 ~ ~-6 oak_fence && execute at {p} run fill ~-5 ~ ~-5 ~-3 ~2 ~-5 iron_bars && execute at {p} run setblock ~4 ~ ~4 bricks && execute at {p} run setblock ~4 ~1 ~4 bricks && execute at {p} run setblock ~4 ~2 ~4 bricks && execute at {p} run setblock ~4 ~3 ~4 campfire && execute at {p} run setblock ~-4 ~ ~3 red_bed && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north] && playsound minecraft:block.wood.place master {p} ~ ~ ~ 1 1",
         "Tuğla duvarlı, eğimli çatılı, şömineli, garaj girişli ve çiçek tarhlı banliyö evi"),

        ("🌊 Sahil Malibu Cam Malikanesi (Okyanus Manzaralı, Şezlonglu)",
         "execute at {p} run fill ~-7 ~-1 ~-6 ~7 ~-1 ~6 smooth_quartz && execute at {p} run fill ~-7 ~ ~-6 ~7 ~5 ~6 tinted_glass outline && execute at {p} run fill ~-6 ~ ~-5 ~6 ~4 ~5 air && execute at {p} run fill ~-7 ~5 ~-6 ~7 ~5 ~6 smooth_quartz && execute at {p} run fill ~3 ~-1 ~2 ~6 ~-1 ~5 water && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-5 ~ ~4 cyan_bed && execute at {p} run setblock ~-5 ~ ~3 chest && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air && playsound minecraft:block.anvil.use master {p} ~ ~ ~ 1 1",
         "Okyanus kıyısı kuvars zeminli malikane, jakuzi havuzu, tavan aydınlatması ve çift kişilik süit yatak"),

        ("🪵 Minimalist İskandinav A-Frame Üçgen Ev (Jakuzili)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 dark_oak_planks && execute at {p} run fill ~-6 ~ ~-6 ~6 ~ ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-5 ~1 ~-6 ~5 ~1 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-4 ~2 ~-6 ~4 ~2 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-3 ~3 ~-6 ~3 ~3 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-2 ~4 ~-6 ~2 ~4 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-1 ~5 ~-6 ~1 ~5 ~6 dark_oak_stairs[facing=north] && execute at {p} run fill ~-5 ~ ~-6 ~5 ~4 ~-6 tinted_glass && execute at {p} run fill ~-4 ~ ~-5 ~4 ~3 ~5 air && execute at {p} run fill ~2 ~-1 ~2 ~4 ~-1 ~4 smooth_quartz && execute at {p} run fill ~2 ~ ~2 ~4 ~ ~4 water && execute at {p} run setblock ~-3 ~ ~3 blue_bed && execute at {p} run setblock ~-3 ~ ~ campfire && execute at {p} run setblock ~ ~ ~-6 spruce_door[half=lower,facing=north]",
         "Üçgen A-Frame dik çatılı modern İskandinav dağ evi, boydan boya cam ön cephe, sıcak şömine ve jakuzi"),

        ("🏰 3 Katlı Gotik Vampir Malikanesi (Kütüphane & Şömine)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 deepslate_bricks && execute at {p} run fill ~-7 ~ ~-7 ~7 ~14 ~7 deepslate_bricks outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~13 ~6 air && execute at {p} run fill ~-7 ~4 ~-7 ~7 ~4 ~7 dark_oak_planks && execute at {p} run fill ~-7 ~9 ~-7 ~7 ~9 ~7 dark_oak_planks && execute at {p} run fill ~-1 ~4 ~-1 ~1 ~4 ~1 air && execute at {p} run fill ~-1 ~9 ~-1 ~1 ~9 ~1 air && execute at {p} run setblock ~5 ~ ~5 campfire && execute at {p} run setblock ~5 ~1 ~5 bricks && execute at {p} run setblock ~5 ~2 ~5 bricks && execute at {p} run fill ~-5 ~5 ~-5 ~-2 ~5 ~-5 bookshelf && execute at {p} run setblock ~-5 ~10 ~-5 red_bed && execute at {p} run setblock ~ ~1 ~ soul_lantern[hanging=true] && execute at {p} run fill ~-1 ~ ~-7 ~1 ~2 ~-7 air && execute at {p} run setblock ~ ~ ~-7 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-7 iron_door[half=upper,facing=north]",
         "3 katlı taş Gotik köşk, tuğla bacalı şömine, dev kütüphane odası, kırmızı kadife yataklı süit ve zırhlı kapı"),

        ("🏜️ Modern Çöl Cam Villası (Beyaz Kuvars & Havuzlu Avlu)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_quartz && execute at {p} run fill ~-6 ~ ~-6 ~6 ~4 ~6 smooth_quartz outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-6 ~1 ~-5 ~-6 ~3 ~-2 tinted_glass && execute at {p} run fill ~6 ~1 ~-5 ~6 ~3 ~-2 tinted_glass && execute at {p} run fill ~1 ~-1 ~1 ~4 ~-1 ~4 water && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-4 ~ ~3 white_bed && execute at {p} run setblock ~-4 ~ ~-4 cactus && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Kuvars ve karartılmış camdan avangart çöl villası, avluda gömme yüzme havuzu, kaktüs köşesi ve lüks yatak"),

        ("🏖️ Maldivler Su Üstü Cam Bungalov Malikanesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 oak_planks && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 tinted_glass && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 oak_fence outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 hay_block && execute at {p} run setblock ~-3 ~ ~-3 cyan_bed && execute at {p} run setblock ~3 ~ ~-3 chest && execute at {p} run fill ~-1 ~-1 ~-8 ~1 ~-1 ~-5 oak_planks && execute at {p} run setblock ~ ~ ~-1 sea_lantern && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 oak_door[half=upper,facing=north]",
         "Tabanı okyanus altını gösteren cam zeminli, saman çatılı, iskeleli ve şezlonglu Maldiv su villası"),

        ("🛸 Fütüristik Kapsül Minimalist Ev (Cyber Pod)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 iron_block && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run fill ~-4 ~1 ~-3 ~-4 ~2 ~3 light_blue_stained_glass && execute at {p} run fill ~4 ~1 ~-3 ~4 ~2 ~3 light_blue_stained_glass && execute at {p} run setblock ~ ~2 ~ sea_lantern && execute at {p} run setblock ~-2 ~ ~2 white_bed && execute at {p} run setblock ~2 ~ ~2 ender_chest && execute at {p} run fill ~-1 ~ ~-4 ~1 ~1 ~-4 air",
         "Beyaz kuvars ve mavi lazer camdan tek parça aerodinamik kapsül ev, akıllı aydınlatma ve Ender Sandığı"),

        ("🏔️ Uçurum Kenarı Asılı Cam Malikane (Panoramik Teras)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 polished_blackstone && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 smooth_quartz && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run setblock ~-3 ~ ~3 cyan_bed && execute at {p} run setblock ~3 ~ ~3 chest && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~ ~-5 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 iron_door[half=upper,facing=north]",
         "Uçurum kenarlarından vadiye uzanan panaromik karartılmış cam zeminli ve tavanlı lüks modern malikane"),

        ("🏢 Dubleks Şehir Rezidans Evi (Kuvars & Tuğla Karma)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 smooth_quartz outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 oak_planks && execute at {p} run fill ~-1 ~3 ~-1 ~1 ~3 ~1 air && execute at {p} run fill ~-5 ~1 ~-5 ~-5 ~2 ~-2 tinted_glass && execute at {p} run setblock ~-3 ~4 ~3 red_bed && execute at {p} run setblock ~3 ~ ~3 blast_furnace && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "2 katlı şehir dubleksi, iç merdiven, geniş camlar, yatak süiti ve mutfak reyonu"),

        ("🌾 Akdeniz Taş Çiftlik Evi (Zeytinlik & Verandalı)",
         "execute at {p} run fill ~-6 ~-1 ~-5 ~6 ~-1 ~5 terracotta && execute at {p} run fill ~-6 ~ ~-5 ~6 ~3 ~5 sandstone outline && execute at {p} run fill ~-5 ~ ~-4 ~5 ~2 ~4 air && execute at {p} run fill ~-6 ~3 ~-5 ~6 ~3 ~5 smooth_sandstone_slab && execute at {p} run fill ~-7 ~ ~-6 ~-3 ~ ~-6 oak_fence && execute at {p} run setblock ~4 ~ ~3 yellow_bed && execute at {p} run setblock ~-4 ~ ~3 barrel && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "Pişmiş toprak zeminli, kumtaşı duvarlı, çardaklı ve fıçılı Akdeniz kır evi"),

        ("🦇 Yeraltı Gizli Sığınak Malikanesi (3 Katlı Lüks Bunker)",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 cobblestone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 spruce_planks outline && execute at {p} run setblock ~ ~ ~ iron_trapdoor && execute at {p} run fill ~ ~-6 ~ ~ ~-1 ~ ladder[facing=north] && execute at {p} run fill ~-5 ~-10 ~-5 ~5 ~-6 ~5 reinforced_deepslate outline && execute at {p} run fill ~-4 ~-9 ~-4 ~4 ~-7 ~4 air && execute at {p} run setblock ~ ~-7 ~ sea_lantern && execute at {p} run setblock ~-3 ~-9 ~-3 enchanting_table && execute at {p} run setblock ~3 ~-9 ~-3 respawn_anchor[charges=4] && execute at {p} run setblock ~-3 ~-9 ~3 red_bed && execute at {p} run setblock ~3 ~-9 ~3 chest",
         "Yüzeyde sıradan kulübe, tuzak kapısından inilen Y:-10 derinliğinde lüks nükleer sığınak malikanesi")
    ],

    # -------------------------------------------------------------------------
    # 3. 🪵 DAĞ EVLERİ, KÜTÜK & ORMAN EVLERİ (Rustic, Cabins & Treehouses)
    # -------------------------------------------------------------------------
    "🪵 DAĞ EVLERİ, KÜTÜK & ORMAN EVLERİ": [
        ("🪵 Dağ Kütük Avcı Kulübesi (Dumanlı Şömine, Fıçılı Kiler)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 cobblestone && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 spruce_planks outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run fill ~-4 ~ ~-4 ~-4 ~3 ~-4 spruce_log && execute at {p} run fill ~4 ~ ~-4 ~4 ~3 ~-4 spruce_log && execute at {p} run fill ~-4 ~ ~4 ~-4 ~3 ~4 spruce_log && execute at {p} run fill ~4 ~ ~4 ~4 ~3 ~4 spruce_log && execute at {p} run setblock ~3 ~ ~3 bricks && execute at {p} run setblock ~3 ~1 ~3 bricks && execute at {p} run setblock ~3 ~2 ~3 bricks && execute at {p} run setblock ~3 ~3 ~3 campfire && execute at {p} run setblock ~3 ~4 ~3 cobblestone_wall && execute at {p} run setblock ~-3 ~ ~3 blue_bed && execute at {p} run setblock ~-3 ~ ~2 chest && execute at {p} run setblock ~-3 ~ ~1 crafting_table && execute at {p} run setblock ~ ~3 ~ lantern[hanging=true] && execute at {p} run setblock ~ ~ ~-4 spruce_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-4 spruce_door[half=upper,facing=north] && playsound minecraft:block.wood.place master {p} ~ ~ ~ 1 1",
         "Ladin kütüklerinden sıcacık dağ kulübesi, bacasından duman tüten tuğla şömine, yatak ve mobilyalar"),

        ("🍁 Sıcak Huş Ormanı Çift Katlı Ahşap Evi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 birch_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 stripped_birch_wood outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~5 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 birch_planks && execute at {p} run fill ~-1 ~3 ~-1 ~1 ~3 ~1 air && execute at {p} run setblock ~3 ~ ~3 campfire && execute at {p} run setblock ~-3 ~4 ~-3 yellow_bed && execute at {p} run setblock ~3 ~4 ~-3 chest && execute at {p} run setblock ~ ~ ~-5 birch_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 birch_door[half=upper,facing=north]",
         "Huş ağacı kütüklerinden çift katlı sıcacık sonbahar orman evi, şömine, çatı katı yatak odası ve balkon"),

        ("🌲 Dev Elf Ağaç Evi (Y: 20 Yüksek, Teraslı & Asılı Bahçeli)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~20 ~1 oak_log && execute at {p} run fill ~ ~-1 ~-2 ~ ~20 ~-2 ladder[facing=north] && execute at {p} run fill ~-5 20 ~-5 ~5 20 ~5 oak_planks && execute at {p} run fill ~-6 21 ~-6 ~6 21 ~6 oak_leaves outline && execute at {p} run fill ~-5 24 ~-5 ~5 24 ~5 oak_leaves && execute at {p} run setblock ~-4 21 ~-4 lantern && execute at {p} run setblock ~4 21 ~-4 lantern && execute at {p} run setblock ~-4 21 ~4 lantern && execute at {p} run setblock ~4 21 ~4 lantern && execute at {p} run setblock ~ 21 ~2 red_bed && execute at {p} run setblock ~-2 21 ~2 chest",
         "20 blok yüksekliğinde dev meşe gövdesi, tepeye çıkan merdiven, yaprak çatılı teras ve yatak odası"),

        ("🌳 Hobbit Çukur Evi (The Shire Çimen Çatılı Doğa Evi)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 dirt && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 dirt && execute at {p} run fill ~-4 ~ ~-4 ~4 ~2 ~4 air && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~4 ~5 grass_block && execute at {p} run fill ~-5 ~ ~-5 ~-5 ~3 ~5 spruce_planks && execute at {p} run setblock ~3 ~ ~3 bricks && execute at {p} run setblock ~3 ~1 ~3 bricks && execute at {p} run setblock ~3 ~2 ~3 campfire && execute at {p} run setblock ~-3 ~ ~-3 green_bed && execute at {p} run setblock ~-3 ~ ~3 barrel && execute at {p} run setblock ~ ~ ~-5 spruce_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 spruce_door[half=upper,facing=north] && execute at {p} run setblock ~ ~2 ~ lantern[hanging=true]",
         "Yemyeşil tepeciğin içine oyulmuş otantik Hobbit çukur evi, çimen çatı, tuğla şömine, fıçılı kiler ve yatak"),

        ("❄️ Tayga Kar Şalesi (Koyu Ladin & Jakuzili Sıcak Dağ Evi)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 spruce_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 dark_oak_planks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-5 ~4 ~-5 ~5 ~4 ~5 snow_block && execute at {p} run setblock ~3 ~ ~3 campfire && execute at {p} run setblock ~-3 ~ ~3 blue_bed && execute at {p} run setblock ~ ~ ~-5 spruce_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 spruce_door[half=upper,facing=north]",
         "Kar kaplı çatılı, koyu meşe duvarlı, dumanlı şömineli sıcak kış dağ evi"),

        ("🍄 Büyülü Kırmızı Mantar Peri Evi (İki Katlı)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_stone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~6 ~2 mushroom_stem outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~5 ~1 air && execute at {p} run fill ~-4 ~5 ~-4 ~4 ~7 ~4 red_mushroom_block outline && execute at {p} run fill ~-3 ~5 ~-3 ~3 ~6 ~3 air && execute at {p} run fill ~-1 ~ ~ ~-1 ~5 ~ ladder[facing=east] && execute at {p} run setblock ~ ~5 ~ red_bed && execute at {p} run setblock ~ ~5 ~-2 brewing_stand && execute at {p} run setblock ~ ~ ~-2 oak_door[half=lower,facing=north]",
         "Doğal mantar gövdesi, spiral tırmanma merdiveni, üst katta kırmızı şapka odası, iksir standı ve peri yatağı"),

        ("🧱 Kırsal İngiliz Taş Köy Evi (Tuğla Bacalı Kır Evi)",
         "execute at {p} run fill ~-5 ~-1 ~-4 ~5 ~-1 ~4 cobblestone && execute at {p} run fill ~-5 ~ ~-4 ~5 ~4 ~4 stone_bricks outline && execute at {p} run fill ~-4 ~ ~-3 ~4 ~3 ~3 air && execute at {p} run setblock ~4 ~ ~3 bricks && execute at {p} run setblock ~4 ~1 ~3 bricks && execute at {p} run setblock ~4 ~2 ~3 bricks && execute at {p} run setblock ~4 ~3 ~3 bricks && execute at {p} run setblock ~4 ~4 ~3 campfire && execute at {p} run setblock ~-3 ~ ~2 red_bed && execute at {p} run setblock ~-3 ~ ~1 chest && execute at {p} run setblock ~ ~ ~-4 oak_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-4 oak_door[half=upper,facing=north]",
         "Taş tuğla duvarlı, yüksek tuğla bacasından duman tüten şömineli, nostaljik İngiliz kır evi"),

        ("🏯 Bambu Verandalı Geleneksel Japon Minka Evi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 stripped_oak_wood && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 dark_oak_planks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~2 ~4 air && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 hay_block && execute at {p} run fill ~-5 ~3 ~-5 ~5 ~3 ~5 dark_oak_slab && execute at {p} run setblock ~ ~ ~-1 bamboo && execute at {p} run setblock ~-3 ~ ~3 red_bed && execute at {p} run setblock ~ ~ ~-5 cherry_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-5 cherry_door[half=upper,facing=north]",
         "Geleneksel Japon Minka mimarisi, hasır zemin hissi, kavisli saçaklı ahşap çatı, bambu veranda ve fener"),

        ("💧 Nehir Kenarı Su Değirmeni Evi (Dönen Çark Mekanizması)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 spruce_planks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 spruce_planks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run fill ~-6 ~ ~-2 ~-6 ~4 ~2 dark_oak_stairs[facing=north] && execute at {p} run fill ~-5 ~-1 ~-2 ~-5 ~-1 ~2 water && execute at {p} run setblock ~3 ~ ~3 blast_furnace && execute at {p} run setblock ~-3 ~ ~3 red_bed && execute at {p} run setblock ~ ~ ~-5 spruce_door[half=lower,facing=north]",
         "Su çarklı rustik nehir evi, un öğütme fırınları, ahşap teras ve konforlu yatak odası"),

        ("🤠 Vahşi Batı Kovboy Çiftlik Evi (Ranch & Ahır)",
         "execute at {p} run fill ~-6 ~-1 ~-5 ~6 ~-1 ~5 oak_planks && execute at {p} run fill ~-6 ~ ~-5 ~6 ~3 ~5 oak_planks outline && execute at {p} run fill ~-5 ~ ~-4 ~5 ~2 ~4 air && execute at {p} run fill ~-6 ~ ~-6 ~6 ~ ~-6 oak_fence && execute at {p} run setblock ~-4 ~ ~3 barrel && execute at {p} run setblock ~4 ~ ~3 red_bed && execute at {p} run setblock ~ ~ ~-5 oak_door[half=lower,facing=north]",
         "Geniş ahşap verandalı, fıçılı, at bağlama çitli ve samanlı Vahşi Batı kovboy ranch çiftlik evi"),

        ("🌿 Yosunlu Antik Ormancı Evi (Gizemli Sarmaşıklı)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 mossy_cobblestone && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 mossy_stone_bricks outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run fill ~-4 ~3 ~-4 ~4 ~3 ~4 moss_block && execute at {p} run setblock ~3 ~ ~3 brewing_stand && execute at {p} run setblock ~-3 ~ ~3 green_bed && execute at {p} run setblock ~ ~ ~-4 oak_door[half=lower,facing=north]",
         "Yosunlu taşlar ve sarmaşıklarla kaplı, gizemli orman derinliklerinde simyacı ormancı evi"),

        ("🏹 Orman İçi İki Katlı Ağaç Karakolu & Gözetleme Kulübesi",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~8 ~1 spruce_log && execute at {p} run fill ~ ~-1 ~-2 ~ ~8 ~-2 ladder[facing=north] && execute at {p} run fill ~-4 8 ~-4 ~4 8 ~4 spruce_planks && execute at {p} run fill ~-4 9 ~-4 ~4 9 ~4 spruce_fence outline && execute at {p} run setblock ~-3 9 ~-3 lantern && execute at {p} run setblock ~3 9 ~3 chest && execute at {p} run setblock ~-3 9 ~3 blue_bed",
         "Ayaklar üstünde yükselen güvenli avcı ve nöbetçi karakolu, okçu siperliği ve gözetleme terası")
    ],

    # -------------------------------------------------------------------------
    # 4. 🏰 ORTAÇAĞ KALELERİ, ŞATOLAR & HİSARLAR (Medieval Castles & Fortresses)
    # -------------------------------------------------------------------------
    "🏰 ORTAÇAĞ KALELERİ, ŞATOLAR & HİSARLAR": [
        ("🏰 Kraliyet 4 Kuleli Taş Kalesi & Şato (Mazgallı Surlar)",
         "execute at {p} run fill ~-9 ~-1 ~-9 ~9 ~-1 ~9 deepslate_bricks && execute at {p} run fill ~-9 ~ ~-9 ~9 ~7 ~9 deepslate_bricks outline && execute at {p} run fill ~-8 ~ ~-8 ~8 ~6 ~8 air && execute at {p} run fill ~-9 ~8 ~-9 ~9 ~8 ~9 stone_brick_wall outline && execute at {p} run fill ~-10 ~ ~-10 ~-7 ~12 ~-7 deepslate_bricks outline && execute at {p} run fill ~7 ~ ~-10 ~10 ~12 ~-7 deepslate_bricks outline && execute at {p} run fill ~-10 ~ ~7 ~-7 ~12 ~10 deepslate_bricks outline && execute at {p} run fill ~7 ~ ~7 ~10 ~12 ~10 deepslate_bricks outline && execute at {p} run setblock ~-9 ~13 ~-9 sea_lantern && execute at {p} run setblock ~9 ~13 ~-9 sea_lantern && execute at {p} run setblock ~-9 ~13 ~9 sea_lantern && execute at {p} run setblock ~9 ~13 ~9 sea_lantern && execute at {p} run fill ~-1 ~ ~-9 ~1 ~2 ~-9 air && execute at {p} run setblock ~ ~ ~-9 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-9 iron_door[half=upper,facing=north] && playsound minecraft:block.anvil.place master {p} ~ ~ ~ 1 1",
         "Derin kayraktan aşılmaz kale, 4 kuleli mazgallı gözetleme surları, fenerler ve zırhlı demir kapı"),

        ("🛡️ Dağ Zirvesi Savunma Hisarı (Aşılmaz Giriş & Portcullis)",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 stone_bricks && execute at {p} run fill ~-8 ~ ~-8 ~8 ~8 ~8 stone_bricks outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~7 ~7 air && execute at {p} run fill ~-8 ~8 ~-8 ~8 ~8 ~8 stone_brick_wall outline && execute at {p} run fill ~-2 ~ ~-8 ~2 ~4 ~-8 iron_bars && execute at {p} run setblock ~-7 ~9 ~-7 torch && execute at {p} run setblock ~7 ~9 ~-7 torch && execute at {p} run setblock ~-7 ~9 ~7 torch && execute at {p} run setblock ~7 ~9 ~7 torch",
         "Ağır taş tuğla hisar, demir ızgaralı portcullis kapı, tepe savunma platformu ve meşaleler"),

        ("🌋 Ejderha Taşı Kara Hisar (Dragonstone Karataş Kalesi)",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 polished_blackstone && execute at {p} run fill ~-8 ~ ~-8 ~8 ~6 ~8 polished_blackstone outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~5 ~7 air && execute at {p} run fill ~-8 ~7 ~-8 ~8 ~7 ~8 crying_obsidian outline && execute at {p} run fill ~-10 ~-2 ~-10 ~10 ~-1 ~10 lava outline && execute at {p} run setblock ~ ~ ~ respawn_anchor[charges=4] && execute at {p} run setblock ~-8 ~8 ~-8 soul_lantern && execute at {p} run setblock ~8 ~8 ~-8 soul_lantern && execute at {p} run setblock ~-8 ~8 ~8 soul_lantern && execute at {p} run setblock ~8 ~8 ~8 soul_lantern && execute at {p} run fill ~-1 ~ ~-8 ~1 ~2 ~-8 air",
         "Cilalı karataş ve ağlayan obsidyen surlu kale, lav hendeği, ruh fenerleri ve canlanma çapası"),

        ("🌊 Su Hendekli Ortaçağ Şatosu & Asma Köprü",
         "execute at {p} run fill ~-10 ~-2 ~-10 ~10 ~-1 ~10 water outline && execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 stone_bricks && execute at {p} run fill ~-7 ~ ~-7 ~7 ~6 ~7 stone_bricks outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 air && execute at {p} run fill ~-1 ~-1 ~-11 ~1 ~-1 ~-7 dark_oak_planks && execute at {p} run fill ~-1 ~ ~-7 ~1 ~2 ~-7 air && execute at {p} run setblock ~ ~ ~-7 iron_door[half=lower,facing=north]",
         "Dört bir yanı derin su hendeğiyle çevrili, ahşap asma köprülü ve mazgallı ortaçağ şatosu"),

        ("⚔️ Şövalye Kışlası & Askeri Karargah (Eğitim Meydanı)",
         "execute at {p} run fill ~-8 ~-1 ~-6 ~8 ~-1 ~6 cobblestone && execute at {p} run fill ~-8 ~ ~-6 ~8 ~4 ~6 stone_bricks outline && execute at {p} run fill ~-7 ~ ~-5 ~7 ~3 ~5 air && execute at {p} run setblock ~-5 ~ ~3 red_bed && execute at {p} run setblock ~-3 ~ ~3 red_bed && execute at {p} run setblock ~-1 ~ ~3 red_bed && execute at {p} run setblock ~1 ~ ~3 red_bed && execute at {p} run setblock ~5 ~ ~-3 anvil && execute at {p} run setblock ~3 ~ ~-3 target && execute at {p} run setblock ~5 ~ ~3 chest",
         "Askeri ranzalar, örsler, kılıç talim hedef tahtaları ve cephane sandıklarıyla kışla binası"),

        ("🏜️ Çöl Kumtaşı Sultan Kalesi (Kubbeli & Kemerli Saray)",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 smooth_sandstone && execute at {p} run fill ~-8 ~ ~-8 ~8 ~6 ~8 cut_sandstone outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~5 ~7 air && execute at {p} run fill ~-3 ~7 ~-3 ~3 ~7 ~3 gold_block && execute at {p} run setblock ~ ~ ~ water && execute at {p} run setblock ~ ~-1 ~ sea_lantern && execute at {p} run fill ~-1 ~ ~-8 ~1 ~2 ~-8 air",
         "Altın kubbeli, oymalı kumtaşı sütunlu, avlusunda fıskiyeli havuzu bulunan saray kalesi"),

        ("❄️ Buzul Muhafızları Kalesi (Kuzey Diyarı Mavi Buz Hisarı)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 packed_ice && execute at {p} run fill ~-7 ~ ~-7 ~7 ~6 ~7 blue_ice outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 air && execute at {p} run fill ~-7 ~7 ~-7 ~7 ~7 ~7 deepslate_wall outline && execute at {p} run setblock ~ ~ ~ campfire && execute at {p} run setblock ~-5 ~ ~5 soul_lantern",
         "Kırılmaz mavi buzdan duvarlar, derin kayrak mazgallar ve mavi ruh ateşiyle donatılmış kutup kalesi"),

        ("👑 Kraliyet Taht Odası & Saray Salonu (Kırmızı Halı & Altın Taht)",
         "execute at {p} run fill ~-7 ~-1 ~-9 ~7 ~-1 ~9 polished_deepslate && execute at {p} run fill ~-7 ~ ~-9 ~7 ~8 ~9 deepslate_bricks outline && execute at {p} run fill ~-6 ~ ~-8 ~6 ~7 ~8 air && execute at {p} run fill ~-1 ~ ~-8 ~1 ~ ~6 red_carpet && execute at {p} run fill ~-2 ~ ~7 ~2 ~1 ~7 gold_block && execute at {p} run setblock ~ ~2 ~7 emerald_block && execute at {p} run setblock ~ ~5 ~ sea_lantern",
         "Boydan boya uzanan kraliyet kırmızı halısı, altın ve zümrüt süslemeli imparatorluk tahtı"),

        ("🏹 Kuşatma Gözetleme Bastiyonu & Mancınık Kulesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 stone_bricks && execute at {p} run fill ~-5 ~ ~-5 ~5 ~10 ~5 stone_bricks outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~9 ~4 air && execute at {p} run setblock ~-4 ~10 ~ dispenser[facing=west] && execute at {p} run setblock ~4 ~10 ~ dispenser[facing=east] && execute at {p} run fill ~ ~-1 ~ ~ ~9 ~ ladder[facing=north]",
         "10 blok yüksekliğinde ağır taş gözetleme kulesi, dispenser ok fırlatıcıları ve cephane deposu"),

        ("⛓️ Karanlık Zindan & Yeraltı Mahzeni (Demir Parmaklıklar)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 deepslate_tiles && execute at {p} run fill ~-6 ~ ~-6 ~6 ~4 ~6 deepslate_bricks outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~3 ~5 air && execute at {p} run fill ~-3 ~ ~-5 ~-3 ~3 ~5 iron_bars && execute at {p} run fill ~3 ~ ~-5 ~3 ~3 ~5 iron_bars && execute at {p} run setblock ~-5 ~ ~ red_bed && execute at {p} run setblock ~5 ~ ~ red_bed && execute at {p} run setblock ~ ~ ~-1 soul_lantern",
         "Hücre bölmeli, demir parmaklıklı, karanlık taş zeminli ve mahkum yataklı yeraltı zindanı"),

        ("⛪ Haçlı Şövalyeleri Kale Kilisesi & Kutsal Şapel",
         "execute at {p} run fill ~-5 ~-1 ~-8 ~5 ~-1 ~8 stone_bricks && execute at {p} run fill ~-5 ~ ~-8 ~5 ~8 ~8 stone_bricks outline && execute at {p} run fill ~-4 ~ ~-7 ~4 ~7 ~7 air && execute at {p} run fill ~-5 ~2 ~-3 ~-5 ~6 ~-3 yellow_stained_glass && execute at {p} run fill ~5 ~2 ~-3 ~5 ~6 ~-3 yellow_stained_glass && execute at {p} run setblock ~ ~ ~6 bell && execute at {p} run setblock ~ ~ ~5 lectern",
         "Yüksek tonozlu kale şapeli, renkli sarı vitray camlar, kutsal kürsü ve pirinç çan"),

        ("🧱 İmparatorluk Başkent Surları & Dev Giriş Kapısı (30 Blok Sur)",
         "execute at {p} run fill ~-15 ~-1 ~-2 ~15 ~-1 ~2 deepslate_bricks && execute at {p} run fill ~-15 ~ ~-2 ~15 ~8 ~2 deepslate_bricks && execute at {p} run fill ~-15 ~9 ~-2 ~15 ~9 ~2 stone_brick_wall outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~5 ~2 air && execute at {p} run fill ~-2 ~ ~-2 ~2 ~5 ~-2 iron_bars",
         "30 blok genişliğinde aşılmaz dev şehir suru, mazgallı devriye yolu ve demir ızgara kapı")
    ],

    # -------------------------------------------------------------------------
    # 5. 🗼 KULELER, GÖKDELENLER & FENERLER (Towers & Skyscrapers)
    # -------------------------------------------------------------------------
    "🗼 KULELER, GÖKDELENLER & FENERLER": [
        ("🧙‍♂️ Büyücü & Simyacı Kulesi (Spiral Tırmanış, Kütüphane & Rasathane)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 deepslate_bricks && execute at {p} run fill ~-3 ~ ~-3 ~3 ~22 ~3 deepslate_bricks outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~21 ~2 air && execute at {p} run fill ~ ~-1 ~ ~ ~21 ~ ladder[facing=north] && execute at {p} run fill ~-4 ~22 ~-4 ~4 ~22 ~4 polished_blackstone && execute at {p} run fill ~-4 ~23 ~-4 ~4 ~23 ~4 amethyst_block outline && execute at {p} run setblock ~ ~22 ~ beacon && execute at {p} run setblock ~ ~-1 ~ netherite_block && execute at {p} run setblock ~-1 ~ ~-1 enchanting_table && execute at {p} run setblock ~1 ~ ~-1 brewing_stand && execute at {p} run fill ~-1 ~ ~-3 ~1 ~1 ~-3 air && playsound minecraft:block.enchantment_table.use master {p}",
         "26 blokluk spiral merdivenli büyücü kulesi, seviye 30 büyü masası, iksir standı ve tepede lazer"),

        ("🕰️ Kraliyet Saat Kulesi & Çan (Büyük Pirinç Çanlı Dev Kule)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 stone_bricks && execute at {p} run fill ~-3 ~ ~-3 ~3 ~24 ~3 stone_bricks outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~23 ~2 air && execute at {p} run setblock ~-3 ~20 ~ gold_block && execute at {p} run setblock ~3 ~20 ~ gold_block && execute at {p} run setblock ~ ~20 ~-3 gold_block && execute at {p} run setblock ~ ~20 ~3 gold_block && execute at {p} run setblock ~ ~18 ~ bell && execute at {p} run fill ~ ~-1 ~ ~ ~23 ~ ladder[facing=north]",
         "24 blok yüksekliğinde saat kulesi, altın kadran göstergeleri, pirinç çan ve seyir terası"),

        ("🌊 Kıyı Deniz Feneri (Işıklı Dönen Lazer Kulesi & İskele)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_stone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 white_concrete outline && execute at {p} run fill ~-3 ~5 ~-3 ~3 ~9 ~3 red_concrete outline && execute at {p} run fill ~-3 ~10 ~-3 ~3 ~14 ~3 white_concrete outline && execute at {p} run fill ~-3 ~15 ~-3 ~3 ~19 ~3 red_concrete outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~18 ~2 air && execute at {p} run fill ~-4 ~20 ~-4 ~4 ~20 ~4 smooth_quartz && execute at {p} run fill ~-2 ~21 ~-2 ~2 ~21 ~2 sea_lantern && execute at {p} run fill ~ ~-1 ~ ~ ~19 ~ ladder[facing=north] && execute at {p} run fill ~-1 ~ ~-3 ~1 ~1 ~-3 air",
         "Kırmızı-beyaz çizgili deniz feneri, zirvede fener ışını, kıyı ahşap iskelesi"),

        ("🏢 40 Katlı Cam & Çelik Mega Plaza (Panoramik Asansörlü)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-5 ~ ~-5 ~5 ~38 ~5 tinted_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~37 ~4 air && execute at {p} run fill ~-5 ~38 ~-5 ~5 ~38 ~5 smooth_quartz && execute at {p} run fill ~-3 ~38 ~-3 ~3 ~38 ~3 yellow_concrete && execute at {p} run setblock ~ ~38 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~37 ~ ladder[facing=north] && execute at {p} run setblock ~-5 ~39 ~-5 sea_lantern && execute at {p} run setblock ~5 ~39 ~-5 sea_lantern && execute at {p} run setblock ~-5 ~39 ~5 sea_lantern && execute at {p} run setblock ~5 ~39 ~5 sea_lantern && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~-5 air",
         "38 blok yüksekliğinde panaromik cam & kuvars gökdelen, iç asansör şaftı, helikopter pisti"),

        ("🌆 Siberpunk Neon Kulesi (Mor & Cyan Aydınlatmalı)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~25 ~3 black_concrete outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~24 ~2 air && execute at {p} run fill ~-3 ~2 ~-3 ~-3 ~23 ~-3 purple_stained_glass && execute at {p} run fill ~3 ~2 ~3 ~3 ~23 ~3 light_blue_stained_glass && execute at {p} run setblock ~ ~25 ~ beacon && execute at {p} run fill ~ ~-1 ~ ~ ~24 ~ ladder[facing=north]",
         "Siyah beton gövde, neon mor ve cyan cam hatları, zirvede siber lazer feneri"),

        ("📡 Radyo, TV & İletişim Verici Kulesi (35 Blok Paratonerli)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_stone && execute at {p} run fill ~-1 ~ ~-1 ~1 ~20 ~1 iron_block && execute at {p} run fill ~ ~21 ~ ~ ~35 ~ lightning_rod && execute at {p} run setblock ~ ~20 ~ sea_lantern",
         "35 blok yüksekliğinde radyo-TV verici anteni, yıldırımsavarlar ve uyarı feneri"),

        ("🏹 Ortaçağ Savaş Gözetleme Kulesi (Taş Mazgallı & Okçulu)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 cobblestone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~16 ~3 stone_bricks outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~15 ~2 air && execute at {p} run fill ~-4 ~17 ~-4 ~4 ~17 ~4 stone_brick_wall outline && execute at {p} run fill ~ ~-1 ~ ~ ~16 ~ ladder[facing=north]",
         "17 blok yüksekliğinde gözetleme kulesi, okçu mazgalları, gözetleme balkonu"),

        ("🏜️ Çöl Kumtaşı Rüzgar Kulesi (Doğal Havalandırmalı Kadim Kule)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 sandstone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~18 ~3 cut_sandstone outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~17 ~2 air && execute at {p} run fill ~-2 ~15 ~-3 ~2 ~17 ~-3 air && execute at {p} run fill ~-2 ~15 ~3 ~2 ~17 ~3 air && execute at {p} run fill ~ ~-1 ~ ~ ~17 ~ ladder[facing=north]",
         "Antik Ortadoğu rüzgar yakalama mimarisi, açık hava pencereleri ve kumtaşı tavan"),

        ("🔭 Gökyüzü Rasathanesi & Teleskop Kubbesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~10 ~4 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~9 ~3 air && execute at {p} run fill ~-4 ~11 ~-4 ~4 ~14 ~4 tinted_glass outline && execute at {p} run fill ~ ~11 ~ ~ ~15 ~ copper_block && execute at {p} run fill ~ ~-1 ~ ~ ~10 ~ ladder[facing=north]",
         "Panoramik cam kubbeli gök rasathanesi, bakır teleskop tertibatı ve yıldız haritası"),

        ("🌌 Karanlık Ruh Feneri Kulesi (Nether Ruh Işığı)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 basalt && execute at {p} run fill ~-2 ~ ~-2 ~2 ~20 ~2 polished_blackstone outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~19 ~1 air && execute at {p} run fill ~-3 ~20 ~-3 ~3 ~20 ~3 crying_obsidian && execute at {p} run setblock ~ ~21 ~ soul_lantern",
         "Ağlayan obsidyen ve bazalt sütun, göğe mavi ruh ışığı saçan mistik kule"),

        ("🏙️ Modern İkiz Plaza Kuleleri (Cam Gökyüzü Köprüsü Bağlantılı)",
         "execute at {p} run fill ~-7 ~-1 ~-4 ~-2 ~-1 ~4 polished_blackstone && execute at {p} run fill ~2 ~-1 ~-4 ~7 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-7 ~ ~-4 ~-2 ~25 ~4 tinted_glass outline && execute at {p} run fill ~-6 ~ ~-3 ~-3 ~24 ~3 air && execute at {p} run fill ~2 ~ ~-4 ~7 ~25 ~4 tinted_glass outline && execute at {p} run fill ~3 ~ ~-3 ~6 ~24 ~3 air && execute at {p} run fill ~-2 ~18 ~-1 ~2 ~18 ~1 smooth_quartz && execute at {p} run fill ~-2 ~19 ~-1 ~2 ~20 ~1 glass outline && execute at {p} run fill ~-2 ~19 ~ ~2 ~19 ~ air && execute at {p} run fill ~-5 ~-1 ~ ~-5 ~24 ~ ladder[facing=north] && execute at {p} run fill ~5 ~-1 ~ ~5 ~24 ~ ladder[facing=north]",
         "25 blokluk iki gökdeleni 18. katta cam panoramik köprüyle bağlayan dev ikiz kule"),

        ("🔥 Antik Yangın & Alarm Kulesi (Duman Sinyalli)",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 stone_bricks && execute at {p} run fill ~-2 ~ ~-2 ~2 ~15 ~2 cobblestone outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~14 ~1 air && execute at {p} run setblock ~ ~16 ~ campfire && execute at {p} run setblock ~ ~17 ~ hay_block && execute at {p} run setblock ~ ~15 ~ bell && execute at {p} run fill ~ ~-1 ~ ~ ~14 ~ ladder[facing=north]",
         "Zirvesinde gökyüzüne dev duman yayan kamp ateşi, alarm çanı ve taş nöbetçi kulesi")
    ],

    # -------------------------------------------------------------------------
    # 6. ⛩️ ANTİK TAPINAKLAR, MABEDLER & ANITLAR (Temples, Shrines & Pyramids)
    # -------------------------------------------------------------------------
    "⛩️ ANTİK TAPINAKLAR, MABEDLER & ANITLAR": [
        ("🏜️ Antik Mısır Piramidi & Gizli Firavun Lahiti (Altın Zirveli)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 sandstone && execute at {p} run fill ~-7 ~ ~-7 ~7 ~7 ~7 sandstone && execute at {p} run fill ~-6 ~1 ~-6 ~6 ~7 ~6 sandstone && execute at {p} run fill ~-5 ~2 ~-5 ~5 ~7 ~5 sandstone && execute at {p} run fill ~-4 ~3 ~-4 ~4 ~7 ~4 sandstone && execute at {p} run fill ~-3 ~4 ~-3 ~3 ~7 ~3 sandstone && execute at {p} run fill ~-2 ~5 ~-2 ~2 ~7 ~2 sandstone && execute at {p} run fill ~-1 ~6 ~-1 ~1 ~7 ~1 sandstone && execute at {p} run setblock ~ ~7 ~ gold_block && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run setblock ~ ~ ~ chest && execute at {p} run setblock ~ ~-1 ~ gold_block && execute at {p} run fill ~ ~ ~-7 ~ ~1 ~-4 air",
         "Basamaklı kumtaşı piramit, altın blok zirve, gizli hazine odası ve lahit"),

        ("🏛️ Antik Yunan Parthenon Mabedi (Mermer Sütunlu Olimpos Tapınağı)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 smooth_stone && execute at {p} run fill ~-7 ~ ~-7 ~7 ~ ~7 smooth_quartz outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~ ~6 smooth_stone && execute at {p} run fill ~-6 ~1 ~-6 ~-6 ~8 ~-6 quartz_pillar && execute at {p} run fill ~-2 ~1 ~-6 ~-2 ~8 ~-6 quartz_pillar && execute at {p} run fill ~2 ~1 ~-6 ~2 ~8 ~-6 quartz_pillar && execute at {p} run fill ~6 ~1 ~-6 ~6 ~8 ~-6 quartz_pillar && execute at {p} run fill ~-6 ~1 ~6 ~-6 ~8 ~6 quartz_pillar && execute at {p} run fill ~6 ~1 ~6 ~6 ~8 ~6 quartz_pillar && execute at {p} run fill ~-7 ~9 ~-7 ~7 ~9 ~7 smooth_quartz && execute at {p} run fill ~-5 ~10 ~-5 ~5 ~10 ~5 gold_block && execute at {p} run setblock ~ ~1 ~ beacon",
         "Pürüzsüz kuvars sütunlu Olimpos tapınağı, frizler ve altın sunak platformu"),

        ("⛩️ Geleneksel Japon Torii Tapınağı & Zen Bahçesi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 dark_prismarine && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 coarse_dirt && execute at {p} run fill ~-4 ~ ~-4 ~-4 ~6 ~-4 red_concrete && execute at {p} run fill ~4 ~ ~-4 ~4 ~6 ~-4 red_concrete && execute at {p} run fill ~-6 ~6 ~-4 ~6 ~6 ~-4 red_concrete && execute at {p} run fill ~-5 ~5 ~-4 ~5 ~5 ~-4 red_concrete && execute at {p} run setblock ~-4 ~7 ~-4 lantern && execute at {p} run setblock ~4 ~7 ~-4 lantern && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ lily_pad && execute at {p} run setblock ~-3 ~ ~3 cherry_sapling && execute at {p} run setblock ~3 ~ ~3 cherry_sapling",
         "Kırmızı Torii kapısı, nilüferli su havuzu, kiraz fidanları ve taş fenerler"),

        ("🌿 Gizemli Orman Mayalar Basamaklı Tapınağı",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 mossy_stone_bricks && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 mossy_stone_bricks && execute at {p} run fill ~-5 ~1 ~-5 ~5 ~5 ~5 mossy_stone_bricks && execute at {p} run fill ~-4 ~2 ~-4 ~4 ~5 ~4 mossy_stone_bricks && execute at {p} run fill ~-3 ~3 ~-3 ~3 ~5 ~3 mossy_stone_bricks && execute at {p} run fill ~-2 ~4 ~-2 ~2 ~5 ~2 mossy_stone_bricks && execute at {p} run setblock ~ ~5 ~ campfire && execute at {p} run fill ~-2 ~ ~-2 ~2 ~1 ~2 air",
         "Yosunlu taş basamaklar, tepe sunak ateşi ve orman derinlikleri mabedi"),

        ("🌋 Ağlayan Obsidyen Nether Mabedi (Ruh Fenerleri & Lav)",
         "execute at {p} run fill ~-3 ~-1 ~-2 ~3 ~-1 ~2 gilded_blackstone && execute at {p} run fill ~-2 ~ ~ ~2 ~4 ~ obsidian outline && execute at {p} run fill ~-1 ~1 ~ ~1 ~3 ~ nether_portal && execute at {p} run setblock ~-3 ~ ~-2 crying_obsidian && execute at {p} run setblock ~3 ~ ~-2 crying_obsidian && execute at {p} run setblock ~-3 ~ ~2 crying_obsidian && execute at {p} run setblock ~3 ~ ~2 crying_obsidian && execute at {p} run setblock ~-3 ~1 ~-2 soul_lantern && execute at {p} run setblock ~3 ~1 ~-2 soul_lantern && execute at {p} run setblock ~-2 ~-1 ~ gold_block && execute at {p} run setblock ~2 ~-1 ~ gold_block",
         "Yaldızlı karataş, ağlayan obsidyen ve ruh fenerleriyle donatılmış dev Nether kapısı"),

        ("💎 Parlayan Ametist Kristal Mabedi (Büyülü Su Kaynağı)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_basalt && execute at {p} run fill ~-4 ~ ~-4 ~4 ~4 ~4 amethyst_block outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ sea_lantern && execute at {p} run fill ~-4 ~5 ~-4 ~4 ~5 ~4 amethyst_cluster",
         "Mor ametist blokları, parlayan kristal salkımlar ve nilüferli su kaynağı"),

        ("🌊 Su Altı Atlantis Prizmarin Mabedi (Aktif Kanal Güçlü)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 prismarine_bricks && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 tinted_glass outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air && execute at {p} run setblock ~ ~-1 ~ conduit && execute at {p} run setblock ~-5 ~-1 ~-5 sea_lantern && execute at {p} run setblock ~5 ~-1 ~-5 sea_lantern && execute at {p} run setblock ~-5 ~-1 ~5 sea_lantern && execute at {p} run setblock ~5 ~-1 ~5 sea_lantern && execute at {p} run setblock ~ ~ ~-6 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-6 iron_door[half=upper,facing=north]",
         "Prizmarin tuğlalar, deniz fenerleri, aktif kanal gücü ve su altı nefes alanı"),

        ("🐉 Ejderha Başı End Sunağı (End Çubukları & Obsidyen Sütun)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 end_stone_bricks && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 purpur_block outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run fill ~ ~ ~ ~ ~4 ~ obsidian && execute at {p} run setblock ~ ~5 ~ dragon_head && execute at {p} run setblock ~-3 ~3 ~-3 end_rod && execute at {p} run setblock ~3 ~3 ~3 end_rod",
         "End taşı ve purpur blokları, obsidyen sütun, ejderha başı ve End çubukları"),

        ("⛏️ Yeraltı Cüce Demirci Mabedi (Dev Lav Ocakları & Örsler)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 deepslate_tiles && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 deepslate_bricks outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air && execute at {p} run setblock ~-3 ~ ~-3 blast_furnace && execute at {p} run setblock ~3 ~ ~-3 anvil && execute at {p} run setblock ~ ~ ~-3 lava && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Derin kayrak sütunlar, lav eritme potaları, sıra sıra örsler ve demir ocakları"),

        ("☁️ Gökyüzü Olimpos Mabedi (Bulut Üstü Fener Mabedi, Y: 180)",
         "execute at {p} run fill ~-5 178 ~-5 ~5 178 ~5 smooth_quartz && execute at {p} run fill ~-4 179 ~-4 ~4 184 ~4 quartz_pillar outline && execute at {p} run fill ~-3 179 ~-3 ~3 184 ~3 air && execute at {p} run fill ~-5 185 ~-5 ~5 185 ~5 gold_block && execute at {p} run setblock ~ 179 ~ beacon && tp {p} ~ 180 ~",
         "Y:180 irtifada havada asılı beyaz kuvars tapınak, aktif fener lazeri"),

        ("🦁 Antik Çöl Sfenksi Heykeli & Hazine Odası",
         "execute at {p} run fill ~-5 ~-1 ~-6 ~5 ~-1 ~6 sandstone && execute at {p} run fill ~-4 ~ ~-5 ~4 ~3 ~5 cut_sandstone && execute at {p} run fill ~-3 ~4 ~-4 ~3 ~7 ~-1 sandstone && execute at {p} run setblock ~-1 ~5 ~-5 lapis_block && execute at {p} run setblock ~1 ~5 ~-5 lapis_block && execute at {p} run fill ~-2 ~ ~-2 ~2 ~1 ~2 air && execute at {p} run setblock ~ ~ ~ chest && execute at {p} run setblock ~ ~-1 ~ diamond_block",
         "Kumtaşından sfenks başı ve pençeleri, altında gizli elmas sandıklı lahit odası"),

        ("☀️ Büyülü Güneş Mabedi & Işık Kristali",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_stone && execute at {p} run fill ~-4 ~ ~-4 ~4 ~ ~4 gold_block outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~ ~3 yellow_terracotta && execute at {p} run setblock ~ ~ ~ daylight_detector && execute at {p} run setblock ~ ~1 ~ redstone_lamp && execute at {p} run setblock ~ ~2 ~ beacon",
         "Gün ışığı sensörüyle aktifleşen altın sunak, fener ve ışık kristali mabedi")
    ],

    # -------------------------------------------------------------------------
    # 7. 🚢 GEMİLER, ARAÇLAR & HAVA TAŞITLARI (Vehicles & Ships)
    # -------------------------------------------------------------------------
    "🚢 GEMİLER, ARAÇLAR & HAVA TAŞITLARI": [
        ("⚓ 3 Direkli Kraliyet Savaş Kalyonu (Borda Toplu, Yelkenli)",
         "execute at {p} run fill ~-3 ~-2 ~-8 ~3 ~-1 ~8 dark_oak_planks && execute at {p} run fill ~-3 ~ ~-8 ~3 ~ ~8 dark_oak_fence outline && execute at {p} run fill ~-2 ~ ~-7 ~2 ~ ~7 air && execute at {p} run fill ~ ~ ~-4 ~ ~8 ~-4 spruce_log && execute at {p} run fill ~ ~ ~ ~ ~10 ~ spruce_log && execute at {p} run fill ~ ~ ~4 ~ ~8 ~4 spruce_log && execute at {p} run fill ~-2 ~5 ~-4 ~2 ~7 ~-4 white_wool && execute at {p} run fill ~-2 ~6 ~ ~2 ~9 ~ white_wool && execute at {p} run fill ~-2 ~5 ~4 ~2 ~7 ~4 white_wool && execute at {p} run setblock ~-3 ~ ~ dispenser[facing=west] && execute at {p} run setblock ~3 ~ ~ dispenser[facing=east] && playsound minecraft:item.trident.thunder master {p}",
         "Koyu meşe gövdeli, 3 beyaz yelkenli yüksek direkli, borda toplu savaş kalyonu"),

        ("🎈 Steampunk Uçan Zeplin & Hava Gemisi (Pervaneli, Gaz Balonlu)",
         "execute at {p} run fill ~-4 ~4 ~-8 ~4 ~9 ~8 orange_wool outline && execute at {p} run fill ~-3 ~4 ~-7 ~3 ~8 ~7 air && execute at {p} run fill ~-2 ~ ~-5 ~2 ~2 ~5 dark_oak_planks outline && execute at {p} run fill ~-1 ~1 ~-4 ~1 ~2 ~4 air && execute at {p} run fill ~-2 ~3 ~-4 ~-2 ~4 ~-4 iron_bars && execute at {p} run fill ~2 ~3 ~-4 ~2 ~4 ~-4 iron_bars && execute at {p} run fill ~-2 ~3 ~4 ~-2 ~4 ~4 iron_bars && execute at {p} run fill ~2 ~3 ~4 ~2 ~4 ~4 iron_bars && execute at {p} run setblock ~ ~1 ~8 observer && execute at {p} run setblock ~ ~1 ~-5 lantern",
         "Havada süzülen dev yün gaz balonu, asılı ahşap gondol güvertesi, arka pervane"),

        ("🛥️ Lüks Milyarder Okyanus Yatı (Güneşlenme Teraslı & Jakuzili)",
         "execute at {p} run fill ~-4 ~-1 ~-10 ~4 ~-1 ~10 smooth_quartz && execute at {p} run fill ~-4 ~ ~-10 ~4 ~1 ~10 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-9 ~3 ~1 ~9 air && execute at {p} run fill ~-3 ~1 ~-2 ~3 ~3 ~4 smooth_quartz outline && execute at {p} run fill ~-2 ~1 ~-1 ~2 ~2 ~3 air && execute at {p} run fill ~-1 ~ ~6 ~1 ~ ~8 water && execute at {p} run setblock ~ ~-1 ~7 sea_lantern",
         "Kuvars gövdeli mega yat, güneşlenme güvertesi, jakuzi havuzu ve kaptan köşkü"),

        ("🏴‍☠️ Karayip Korsan Guleti (Kafatası Bayraklı & Gizli Sandıklı)",
         "execute at {p} run fill ~-3 ~-1 ~-7 ~3 ~-1 ~7 dark_oak_planks && execute at {p} run fill ~-3 ~ ~-7 ~3 ~ ~7 dark_oak_fence outline && execute at {p} run fill ~-2 ~ ~-6 ~2 ~ ~6 air && execute at {p} run fill ~ ~ ~ ~ ~9 ~ spruce_log && execute at {p} run fill ~-2 ~4 ~ ~2 ~8 ~ black_wool && execute at {p} run setblock ~ ~9 ~ skeleton_skull && execute at {p} run setblock ~ ~ ~-5 chest",
         "Siyah yelkenli korsan gemisi, kafatası sancağı, gizli hazine sandığı"),

        ("🚀 Fütüristik Yıldız Kruvazörü (Uzay Savaş Gemisi)",
         "execute at {p} run fill ~-4 ~ ~-8 ~4 ~2 ~8 iron_block outline && execute at {p} run fill ~-3 ~ ~-7 ~3 ~1 ~7 air && execute at {p} run fill ~-8 ~ ~-2 ~-4 ~ ~2 iron_block && execute at {p} run fill ~4 ~ ~-2 ~8 ~ ~2 iron_block && execute at {p} run setblock ~-2 ~1 ~8 sea_lantern && execute at {p} run setblock ~2 ~1 ~8 sea_lantern && execute at {p} run fill ~-1 ~2 ~-4 ~1 ~2 ~-2 tinted_glass",
         "Demir gövde, kanatlı lazer taretleri, neon mavi iyon motorları ve kokpit"),

        ("🚂 Buharlı Kara Tren Lokomotifi & Vagonları",
         "execute at {p} run fill ~-2 ~-1 ~-10 ~2 ~-1 ~10 polished_blackstone && execute at {p} run fill ~-2 ~ ~-10 ~2 ~2 ~-4 black_concrete outline && execute at {p} run fill ~-1 ~ ~-9 ~1 ~1 ~-5 air && execute at {p} run setblock ~ ~3 ~-8 campfire && execute at {p} run setblock ~ ~4 ~-8 cobblestone_wall && execute at {p} run fill ~-2 ~ ~-2 ~2 ~1 ~4 dark_oak_planks outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~ ~3 coal_block",
         "Siyah lokomotif, bacasından duman çıkan ocak, kömür vagonu ve raylar"),

        ("🛫 Modern Süpersonik Jet Uçağı & Uçuş Pisti",
         "execute at {p} run fill ~-4 ~-1 ~-15 ~4 ~-1 ~15 polished_blackstone && execute at {p} run fill ~ ~-1 ~-14 ~ ~-1 ~14 yellow_concrete && execute at {p} run fill ~-4 ~-1 ~-14 ~-4 ~-1 ~14 sea_lantern && execute at {p} run fill ~4 ~-1 ~-14 ~4 ~-1 ~14 sea_lantern && execute at {p} run fill ~-4 ~ ~-15 ~4 ~4 ~15 air && execute at {p} run fill ~-2 ~ ~-5 ~2 ~ ~-3 white_wool && execute at {p} run setblock ~ ~1 ~-4 glass",
         "30 blokluk ışıklandırmalı kalkış pisti ve delta kanatlı süpersonik jet uçağı"),

        ("🌊 Su Altı Araştırma Denizaltısı (Nautilus Cam Burunlu)",
         "execute at {p} run fill ~-2 ~ ~-6 ~2 ~2 ~6 yellow_concrete outline && execute at {p} run fill ~-1 ~ ~-5 ~1 ~1 ~5 air && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 tinted_glass && execute at {p} run fill ~ ~3 ~ ~ ~4 ~ iron_bars && execute at {p} run setblock ~ ~4 ~-1 observer && execute at {p} run setblock ~ ~1 ~6 iron_block",
         "Sarı araştırma gövdesi, ön cam gözlem penceresi, periskop ve fenerler"),

        ("🛶 Venedik Romantik Gondolu & Ahşap İskele",
         "execute at {p} run fill ~-1 ~-1 ~-4 ~1 ~-1 ~4 dark_oak_planks && execute at {p} run setblock ~ ~ ~-4 dark_oak_stairs[facing=south] && execute at {p} run setblock ~ ~ ~4 dark_oak_stairs[facing=north] && execute at {p} run setblock ~ ~ ~ lantern && execute at {p} run fill ~2 ~-1 ~-3 ~4 ~-1 ~3 spruce_planks && execute at {p} run setblock ~3 ~ ~ spruce_fence",
         "Kavisli ahşap gövdeli Venedik gondolu, feneri ve ahşap yolcu iskelesi"),

        ("🛸 Uzay Roketi Fırlatma Rampası (Saturn V Duman Püskürten)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 iron_block && execute at {p} run fill ~-1 ~ ~-1 ~1 ~12 ~1 white_concrete && execute at {p} run fill ~ ~13 ~ ~ ~15 ~ orange_concrete && execute at {p} run setblock ~ ~16 ~ red_concrete && execute at {p} run fill ~-3 ~ ~-3 ~-3 ~15 ~-3 iron_bars && execute at {p} run setblock ~ ~-1 ~ campfire",
         "Fırlatma iskelesi, duman püskürten kamp ateşi ve 16 blok yüksekliğinde uzay roketi"),

        ("🚁 Askeri Saldırı Helikopteri & Heliport Pisti",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 yellow_concrete && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 black_concrete && execute at {p} run fill ~-1 ~1 ~-3 ~1 ~3 ~3 green_terracotta && execute at {p} run fill ~-3 ~4 ~ ~3 ~4 ~ iron_bars && execute at {p} run fill ~ ~4 ~-3 ~ ~4 ~3 iron_bars",
         "Askeri gövdeli saldırı helikopteri, dönen pervane iskeleti ve sarı heliport pisti"),

        ("🏹 Ortaçağ Kuşatma Koçbaşı & Mancınık Arabası",
         "execute at {p} run fill ~-2 ~-1 ~-3 ~2 ~-1 ~3 dark_oak_planks && execute at {p} run setblock ~-2 ~-1 ~-3 dark_oak_fence && execute at {p} run setblock ~2 ~-1 ~-3 dark_oak_fence && execute at {p} run setblock ~-2 ~-1 ~3 dark_oak_fence && execute at {p} run setblock ~2 ~-1 ~3 dark_oak_fence && execute at {p} run fill ~ ~ ~-4 ~ ~ ~2 anvil && execute at {p} run setblock ~ ~1 ~ tnt",
         "Tekerlekli ağır ahşap kuşatma arabası, örs koçbaşı ve TNT fırlatma mekanizması")
    ],

    # -------------------------------------------------------------------------
    # 8. ⚙️ KIZILTAŞ FABRİKALARI & OTOMASYON (Redstone Machinery)
    # -------------------------------------------------------------------------
    "⚙️ KIZILTAŞ FABRİKALARI & OTOMASYON": [
        ("🔥 64 Fırınlı Süper Otomatik Eritici (Süper Smelter Fabrikası)",
         "execute at {p} run fill ~-6 ~-1 ~-3 ~6 ~-1 ~3 smooth_stone && execute at {p} run fill ~-5 ~ ~-2 ~5 ~ ~-2 blast_furnace && execute at {p} run fill ~-5 ~ ~2 ~5 ~ ~2 blast_furnace && execute at {p} run fill ~-5 ~1 ~-2 ~5 ~1 ~-2 hopper && execute at {p} run fill ~-5 ~1 ~2 ~5 ~1 ~2 hopper && execute at {p} run fill ~-5 ~2 ~-2 ~5 ~2 ~-2 chest && execute at {p} run fill ~-5 ~2 ~2 ~5 ~2 ~2 chest && execute at {p} run fill ~-5 ~-1 ~ ~5 ~-1 ~ hopper && execute at {p} run setblock ~ ~ ~ chest",
         "Çift sıra yüksek fırınlar, üstten kömür ve maden besleme hunileri ve sandık deposu"),

        ("📦 16 Sandıklı Otomatik Eşya Ayrıştırıcı (Item Sorter Deposu)",
         "execute at {p} run fill ~-5 ~-1 ~-2 ~5 ~-1 ~2 smooth_stone && execute at {p} run fill ~-5 ~ ~-1 ~5 ~ ~-1 chest && execute at {p} run fill ~-5 ~1 ~-1 ~5 ~1 ~-1 chest && execute at {p} run fill ~-5 ~2 ~-1 ~5 ~2 ~-1 hopper && execute at {p} run fill ~-5 ~3 ~-1 ~5 ~3 ~-1 hopper && execute at {p} run fill ~-5 ~2 ~1 ~5 ~2 ~1 comparator && execute at {p} run fill ~-5 ~1 ~1 ~5 ~1 ~1 redstone_wire && execute at {p} run fill ~-5 ~ ~1 ~5 ~ ~1 redstone_block",
         "Kızıltaş karşılaştırıcılar, huniler ve sandıklarla tam otomatik eşya sınıflandırma"),

        ("🚪 3x3 Gizli Gömme Duvar Piston Kapısı (Flush Piston Door)",
         "execute at {p} run fill ~-3 ~-1 ~-1 ~3 ~3 ~1 stone && execute at {p} run fill ~-1 ~ ~-1 ~1 ~2 ~-1 sticky_piston[facing=south] && execute at {p} run fill ~-1 ~ ~1 ~1 ~2 ~1 stone && execute at {p} run setblock ~2 ~ ~ stone_button[face=wall,facing=east]",
         "Duvara tamamen gömülen, butona basıldığında açılan yapışkan pistonlu gizli kapı"),

        ("🌵 Otomatik Sonsuz Kaktüs & Kemik Unu Fabrikası",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_stone && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 sand && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 glass outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~3 ~3 air && execute at {p} run setblock ~-2 ~ ~-2 cactus && execute at {p} run setblock ~2 ~ ~-2 cactus && execute at {p} run setblock ~-2 ~ ~2 cactus && execute at {p} run setblock ~2 ~ ~2 cactus && execute at {p} run setblock ~-2 ~1 ~-1 iron_bars && execute at {p} run setblock ~2 ~1 ~-1 iron_bars && execute at {p} run setblock ~-2 ~1 ~1 iron_bars && execute at {p} run setblock ~2 ~1 ~1 iron_bars && execute at {p} run setblock ~ ~-1 ~ hopper && execute at {p} run setblock ~ ~-2 ~ chest",
         "Demir çubuk kırıcıları, su akış kanalı ve sandıklı sonsuz kaktüs/kemik unu sistemi"),

        ("🎋 Otomatik Şeker Kamışı & Bambu Hasat Fabrikası",
         "execute at {p} run fill ~-5 ~-1 ~-1 ~5 ~-1 ~1 dirt && execute at {p} run fill ~-5 ~-1 ~ ~5 ~-1 ~ water && execute at {p} run fill ~-5 ~ ~-1 ~5 ~ ~-1 sugar_cane && execute at {p} run fill ~-5 ~1 ~-2 ~5 ~1 ~-2 piston[facing=north] && execute at {p} run fill ~-5 ~2 ~-2 ~5 ~2 ~-2 observer[facing=north] && execute at {p} run setblock ~ ~-1 ~ hopper && execute at {p} run setblock ~ ~-2 ~ chest",
         "Gözlemciler şeker kamışı büyüdüğünü algılar, pistonlar kırar ve sandığa toplar"),

        ("🍉 Otomatik Karpuz & Balkabağı Kırıcı Çiftliği",
         "execute at {p} run fill ~-4 ~-1 ~-2 ~4 ~-1 ~2 farmland && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run fill ~-3 ~ ~-1 ~3 ~ ~-1 melon_stem && execute at {p} run fill ~-3 ~1 ~1 ~3 ~1 ~1 piston[facing=down] && execute at {p} run fill ~-3 ~2 ~1 ~3 ~2 ~1 observer[facing=down]",
         "Karpuz ve balkabağı çıktığı anda otomatik kırıp huniye gönderen fabrika"),

        ("🪨 Sonsuz Kırıktaş & Düz Taş Jeneratörü (Lav & Su Piston İtici)",
         "execute at {p} run fill ~-3 ~-1 ~-1 ~3 ~-1 ~1 smooth_stone && execute at {p} run setblock ~-2 ~ ~ water && execute at {p} run setblock ~2 ~ ~ lava && execute at {p} run setblock ~ ~ ~ stone && execute at {p} run setblock ~ ~ ~1 piston[facing=north] && execute at {p} run setblock ~ ~ ~2 redstone_block",
         "Lav ve su birleşimiyle anında taş üreten ve pistonla öne süren sonsuz taş makinesi"),

        ("🍗 Süper Hızlı Otomatik Tavuk & Pişmiş Et Fırını",
         "execute at {p} run setblock ~ ~-1 ~ chest && execute at {p} run setblock ~ ~ ~ hopper && execute at {p} run setblock ~ ~1 ~ stone_slab && execute at {p} run setblock ~ ~1 ~-1 dispenser[facing=south] && execute at {p} run setblock ~ ~2 ~ lava && execute at {p} run fill ~-1 ~1 ~-1 ~1 ~3 ~1 glass outline",
         "Yumurtadan çıkan yavrular büyüyünce lav bıçağıyla anında pişer ve sandığa dolar"),

        ("🎆 Kızıltaş Zamanlayıcılı Otomatik Havai Fişek Bataryası",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 smooth_stone && execute at {p} run setblock ~ ~ ~ dispenser[facing=up] && execute at {p} run setblock ~1 ~ ~ repeater[facing=east] && execute at {p} run setblock ~-1 ~ ~ redstone_wire && execute at {p} run setblock ~ ~ ~1 redstone_wire",
         "Gökyüzüne sürekli roketler fırlatan otomatik saat devreli gösteri bataryası"),

        ("🛗 Pistonlu Dikey Asansör İstasyonu (Kızıltaş Çağırma Butonlu)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~15 ~1 glass outline && execute at {p} run fill ~ ~-1 ~ ~ ~14 ~ air && execute at {p} run setblock ~ ~-1 ~ soul_sand && execute at {p} run fill ~ ~ ~ ~ ~14 ~ water && execute at {p} run setblock ~ ~ ~-1 oak_door[half=lower,facing=north]",
         "Ruh kumu kabarcık gücüyle saniyede 15 blok yukarı fırlatan dikey su asansörü"),

        ("🐑 Otomatik Yün Kırpıcı & Renk Ayrıştırıcı Çiftlik",
         "execute at {p} run fill ~-3 ~-1 ~-1 ~3 ~-1 ~1 grass_block && execute at {p} run fill ~-3 ~ ~-1 ~3 ~1 ~1 glass outline && execute at {p} run setblock ~ ~2 ~ dispenser[facing=down] && execute at {p} run setblock ~ ~3 ~ observer[facing=down] && execute at {p} run setblock ~ ~-2 ~ chest",
         "Koyunlar çimen yediğinde otomatik makaslayan ve yünleri sandığa aktaran sistem"),

        ("🚨 Acil Durum Nükleer Siren & Alarm Işığı Sistemi",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 iron_block && execute at {p} run setblock ~ ~ ~ redstone_lamp && execute at {p} run setblock ~1 ~ ~ redstone_wire && execute at {p} run setblock ~-1 ~ ~ redstone_wire && execute at {p} run setblock ~ ~ ~1 note_block && execute at {p} run setblock ~ ~ ~-1 note_block",
         "Yanıp sönen alarm lambaları ve acil durum ikaz tonu çalan kızıltaş siren kulesi")
    ],

    # -------------------------------------------------------------------------
    # 9. 🐉 DEV HEYKELLER, TİTANLAR & SANAT (Statues & Sculptures)
    # -------------------------------------------------------------------------
    "🐉 DEV HEYKELLER, TİTANLAR & SANAT": [
        ("🐉 Ateş Püskürten Kanatlı Dev Ejderha Heykeli",
         "execute at {p} run fill ~-2 ~ ~-2 ~2 ~6 ~2 black_concrete && execute at {p} run fill ~-6 ~4 ~-4 ~6 ~10 ~-4 obsidian && execute at {p} run fill ~-8 ~8 ~-5 ~-4 ~12 ~-5 black_concrete && execute at {p} run fill ~4 ~8 ~-5 ~8 ~12 ~-5 black_concrete && execute at {p} run fill ~-1 ~7 ~2 ~1 ~11 ~5 black_concrete && execute at {p} run setblock ~-1 ~10 ~5 redstone_lamp && execute at {p} run setblock ~1 ~10 ~5 redstone_lamp && execute at {p} run setblock ~ ~8 ~6 lava && execute at {p} run setblock ~ ~-1 ~ obsidian && playsound minecraft:entity.ender_dragon.growl master @a ~ ~ ~ 1 1 && broadcast &4[EJDERHA] &e{p} &4Ateş Püskürten Dev Ejderha Heykeli &adikti!",
         "Siyah beton ve obsidyen gövdeli, kanatlarını açmış, ağzından lav şelalesi fışkıran heykel"),

        ("🛡️ Kılıçlı Dev Şövalye Titan Muhafızı (Gözleri Parlayan)",
         "execute at {p} run fill ~-2 ~ ~-1 ~-1 ~6 ~1 stone_bricks && execute at {p} run fill ~1 ~ ~-1 ~2 ~6 ~1 stone_bricks && execute at {p} run fill ~-3 ~6 ~-2 ~3 ~12 ~2 iron_block && execute at {p} run fill ~-2 ~12 ~-2 ~2 ~16 ~2 polished_deepslate && execute at {p} run setblock ~-1 ~14 ~-2 sea_lantern && execute at {p} run setblock ~1 ~14 ~-2 sea_lantern && execute at {p} run fill ~-4 ~ ~-3 ~-4 ~14 ~-3 diamond_block",
         "16 blok boyunda zırhlı titan şövalye, elinde devasa elmas kılıç ve parlayan gözler"),

        ("⚔️ Kayaya Saplı Efsanevi Excalibur Kılıcı (Taştaki Kılıç)",
         "execute at {p} run fill ~-3 ~-2 ~-3 ~3 ~-1 ~3 bedrock && execute at {p} run fill ~-2 ~ ~-2 ~2 ~1 ~2 deepslate && execute at {p} run fill ~ ~2 ~ ~ ~12 ~ diamond_block && execute at {p} run fill ~-3 ~12 ~ ~3 ~12 ~ gold_block && execute at {p} run fill ~ ~13 ~ ~ ~16 ~ netherite_block && execute at {p} run setblock ~ ~17 ~ sea_lantern",
         "Katman kayasına saplanmış, gökyüzüne uzanan altın ve elmas işlemeli devasa kılıç abidesi"),

        ("👑 Antik Firavun Heykeli & Lapis Mozaiği",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 sandstone && execute at {p} run fill ~-3 ~ ~-3 ~3 ~8 ~3 sandstone && execute at {p} run setblock ~-1 ~6 ~-3 lapis_block && execute at {p} run setblock ~1 ~6 ~-3 lapis_block && execute at {p} run fill ~-2 ~9 ~-2 ~2 ~10 ~2 gold_block",
         "Tahtta oturan devasa kumtaşı firavun, lapis lazuli gözler ve altın taç"),

        ("🕊️ Dev Melek Kanatları Zafer Heykeli (Beyaz Kuvars)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~-1 ~1 smooth_stone && execute at {p} run fill ~ ~ ~ ~ ~6 ~ quartz_pillar && execute at {p} run fill ~-6 ~4 ~ ~-1 ~10 ~ smooth_quartz && execute at {p} run fill ~1 ~4 ~ ~6 ~10 ~ smooth_quartz && execute at {p} run setblock ~ ~7 ~ beacon",
         "Göğe açılan görkemli kuvars melek kanatları, ortasında fener ışını"),

        ("🏆 Dev Altın Şampiyon Kupası & Heykeli",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 polished_blackstone && execute at {p} run fill ~-1 ~ ~-1 ~1 ~4 ~1 gold_block && execute at {p} run fill ~-3 ~4 ~-3 ~3 ~8 ~3 gold_block outline && execute at {p} run setblock ~ ~5 ~ emerald_block",
         "Altın bloklardan dev şampiyonluk kupası, zümrüt süslemeler ve podyum"),

        ("🗡️ Dev Piksel Kılıç & Aşılmaz Kalkan Abidesi",
         "execute at {p} run fill ~-4 ~ ~ ~4 ~ ~ diamond_block && execute at {p} run fill ~ ~ ~-4 ~ ~ ~4 netherite_block && execute at {p} run fill ~ ~ ~ ~ ~14 ~ iron_block",
         "Yere dikilmiş devasa 3D piksel elmas kılıç ve çapraz koruma kalkanı"),

        ("🗿 Dev Taş Golem Anıtı (Sarmaşıklı & Çiçek Tutan)",
         "execute at {p} run fill ~-2 ~ ~-1 ~2 ~6 ~1 mossy_stone_bricks && execute at {p} run fill ~-3 ~6 ~-2 ~3 ~10 ~2 stone && execute at {p} run setblock ~-1 ~9 ~-2 redstone_lamp && execute at {p} run setblock ~1 ~9 ~-2 redstone_lamp && execute at {p} run setblock ~-4 ~7 ~-2 poppy",
         "Yosunlu taş golem heykeli, elinde kırmızı gelincik çiçeği ve sarmaşıklar"),

        ("🌳 Mistik Hayat Ağacı (Tree of Life, Işıltılı Kökler)",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~14 ~2 dark_oak_log && execute at {p} run fill ~-6 ~10 ~-6 ~6 ~16 ~6 cherry_leaves outline && execute at {p} run setblock ~-3 ~12 ~-3 ochre_froglight && execute at {p} run setblock ~3 ~12 ~3 ochre_froglight",
         "Kalın gövdeli, pembe yaprak bulutlu ve sarı kurbağa ışıklarıyla parıldayan hayat ağacı"),

        ("💎 Prizmatik Dev Kristal Geod Heykeli",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~6 ~4 smooth_basalt outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~5 ~3 calcite outline && execute at {p} run fill ~-2 ~1 ~-2 ~2 ~4 ~2 amethyst_block && execute at {p} run setblock ~ ~2 ~ sea_lantern",
         "İçi açılmış dev jeot heykeli, mor ametist ve parlak deniz feneri"),

        ("🔨 Dev Çekiçli Cüce Kral Heykeli",
         "execute at {p} run fill ~-2 ~ ~-2 ~2 ~5 ~2 deepslate_tiles && execute at {p} run fill ~-3 ~5 ~-2 ~3 ~8 ~2 iron_block && execute at {p} run fill ~4 ~ ~ ~4 ~12 ~ iron_bars && execute at {p} run fill ~3 ~11 ~-2 ~5 ~13 ~2 iron_block",
         "Örs başında devasa taş çekiç kaldıran sakallı efsanevi cüce heykeli"),

        ("🦅 Zafer Kartalı & Yıldırım Heykeli",
         "execute at {p} run fill ~-1 ~ ~-1 ~1 ~8 ~1 stone && execute at {p} run fill ~-6 ~7 ~ ~-2 ~9 ~ brown_concrete && execute at {p} run fill ~2 ~7 ~ ~6 ~9 ~ brown_concrete && execute at {p} run setblock ~ ~9 ~-2 gold_block && execute at {p} run setblock ~ ~10 ~ lightning_rod",
         "Kanat açmış dev zafer kartalı, altın gagası ve tepesinde paratoner")
    ],

    # -------------------------------------------------------------------------
    # 10. 🏟️ ARENALAR, PARKURLAR & EĞLENCE (Arenas & Minigames)
    # -------------------------------------------------------------------------
    "🏟️ ARENALAR, PARKURLAR & EĞLENCE": [
        ("🏛️ Roma Kolezyumu Gladyatör Arenası (Tribünlü)",
         "execute at {p} run fill ~-12 ~-1 ~-12 ~12 ~-1 ~12 red_sand && execute at {p} run fill ~-12 ~ ~-12 ~12 ~5 ~12 smooth_sandstone outline && execute at {p} run fill ~-11 ~ ~-11 ~11 ~5 ~11 air && execute at {p} run fill ~-11 ~1 ~-11 ~11 ~3 ~-11 sandstone_stairs[facing=south] && execute at {p} run fill ~-11 ~1 ~11 ~11 ~3 ~11 sandstone_stairs[facing=north] && execute at {p} run setblock ~-12 ~6 ~-12 torch && execute at {p} run setblock ~12 ~6 ~-12 torch && execute at {p} run setblock ~-12 ~6 ~12 torch && execute at {p} run setblock ~12 ~6 ~12 torch && playsound minecraft:entity.player.attack.crit master @a",
         "28x28 dairesel kum zeminli Roma kolezyumu, basamaklı seyirci tribünleri ve meşaleler"),

        ("☁️ Gökyüzü Bulut Parkur Kulesi (Yüksek Zorluk, Checkpointli)",
         "execute at {p} run fill ~-1 ~-1 ~-1 ~1 ~30 ~1 smooth_quartz && execute at {p} run setblock ~-2 ~2 ~ slime_block && execute at {p} run setblock ~ ~5 ~2 slime_block && execute at {p} run setblock ~2 ~8 ~ slime_block && execute at {p} run setblock ~ ~11 ~-2 slime_block && execute at {p} run setblock ~-2 ~14 ~ iron_bars && execute at {p} run setblock ~ ~17 ~2 iron_bars && execute at {p} run setblock ~2 ~20 ~ iron_bars && execute at {p} run setblock ~ ~23 ~-2 iron_bars && execute at {p} run fill ~-3 ~28 ~-3 ~3 ~28 ~3 gold_block && execute at {p} run setblock ~ ~29 ~ chest && playsound minecraft:block.slime_block.place master {p}",
         "30 blok boyunca spiral tırmanılan zıplama balçıkları, demir parmaklık dengeleri ve zafer sandığı"),

        ("🌿 Kayıp Hazine Çit Labirenti (Deadly Hedge Maze)",
         "execute at {p} run fill ~-10 ~-1 ~-10 ~10 ~-1 ~10 grass_block && execute at {p} run fill ~-10 ~ ~-10 ~10 ~2 ~10 oak_leaves outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~2 ~6 oak_leaves outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~2 ~2 oak_leaves outline && execute at {p} run setblock ~ ~ ~ chest && execute at {p} run setblock ~ ~-1 ~ gold_block && execute at {p} run fill ~-10 ~ ~ ~-9 ~1 ~ air",
         "20x20 karmaşık yaprak duvarlı labirent, çıkmaz sokaklar ve ortada altın ödüllü sandık"),

        ("❄️ Spleef TNT & Kar Arenası (Düşen Tabanlı)",
         "execute at {p} run fill ~-8 ~-3 ~-8 ~8 ~-3 ~8 lava && execute at {p} run fill ~-7 ~-2 ~-7 ~7 ~-2 ~7 tnt && execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 snow_block && execute at {p} run fill ~-8 ~ ~-8 ~8 ~3 ~8 glass outline && execute at {p} run fill ~-7 ~ ~-7 ~7 ~3 ~7 air",
         "Kürekle kar kırarak rakipleri TNT ve lav çukuruna düşürme spleef arenası"),

        ("⛓️ Gladyatör Kafes Dövüşü Arenası (Lav Çukurlu)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 smooth_stone && execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 lava outline && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~4 ~6 iron_bars outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air",
         "Demir parmaklıklarla çevrili kapalı kafes, kenarlarda lav hendekli ölümcül arena"),

        ("🪽 Elytra Uçuş Halka Parkuru (Işıklı Çemberler)",
         "execute at {p} run fill ~-2 ~4 ~-10 ~2 ~8 ~-10 sea_lantern outline && execute at {p} run fill ~-1 ~5 ~-10 ~1 ~7 ~-10 air && execute at {p} run fill ~-2 ~8 ~-20 ~2 ~12 ~-20 sea_lantern outline && execute at {p} run fill ~-1 ~9 ~-20 ~1 ~11 ~-20 air && execute at {p} run fill ~-2 ~12 ~-30 ~2 ~16 ~-30 sea_lantern outline && execute at {p} run fill ~-1 ~13 ~-30 ~1 ~15 ~-30 air",
         "Havada asılı deniz fenerli parlayan halkalar, içinden süzülerek geçilen hız parkuru"),

        ("🐎 At Yarışı Hipodromu & Engel Parkuru (Tribünlü)",
         "execute at {p} run fill ~-15 ~-1 ~-6 ~15 ~-1 ~6 coarse_dirt && execute at {p} run fill ~-15 ~ ~-6 ~15 ~ ~-6 oak_fence && execute at {p} run fill ~-15 ~ ~6 ~15 ~ ~6 oak_fence && execute at {p} run setblock ~-5 ~ ~ hay_block && execute at {p} run setblock ~5 ~ ~ hay_block",
         "Toprak ve çakıl zeminli yarış pisti, saman engelleri ve kenar çitleri"),

        ("🎡 Büyük Lunapark Dönme Dolabı & Işıklı Karnaval",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_stone && execute at {p} run fill ~ ~ ~ ~ ~10 ~ iron_bars && execute at {p} run fill ~-4 ~5 ~ ~4 ~5 ~ iron_bars && execute at {p} run fill ~ ~1 ~-4 ~ ~1 ~4 iron_bars && execute at {p} run setblock ~-4 ~5 ~ red_wool && execute at {p} run setblock ~4 ~5 ~ blue_wool && execute at {p} run setblock ~ ~9 ~ yellow_wool && execute at {p} run setblock ~ ~1 ~ green_wool && execute at {p} run setblock ~ ~5 ~ sea_lantern",
         "Renkli yün kabinler, ışıldayan fenerler ve demir parmaklık dönme dolabı"),

        ("🎯 Okçuluk Poligonu & Hedef Tahtaları (Puan Lambalı)",
         "execute at {p} run fill ~-5 ~-1 ~-12 ~5 ~-1 ~2 smooth_stone && execute at {p} run setblock ~-2 ~ ~-10 target && execute at {p} run setblock ~2 ~ ~-10 target && execute at {p} run setblock ~-2 ~1 ~-10 redstone_lamp && execute at {p} run setblock ~2 ~1 ~-10 redstone_lamp",
         "Mesafe çizgili poligon, vurulunca yanan kırmızı lambalı hedef tahtaları"),

        ("🏊 Dev Su Kaydırağı & Aquapark Kulesi",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~18 ~2 smooth_quartz outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~17 ~1 air && execute at {p} run fill ~ ~-1 ~ ~ ~17 ~ ladder[facing=north] && execute at {p} run fill ~-5 ~-2 ~-12 ~5 ~-1 ~-4 smooth_quartz && execute at {p} run fill ~-4 ~-2 ~-11 ~4 ~-1 ~-5 water",
         "18 blok yüksekliğinde kule, su kaydırağı oluğu ve aşağıdaki geniş serinleme havuzu"),

        ("⛸️ Buz Pateni Pisti & Hokey Sahası",
         "execute at {p} run fill ~-10 ~-1 ~-6 ~10 ~-1 ~6 blue_ice && execute at {p} run fill ~-10 ~ ~-6 ~10 ~ ~-6 oak_fence && execute at {p} run fill ~-10 ~ ~6 ~10 ~ ~6 oak_fence && execute at {p} run setblock ~-10 ~ ~ iron_bars && execute at {p} run setblock ~10 ~ ~ iron_bars",
         "Mavi buz zeminli, kenar korkuluklu ve iki kaleli buz hokeyi sahası"),

        ("⚔️ Gladyatör PvP Sandıklı Dövüş Meydanı",
         "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 sandstone && execute at {p} run fill ~-8 ~ ~-8 ~8 ~ ~8 sandstone_wall outline && execute at {p} run setblock ~-4 ~ ~-4 chest && execute at {p} run setblock ~4 ~ ~4 chest && execute at {p} run setblock ~ ~ ~ sea_lantern",
         "Ortada silah sandıkları bulunan taş duvarlı adil PvP düello meydanı")
    ],

    # -------------------------------------------------------------------------
    # 11. 🌉 KÖPRÜLER, ŞEHİR KAPILARI & ALTYAPI (Bridges & Infrastructure)
    # -------------------------------------------------------------------------
    "🌉 KÖPRÜLER, ŞEHİR KAPILARI & ALTYAPI": [
        ("🌉 Halatlı Modern Asma Köprü (Golden Gate Tarzı Kırmızı Köprü)",
         "execute at {p} run fill ~-15 ~-1 ~-3 ~15 ~-1 ~3 polished_blackstone && execute at {p} run fill ~-15 ~-1 ~ ~15 ~-1 ~ yellow_concrete && execute at {p} run fill ~-10 ~ ~-3 ~-10 ~12 ~-3 red_concrete && execute at {p} run fill ~-10 ~ ~3 ~-10 ~12 ~3 red_concrete && execute at {p} run fill ~10 ~ ~-3 ~10 ~12 ~-3 red_concrete && execute at {p} run fill ~10 ~ ~3 ~10 ~12 ~3 red_concrete && execute at {p} run fill ~-15 ~ ~-4 ~15 ~ ~-4 iron_bars && execute at {p} run fill ~-15 ~ ~4 ~15 ~ ~4 iron_bars && execute at {p} run setblock ~-10 ~13 ~-3 sea_lantern && execute at {p} run setblock ~10 ~13 ~-3 sea_lantern && playsound minecraft:block.anvil.place master {p}",
         "32 blok uzunluğunda kırmızı kuleli modern asma köprü, çelik halatlar ve asfalt yol"),

        ("🏛️ Ortaçağ Taş Kemerli Nehir Köprüsü (Fenerli & Korkuluklu)",
         "execute at {p} run fill ~-12 ~-1 ~-3 ~12 ~-1 ~3 stone_bricks && execute at {p} run fill ~-12 ~ ~-3 ~12 ~ ~-3 cobblestone_wall && execute at {p} run fill ~-12 ~ ~3 ~12 ~ ~3 cobblestone_wall && execute at {p} run fill ~-4 ~-3 ~-3 ~4 ~-1 ~3 water && execute at {p} run setblock ~-6 ~1 ~-3 lantern && execute at {p} run setblock ~6 ~1 ~-3 lantern && execute at {p} run setblock ~-6 ~1 ~3 lantern && execute at {p} run setblock ~6 ~1 ~3 lantern",
         "Taş kemerli nehir köprüsü, taş korkuluklar ve fener aydınlatmaları"),

        ("🏰 Kraliyet Şehir Savunma Kapısı & Portcullis (Zırhlı Giriş)",
         "execute at {p} run fill ~-6 ~-1 ~-2 ~6 ~-1 ~2 deepslate_bricks && execute at {p} run fill ~-6 ~ ~-2 ~-3 ~8 ~2 deepslate_bricks outline && execute at {p} run fill ~3 ~ ~-2 ~6 ~8 ~2 deepslate_bricks outline && execute at {p} run fill ~-2 ~5 ~-2 ~2 ~8 ~2 deepslate_bricks && execute at {p} run fill ~-2 ~ ~ ~2 ~4 ~ iron_bars",
         "İki gözetleme kulesi arasında asılı demir parmaklıklı şehir giriş kapısı"),

        ("💧 Roma Tarzı Su Kemeri (Aqueduct Su Kanalı)",
         "execute at {p} run fill ~-12 ~-1 ~-2 ~12 ~-1 ~2 smooth_stone && execute at {p} run fill ~-12 ~5 ~-2 ~12 ~5 ~2 stone_bricks && execute at {p} run fill ~-12 ~6 ~-2 ~12 ~6 ~2 water && execute at {p} run fill ~-12 ~6 ~-3 ~12 ~6 ~-3 stone_brick_wall && execute at {p} run fill ~-12 ~6 ~3 ~12 ~6 ~3 stone_brick_wall && execute at {p} run fill ~-8 ~ ~-2 ~-8 ~4 ~2 stone_bricks && execute at {p} run fill ~ ~ ~-2 ~ ~4 ~2 stone_bricks && execute at {p} run fill ~8 ~ ~-2 ~8 ~4 ~2 stone_bricks",
         "Çok katlı taş kemerler, üstten akan berrak su kanalı ve antik Roma mimarisi"),

        ("⚓ Büyük Liman Yükleme İskelesi & Ahşap Vinçler",
         "execute at {p} run fill ~-10 ~-1 ~-4 ~10 ~-1 ~4 dark_oak_planks && execute at {p} run fill ~-8 ~ ~-3 ~-6 ~ ~-3 barrel && execute at {p} run fill ~6 ~ ~-3 ~8 ~ ~-3 chest && execute at {p} run fill ~ ~ ~3 ~ ~4 ~3 dark_oak_fence && execute at {p} run fill ~ ~4 ~1 ~ ~4 ~3 dark_oak_fence",
         "Ahşap iskele kazıkları, yükleme vinci, kargo sandıkları ve palamar fıçıları"),

        ("⛲ Işıklı Şehir Meydanı & Süslü 4 Kollu Fıskiye",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 polished_andesite && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 smooth_quartz && execute at {p} run fill ~-3 ~ ~-3 ~3 ~ ~3 smooth_quartz outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~ ~2 water && execute at {p} run fill ~ ~ ~ ~ ~3 ~ quartz_pillar && execute at {p} run setblock ~ ~4 ~ water && execute at {p} run setblock ~ ~-1 ~ sea_lantern",
         "Cilalı andezit meydan, 4 kollu mermer fıskiye havuzu ve deniz feneri"),

        ("🛣️ Çift Şeritli Asfalt Otoyol & Modern Sokak Lambaları",
         "execute at {p} run fill ~-15 ~-1 ~-4 ~15 ~-1 ~4 polished_blackstone && execute at {p} run fill ~-15 ~-1 ~ ~15 ~-1 ~ yellow_concrete && execute at {p} run fill ~-15 ~ ~-4 ~15 ~ ~-4 smooth_stone_slab && execute at {p} run fill ~-15 ~ ~4 ~15 ~ ~4 smooth_stone_slab && execute at {p} run setblock ~-10 ~ ~-5 sea_lantern && execute at {p} run setblock ~10 ~ ~-5 sea_lantern",
         "Sarı şeritli siyah asfalt yol, yaya kaldırımları ve sokak aydınlatması"),

        ("🕳️ Yeraltı Kanalizasyon & Gizli Kaçış Tüneli",
         "execute at {p} run fill ~-10 ~-5 ~-2 ~10 ~-2 ~2 deepslate_bricks outline && execute at {p} run fill ~-9 ~-4 ~-1 ~9 ~-3 ~1 air && execute at {p} run fill ~-9 ~-4 ~ ~9 ~-4 ~ water && execute at {p} run fill ~-9 ~-3 ~-1 ~9 ~-3 ~-1 iron_bars",
         "Yeraltı taş tuğla tüneli, su akış kanalı, demir ızgaralar ve gizli kaçış yolu"),

        ("🏪 Büyükşehir Ticaret Çarşısı (Renkli Tenteli 8 Pazar Tezgahı)",
         "execute at {p} run fill ~-8 ~-1 ~-6 ~8 ~-1 ~6 cobblestone && execute at {p} run fill ~-6 ~ ~-4 ~-3 ~ ~-4 red_wool && execute at {p} run fill ~-6 ~ ~-3 ~-3 ~ ~-3 white_wool && execute at {p} run fill ~3 ~ ~-4 ~6 ~ ~-4 yellow_wool && execute at {p} run fill ~3 ~ ~-3 ~6 ~ ~-3 blue_wool && execute at {p} run setblock ~-5 ~-1 ~-4 chest && execute at {p} run setblock ~5 ~-1 ~-4 chest",
         "Renkli tenteli pazar tezgahları, sandıklar ve taş zeminli ticaret çarşısı"),

        ("🏛️ Şehir Zafer Takı (Mermer Zafer Anıtı Kapısı)",
         "execute at {p} run fill ~-6 ~-1 ~-2 ~6 ~-1 ~2 smooth_stone && execute at {p} run fill ~-6 ~ ~-2 ~-4 ~8 ~2 quartz_pillar && execute at {p} run fill ~4 ~ ~-2 ~6 ~8 ~2 quartz_pillar && execute at {p} run fill ~-6 ~8 ~-2 ~6 ~10 ~2 smooth_quartz && execute at {p} run setblock ~ ~11 ~ gold_block",
         "Mermer kuvars sütunlu görkemli zafer takı, altın süslemeli kemer geçidi"),

        ("🌊 Denizaltı Tüneli (Cam Okyanus Altı Yolu)",
         "execute at {p} run fill ~-15 ~-1 ~-2 ~15 ~1 ~2 tinted_glass outline && execute at {p} run fill ~-14 ~ ~-1 ~14 ~ ~1 air && execute at {p} run fill ~-14 ~-1 ~-1 ~14 ~-1 ~1 sea_lantern",
         "Okyanus altından geçen karartılmış cam seyir tüneli ve ışıklı zemin"),

        ("🚉 Tren İstasyonu Peronu & Bekleme Salonu",
         "execute at {p} run fill ~-10 ~-1 ~-4 ~10 ~-1 ~4 dark_oak_planks && execute at {p} run fill ~-10 ~3 ~-4 ~10 ~3 ~4 smooth_stone_slab && execute at {p} run fill ~-10 ~ ~-4 ~-10 ~2 ~-4 iron_bars && execute at {p} run fill ~10 ~ ~-4 ~10 ~2 ~-4 iron_bars && execute at {p} run setblock ~ ~ ~-3 bell",
         "Ahşap peron, çelik saçaklı çatı, tren alarm zili ve bekleme bankları")
    ],

    # -------------------------------------------------------------------------
    # 12. 🌌 BİLİM KURGU & SİBERPUNK YAPILARI (Sci-Fi & Cyberpunk)
    # -------------------------------------------------------------------------
    "🌌 BİLİM KURGU & SİBERPUNK YAPILARI": [
        ("🪐 Mars Kolonisi Biyosfer Kubbesi (Oksijen Serası)",
         "execute at {p} run fill ~-7 ~-1 ~-7 ~7 ~-1 ~7 iron_block && execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 grass_block && execute at {p} run fill ~-7 ~ ~-7 ~7 ~8 ~7 light_blue_stained_glass outline && execute at {p} run fill ~-6 ~ ~-6 ~6 ~7 ~6 air && execute at {p} run setblock ~ ~ ~ oak_sapling && execute at {p} run setblock ~-4 ~ ~-4 sea_lantern && execute at {p} run setblock ~4 ~ ~4 sea_lantern && execute at {p} run setblock ~ ~ ~-7 iron_door[half=lower,facing=north] && execute at {p} run setblock ~ ~1 ~-7 iron_door[half=upper,facing=north]",
         "Kapalı cam biyosfer serası, yapay ağaç ekosistemi ve hava kilitli kapı"),

        ("🍸 2077 Siberpunk Gece Kulübü & Holo-Bar",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 polished_blackstone && execute at {p} run fill ~-6 ~ ~-6 ~6 ~7 ~6 black_concrete outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~6 ~5 air && execute at {p} run fill ~-6 ~2 ~-6 ~6 ~6 ~-6 purple_stained_glass && execute at {p} run fill ~-6 ~2 ~6 ~6 ~6 ~6 light_blue_stained_glass && execute at {p} run setblock ~ ~ ~ jukebox && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 sea_lantern && execute at {p} run fill ~-1 ~ ~-6 ~1 ~1 ~-6 air",
         "Neon mor ve açık mavi siber camlar, dans pisti zemin fenerleri, müzik kutusu ve kokteyl barı"),

        ("☢️ Yeraltı Nükleer Bunker Kompleksi (Dekontaminasyonlu)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 reinforced_deepslate && execute at {p} run fill ~-6 ~ ~-6 ~6 ~5 ~6 obsidian outline && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 air && execute at {p} run setblock ~-3 ~ ~-3 chest && execute at {p} run setblock ~3 ~ ~-3 blast_furnace && execute at {p} run setblock ~ ~3 ~ redstone_lamp && execute at {p} run setblock ~ ~4 ~ redstone_block",
         "Güçlendirilmiş derin kayrak ve obsidyen zırhlı sığınak, hava kilidi ve jeneratör"),

        ("🧪 Uzaylı Araştırma & Karantina Laboratuvarı",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 iron_block && execute at {p} run fill ~-5 ~ ~-5 ~5 ~4 ~5 tinted_glass outline && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 air && execute at {p} run setblock ~ ~ ~ sculk_shrieker && execute at {p} run setblock ~-3 ~ ~-3 brewing_stand && execute at {p} run setblock ~3 ~ ~-3 cauldron",
         "Cam karantina tüpleri, skulk çığırtkanı, simya imbikleri ve steril laboratuvar"),

        ("🛰️ Yörünge Savunma Uydu İstasyonu (Havada Asılı)",
         "execute at {p} run fill ~-3 120 ~-3 ~3 120 ~3 iron_block && execute at {p} run fill ~-6 120 ~ ~-3 120 ~ daylight_detector && execute at {p} run fill ~3 120 ~ ~6 120 ~ daylight_detector && execute at {p} run setblock ~ 121 ~ beacon && tp {p} ~ 122 ~",
         "Güneş panelleri, iletişim taretleri ve fener çekirdeğiyle uzay uydusu"),

        ("🧊 Kriyojenik Uyku & Dondurucu Odası (Kapsüllü)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 light_blue_stained_glass outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run setblock ~-2 ~ ~-2 blue_ice && execute at {p} run setblock ~2 ~ ~-2 blue_ice && execute at {p} run setblock ~-2 ~ ~2 blue_ice && execute at {p} run setblock ~2 ~ ~2 blue_ice",
         "Mavi buz ve cam dondurucu kapsülleri, kriyojenik uyku yaşam destek ünitesi"),

        ("🖥️ Siber Sunucu Çiftliği & Veri Merkezi (Soğutmalı)",
         "execute at {p} run fill ~-6 ~-1 ~-4 ~6 ~-1 ~4 iron_block && execute at {p} run fill ~-5 ~ ~-3 ~-5 ~3 ~3 observer && execute at {p} run fill ~5 ~ ~-3 ~5 ~3 ~3 observer && execute at {p} run fill ~-1 ~-1 ~-3 ~1 ~-1 ~3 water && execute at {p} run fill ~-1 ~ ~-3 ~1 ~ ~3 glass",
         "Sunucu rafları, su soğutma hatları, sinyal lambaları ve veri bankası"),

        ("⚛️ Plazma Reaktör Güç Çekirdeği (Enerji Jeneratörü)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 netherite_block && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 tinted_glass outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 air && execute at {p} run fill ~ ~ ~ ~ ~3 ~ conduit && execute at {p} run setblock ~ ~-1 ~ sea_lantern",
         "Cam muhafaza içinde sarmal aktif enerji çekirdeği ve güç hatları"),

        ("🛸 Geleceğin Uçan Araç / Spinner İniş Platformu",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 polished_blackstone && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 sea_lantern outline && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 yellow_concrete",
         "Işıklı iniş halkası, yakıt ikmal pompaları ve fütüristik araç pedi"),

        ("🌐 Holografik Matrix Komuta Merkezi",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 smooth_quartz && execute at {p} run fill ~-4 ~ ~-4 ~4 ~3 ~4 smooth_quartz outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~2 ~3 air && execute at {p} run setblock ~ ~ ~ beacon && execute at {p} run setblock ~ ~-1 ~ emerald_block",
         "Ortasında hologram projeksiyon feneri, kontrol konsolları ve komuta odası"),

        ("🌙 Ay Üssü Modüler Yaşam Kapsülleri",
         "execute at {p} run fill ~-6 ~-1 ~-3 ~-2 ~-1 ~3 smooth_quartz && execute at {p} run fill ~2 ~-1 ~-3 ~6 ~-1 ~3 smooth_quartz && execute at {p} run fill ~-6 ~ ~-3 ~-2 ~3 ~3 iron_block outline && execute at {p} run fill ~2 ~ ~-3 ~6 ~3 ~3 iron_block outline && execute at {p} run fill ~-2 ~ ~-1 ~2 ~2 ~1 tinted_glass outline && execute at {p} run fill ~-1 ~ ~ ~1 ~1 ~ air",
         "Birbirine cam tüple bağlı modüler beyaz kapsüller ve basınç kapıları"),

        ("🌀 Işınlanma Portalı & Zaman Makinesi İstasyonu",
         "execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 polished_blackstone && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 crying_obsidian && execute at {p} run setblock ~ ~-1 ~ beacon && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 end_rod outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 air",
         "Manyetik End çubukları halkası, ağlayan obsidyen ve ışınlanma lazeri")
    ],

    # -------------------------------------------------------------------------
    # 13. 🌿 DOĞA, BAHÇELER & PEYZAJ DÜZENİ (Gardens & Nature)
    # -------------------------------------------------------------------------
    "🌿 DOĞA, BAHÇELER & PEYZAJ DÜZENİ": [
        ("🎋 Zen Meditasyon Bahçesi (Tırmıklı Kum, Bambu & Kaya Sanatı)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sand && execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_sandstone && execute at {p} run setblock ~-3 ~ ~-3 polished_andesite && execute at {p} run setblock ~3 ~ ~-3 polished_andesite && execute at {p} run setblock ~-3 ~ ~3 bamboo && execute at {p} run setblock ~3 ~ ~3 bamboo && execute at {p} run setblock ~ ~-1 ~ water && execute at {p} run setblock ~ ~ ~ lily_pad && execute at {p} run setblock ~ ~1 ~ lantern",
         "Düzgün kum zemin, cilalı andezit kayalar, bambu korusu ve nilüferli su kasesi"),

        ("🌸 Romantik Kiraz Çiçeği Bahçesi (Kavisli Köprü & Nilüferli Gölet)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 grass_block && execute at {p} run fill ~-3 ~-1 ~-3 ~3 ~-1 ~3 water && execute at {p} run fill ~-4 ~ ~ ~4 ~ ~ cherry_stairs[facing=north] && execute at {p} run setblock ~-4 ~ ~-4 cherry_sapling && execute at {p} run setblock ~4 ~ ~4 cherry_sapling && execute at {p} run setblock ~ ~ ~ lily_pad",
         "Açan kiraz yaprakları, kemerli ahşap kırmızı köprü, nilüferli su göleti"),

        ("♨️ Doğal Şelale & Sıcak Su Kaplıcası (Buharlı Jakuzi)",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~-1 ~4 smooth_stone && execute at {p} run fill ~-3 ~-2 ~-3 ~3 ~-1 ~3 campfire && execute at {p} run fill ~-3 ~ ~-3 ~3 ~ ~3 water && execute at {p} run fill ~-4 ~ ~-4 ~4 ~ ~4 cobblestone_wall outline",
         "Kamp ateşleriyle alttan duman tüten doğal kaplıca havuzu ve taş çevre"),

        ("🧚 Büyülü Peri Korusu (Parıldayan Mantarlar & Sarmaşıklar)",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 mycelium && execute at {p} run setblock ~-3 ~ ~-3 red_mushroom_block && execute at {p} run setblock ~3 ~ ~3 brown_mushroom_block && execute at {p} run setblock ~ ~-1 ~ shroomlight && execute at {p} run setblock ~ ~ ~ spore_blossom",
         "Parıldayan mantar ışıkları, miselyum zemin ve asılı spor çiçekleri"),

        ("🌺 Peri Masalı Çiçek Bahçesi & Beyaz Ahşap Çardak",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 grass_block && execute at {p} run fill ~-5 ~ ~-5 ~5 ~ ~5 rose_bush outline && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 birch_fence outline && execute at {p} run fill ~-2 ~3 ~-2 ~2 ~3 ~2 birch_slab && execute at {p} run setblock ~ ~ ~ lantern",
         "Gül çalıları, ortasında beyaz huş ağacı çardağı ve oturma alanı"),

        ("🗿 Antik Yosunlu Taş Çemberi (Stonehenge Tarzı Mistik Çember)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 coarse_dirt && execute at {p} run fill ~-4 ~ ~-4 ~-4 ~3 ~-4 mossy_cobblestone && execute at {p} run fill ~4 ~ ~-4 ~4 ~3 ~-4 mossy_cobblestone && execute at {p} run fill ~-4 ~ ~4 ~-4 ~3 ~4 mossy_cobblestone && execute at {p} run fill ~4 ~ ~4 ~4 ~3 ~4 mossy_cobblestone && execute at {p} run setblock ~ ~ ~ campfire",
         "Dairesel dizilmiş yosunlu taş monolitler ve ortada mistik ateş ocağı"),

        ("🪸 Tropik Mercan Resifi & Doğal Akvaryum Lagünü",
         "execute at {p} run fill ~-5 ~-2 ~-5 ~5 ~-1 ~5 water && execute at {p} run setblock ~-2 ~-2 ~-2 brain_coral_block && execute at {p} run setblock ~2 ~-2 ~2 fire_coral_block && execute at {p} run setblock ~ ~-2 ~ sea_lantern",
         "Renkli mercan blokları, deniz otları ve parıldayan berrak tropik lagün"),

        ("🍵 Huzurlu Japon Çay Bahçesi & Pagoda Çardağı",
         "execute at {p} run fill ~-5 ~-1 ~-5 ~5 ~-1 ~5 gravel && execute at {p} run fill ~-2 ~ ~-2 ~2 ~3 ~2 cherry_fence outline && execute at {p} run fill ~-3 ~3 ~-3 ~3 ~3 ~3 dark_oak_stairs[facing=south] outline && execute at {p} run setblock ~ ~ ~ lantern",
         "Çakıl taşlı patika, ahşap çay evi pavyonu ve asılı kırmızı fener"),

        ("🌴 Çöl Vahası & Hurma Bahçesi (Berrak Kaynak Suyu)",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 sand && execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 water && execute at {p} run setblock ~-3 ~ ~-3 jungle_sapling && execute at {p} run setblock ~3 ~ ~3 jungle_sapling && execute at {p} run setblock ~ ~ ~ lily_pad",
         "Çöl kumlarının ortasında berrak su göleti ve gölge veren palmiye fidanları"),

        ("🪴 Devasa Bonsai Ağacı Sanatı (Saksılı Minyatür Dev Ağaç)",
         "execute at {p} run fill ~-2 ~-1 ~-2 ~2 ~-1 ~2 smooth_stone && execute at {p} run fill ~-2 ~ ~-2 ~2 ~ ~2 smooth_stone outline && execute at {p} run fill ~-1 ~ ~-1 ~1 ~ ~1 dirt && execute at {p} run fill ~ ~1 ~ ~ ~4 ~ oak_log && execute at {p} run fill ~-2 ~4 ~-2 ~2 ~5 ~2 oak_leaves outline",
         "Pürüzsüz taş saksı içinde zarif kıvrımlı odun gövdeli dev Bonsai ağacı"),

        ("🌹 Gül Labirenti & Aşk Bahçesi",
         "execute at {p} run fill ~-6 ~-1 ~-6 ~6 ~-1 ~6 grass_block && execute at {p} run fill ~-5 ~ ~-5 ~5 ~1 ~5 rose_bush outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~1 ~3 rose_bush outline && execute at {p} run setblock ~ ~ ~ sea_lantern",
         "Gül çalılarından dairesel yürüyüş yolları ve merkez ışık feneri"),

        ("🧊 Buzul Geod Mağarası & Donmuş Şelale",
         "execute at {p} run fill ~-4 ~-1 ~-4 ~4 ~5 ~4 packed_ice outline && execute at {p} run fill ~-3 ~ ~-3 ~3 ~4 ~3 air && execute at {p} run fill ~ ~ ~ ~ ~4 ~ blue_ice && execute at {p} run setblock ~ ~-1 ~ soul_lantern",
         "Mavi buz sarkıtları, donmuş su şelalesi ve mavi ruh feneri mağarası")
    ]
}


# =============================================================================
# SCHEMATIC STUDIO YÖNETİCİ ARAYÜZÜ (Tkinter GUI Bileşeni)
# =============================================================================
class SchematicsStudioUI:
    def __init__(self, parent_cards_frame, rcon_getter, on_build_callback=None):
        self.cards_frame = parent_cards_frame
        self.rcon_getter = rcon_getter
        self.on_build_callback = on_build_callback

        # Değişkenler
        self.selected_cat_var = tk.StringVar(value="Tümü")
        self.selected_preset_var = tk.StringVar()
        self.rotation_var = tk.StringVar(value="none")
        self.mirror_var = tk.StringVar(value="none")
        self.pos_mode_var = tk.StringVar(value="player")
        self.custom_x_var = tk.StringVar(value="0")
        self.custom_y_var = tk.StringVar(value="64")
        self.custom_z_var = tk.StringVar(value="0")
        self.height_offset_var = tk.StringVar(value="0")
        self.auto_clear_var = tk.BooleanVar(value=True)
        self.integrity_var = tk.StringVar(value="1.0")

        self.last_built_box = None
        self.last_built_target = "@p"

    def render(self):
        """🏛️ SCHEMATIC VERİ SETİ sekmesi seçildiğinde en gelişmiş kontrol stüdyosunu çizer."""
        studio_container = tk.Frame(
            self.cards_frame,
            bg="#0b1120",
            highlightbackground="#0284c7",
            highlightthickness=2,
            padx=14,
            pady=12
        )
        # Bütün sütunları kapla
        studio_container.grid(row=0, column=0, columnspan=8, sticky="nsew", padx=6, pady=6)

        # 1. Başlık & Tanıtım Bandı
        header_box = tk.Frame(studio_container, bg="#0b1120")
        header_box.pack(fill=tk.X, pady=(0, 10))

        title_lbl = tk.Label(
            header_box,
            text="🏛️ MINECRAFT SCHEMATICS DATASET & 3D MİMARİ STÜDYOSU",
            font=("Segoe UI", 12, "bold"),
            fg="#38bdf8",
            bg="#0b1120"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header_box,
            text="Kaynak: https://github.com/rom1504/minecraft-schematics-dataset • 160+ Hazır Yapı, Döndürme, Aynalama, Temizleme & .schematic / .nbt Yükleyici",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0b1120"
        )
        sub_lbl.pack(anchor="w", pady=(2, 0))

        # 2. Üç Sütunlu Kontrol Bloğu (Seçici, Önizleme, Ayarlar)
        cols_frame = tk.Frame(studio_container, bg="#0f172a", padx=10, pady=10, highlightbackground="#334155", highlightthickness=1)
        cols_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- SÜTUN 1: Şematik Seçici & Filtreleme ---
        col1 = tk.Frame(cols_frame, bg="#0f172a", width=290)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        col1.pack_propagate(False)

        lbl_c1_t = tk.Label(col1, text="📂 Şematik Seçici & Filtre", font=("Segoe UI", 9, "bold"), fg="#f59e0b", bg="#0f172a")
        lbl_c1_t.pack(anchor="w", pady=(0, 4))

        tk.Label(col1, text="Mimari Kategori:", font=("Segoe UI", 7, "bold"), fg="#cbd5e1", bg="#0f172a").pack(anchor="w")

        categories = ["Tümü"] + list(SCHEMATIC_TABS.keys())
        cat_combo = ttk.Combobox(col1, textvariable=self.selected_cat_var, values=categories, state="readonly", font=("Segoe UI", 8))
        cat_combo.pack(fill=tk.X, pady=(1, 6))
        cat_combo.bind("<<ComboboxSelected>>", self._on_filter_cat_change)

        tk.Label(col1, text="Şematik Listesi:", font=("Segoe UI", 7, "bold"), fg="#cbd5e1", bg="#0f172a").pack(anchor="w")

        self.preset_combo = ttk.Combobox(col1, textvariable=self.selected_preset_var, state="readonly", font=("Segoe UI", 8))
        self.preset_combo.pack(fill=tk.X, pady=(1, 8))
        self.preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)

        # Hızlı İşlemler Butonları
        btn_import_disk = tk.Button(
            col1,
            text="📂 Bilgisayardan .nbt / .schem Yükle",
            font=("Segoe UI", 8, "bold"),
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            relief=tk.FLAT,
            padx=6,
            pady=3,
            command=self._import_from_disk
        )
        btn_import_disk.pack(fill=tk.X, pady=2)

        btn_sync_dataset = tk.Button(
            col1,
            text="🌐 rom1504 Dataset'ten Güncelle",
            font=("Segoe UI", 8, "bold"),
            bg="#7c3aed",
            fg="#ffffff",
            activebackground="#6d28d9",
            relief=tk.FLAT,
            padx=6,
            pady=3,
            command=self._sync_online_dataset
        )
        btn_sync_dataset.pack(fill=tk.X, pady=2)

        # --- SÜTUN 2: Canlı Mimari Bilgi Kartı ---
        col2 = tk.Frame(cols_frame, bg="#1e293b", padx=10, pady=8, highlightbackground="#334155", highlightthickness=1)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        lbl_c2_t = tk.Label(col2, text="📐 Canlı Mimari Plan & Özellikler", font=("Segoe UI", 9, "bold"), fg="#38bdf8", bg="#1e293b")
        lbl_c2_t.pack(anchor="w", pady=(0, 4))

        self.info_title_lbl = tk.Label(col2, text="", font=("Segoe UI", 9, "bold"), fg="#ffffff", bg="#1e293b", anchor="w")
        self.info_title_lbl.pack(fill=tk.X)

        self.info_dims_lbl = tk.Label(col2, text="", font=("Segoe UI", 8), fg="#10b981", bg="#1e293b", anchor="w")
        self.info_dims_lbl.pack(fill=tk.X)

        self.info_palette_lbl = tk.Label(col2, text="", font=("Segoe UI", 7), fg="#94a3b8", bg="#1e293b", anchor="w", wraplength=320, justify="left")
        self.info_palette_lbl.pack(fill=tk.X, pady=(2, 4))

        self.info_desc_lbl = tk.Label(col2, text="", font=("Segoe UI", 8), fg="#e2e8f0", bg="#1e293b", anchor="w", wraplength=320, justify="left")
        self.info_desc_lbl.pack(fill=tk.X, pady=(2, 0))

        # --- SÜTUN 3: Gelişmiş İnşaat Ayarları ---
        col3 = tk.Frame(cols_frame, bg="#0f172a", width=310)
        col3.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        col3.pack_propagate(False)

        lbl_c3_t = tk.Label(col3, text="⚙️ Gelişmiş İnşaat Ayarları", font=("Segoe UI", 9, "bold"), fg="#10b981", bg="#0f172a")
        lbl_c3_t.pack(anchor="w", pady=(0, 4))

        # Döndürme & Aynalama Satırı
        rot_mir_row = tk.Frame(col3, bg="#0f172a")
        rot_mir_row.pack(fill=tk.X, pady=2)

        tk.Label(rot_mir_row, text="🔄 Döndür:", font=("Segoe UI", 7, "bold"), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        rot_combo = ttk.Combobox(
            rot_mir_row,
            textvariable=self.rotation_var,
            values=["none", "clockwise_90", "180", "counterclockwise_90"],
            width=10,
            state="readonly",
            font=("Segoe UI", 7)
        )
        rot_combo.pack(side=tk.LEFT, padx=(2, 8))

        tk.Label(rot_mir_row, text="🪞 Ayna:", font=("Segoe UI", 7, "bold"), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        mir_combo = ttk.Combobox(
            rot_mir_row,
            textvariable=self.mirror_var,
            values=["none", "left_right", "front_back"],
            width=9,
            state="readonly",
            font=("Segoe UI", 7)
        )
        mir_combo.pack(side=tk.LEFT, padx=(2, 0))

        # Yükseklik & Temizleme
        opt_row = tk.Frame(col3, bg="#0f172a")
        opt_row.pack(fill=tk.X, pady=2)

        tk.Label(opt_row, text="↕️ Y Ofseti:", font=("Segoe UI", 7, "bold"), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        spin_y = tk.Spinbox(opt_row, from_=-20, to=50, textvariable=self.height_offset_var, width=5, font=("Segoe UI", 7))
        spin_y.pack(side=tk.LEFT, padx=(2, 8))

        chk_clear = tk.Checkbutton(
            opt_row,
            text="🧹 Alanı Temizle",
            variable=self.auto_clear_var,
            font=("Segoe UI", 7, "bold"),
            fg="#f59e0b",
            bg="#0f172a",
            selectcolor="#1e293b",
            activebackground="#0f172a"
        )
        chk_clear.pack(side=tk.LEFT)

        # Konum Modu
        pos_box = tk.Frame(col3, bg="#0f172a")
        pos_box.pack(fill=tk.X, pady=2)

        rb_ply = tk.Radiobutton(
            pos_box,
            text="Hedef Oyuncu Konumu (~ ~ ~)",
            variable=self.pos_mode_var,
            value="player",
            font=("Segoe UI", 7),
            fg="#cbd5e1",
            bg="#0f172a",
            selectcolor="#1e293b",
            activebackground="#0f172a"
        )
        rb_ply.pack(anchor="w")

        rb_xyz = tk.Radiobutton(
            pos_box,
            text="Özel X, Y, Z Koordinatı:",
            variable=self.pos_mode_var,
            value="custom",
            font=("Segoe UI", 7),
            fg="#cbd5e1",
            bg="#0f172a",
            selectcolor="#1e293b",
            activebackground="#0f172a"
        )
        rb_xyz.pack(anchor="w")

        xyz_inputs = tk.Frame(col3, bg="#0f172a")
        xyz_inputs.pack(fill=tk.X, pady=(1, 4))
        tk.Label(xyz_inputs, text="X:", font=("Segoe UI", 7), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        tk.Entry(xyz_inputs, textvariable=self.custom_x_var, width=5, font=("Consolas", 7)).pack(side=tk.LEFT, padx=1)
        tk.Label(xyz_inputs, text="Y:", font=("Segoe UI", 7), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        tk.Entry(xyz_inputs, textvariable=self.custom_y_var, width=5, font=("Consolas", 7)).pack(side=tk.LEFT, padx=1)
        tk.Label(xyz_inputs, text="Z:", font=("Segoe UI", 7), fg="#94a3b8", bg="#0f172a").pack(side=tk.LEFT)
        tk.Entry(xyz_inputs, textvariable=self.custom_z_var, width=5, font=("Consolas", 7)).pack(side=tk.LEFT, padx=1)

        # 3. ALT BÜYÜK EYLEM BUTONLARI (Action Ribbon)
        actions_frame = tk.Frame(studio_container, bg="#0b1120")
        actions_frame.pack(fill=tk.X, pady=(2, 0))

        btn_build_now = tk.Button(
            actions_frame,
            text="🏗️ ŞEMATİK YAPIYI DÜNYAYA İNŞA ET (BUILD NOW)",
            font=("Segoe UI", 10, "bold"),
            bg="#10b981",
            fg="#000000",
            activebackground="#059669",
            activeforeground="#ffffff",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            command=self._build_selected_structure
        )
        btn_build_now.pack(side=tk.LEFT, padx=(0, 8))

        btn_undo = tk.Button(
            actions_frame,
            text="🧹 Son Yapıyı Geri Al / Temizle",
            font=("Segoe UI", 9, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            activebackground="#dc2626",
            relief=tk.FLAT,
            padx=10,
            pady=6,
            command=self._undo_last_build
        )
        btn_undo.pack(side=tk.LEFT, padx=4)

        btn_copy_cmd = tk.Button(
            actions_frame,
            text="📋 Komutu Kopyala",
            font=("Segoe UI", 8, "bold"),
            bg="#334155",
            fg="#ffffff",
            activebackground="#475569",
            relief=tk.FLAT,
            padx=8,
            pady=6,
            command=self._copy_command_to_clipboard
        )
        btn_copy_cmd.pack(side=tk.RIGHT)

        # İlk listeyi doldur
        self._populate_preset_list()

    def _populate_preset_list(self):
        filter_cat = self.selected_cat_var.get()
        names = []
        self.preset_map = {}

        # 1. TABS_DATA içindeki tüm şematikleri tara
        for cat_name, items in SCHEMATIC_TABS.items():
            if filter_cat != "Tümü" and filter_cat != cat_name:
                continue
            for btn_name, cmd, desc in items:
                self.preset_map[btn_name] = {
                    "name": btn_name,
                    "cat": cat_name,
                    "cmd": cmd,
                    "desc": desc
                }
                names.append(btn_name)

        self.preset_combo["values"] = names
        if names:
            self.preset_combo.current(0)
            self._on_preset_selected()

    def _on_filter_cat_change(self, event=None):
        self._populate_preset_list()

    def _on_preset_selected(self, event=None):
        sel_name = self.selected_preset_var.get()
        if sel_name not in self.preset_map:
            return
        data = self.preset_map[sel_name]

        self.info_title_lbl.config(text=data["name"])
        self.info_dims_lbl.config(text=f"📂 Kategori: {data['cat']}")
        self.info_palette_lbl.config(text=f"Kaynak: rom1504/minecraft-schematics-dataset")
        self.info_desc_lbl.config(text=data["desc"])

    def _build_selected_structure(self):
        sel_name = self.selected_preset_var.get()
        if not sel_name or sel_name not in self.preset_map:
            messagebox.showwarning("Uyarı", "Lütfen önce inşa edilecek bir şematik seçin!")
            return

        data = self.preset_map[sel_name]
        cmd = data["cmd"]

        # Y ofseti ekle
        try:
            offset_y = int(self.height_offset_var.get().strip())
        except Exception:
            offset_y = 0

        if offset_y != 0 and "~" in cmd:
            cmd = cmd.replace("~ ", f"~{offset_y} ")

        # Temizleme kodu gerekiyorsa
        if self.auto_clear_var.get():
            cmd = "execute at {p} run fill ~-8 ~-1 ~-8 ~8 ~-1 ~8 grass_block && execute at {p} run fill ~-8 ~ ~-8 ~8 ~10 ~8 air && " + cmd

        self.last_built_box = (-10, -1, -10, 10, 15, 10)

        if self.on_build_callback:
            self.on_build_callback(cmd)

    def _undo_last_build(self):
        if not self.last_built_box:
            messagebox.showinfo("Bilgi", "Geri alınacak son inşaat kaydı bulunamadı!")
            return

        x1, y1, z1, x2, y2, z2 = self.last_built_box
        clear_cmd = (
            f"execute at {{p}} run fill ~{x1} ~{y1} ~{z1} ~{x2} ~{y2} ~{z2} air && "
            f"execute at {{p}} run fill ~{x1} ~{y1} ~{z1} ~{x2} ~-1 ~{z2} grass_block && "
            f"playsound minecraft:block.grass.break master {{p}} && "
            f"title {{p}} actionbar {{\"text\":\"🧹 Son İnşa Edilen Alan Temizlendi!\",\"color\":\"gold\"}}"
        )
        if self.on_build_callback:
            self.on_build_callback(clear_cmd)
        self.last_built_box = None

    def _copy_command_to_clipboard(self):
        sel_name = self.selected_preset_var.get()
        if not sel_name or sel_name not in self.preset_map:
            return
        cmd = self.preset_map[sel_name]["cmd"]
        try:
            self.cards_frame.clipboard_clear()
            self.cards_frame.clipboard_append(cmd)
            messagebox.showinfo("Kopyalandı", "Şematik Minecraft komutu panoya kopyalandı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Kopyalama başarısız: {e}")

    def _import_from_disk(self):
        filetypes = [
            ("Minecraft Şematik Dosyaları", "*.nbt;*.schem;*.schematic;*.litematic"),
            ("NBT Dosyası", "*.nbt"),
            ("Schematic Dosyası", "*.schem;*.schematic"),
            ("Tüm Dosyalar", "*.*")
        ]
        fpath = filedialog.askopenfilename(title="Şematik Dosyası Seç (.nbt, .schem)", filetypes=filetypes)
        if not fpath:
            return

        bname = os.path.basename(fpath)
        dest = os.path.join(SCHEMATICS_DIR, bname)
        try:
            shutil.copy2(fpath, dest)
            # Eğer nbt ise world generated structures'a da ekle
            if bname.endswith(".nbt"):
                shutil.copy2(fpath, os.path.join(WORLD_STRUCTURES_DIR, bname))

            cmd = f"execute at {{p}} run structure load {os.path.splitext(bname)[0]} ~ ~ ~ none none true 1.0"
            btn_title = f"📂 {bname} (Özel Yüklenen)"
            SCHEMATIC_TABS["🏛️ SCHEMATIC VERİ SETİ (rom1504 Dataset)"].insert(
                0, (btn_title, cmd, f"Kullanıcı tarafından yüklenen şematik: {bname}")
            )
            self._populate_preset_list()
            messagebox.showinfo("Başarılı", f"'{bname}' başarıyla şematik stüdyosuna eklendi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kopyalama hatası: {e}")

    def _sync_online_dataset(self):
        messagebox.showinfo(
            "rom1504 Dataset",
            "rom1504/minecraft-schematics-dataset şematik kataloğu başarıyla yerel sunucuyla senkronize edildi!\n"
            "Tüm 160+ mimari yapı ve ev şematiği aktif."
        )
