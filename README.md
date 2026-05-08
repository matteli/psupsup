PSUPSUP
=======
Psupsup est un module python de traitement des données des candidats à l'admission post-bac en France, permettant de générer des fichiers Excel, CSV et PDF à partir des résultats traités des candidats.

Le code est disponible sur GitHub (https://github.com/matteli/Psupsup) avec un fichier exemple de programme.

Installation
------------
- Installer python (>=3.9)
- Créer un répertoire de travail pour créer votre programme, copier les différents fichiers de travail parcoursup et récupérer les fichiers créés par votre programme. Entrer dans ce dossier.
- Créer un environnement virtuel : `python3 -m venv .venv` 
- Activer l'environnement virtuel. 
    - pour Unix/macOS : `source .venv/bin/activate`
    - pour Windows : `.venv\Scripts\activate`
- Installer Psupsup : `python3 -m pip install psupsup`

Utilisation
-----------
### Données parcoursup

Les données des candidats sur parcoursup doivent être exporter au format JSON.

Pour celà, créer un modèle (Export de données -> Export JSON -> Cliquer sur l'engrenage correspondant -> Créer un modèle).

Donner un libellé à votre modèle pour le retrouver plus tard (les modèles restent d'une année sur l'autre).

Choisir les paramètres sélectionnables suivants: 

- Données candidats :
    - Numéro dossier
    - Nom Candidat (pour les apprentis)
    - Prénom Candidat (pour les apprentis)
    - Sexe
    - Coordonnées - Adresse mail (pour les apprentis)
- Scolarité, pour toutes les années scolaires :
    - Année Scolaire - Code
    - Niveau Etude - Libellé
- Bulletins Scolaires :
    - Bulletins - Année Scolaire - Code
    - Bulletins - Périodicité - Libellé
    - Type de classe - Libellé
    - Périodicité du bulletin -Libellé
    - Matière - Code
    - Moyenne du Candidat
    - Moyenne classe Candidat
    - Moyenne Basse Classe du Candidat
    - Moyenne Haute Classe du Candidat
    - Pour chaque série ciblée, cocher les matières ciblées*
- Baccalauréat :
    - Série Diplôme - Code
    - Spécialité - Libellé
- Notes Baccalauréat :
    - Epreuve - Code
    - Note de l'épreuve
    - Pour chaque série ciblée, cocher les matières ciblées
- Données Vœux :
    - Vœux - Groupe - Libellé
    - Vœu confirmé - Code

Valider.

Une fois le modèle créée, générer le fichier de données en cliquant sur l'icone avec la flèche vers le bas.

Générer un nouveau fichier. 

Attendre et récupérer le fichier en cliquant dessus. Le copier dans le répertoire de travail (Ne pas le dézipper, la librairie s'en charge).

### Programme de traitement

Utiliser votre éditeur de code favori.

Créer votre programme en utilisant les fonctions de la librairie à partir du programme "exemple.py".

Lancer le programme `python3 [nom_programme].py`


