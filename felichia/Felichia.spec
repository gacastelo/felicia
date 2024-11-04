# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_path = os.getcwd()

# Coleta todos os submódulos e dados do customtkinter
customtkinter_submodules = collect_submodules('customtkinter')
customtkinter_datas = collect_data_files('customtkinter')

# Lista todos os arquivos de assets e sons
datas_to_include = []
assets_dir = os.path.join(project_path, 'assets')
for root, dirs, files in os.walk(assets_dir):
    for file in files:
        if file.endswith(('.png', '.ico', '.jpg', '.jpeg', '.wav')):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, project_path)
            target_path = os.path.dirname(rel_path)
            datas_to_include.append((rel_path, target_path))

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[project_path],
    binaries=[],
    datas=[
        ('assets', 'assets'),  # Inclui toda a pasta assets
        ('database', 'database'),
        ('views', 'views'),
        ('controllers', 'controllers'),
        ('models', 'models'),
        ('utils', 'utils'),
    ] + customtkinter_datas,  # Adiciona dados do customtkinter
    hiddenimports=customtkinter_submodules + [
        'PIL',
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk',
        'sqlite3',
        'tkinter',
        'tkinter.ttk',
        'views.animations.splash_screen',
        'views.login_view',
        'json',
        'datetime',
        'pygame',
        'pygame.mixer',
        'pygame.mixer_music',
        'utils.sound_manager',
        'winsound',  # Adicionado como alternativa
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Felichia',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Mudado de True para False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('assets', 'Felichia_logo3.ico'),
    uac_admin=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Felichia',
)
