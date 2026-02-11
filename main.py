import mysql.connector
import bcrypt

connection = mysql.connector.connect(
    host="localhost", user="root", password="", database="gestion_stock"
)
curseur = connection.cursor()


def ajouter_categories():
    categorie = input("Saisir une categories : ")
    sql = """INSERT INTO Categories(categorie_nom) values(%s)"""
    valeurs = (categorie,)
    curseur.execute(sql, valeurs)
    connection.commit()


def ajouter_produit():
    print("voici les categories disponibles")
    sql = """SELECT * FROM Categories"""
    curseur.execute(sql)
    affichage = curseur.fetchall()
    for c in affichage:
        print(c)

    id_categorie = input("saisir l'id de la categorie")
    nom_produit = input("saisir le nom du produit: ")
    prix = input("saisir le prix du produit: ")
    qtite_initiale = input("saisir la quantitee: ")
    sql_produit = """INSERT INTO produits(id_categorie,nom_produit,prix,quantité_initiale) values(%s,%s,%s,%s)"""
    valeurs = (id_categorie, nom_produit, prix, qtite_initiale)
    curseur.execute(sql_produit, valeurs)
    connection.commit()


def affichage_produits():
    sql = """SELECT produits.nom_produit,produits.prix,produits.quantité_initiale,Categories.categorie_nom 
    FROM produits 
    join Categories on Categories.id_categorie=produits.id_categorie
    WHERE produits.quantité_initiale>0"""
    curseur.execute(sql)
    affichage = curseur.fetchall()
    for p in affichage:
        print(p)


def mise_a_jour():
    nom_produit = input("saisir le nom  du produit a mettre a jour: ")
    nouvelle_qtité = input("saisir la nouvelle quantité: ")
    sql = """
    UPDATE produits p
    JOIN Categories c ON p.id_categorie = c.id_categorie
    SET p.quantité_initiale = %s
    WHERE p.nom_produit  = %s
    """
    valeurs = (nouvelle_qtité, nom_produit)
    curseur.execute(sql, valeurs)
    connection.commit()
    print("Mise à jour effectuée.")


def Rechercher_produit():
    nom = input("choisir le nom du produit a rechercher: ")
    sql = """SELECT produits.prix,produits.quantité_initiale,produits.nom_produit,Categories.categorie_nom 
    FROM produits 
    join Categories on Categories.id_categorie=produits.id_categorie
    where produits.nom_produit=%s"""
    curseur.execute(sql, (nom,))
    affichage = curseur.fetchone()
    if affichage:
        print(f"produit retrouvé : {affichage}")
    else:
        print("Produit non trouvé.")


def Supprimer_produit():
    identifiant = input("saisir l'id du produit a supprimer: ")
    sql = """delete from produits where id_produit=%s"""
    curseur.execute(sql, (identifiant,))
    connection.commit()
    print(f"Produit supprimé avec succès.")


def Supprimer_categorie():
    identifiant = input("saisir l'id du categorie a supprimer: ")
    sql = """delete from Categories where id_categorie=%s"""
    curseur.execute(sql, (identifiant,))
    connection.commit()
    print(f"Catégorie supprimée avec succès.")


def Dashboard():
    while True:
        print("#### Visualisation ####")
        print("1. Quel est le produit le plus cher ?")
        print("2. Valeur totale financière du stock")
        print("3. Nombre de produits par catégorie")
        print("4. Quitter")

        choix = input("Saisir votre choix : ")

        if choix == "1":
            sql = """
            SELECT c.categorie_nom,p.nom_produit,p.prix
            FROM produits p
            JOIN Categories c ON p.id_categorie = c.id_categorie
            ORDER BY p.prix DESC
            LIMIT 1
            """
            curseur.execute(sql)
            resultat = curseur.fetchone()
            print("voici le produit le plus cher :", resultat)

        elif choix == "2":
            sql = """
            SELECT SUM(prix * quantité_initiale)
            FROM produits
            """
            curseur.execute(sql)
            resultat = curseur.fetchone()
            print("Valeur totale du stock :", resultat)

        elif choix == "3":
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

        elif choix == "4":
            break

        else:
            print("Choix invalide")


def authentification():
    print("Pour continuer, veuillez vous authentifier. 1- S'inscrire 2- Se connecter")
    while True:
        autuh_choice = input("Votre choix : ")
        match autuh_choice:
            case "1":
                sign_up()
            case "2":
                sign_in()
            case _:
                print("Choix invalide")


def sign_up():

    email_exist = True

    if email_exist:
        curseur.execute("SELECT email FROM user")
        emails = [email[0] for email in curseur.fetchall()]

    while True:
        email = input("Entrez votre email : ").strip().lower()
        if email == "" or "@" not in email:
            print("Email invalide. Veuillez réessayer.")
            continue
        if email in emails:
            print("Email déjà utilisé. Veuillez réessayer.")
            continue
        break
    while True:
        password = input("Entrez votre mot de passe: ").strip()
        password_hash = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_hash, salt)

        if len(password) < 8:
            print(
                "Le mot de passe doit contenir au moins 8 caractères. Veuillez réessayer."
            )
            continue
        elif password.isdigit() or password.isalpha():
            print(
                "Le mot de passe doit contenir à la fois des lettres et des chiffres. Veuillez réessayer."
            )
            continue
        break

    query = "INSERT INTO user (email, password) VALUES (%s, %s)"
    values = (email, hashed_password.decode("utf-8"))
    curseur.execute(query, values)
    connection.commit()
    print("Inscription réussie ! Vous pouvez maintenant vous connecter.")
    sign_in()


def sign_in():
    email_exist = True
    
    if email_exist:
        curseur.execute("SELECT email FROM user")
        emails = [email[0] for email in curseur.fetchall()]
        
    
    while True:
        email = input("Entrez votre email : ").strip().lower()
        if email == "" or "@" not in email:
            print("Email invalide. Veuillez réessayer.")
            continue
        elif email not in emails:
            print("Email non trouvé. Veuillez réessayer.")
            continue
        break
    while True:
        password = input("Entrez votre mot de passe : ").strip()
        if password == "":
            print("Mot de passe invalide. Veuillez réessayer.")
            continue
        break
    
    query = "SELECT password FROM user WHERE email = %s"
    curseur.execute(query, (email,))
    result = curseur.fetchone()
    stored_password = result[0].encode("utf-8")
    if bcrypt.checkpw(password.encode("utf-8"), stored_password):
        print("Connexion réussie !")
        menu()
    else:
        print("Mot de passe incorrect. Veuillez réessayer.")
        return sign_in()


def sign_out():
    print("Déconnexion réussie !")
    authentification()

def menu():
    while True:
        print("######  Menu principal  #####")
        print("1.Ajouter un produit")
        print("2.Lister l'inventaire")
        print("3.Mettre à jour le stock")
        print("4.Rechercher un produit")
        print("5.Supprimer un produit")
        print("6.Supprimer une categorie")
        print("7.Dashboard")
        print("8.Deconnexion")
        print("9.Quitter")
        choice = input("faire votre choix: ")
        if choice == "1":
            ajouter_categories()
            ajouter_produit()
        elif choice == "2":
            affichage_produits()
        elif choice == "3":
            mise_a_jour()
        elif choice == "4":
            Rechercher_produit()
        elif choice == "5":
            Supprimer_produit()
        elif choice == "6":
            Supprimer_categorie()
        elif choice == "7":
            Dashboard()
        elif choice == "8":
            sign_out()
        elif choice == "9":
            print("Au revoir !")
            break
        else:
            print("Choix invalide.")


authentification()
curseur.close()
connection.close()
