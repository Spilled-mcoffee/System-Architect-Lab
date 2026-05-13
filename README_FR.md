# System Architect Lab

**Equipe :** Ahmed Cheikh et Varha Mohamed Mahmoud  
**Cours :** Introduction aux Systemes d'Exploitation - LIU 2026  
**Theme :** Administration Linux, ordonnancement CPU et conteneurisation Docker

---

## 1. Presentation du projet

Ce depot contient l'implementation du mini-projet **System Architect Lab**. Le projet combine trois composants techniques principaux :

1. **Automatisation Bash** pour l'administration systeme Linux.
2. **Simulation d'ordonnancement CPU** avec comparaison entre Round Robin et SRTF.
3. **Infrastructure Docker** utilisant une image Debian personnalisee, MySQL, Apache et des operations CRUD automatisees.

La version actuelle du projet execute le script Bash d'administration et le simulateur Python depuis l'environnement Debian Docker. Cela rend les tests plus surs, plus reproductibles et plus proches d'un laboratoire reel.

---

## 2. Structure du depot

```text
System-Architect-Lab/
│
├── bash/
│   └── admin_systeme.sh
│
├── scheduling/
│   └── scheduling.py
│
├── Docker/
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

## 3. Composants du projet

### 3.1 Automatisation Bash

Le script Bash se trouve dans :

```text
bash/admin_systeme.sh
```

Il automatise les taches suivantes :

- Verification des privileges administrateur.
- Creation d'un compte utilisateur.
- Creation d'un repertoire de travail.
- Configuration du proprietaire avec `chown`.
- Configuration des permissions avec `chmod 700`.
- Simulation d'un quota disque.

Le script est teste dans le conteneur Debian au lieu d'etre execute directement sur la machine hote. Cela evite toute modification accidentelle du systeme hote.

---

### 3.2 Simulation d'ordonnancement CPU

La simulation Python se trouve dans :

```text
scheduling/scheduling.py
```

Elle implemente et compare :

- **Round Robin** avec quantum fixe.
- **SRTF** - Shortest Remaining Time First.

Le programme affiche :

- Une representation d'execution de type Gantt.
- Le temps d'attente de chaque processus.
- Le temps de retour de chaque processus.
- La comparaison du temps d'attente moyen.

Le script est execute dans le conteneur Debian personnalise, ou Python est deja installe.

---

### 3.3 Infrastructure Docker

L'environnement Docker contient trois services :

| Service | Role |
|---|---|
| `debian_lab` | Environnement Debian personnalise pour tester Bash et Python |
| `mysql_server` | Service MySQL pour la base `etudiants` |
| `apache_server` | Serveur HTTP Apache avec page web personnalisee |

L'infrastructure est definie dans :

```text
docker/docker-compose.yml
```

L'image Debian personnalisee est definie dans :

```text
docker/Dockerfile.debian
```

---

## 4. Image Debian personnalisee

Le projet utilise une image Debian personnalisee afin d'eviter l'installation manuelle des outils apres chaque recreation du conteneur.

Le Dockerfile installe :

- `python3`
- `passwd`
- `procps`
- `iproute2`
- `iputils-ping`
- `nano`

Cela permet au conteneur Debian d'executer :

- Le script d'administration Bash.
- La simulation Python d'ordonnancement.
- Des commandes de diagnostic Linux de base.

Section Compose correspondante :

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

## 5. Demarrage de l'infrastructure

Depuis la racine du projet :

```bash
cd docker
```

Construire et demarrer les services :

```bash
docker compose up -d --build
```

Verifier les conteneurs :

```bash
docker compose ps
```

Services attendus :

```text
debian_lab
mysql_server
apache_server
```

---

## 6. Tester le conteneur Debian

Entrer dans le conteneur Debian :

```bash
docker exec -it debian_lab bash
```

Verifier que Python est installe :

```bash
python3 --version
```

Verifier les dossiers montes :

```bash
ls -la /lab/bash
ls -la /lab/scheduling
```

Quitter le conteneur :

```bash
exit
```

---

## 7. Executer le script Bash dans Docker

Entrer dans le conteneur Debian :

```bash
docker exec -it debian_lab bash
```

Executer le script :

```bash
bash /lab/bash/admin_systeme.sh
```

Exemple de nom d'utilisateur de test :

```text
testuser
```

Verifier l'utilisateur cree :

```bash
id testuser
```

Verifier les permissions du workspace :

```bash
ls -ld /home/testuser/workspace
```

Permissions attendues :

```text
drwx------
```

Quitter le conteneur :

```bash
exit
```

---

## 8. Executer la simulation Python dans Docker

Entrer dans le conteneur Debian :

```bash
docker exec -it debian_lab bash
```

Executer le programme :

```bash
python3 /lab/scheduling/scheduling.py
```

Quitter :

```bash
exit
```

---

## 9. Automatisation CRUD MySQL

Le fichier SQL CRUD se trouve dans :

```text
sql/crud.sql
```

Le script d'automatisation se trouve dans :

```text
scripts/run_crud.sh
```

Depuis la racine du projet, executer :

```bash
./scripts/run_crud.sh
```

Le script execute le fichier SQL dans le conteneur MySQL et realise :

- Creation de table.
- Insertion de donnees.
- Lecture de donnees.
- Mise a jour de donnees.
- Suppression de donnees.
- Verification finale.

---

## 10. Port MySQL et volume persistant

Le conteneur MySQL utilise le mapping de port suivant :

```yaml
ports:
  - "3307:3306"
```

Cela signifie :

```text
Port hote 3307 -> port conteneur 3306
```

Le port `3307` est utilise pour eviter un conflit avec un service MySQL local utilisant deja le port `3306`.

Le service MySQL utilise aussi un volume Docker persistant :

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

Ce volume conserve les fichiers de la base de donnees en dehors du cycle de vie temporaire du conteneur. La commande `docker compose down` arrete et supprime les conteneurs tout en gardant le volume. La commande `docker compose down -v` supprime aussi le volume et doit etre utilisee seulement pour reinitialiser la base.

---

## 11. Serveur HTTP Apache

Le service Apache expose le port 80 du conteneur sur le port 8080 de la machine hote :

```yaml
ports:
  - "8080:80"
```

La page web personnalisee se trouve dans :

```text
web/index.html
```

Elle est montee dans Apache avec :

```yaml
volumes:
  - ../web:/usr/local/apache2/htdocs
```

Ouvrir le service dans un navigateur :

```text
http://localhost:8080
```

---

## 12. Arreter l'infrastructure

Depuis le dossier `docker/` :

```bash
docker compose down
```

Pour supprimer les conteneurs et les volumes, uniquement si une reinitialisation complete est necessaire :

```bash
docker compose down -v
```

---

## 13. Workflow Git

Apres modification des fichiers, pousser les mises a jour avec :

```bash
git status
git add .
git commit -m "Update project files"
git push
```

Si le depot distant contient des changements absents localement :

```bash
git pull --rebase origin main
git push
```

---

## 14. Checklist de demonstration

Une demonstration complete doit montrer :

1. La structure du depot.
2. La construction et le demarrage avec Docker Compose.
3. Les conteneurs actifs avec `docker compose ps`.
4. L'execution du script Bash dans `debian_lab`.
5. L'execution du simulateur Python dans `debian_lab`.
6. La page Apache sur `http://localhost:8080`.
7. L'automatisation CRUD avec `./scripts/run_crud.sh`.
8. L'explication du volume persistant MySQL.

---

## 15. Equipe

- Ahmed Cheikh
- Varha Mohamed Mahmoud
