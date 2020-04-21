<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:exslt="http://exslt.org/common">
    <xsl:output method="html" doctype-public="-//W3C//DTD HTML 5 Transitional//EN" encoding="utf-8" indent="yes"/>

    <xsl:variable name="minuscules" select="'aãbcçdeèềẽfghiîjklmnńoòôõpqrstuûvwxyz'" />
    <xsl:variable name="majuscules" select="'AÃBCÇDEÈỀẼFGHIÎJKLMNŃOÒÔÕPQRSTUÛVWXYZ'" />

    <xsl:param name="racine"/>
    <xsl:param name="languev"/>
    <xsl:param name="langue1"/>
    <xsl:param name="langue2"/>
    <xsl:param name="langue3"/>
    <xsl:param name="caractère" select="'*'"/>

    <xsl:variable name="langues">
        <langue><xsl:value-of select="$languev"/></langue>
        <langue><xsl:value-of select="$langue1"/></langue>
        <langue><xsl:value-of select="$langue2"/></langue>
        <langue><xsl:value-of select="$langue3"/></langue>
    </xsl:variable>

    <xsl:template match="RessourceLexicale">
        <!--<html>
            <head>
                <title>
                    <xsl:value-of select="InformationsGlobales/Général/Nom"/> – <xsl:value-of select="InformationsGlobales/Général/Auteur"/>
                </title>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"/>
                <link rel="stylesheet" type="text/css" href="style.css"/>
            </head>
            <body data-spy="scroll" data-target="#liste-index" data-offset="0">
                <script src="https://code.jquery.com/jquery-3.3.1.min.js"	 integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>-->
                <!-- Début du contenu. -->
                <div class="container-fluid">
                    <div class="row">
                        <nav id="gouvernail" class="navbar navbar-expand-lg navbar-light bg-light justify-content-between fixed-top">
                            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#barre-navigation" aria-controls="barre-navigation" aria-expanded="false" aria-label="Basculer navigation">
                                <span class="navbar-toggler-icon"></span>
                            </button>
                            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#index" aria-controls="index«" aria-expanded="false" aria-label="Basculer navigation">
                                <span class="navbar-toggler-icon"></span>
                            </button>
                            <xsl:element name="a">
                                <xsl:attribute name="class">nav-link</xsl:attribute>
                                <xsl:attribute name="class">navbar-brand</xsl:attribute>
                                <xsl:attribute name="href"><xsl:value-of select="$racine"/></xsl:attribute>
                                <xsl:text>Accueil</xsl:text>
                            </xsl:element>
                            <div class="collapse navbar-collapse" id="barre-navigation">
                                <ul class="navbar-nav mr-auto">
                                    <li id="dictionnaires" class="dropdown">
                                        <xsl:call-template name="dictionnaires"/>
                                    </li>
                                    <li id="lettrines">
                                        <xsl:call-template name="lettrines"/>
                                    </li>
                                </ul>
                                <!--<xsl:call-template name="recherche"/>
                                <xsl:call-template name="sélecteur_langue"/>-->
                            </div>
                        </nav>
                    </div>
                    <div class="row">
                        <div id="index" class="fixed-top col col-lg-1">
                            <xsl:call-template name="index"/>
                        </div>
                        <div id="corps" class="col col-lg-11">
                            <xsl:call-template name="dictionnaire"/>
                        </div>
                    </div>
                </div>
            <!--</body>
        </html>-->
    </xsl:template>

    <xsl:template match="InformationsGlobales">
    </xsl:template>

    <xsl:template name="dictionnaires">
        <a class="dropdown-toggle nav-link" data-toggle="dropdown">Dictionnaires <span class="caret"></span></a>
        <ul id="menu-dictionnaires" class="dropdown-menu">
            <li class="nav-item">Mwotlap
                <ul>
                    <li class="nav-item">
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:call-template name="adresse">
                                    <xsl:with-param name="languev" select="'mlv'"/>
                                    <xsl:with-param name="langue1" select="'bis'"/>
                                    <xsl:with-param name="langue2" select="'fra'"/>
                                    <xsl:with-param name="langue3" select="'eng'"/>
                                    <xsl:with-param name="caractère" select="$caractère"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:text>Mtp – Bis – Fr – Eng</xsl:text>
                        </xsl:element>
                    </li>
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:call-template name="adresse">
                                    <xsl:with-param name="languev" select="'mlv'"/>
                                    <xsl:with-param name="langue1" select="'bis'"/>
                                    <xsl:with-param name="langue2" select="'eng'"/>
                                    <xsl:with-param name="langue3" select="'fra'"/>
                                    <xsl:with-param name="caractère" select="$caractère"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:text>Mtp – Bis – Eng – Fr</xsl:text>
                        </xsl:element>
                    </li>
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:call-template name="adresse">
                                    <xsl:with-param name="languev" select="'mlv'"/>
                                    <xsl:with-param name="langue1" select="'fra'"/>
                                    <xsl:with-param name="caractère" select="$caractère"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:text>Mtp – Fr</xsl:text>
                        </xsl:element>
                    </li>
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:call-template name="adresse">
                                    <xsl:with-param name="languev" select="'mlv'"/>
                                    <xsl:with-param name="langue1" select="'eng'"/>
                                    <xsl:with-param name="caractère" select="$caractère"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:text>Mtp – Eng</xsl:text>
                        </xsl:element>
                    </li>
                </ul>
            </li>
            <li class="dropdown-divider"></li>
            <li>Teanu
                <ul>
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:call-template name="adresse">
                                    <xsl:with-param name="languev" select="'mlv'"/>
                                    <xsl:with-param name="langue1" select="'fra'"/>
                                    <xsl:with-param name="langue2" select="'eng'"/>
                                    <xsl:with-param name="caractère" select="$caractère"/>
                                </xsl:call-template>
                            </xsl:attribute>
                            <xsl:text>Tea – Fr – Eng</xsl:text>
                        </xsl:element>
                    </li>
                </ul>
            </li>
        </ul>
    </xsl:template>

    <xsl:template name="lettrines">
        <ul class="nav navbar-nav flex-row nav-pills">
            <li>
                <xsl:element name="a">
                    <xsl:attribute name="class">nav-link</xsl:attribute>
                    <xsl:attribute name="href">
                        <xsl:text>?caractère=*</xsl:text>
                    </xsl:attribute>
                    <xsl:text>*</xsl:text>
                </xsl:element>
            </li>
            <li class="divider"></li>
            <xsl:for-each select="Dictionnaire/EntréeLexicale">
                <xsl:variable name="lettrine" select="substring(translate(translate(Lemme/ReprésentationDeForme, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)"/>
                <xsl:if test="$lettrine != substring(translate(translate(preceding-sibling::EntréeLexicale[1]/Lemme/ReprésentationDeForme, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)">
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:text>?caractère=</xsl:text>
                                <xsl:value-of select="$lettrine"/>
                            </xsl:attribute>
                            <xsl:value-of select="$lettrine"/>
                        </xsl:element>
                    </li>
                </xsl:if>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <xsl:template name="recherche">
        <form class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2" type="search" placeholder="Tapez quelque chose…" aria-label="Recherche" lang="fr"/>
            <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Recherchez</button>
        </form>
    </xsl:template>

    <xsl:template name="sélecteur_langue">
    </xsl:template>

    <xsl:template name="index">
        <ul id="liste-index" class="nav flex-column nav-pills">
            <xsl:for-each select="Dictionnaire/EntréeLexicale">
                <xsl:if test="$caractère = '*' or $caractère != '*' and substring(Lemme/ReprésentationDeForme, 1, 1) = $caractère">
                    <li class="nav-item">
                        <xsl:element name="a">
                            <xsl:attribute name="class">nav-link</xsl:attribute>
                            <xsl:attribute name="href">
                                <xsl:text>#</xsl:text>
                                <xsl:value-of select="@identifiant"/>
                            </xsl:attribute>
                            <xsl:value-of select="Lemme/ReprésentationDeForme"/><sub class="homonyme"><xsl:value-of select="NuméroDHomonyme"/></sub><br/>
                        </xsl:element>
                    </li>
                </xsl:if>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <xsl:template name="dictionnaire">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="EntréeLexicale">
        <xsl:if test="$caractère = '*' or $caractère != '*' and substring(Lemme/ReprésentationDeForme, 1, 1) = $caractère">
            <div class="entrée">
                <xsl:attribute name="id">
                    <xsl:value-of select="@identifiant"/>
                </xsl:attribute>
                <p class="en-tête_entrée">
                    <span class="vedette">
                        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
                    </span>
                    <xsl:if test="NuméroDHomonyme">
                        <xsl:apply-templates select="NuméroDHomonyme"/>
                    </xsl:if>
                    <xsl:if test="Lemme/FormeDeCitation">
                        <xsl:apply-templates select="Lemme/FormeDeCitation"/>
                    </xsl:if>
                    <xsl:if test="Lemme/Variante">
                        <span class="variantes">
                            <xsl:for-each select="Lemme/Variante">
                                <xsl:apply-templates select="."/>
                                <xsl:if test="not(position() = last())">, </xsl:if>
                            </xsl:for-each>
                        </span>
                    </xsl:if>
                    <xsl:if test="Lemme/FormePhonétique">
                        <xsl:apply-templates select="Lemme/FormePhonétique"/>
                    </xsl:if>
                    <xsl:if test="ClasseGrammaticale">
                        <xsl:apply-templates select="ClasseGrammaticale"/>
                    </xsl:if>
                </p>
                <xsl:apply-templates select="Groupe|Sens|Sous-entrée"/>
                <xsl:apply-templates select="Étymologie"/>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="Sous-entréeLexicale">
        <div class="sous-entrée">
            <xsl:attribute name="id">
                <xsl:value-of select="@identifiant"/>
            </xsl:attribute>
            <p class="en-tête_sous-entrée">
                <span class="vedette">
                    <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
                </span>
                 <xsl:if test="Lemme/FormeDeCitation">
                    <xsl:apply-templates select="Lemme/FormeDeCitation"/>
                </xsl:if>
                <xsl:if test="Lemme/FormePhonétique">
                    <xsl:apply-templates select="Lemme/FormePhonétique"/>
                </xsl:if>
                <xsl:if test="ClasseGrammaticale">
                    <xsl:apply-templates select="ClasseGrammaticale"/>
                </xsl:if>
            </p>
            <xsl:apply-templates select="Sens"/>
            <xsl:apply-templates select="Étymologie"/>
        </div>
    </xsl:template>

    <xsl:template match="Groupe">
        <div class="groupe">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <xsl:apply-templates select="NomDeGroupe"/>
            <xsl:if test="ClasseGrammaticale">
                <xsl:apply-templates select="ClasseGrammaticale"/>
            </xsl:if>
            <xsl:apply-templates select="Sens|Sous-entrée"/>
        </div>
    </xsl:template>

    <xsl:template match="Sens">
        <div class="sens">
            <xsl:attribute name="id">
                <xsl:value-of select="@identifiant"/>
            </xsl:attribute>
            <xsl:apply-templates select="NuméroDeSens"/>
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="exslt:node-set($langues)/langue">
                <xsl:variable name="langue" select="node()"/>
                <xsl:choose>
                    <xsl:when test="$parent/Définition">
                        <xsl:apply-templates select="$parent/Définition[ReprésentationDeTexte[@langue=$langue]]"/>
                    </xsl:when>
                    <xsl:when test="$parent/Glose">
                        <xsl:apply-templates select="$parent/Glose[@langue=$langue]"/>
                    </xsl:when>
                </xsl:choose>
            </xsl:for-each>
            <xsl:apply-templates select="Exemple"/>
            <xsl:apply-templates select="Sous-entréeLexicale"/>
            <xsl:apply-templates select="Sens"/>
        </div>
    </xsl:template>

    <xsl:template match="Glose">
        <span class="glose">
            <span>
        		<xsl:attribute name="class">
                    <xsl:call-template name="statut_langue">
                        <xsl:with-param name="code" select="@langue"/>
                    </xsl:call-template>
                </xsl:attribute>
                <xsl:value-of select="node()"/>
            </span>
        </span>
    </xsl:template>

    <xsl:template match="Définition">
        <span class="définition">
            <xsl:apply-templates select="Étiquette[Type='syntaxe']"/>
            <xsl:apply-templates select="TraductionLittérale"/>
            <xsl:apply-templates select="ReprésentationDeTexte"/>
        </span>
    </xsl:template>

    <xsl:template match="Exemple">
        <div class="exemple">
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="exslt:node-set($langues)/langue">
                <xsl:variable name="langue" select="node()"/>
                <span class="traduction_exemple">
                    <xsl:apply-templates select="$parent/ReprésentationDeTexte[@langue=$langue]"/>
                </span>
            </xsl:for-each>
        </div>
    </xsl:template>

    <xsl:template match="Étymologie">
        <div class="étymologie">
            <xsl:apply-templates select="Étymon"/>
        </div>
    </xsl:template>

    <xsl:template match="Étymon">
        <span class="étymon">
            <xsl:apply-templates select="Langue"/>
            <span class="forme_étymon">
                <xsl:apply-templates select="ReprésentationDeForme"/>
            </span>
            <xsl:apply-templates select="Glose"/>
        </span>
    </xsl:template>

    <xsl:template match="Langue">
        <span class="langue">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="Glose[name(..)='Étymon']">
        <span class="glose_étymon">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="ReprésentationDeForme">
        <xsl:value-of select="node()"/>
    </xsl:template>

    <xsl:template match="NuméroDHomonyme">
        <span class="homonyme">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="FormeDeCitation">
        <span class="forme_citation">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="Variante">
        <span class="variante">
            <xsl:value-of select="ReprésentationDeForme"/>
            <xsl:if test="Région">
                <xsl:apply-templates select="Région"/>
            </xsl:if>
        </span>
    </xsl:template>

    <xsl:template match="Région">
        <span class="région">
        <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="FormePhonétique">
        <span class="forme_phonétique">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="ClasseGrammaticale">
        <span class="classe_grammaticale">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="NomDeGroupe">
        <span class="nom_groupe">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="NuméroDeSens">
        <span class="numéro_sens">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="Étiquette[Type='syntaxe']">
        (<span class="étiquette_syntaxique">
            <xsl:apply-templates select="ReprésentationDeTexte"/>
        </span>)
    </xsl:template>

    <xsl:template match="TraductionLittérale">
        <span>
            <xsl:attribute name="class">
                <xsl:text>traduction_littérale </xsl:text>
                <xsl:value-of select="@langue"/><xsl:text> </xsl:text>
                <xsl:call-template name="statut_langue">
                    <xsl:with-param name="code" select="@langue"/>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:apply-templates select="node()"/>
        </span>
    </xsl:template>

    <xsl:template match="DomaineSémantique">
        <span class="domaine_sémantique">
            <xsl:text>&lt;</xsl:text><xsl:value-of select="caractéristique[@attribut='domaine']/@valeur"/><xsl:text>&gt;</xsl:text>
        </span>
    </xsl:template>

    <xsl:template match="noms_scientifiques">
        <xsl:for-each select="NomScientifique">
            <p class="nom_scientifique">
                <xsl:text>☘ </xsl:text>
		<xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:value-of select="concat('http://www.google.com/images?q=', caractéristique[@attribut='nom']/@valeur)"/>
                    </xsl:attribute>
                    <xsl:attribute name="target">
						<xsl:text>_blank</xsl:text>
					</xsl:attribute>
                    <xsl:choose>
                        <xsl:when test="caractéristique/contenu">
                            <xsl:apply-templates select="caractéristique/contenu"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="caractéristique[@attribut='nom']/@valeur"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
            </p>
        </xsl:for-each>
    </xsl:template>


    <xsl:template match="commentaires">
        <span class="commentaireDexemple">
            [<xsl:value-of select="CommentaireDexemple/caractéristique[@attribut='commentaire']/@valeur"/>]
        </span>
    </xsl:template>

    <xsl:template match="relations_sémantiques">
        <p>
            <xsl:for-each select="RelationSémantique">
                <span class="relation_sémantique">
                    <span class="type">
                        <xsl:value-of select="caractéristique[@attribut='type']/@valeur"/>
                        <xsl:text> : </xsl:text>
                    </span>
                    <xsl:apply-templates select="node()"/>
                </span>
            </xsl:for-each>
        </p>
    </xsl:template>

    <xsl:template match="Note[caractéristique[@attribut='type' and @valeur='syntaxique']]">
        <span class="syntax">
            [<xsl:value-of select="caractéristique[@attribut='note']/@valeur"/>]
        </span>
    </xsl:template>
   <xsl:template match="Note[caractéristique[@attribut='type' and @valeur='usage']]">
        <span class="sujet">
            (<xsl:value-of select="caractéristique[@attribut='note']/@valeur"/>)
        </span>
    </xsl:template>

    <xsl:template match="Image">
        <figure>
            <xsl:element name="img">
                <xsl:attribute name="src">
		    <xsl:text>./img/</xsl:text>
                    <xsl:value-of select="caractéristique[@attribut='chemin']/@valeur"/>
                </xsl:attribute>
		<xsl:attribute name="class">
                    <xsl:text>figure</xsl:text>
		</xsl:attribute>
		 <xsl:attribute name="max-width">
                    <xsl:text>200</xsl:text>
		</xsl:attribute>
            </xsl:element>
            <xsl:element name="figcaption">
                <xsl:choose>
                    <xsl:when test="caractéristique/contenu">
                        <xsl:apply-templates select="caractéristique/contenu"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="caractéristique[@attribut='légende']/@valeur"/>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:element>
        </figure>
    </xsl:template>

    <xsl:template match="Tableau">
        <div class="tableau">
            <xsl:apply-templates select="Titre"/>
            <table>
                <xsl:for-each select="Contenu/groupe">
                    <tr>
                        <xsl:for-each select="node()">
                            <td>
                                <xsl:choose>
                                    <xsl:when test="variante">
                                        <xsl:for-each select="node()">
                                            <xsl:choose>
                                                <xsl:when test="lien">
                                                    <xsl:apply-templates select="node()"/>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <xsl:value-of select="."/>
                                                </xsl:otherwise>
                                            </xsl:choose>
                                            <xsl:if test="not(position() = last())"> ; </xsl:if>
                                        </xsl:for-each>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:choose>
                                            <xsl:when test="lien">
                                                <xsl:apply-templates select="node()"/>
                                            </xsl:when>
                                            <xsl:otherwise>
                                                <xsl:value-of select="."/>
                                            </xsl:otherwise>
                                        </xsl:choose>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </td>
                        </xsl:for-each>
                    </tr>
                </xsl:for-each>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="Encadré">
        <div class="encadré">
            <xsl:apply-templates select="Titre"/>
            <xsl:for-each select="ReprésentationDeTexte">
                <div>
                    <xsl:attribute name="class">
                        <xsl:variable name="statut">
                            <xsl:call-template name="statut_langue">
                                <xsl:with-param name="code" select="@langue"/>
                            </xsl:call-template>
                        </xsl:variable>
                    </xsl:attribute>
                    <xsl:apply-templates select="node()"/>
                </div>
                <xsl:text> </xsl:text>
            </xsl:for-each>
        </div>
    </xsl:template>

    <xsl:template match="Titre">
        <span class="titre">
            <span>
                <xsl:attribute name="class">
            		<xsl:text> </xsl:text>
                    <xsl:call-template name="statut_langue">
                        <xsl:with-param name="code" select="@langue"/>
                    </xsl:call-template>
                </xsl:attribute>
                <xsl:value-of select="node()"/>
            </span>
        </span>
    </xsl:template>

    <xsl:template match="ReprésentationDeTexte">
        <span>
    		<xsl:attribute name="class">
                <xsl:call-template name="statut_langue">
                    <xsl:with-param name="code" select="@langue"/>
                </xsl:call-template>
            </xsl:attribute>
            <xsl:apply-templates/>
        </span>
    </xsl:template>

    <xsl:template match="lien">
        <xsl:element name="a">
