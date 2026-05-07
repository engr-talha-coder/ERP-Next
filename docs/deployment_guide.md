# Deployment Guide — facilities_ops

## Overview

This guide covers deploying the `facilities_ops` custom Frappe app on ERPNext v15.

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| MariaDB | 10.6+ |
| Redis | 6+ |
| ERPNext | v15 |
| frappe-bench | Latest |

---

## Step 1: Set Up Bench

```bash
export BENCH_DIR=/home/frappe/frappe-bench
export FRAPPE_BRANCH=version-15
bash install/01_setup_bench.sh
```

This script:
- Installs `frappe-bench` via pip
- Initialises a new bench in `BENCH_DIR`
- Fetches the ERPNext app

---

## Step 2: Create a Site

```bash
export SITE_NAME=facilities.local
export ADMIN_PASSWORD=SecurePassword123
export DB_ROOT_PASSWORD=mysql_root_password
bash install/02_create_site.sh
```

---

## Step 3: Install Apps

```bash
export APP_PATH=/path/to/facilities_ops
bash install/03_install_apps.sh
```

This installs both `erpnext` and `facilities_ops` on the site and runs `bench migrate`.

---

## Step 4: Configure Base Masters

```bash
cd /home/frappe/frappe-bench
bench --site facilities.local execute facilities_ops.setup.install.after_install
```

Or run the standalone script:

```bash
export FRAPPE_SITE=facilities.local
python install/04_configure_base.py
```

---

## Step 5: Import Fixtures

Fixtures are automatically loaded during `bench migrate`. To reload manually:

```bash
bench --site facilities.local import-fixtures --app facilities_ops
```

---

## Step 6: Verify Installation

```bash
export SITE_NAME=facilities.local
bash scripts/verify_install.sh
```

---

## Production Checklist

- [ ] Set `developer_mode = 0` in `site_config.json`
- [ ] Configure email settings in System Settings
- [ ] Enable Scheduler: `bench --site <site> enable-scheduler`
- [ ] Set up SSL via `bench setup lets-encrypt <site>`
- [ ] Configure backups: `bench --site <site> add-to-hosts`
- [ ] Set `workers` configuration in `Procfile`
- [ ] Review and tighten Role permissions

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BENCH_DIR` | `/home/frappe/frappe-bench` | Bench root directory |
| `SITE_NAME` | `facilities.local` | Frappe site name |
| `FRAPPE_BRANCH` | `version-15` | Frappe git branch |
| `ADMIN_PASSWORD` | `admin` | Site admin password |
| `DB_ROOT_PASSWORD` | *(prompt)* | MariaDB root password |
| `APP_PATH` | *(required)* | Path to `facilities_ops` app |

---

## Upgrading

```bash
cd /home/frappe/frappe-bench
bench update --reset
bench --site facilities.local migrate
```

---

## Troubleshooting

### Migrate fails with "No module named facilities_ops"
Ensure the app is in `apps/` directory:
```bash
bench get-app facilities_ops /path/to/facilities_ops
```

### Fixtures not loading
```bash
bench --site facilities.local import-fixtures --app facilities_ops
```

### Scheduler not running
```bash
bench --site facilities.local enable-scheduler
bench start  # in development
# or in production:
sudo supervisorctl restart all
```
