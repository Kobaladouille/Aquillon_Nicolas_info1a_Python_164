"""
    Fichier : gestions_voiture_wtf.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp
from wtforms.validators import Length, InputRequired, NumberRange, DataRequired
from wtforms import StringField, IntegerField, DateField

class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "voiture_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_chevaux_regexp = "^(. *[^0-9]|)(1000|[1-9]\d{0,2})([^0-9]. *|)$"
    nom_genre_wtf = StringField("Entrez la Marque de la voiture", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_genre_regexp,
                                                                          message="ce champ est obligatoire")
                                                                   ])
    nom_modele_wtf = StringField("Entrez le modèle de la voiture", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_genre_regexp,
                                                                          message="ce champ est obligatoire")
                                                                   ])
    nom_chevaux_wtf = IntegerField("Entrez les chevaux de la voiture ", validators=[NumberRange(min=1, max=5000,
                                                                                            message="ce champ est obligatoire")])

    submit = SubmitField("Ajouter la voiture")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "voiture_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_genre_update_wtf = StringField("Modifier la marque de la voiture", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_genre_wtf_essai = StringField("Modifer le modele de la voiture ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    nom_voiture_chevaux_update_wtf = IntegerField("Modifier les chevaux de la voiture ", validators=[NumberRange(min=1, max=5000,
                                                                                            message=u"Min %(min)d et "
                                                                                                    u"max %(max)d "
                                                                                                    u"Selon Wikipédia "
                                                                                                    u"L'Incendie du "
                                                                                                    u"monastère du "
                                                                                                    u"Lotus rouge "
                                                                                                    u"durée 1620 "
                                                                                                    u"min")])
    submit = SubmitField("Modifier la voiture")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "voiture_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Effacer cette voiture")
    submit_btn_del = SubmitField("Effacer voiture")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
