#!/usr/bin/env bash

# Update sistem
sudo apt update -y

# Instal dependensi build & tools
sudo apt install -y software-properties-common build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev libbz2-dev

# Tambah repo deadsnakes untuk Python 3.11
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update

# Instal Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev

# Instal pip untuk Python 3.11
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11

# Instal dependensi dasar (Pillow via apt untuk kecepatan)
sudo apt install -y python3-pil

# Instal semua modul yang dibutuhkan skrip (pastikan sesuai error yang muncul)
python3.11 -m pip install rich python-dotenv ascii_magic requests brotli pycryptodome "qrcode[pil]"

# Opsional: jika kamu punya requirements.txt yang valid, pakai ini sebagai ganti baris di atas:
# python3.11 -m pip install -r requirements.txt

echo "Setup selesai! Jalankan dengan: python3.11 main.py"