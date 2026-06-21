# BugBounty-script

`main.py` — установочный скрипт, который готовит рабочее окружение для Bug Bounty / пентестинга на Linux: ставит системные зависимости, создаёт виртуальное окружение Python, скачивает и раскладывает по папкам набор открытых инструментов разведки и сканирования.

## Что делает `main.py`

- Проверяет, что скрипт запущен на Linux, и завершает работу с понятной ошибкой, если нет.
- Проверяет доступность `sudo` (если скрипт запущен не от root).
- Определяет пакетный менеджер (`apt`, `dnf`, `yum`, `pacman`, `zypper`) автоматически, с возможностью подтвердить/выбрать вручную или задать флагом.
- Устанавливает системные зависимости и инструменты одним проходом (git, python3, curl, golang, nmap, nikto, ruby, ffuf и др.) — без повторного `update` пакетного менеджера.
- Ставит WPScan через `gem` (Ruby уже есть в системных зависимостях).
- Создаёт виртуальное окружение Python (`venv`) **после** установки системных пакетов — на Debian/Ubuntu для этого нужен пакет `python3-venv`, который ставится на предыдущем шаге.
- Создаёт структуру папок для инструментов (Web_catalog, Subdomains, Scaner, CMS, SSRF, Open_redirect, LFI, XSS, SQLj, JS, Dorks, Reconnaissance, Secrets, Nuclei_Templates, Wordlists).
- Клонирует инструменты с GitHub в соответствующие директории.
- Устанавливает Go-инструменты через `go install` и печатает подсказку по добавлению `GOPATH/bin` в `PATH`.
- Устанавливает SecLists (опционально) и пытается создать символическую ссылку `/usr/share/seclists`.
- Устанавливает Metasploit Framework (опционально): скачивает официальный установщик, проверяет, что файл не пустой, запускает установку и инициализирует БД (`msfdb`); при сбое пробует поставить через пакетный менеджер.
- Устанавливает общие Python-пакеты в venv и зависимости из всех найденных `requirements.txt`.
- В конце печатает сводный отчёт обо всех шагах, которые завершились с ошибкой — вместо того чтобы искать их по логу вручную.

## Пререквизиты

- Linux с одним из пакетных менеджеров: `apt`, `dnf`, `yum`, `pacman`, `zypper`.
- Python 3.x.
- Интернет-соединение.
- Права `sudo` для установки системных пакетов (либо запуск от root).

## Как запустить

Интерактивный режим (скрипт сам спросит про пакетный менеджер, SecLists и Metasploit):

```bash
python3 main.py
```

Неинтерактивный режим — без вопросов, для автоматизации/CI:

```bash
python3 main.py --non-interactive --package-manager apt --install-seclists --install-metasploit
```

### Доступные флаги

| Флаг | Описание |
|---|---|
| `--package-manager {apt,dnf,yum,pacman,zypper}` | Задать пакетный менеджер вручную, без автоопределения и вопроса |
| `--venv-dir DIR` | Имя каталога для виртуального окружения (по умолчанию `venv`) |
| `--skip-venv` | Не создавать виртуальное окружение Python |
| `--install-seclists` | Установить SecLists без вопроса |
| `--install-metasploit` | Установить Metasploit Framework без вопроса |
| `--non-interactive`, `-y` | Не задавать никаких вопросов, использовать автоопределение и флаги выше |

## После выполнения вы получите

- Виртуальное окружение `venv` (если не передан `--skip-venv`); инструкция по активации/деактивации печатается в консоль.
- Набор папок с клонированными инструментами.
- Установленные (или частично установленные при ошибках) системные, Ruby- и Go-инструменты.
- Подсказку в консоли, как добавить `GOPATH/bin` в `PATH`, если он туда ещё не входит.
- Сводку в конце вывода: что установлено, рекомендуемый workflow и список ошибок (если есть).

## Структура папок

| Папка | Назначение |
|---|---|
| `Web_catalog` | перебор директорий/файлов, поиск параметров |
| `Subdomains` | поиск поддоменов |
| `Scaner` | сканеры уязвимостей общего назначения |
| `CMS` | определение и анализ CMS (WordPress, Drupal, Joomla и др.) |
| `SSRF` | обнаружение SSRF |
| `Open_redirect` | проверка открытых редиректов |
| `LFI` | Local File Inclusion |
| `XSS` | поиск и fuzzing XSS |
| `SQLj` | SQL-инъекции |
| `JS` | анализ JavaScript, поиск секретов в коде фронтенда |
| `Dorks` | dork-запросы |
| `Reconnaissance` | разведка (домены, email и т.д.) |
| `Secrets` | поиск credentials в репозиториях |
| `Nuclei_Templates` | шаблоны для `nuclei` |
| `Wordlists` | словари для брутфорса (в т.ч. SecLists) |

