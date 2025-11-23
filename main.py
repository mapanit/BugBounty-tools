import os
import subprocess
import sys
import venv

def detect_os():
    """Определяет операционную систему"""
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('win'):
        return 'windows'
    else:
        return 'unknown'

def detect_linux_package_manager():
    """Определяет пакетный менеджер Linux"""
    try:
        # Проверяем какой пакетный менеджер доступен
        if subprocess.run(["which", "apt"], capture_output=True).returncode == 0:
            return "apt"
        elif subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
            return "dnf"
        elif subprocess.run(["which", "yum"], capture_output=True).returncode == 0:
            return "yum"
        elif subprocess.run(["which", "pacman"], capture_output=True).returncode == 0:
            return "pacman"
        elif subprocess.run(["which", "zypper"], capture_output=True).returncode == 0:
            return "zypper"
        else:
            return "unknown"
    except:
        return "unknown"

def ask_os():
    """Спрашивает пользователя о его ОС"""
    print("Выберите вашу операционную систему:")
    print("1. Linux")
    print("2. Windows")
    
    while True:
        choice = input("Введите номер (1 или 2): ").strip()
        if choice == '1':
            return 'linux'
        elif choice == '2':
            return 'windows'
        else:
            print("Неверный выбор. Попробуйте снова.")

def ask_package_manager():
    """Спрашивает пользователя о пакетном менеджере для Linux"""
    print("\nВыберите ваш пакетный менеджер:")
    print("1. apt (Debian/Ubuntu/Kali)")
    print("2. dnf (Fedora/RHEL)")
    print("3. pacman (Arch/Manjaro)")
    print("4. yum (CentOS/RHEL)")
    print("5. zypper (openSUSE)")
    
    while True:
        choice = input("Введите номер (1-5): ").strip()
        if choice == '1':
            return 'apt'
        elif choice == '2':
            return 'dnf'
        elif choice == '3':
            return 'pacman'
        elif choice == '4':
            return 'yum'
        elif choice == '5':
            return 'zypper'
        else:
            print("Неверный выбор. Попробуйте снова.")

def show_banner():
    """Показывает баннер"""
    banner = r"""
        ____                 ____                    __       
      / __ )__  ______ _   / __ )____  __  ______  / /___  __
      / __  / / / / __ `/  / __  / __ \/ / / / __ \/ __/ / / /
    / /_/ / /_/ / /_/ /  / /_/ / /_/ / /_/ / / / / /_/ /_/ / 
    /_____/\__,_/\__, /  /_____/\____/\__,_/_/ /_/\__/\__, /  
                /____/                               /____/   
      __              __    
      / /_____  ____  / /____
    / __/ __ \/ __ \/ / ___/
    / /_/ /_/ / /_/ / (__  ) 
    \__/\____/\____/_/____/  
    """
    print(banner)

def create_virtual_environment():
    """Создает виртуальное окружение Python"""
    print("\n" + "="*50)
    print("Создание виртуального окружения Python...")
    print("="*50)
    
    venv_dir = "venv"
    
    if os.path.exists(venv_dir):
        print(f"Виртуальное окружение '{venv_dir}' уже существует")
        return venv_dir
    
    try:
        # Создаем виртуальное окружение
        venv.create(venv_dir, with_pip=True)
        print(f"✓ Виртуальное окружение создано: {venv_dir}")
        return venv_dir
    except Exception as e:
        print(f"✗ Ошибка при создании виртуального окружения: {e}")
        return None

def get_venv_python(venv_dir):
    """Возвращает путь к Python в виртуальном окружении"""
    if sys.platform.startswith('win'):
        return os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        return os.path.join(venv_dir, "bin", "python")

def get_venv_pip(venv_dir):
    """Возвращает путь к pip в виртуальном окружении"""
    if sys.platform.startswith('win'):
        return os.path.join(venv_dir, "Scripts", "pip.exe")
    else:
        return os.path.join(venv_dir, "bin", "pip")

