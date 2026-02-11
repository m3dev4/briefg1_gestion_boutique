import mysql.connector
connection=mysql.connector.connect(
    host='localhost',
    user='admin',
    password='admin123',
    database='gestion_stock'
)
if connection.is_connected():
    print("Connexion établie avec succes!")
curseur=connection.cursor()

def ajouter_categories():
   while True:
     
     
     categorie=input("saisir le nom  du produit a mettre a jour: ").strip().capitalize()
     if categorie.replace(" ", "").isalpha():
       break  
     else:
         print("type non validé ")
     
     sql="""INSERT INTO Categories(categorie_nom) values(%s)
        """
     valeurs=(categorie,)
     curseur.execute(sql,valeurs)
     connection.commit()
     break
#ajouter_categories()   
def ajouter_produit():
 while True:
    print("voici les categories disponibles")
    sql="""SELECT * FROM Categories"""
    curseur.execute(sql)
    affichage=curseur.fetchall()
    for c in affichage:
        print(c)
    
    
    
   
    id_categorie=input("saisir l'id de la categorie")
    if id_categorie.isnumeric():
       id_categorie=id_categorie
       
 
    else:
        print("saisir des elements de ype numerique pour les id")
      
    sql_verif="""SELECT * FROM produits where id_produit=%s"""
    curseur.execute(sql_verif,(id_categorie,))
    p=curseur.fetchone()
    if not p:
        print("id du categorie non trouve")
        break
        
    nom_produit=input("saisir le nom du produit: ").capitalize()
    if nom_produit.isalpha():
       nom_produit=nom_produit
      
    else:
        print("le nom doit etre composé que des lettres alphabétiques")
    
    prix=input("saisir le prix du produit: ")
    if prix.isnumeric():
        prix=prix
        
    else:
        print("le prix doit etre un nombre entier")
    qtite_initiale=input("saisir la quantitee: ")
    if qtite_initiale.isnumeric():
        qtite_initiale=qtite_initiale
       
    else:
        print("saisir que des nobres pour les quantites")
    sql_produit="""INSERT INTO produits(id_categorie,nom_produit,prix,quantité_initiale) values(%s,%s,%s,%s)"""
    valeurs=(id_categorie,nom_produit,prix,qtite_initiale)
    curseur.execute(sql_produit,valeurs)
    connection.commit()
    break
#ajouter_produit()   

def affichage_produits():
    sql="""SELECT produits.nom_produit,produits.prix,produits.quantité_initiale,Categories.categorie_nom 
    FROM produits 
    join Categories on Categories.id_categorie=produits.id_categorie
    WHERE produits.quantité_initiale>0""" 
    curseur.execute(sql)  
    affichage=curseur.fetchall()
    for nom_produit,prix,quantité_initiale,categorie_nom in affichage:
        print(f"nom_produit: {nom_produit:<5}  prix: {prix:<15}  quantité_initiale: {quantité_initiale:<5}  categorie_nom : {categorie_nom :<5}")
        break
affichage_produits()
def mise_a_jour():
    
 while True:
    nom_produit=input("saisir le nom  du produit a mettre a jour: ").strip().capitalize()
    if nom_produit.replace(" ", "").isalpha():
       break  

       
    else:
        print("le nom d un produit doit etre compose que des lettres alphabetiques")
    nouvelle_qtité=input("saisir la nouvelle quantité: ").strip()
    if nouvelle_qtité.isnumeric():
       nouvelle_qtité=int(nouvelle_qtité)
       break
    else:
        print("quantite doit etre de type entier")
    sql = """
    UPDATE produits p
    JOIN Categories c ON p.id_categorie = c.id_categorie
    SET p.quantité_initiale = %s
    WHERE p.nom_produit  = %s
   
    """

    valeurs = (nouvelle_qtité,nom_produit)
    curseur.execute(sql,valeurs)
    connection.commit()
    curseur.close()
    print("Mise à jour effectuée.")
    break
#mise_a_jour()
def Rechercher_produit():
 while True:
    id_produit=input("choisir l'id du produit à rechercher: ").capitalize()
    
    sql="""SELECT produits.prix,produits.quantité_initiale,produits.nom_produit,Categories.categorie_nom 
    
    FROM produits 
    join Categories on Categories.id_categorie=produits.id_categorie
    where   produits.id_produit=%s"""
    curseur.execute(sql,(id_produit,))
    affichage=curseur.fetchall()
    for prix,quantité_initiale,nom_produit,categorie_nom in affichage:
        print(f"prix: {prix:<15} quantité_initiale: {quantité_initiale:<5} nom_produit: {nom_produit:<5} categorie_nom : {categorie_nom :<5}")
        break
#Rechercher_produit()   


def Supprimer_produit(): #faire un select pour savoir si l id existe ou non,utiliser try except
 while True:
    identifiant=input("saisir l'id du produit a supprimer: ")
    if identifiant.isnumeric():
       identifiant=identifiant
       
    else:
        print("type non valide")
    sql_verif="""SELECT * FROM produits where id_produit=%s"""
    curseur.execute(sql_verif,(identifiant,))
    p=curseur.fetchone()
    if not p:
        print("id du produit non trouve")
        return
    
    sql=""" delete from produits where id_produit=%s """
    curseur.execute(sql,(identifiant,))
    connection.commit()
    
    print(f"produit supprimer avec sucess ")
    break 
