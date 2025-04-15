import os
import argparse
import shutil
import json
import zipfile
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional

CONVERTER_VERSION = "2.0.1"
DEFAULT_COMPANY = "DefaultCompany"
DEFAULT_PRODUCT = "My Project"
DEFAULT_VERSION = "0.1"

COVERVIEW_CUSTOMIZED = False

class ConverterConfig:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='WeChat Mini Game Converter')
        self._setup_arguments()
        
    def _setup_arguments(self):
        self.parser.add_argument('--source', '-s', required=True, 
                               help='Path to source directory')
        self.parser.add_argument('--target', '-t', required=True,
                               help='Path to target directory')
        self.parser.add_argument('--subpackage', '-sp', nargs='?', const='true', type=str.lower,
                               help='Pack main and subpackages separately')


def copy_cached_plugins(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)

    for root, dirs, files in os.walk(source):
        rel_path = os.path.relpath(root, source)
        target_subdir = os.path.normpath(os.path.join(target, rel_path))
        os.makedirs(target_subdir, exist_ok=True)

        for file_name in files:
            source_file = os.path.normpath(os.path.join(root, file_name))
            target_file = os.path.normpath(os.path.join(target_subdir, file_name))
            if file_name.endswith('.js'):
                minify_js_with_terser(source_file, target_file)
            else:
                shutil.copy2(source_file, target_file)

def minify_js_with_terser(source_file, target_file):
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        source_file_abs = os.path.join(script_dir, source_file)
        target_file_abs = os.path.join(script_dir, target_file)
        terser_command = f'npx terser {source_file_abs} -o {target_file_abs} --compress --mangle'
        run_command(terser_command)

    except FileNotFoundError:
        print("Error: terser is not found. Please ensure terser is installed through npm. Try npm i.")
        sys.exit(1)


def validate_source_path(path: str) -> Path:
    """Verify source path exists"""
    path_obj = Path(path).resolve()
    if not path_obj.exists():
        raise FileNotFoundError(f"Source path does not exist: {path}")
    return path_obj

def ensure_target_path(path: str) -> Path:
    """Create target path if needed with confirmation"""
    
    # Check if on Windows and path contains reserved names
    if sys.platform == 'win32' or sys.platform == 'win64':
        parts = path.split('\\')
        reserved_names = {'con', 'prn', 'aux', 'nul', 'com1', 'com2', 'com3', 'com4',
                        'com5', 'com6', 'com7', 'com8', 'com9', 'lpt1', 'lpt2', 'lpt3',
                        'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9'}
        for part in parts:
            if part.lower() in reserved_names:
                raise ValueError(f"Path contains Windows reserved name '{part}'. Please use a different path.")
    try:
        path_obj = Path(path).resolve()
    except Exception as e:
        raise ValueError(f"Fail to create target path. Please use a different path.") from e
    
    if path_obj.exists() and any(path_obj.iterdir()):
        response = input(f"Target directory {path_obj} is not empty. Continue? [y/N] ").lower()
        if response != 'y':
            print("Operation cancelled by user")
            sys.exit(0)
        print("Removing existing directory...")
        shutil.rmtree(path_obj)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj

def copy_assets(source: Path, target: Path) -> None:
    """Copy assets with overwrite confirmation"""
    if target.exists():
        print(f"Found existing directory: {target}")
        response = input(f"Target directory {target} exists. Overwrite? [y/N] ").lower()
        if response != 'y':
            print("Operation cancelled by user")
            sys.exit(0)
        print("Removing existing directory...")
        shutil.rmtree(target)
    
    print(f"Copying files from {source} to {target}...")
    try:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns(
            '.*', '__pycache__', '*.meta', '*.bak'
        ))
    except shutil.Error as e:
        print(f"[ERROR] Copy error: {str(e)}")
        sys.exit(1)

