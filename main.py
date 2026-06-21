#!/usr/bin/env python3
"""
BugBounty-script — автоматическая подготовка окружения для Bug Bounty / пентестинга.

ВАЖНО: используйте установленные инструменты только в рамках законных
и согласованных тестов (authorized testing / bug bounty программы).
Несанкционированное использование может нарушать закон.
"""

import argparse
import os
import shutil
import subprocess
import sys
import venv

IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0
FAILURES = []  # список (этап, элемент, ошибка) для финального отчёта


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def print_header(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)


def sudo():
    """Возвращает 'sudo ' если скрипт запущен не от root, иначе ''."""
    return "" if IS_ROOT else "sudo "


def binary_exists(name):
    return shutil.which(name) is not None


def run(cmd, stage, item, shell=True, check_output=False):
    """
    Унифицированный запуск команды с обработкой ошибок и записью в FAILURES.
    При check_output=True возвращает CompletedProcess при успехе или False при ошибке.
    Иначе возвращает True/False.
    """
    try:
        if check_output:
            return subprocess.run(cmd, shell=shell, check=True,
                                   capture_output=True, text=True)
        subprocess.run(cmd, shell=shell, check=True)
        return True
    except subprocess.CalledProcessError as e:
        FAILURES.append((stage, item, str(e)))
        return False
    except FileNotFoundError as e:
        FAILURES.append((stage, item, f"команда не найдена: {e}"))
        return False


# ---------------------------------------------------------------------------
# Определение системы
# ---------------------------------------------------------------------------

def detect_os():
    """Определяет операционную систему"""
    if sys.platform.startswith("linux"):
        return "linux"
    return "unknown"


def check_linux_system():
    """Проверяет, что скрипт запущен на Linux"""
    if detect_os() != "linux":
        print("\n" + "!" * 60)
        print("ОШИБКА: Этот скрипт предназначен только для Linux!")
        print("Обнаружена ОС:", sys.platform)
        print("!" * 60)
        sys.exit(1)


def check_sudo_access():
    """Проверяет, что есть возможность выполнять команды с повышенными правами"""
    if IS_ROOT:
        return
    if not binary_exists("sudo"):
        print("\n" + "!" * 60)
        print("ОШИБКА: команда 'sudo' не найдена, а скрипт запущен не от root.")
        print("Установите sudo или запустите скрипт от имени root.")
        print("!" * 60)
        sys.exit(1)


def detect_linux_package_manager():
    """Определяет пакетный менеджер Linux"""
    for pm in ("apt", "dnf", "yum", "pacman", "zypper"):
        if binary_exists(pm):
            return pm
    return "unknown"


def ask_package_manager():
    """Спрашивает пользователя о пакетном менеджере для Linux"""
    print("\nВыберите ваш пакетный менеджер:")
    print("1. apt (Debian/Ubuntu/Kali)")
    print("2. dnf (Fedora/RHEL)")
    print("3. pacman (Arch/Manjaro)")
    print("4. yum (CentOS/RHEL)")
    print("5. zypper (openSUSE)")

    mapping = {"1": "apt", "2": "dnf", "3": "pacman", "4": "yum", "5": "zypper"}
    while True:
        choice = input("Введите номер (1-5): ").strip()
        if choice in mapping:
            return mapping[choice]
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


# ---------------------------------------------------------------------------
# Виртуальное окружение
# ---------------------------------------------------------------------------

def create_virtual_environment(venv_dir="venv"):
    """Создаёт виртуальное окружение Python (вызывать ПОСЛЕ установки системных пакетов,
    т.к. на Debian/Ubuntu для этого нужен системный пакет python3-venv)."""
    print_header("Создание виртуального окружения Python...")

    if os.path.exists(venv_dir):
        print(f"Виртуальное окружение '{venv_dir}' уже существует")
        return venv_dir

    try:
        venv.create(venv_dir, with_pip=True)
        print(f"✓ Виртуальное окружение создано: {venv_dir}")
        return venv_dir
    except Exception as e:
        FAILURES.append(("venv", venv_dir, str(e)))
        print(f"✗ Ошибка при создании виртуального окружения: {e}")
        return None


def get_venv_pip(venv_dir):
    """Возвращает путь к pip в виртуальном окружении"""
    return os.path.join(venv_dir, "bin", "pip")