#Supprimer_produit()    
def Supprimer_categorie():
  while True:
    identifiant=input("saisir l'id du categorie a supprimer: ")
    if identifiant.isnumeric():
       identifiant=int(identifiant)
       
    else:
        print("type non valide")
    sql_verif="""SELECT * FROM Categories where id_categorie=%s"""
    curseur.execute(sql_verif,(identifiant,))
    p=curseur.fetchone()
    if not p:
        print("id du produit non trouve")
        return
    sql=""" delete from Categories where id_categorie=%s"""
    curseur.execute(sql,(identifiant,))
    connection.commit()
    
    affichage=curseur.fetchone()
    if affichage:
        print(f"categorie supprimer avec sucess : {affichage}")
        break
#Supprimer_produit()    


def Dashboard():
    while True:
        print("#### Visualisation ####")
        print("1. Quel est le produit le plus cher ?")
        print("2. Valeur totale financière du stock")
        print("3. Nombre de produits par catégorie")
        print("4. Quitter")

        choix = input("Saisir votre choix : ")

        if choix == '1':
            sql = """
            SELECT c.categorie_nom,p.nom_produit,p.prix
            FROM produits p
            JOIN Categories c ON p.id_categorie = c.id_categorie
            ORDER BY p.prix DESC
            LIMIT 1
            """
            curseur.execute(sql)
            resultat = curseur.fetchone()
            print("voici le produit le produit le plus cher",resultat)

        elif choix == '2':
            sql = """
            SELECT SUM(prix * quantité_initiale)
            FROM produits
            """
            curseur.execute(sql)
            resultat = curseur.fetchone()
            print("Valeur totale du stock :", resultat)

        elif choix == '3':
            sql = """
            SELECT c.categorie_nom, COUNT(*)
            FROM produits p
            JOIN Categories c ON p.id_categorie = c.id_categorie
            GROUP BY c.categorie_nom
            """
            curseur.execute(sql)
            resultat = curseur.fetchall()
            for ligne in resultat:
                print(ligne)

        elif choix == '4':
            break

        else:
            print("Choix invalide")

#Dashboard()  


#Ajout utilisateur
def creer_utilisateur():
    mail = input("Nom d'utilisateur : ")
    mot_passe = input("Mot de passe : ")
    role_utilisateur = input("Rôle (admin/employe) : ")

    sql = """
    INSERT INTO utilisateurs(mail, mot_passe, role_utilisateur)
    VALUES (%s, %s, %s)
    """

    curseur.execute(sql, (mail, mot_passe, role_utilisateur))
    connection.commit()

    print("Utilisateur enregistré")



#auth
def authentification():
    mail= input("Nom d'utilisateur : ")
    mot_passe= input("Mot de passe : ")

    sql = """
    SELECT role_utilisateur
    FROM utilisateurs
    WHERE mail=%s AND mot_passe=%s
    """

    curseur.execute(sql, (mail, mot_passe))
    resultat = curseur.fetchone()

    if resultat:
         print("Connexion réussie")
         return resultat
    else:

        print("Identifiants incorrects")
        return None




  

def menu():
 while True:
    print("######  Menu principal  #####")
    print( "1.Ajouter un produit")
    print("2.Lister l'inventaire")
    print( "3.Mettre à jour le stock")
    print( "4.Rechercher un produit")
    print( "5.Supprimer un produit")
    print( "6.Supprimer une categorie")
    print ("7.Dashboard")
    print("8.ajouter une categorie")
    print("9.ajouter un utilisateur")
    print("10.Quitter le programme")
    choice=input("faire votre choix")
    if choice=='1':
     
     ajouter_produit()
    elif choice=='2':
     affichage_produits()
    elif choice=='4':
     Rechercher_produit()
    elif choice=='5':
     Supprimer_produit()
    elif choice=='6':
        Supprimer_categorie()
    elif choice=='7':
     Dashboard()
    elif choice=='8':
        ajouter_categories()
    elif choice=='9':
        creer_utilisateur()
    elif choice == '10':
        print("Merci! à bientot")
    
    
def menu_caissier():
    while True:
        print("\n=== MENU CAISSIER ===")
        print("1. Consulter la liste des produits")
        print("2. Quitter")

        choix = input("Choisir une option : ")

        if choix == "1":
            affichage_produits()  
        elif choix == "2":
            break
        else:
            print("Option invalide.")

#menu()   

      
    
#menu principal

def menu_principal():
    while True:
        print("Bienvenue!")    
        print("Proccédure d'authenfication") 
        role_tuple = authentification()  # ('admin',)
        if role_tuple:
         role = role_tuple[0] 
         print("C'est un admin")
         menu()
        elif role == "caissier":
         print("C'est un caissier")
         menu_caissier()
        else:
         print("Connexion échouée ou rôle inconnu")
#menu_principal()
curseur.close()
connection.close()         
    