def handle_game_config(target_folder: Path) -> Dict:
    """Process game configuration files"""
    global COVERVIEW_CUSTOMIZED
    config_path = target_folder / 'game.json'
    
    if not config_path.exists():
        config_path = target_folder / 'manifest.json'
        if not config_path.exists():
            raise FileNotFoundError("Missing game configuration file")

    with open(config_path, 'r+', encoding='utf-8') as f:
        config = json.load(f)
        
        # Apply default settings
        config.update({
            "companyName": DEFAULT_COMPANY,
            "productName": DEFAULT_PRODUCT,
            "productVersion": DEFAULT_VERSION,
            "convertScriptVersion": CONVERTER_VERSION
        })
        
        # Update coverviewCustomized settings
        COVERVIEW_CUSTOMIZED = config.get("coverviewCustomized", False)

        # Update orientation setting
        if 'orientation' in config:
            config['deviceOrientation'] = config['orientation']
            del config['orientation']
            
        f.seek(0)
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.truncate()

        # Print config line by line
        print("Game configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
    
    return config

def copy_plugin(target_folder, plugins):
    cache_dir = 'wx_unity_converter'
    for plugin in plugins:
        plugin_path = f"{cache_dir}/{plugin['name']}-{plugin['version']}"
        if plugin['name'] == "UnityPlugin":
            handle_unity_plugins(target_folder)
            continue
        elif plugin['name'] == "MinigameLoading" or plugin['name'] == "MiniGameCommon" or plugin['name'] == "MiniGameCenter" :
            plugin_path = f"{cache_dir}/{plugin['name']}"

        if(os.path.exists(plugin_path)):
            if plugin['name'] == "MinigameLoading" or plugin['name'] == "MiniGameCommon" or plugin['name'] == "MiniGameCenter" :
                print("Warning: We use our mock file instead of original plugin in order to run game correctly.")
            print("Copied plugin", plugin)
            copy_cached_plugins(plugin_path, f"{target_folder}/cachedPlugin/{plugin['name']}")
        else:
            if(plugin['name'] == "layaPlugin"):
                plugin_path = f"{cache_dir}/{plugin['name']}-{plugin['provider']}"
                if(os.path.exists(plugin_path)):
                    print("Warning: The game is using ", plugin)
                    print("Missing layaPlugin version, but successfully detected its provider. The converted game may not function properly.")
                    print("Copied plugin", plugin)
                    copy_cached_plugins(plugin_path, f"{target_folder}/cachedPlugin/{plugin['name']}")
                else:
                    print("Missing both layaPlugin version and its provider.")
                    print("Now only Unity, cocos and Laya supported. Ignore plugin ", plugin)
            else:
                print("Not supported plugin. Ignore plugin ", plugin)



def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True, stdout=sys.stdout, stderr=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        sys.exit(1)

def handle_unity_plugins(target_folder: Path) -> None:
    """Handle Unity plugin integration"""
    plugin_dir = target_folder / 'cachedPlugin' / 'UnityPlugin'
    plugin_dir.mkdir(parents=True, exist_ok=True)
    
    # Default plugin handling
    default_plugin = Path('libs/UnityPlugin/dist/index.js')
    if not default_plugin.exists():
        raise FileNotFoundError("UnityPlugin not found. Run 'npm run build' in libs/UnityPlugin")
    shutil.copy(default_plugin, plugin_dir / 'index.js')
    print("Copied plugin", plugin_dir / 'index.js')

def inject_runtime_code(game_js: Path) -> None:
    """Inject necessary runtime code into game.js"""
    injection_file = Path('wx_unity_converter') / 'wx_unity.js'
    
    try:
        injection_code = injection_file.read_text(encoding='utf-8')
        original_content = game_js.read_text(encoding='utf-8')
        game_js.write_text(f'/* Unity Converter Injection */\n{injection_code}\n{original_content}', 
                         encoding='utf-8')
    except FileNotFoundError:
        print(f"Warning: Missing injection file {injection_file}")
        
def replace_in_js(file_path: Path, old_str: str, new_str: str) -> bool:
    """Safely replace text in JS file with validation"""
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            count = content.count(old_str)
            if count == 0:
                print(f"  - No occurrences of '{old_str}' found")
                return False

            modified = content.replace(old_str, new_str)
            f.seek(0)
            f.write(modified)
            f.truncate()
            print(f"  - Replaced {count} occurrence(s) of '{old_str}' with '{new_str}'")
            return True
    except Exception as e:
        print(f"[ERROR] Error processing {file_path}: {str(e)}")
        return False
    
def prepend_file(file_path: Path, content: str) -> None:
    """Prepend content to the beginning of a file"""
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            original_content = f.read()
            f.seek(0)
            f.write(f'{content}\n{original_content}')
    except Exception as e:
        print(f"[ERROR] Error prepending file: {file_path}: {str(e)}")

def handle_wasm_split(target_folder: Path) -> None:
    """Process wasm-split.js for platform compatibility"""
    wasm_split = target_folder / 'wasm-split.js'
    if not wasm_split.exists():
        print("  - wasm-split.js not found, skipping...")
        return

    print("  - Found wasm-split.js, processing replacements...")
    # Replace environment checks
    replacements = [
        ('GameGlobal.isIOSHighPerformanceMode', '__rep_isIOSHighPerformanceMode'),
        ('GameGlobal.canUseH5Renderer', '__rep_canUseH5Renderer')
    ]

    replaced_count = 0
    for old, new in replacements:
        if replace_in_js(wasm_split, old, new):
            print(f"  - Adding variable declaration: var {new} = false")
            prepend_file(wasm_split, f'var {new} = false;')
            replaced_count += 1

    print(f"  - Completed WASM processing: {replaced_count} of {len(replacements)} patterns modified")


def handle_customized_coverview(target_folder: Path) -> None:
    """Inject customized coverview settings"""
    index_js_path = os.path.join(target_folder, 'cachedPlugin/UnityPlugin/index.js')
    if not os.path.exists(index_js_path):
        print("cachedPlugin/UnityPlugin/index.js does not exist. Skip prepending.")
        return
    
    result = 'true' if COVERVIEW_CUSTOMIZED else 'false';
    coverviewCode = f"GameGlobal.pluginEnv.coverviewCustomized = {result};"
    prepend_file(index_js_path, coverviewCode)
    print(f"  - Completed coverviewCustomized processing: prepending 1 line to index.js")

def pack_game(target_folder: Path, config: Dict, use_subpackage: bool) -> None:
    """Create ZIP packages for main and subpackages"""
    subpackages = config.get('subPackages', config.get('subpackages', []))
    
    # Package main game
    main_zip = target_folder.parent / 'game.zip'
    print(f"Creating main package: {main_zip}")
    with zipfile.ZipFile(main_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for path in target_folder.rglob('*'):
            if path.is_file():
                # Only exclude subpackages if -sp flag is used
                if use_subpackage and any(sp['root'].strip('/') in str(path.relative_to(target_folder)) for sp in subpackages):
                    continue
                zf.write(path, path.relative_to(target_folder))

    # Package subpackages only if -sp flag is used
    if use_subpackage and subpackages:
        print(f"Found {len(subpackages)} subpackage(s)")
        # Create subpkg directory if needed
        subpkg_dir = target_folder.parent / 'subpkg'
        subpkg_dir.mkdir(exist_ok=True)
        
        for sp in subpackages:
            sp_root = target_folder / sp['root'].strip('/')
            print(f"  - Packing Subpackage: {sp_root}")
            if not sp_root.exists():
                print(f"Skipping missing subpackage: {sp['name']}")
                continue

            sp_zip = subpkg_dir / f"{sp['name']}.zip"
            print(f"Creating subpackage: {sp_zip}")
            with zipfile.ZipFile(sp_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                for path in sp_root.rglob('*'):
                    if path.is_file():
                        zf.write(path, path.relative_to(sp_root))

def process_unity_project(args) -> None:
    """Main processing pipeline for Unity projects"""
    print("\n=== WeChat Mini Game Converter ===")
    
    print("\n[1/10] Validating paths...")
    source = validate_source_path(args.source)
    target_parent = ensure_target_path(args.target)
    target = target_parent / 'game'
    
    print("\n[2/10] Copying project files...")
    copy_assets(source, target)
    
    print("\n[3/10] Processing game configuration...")
    config = handle_game_config(target)
    
    print("\n[4/10] Injecting plugins in game.json...")
    plugins = config.get("plugins", {})
    plugin_info_list = []
    for plugin_name, plugin_info in plugins.items():
        version = plugin_info.get("version")
        provider = plugin_info.get("provider")
        plugin_info_list.append({'name': plugin_name, 'version': version, 'provider': provider})
    copy_plugin(target, plugin_info_list)
    
    print("\n[5/10] Running Babel transformation...")
    babel_dir = target / '@babel'
    if not babel_dir.exists():
        print("  - Running Babel transformation...")
        babel_command = f'npx babel --config-file ./.babelrc "{target}" -d "{target}"'
        try:
            subprocess.run(babel_command, shell=True, check=True)
            print("  - Babel transformation completed successfully")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Babel transformation failed: {str(e)}")
    
    print("\n[6/10] Injecting runtime code...")
    game_js = target / 'game.js'
    if not game_js.exists():
        raise FileNotFoundError("Missing game.js entry point")
    inject_runtime_code(game_js)
    
    print("\n[7/10] Processing WASM compatibility...")
    handle_wasm_split(target)

    print("\n[8/10] Processing coverviewCustomized settings...")
    handle_customized_coverview(target)
    
    print("\n[9/10] Injecting version checker...")
    shutil.copy('wx_unity_converter/check-version.js', target / 'check-version.js')
    
    print("\n[10/10] Creating distribution packages...")
    # True if -sp present without value or -sp true
    use_subpackage = args.subpackage in ['true', 'yes', 'y']
    if use_subpackage:
        print("Packing main package and subpackages separately...")
    else:
        print("Packing all files into main package...")
    pack_game(target, config, use_subpackage)
    
    print("\n[DONE] Conversion completed successfully!")
    print(f"Output directory: {target_parent}")
    # Open output folder in system file explorer
    if sys.platform == "win32":
        os.startfile(target_parent)
    elif sys.platform == "darwin":
        subprocess.run(["open", target_parent])
    else:
        subprocess.run(["xdg-open", target_parent])

if __name__ == "__main__":
    config = ConverterConfig()
    args = config.parser.parse_args()
    
    try:
        process_unity_project(args)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    