# ---------------------------------------------------------------------------
# Системные пакеты
# ---------------------------------------------------------------------------

PACKAGE_COMMANDS = {
    "apt": [
        "{sudo}apt update",
        "{sudo}apt install -y git python3 python3-venv python3-pip curl wget "
        "golang-go nmap nikto ruby ruby-dev build-essential libpq-dev "
        "zlib1g-dev libsqlite3-dev subfinder feroxbuster ffuf",
    ],
    "dnf": [
        "{sudo}dnf update -y",
        "{sudo}dnf install -y git python3 python3-pip curl wget golang nmap "
        "nikto ruby ruby-devel postgresql-devel zlib-devel sqlite-devel "
        "subfinder ffuf",
        "{sudo}dnf copr enable atim/rustscan -y && {sudo}dnf install -y rustscan",
    ],
    "pacman": [
        "{sudo}pacman -Syu --noconfirm",
        "{sudo}pacman -S --noconfirm git python python-pip curl wget go nmap "
        "nikto ruby subfinder ffuf",
    ],
    "yum": [
        "{sudo}yum update -y",
        "{sudo}yum install -y git python3 python3-pip curl wget golang nmap "
        "nikto ruby ruby-devel ffuf",
    ],
    "zypper": [
        "{sudo}zypper refresh",
        "{sudo}zypper install -y git python3 python3-pip curl wget go nmap "
        "nikto ruby ruby-devel ffuf",
    ],
}


def install_system_packages(package_manager):
    """Устанавливает системные зависимости и инструменты одним проходом
    (раньше это были две отдельные функции с дублирующимся apt update и пакетами)."""
    print_header("Установка системных зависимостей и инструментов...")

    commands = PACKAGE_COMMANDS.get(package_manager)
    if not commands:
        print("Неизвестный пакетный менеджер. Пропускаем установку системных пакетов.")
        return

    for template in commands:
        cmd = template.format(sudo=sudo())
        print(f"Выполняю: {cmd}")
        if not run(cmd, "Системные пакеты", cmd):
            print(f"Предупреждение: команда завершилась с ошибкой: {cmd}")


def install_ruby_tools():
    """Устанавливает Ruby-инструменты (WPScan) поверх системного Ruby"""
    print_header("Установка Ruby-инструментов (WPScan)...")

    if not binary_exists("gem"):
        print("✗ gem не найден, пропускаем установку WPScan")
        FAILURES.append(("Ruby tools", "wpscan", "бинарь gem не найден"))
        return

    cmd = f"{sudo()}gem install wpscan"
    print(f"Выполняю: {cmd}")
    if run(cmd, "Ruby tools", "wpscan"):
        print("✓ Установлен: wpscan")
    else:
        print("✗ Ошибка установки: wpscan")


# ---------------------------------------------------------------------------
# Структура папок и инструменты
# ---------------------------------------------------------------------------

def create_folders():
    """Создаёт структуру папок для инструментов"""
    print_header("Создание структуры папок...")

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
        "Reconnaissance",
        "Secrets",
        "Nuclei_Templates",
        "Wordlists",
    ]

    for folder in folders:
        try:
            os.makedirs(folder, exist_ok=True)
            print(f"Создана папка: {folder}")
        except OSError as e:
            FAILURES.append(("Папки", folder, str(e)))
            print(f"Ошибка при создании папки {folder}: {e}")


