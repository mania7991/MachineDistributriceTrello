from os import name, system
from random import uniform, randint, shuffle


#######################################################
# SECTION 1 : DÉCLARATION DES CONSTANTES DU PROGRAMME #
#             Vous ne devez en aucun cas modifier les #
#             constantes ci-dessous !                 #
#######################################################

MONNAIES_ACCEPTABLES = [2.00, 1.00, 0.25, 0.10, 0.05]
NOMS_PRODUITS = ["Barre au moka et amandes", "Mélange du randonneur", "Croque-nature au miel et canneberges",
                "Barre citrouille-épices", "Barre aux fraises et amandes ", "Barre au chocolat noir et oranges",
                "Bouchées aux baies mélangées", "Bouchées aux noix de pécan", "Bouchées à la noix de coco",
                "Pepsi", "Seven Up", "Mountain Dew", "Coca-Cola", "Fanta aux raisins", "Fanta à l'orange",
                "Sprite", "Fruitopia aux fraises", "Sunny Delight", "Jus de pomme", "Galette au chocolat noir",
                "Galette aux morceaux de chocolat", "Galette aux raisons secs et avoine", "Jus d'orange",
                "Barre tendre aux arachides", "Galette aux noix de macadame", "Croustilles au sel et vinaigre",
                "Croustilles au cheddar", "Croustilles au bacon à l'érable", "Croustilles au ketchup",
                "Croustilles aux piments jalapenos", "Croustilles natures", "Croustilles à saveur BBQ",
                "Croustilles aux cornichons à l'aneth", "Jujubes aux pêches", "Jujubes à la framboise bleue",
                "Jujubes aux cerises", "Jujubes aux melons d'eau", "Croustilles de riz", "Bretzels sucrés salés",
                "Barre aux pistaches et pommes"]
NB_LIGNES = 10
NB_COLONNES = len(NOMS_PRODUITS) // NB_LIGNES
PRIX_MIN = 0.10
PRIX_MAX = 5.00
QUANTITE_MIN = 1
QUANTITE_MAX = 12


#################################################################
# SECTION 2 : DÉFINITION DES FONCTIONS DÉJÀ CODÉES ET COMPLÈTES #
#             Vous ne devez en aucun cas modifier les fonctions #
#             ci-dessous !                                      #
#################################################################

def melanger_noms() :
    shuffle(NOMS_PRODUITS)


def choisir_nom(liste_elements_uniques : list, liste_complete : list) -> str:
    for element in liste_complete :
        if element not in liste_elements_uniques :
            liste_elements_uniques.append(element)
            return element


def choisir_produit(machine_distributrice : dict) -> str :
    effacer_ecran()
    afficher_contenu_machine_distributrice(machine_distributrice)

    return saisir_code_produit(machine_distributrice)


def effacer_ecran() :
    system('cls' if name == 'nt' else 'clear')


def saisir_touche() -> str :
    caractere = ""
    
    if name == "nt" : # Pour Windows
        import msvcrt
        caractere = msvcrt.getch()
    
    else : # Pour Mac Os ou Linux
        import tty, termios, sys
        console = sys.stdin.fileno()
        ancienne_configuration = termios.tcgetattr(console)

        try:
            tty.setraw(sys.stdin.fileno())
            caractere = sys.stdin.read(1)
        
        finally:
            termios.tcsetattr(console, termios.TCSADRAIN, ancienne_configuration)
        
    if ord(caractere) in [3, 4, 26, 27] : # Pour Ctrl+C, Ctrl+D, Ctrl+Z, Esc,
        quit()

    return (caractere.decode("utf-8")).upper()


def remplir_machine_distributrice(machine_distributrice : dict) :
    liste_noms_uniques = []
    melanger_noms()

    for i in range(NB_LIGNES):
        liste_produits = []

        for j in range(NB_COLONNES):
            liste_produits.append({
                "nom"      : choisir_nom(liste_noms_uniques, NOMS_PRODUITS),
                "prix"     : round(uniform(PRIX_MIN, PRIX_MAX), 1),
                "quantite" : randint(QUANTITE_MIN, QUANTITE_MAX)
            })

        machine_distributrice[chr(ord('A') + i)] = liste_produits


def trouver_largeurs_colonnes(liste_largeurs_colonnes : list, machine_distributrice : dict) :
    for colonne in range(NB_COLONNES) :
        largeur_colonne_max = 0
        
        for ligne in machine_distributrice :
            largeur_colonne_courante = len(machine_distributrice[ligne][colonne]["nom"])

            if largeur_colonne_courante > largeur_colonne_max :
                largeur_colonne_max = largeur_colonne_courante

        liste_largeurs_colonnes.append(largeur_colonne_max)


