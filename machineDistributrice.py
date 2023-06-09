from os import name, system
from random import uniform, randint, shuffle
import time


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
def saisir_code_produit(machine_distributrice : dict) -> str :
    code_produit = input("Veuillez saisir le code de votre produit : ")
    if not code_produit.isalnum():
        code_produit = input("Veuillez saisir le code de votre produit : ")
    
    while verifier_disponibilite_produit == False :
        code_produit = input("Veuillez saisir le code de votre produit : ")
    if code_produit.isalnum():
        effacer_ecran
        print("Ce produit est disponible.")
    return code_produit
  
#Ryan
def afficher_details_produit(machine_distributrice : dict, code_produit : str) :
        effacer_ecran()
        b = ""
        c = ""
        d = ""
        b = obtenir_nom_produit(machine_distributrice, code_produit)
        c = obtenir_prix_produit(machine_distributrice, code_produit)
        d = obtenir_quantite_produit(machine_distributrice, code_produit)
        print(f"Nom du produit : {b}"), print(f"Prix unitaire : {c} $"), print(f"Quantite restante : {d}")
                

 
#Ryan
#!# Ou est l'Addition des pièces insérées ? +25c : total= 25c , +2$ : total = 2,25$ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def inserer_argent(touche_enfoncee : str, montant_fourni : float) -> float :
    b = obtenir_nom_produit(machine_distributrice, code_produit)
    time.sleep(1.5), print(f"Vous pouvez proceder au paiement du : \n{b}...")
    montant_fourni_ = []
    time.sleep(1.5)
    touche_enfoncee = input("Frapper sur une de ces lettres \n Z:2.00, X:1.00, C:0.25, V:0.10, B:0.05, svp : ")
    if touche_enfoncee == "Z":  
        touche_enfoncee = MONNAIES_ACCEPTABLES[0]
        print(f" Somme entree : {touche_enfoncee} $")
    if touche_enfoncee == "X":  
        touche_enfoncee = MONNAIES_ACCEPTABLES[1]
        montant_fourni_.append(touche_enfoncee)
        print(f" Somme entree : {touche_enfoncee} $")
    if touche_enfoncee == "C":  
        touche_enfoncee = MONNAIES_ACCEPTABLES[2]
        montant_fourni_.append(touche_enfoncee)
        print(f" Somme entree : {touche_enfoncee} $")
    if touche_enfoncee == "V":  
        touche_enfoncee = MONNAIES_ACCEPTABLES[3]
        montant_fourni_.append(touche_enfoncee)
        print(f" Somme entree : {touche_enfoncee} $")
    if touche_enfoncee == "B":  
        touche_enfoncee = MONNAIES_ACCEPTABLES[4]
        montant_fourni_.append(touche_enfoncee)
        print(f" Somme entree : {touche_enfoncee} $")
        montant_fourni = montant_fourni_
    return montant_fourni

def argent(Price: float):
    c = obtenir_prix_produit(machine_distributrice, code_produit)
    touche_enfoncee = input("Combien avez-vous mis (Z,X,C,V,B) : ")
    if touche_enfoncee == "Z" :
            Price = c - MONNAIES_ACCEPTABLES[0]
    if touche_enfoncee == "X" :
            Price = c - MONNAIES_ACCEPTABLES[1]
    if touche_enfoncee == "C" :
            Price = c - MONNAIES_ACCEPTABLES[2]
    if touche_enfoncee == "V" :
            Price = c - MONNAIES_ACCEPTABLES[3]
    if touche_enfoncee == "B" :
            Price = c - MONNAIES_ACCEPTABLES[4]
    print(f"\n Il vous reste a payer {Price} $")
    return Price


#Ryan
def payer_produit(machine_distributrice : dict, code_produit : str) :
    c = float(obtenir_prix_produit(machine_distributrice, code_produit))
    montant_fourni = inserer_argent(touche_enfoncee="", Price="", montant_fourni="")
    if not montant_fourni == c :
        effacer_ecran(), afficher_details_produit(machine_distributrice, code_produit), argent(Price="")
    


#Anthony
def distribuer_produit(machine_distributrice : dict, code_produit : str, montant_fourni : float) :
    afficher_details_produit(machine_distributrice, code_produit)
    
    if is_payed == True :
        time.sleep(5)
        print("Distribution du produit en cours...")
                                                                                    


#Anthony
def calculer_monnaie(argent_a_rendre : float, liste_monnaies_rendues : list) -> float :

    for i in MONNAIES_ACCEPTABLES:
        nombre_monnaie = 0
        while argent_a_rendre - i >= 0 and i <= argent_a_rendre:
            argent_a_rendre = argent_a_rendre - i
            
            nombre_monnaie = nombre_monnaie +1
        liste_monnaies_rendues.append(nombre_monnaie)
            
    return liste_monnaies_rendues       


#Anthony
def remettre_argent(machine_distributrice : dict, code_produit : str, montant_fourni : float) :
    #Affichage
    effacer_ecran()
    
    print(f"Montant inséré  :",montant_fourni,"$")
    print("Prix du produit : ", obtenir_prix_produit(machine_distributrice, code_produit), "$")
    
    #calcule de l'argent à rendre
    c = float(obtenir_prix_produit(machine_distributrice, code_produit))
    argent_a_rendre = round(float(montant_fourni) - c, 2)
    
    time.sleep(.5)
    
    print(f"Argent à rendre :",argent_a_rendre,"$")
    print("")
    
    #Appel de la fonction calculer_monnaie pour qu'elle calcule le change à distribuer et sauvegarde la liste de monnaies à rendre
    liste_monnaies_rendues = calculer_monnaie(argent_a_rendre, liste_monnaies_rendues=[])
    
    for i in range(len(liste_monnaies_rendues)):
        if liste_monnaies_rendues[i] > 0:
            if i == 0:
                print(liste_monnaies_rendues[i], " x 2.00$" )
            elif i == 1:
                print(liste_monnaies_rendues[i], " x 1.00$" )
            elif i == 2:
                print(liste_monnaies_rendues[i], " x 0,25$" )
            elif i == 3:
                print(liste_monnaies_rendues[i], " x 0,10$" )
            elif i == 4:
                print(liste_monnaies_rendues[i], " x 0,05$" )
    print("")
    input("Remise des pièces de monnaie en cours...")
        



##########################################################
# SECTION 4 : EXÉCUTION PRINCIPALE ("MAIN") DU PROGRAMME #
#             Vous ne devez en aucun cas modifier le     #
#             code ci-dessous !                          #
##########################################################

if __name__ == "__main__" :
    machine_distributrice = {}
    remplir_machine_distributrice(machine_distributrice)
    afficher_contenu_machine_distributrice(machine_distributrice)
    code_produit = saisir_code_produit(machine_distributrice)
    montant_fourni = payer_produit(machine_distributrice, code_produit)
    montant_fourni = input("DEBUG Insérer argent")
    distribuer_produit(machine_distributrice, code_produit, montant_fourni)
    remettre_argent(machine_distributrice, code_produit, montant_fourni)
    afficher_remerciements(machine_distributrice, code_produit)