def download_tools(venv_dir=None):
    """Скачивает инструменты из GitHub"""
    print_header("Скачивание инструментов...")

    if not binary_exists("git"):
        print("✗ git не найден, пропускаем скачивание инструментов")
        FAILURES.append(("Скачивание инструментов", "git", "бинарь git не найден"))
        return

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
            "https://github.com/projectdiscovery/nuclei.git",
        ],
        "LFI": [
            "https://github.com/R3LI4NT/LFIscanner.git",
            "https://github.com/capture0x/Lfi-Space.git",
        ],
        "SQLj": [
            "https://github.com/j1t3sh/SQL-Injection-Finder",
            "https://github.com/sqlmapproject/sqlmap",
        ],
        "XSS": [
            "https://github.com/s0md3v/XSStrike",
        ],
        "SSRF": [
            "https://github.com/swisskyrepo/SSRFmap",
        ],
        "JS": [
            "https://github.com/000pp/Pinkerton",
            "https://github.com/m4ll0k/SecretFinder",
        ],
        "CMS": [
            "https://github.com/Tuhinshubhra/CMSeeK.git",
            "https://github.com/droope/droopescan.git",
        ],
        "Dorks": [
            "https://github.com/techgaun/github-dorks",
        ],
        "Reconnaissance": [
            "https://github.com/laramies/theHarvester",
        ],
        "Secrets": [
            "https://github.com/trufflesecurity/trufflehog",
        ],
        "Nuclei_Templates": [
            "https://github.com/projectdiscovery/nuclei-templates",
        ],
    }

    for category, repos in tools.items():
        print(f"\n--- {category} ---")
        if not repos:
            print("  (пока нет инструментов в этой категории)")
            continue

        for repo in repos:
            repo_name = repo.split("/")[-1].replace(".git", "")
            target_dir = os.path.join(category, repo_name)

            if os.path.exists(target_dir):
                print(f"Пропускаем {repo_name} (уже существует)")
                continue

            print(f"Скачиваю: {repo_name}")
            cmd = f"git clone --depth 1 {repo} {target_dir}"
            if run(cmd, category, repo_name):
                print(f"✓ Успешно: {repo_name}")
            else:
                print(f"✗ Ошибка при скачивании: {repo_name}")


def install_seclists():
    """Устанавливает SecLists — коллекции wordlists для пентеста"""
    print_header("Установка SecLists...")

    seclists_dir = os.path.join("Wordlists", "SecLists")

    if os.path.exists(seclists_dir):
        print("SecLists уже установлены")
        return True

    if not binary_exists("git"):
        print("✗ git не найден, пропускаем установку SecLists")
        FAILURES.append(("SecLists", "git", "бинарь git не найден"))
        return False

    print("Скачиваю SecLists...")
    cmd = f"git clone --depth 1 https://github.com/danielmiessler/SecLists.git {seclists_dir}"
    if not run(cmd, "SecLists", "клонирование"):
        print("✗ Ошибка при установке SecLists")
        return False

    print("✓ SecLists успешно установлены")

    link_target = "/usr/share/seclists"
    if os.path.exists(link_target):
        print(f"{link_target} уже существует")
    else:
        current_dir = os.getcwd()
        cmd = f"{sudo()}ln -sf {current_dir}/{seclists_dir} {link_target}"
        if run(cmd, "SecLists", "symlink"):
            print(f"✓ Создана символическая ссылка {link_target}")
        else:
            print(f"⚠ Не удалось создать ссылку {link_target}. Создайте вручную при необходимости.")

    return True


def install_metasploit(package_manager):
    """Устанавливает Metasploit Framework через пакетный менеджер, без скачивания
    отдельного файла-установщика."""
    print_header("Установка Metasploit Framework...")

    if binary_exists("msfconsole"):
        print("Metasploit Framework уже установлен")
        db_check = subprocess.run(["msfdb", "status"], capture_output=True, text=True)
        if "not running" in db_check.stdout or "not initialized" in db_check.stdout:
            print("Инициализируем базу данных Metasploit...")
            run(f"{sudo()}msfdb init", "Metasploit", "msfdb init")
        return True

    install_commands = {
        "apt": f"{sudo()}apt install -y metasploit-framework",
        "dnf": f"{sudo()}dnf install -y metasploit-framework",
        "yum": f"{sudo()}yum install -y metasploit-framework",
        "pacman": f"{sudo()}pacman -S --noconfirm metasploit",
        "zypper": f"{sudo()}zypper install -y metasploit-framework",
    }

    cmd = install_commands.get(package_manager)
    if not cmd:
        print(f"✗ Нет команды установки Metasploit для пакетного менеджера '{package_manager}'")
        FAILURES.append(("Metasploit", "install", f"нет команды для {package_manager}"))
        return False

    if package_manager == "apt":
        print("Установка зависимостей для Metasploit...")
        run(f"{sudo()}apt install -y libpq-dev postgresql postgresql-contrib libpcap-dev",
            "Metasploit", "зависимости apt")

    print(f"Выполняю: {cmd}")
    if not run(cmd, "Metasploit", "установка пакета"):
        print("✗ Не удалось установить Metasploit Framework через пакетный менеджер")
        print("  Возможно, пакет недоступен в репозиториях вашего дистрибутива")
        print("  (типично для не-Kali Debian/Ubuntu) — установите вручную при необходимости")
        return False

    run(f"{sudo()}msfdb init", "Metasploit", "инициализация БД")

    print("✓ Metasploit Framework успешно установлен")
    return True


