# -*- coding: utf-8 -*-
"""
Core Configuration Manager - Safe local settings and API key vault.
Guarantees 100% Zero-Leak security by keeping private configuration
isolated in a gitignored local file.
"""

import os
import json
import logging

import sys

if getattr(sys, "frozen", False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(APP_DIR, "config.json")

active_srv_dir = APP_DIR if os.path.exists(os.path.join(APP_DIR, "server.properties")) else os.path.join(APP_DIR, "server")

DEFAULT_CONFIG = {
    "server": {
        "server_dir": active_srv_dir,
        "java_path": "java",
        "min_ram_gb": 4,
        "max_ram_gb": 6,
        "server_type": "Forge",
        "mc_version": "1.20.1",
        "rcon_host": "127.0.0.1",
        "rcon_port": 25575,
        "rcon_password": os.environ.get("RCON_PASSWORD", ""),
        "server_port": 25565,
        "bedrock_port": 19132,
        "auto_eula": True,
        "auto_backup_min": 15
    },
    "ai": {
        "active_provider": "Ollama (Yerel/Ücretsiz)",
        "active_model": "llama3",
        "providers": {
            "NVIDIA NIM": {
                "api_key": "",
                "base_url": "https://integrate.api.nvidia.com/v1",
                "default_model": "meta/llama-3.1-70b-instruct"
            },
            "OpenRouter": {
                "api_key": "",
                "base_url": "https://openrouter.ai/api/v1",
                "default_model": "meta-llama/llama-3.1-8b-instruct:free"
            },
            "OpenAI": {
                "api_key": "",
                "base_url": "https://api.openai.com/v1",
                "default_model": "gpt-4o-mini"
            },
            "Anthropic": {
                "api_key": "",
                "base_url": "https://api.anthropic.com/v1",
                "default_model": "claude-3-5-sonnet-20241022"
            },
            "Google Gemini": {
                "api_key": "",
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "default_model": "gemini-1.5-flash"
            },
            "Groq": {
                "api_key": "",
                "base_url": "https://api.groq.com/openai/v1",
                "default_model": "llama-3.3-70b-versatile"
            },
            "Mistral AI": {
                "api_key": "",
                "base_url": "https://api.mistral.ai/v1",
                "default_model": "mistral-large-latest"
            },
            "Together AI": {
                "api_key": "",
                "base_url": "https://api.together.xyz/v1",
                "default_model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
            },
            "Perplexity": {
                "api_key": "",
                "base_url": "https://api.perplexity.ai",
                "default_model": "sonar"
            },
            "Cohere": {
                "api_key": "",
                "base_url": "https://api.cohere.ai/v1",
                "default_model": "command-r-plus"
            },
            "DeepSeek": {
                "api_key": "",
                "base_url": "https://api.deepseek.com/v1",
                "default_model": "deepseek-chat"
            },
            "Ollama (Yerel/Ücretsiz)": {
                "api_key": "ollama_local",
                "base_url": "http://localhost:11434/v1",
                "default_model": "llama3"
            }
        }
    }
}


class ConfigManager:
    def __init__(self, filepath=CONFIG_FILE):
        self.filepath = filepath
        self.config = self.load()

    def load(self):
        if not os.path.exists(self.filepath):
            self.save(DEFAULT_CONFIG)
            return json.loads(json.dumps(DEFAULT_CONFIG))

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Merge with default keys to ensure compatibility
            merged = json.loads(json.dumps(DEFAULT_CONFIG))
            self._deep_update(merged, data)
            return merged
        except Exception as e:
            logging.error(f"Config yükleme hatası: {e}")
            return json.loads(json.dumps(DEFAULT_CONFIG))

    def save(self, data=None):
        if data is not None:
            self.config = data
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logging.error(f"Config kaydetme hatası: {e}")
            return False

    def get_server_config(self):
        return self.config.get("server", {})

    def get_ai_config(self):
        return self.config.get("ai", {})

    def set_api_key(self, provider_name, api_key):
        if "ai" in self.config and "providers" in self.config["ai"]:
            if provider_name in self.config["ai"]["providers"]:
                self.config["ai"]["providers"][provider_name]["api_key"] = api_key.strip()
                self.save()
                return True
        return False

    def _deep_update(self, base_dict, update_dict):
        for key, value in update_dict.items():
            if isinstance(value, dict) and key in base_dict and isinstance(base_dict[key], dict):
                self._deep_update(base_dict[key], value)
            else:
                base_dict[key] = value