def install_dependencies(os_type, package_manager=None, venv_dir=None):
    """Устанавливает системные зависимости"""
    print("\n" + "="*50)
    print("Установка системных зависимостей...")
    print("="*50)
    
    if os_type == 'linux':
        if package_manager == 'apt':
            commands = [
                "sudo apt update",
                "sudo apt install -y git python3 python3-pip curl golang-go nmap",
            ]
        elif package_manager == 'dnf':
            commands = [
                "sudo dnf update -y",
                "sudo dnf install -y git python3 python3-pip curl golang nmap",
            ]
        elif package_manager == 'pacman':
            commands = [
                "sudo pacman -Syu --noconfirm",
                "sudo pacman -S --noconfirm git python python-pip curl go nmap",
            ]
        elif package_manager == 'yum':
            commands = [
                "sudo yum update -y",
                "sudo yum install -y git python3 python3-pip curl golang nmap",
            ]
        elif package_manager == 'zypper':
            commands = [
                "sudo zypper refresh",
                "sudo zypper install -y git python3 python3-pip curl go nmap",
            ]
        else:
            print("Неизвестный пакетный менеджер. Пропускаем установку системных зависимостей.")
            return
    
    elif os_type == 'windows':
        # Для Windows устанавливаем Go и необходимые инструменты
        commands = [
            "python --version || python3 --version || echo 'Установите Python с https://python.org'",
            "git --version || echo 'Установите Git с https://git-scm.com'",
            "go version || echo 'Установите Go с https://golang.org/dl/'",
        ]
    
    for cmd in commands:
        print(f"Выполняю: {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Предупреждение: команда завершилась с ошибкой: {cmd}")
            continue

def create_folders():
    """Создает структуру папок для инструментов"""
    print("\n" + "="*50)
    print("Создание структуры папок...")
    print("="*50)
    
    folders = [
        "Web_catalog",
        "Subdomains", 
        "Scaner",
        "CMS",
        "SSRF",
        "Open_redirect",
        "LFI",
        "XSS",
        "SQLj",
        "JS",
        "Dorks",
    ]
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Создана папка: {folder}")
        except Exception as e:
            print(f"Ошибка при создании папки {folder}: {e}")

def download_tools(os_type, venv_dir=None):
    """Скачивает инструменты из GitHub"""
    print("\n" + "="*50)
    print("Скачивание инструментов...")
    print("="*50)
    
    tools = {
        "Web_catalog": [
            "https://github.com/maurosoria/dirsearch.git",
            "https://github.com/0xKayala/ParamSpider.git",
        ],
        "Subdomains": [
            "https://github.com/m8sec/subscraper.git",
        ],
        "Open_redirect": [
            "https://github.com/devanshbatham/openredirex.git",
        ],
        "Scaner": [
            "https://github.com/coffinsp/lostools.git",
            "https://github.com/cc1a2b/PenHunter.git",
            "https://github.com/jasonxtn/argus.git",
            "https://github.com/atoz-chevara/xlsNinja.git",
        ],
        "LFI": [
            "https://github.com/R3LI4NT/LFIscanner.git",
            "https://github.com/capture0x/Lfi-Space.git",
        ],
        "SQLj": [
            "https://github.com/j1t3sh/SQL-Injection-Finder.git",
            "https://github.com/sqlmapproject/sqlmap.git",
        ],
        "XSS": [
            "https://github.com/s0md3v/XSStrike.git",
        ],
        "SSRF": [
            "https://github.com/swisskyrepo/SSRFmap.git",
        ],
        "JS": [
            "https://github.com/000pp/Pinkerton.git",
            "https://github.com/m4ll0k/SecretFinder.git",
        ],
        "CMS": [
            "https://github.com/Chocapikk/wpprobe.git",
        ],
        "Dorks": [
            "https://github.com/techgaun/github-dorks.git",
        ]
    }
    
    for category, repos in tools.items():
        print(f"\n--- {category} ---")
        for repo in repos:
            repo_name = repo.split("/")[-1].replace(".git", "")
            target_dir = os.path.join(category, repo_name)
            
            if os.path.exists(target_dir):
                print(f"Пропускаем {repo_name} (уже существует)")
                continue
                
            print(f"Скачиваю: {repo_name}")
            try:
                cmd = f"git clone --depth 1 {repo} {target_dir}"
                subprocess.run(cmd, shell=True, check=True)
                print(f"✓ Успешно: {repo_name}")
            except subprocess.CalledProcessError:
                print(f"✗ Ошибка при скачивании: {repo_name}")