def install_python_requirements(venv_dir):
    """Устанавливает Python-зависимости для инструментов в виртуальном окружении"""
    print_header("Установка Python-зависимостей в виртуальном окружении...")

    venv_pip = get_venv_pip(venv_dir)

    common_packages = [
        "requests", "beautifulsoup4", "urllib3", "colorama", "lxml",
        "pyyaml", "tqdm", "bs4", "dnspython", "certifi",
        "charset-normalizer", "idna", "soupsieve",
    ]

    print("Установка общих Python-пакетов...")
    for package in common_packages:
        cmd = f'"{venv_pip}" install {package}'
        if run(cmd, "Python deps", package):
            print(f"✓ Установлен: {package}")
        else:
            print(f"✗ Ошибка установки: {package}")

    for root, _dirs, files in os.walk("."):
        for file in files:
            if file == "requirements.txt":
                req_path = os.path.join(root, file)
                print(f"Найден requirements.txt: {req_path}")
                cmd = f'"{venv_pip}" install -r "{req_path}"'
                if run(cmd, "Python deps", req_path):
                    print(f"✓ Зависимости установлены для {root}")
                else:
                    print(f"✗ Ошибка установки зависимостей для {root}")

            if file == "setup.py" and "xlsNinja" in root:
                print(f"Устанавливаю xlsNinja: {root}")
                cmd = f'cd "{root}" && "{venv_pip}" install .'
                if run(cmd, "Python deps", "xlsNinja"):
                    print("✓ xlsNinja установлен")
                else:
                    print("✗ Ошибка установки xlsNinja")


def setup_go_tools():
    """Устанавливает Go-инструменты"""
    print_header("Установка Go-инструментов...")

    if not binary_exists("go"):
        print("✗ Go не найден в системе, пропускаем установку Go-инструментов")
        FAILURES.append(("Go tools", "go", "бинарь go не найден"))
        return

    go_tools = [
        "github.com/tomnomnom/assetfinder@latest",
        "github.com/hahwul/dalfox/v2@latest",
        "github.com/projectdiscovery/katana/cmd/katana@latest",
        "github.com/cc1a2b/jshunter@latest",
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "github.com/Chocapikk/wpprobe@latest",
        # добавлено по итогам обсуждения:
        "github.com/tomnomnom/waybackurls@latest",   # сбор исторических URL
        "github.com/lc/gau/v2/cmd/gau@latest",        # сбор исторических URL (доп. источники)
        "github.com/sensepost/gowitness@latest",      # массовые скриншоты хостов
        "github.com/PentestPad/subzy@latest",          # детект subdomain takeover
        "github.com/gitleaks/gitleaks/v8@latest",      # поиск секретов в коде
    ]

    for tool in go_tools:
        print(f"Устанавливаю: {tool}")
        cmd = f"go install {tool}"
        if run(cmd, "Go tools", tool):
            print(f"✓ Успешно: {tool}")
        else:
            print(f"✗ Ошибка установки: {tool}")


def setup_go_path():
    """Определяет каталог GOPATH/bin и печатает подсказку по добавлению в PATH.
    Возвращает путь к go_bin или None, если Go недоступен."""
    print_header("Настройка PATH для Go-инструментов...")

    if not binary_exists("go"):
        print("✗ Go не найден, пропускаем настройку PATH")
        return None

    result = run(["go", "env", "GOPATH"], "Go PATH", "go env GOPATH",
                 shell=False, check_output=True)
    if not result:
        print("Ошибка при определении Go PATH")
        return None

    go_path = result.stdout.strip()
    go_bin = os.path.join(go_path, "bin")

    if not os.path.exists(go_bin):
        print(f"Каталог {go_bin} пока не создан (возможно, go install ещё не запускался)")
        return go_bin

    print(f"Go bin directory: {go_bin}")

    current_path = os.environ.get("PATH", "")
    if go_bin in current_path:
        print("✓ Go bin уже добавлен в PATH")
        return go_bin

    print("Добавьте этот путь в переменную окружения PATH:")
    print(f'  export PATH="$PATH:{go_bin}"')
    print("Добавьте эту строку в файл ~/.bashrc или ~/.zshrc для постоянного эффекта")

    return go_bin


