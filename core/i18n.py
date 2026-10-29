# -*- coding: utf-8 -*-
"""
Internationalization (i18n) Engine - Bilingual Support (TR / EN)
Provides comprehensive Turkish and English localization for all UI components,
banners, installer actions, admin panel commands, and AI wizard modules.
"""

import json
import os
import sys

class I18n:
    _instance = None
    _current_lang = "tr"
    _listeners = []

    TRANSLATIONS = {
        "tr": {
            # App General
            "app_title": "Auto Minecraft Server Maker Pro",
            "app_subtitle": "Otonom Minecraft Sunucu Kurucu & AI Mühendislik İstasyonu",
            "lang_name": "Türkçe",
            "lang_switch_tooltip": "Change language to English",
            
            # Sidebar Navigation
            "nav_installer": "🚀 Kurulum & Başlatıcı",
            "nav_ai_engineer": "🤖 AI Mühendis Pro",
            "nav_admin_panel": "👑 Admin Kontrol Paneli",
            "nav_tunnel": "🌐 Tünel & Dış Bağlantı",
            "nav_plugins": "🧩 Eklenti & Mod Merkezi",
            "nav_backup": "💾 Yedekleme Yöneticisi",
            "nav_properties": "⚙️ Sunucu Ayarları",
            "nav_settings": "🔧 Sistem & AI API",
            "nav_ai_wizard": "⚡ AI Otonom Kurulum",

            # Top Banner (Rakamlara Bak)
            "banner_flavors": "10+ SUNUCU TÜRÜ",
            "banner_flavors_sub": "Paper • Purpur • Fabric • Forge...",
            "banner_versions": "1.0 ➔ 1.21.4+",
            "banner_versions_sub": "Tüm Sürümler (Eskiden Yeniye)",
            "banner_ai": "12 AI MOTORU",
            "banner_ai_sub": "Ollama, Groq, DeepSeek & Yerel",
            "banner_admin": "380+ ADMİN KOMUTU",
            "banner_admin_sub": "300+ Blok • 16 Kategori Sekmesi",

            # Server Installer Card
            "installer_title": "🚀 TEK TIKLA SUNUCU KURUCU",
            "installer_flavor_label": "⚙️ Sunucu Yazılımı (10+ Tür):",
            "installer_version_label": "📌 Minecraft Sürümü (En Eskiden En Yeniye):",
            "installer_custom_version": "Veya Özel Sürüm Girin:",
            "installer_java_status": "☕ Java Uyumluluk Durumu:",
            "installer_java_btn": "⚡ Java İndir",
            "installer_ram_label": "💾 Bellek (RAM) Dağılımı:",
            "installer_ram_min": "Min:",
            "installer_ram_max": "Max:",
            "installer_crossplay": "📱 Mobil & Konsol Crossplay (Geyser + Floodgate)",
            "installer_btn_install": "⚡ TEK TIKLA İNDİR & KUR",
            "installer_btn_start": "▶️ Başlat",
            "installer_btn_stop": "⏹️ Durdur",
            "installer_status_running": "● SUNUCU ÇALIŞIYOR (Port: 25565)",
            "installer_status_stopped": "● SUNUCU KAPALI",
            "installer_status_starting": "● SUNUCU BAŞLATILIYOR...",
            "installer_terminal_clear": "Temizle",
            "installer_terminal_doctor": "🩺 AI Çökme Doktoru",

            # AI Autonomous Setup Wizard
            "ai_wizard_title": "🤖 AI OTONOM KURULUM ASİSTANI",
            "ai_wizard_desc": "Ne tür bir sunucu kurmak istediğinizi yazın, AI en uygun sürüm, tür, RAM ve eklentileri belirlesin ve kursun!",
            "ai_wizard_placeholder": "Örnek: Arkadaşlarımla 1.20.4 hafif modlu Fabric oynamak istiyorum, 4GB RAM ver...",
            "ai_wizard_btn_run": "⚡ AI İle Otomatik Kurulumu Başlat",
            "ai_wizard_chip_1": "🚀 1.20.4 Arkadaşlarla Vanilla+ (Hafif & Hızlı)",
            "ai_wizard_chip_2": "📱 1.21.1 Bedrock & Java Crossplay (Mobil Uyumlu)",
            "ai_wizard_chip_3": "⚔️ 1.16.5 PvP & Klan Sunucusu (EssentialsX)",
            "ai_wizard_chip_4": "🧵 1.20.1 Fabric Modlu Sunucu (Performans Odaklı)",
            "ai_wizard_chip_5": "🏰 1.8.9 Klasik PvP & Bedwars Sunucusu",
            "ai_wizard_analyzing": "🤖 AI sunucu planını analiz ediyor...",
            "ai_wizard_plan_ready": "📋 AI Kurulum Planı Hazırlandı:",

            # Admin Panel
            "admin_title": "👑 MASTER YÖNETİCİ KONTROL PANELİ",
            "admin_target_label": "🎯 Hedef Oyuncu:",
            "admin_target_all": "@a (Herkes)",
            "admin_target_nearest": "@p (En Yakın)",
            "admin_search_placeholder": "🔍 380+ Komut ve Blok İçinde Anında Ara...",
            "admin_tab_quick": "👑 Hızlı Yönetim",
            "admin_tab_blocks": "🧱 Blok Dağıtım Merkezi",
            "admin_tab_shulker": "📦 Kombine Sandıklar",
            "admin_tab_troll": "🤡 Troll & Eğlence",
            "admin_tab_master": "⚡ Efsanevi Master Set",
            "admin_tab_enchanter": "🪄 Büyücü & İksir",
            "admin_tab_fill": "🪄 Hızlı İnşa & Fill",
            "admin_tab_illegal": "🧱 İllegal Bloklar",
            "admin_tab_ores": "💎 Madenler & Cevher",
            "admin_tab_build": "🏗️ Mimari & İnşaat",
            "admin_tab_wood": "🪵 Tüm Ağaçlar",
            "admin_tab_concrete": "🌈 Beton & Renkler",
            "admin_tab_light": "💡 Işık Blokları",
            "admin_tab_redstone": "⚙️ Kızıltaş & TNT",
            "admin_tab_mobs": "🥚 Canavarlar & Mob",
            "admin_tab_teleport": "🗺️ Işınlanma & Dünya",

            # Common Dialogs & Messages
            "msg_installing": "Kurulum Başlatıldı",
            "msg_install_success": "Minecraft sunucusu başarıyla kuruldu ve yapılandırıldı!",
            "msg_install_error": "Kurulum sırasında bir hata oluştu.",
            "msg_server_started": "Sunucu arka planda başarıyla başlatıldı.",
            "msg_server_stopped": "Sunucu durduruldu.",
            "msg_rcon_success": "Komut RCON üzerinden başarıyla gönderildi: {cmd}",
            "msg_copied": "Panoya Kopyalandı!"
        },
        "en": {
            # App General
            "app_title": "Auto Minecraft Server Maker Pro",
            "app_subtitle": "Autonomous Minecraft Server Installer & AI Engineering Station",
            "lang_name": "English",
            "lang_switch_tooltip": "Dili Türkçe'ye çevir",

            # Sidebar Navigation
            "nav_installer": "🚀 Installer & Launcher",
            "nav_ai_engineer": "🤖 AI Engineer Pro",
            "nav_admin_panel": "👑 Master Admin Panel",
            "nav_tunnel": "🌐 Tunnel & Port Forward",
            "nav_plugins": "🧩 Plugin & Mod Hub",
            "nav_backup": "💾 Backup Manager",
            "nav_properties": "⚙️ Server Settings",
            "nav_settings": "🔧 System & AI API",
            "nav_ai_wizard": "⚡ AI Autonomous Setup",

            # Top Banner
            "banner_flavors": "10+ SERVER FLAVORS",
            "banner_flavors_sub": "Paper • Purpur • Fabric • Forge...",
            "banner_versions": "1.0 ➔ 1.21.4+",
            "banner_versions_sub": "All Versions (Legacy to Modern)",
            "banner_ai": "12 AI ENGINES",
            "banner_ai_sub": "Ollama, Groq, DeepSeek & Local",
            "banner_admin": "380+ ADMIN ACTIONS",
            "banner_admin_sub": "300+ Blocks • 16 Dedicated Tabs",

            # Server Installer Card
            "installer_title": "🚀 1-CLICK SERVER INSTALLER",
            "installer_flavor_label": "⚙️ Server Software (10+ Flavors):",
            "installer_version_label": "📌 Minecraft Version (Oldest to Newest):",
            "installer_custom_version": "Or Type Custom Version:",
            "installer_java_status": "☕ Java Compatibility Status:",
            "installer_java_btn": "⚡ Download Java",
            "installer_ram_label": "💾 Memory (RAM) Allocation:",
            "installer_ram_min": "Min:",
            "installer_ram_max": "Max:",
            "installer_crossplay": "📱 Mobile & Console Crossplay (Geyser + Floodgate)",
            "installer_btn_install": "⚡ 1-CLICK DOWNLOAD & SETUP",
            "installer_btn_start": "▶️ Start Server",
            "installer_btn_stop": "⏹️ Stop Server",
            "installer_status_running": "● SERVER RUNNING (Port: 25565)",
            "installer_status_stopped": "● SERVER STOPPED",
            "installer_status_starting": "● SERVER STARTING...",
            "installer_terminal_clear": "Clear",
            "installer_terminal_doctor": "🩺 AI Crash Doctor",

            # AI Autonomous Setup Wizard
            "ai_wizard_title": "🤖 AI AUTONOMOUS SETUP WIZARD",
            "ai_wizard_desc": "Describe the server you want to create, and AI will automatically choose the flavor, version, RAM, and plugins!",
            "ai_wizard_placeholder": "E.g.: Setup a 1.20.4 lightweight Fabric server for playing with friends, 4GB RAM...",
            "ai_wizard_btn_run": "⚡ Run AI Autonomous Setup",
            "ai_wizard_chip_1": "🚀 1.20.4 Vanilla+ for Friends (Lightweight)",
            "ai_wizard_chip_2": "📱 1.21.1 Bedrock & Java Crossplay (Mobile Ready)",
            "ai_wizard_chip_3": "⚔️ 1.16.5 PvP & Clan Server (EssentialsX)",
            "ai_wizard_chip_4": "🧵 1.20.1 Fabric Modded Server (Performance)",
            "ai_wizard_chip_5": "🏰 1.8.9 Classic PvP & Bedwars Server",
            "ai_wizard_analyzing": "🤖 AI is analyzing server architecture plan...",
            "ai_wizard_plan_ready": "📋 AI Setup Architecture Plan Ready:",

            # Admin Panel
            "admin_title": "👑 MASTER ADMIN CONTROL PANEL",
            "admin_target_label": "🎯 Target Player:",
            "admin_target_all": "@a (All Players)",
            "admin_target_nearest": "@p (Nearest Player)",
            "admin_search_placeholder": "🔍 Search across 380+ commands and blocks instantly...",
            "admin_tab_quick": "👑 Quick Admin",
            "admin_tab_blocks": "🧱 Universal Block Hub",
            "admin_tab_shulker": "📦 Themed Shulker Kits",
            "admin_tab_troll": "🤡 Troll & Fun",
            "admin_tab_master": "⚡ Legendary Master Gear",
            "admin_tab_enchanter": "🪄 Enchanter & Potions",
            "admin_tab_fill": "🪄 Quick Fill & Build",
            "admin_tab_illegal": "🧱 Illegal & Admin Blocks",
            "admin_tab_ores": "💎 Precious Ores",
            "admin_tab_build": "🏗️ Architecture Blocks",
            "admin_tab_wood": "🪵 All Wood & Logs",
            "admin_tab_concrete": "🌈 Concrete & Colors",
            "admin_tab_light": "💡 Light Blocks",
            "admin_tab_redstone": "⚙️ Redstone & TNT",
            "admin_tab_mobs": "🥚 Monster & Mob Eggs",
            "admin_tab_teleport": "🗺️ Teleport & World",

            # Common Dialogs & Messages
            "msg_installing": "Installation Started",
            "msg_install_success": "Minecraft server was successfully downloaded and configured!",
            "msg_install_error": "An error occurred during installation.",
            "msg_server_started": "Server was successfully launched in background.",
            "msg_server_stopped": "Server stopped.",
            "msg_rcon_success": "Command sent via RCON: {cmd}",
            "msg_copied": "Copied to Clipboard!"
        }
    }

    @classmethod
    def set_language(cls, lang_code):
        if lang_code in cls.TRANSLATIONS:
            cls._current_lang = lang_code
            for callback in cls._listeners:
                try:
                    callback(lang_code)
                except Exception:
                    pass

    @classmethod
    def get_language(cls):
        return cls._current_lang

    @classmethod
    def t(cls, key, **kwargs):
        """Translate key for current active language."""
        lang_dict = cls.TRANSLATIONS.get(cls._current_lang, cls.TRANSLATIONS["tr"])
        text = lang_dict.get(key)
        if text is None:
            # Fallback to English, then key itself
            text = cls.TRANSLATIONS["en"].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    @classmethod
    def register_listener(cls, callback):
        """Register a UI refresh callback on language change."""
        if callback not in cls._listeners:
            cls._listeners.append(callback)

    @classmethod
    def unregister_listener(cls, callback):
        if callback in cls._listeners:
            cls._listeners.remove(callback)

def t(key, **kwargs):
    return I18n.t(key, **kwargs)
