"""Gestion des "routes" FLASK et des données pour les voiture.
Fichier : gestions_voiture_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.voiture.gestions_voiture_wtf import FormWTFAjouterGenres
from APP_FILMS_164.voiture.gestions_voiture_wtf import FormWTFDeleteGenre
from APP_FILMS_164.voiture.gestions_voiture_wtf import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5575/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les voiture.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_genres_afficher = """SELECT * FROM t_voiture"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_voiture"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_genres_afficher = """SELECT id_voiture, marque, modele  FROM t_voiture WHERE id_voiture = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_genre_selected_dictionnaire)

                    mc_afficher.execute(strsql_genres_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "t_voiture" est vide. !""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"La voiture demandé n'existe pas !", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_voiture" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données voiture affichés !", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("voiture/voiture_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter
    
    Test : ex : http://127.0.0.1:5575/genres_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "voiture/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():

                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()

                name_modele_wtf = form.nom_modele_wtf.data
                name_modele = name_modele_wtf.lower()

                name_chevaux_wtf = form.nom_chevaux_wtf.data
                name_chevaux = name_chevaux_wtf.lower()

                valeurs_insertion_dictionnaire = {"value_intitule_genre": name_genre,
                                                  "value_intitule_nodele": name_modele,
                                                  "value_intitule_chevaux": name_chevaux,
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_voiture (marque, modele, chevaux) VALUES (%(value_intitule_genre)s, %(value_intitule_nodele)s, %(value_intitule_chevaux)s);
                                         """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='ASC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("voiture/voiture_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "voiture" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "voiture_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "voiture/voiture_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_genre_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "voiture_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_voiture_marque_update = form_update.nom_genre_update_wtf.data
            name_voiture_modele_update = form_update.date_genre_wtf_essai.data
            name_voiture_chevaux_update = form_update.nom_voiture_chevaux_update_wtf.data

            valeur_update_dictionnaire = {"value_id_genre": id_genre_update,
                                          "value_name_modele_update": name_voiture_marque_update,
                                          "value_name_marque_update": name_voiture_modele_update,
                                          "value_name_chevaux_update": name_voiture_chevaux_update,
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_voiture SET 
                marque = %(value_name_modele_update)s, 
                modele = %(value_name_marque_update)s,
                chevaux = %(value_name_chevaux_update)s
                WHERE id_voiture = %(value_id_genre)s; """

            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_voiture"
            str_sql_id_genre = "SELECT id_voiture, marque, modele, chevaux FROM t_voiture " \
                               "WHERE id_voiture = %(value_id_genre)s"
            valeur_select_dictionnaire = {"value_id_genre": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["marque"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "voiture_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_genre["marque"]
            form_update.date_genre_wtf_essai.data = data_nom_genre["modele"]
            form_update.nom_voiture_chevaux_update_wtf.data = data_nom_genre["chevaux"]


    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("voiture/voiture_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "voiture" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "voiture_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "voiture/voiture_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_genre_delete = request.values['id_genre_btn_delete_html']
    name_marque_delete = request.values['id_genre_btn_delete_html']
    name_modele_delete =request.values['id_genre_btn_delete_html']
    name_chevaux_delete =request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "voiture/voiture_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer la voiture de façon définitive de la BD !", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_genre_delete,
                                              "value_marque_delete": name_marque_delete,
                                              "value_modele_delete": name_modele_delete,
                                              "value_chevaux_delete": name_chevaux_delete,
                                              }
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre ="""DELETE FROM t_voiture 
                                                WHERE marque = %(value_marque_delete)s
                                                AND modele = %(value_modele_delete)s
                                                AND chevaux = %(value_chevaux_delete)s;
                                            """


                str_sql_delete_idgenre = """DELETE FROM t_voiture WHERE id_voiture = %(value_id_genre)s;"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_voiture_entretien"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_voiture_entretien"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Genre définitivement effacé !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_genre_delete}
            print(id_genre_delete, type(id_genre_delete))

            # Requête qui affiche tous les entretien_voiture qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_voiture_entretien FROM t_voiture_avoir_entretien 
                                            INNER JOIN t_entretien ON t_voiture_avoir_entretien.fk_entretien = t_entretien.id_entretien
                                            INNER JOIN t_voiture ON t_voiture_avoir_entretien.fk_voiture = t_voiture.id_voiture
                                            WHERE fk_voiture = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "voiture/voiture_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_voiture"
                str_sql_id_genre = "SELECT id_voiture FROM t_voiture WHERE id_voiture = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["modele"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "voiture_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_genre["marque"]

            # Le bouton pour l'action "DELETE" dans le form. "voiture_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("voiture/voiture_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