def print_venv_activation_info(venv_dir):
    """Печатает инструкцию по активации виртуального окружения (без записи в файл)"""
    print_header("Инструкция по активации виртуального окружения:")

    print("\nДля активации виртуального окружения выполните:")
    print(f"source {venv_dir}/bin/activate")
    print("\nДля деактивации выполните:")
    print("deactivate")


# ---------------------------------------------------------------------------
# Итоговые отчёты
# ---------------------------------------------------------------------------

def print_installed_tools_summary():
    print("\n✓ Установленные инструменты:")
    print("  РАЗВЕДКА (Reconnaissance):")
    print("    - theHarvester — сбор информации о доменах")
    print("    - assetfinder, subfinder — поиск поддоменов (Go)")
    print("    - subzy — детект subdomain takeover (Go)")
    print("    - waybackurls, gau — сбор исторических URL (Go)")
    print("    - gowitness — массовые скриншоты хостов (Go)")
    print("  ")
    print("  СКАНИРОВАНИЕ УЯЗВИМОСТЕЙ:")
    print("    - nuclei — темплейт-базированное сканирование (Go)")
    print("    - nikto — веб-сканер")
    print("    - Metasploit — фреймворк для эксплуатации уязвимостей (опционально)")
    print("  ")
    print("  CMS:")
    print("    - WPScan — сканер WordPress (gem)")
    print("    - CMSeeK, droopescan — определение и анализ CMS")
    print("  ")
    print("  WORDLISTS:")
    print("    - SecLists — коллекции словарей для брутфорса (опционально)")
    print("  ")
    print("  АНАЛИЗ JAVASCRIPT & SECRETS:")
    print("    - SecretFinder — поиск API-ключей в JS")
    print("    - Pinkerton — анализ JS на уязвимости")
    print("    - trufflehog, gitleaks — поиск credentials в коде")
    print("  ")
    print("  FUZZING & BRUTE FORCE:")
    print("    - ffuf — быстрый HTTP fuzzer (Go)")
    print("    - feroxbuster — перебор путей")
    print("    - dirsearch — поиск скрытых папок")
    print("  ")
    print("  СПЕЦИАЛИЗИРОВАННЫЕ СКАНЕРЫ:")
    print("    - sqlmap — SQL-инъекции")
    print("    - XSStrike, dalfox — XSS-уязвимости")
    print("    - SSRFmap — SSRF-уязвимости")
    print("    - LFI Scanner, Lfi-Space — Local File Inclusion")
    print("  ")
    print("  ДОПОЛНИТЕЛЬНО:")
    print("    - nuclei-templates — готовые шаблоны сканирования")


def print_recommended_workflow():
    print("\nРЕКОМЕНДУЕМЫЙ WORKFLOW для Bug Bounty:")
    print("  1. Разведка: theHarvester → subfinder → assetfinder → httpx")
    print("  2. Проверка takeover: subzy")
    print("  3. Поиск секретов: SecretFinder → trufflehog → gitleaks")
    print("  4. Fuzzing: ffuf → feroxbuster → dirsearch (с использованием SecLists)")
    print("  5. Сканирование: nuclei → nikto")
    print("  6. Эксплуатация: Metasploit для известных уязвимостей")


def print_failures_report():
    print("\n" + "=" * 70)
    if not FAILURES:
        print("✓ Все шаги установки завершились без ошибок.")
        return
    print(f"⚠ Обнаружено {len(FAILURES)} ошибок/предупреждений в процессе установки:")
    print("=" * 70)
    for stage, item, error in FAILURES:
        short_error = error if len(error) < 200 else error[:200] + "..."
        print(f"  [{stage}] {item}: {short_error}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Подготовка окружения для Bug Bounty / пентестинга."
    )
    parser.add_argument(
        "--package-manager", choices=["apt", "dnf", "yum", "pacman", "zypper"],
        help="Явно указать пакетный менеджер (пропускает автоопределение и вопрос)",
    )
    parser.add_argument(
        "--venv-dir", default="venv",
        help="Имя каталога для виртуального окружения (по умолчанию: venv)",
    )
    parser.add_argument(
        "--skip-venv", action="store_true",
        help="Не создавать виртуальное окружение Python",
    )
    parser.add_argument(
        "--install-seclists", action="store_true",
        help="Установить SecLists без вопроса",
    )
    parser.add_argument(
        "--install-metasploit", action="store_true",
        help="Установить Metasploit Framework без вопроса",
    )
    parser.add_argument(
        "--non-interactive", "-y", action="store_true",
        help="Не задавать вопросы; использовать автоопределение и флаги выше",
    )
    return parser.parse_args()