## Инструменты, которые скачивает/устанавливает `main.py`

### Git-репозитории по категориям

- **Web_catalog**: [dirsearch](https://github.com/maurosoria/dirsearch), [ParamSpider](https://github.com/0xKayala/ParamSpider)
- **Subdomains**: [subscraper](https://github.com/m8sec/subscraper)
- **Open_redirect**: [openredirex](https://github.com/devanshbatham/openredirex)
- **Scaner**: [lostools](https://github.com/coffinsp/lostools), [PenHunter](https://github.com/cc1a2b/PenHunter), [argus](https://github.com/jasonxtn/argus), [xlsNinja](https://github.com/atoz-chevara/xlsNinja), [nuclei](https://github.com/projectdiscovery/nuclei)
- **LFI**: [LFIscanner](https://github.com/R3LI4NT/LFIscanner), [Lfi-Space](https://github.com/capture0x/Lfi-Space)
- **SQLj**: [SQL-Injection-Finder](https://github.com/j1t3sh/SQL-Injection-Finder), [sqlmap](https://github.com/sqlmapproject/sqlmap)
- **XSS**: [XSStrike](https://github.com/s0md3v/XSStrike)
- **SSRF**: [SSRFmap](https://github.com/swisskyrepo/SSRFmap)
- **JS**: [Pinkerton](https://github.com/000pp/Pinkerton), [SecretFinder](https://github.com/m4ll0k/SecretFinder)
- **CMS**: [CMSeeK](https://github.com/Tuhinshubhra/CMSeeK), [droopescan](https://github.com/droope/droopescan)
- **Dorks**: [github-dorks](https://github.com/techgaun/github-dorks)
- **Reconnaissance**: [theHarvester](https://github.com/laramies/theHarvester)
- **Secrets**: [trufflehog](https://github.com/trufflesecurity/trufflehog)
- **Nuclei_Templates**: [nuclei-templates](https://github.com/projectdiscovery/nuclei-templates)
- **Wordlists**: [SecLists](https://github.com/danielmiessler/SecLists) — опционально, по флагу/вопросу

### Go-инструменты (`go install`)

- [assetfinder](https://github.com/tomnomnom/assetfinder) — поиск связанных доменов
- [dalfox](https://github.com/hahwul/dalfox) — обнаружение XSS
- [katana](https://github.com/projectdiscovery/katana) — краулер
- [jshunter](https://github.com/cc1a2b/jshunter) — анализ JS
- [subfinder](https://github.com/projectdiscovery/subfinder) — пассивный поиск поддоменов
- [nuclei](https://github.com/projectdiscovery/nuclei) — шаблонное сканирование
- [httpx](https://github.com/projectdiscovery/httpx) — проверка HTTP-доступности/заголовков
- [wpprobe](https://github.com/Chocapikk/wpprobe) — обнаружение WordPress
- [waybackurls](https://github.com/tomnomnom/waybackurls) — сбор исторических URL из архивов
- [gau](https://github.com/lc/gau) — сбор исторических URL (доп. источники)
- [gowitness](https://github.com/sensepost/gowitness) — массовые скриншоты хостов
- [subzy](https://github.com/PentestPad/subzy) — детект subdomain takeover
- [gitleaks](https://github.com/gitleaks/gitleaks) — поиск секретов в коде

### Ruby (`gem`)

- [WPScan](https://github.com/wpscanteam/wpscan) — сканер уязвимостей WordPress

### Системные пакеты (через пакетный менеджер)

- **nmap** — сетевой сканер портов и сервисов
- **ffuf** — быстрый HTTP fuzzer
- **feroxbuster** — перебор директорий
- **nikto** — веб-сканер уязвимостей сервера
- **Metasploit Framework** — платформа для эксплуатации (опционально, через официальный установщик Rapid7)
- **rustscan** — быстрый сканер портов на Rust (опционально, через COPR для `dnf`)

## Рекомендуемый workflow для Bug Bounty

1. Разведка: `theHarvester` → `subfinder` → `assetfinder` → `httpx`
2. Проверка takeover: `subzy`
3. Поиск секретов: `SecretFinder` → `trufflehog` → `gitleaks`
4. Fuzzing: `ffuf` → `feroxbuster` → `dirsearch` (с использованием SecLists)
5. Сканирование: `nuclei` → `nikto`
6. Эксплуатация: `Metasploit` для известных уязвимостей

## Важно

Используйте установленный набор инструментов только в рамках законных и согласованных тестов (authorized testing, программы bug bounty со scope). Скрипт автоматизирует установку мощных инструментов, неправильное или несанкционированное использование которых может привести к нарушению закона.