def install_python_requirements(venv_dir):
    """Устанавливает Python зависимости для инструментов в виртуальном окружении"""
    print("\n" + "="*50)
    print("Установка Python зависимостей в виртуальном окружении...")
    print("="*50)
    
    venv_pip = get_venv_pip(venv_dir)
    
    # Сначала устанавливаем общие зависимости
    common_packages = [
        "requests",
        "beautifulsoup4",
        "urllib3",
        "colorama",
        "lxml",
        "pyyaml",
        "tqdm",
        "bs4",
        "dnspython",
        "certifi",
        "charset-normalizer",
        "idna",
        "soupsieve",
    ]
    
    print("Установка общих Python пакетов...")
    for package in common_packages:
        try:
            cmd = f'"{venv_pip}" install {package}'
            subprocess.run(cmd, shell=True, check=True)
            print(f"✓ Установлен: {package}")
        except subprocess.CalledProcessError:
            print(f"✗ Ошибка установки: {package}")
    
    # Затем устанавливаем зависимости из requirements.txt файлов
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"Найден requirements.txt: {req_path}")
                try:
                    cmd = f'"{venv_pip}" install -r "{req_path}"'
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"✓ Зависимости установлены для {root}")
                except subprocess.CalledProcessError:
                    print(f"✗ Ошибка установки зависимостей для {root}")
            
            # Устанавливаем зависимости для xlsNinja
            if file == "setup.py" and "xlsNinja" in root:
                print(f"Устанавливаю xlsNinja: {root}")
                try:
                    cmd = f'cd "{root}" && "{venv_pip}" install .'
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"✓ xlsNinja установлен")
                except subprocess.CalledProcessError:
                    print(f"✗ Ошибка установки xlsNinja")

def setup_go_tools(os_type, package_manager=None):
    """Устанавливает Go инструменты"""
    print("\n" + "="*50)
    print("Установка Go инструментов...")
    print("="*50)
    
    go_tools = [
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/hahwul/dalfox/v2@latest",
        "github.com/projectdiscovery/katana/cmd/katana@latest",
        "github.com/cc1a2b/jshunter@latest",
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    ]
    
    for tool in go_tools:
        print(f"Устанавливаю: {tool}")
        try:
            cmd = f"go install {tool}"
            subprocess.run(cmd, shell=True, check=True)
            print(f"✓ Успешно: {tool}")
        except subprocess.CalledProcessError:
            print(f"✗ Ошибка установки: {tool}")

