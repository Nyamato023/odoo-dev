# Odoo Multi-Version Development Environment

A unified development environment for working with multiple Odoo versions (17, 18, and 19) with optional Enterprise addons.

---

# Repository Structure

```text
odoo-dev/
├── .gitignore
│
├── odoo-17/
│   └── enterprise-17.0/
│
├── odoo-18/
│   └── enterprise-18.0/
│
├── odoo-19/
│   └── enterprise-19.0/
│
├── 17.conf
├── 18.conf
└── 19.conf
```

## Directory Description

| Directory/File     | Description                   |
| ------------------ | ----------------------------- |
| `odoo-17/`         | Odoo 17 Community source code |
| `enterprise-17.0/` | Odoo 17 Enterprise addons     |
| `odoo-18/`         | Odoo 18 Community source code |
| `enterprise-18.0/` | Odoo 18 Enterprise addons     |
| `odoo-19/`         | Odoo 19 Community source code |
| `enterprise-19.0/` | Odoo 19 Enterprise addons     |
| `17.conf`          | Odoo 17 configuration         |
| `18.conf`          | Odoo 18 configuration         |
| `19.conf`          | Odoo 19 configuration         |

---

# Prerequisites

Before starting, install the following:

* Python 3.10+
* PostgreSQL 14+
* Git
* Node.js 18+ (required for newer Odoo versions)
* pip
* virtualenv (optional)

Verify installations:

```bash
python3 --version
psql --version
node --version
git --version
```
# System Dependencies



Before installing Odoo, install the required system packages.



## Ubuntu / Debian



Update your system:



```bash

sudo apt update

sudo apt upgrade -y

```



Install common dependencies:



```bash

sudo apt install -y \

    git \

    python3 \

    python3-venv \

    python3-pip \

    build-essential \

    libpq-dev \

    postgresql \

    postgresql-contrib \

    nodejs \

    npm \

    xfonts-75dpi \

    xfonts-base

```



---



# Install wkhtmltopdf (Patched Version)



Odoo PDF reports require the patched Qt version of wkhtmltopdf.



Verify your Ubuntu version:



```bash

lsb_release -a

```



Download the appropriate package from the wkhtmltopdf packaging releases:



```bash

wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb

```



Install:



```bash

sudo apt install ./wkhtmltox_0.12.6.1-3.jammy_amd64.deb

```



Verify installation:



```bash

wkhtmltopdf --version

```



Expected output:



```text

wkhtmltopdf 0.12.6.1 (with patched qt)

```



**Important:** The output must include:



```text

(with patched qt)

```



If it does not, PDF generation may fail or produce incorrect reports.



---


---

# Clone the Repository

```bash
git clone <repository-url>
cd odoo-dev
```

---

# PostgreSQL Setup

Create a PostgreSQL user for Odoo:

```bash
sudo -u postgres createuser -s odoo
sudo -u postgres psql
```

Set a password:

```sql
ALTER USER odoo WITH PASSWORD 'odoo';
\q
```

Create development databases:

```bash
createdb -O odoo odoo17
createdb -O odoo odoo18
createdb -O odoo odoo19
```

---

# Installing Odoo

This repository uses a **single Python virtual environment** shared across all supported Odoo versions.

## Create the Virtual Environment

From the repository root:

```bash
cd odoo-dev

python3 -m venv .venv
source .venv/bin/activate
```

Upgrade packaging tools:

```bash
pip install --upgrade pip setuptools wheel
```

## Install Dependencies

Install the requirements for all supported Odoo versions:

```bash
pip install -r odoo-17/requirements.txt
pip install -r odoo-18/requirements.txt
pip install -r odoo-19/requirements.txt
```

This ensures that the shared virtual environment contains all Python packages required to run any supported Odoo version.

## Verify Installation

```bash
pip list
```

You should see the required Odoo dependencies installed successfully.

---

# Activating the Environment
# Installing Odoo

Each version should have its own Python virtual environment.

## Odoo 17