def afficher_contenu_machine_distributrice(machine_distributrice : dict) :
    liste_largeurs_colonnes = []
    trouver_largeurs_colonnes(liste_largeurs_colonnes, machine_distributrice)
    separateur_lignes = "-" * (sum(liste_largeurs_colonnes) + 3 * NB_COLONNES + 4)

    print("\n" + separateur_lignes)

    for i in range(NB_COLONNES) :
        if i == 0 :
            print(" # | ", end = "")

        print("{:{remplissage}{alignement}{longueur}}".format(
            str(i + 1),
            remplissage = "",
            alignement = "^",
            longueur = liste_largeurs_colonnes[i]
        ), end = " | ")

    print("\n" + separateur_lignes)

    for ligne in machine_distributrice :
        print(" " + ligne, end = " | ")

        for colonne in range(NB_COLONNES) :
            print("{:{remplissage}{alignement}{longueur}}".format(
                machine_distributrice[ligne][colonne]["nom"],
                remplissage = "",
                alignement = "^",
                longueur = liste_largeurs_colonnes[colonne]
            ), end = " | ")

        print()
    
    print(separateur_lignes)


def afficher_remerciements(machine_distributrice : dict, code_produit : str) :
    effacer_ecran()
    print("\nMerci d'avoir utilisé notre machine distributrice!",
          "Nous espérons que vous aimerez le produit acheté :\n",
          (obtenir_nom_produit(machine_distributrice, code_produit) + "\n"),
		  sep = "\n")
    input("(Appuyez sur [ENTER] pour continuer) ")


def obtenir_nom_produit(machine_distributrice : dict, code_produit : str) -> str :
    return machine_distributrice[code_produit[0]][int(code_produit[1:]) - 1]['nom']


def obtenir_prix_produit(machine_distributrice : dict, code_produit : str) -> float :
    return machine_distributrice[code_produit[0]][int(code_produit[1:]) - 1]['prix']


def obtenir_quantite_produit(machine_distributrice : dict, code_produit : str) -> int :
    return machine_distributrice[code_produit[0]][int(code_produit[1:]) - 1]['quantite']


def verifier_disponibilite_produit(machine_distributrice : dict, code_produit : str) -> bool :
    return (obtenir_quantite_produit(machine_distributrice, code_produit) > 0)







#############################################################
# SECTION 3 : DÉFINITION DES FONCTIONS QUE VOUS DEVEZ CODER #
#             Vous devez, par vous-mêmes, compléter le code #
#             des fonctions ci-dessous.                     #
#############################################################

is_payed = False

#Anthony
def modifier_quantite_produit(machine_distributrice : dict, code_produit : str, quantite : int) :
    if (quantite > 0) :
        machine_distributrice[code_produit[0]][int(code_produit[1:]) - 1]['quantite'] = quantite - 1
    

#Ryan
def afficher_details_produit(machine_distributrice : dict, code_produit : str) :
    pass

#Ryan
def saisir_code_produit(machine_distributrice : dict) -> str :
    pass

#Anthony
def distribuer_produit(machine_distributrice : dict, code_produit : str, montant_fourni : float) :
    afficher_details_produit(machine_distributrice, code_produit)
   
    if is_payed == True :
        ENTER_Input = input("Distribution du produit en cours...")
        while not ENTER_Input == "":
            input() 

#Ryan
def payer_produit(machine_distributrice : dict, code_produit : str) :
    pass

#Ryan
def inserer_argent(touche_enfoncee : str, montant_fourni : float) -> float :
    pass

#Anthony
def calculer_monnaie(argent_a_rendre : float, liste_monnaies_rendues : list) -> float :
    pass

#Anthony
def remettre_argent(code_produit : str, montant_fourni : float) :
    pass


















##########################################################
# SECTION 4 : EXÉCUTION PRINCIPALE ("MAIN") DU PROGRAMME #
#             Vous ne devez en aucun cas modifier le     #
#             code ci-dessous !                          #
##########################################################

if __name__ == "__main__" :
    machine_distributrice = {}
    remplir_machine_distributrice(machine_distributrice)
    
    # Dans la console, appuyez sur les touches [CTRL] et [C]
    # pour arrêter cette boucle infinie et, donc, l'exécution
    # du programme. 
    while True :
        is_payed = True
        afficher_contenu_machine_distributrice(machine_distributrice)
        distribuer_produit(machine_distributrice, "B3", 4)
        input()
        # remettre_argent(code_produit, montant_fourni)
        # afficher_remerciements(machine_distributrice, code_produit)
        
        
        
        
        
        
        
        
        
        
        ########################Original############################
        # code_produit = choisir_produit(machine_distributrice)
        # montant_fourni = payer_produit(machine_distributrice, code_produit)
        # distribuer_produit(machine_distributrice, code_produit, montant_fourni)
        # remettre_argent(code_produit, montant_fourni)
        # afficher_remerciements(machine_distributrice, code_produit)
        ############################################################