def install_system_tools(os_type, package_manager):
    """Устанавливает системные инструменты"""
    print("\n" + "="*50)
    print("Установка системных инструментов...")
    print("="*50)
    
    if os_type == 'linux':
        tools_commands = {
            'apt': [
                "sudo apt install -y nmap subfinder feroxbuster",
                "sudo apt install -y golang-go",
            ],
            'dnf': [
                "sudo dnf install -y nmap subfinder",
                "sudo dnf install -y golang",
                "dnf copr enable atim/rustscan -y && dnf install rustscan -y",
            ],
            'pacman': [
                "sudo pacman -S --noconfirm nmap subfinder",
                "sudo pacman -S --noconfirm go",
            ],
            'yum': [
                "sudo yum install -y nmap",
                "sudo yum install -y golang",
            ],
            'zypper': [
                "sudo zypper install -y nmap",
                "sudo zypper install -y go",
            ]
        }
        
        if package_manager in tools_commands:
            for cmd in tools_commands[package_manager]:
                print(f"Выполняю: {cmd}")
                try:
                    subprocess.run(cmd, shell=True, check=True)
                except subprocess.CalledProcessError:
                    print(f"Ошибка в команде: {cmd}")
                    continue
    
    elif os_type == 'windows':
        print("Установка инструментов для Windows...")
        windows_tools = [
            "github.com/tomnomnom/assetfinder@latest",
            "github.com/hahwul/dalfox/v2@latest", 
            "github.com/projectdiscovery/katana/cmd/katana@latest",
            "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        ]
        
        for tool in windows_tools:
            print(f"Устанавливаю: {tool}")
            try:
                cmd = f"go install {tool}"
                subprocess.run(cmd, shell=True, check=True)
                print(f"✓ Успешно: {tool}")
            except subprocess.CalledProcessError:
                print(f"✗ Ошибка установки: {tool}")

def setup_windows_go_path():
    """Настраивает PATH для Go инструментов в Windows"""
    print("\n" + "="*50)
    print("Настройка PATH для Windows...")
    print("="*50)
    
    try:
        result = subprocess.run(["go", "env", "GOPATH"], capture_output=True, text=True, check=True)
        go_path = result.stdout.strip()
        go_bin = os.path.join(go_path, "bin")
        
        if os.path.exists(go_bin):
            print(f"Go bin directory: {go_bin}")
            
            path_result = subprocess.run(["echo", "%PATH%"], shell=True, capture_output=True, text=True)
            if go_bin not in path_result.stdout:
                print("\nДобавьте следующий путь в переменную окружения PATH:")
                print(go_bin)
                print("\nИли выполните команду:")
                print(f'setx PATH "%PATH%;{go_bin}"')
        else:
            print("Не удалось найти Go bin directory")
            
    except subprocess.CalledProcessError:
        print("Ошибка при определении Go PATH")

def create_activation_script(venv_dir):
    """Создает скрипт для активации виртуального окружения"""
    print("\n" + "="*50)
    print("Создание скрипта активации...")
    print("="*50)
    
    # Создаем Bash скрипт для активации (работает и на Linux и на Windows с Git Bash/WSL)
    bash_content = f"""#!/bin/bash
echo "Активация виртуального окружения для инструментов пентеста..."
source {venv_dir}/bin/activate
echo "Виртуальное окружение активировано!"
echo ""
echo "Доступные папки с инструментами:"
echo "- Web_catalog - инструменты сканирования каталогов"
echo "- Subdomains - инструменты поиска поддоменов"
echo "- Scaner - сканеры уязвимостей"
echo "- CMS - инструменты для CMS"
echo "- SSRF - инструменты для обнаружения SSRF"
echo "- Open_redirect - инструменты для открытых редиректов"
echo "- LFI - инструменты для Local File Inclusion"
echo "- XSS - инструменты для XSS"
echo "- SQLj - инструменты для SQL инъекций"
echo "- JS - инструменты для анализа JavaScript"
echo "- Dorks - инструменты для поиска уязвимостей"
echo ""
echo "Для деактивации виртуального окружения выполните: deactivate"
"""
    
    with open("activate_venv.sh", "w", encoding="utf-8") as f:
        f.write(bash_content)
    
    # Делаем скрипт исполняемым
    os.chmod("activate_venv.sh", 0o755)
    print("✓ Создан файл activate_venv.sh для активации окружения")
    
    # Создаем инструкцию для Windows пользователей
    if sys.platform.startswith('win'):
        print("\nДля пользователей Windows:")
        print("1. Установите Git Bash или используйте WSL")
        print("2. Запустите скрипт: ./activate_venv.sh")
        print("3. Или активируйте вручную: source venv/Scripts/activate")

def main():
    """Основная функция"""
    show_banner()
    
    # Создаем виртуальное окружение
    venv_dir = create_virtual_environment()
    if not venv_dir:
        print("Не удалось создать виртуальное окружение. Продолжаем без него...")
        venv_dir = None
    
    # Автоматическое определение ОС
    detected_os = detect_os()
    package_manager = None
    
    if detected_os in ['linux', 'windows']:
        print(f"Автоматически определена ОС: {detected_os}")
        use_detected = input("Использовать автоматическое определение? (y/n): ").strip().lower()
        if use_detected == 'y':
            os_type = detected_os
            if os_type == 'linux':
                auto_pm = detect_linux_package_manager()
                if auto_pm != 'unknown':
                    print(f"Автоматически определен пакетный менеджер: {auto_pm}")
                    use_auto_pm = input(f"Использовать {auto_pm}? (y/n): ").strip().lower()
                    if use_auto_pm == 'y':
                        package_manager = auto_pm
                    else:
                        package_manager = ask_package_manager()
                else:
                    print("Не удалось определить пакетный менеджер автоматически.")
                    package_manager = ask_package_manager()
        else:
            os_type = ask_os()
            if os_type == 'linux':
                package_manager = ask_package_manager()
    else:
        os_type = ask_os()
        if os_type == 'linux':
            package_manager = ask_package_manager()
    
    print(f"\nВыбрана ОС: {os_type}")
    if os_type == 'linux':
        print(f"Пакетный менеджер: {package_manager}")
    
    # Выполняем установку
    install_dependencies(os_type, package_manager, venv_dir)
    install_system_tools(os_type, package_manager)
    create_folders()
    download_tools(os_type, venv_dir)
    setup_go_tools(os_type, package_manager)
    
    if venv_dir:
        install_python_requirements(venv_dir)
        create_activation_script(venv_dir)
    
    if os_type == 'windows':
        setup_windows_go_path()
    
    print("\n" + "="*50)
    print("УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*50)
    
    if venv_dir:
        print(f"\n✓ Виртуальное окружение создано в папке: {venv_dir}")
        print("✓ Для активации окружения выполните: source activate_venv.sh")
        print("✓ Или вручную: source venv/bin/activate (Linux) или venv\\Scripts\\activate (Windows)")
    
    print("\nВсе инструменты успешно скачаны в соответствующие папки.")
    
    if os_type == 'linux':
        print(f"\nИспользованный пакетный менеджер: {package_manager}")
        print("Для использования Go инструментов добавьте ~/go/bin в PATH:")
        print('export PATH="$HOME/go/bin:$PATH"')
    
    print("\nДобавленные инструменты:")
    print("- github-dorks (в папке Dorks)")
    print("- xlsNinja (в папке Scaner)")
    print("- subfinder (через Go install)")
    
    print("\nДля использования некоторых инструментов может потребоваться:")
    print("- Дополнительная настройка")
    print("- Установка отсутствующих зависимостей")
    print("- Компиляция (для некоторых инструментов)")

if __name__ == "__main__":
    main()