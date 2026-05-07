# System Architect Lab

This repository contains the deliverables for the **System Architect Lab** mini-project in Operating Systems. The project combines Linux administration, CPU scheduling simulation, and Docker-based service deployment.

## Project Objectives

The project is divided into three main technical parts:

1. **Shell Automation with Bash**
   - Automate user creation.
   - Prepare a secure workspace directory.
   - Configure ownership and permissions.
   - Simulate disk quota assignment.

2. **CPU Scheduling Modeling**
   - Implement and compare Round Robin and SRTF scheduling algorithms.
   - Generate Gantt chart traces.
   - Calculate average waiting time.

3. **Docker Infrastructure and Containerization**
   - Deploy a Debian Linux lab container.
   - Deploy a MySQL database container.
   - Deploy an Apache HTTP server container.
   - Use a persistent MySQL volume.
   - Automate CRUD operations through a Bash script and SQL file.

## Repository Structure

```text
System-Architect-Lab/
├── Docker/
│   └── docker-compose.yml
├── bash/
│   └── admin_systeme.sh
├── scheduling/
│   └── scheduling.py
├── scripts/
│   └── run_crud.sh
├── sql/
│   └── crud.sql
├── web/
│   └── index.html
└── README.md
```

## Requirements

Before running the project, make sure the following tools are installed and available:

- Docker Desktop or Docker Engine
- Docker Compose
- Python 3
- Bash shell
- A terminal emulator
- A web browser

## 1. Bash Automation

The Bash script is located at:

```text
bash/admin_systeme.sh
```

### Make the script executable

```bash
chmod +x bash/admin_systeme.sh
```

### Run the script

```bash
sudo ./bash/admin_systeme.sh
```

The script must be executed with administrator privileges because user creation and permission management require root access.

### Main operations

The script performs the following actions:

- Checks whether it is being executed as root.
- Reads the username to create.
- Verifies whether the user already exists.
- Creates the user with a home directory.
- Sets the user password.
- Creates a workspace directory.
- Applies ownership with `chown`.
- Applies secure permissions with `chmod 700`.
- Displays a summary of the configuration.

## 2. CPU Scheduling Simulation

The scheduling program is located at:

```text
scheduling/scheduling.py
```

### Run the program

```bash
python3 scheduling/scheduling.py
```

### Implemented algorithms

- **Round Robin** with a quantum of 2 time units.
- **SRTF** (Shortest Remaining Time First).

### Output

The program displays:

- Gantt chart traces.
- Waiting time for each process.
- Turnaround time for each process.
- Average waiting time.
- Analytical comparison between Round Robin and SRTF.

## 3. Docker Infrastructure

The Docker Compose file is located at:

```text
Docker/docker-compose.yml
```

### Start the infrastructure

From the `Docker/` directory, run:

```bash
cd Docker
docker compose up -d
```

If your system uses the older Compose command, use:

```bash
docker-compose up -d
```

### Stop the infrastructure

```bash
docker compose down
```

To remove orphan containers as well:

```bash
docker compose down --remove-orphans
```

Do not use `docker compose down -v` unless you intentionally want to delete the MySQL volume and reset the database data.

## Docker Services

The stack contains three services:

| Service | Image | Role | Port / Storage |
|---|---|---|---|
| `debian_lab` | `debian:stable-slim` | Linux testing environment | Interactive terminal |
| `mysql_server` | `mysql:8.0` | MySQL database | `3307:3306` + `mysql_data` volume |
| `apache_server` | `httpd:latest` | Apache HTTP server | `8080:80` + `web` bind mount |

## Apache HTTP Server

The Apache server is available from the host machine at:

```text
http://localhost:8080
```

The custom web page is located at:

```text
web/index.html
```

It is mounted into the Apache container using:

```yaml
volumes:
  - ../web:/usr/local/apache2/htdocs
```

This means that the local `web/` folder replaces Apache's default website directory inside the container.

## MySQL Database

The MySQL container creates a database named:

```text
etudiants
```

The root password used in the project is:

```text
root123
```

The host port is `3307` because port `3306` may already be used by a local MySQL service.

### Connect to MySQL from inside the container

```bash
docker exec -it mysql_server mysql -u root -p
```

Password:

```text
root123
```

### Connect to MySQL from the host machine

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p
```

Password:

```text
root123
```

## Persistent MySQL Volume

The MySQL service uses the following named volume:

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

The `/var/lib/mysql` directory is where MySQL stores its physical database files. By mounting a persistent Docker volume there, the database state is separated from the lifecycle of the container.

This means:

- The container can be stopped and recreated.
- The MySQL data can remain available.
- The database is not lost unless the volume is explicitly deleted.

To list Docker volumes:

```bash
docker volume ls
```

## Automated CRUD Operations

The CRUD SQL file is located at:

```text
sql/crud.sql
```

The automation script is located at:

```text
scripts/run_crud.sh
```

### Make the CRUD script executable

```bash
chmod +x scripts/run_crud.sh
```

### Run the CRUD automation

From the project root, run:

```bash
./scripts/run_crud.sh
```

The script checks whether the `mysql_server` container is running, then executes the SQL file inside the MySQL container.

### CRUD operations included

| Operation | SQL Example | Purpose |
|---|---|---|
| Create | `INSERT INTO etudiants ...` | Add student records |
| Read | `SELECT * FROM etudiants;` | Display records |
| Update | `UPDATE etudiants SET ...` | Modify a record |
| Delete | `DELETE FROM etudiants WHERE ...` | Delete a record |

## Useful Docker Commands

### Check running containers

```bash
docker compose ps
```

### View all containers

```bash
docker ps -a
```

### View Apache logs

```bash
docker logs apache_server
```

### Enter the Debian container

```bash
docker exec -it debian_lab bash
```

Exit with:

```bash
exit
```

### Enter the Apache container

```bash
docker exec -it apache_server bash
```

If Bash is not available:

```bash
docker exec -it apache_server sh
```

## Validation Checklist

Before submitting or recording the demonstration video, verify the following:

- `docker compose ps` shows all three containers as `Up`.
- `http://localhost:8080` shows the custom Apache page.
- `docker exec -it mysql_server mysql -u root -p` connects successfully.
- `./scripts/run_crud.sh` runs without errors.
- `docker volume ls` shows the MySQL volume.
- `python3 scheduling/scheduling.py` displays Gantt charts and average waiting times.
- `sudo ./bash/admin_systeme.sh` performs the expected Linux administration tasks.

## Suggested Demonstration Flow

A 3-minute demonstration video can follow this order:

1. Show the project directory structure.
2. Show the `docker-compose.yml` file.
3. Start the stack with `docker compose up -d`.
4. Verify services with `docker compose ps`.
5. Open `http://localhost:8080` and show the Apache page.
6. Run `./scripts/run_crud.sh` and show the SQL output.
7. Open the MySQL container and show the `etudiants` database.
8. Briefly explain the persistent MySQL volume.
9. Run the scheduling Python script.
10. Mention the Bash administration script.

## Notes

- If port `3306` is already used by local MySQL, keep the Docker mapping as `3307:3306`.
- If Apache does not show the custom page, verify the bind mount path `../web:/usr/local/apache2/htdocs`.
- If Docker Compose warns about orphan containers, run `docker compose down --remove-orphans`.
- If Docker cannot connect to the daemon, ensure Docker Desktop or Docker Engine is running.

## Author

Ahmed Cheikh

## Academic Context

Mini-Project: **System Architect Lab**  
Course: **Introduction to Operating Systems**  
Year: **LIU 2026**