def main():
    """Основная функция"""
    args = parse_args()
    show_banner()

    check_linux_system()
    check_sudo_access()

    # --- Пакетный менеджер ---
    if args.package_manager:
        package_manager = args.package_manager
        print(f"\n✓ Пакетный менеджер задан вручную: {package_manager}")
    else:
        auto_pm = detect_linux_package_manager()
        if auto_pm != "unknown":
            print(f"\n✓ Автоматически определён пакетный менеджер: {auto_pm}")
            if args.non_interactive:
                package_manager = auto_pm
            else:
                use_auto_pm = input("Использовать его? (y/n): ").strip().lower()
                package_manager = auto_pm if use_auto_pm == "y" else ask_package_manager()
        else:
            print("\nНе удалось определить пакетный менеджер автоматически.")
            if args.non_interactive:
                print("Неинтерактивный режим без --package-manager — выходим.")
                sys.exit(1)
            package_manager = ask_package_manager()

    print(f"\n✓ Выбран пакетный менеджер: {package_manager}")

    # --- Опциональные компоненты ---
    install_seclists_flag = args.install_seclists
    install_metasploit_flag = args.install_metasploit

    if not args.non_interactive:
        print("\n" + "-" * 50)
        if not install_seclists_flag:
            install_seclists_flag = input(
                "Установить SecLists (коллекция wordlists)? (y/n): "
            ).strip().lower() == "y"

        print("\n" + "-" * 50)
        if not install_metasploit_flag:
            install_metasploit_flag = input(
                "Установить Metasploit Framework? (y/n): "
            ).strip().lower() == "y"

    # --- Установка системных пакетов СНАЧАЛА (включая python3-venv) ---
    install_system_packages(package_manager)
    install_ruby_tools()

    # --- venv создаём ПОСЛЕ системных зависимостей ---
    venv_dir = None
    if not args.skip_venv:
        venv_dir = create_virtual_environment(args.venv_dir)
        if not venv_dir:
            print("Не удалось создать виртуальное окружение. Продолжаем без него...")

    create_folders()
    download_tools(venv_dir)
    setup_go_tools()
    go_bin = setup_go_path()

    if install_seclists_flag:
        install_seclists()

    if install_metasploit_flag:
        install_metasploit(package_manager)

    if venv_dir:
        install_python_requirements(venv_dir)
        print_venv_activation_info(venv_dir)

    # --- Итоги ---
    print_header("✓ УСТАНОВКА ЗАВЕРШЕНА!")

    if venv_dir:
        print(f"\n✓ Виртуальное окружение создано в папке: {venv_dir}")
        print(f"✓ Для активации окружения выполните: source {venv_dir}/bin/activate")
        print("✓ Для деактивации: deactivate")

    print("\n✓ Инструменты скачаны в соответствующие папки (см. отчёт об ошибках ниже).")
    print(f"\n✓ Использованный пакетный менеджер: {package_manager}")

    if go_bin:
        print("\n" + "-" * 50)
        print("GO-ИНСТРУМЕНТЫ:")
        print("-" * 50)
        print(f'export PATH="$PATH:{go_bin}"')
        print("Добавьте строку выше в ~/.bashrc или ~/.zshrc для постоянного эффекта.")

    if install_seclists_flag:
        print("\n✓ SecLists установлены в папке Wordlists/SecLists")
        print("  Для использования в других инструментах: /usr/share/seclists")

    if install_metasploit_flag:
        print("\n✓ Metasploit Framework установлен")
        print("  Для запуска: msfconsole")
        print("  Для инициализации БД: sudo msfdb init")
        print("  Для проверки статуса БД: msfdb status")

    print_installed_tools_summary()
    print_recommended_workflow()
    print_failures_report()

    print("\n" + "=" * 70)
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nУстановка прервана пользователем.")
        print_failures_report()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Непредвиденная ошибка: {e}")
        print_failures_report()
        sys.exit(1)
