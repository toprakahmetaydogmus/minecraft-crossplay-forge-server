import os
import subprocess
import shutil

src_dir = os.path.abspath("build_plugin/src/com/crossplay/sell")
os.makedirs(src_dir, exist_ok=True)
bin_dir = os.path.abspath("build_plugin/bin")
os.makedirs(bin_dir, exist_ok=True)

plugin_yml = """name: CrossplayEkoSell
version: 1.0.0
main: com.crossplay.sell.CrossplayEkoSell
api-version: '1.20'
depend: [Vault, EconomyShopGUI]
commands:
  sell:
    description: Elinizdeki veya secilen esyayi satar
    aliases: [sat, sellhand, sathand]
  sellall:
    description: Tum envanteri veya secilen esyayi satar
    aliases: [satall, sathepsi, hepsinisat]
  akce:
    description: Akce yonetim ve transfer komutu
    aliases: [para]
"""

with open("build_plugin/plugin.yml", "w", encoding="utf-8") as f:
    f.write(plugin_yml)

java_code = """package com.crossplay.sell;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.plugin.RegisteredServiceProvider;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scoreboard.Objective;
import org.bukkit.scoreboard.Scoreboard;
import net.milkbowl.vault.economy.Economy;

public class CrossplayEkoSell extends JavaPlugin implements CommandExecutor {

    private static Economy econ = null;

    @Override
    public void onEnable() {
        setupEconomy();
        if (getCommand("sell") != null) getCommand("sell").setExecutor(this);
        if (getCommand("sellall") != null) getCommand("sellall").setExecutor(this);
        if (getCommand("akce") != null) getCommand("akce").setExecutor(this);

        // Scoreboard & Vault Realtime Auto-Sync (Her saniye)
        Bukkit.getScheduler().runTaskTimer(this, () -> {
            if (econ == null) return;
            Scoreboard sb = Bukkit.getScoreboardManager().getMainScoreboard();
            Objective obj = sb.getObjective("akce");
            if (obj == null) return;

            for (Player p : Bukkit.getOnlinePlayers()) {
                try {
                    int bal = (int) econ.getBalance(p);
                    if (obj.getScore(p.getName()).getScore() != bal) {
                        obj.getScore(p.getName()).setScore(bal);
                    }
                } catch (Exception ignored) {}
            }
        }, 20L, 20L);

        getLogger().info("CrossplayEkoSell basariyla yuklendi! Realtime Akce Senkronizasyonu Devrede.");
    }

    private boolean setupEconomy() {
        if (getServer().getPluginManager().getPlugin("Vault") == null) return false;
        RegisteredServiceProvider<Economy> rsp = getServer().getServicesManager().getRegistration(Economy.class);
        if (rsp == null) return false;
        econ = rsp.getProvider();
        return econ != null;
    }

    public static Economy getEconomy() {
        return econ;
    }

    @Override
    public boolean onCommand(CommandSender sender, Command cmd, String label, String[] args) {
        String name = cmd.getName().toLowerCase();

        if (name.equals("sellall")) {
            if (!(sender instanceof Player)) {
                sender.sendMessage(ChatColor.RED + "Bu komut yalnizca oyuncular tarafindan kullanilabilir.");
                return true;
            }
            Player p = (Player) sender;
            if (args.length == 0) {
                // Hepsini sat (Tum envanter)
                p.performCommand("economyshopgui:sellall");
            } else {
                // Argumanli sat (orn: /sellall diamond)
                p.performCommand("economyshopgui:sellall " + String.join(" ", args));
            }
            return true;
        }

        if (name.equals("sell")) {
            if (!(sender instanceof Player)) {
                sender.sendMessage(ChatColor.RED + "Bu komut yalnizca oyuncular tarafindan kullanilabilir.");
                return true;
            }
            Player p = (Player) sender;

            if (args.length == 0) {
                // Eldeki esyayi sat
                ItemStack hand = p.getInventory().getItemInMainHand();
                if (hand == null || hand.getType() == Material.AIR) {
                    p.sendMessage(ChatColor.GOLD + "Market " + ChatColor.DARK_GRAY + "» " + ChatColor.RED + "Elinizde satilabilecek bir esya yok!");
                    p.sendMessage(ChatColor.YELLOW + "  ➥ Belirli bir esyayi satmak icin: " + ChatColor.WHITE + "/sell [esya]");
                    p.sendMessage(ChatColor.YELLOW + "  ➥ Tum envanteri satmak icin: " + ChatColor.GREEN + "/sellall");
                    return true;
                }
                p.performCommand("economyshopgui:sellall hand");
            } else {
                String sub = args[0].toLowerCase();
                if (sub.equals("all") || sub.equals("hepsi")) {
                    p.performCommand("economyshopgui:sellall");
                } else if (sub.equals("hand") || sub.equals("el")) {
                    p.performCommand("economyshopgui:sellall hand");
                } else if (sub.equals("gui")) {
                    p.performCommand("economyshopgui:sellgui");
                } else {
                    // Verilen esya adini sat (orn: /sell diamond)
                    p.performCommand("economyshopgui:sellall " + String.join(" ", args));
                }
            }
            return true;
        }

        if (name.equals("akce")) {
            if (args.length == 0) {
                if (sender instanceof Player) {
                    Player p = (Player) sender;
                    double bal = econ != null ? econ.getBalance(p) : 0;
                    p.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.YELLOW + "Bakiyeniz: " + ChatColor.GREEN + String.format("%,.0f", bal) + " Akce");
                } else {
                    sender.sendMessage(ChatColor.YELLOW + "Kullanim: /akce [ver|al|ayarla|gonder|bakiye] [oyuncu] [miktar]");
                }
                return true;
            }

            String action = args[0].toLowerCase();

            if (action.equals("bakiye")) {
                String targetName = args.length > 1 ? args[1] : sender.getName();
                Player target = Bukkit.getPlayer(targetName);
                if (target == null) {
                    sender.sendMessage(ChatColor.RED + "Oyuncu bulunamadi: " + targetName);
                    return true;
                }
                double bal = econ != null ? econ.getBalance(target) : 0;
                sender.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.YELLOW + target.getName() + " Bakiyesi: " + ChatColor.GREEN + String.format("%,.0f", bal) + " Akce");
                return true;
            }

            if (action.equals("gonder") || action.equals("pay")) {
                if (!(sender instanceof Player)) {
                    sender.sendMessage(ChatColor.RED + "Bu komutu sadece oyuncular kullanabilir.");
                    return true;
                }
                if (args.length < 3) {
                    sender.sendMessage(ChatColor.RED + "Kullanim: /akce gonder [oyuncu] [miktar]");
                    return true;
                }
                Player from = (Player) sender;
                Player to = Bukkit.getPlayer(args[1]);
                if (to == null) {
                    from.sendMessage(ChatColor.RED + "Oyuncu bulunamadi: " + args[1]);
                    return true;
                }
                if (to.equals(from)) {
                    from.sendMessage(ChatColor.RED + "Kendinize akce gonderemezsiniz.");
                    return true;
                }
                double amount;
                try {
                    amount = Double.parseDouble(args[2]);
                    if (amount <= 0) throw new NumberFormatException();
                } catch (NumberFormatException e) {
                    from.sendMessage(ChatColor.RED + "Gecersiz miktar!");
                    return true;
                }

                if (econ.getBalance(from) < amount) {
                    from.sendMessage(ChatColor.RED + "Yetersiz bakiye! Mevcut: " + (int)econ.getBalance(from) + " Akce");
                    return true;
                }

                econ.withdrawPlayer(from, amount);
                econ.depositPlayer(to, amount);

                Scoreboard sb = Bukkit.getScoreboardManager().getMainScoreboard();
                Objective obj = sb.getObjective("akce");
                if (obj != null) {
                    obj.getScore(from.getName()).setScore((int) econ.getBalance(from));
                    obj.getScore(to.getName()).setScore((int) econ.getBalance(to));
                }

                from.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.GREEN + to.getName() + " adli oyuncuya " + String.format("%,.0f", amount) + " Akce gonderildi!");
                to.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.GREEN + from.getName() + " adli oyuncu size " + String.format("%,.0f", amount) + " Akce gonderdi!");
                return true;
            }

            // Admin komutlari: ver, al, ayarla
            if (!sender.hasPermission("admin.akce") && !sender.isOp()) {
                sender.sendMessage(ChatColor.RED + "Bu komutu kullanmak icin yetkiniz yok.");
                return true;
            }

            if (args.length < 3) {
                sender.sendMessage(ChatColor.YELLOW + "Kullanim: /akce [ver|al|ayarla] [oyuncu] [miktar]");
                return true;
            }

            Player target = Bukkit.getPlayer(args[1]);
            if (target == null) {
                sender.sendMessage(ChatColor.RED + "Oyuncu bulunamadi: " + args[1]);
                return true;
            }

            double amount;
            try {
                amount = Double.parseDouble(args[2]);
            } catch (NumberFormatException e) {
                sender.sendMessage(ChatColor.RED + "Gecersiz miktar!");
                return true;
            }

            Scoreboard sb = Bukkit.getScoreboardManager().getMainScoreboard();
            Objective obj = sb.getObjective("akce");

            if (action.equals("ver") || action.equals("give")) {
                econ.depositPlayer(target, amount);
                if (obj != null) obj.getScore(target.getName()).setScore((int) econ.getBalance(target));
                sender.sendMessage(ChatColor.GREEN + target.getName() + " adli oyuncuya " + String.format("%,.0f", amount) + " Akce verildi.");
                target.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.GREEN + "+" + String.format("%,.0f", amount) + " Akce hesabiniza eklendi!");
            } else if (action.equals("al") || action.equals("take")) {
                econ.withdrawPlayer(target, amount);
                if (obj != null) obj.getScore(target.getName()).setScore((int) econ.getBalance(target));
                sender.sendMessage(ChatColor.YELLOW + target.getName() + " adli oyuncudan " + String.format("%,.0f", amount) + " Akce kesildi.");
                target.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.RED + "-" + String.format("%,.0f", amount) + " Akce hesabinizdan kesildi!");
            } else if (action.equals("ayarla") || action.equals("set")) {
                double current = econ.getBalance(target);
                if (current > 0) econ.withdrawPlayer(target, current);
                if (amount > 0) econ.depositPlayer(target, amount);
                if (obj != null) obj.getScore(target.getName()).setScore((int) amount);
                sender.sendMessage(ChatColor.AQUA + target.getName() + " bakiyesi " + String.format("%,.0f", amount) + " Akce olarak ayarlandi.");
                target.sendMessage(ChatColor.GOLD + "✦ AKCE ✦ " + ChatColor.DARK_GRAY + "» " + ChatColor.AQUA + "Bakiyeniz " + String.format("%,.0f", amount) + " Akce olarak guncellendi.");
            }
            return true;
        }

        return false;
    }
}
"""

with open("build_plugin/src/com/crossplay/sell/CrossplayEkoSell.java", "w", encoding="utf-8") as f:
    f.write(java_code)

print("Files generated. Compiling...")

arclight_jar = os.path.abspath(".arclight/mod_file/arclight-1.20.1-1.0.5-1a8925b.jar")
vault_jar = os.path.abspath("plugins/Vault.jar")

cp = f"{arclight_jar};{vault_jar}"
cmd = [
    "javac",
    "--release", "17",
    "-encoding", "utf-8",
    "-cp", cp,
    "-d", bin_dir,
    "build_plugin/src/com/crossplay/sell/CrossplayEkoSell.java"
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Compilation error:\n", res.stderr)
    exit(1)

print("Compilation successful! Creating jar...")
shutil.copy("build_plugin/plugin.yml", "build_plugin/bin/plugin.yml")

jar_target = os.path.abspath("plugins/CrossplayEkoSell.jar")
jar_cmd = ["jar", "cvf", jar_target, "-C", bin_dir, "."]
res2 = subprocess.run(jar_cmd, capture_output=True, text=True)
if res2.returncode != 0:
    print("Jar error:\n", res2.stderr)
    exit(1)

print("Plugin jar created at:", jar_target)
