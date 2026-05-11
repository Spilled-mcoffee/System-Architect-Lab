# System Architect Lab

**Team:** Ahmed Cheikh and Varha Mohamed Mahmoud  
**Course:** Introduction to Operating Systems - LIU 2026  
**Theme:** Linux administration, CPU scheduling and Docker containerization

---

## 1. Project Overview

This repository contains the implementation of the **System Architect Lab** mini-project. The project combines three main technical components:

1. **Bash automation** for Linux system administration.
2. **CPU scheduling simulation** comparing Round Robin and SRTF.
3. **Docker infrastructure** using a custom Debian image, MySQL, Apache and automated CRUD operations.

The latest version of the project executes both the Bash administration script and the Python scheduling simulator from inside the Docker-based Debian environment. This makes testing safer, more reproducible and closer to a real lab setup.

---

## 2. Repository Structure

```text
System-Architect-Lab/
│
├── bash/
│   └── admin_systeme.sh
│
├── scheduling/
│   └── scheduling.py
│
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile.debian
│
├── sql/
│   └── crud.sql
│
├── scripts/
│   └── run_crud.sh
│
├── web/
│   └── index.html
│
├── README.md
├── README_FR.md
└── .gitignore
```

---

## 3. Components

### 3.1 Bash Automation

The Bash script is located in:

```text
bash/admin_systeme.sh
```

It automates the following tasks:

- Root privilege verification.
- User account creation.
- Workspace directory creation.
- Ownership configuration with `chown`.
- Permission configuration with `chmod 700`.
- Disk quota simulation.

The script is tested inside the Debian container instead of directly on the host machine. This prevents accidental modification of the host system.

---

### 3.2 CPU Scheduling Simulation

The Python simulation is located in:

```text
scheduling/scheduling.py
```

It implements and compares:

- **Round Robin** with a fixed quantum.
- **SRTF** - Shortest Remaining Time First.

The program displays:

- Gantt-style execution output.
- Waiting time for each process.
- Turnaround time for each process.
- Average waiting time comparison.

The script is executed inside the custom Debian Docker container, where Python is already installed.

---

### 3.3 Docker Infrastructure

The Docker environment contains three services:

| Service | Role |
|---|---|
| `debian_lab` | Custom Debian lab environment for Bash and Python testing |
| `mysql_server` | MySQL database service for the `etudiants` database |
| `apache_server` | Apache HTTP server serving a custom web page |

The infrastructure is defined in:

```text
docker/docker-compose.yml
```

The custom Debian image is defined in:

```text
docker/Dockerfile.debian
```

---

## 4. Custom Debian Image

The project uses a custom Debian image to avoid installing tools manually after every container recreation.

The Dockerfile installs:

- `python3`
- `passwd`
- `procps`
- `iproute2`
- `iputils-ping`
- `nano`

This allows the Debian container to run:

- The Bash administration script.
- The Python scheduling simulation.
- Basic Linux diagnostic commands.

Relevant Compose section:

```yaml
debian_lab:
  build:
    context: .
    dockerfile: Dockerfile.debian
  image: system-architect-debian:1.0
  container_name: debian_lab
  tty: true
  stdin_open: true
  volumes:
    - ../bash:/lab/bash
    - ../scheduling:/lab/scheduling
```

---

## 5. Starting the Infrastructure

From the project root:

```bash
cd docker
```

Build and start the services:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

Expected services:

```text
debian_lab
mysql_server
apache_server
```

---

## 6. Testing the Debian Lab Container

Enter the Debian container:

```bash
docker exec -it debian_lab bash
```

Verify Python is installed:

```bash
python3 --version
```

Check the mounted project folders:

```bash
ls -la /lab/bash
ls -la /lab/scheduling
```

Exit the container:

```bash
exit
```

---

## 7. Running the Bash Automation Script inside Docker

Enter the Debian container:

```bash
docker exec -it debian_lab bash
```

Run the script:

```bash
bash /lab/bash/admin_systeme.sh
```

Example test username:

```text
testuser
```

Verify the created user:

```bash
id testuser
```

Verify the workspace permissions:

```bash
ls -ld /home/testuser/workspace
```

Expected permission style:

```text
drwx------
```

Exit the container:

```bash
exit
```

---

## 8. Running the Python Scheduling Simulation inside Docker

Enter the Debian container:

```bash
docker exec -it debian_lab bash
```

Run the scheduling program:

```bash
python3 /lab/scheduling/scheduling.py
```

Exit:

```bash
exit
```

---

## 9. MySQL CRUD Automation

The SQL CRUD file is located in:

```text
sql/crud.sql
```

The automation script is located in:

```text
scripts/run_crud.sh
```

From the project root, run:

```bash
./scripts/run_crud.sh
```

The script executes the SQL file inside the MySQL container and performs:

- Table creation.
- Data insertion.
- Data reading.
- Data update.
- Data deletion.
- Final read verification.

---

## 10. MySQL Port and Persistent Volume

The MySQL container uses this port mapping:

```yaml
ports:
  - "3307:3306"
```

This means:

```text
Host port 3307 -> Container port 3306
```

Port `3307` is used to avoid conflict with a local MySQL service running on port `3306`.

The MySQL service also uses a persistent Docker volume:

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

This keeps database files outside the temporary lifecycle of the container. Running `docker compose down` stops and removes containers but keeps the volume. Running `docker compose down -v` removes the volume and should be used only when intentionally resetting the database.

---

## 11. Apache HTTP Server

The Apache service exposes container port `80` on host port `8080`:

```yaml
ports:
  - "8080:80"
```

The custom web page is stored in:

```text
web/index.html
```

It is mounted into Apache using:

```yaml
volumes:
  - ../web:/usr/local/apache2/htdocs
```

Open the service in a browser:

```text
http://localhost:8080
```

---

## 12. Stopping the Infrastructure

From the `docker/` folder:

```bash
docker compose down
```

To remove containers and volumes, use only if a full reset is required:

```bash
docker compose down -v
```

---

## 13. Git Workflow

After modifying files, push updates with:

```bash
git status
git add .
git commit -m "Update project files"
git push
```

If the remote repository has changes that are not local, use:

```bash
git pull --rebase origin main
git push
```

---

## 14. Demonstration Checklist

A complete demonstration should show:

1. Repository structure.
2. Docker Compose build and startup.
3. Running containers with `docker compose ps`.
4. Bash script execution inside `debian_lab`.
5. Python scheduling execution inside `debian_lab`.
6. Apache page at `http://localhost:8080`.
7. CRUD automation using `./scripts/run_crud.sh`.
8. Explanation of the persistent MySQL volume.

---

## 15. Team

- Ahmed Cheikh
- Varha Mohamed Mahmoud
