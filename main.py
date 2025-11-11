import os
import subprocess
import sys

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

def install_dependencies(os_type, package_manager=None):
    """Устанавливает зависимости в зависимости от ОС и пакетного менеджера"""
    print("\n" + "="*50)
    print("Установка зависимостей...")
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
            print("Неизвестный пакетный менеджер. Пропускаем установку зависимостей.")
            return
    
    elif os_type == 'windows':
        # Для Windows предполагаем, что Python и Git уже установлены
        commands = [
            "python --version || python3 --version || echo 'Установите Python с https://python.org'",
            "git --version || echo 'Установите Git с https://git-scm.com'",
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
    ]
    
    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Создана папка: {folder}")
        except Exception as e:
            print(f"Ошибка при создании папки {folder}: {e}")

def download_tools(os_type):
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

def install_python_requirements():
    """Устанавливает Python зависимости для инструментов"""
    print("\n" + "="*50)
    print("Установка Python зависимостей...")
    print("="*50)
    
    # Ищем requirements.txt файлы и устанавливаем зависимости
    for root, dirs, files in os.walk("."):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"Найден requirements.txt: {req_path}")
                try:
                    cmd = f"pip3 install -r {req_path}"
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"✓ Зависимости установлены для {root}")
                except subprocess.CalledProcessError:
                    print(f"✗ Ошибка установки зависимостей для {root}")

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
    """Устанавливает системные инструменты в зависимости от пакетного менеджера"""
    print("\n" + "="*50)
    print("Установка системных инструментов...")
    print("="*50)
    
    if os_type != 'linux':
        return
        
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

def main():
    """Основная функция"""
    show_banner()
    
    # Автоматическое определение ОС
    detected_os = detect_os()
    package_manager = None
    
    if detected_os in ['linux', 'windows']:
        print(f"Автоматически определена ОС: {detected_os}")
        use_detected = input("Использовать автоматическое определение? (y/n): ").strip().lower()
        if use_detected == 'y':
            os_type = detected_os
            if os_type == 'linux':
                # Автоматическое определение пакетного менеджера
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
    install_dependencies(os_type, package_manager)
    
    if os_type == 'linux':
        install_system_tools(os_type, package_manager)
    
    create_folders()
    download_tools(os_type)
    
    if os_type == 'linux':
        setup_go_tools(os_type, package_manager)
    
    install_python_requirements()
    
    print("\n" + "="*50)
    print("УСТАНОВКА ЗАВЕРШЕНА!")
    print("="*50)
    print("\nВсе инструменты успешно скачаны в соответствующие папки.")
    
    if os_type == 'linux':
        print(f"\nИспользованный пакетный менеджер: {package_manager}")
        print("Для использования Go инструментов добавьте ~/go/bin в PATH:")
        print('export PATH="$HOME/go/bin:$PATH"')
    
    print("\nДля использования некоторых инструментов может потребоваться:")
    print("- Дополнительная настройка")
    print("- Установка отсутствующих зависимостей")
    print("- Компиляция (для некоторых инструментов)")

if __name__ == "__main__":
    main()