<!--            <xsl:attribute name="target">
                <xsl:text>_blank</xsl:text>
            </xsl:attribute>-->
		<xsl:attribute name="class">
                <xsl:text>lien_ok</xsl:text>
            </xsl:attribute>
            <xsl:attribute name="href">
                <xsl:call-template name="adresse">
                    <xsl:with-param name="languev" select="$languev"/>
                    <xsl:with-param name="langue1" select="$langue1"/>
                    <xsl:with-param name="langue2" select="$langue2"/>
                    <xsl:with-param name="langue3" select="$langue3"/>
                    <xsl:with-param name="caractère" select="substring(@cible, 2, 1)"/>
                </xsl:call-template>
                <xsl:text>#</xsl:text>
                <xsl:value-of select="@cible"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>

    <xsl:template match="non_lien">
        <span class="lien_brisé">
            <xsl:value-of select="."/>
        </span>
    </xsl:template>

    <xsl:template match="style">
        <xsl:element name="span">
            <xsl:attribute name="class">
                <xsl:value-of select="@type"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </xsl:element>
    </xsl:template>

    <xsl:template name="statut_langue">
        <xsl:param name="code"/>
        <xsl:choose>
            <xsl:when test="$code = $langue1">
                <xsl:value-of select="'langue1'"/>
            </xsl:when>
            <xsl:when test="$code = $langue2">
                <xsl:value-of select="'langue2'"/>
            </xsl:when>
            <xsl:when test="$code = $languev">
                <xsl:value-of select="'languev'"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="adresse">
        <xsl:param name="languev"/>
        <xsl:param name="langue1"/>
        <xsl:param name="langue2"/>
        <xsl:param name="langue3"/>
        <xsl:param name="caractère"/>
        <xsl:value-of select="$racine"/>
        <xsl:text>?languev=</xsl:text>
        <xsl:value-of select="$languev"/>
        <xsl:text>&amp;langue1=</xsl:text>
        <xsl:value-of select="$langue1"/>
        <xsl:if test="$langue2">
            <xsl:text>&amp;langue2=</xsl:text>
            <xsl:value-of select="$langue2"/>
        </xsl:if>
        <xsl:if test="$langue3">
            <xsl:text>&amp;langue3=</xsl:text>
            <xsl:value-of select="$langue3"/>
        </xsl:if>
        <xsl:text>&amp;caractère=</xsl:text>
        <xsl:value-of select="$caractère"/>
    </xsl:template>
</xsl:stylesheet>