```bash
cd odoo-17

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip wheel setuptools

pip install -r requirements.txt
```

## Odoo 18

```bash
cd odoo-18

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip wheel setuptools

pip install -r requirements.txt
```

## Odoo 19

```bash
cd odoo-19

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip wheel setuptools

pip install -r requirements.txt
```

---

Whenever you start working on the project:

```bash
cd odoo-dev
source .venv/bin/activate
```

---

# Running Odoo

## Odoo 17

```bash
cd odoo-17

python odoo-bin -c ../17.conf
```

## Odoo 18

```bash
cd odoo-18

python odoo-bin -c ../18.conf
```

## Odoo 19

```bash
cd odoo-19

python odoo-bin -c ../19.conf
```

The same virtual environment is used for all versions.

# Enterprise Setup

Enterprise repositories require a valid Odoo Enterprise subscription.

Clone Enterprise inside the corresponding version directory.

Example:

```bash
cd odoo-18

git clone git@github.com:odoo/enterprise.git enterprise-18.0
```

Checkout the matching branch:

```bash
cd enterprise-18.0
git checkout 18.0
```

Repeat for other versions.

---


# Configuration

Each version has a dedicated configuration file.

Example `18.conf`:

```ini
[options]

admin_passwd = admin

db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo

http_port = 8069

addons_path =
    odoo-18/addons,
    odoo-18/enterprise-18.0,
    odoo-18/custom/addons
```

Update:

* Database credentials
* Ports
* Addons paths

as required by your environment.

---

# Running Odoo

## Odoo 17

```bash
cd odoo-17

source .venv/bin/activate

python odoo-bin -c ../17.conf
```

Access:

```text
http://localhost:8069
```

---

## Odoo 18

```bash
cd odoo-18

source .venv/bin/activate

python odoo-bin -c ../18.conf
```

Access:

```text
http://localhost:8070
```

---

## Odoo 19

```bash
cd odoo-19

source .venv/bin/activate

python odoo-bin -c ../19.conf
```

Access:

```text
http://localhost:8071
```

---

# Custom Addons

Recommended structure:

```text
odoo-18/
├── custom/
│   └── addons/
│       └── my_module/
```

Add the path to the configuration file:

```ini
addons_path =
    odoo-18/addons,
    odoo-18/enterprise-18.0,
    odoo-18/custom/addons
```

Update module list:

```bash
python odoo-bin -c ../18.conf -u my_module
```

---



# Common Commands

Update a module:

```bash
python odoo-bin -c ../18.conf -u module_name
```

Install a module:

```bash
python odoo-bin -c ../18.conf -i module_name
```

Run with a specific database:

```bash
python odoo-bin -c ../18.conf -d database_name
```

Enable developer mode from CLI:

```bash
python odoo-bin --dev=all -c ../18.conf
```

---

# Troubleshooting

## PostgreSQL Connection Error

Verify PostgreSQL is running:

```bash
sudo systemctl status postgresql
```

Verify login:

```bash
psql -U odoo -h localhost
```

---

## Missing Python Package

Reinstall requirements:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Port Already In Use

Find the process:

```bash
sudo lsof -i :8069
```

Terminate it:

```bash
kill -9 <PID>
```

---

## Module Not Found

Check:

* `addons_path`
* Module directory structure
* File permissions
* Presence of `__manifest__.py`

---

# Development Recommendations

* Use a separate database per Odoo version.
* Use a dedicated virtual environment per version.
* Keep Enterprise and Community branches aligned.
* Never develop directly on the version branch; create feature branches.

Example:

```bash
git checkout -b feature/customer-statement-report
```

---

# License

* Odoo Community Edition is licensed under LGPL-3.
* Odoo Enterprise Edition requires a valid commercial license from Odoo S.A. 

---

# Support

For Odoo-specific issues:

* Odoo Documentation
* Odoo Partner Support
* Internal development team documentation

Always test upgrades, configuration changes, and custom modules in a development environment before deploying to production.
