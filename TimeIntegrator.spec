# TimeIntegrator.spec (The Golden Standard for macOS Apps)

from PyQt6.QtCore import QLibraryInfo

# ---------------- 核心分析阶段 ----------------
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('Data', 'Data'),
        ('QtUI/rawUI', 'QtUI/rawUI'),
        # 这是一个更健壮、更专业的获取插件路径的方法
        # 它不再依赖于你本地的硬编码路径
        (QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath), 'PyQt6/Qt6/plugins')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# ---------------- Python字节码打包阶段 ----------------
pyz = PYZ(a.pure)

# ---------------- 可执行文件生成阶段 ----------------
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TimeIntegrator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    # 核心：console必须为False，以创建一个无终端的窗口化应用
    console=False, 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ---------------- 最终的应用包捆绑阶段 ----------------
# 我们用 BUNDLE 来代替 COLLECT
app = BUNDLE(
    exe,
    name='TimeIntegrator.app', # 最终产物的名字
    icon='path/to/your/icon.icns', # 你的.icns文件的路径
    bundle_identifier='com.yourname.timeintegrator', # 必须和Info.plist里的一致
    info_plist='Info.plist' # 你的Info.plist文件的路径
)