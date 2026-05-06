from psupsup.psupsup import *

# Exemple d'utilisation du module psupsup pour traiter les données des candidats et générer des résultats.

# Définir les matières et les notes de bac à prendre en compte.
# Les tuples contiennent les identifiants des matières dans les bulletins et les notes de bac.
# Dans cet exemple, la moyenne de maths sera composée de toutes les matières de maths présentes dans les bulletins (1 : maths en STI2D, 700 : Mathématiques Spécialité, 1070 : Mathématiques Complémentaires).
# Si une ou plusieurs de ces matières sont présentes dans les bulletins, elles seront utilisées pour calculer la moyenne de maths. Si aucune de ces matières n'est présente, la moyenne de maths sera considérée comme nulle.
matieres = {
    "maths": (1, 700, 1070),
    "phys/ing": (1056, 1055, 1096, 701, 1040, 2, 4, 1061),
    "LV1": (7,),
    "français": (50,),
}
notes_bac = {"bac_français": (919, 920)}

# Si redoublement_neutralise est True, alors seul les dernières Première et Terminale seront prises en compte pour le calcul des moyennes de matières. Si False, alors toutes les années seront prises en compte.
redoublement_neutralise = True

# Charger les données des candidats à partir d'un fichier JSON ZIP.
candidats = charger_donnees()

# Dictionnaire pour stocker les résultats des candidats. La clé est le numéro de dossier du candidat et la valeur est un dictionnaire contenant les informations et les résultats du candidat.
resultats_candidats = {}

# Parcourir la liste des candidats et traiter les données pour chaque candidat.
for candidat in candidats:
    if candidature_confirmee(candidat):
        num = numero_dossier_candidat(candidat)
        bac = type_bac(candidat)
        id = identite_candidat(candidat)
        groupe = groupe_candidat(candidat)

        # Initialisation si le candidat n'a pas déjà été ajouté au dictionnaire
        if resultats_candidats.get(num) is None:
            resultats_candidats[num] = {
                "AEF": (
                    0 if sexe_candidat(candidat) == "Masculin" else 20
                ),  # Bonus pour les candidates
                "Notes": 0,
                "Bac": bac["série"],
                "Nom": id["nom"],
                "Prénom": id["prénom"],
                "Email": id["email"],
                "Groupe": groupe,
            }
            # Initialiser les moyennes et le nombre de notes pour chaque matière et chaque note de bac à 0
            for m in matieres | notes_bac:
                resultats_candidats[num][m] = {"nbre": 0, "moyenne": 0}

        if (
            bac["série"] == "STI2D" and bac["série"] == "P"
        ):  # Filtrage des candidats suivants le bac

            # Création d'itérateur pour parcourir les matières présentes dans les bulletins du candidat en fonction des matières définies dans le dictionnaire 'matieres' et de la variable 'redoublement_neutralise'.
            matieres_bulletins = iterer_matieres_dans_bulletins(
                candidat, matieres, redoublement_neutralise
            )
            # Utilisation de l'itérateur pour parcourir les matières présentes dans les bulletins du candidat et calculer la note modifiée pour chaque matière.
            for mb in matieres_bulletins:
                # Calcul de la note modifiée pour la matière en utilisant la fonction 'note_modifiee' qui prend en compte la note brute et la note normalisée en fonction de la moyenne de la classe, de la moyenne basse et de la moyenne haute.
                note = note_modifiee(
                    moyennes_bulletins_matiere(mb["bulletin"])["moyenne_candidat"],
                    moyennes_bulletins_matiere(mb["bulletin"])["moyenne_classe"],
                    moyennes_bulletins_matiere(mb["bulletin"])["moyenne_basse"],
                    moyennes_bulletins_matiere(mb["bulletin"])["moyenne_haute"],
                )
                # Calcul de la moyenne de la matière
                if note >= 0:
                    resultats_candidats[num][mb["matiere"]]["nbre"] += 1
                    resultats_candidats[num][mb["matiere"]]["moyenne"] = (
                        resultats_candidats[num][mb["matiere"]]["moyenne"]
                        * (resultats_candidats[num][mb["matiere"]]["nbre"] - 1)
                        + note
                    ) / resultats_candidats[num][mb["matiere"]]["nbre"]

            # Création d'itérateur pour parcourir les matières présentes dans le bac du candidat en fonction des notes de bac définies dans le dictionnaire 'notes_bac'.
            matieres_bac = iterer_matieres_dans_bac(candidat, notes_bac)
            # Utilisation de l'itérateur pour parcourir les matières présentes dans le bac du candidat et calculer la note modifiée pour chaque matière.
            for mb in matieres_bac:
                note = note_bac_modifiee(mb["note"])
                resultats_candidats[num][mb["matiere"]]["nbre"] += 1
                resultats_candidats[num][mb["matiere"]]["moyenne"] = (
                    resultats_candidats[num][mb["matiere"]]["moyenne"]
                    * (resultats_candidats[num][mb["matiere"]]["nbre"] - 1)
                    + note
                ) / resultats_candidats[num][mb["matiere"]]["nbre"]

        # Calcul de la note globale du candidat.
        resultats_candidats[num]["Notes"] = (
            resultats_candidats[num]["phys/ing"]["moyenne"]
            + resultats_candidats[num]["maths"]["moyenne"]
            + resultats_candidats[num]["LV1"]["moyenne"]
            + resultats_candidats[num]["bac_français"]["moyenne"]
            + resultats_candidats[num]["AEF"] / 2
        ) / 4.5

# Classement des candidats en fonction de la note globale.
resultats_candidats = classer_candidats_par_critère(resultats_candidats, "Notes")

# Génération de fichiers PDF pour les résultats des candidats.
generer_pdf(
    resultats_candidats,
    titre="Bac pro",
    headers=[
        "Num",
        "Notes",
        "Ori/Ortho /5",
        "Référenti /5",
        "BIA, PPL /5",
        "Choix LAB /5",
        "SE (0, 10, 20)",
    ],
    col_width=[20, 20, 30, 30, 30, 30, 30],
    nom_fichier="resultats_candidats_bac_pro.pdf",
    criteres=[{"critere": "Bac", "inclus": ["P"]}],
)

generer_pdf(
    resultats_candidats,
    titre="Autres bacs",
    headers=[
        "Num",
        "Notes",
        "Ori/Ortho /5",
        "Référenti /5",
        "BIA, PPL /5",
        "Choix LAB /5",
        "SE (0, 10, 20)",
    ],
    col_width=[20, 20, 30, 30, 30, 30, 30],
    nom_fichier="resultats_candidats_autres_bacs.pdf",
    criteres=[{"critere": "Bac", "exclus": ["P"]}],
)

# Génération d'un fichier CSV importable sur parcoursup pour les résultats des candidats. Pour cette fonction, un fichier CSV exporté de parcoursup et placé dans le répertoire de travail est nécessaire.
generer_csv(resultats_candidats, colonnes=["Notes"])
