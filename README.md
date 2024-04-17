# TP-MongoDB-ReplicaSet

___

## 0. Prérequis

___

- Avoir [Docker](https://docs.docker.com/get-docker/) installé sur votre machine
- Cloner le projet

```bash
git clone https://github.com/Bahsiik/TP-MongoDB-ReplicaSet.git
```

## 1. Configuration de MongoDB en mode ReplicaSet

___

Pour configurer les instances de MongoDB en mode ReplicaSet, nous allons utiliser le fichier `docker-compose.yml` qui
contient la configuration de 3 instances de MongoDB. <br> Il suffit de lancer la commande suivante pour démarrer les instances de MongoDB.

```bash
docker-compose up -d
```

Ce qui va créer 3 conteneurs Docker avec les noms suivants:

- mongo1
- mongo2
- mongo3

Pour vérifier que les instances MongoDB sont bien démarrées, on peut s'y connecter en utilisant la commande suivante:

```bash
docker exec -it mongo1 bash
```

_Pour les instances mongo2 et mongo3, il suffit de remplacer `mongo1` par `mongo2` ou `mongo3` dans la commande
ci-dessus._

Puis, on rentre dans l'instance MongoDB en utilisant la commande suivante:

```bash
mongosh
```

Ensuite, on peut vérifier que les instances sont bien configurées en mode ReplicaSet en exécutant les commandes
suivantes:

```bash
rs.status()
```

## 2. Génération de Fausses Données

___

Pour générer des fausses données, on peut utiliser le script `data_generation.py` qui se trouve dans le
dossier `scripts`. <br> Mais avant cela, il faut transférer le script vers le conteneur `mongo1` en utilisant la commande suivante (dans notre
terminal local, pas dans le conteneur) :

```bash
docker cp .\scripts mongo1:usr/src
```

_On copie le dossier entier, car il contient également un autre script qui nous sera utile plus tard._

On se connecte alors au conteneur `mongo1`, et il va nous falloir installer `python3` et `pip` pour pouvoir exécuter le
script.

```bash
apt-get update
apt-get install python3
apt-get install python3-pip
```

Ensuite, on installe les dépendances nécessaires pour les scripts.

```bash
pip3 install pymongo
pip3 install faker
```

On se déplace ensuite vers le dossier `usr/src/scripts` pour exécuter le script.

```bash
cd usr/src/scripts
python3 data_generation.py
```

Ceci va nous générer une liste de 100 utilisateurs avec leurs informations respectives.

## 3. Manipulations via la CLI MongoDB

___

Il va falloir commencer par insérer les données générées précédemment dans la base de données.
<br>Pour cela, on va effectuer la commande suivante :

```bash
mongoimport --db db_cli --collection users --file users.json --jsonArray
```

_Cela va insérer les données dans la collection `users` de la base de données `db_cli`. <br>Si la base de données ou la
collection n'existent pas, elles seront créées automatiquement. <br>Le chemin du
fichier `users.json` peut varier selon d'où vous exécutez la commande._

Maintenant que notre base de données est peuplée, on peut effectuer des requêtes pour récupérer des informations.
On retourne dans le `mongosh` pour effectuer les requêtes.

Avant toute commande, il faut selectionner la base de données `db_cli` en utilisant la commande suivante:

```bash
use db_cli
```

### Insertion - Nouvel utilisateur

___

```bash
db.users.insertOne({
    "name": "John Doe",
    "email": "johndoe@example.com",
    "age": 25,
    "createdAt": "2024-01-12T10:29:54"
})
```

### Lecture - Tous les utilisateurs ayant plus de 30 ans

___

```bash
db.users.find({ "age": { $gt: 30 } })
```

### Mise à jour - Augmenter l'âge de tous les utilisateurs de 5 ans

___

```bash
db.users.updateMany({}, { $inc: { "age": 5 } })
```

### Suppression - Supprimer un utilisateur spécifique

___

```bash
db.users.deleteOne({ "name": "John Doe" })
```

## 4. Automatisation avec Python

___

Pour automatiser les manipulations précédentes, on peut utiliser le script `crud_automatisation.py` qui se trouve dans
le dossier `scripts`. <br> Nous l'avons déjà copié dans le conteneur `mongo1` lors de la génération des données, il suffit donc de se déplacer vers
le dossier `usr/src/scripts` et d'exécuter le script.

```bash
cd usr/src/scripts
python3 crud_automatisation.py
```

Après l'exécution du script, on peut vérifier que les manipulations ont bien été effectuées, car dans un premier temps,
nous avons un print des utilisateurs trouvés, puis il nous suffit de vérifier dans le `mongosh` que les manipulations
ont bien été effectuées. <br> On y retrouvera effectivement une nouvelle base, ainsi qu'une nouvelle collection `users`, qui
contiendra les mêmes users que la précédente base, parce que nous avons récupéré les données du fichier `users.json`. <br> Il
suffit ensuite d'aller regarder le contenu du script pour voir les manipulations effectuées.

## 5. Différences entre les manipulations via la CLI et via Python

___

Les manipulations effectuées via la CLI et via Python sont les mêmes, mais la différence réside dans le fait que via
Python, on peut automatiser les manipulations, et donc les répéter autant de fois que nécessaire, sans avoir à retaper
les
commandes à chaque fois. <br> Cela permet de gagner du temps et d'augmenter la répétabilité des manipulations. On pourrais
également envisager
d'ajouter une gestion d'erreur pour les manipulations via Python, ce qui n'est pas possible via la CLI.
<br>Cependant, la CLI est plus rapide pour effectuer des manipulations ponctuelles, et est plus adaptée pour des
manipulations
simples. <br> Pour des manipulations plus complexes, il est préférable d'utiliser Python, mais il faudra savoir
à l'avance ce que l'on veut faire, car il faudra écrire le script en conséquence.

## 6. Difficultés rencontrées

___

La principale difficulté rencontrée a été le paramétrage du Docker-Compose pour configurer les instances MongoDB en mode
ReplicaSet. En effet, il a fallu beaucoup de recherches sur des forums et des documentations pour comprendre comment le
faire. <br> Une autre des difficultés rencontrées a été l'utilisation des scripts pythons pour manipuler les données dans la
base de données. J'étais d'abord parti sur une autre piste, en voulant utiliser un Dockerfile pour exécuter les scripts
et installé python et pip, mais je n'ai jamais réussi à le faire démarrer au lancement du docker compose. Au final, j'ai
finalement trouvé une solution plus simple en copiant les scripts dans le conteneur
et en les exécutant directement.