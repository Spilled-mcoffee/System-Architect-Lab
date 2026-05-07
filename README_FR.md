# System Architect Lab — Linux, Ordonnancement et Conteneurisation

## Présentation du projet

Ce projet a pour objectif de mettre en pratique plusieurs notions fondamentales des systèmes d’exploitation et de l’administration système. Il combine trois axes principaux :

1. **Automatisation Shell avec Bash**
2. **Simulation d’algorithmes d’ordonnancement CPU**
3. **Infrastructure conteneurisée avec Docker, MySQL et Apache**

Le projet permet de simuler le travail d’un administrateur système ou d’un ingénieur DevOps débutant, en automatisant des tâches Linux, en comparant des politiques d’ordonnancement et en déployant une architecture distribuée simple avec Docker Compose.

---

## Structure du projet

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
│   └── docker-compose.yml
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
└── README_FR.md
```

---

## 1. Automatisation Bash

### Objectif

Le script `admin_systeme.sh` automatise des tâches classiques d’administration système sous Linux.

Il permet notamment de :

- Vérifier que le script est exécuté avec les privilèges administrateur
- Créer un nouvel utilisateur
- Définir un mot de passe
- Créer un espace de travail dédié
- Appliquer des permissions sécurisées avec `chmod` et `chown`
- Simuler l’attribution d’un quota disque

### Exécution

Depuis le dossier du projet :

```bash
cd bash
chmod +x admin_systeme.sh
sudo ./admin_systeme.sh
```

### Remarque importante

Le script doit être exécuté avec `sudo`, car la création d’utilisateurs et la modification des permissions système nécessitent des privilèges administrateur.

---

## 2. Simulation d’ordonnancement CPU

### Objectif

Le fichier `scheduling.py` implémente et compare deux algorithmes d’ordonnancement :

- **Round Robin**
- **SRTF (Shortest Remaining Time First)**

Le programme génère des diagrammes de Gantt textuels et calcule les métriques suivantes :

- Temps d’attente
- Temps de séjour / turnaround time
- Temps d’attente moyen

### Exécution

```bash
cd scheduling
python3 scheduling.py
```

### Description rapide des algorithmes

#### Round Robin

Round Robin attribue à chaque processus une durée fixe appelée **quantum**. Si le processus n’est pas terminé après ce quantum, il est replacé à la fin de la file d’attente.

Cet algorithme favorise l’équité entre les processus.

#### SRTF

SRTF est un algorithme préemptif qui sélectionne à chaque instant le processus ayant le temps d’exécution restant le plus court.

Cet algorithme réduit généralement le temps d’attente moyen, mais il peut défavoriser les processus longs.

---

## 3. Infrastructure Docker

### Objectif

L’infrastructure Docker déploie plusieurs services isolés :

- Un conteneur Debian pour les tests Linux
- Un conteneur MySQL pour la base de données `etudiants`
- Un conteneur Apache pour le serveur HTTP
- Un volume Docker persistant pour les données MySQL

### Services déployés

| Service | Rôle |
|---|---|
| `debian_lab` | Environnement Linux pour les tests Bash |
| `mysql_server` | Serveur MySQL contenant la base de données |
| `apache_server` | Serveur HTTP Apache |
| `mysql_data` | Volume persistant pour les données MySQL |

---

## 4. Lancement de l’infrastructure Docker

Depuis le dossier contenant le fichier `docker-compose.yml` :

```bash
cd Docker
docker compose up -d
```

Vérifier l’état des conteneurs :

```bash
docker compose ps
```

Arrêter l’infrastructure :

```bash
docker compose down
```

Arrêter l’infrastructure et supprimer les volumes :

```bash
docker compose down -v
```

Attention : la commande `docker compose down -v` supprime aussi le volume MySQL et peut donc effacer les données persistantes.

---

## 5. Accès au serveur Apache

Le serveur Apache est exposé sur le port `8080` de la machine hôte.

Dans un navigateur, ouvrir :

```text
http://localhost:8080
```

La page personnalisée du projet est stockée dans :

```text
web/index.html
```

Elle est montée dans le conteneur Apache avec un bind mount vers :

```text
/usr/local/apache2/htdocs
```

---

## 6. MySQL et automatisation CRUD

### Base de données

Le service MySQL crée une base de données nommée :

```text
etudiants
```

### Fichier SQL

Le fichier suivant contient les opérations CRUD :

```text
sql/crud.sql
```

Il effectue les opérations suivantes :

- Création de la table `etudiants`
- Insertion de données
- Lecture des données
- Modification d’un enregistrement
- Suppression d’un enregistrement
- Affichage final de la table

### Script d’automatisation

Le script suivant exécute automatiquement les opérations CRUD dans le conteneur MySQL :

```text
scripts/run_crud.sh
```

### Exécution

Depuis la racine du projet :

```bash
chmod +x scripts/run_crud.sh
./scripts/run_crud.sh
```

Le script vérifie d’abord que le conteneur `mysql_server` est en cours d’exécution, puis exécute le fichier SQL dans MySQL.

---

## 7. Connexion manuelle à MySQL

### Depuis le conteneur

```bash
docker exec -it mysql_server mysql -u root -p
```

Mot de passe :

```text
root123
```

### Depuis la machine hôte

Si le port hôte utilisé est `3307`, la connexion se fait avec :

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p
```

Mot de passe :

```text
root123
```

---

## 8. Volume persistant MySQL

Le service MySQL utilise un volume Docker nommé `mysql_data` :

```yaml
volumes:
  - mysql_data:/var/lib/mysql
```

Ce volume permet de conserver les données de la base même si le conteneur MySQL est supprimé puis recréé.

Sans volume persistant, les données seraient fortement dépendantes du cycle de vie du conteneur. Avec le volume, les données sont séparées du conteneur et peuvent survivre aux redémarrages.

---

## 9. Commandes utiles

### Docker

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

### Accès aux conteneurs

```bash
docker exec -it debian_lab bash
docker exec -it mysql_server mysql -u root -p
docker exec -it apache_server bash
```

### Volumes

```bash
docker volume ls
docker volume inspect docker_mysql_data
```

---

## 10. Résultats attendus

À la fin de l’exécution, le projet doit démontrer :

- La création automatisée d’un utilisateur Linux
- La simulation et la comparaison de Round Robin et SRTF
- Le lancement d’une infrastructure Docker multi-conteneurs
- L’accès à une page Apache personnalisée
- L’exécution automatique des opérations CRUD sur MySQL
- La persistance des données MySQL grâce à un volume Docker

---

## Auteur

**Ahmed Cheikh**

Projet réalisé dans le cadre du mini-projet :

**System Architect Lab — Linux, Ordonnancement et Conteneurisation**
