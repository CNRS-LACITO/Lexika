<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" encoding="utf-8" indent="yes"/>

    <xsl:variable name="minuscules" select="'abcdeēfghijklmm̄n̄noōpqrstuvwxyz'" />
    <xsl:variable name="majuscules" select="'ABCDEĒFGHIJKLMM̄N̄NOŌPQRSTUVWXYZ'" />
    <xsl:variable name="lang1" select="'eng'"/>
    <xsl:variable name="lang2" select="'fra'"/>
    <xsl:variable name="langn" select="'mlv'"/>
    <xsl:variable name="char" select="'*'"/>
    <xsl:variable name="langues" select="RessourcesLexicales/InformationsGlobales/langues/Langue"/>

    <xsl:template match="RessourcesLexicales">
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="style.css"/>
                <title>
                    <xsl:value-of select="InformationsGlobales/caractéristique[@attribut='nom']/@valeur"/>
                    -
                    <xsl:value-of select="InformationsGlobales/caractéristique[@attribut='auteur']/@valeur"/>
                </title>
            </head>
            <body>
                <div id="lettrines">
                    <xsl:call-template name="lettrines"/>
                </div>
                <div id="entrées">
                    <xsl:call-template name="entrées"/>
                </div>
                <div id="corps">
                    <xsl:call-template name="dictionnaire"/>
                </div>
            </body>
        </html>
    </xsl:template>

    <xsl:template name="lettrines">
        <ul>
            <li>
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:text>?char=*</xsl:text>
                    </xsl:attribute>
                    <xsl:text>Toutes</xsl:text>
                </xsl:element>
            </li>
            <xsl:for-each select="Dictionnaire/entrées/Entrée">
                <xsl:variable name="lettrine" select="substring(translate(translate(caractéristique[@attribut='vedette']/@valeur, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)"/>
                <xsl:if test="$lettrine != substring(translate(translate(preceding-sibling::Entrée[1]/caractéristique[@attribut='vedette']/@valeur, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)">
                    <li>
                        <xsl:element name="a">
                            <xsl:attribute name="href">
                                <xsl:text>?char=</xsl:text>
                                <xsl:value-of select="$lettrine"/>
                            </xsl:attribute>
                            <xsl:value-of select="$lettrine"/>
                        </xsl:element>
                    </li>
                </xsl:if>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <xsl:template name="entrées">
        <xsl:for-each select="Dictionnaire/entrées/Entrée">
            <xsl:if test="$char = '*' or $char != '*' and substring(caractéristique[@attribut='vedette']/@valeur, 1, 1) = $char">
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:text>#</xsl:text>
                        <xsl:value-of select="@id"/>
                    </xsl:attribute>
                    <xsl:value-of select="caractéristique[@attribut='vedette']/@valeur"/><sub class="homonyme"><xsl:value-of select="caractéristique[@attribut='homonyme']/@valeur"/></sub><br/>
                </xsl:element>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="dictionnaire">
        <xsl:apply-templates select="Dictionnaire/entrées"/>
    </xsl:template>

    <xsl:template match="Entrée">
        <xsl:if test="$char = '*' or $char != '*' and substring(caractéristique[@attribut='vedette']/@valeur, 1, 1) = $char">
            <div class="entrée">
                <xsl:attribute name="id">
                    <xsl:value-of select="./@id"/>
                </xsl:attribute>
                <p class="en-tête_entrée">
                    <span class="vedette">
                        <xsl:value-of select="caractéristique[@attribut='vedette']/@valeur"/>
                    </span>
                    <xsl:if test="caractéristique[@attribut='homonyme']">
                        <span class="homonyme">
                            <xsl:value-of select="caractéristique[@attribut='homonyme']/@valeur"/>
                        </span>
                    </xsl:if>
                    <xsl:if test="caractéristique[@attribut='forme de citation']">
                        <span class="forme_citation">
                            (<xsl:value-of select="caractéristique[@attribut='forme de citation']/@valeur"/>)
                        </span>
                    </xsl:if>
                    <xsl:if test="variantes">
                        <xsl:text> (</xsl:text>
                        <span class="variante">
                            <xsl:for-each select="variantes/Variante">
                                <xsl:value-of select="caractéristique[@attribut='variante']/@valeur"/>
                                <xsl:if test="not(position() = last())">, </xsl:if>
                            </xsl:for-each>
                        </span>
                        <xsl:text>)</xsl:text>
                    </xsl:if>
                    <xsl:if test="caractéristique[@attribut='phonétique']">
                        <span class="phonétique">
                            <xsl:text> </xsl:text>
                            [<xsl:value-of select="caractéristique[@attribut='phonétique']/@valeur"/>]
                        </span>
                    </xsl:if>
                    <span class="classe_grammaticale">
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="caractéristique[@attribut='classe grammaticale']/@valeur"/>
                    </span>
                </p>
                <xsl:apply-templates select="groupes"/>
                <xsl:apply-templates select="médias"/>
                <xsl:apply-templates select="domaines_sémantiques"/>
                <xsl:apply-templates select="sens_littéraux"/>
                <xsl:choose>
                    <xsl:when test="définitions">
                        <xsl:apply-templates select="définitions"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="gloses"/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:apply-templates select="noms_scientifiques"/>
                <xsl:apply-templates select="informations_encyclopédiques"/>
                <xsl:apply-templates select="relations_sémantiques"/>
                <xsl:apply-templates select="exemples"/>
                <xsl:apply-templates select="sens"/>
                <xsl:apply-templates select="étymologies"/>
                <xsl:apply-templates select="tableaux"/>
                <xsl:apply-templates select="encadrés"/>
                <xsl:apply-templates select="sous-entrées"/>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="Groupe">
        <div class="groupe">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="nom_groupe">
                <xsl:value-of select="caractéristique[@attribut='nom']/@valeur"/>
            </span>
            <span class="classe_grammaticale">
                <xsl:text> </xsl:text>
                <xsl:value-of select="caractéristique[@attribut='classe grammaticale']/@valeur"/>
            </span>
            <xsl:apply-templates select="médias"/>
            <xsl:apply-templates select="domaines_sémantiques"/>
            <xsl:apply-templates select="sens_littéraux"/>
            <xsl:choose>
                <xsl:when test="définitions">
                    <xsl:apply-templates select="définitions"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="gloses"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="noms_scientifiques"/>
            <xsl:apply-templates select="informations_encyclopédiques"/>
            <xsl:apply-templates select="relations_sémantiques"/>
            <xsl:apply-templates select="exemples"/>
            <xsl:apply-templates select="sens"/>
            <xsl:apply-templates select="tableaux"/>
            <xsl:apply-templates select="encadrés"/>
            <xsl:apply-templates select="sous-entrées"/>
        </div>
    </xsl:template>

    <xsl:template match="Sens">
        <div class="sens">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="numéro_sens">
                <xsl:value-of select="caractéristique[@attribut='acception']/@valeur"/>.
            </span>
            <xsl:apply-templates select="médias"/>
            <xsl:apply-templates select="domaines_sémantiques"/>
            <xsl:apply-templates select="sens_littéraux"/>
            <xsl:choose>
                <xsl:when test="définitions">
                    <xsl:apply-templates select="définitions"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="gloses"/>
                </xsl:otherwise>
            </xsl:choose>
            <div class="bloc">
                <xsl:apply-templates select="noms_scientifiques"/>
                <xsl:apply-templates select="informations_encyclopédiques"/>
                <xsl:apply-templates select="relations_sémantiques"/>
                <xsl:apply-templates select="exemples"/>
                <xsl:apply-templates select="étymologies"/>
                <xsl:apply-templates select="tableaux"/>
                <xsl:apply-templates select="encadrés"/>
                <xsl:apply-templates select="sous-entrées"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="SousEntrée">
        <div class="sous-entrée">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <p class="en-tête_sous-entrée">
                <span class="vedette">
                    <xsl:value-of select="caractéristique[@attribut='vedette']/@valeur"/>
                </span>
                <xsl:if test="caractéristique[@attribut='homonyme']">
                    <span class="homonyme">
                        <xsl:value-of select="caractéristique[@attribut='homonyme']/@valeur"/>
                    </span>
                </xsl:if>
                <xsl:if test="caractéristique[@attribut='forme de citation']">
                    <span class="forme_citation">
                        (<xsl:value-of select="caractéristique[@attribut='forme de citation']/@valeur"/>)
                    </span>
                </xsl:if>
                <xsl:if test="variantes">
                        <xsl:text> (</xsl:text>
                        <span class="variante">
                            <xsl:for-each select="variantes/Variante">
                                <xsl:value-of select="caractéristique[@attribut='variante']/@valeur"/>
                                <xsl:if test="not(position() = last())">, </xsl:if>
                            </xsl:for-each>
                        </span>
                        <xsl:text>)</xsl:text>
                    </xsl:if>
                <xsl:if test="caractéristique[@attribut='phonétique']">
                    <span class="phonétique">
                        <xsl:text> </xsl:text>
                        [<xsl:value-of select="caractéristique[@attribut='phonétique']/@valeur"/>]
                    </span>
                </xsl:if>
                <span class="classe_grammaticale">
                    <xsl:text> </xsl:text>
                    <xsl:value-of select="caractéristique[@attribut='classe grammaticale']/@valeur"/>
                </span>
            </p>
            <xsl:apply-templates select="médias"/>
            <xsl:apply-templates select="domaines_sémantiques"/>
            <xsl:apply-templates select="sens_littéraux"/>
            <xsl:choose>
                <xsl:when test="définitions">
                    <xsl:apply-templates select="définitions"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="gloses"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:apply-templates select="noms_scientifiques"/>
            <xsl:apply-templates select="informations_encyclopédiques"/>
            <xsl:apply-templates select="exemples"/>
            <xsl:apply-templates select="relations_sémantiques"/>
            <xsl:apply-templates select="étymologies"/>
            <xsl:apply-templates select="tableaux"/>
            <xsl:apply-templates select="encadrés"/>
        </div>
    </xsl:template>

    <xsl:template match="DomaineSémantique">
        <span class="domaine_sémantique">
            <xsl:text>&lt;</xsl:text><xsl:value-of select="caractéristique[@attribut='domaine']/@valeur"/><xsl:text>&gt;</xsl:text>
        </span>
    </xsl:template>

    <xsl:template match="SensLittéral">
        <span class="sens_littéral">
            (<xsl:value-of select="caractéristique[@attribut='sens littéral']/@valeur"/>)
        </span>
    </xsl:template>

    <xsl:template match="définitions">
        <xsl:for-each select="Définition">
            <xsl:apply-templates select="notes"/>
            <xsl:apply-templates select="sens_littéraux"/>
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="$langues">
                <xsl:if test="$parent/caractéristique[@attribut='langue']/@valeur = @id">
                    <span class="définition">
                        <xsl:attribute name="id">
                            <xsl:value-of select="$parent/@id"/>
                        </xsl:attribute>
                        <span class="texte_définition">
                            <xsl:element name="span">
                                <xsl:attribute name="class">
                                    <xsl:variable name="statut">
                                        <xsl:call-template name="statut_langue">
                                            <xsl:with-param name="code" select="$parent/caractéristique[@attribut='langue']/@valeur"/>
                                        </xsl:call-template>
                                    </xsl:variable>
                                    <xsl:value-of select="concat(@id, ' ', $statut)"/>
                                </xsl:attribute>
                                <xsl:text>✧ </xsl:text>
                                <xsl:if test="$parent/étiquettes_sémantiques">
                                    <xsl:text>(</xsl:text>
                                    <span class="étiquette_sémantique">
                                        <xsl:for-each select="$parent/étiquettes_sémantiques/ÉtiquetteSémantique">
                                            <xsl:value-of select="caractéristique[@attribut='nom']/@valeur"/>
                                            <xsl:if test="not(position() = last())">, </xsl:if>
                                        </xsl:for-each>
                                    </span>
                                    <xsl:text>) </xsl:text>
                                </xsl:if>
                                <xsl:choose>
                                    <xsl:when test="$parent/caractéristique/contenu">
                                        <xsl:apply-templates select="$parent/caractéristique/contenu"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="$parent/caractéristique[@attribut='définition']/@valeur"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:element>
                        </span>
                    </span>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="gloses">
        <xsl:for-each select="Glose">
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="$langues">
                <xsl:if test="$parent/caractéristique[@attribut='langue']/@valeur = @id">
                    <span class="glose">
                        <xsl:attribute name="id">
                            <xsl:value-of select="$parent/@id"/>
                        </xsl:attribute>
                        <span class="texte_glose">
                            <xsl:element name="span">
                                <xsl:attribute name="class">
                                    <xsl:variable name="statut">
                                        <xsl:call-template name="statut_langue">
                                            <xsl:with-param name="code" select="$parent/caractéristique[@attribut='langue']/@valeur"/>
                                        </xsl:call-template>
                                    </xsl:variable>
                                    <xsl:value-of select="concat(@id, ' ', $statut)"/>
                                </xsl:attribute>
                                <xsl:text>✧ </xsl:text>
                                <xsl:choose>
                                    <xsl:when test="$parent/caractéristique/contenu">
                                        <xsl:apply-templates select="$parent/caractéristique/contenu"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="$parent/caractéristique[@attribut='glose']/@valeur"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:element>
                        </span>
                    </span>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="exemples">
        <xsl:for-each select="Exemple">
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="$langues">
                <xsl:if test="$parent/caractéristique[@attribut='langue']/@valeur = @id">
                    <p class="exemple">
                        <xsl:attribute name="id">
                            <xsl:value-of select="./@id"/>
                        </xsl:attribute>
                        <span class="texte_exemple">
                            <xsl:element name="span">
                                <xsl:attribute name="class">
                                    <xsl:variable name="statut">
                                        <xsl:call-template name="statut_langue">
                                            <xsl:with-param name="code" select="$parent/caractéristique[@attribut='langue']/@valeur"/>
                                        </xsl:call-template>
                                    </xsl:variable>
                                    <xsl:value-of select="concat(@id, ' ', $statut)"/>
                                </xsl:attribute>
                                <xsl:text>➥ </xsl:text>
                                <xsl:choose>
                                    <xsl:when test="$parent/caractéristique/contenu">
                                        <xsl:apply-templates select="$parent/caractéristique/contenu"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="$parent/caractéristique[@attribut='exemple']/@valeur"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:element>
                        </span>
                        <xsl:apply-templates select="$parent/traductions"/>
                        <xsl:apply-templates select="$parent/notes"/>
                    </p>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
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

    <xsl:template match="informations_encyclopédiques">
        <xsl:for-each select="InformationEncyclopédique">
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="$langues">
                <xsl:if test="$parent/caractéristique[@attribut='langue']/@valeur = @id">
                    <p class="informations_encyclopédiques">
                        <xsl:attribute name="id">
                            <xsl:value-of select="./@id"/>
                        </xsl:attribute>
                        <span class="texte_informations">
                            <xsl:element name="span">
                                <xsl:attribute name="class">
                                    <xsl:variable name="statut">
                                        <xsl:call-template name="statut_langue">
                                            <xsl:with-param name="code" select="$parent/caractéristique[@attribut='langue']/@valeur"/>
                                        </xsl:call-template>
                                    </xsl:variable>
                                    <xsl:value-of select="concat(@id, ' ', $statut)"/>
                                </xsl:attribute>
                                <xsl:text>◊ </xsl:text>
                                <xsl:choose>
                                    <xsl:when test="$parent/caractéristique/contenu">
                                        <xsl:apply-templates select="$parent/caractéristique/contenu"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="$parent/caractéristique[@attribut='information']/@valeur"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:element>
                        </span>
                    </p>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="traductions">
        <xsl:for-each select="TraductionDexemple">
            <xsl:variable name="parent" select="."/>
            <xsl:for-each select="$langues">
                <xsl:if test="$parent/caractéristique[@attribut='langue']/@valeur = @id">
                    <div class="traduction">
                        <xsl:attribute name="id">
                            <xsl:value-of select="./@id"/>
                        </xsl:attribute>
                        <span class="texte_traduction">
                            <xsl:element name="span">
                                <xsl:attribute name="class">
                                    <xsl:variable name="statut">
                                        <xsl:call-template name="statut_langue">
                                            <xsl:with-param name="code" select="$parent/caractéristique[@attribut='langue']/@valeur"/>
                                        </xsl:call-template>
                                    </xsl:variable>
                                    <xsl:value-of select="concat(@id, ' ', $statut)"/>
                                </xsl:attribute>
                                <xsl:text>&#160;&#160;&#160;</xsl:text>
                                <xsl:apply-templates select="$parent/commentaires"/>
                                <xsl:choose>
                                    <xsl:when test="$parent/caractéristique/contenu">
                                        <xsl:apply-templates select="$parent/caractéristique/contenu"/>
                                    </xsl:when>
                                    <xsl:otherwise>
                                        <xsl:value-of select="$parent/caractéristique[@attribut='traduction']/@valeur"/>
                                    </xsl:otherwise>
                                </xsl:choose>
                            </xsl:element>
                        </span>
                    </div>
                </xsl:if>
            </xsl:for-each>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="commentaires">
        <span class="commentaire">
            (<xsl:value-of select="CommentaireDexemple/caractéristique[@attribut='commentaire']/@valeur"/>)
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

    <xsl:template match="Note">
        <span class="note">
            <xsl:value-of select="caractéristique[@attribut='note']/@valeur"/>
        </span>
    </xsl:template>

    <xsl:template match="étymologies">
        <p class="étymologie">
            <xsl:text>[</xsl:text>
            <xsl:for-each select="Étymologie">
                <xsl:if test="caractéristique[@attribut='langue']">
                    <span class="langue">
                        <xsl:value-of select="caractéristique[@attribut='langue']/@valeur"/>
                        <xsl:text> </xsl:text>
                    </span>
                </xsl:if>
                <span class="étymon">
                    <xsl:value-of select="caractéristique[@attribut='étymon']/@valeur"/>
                </span>
                <xsl:if test="gloses_dʼétymologie">
                    <span class="glose">
                    ‘<xsl:value-of select="gloses_dʼétymologie/GloseDÉtymologie/caractéristique[@attribut='glose']/@valeur"/>’
                </span>
                </xsl:if>
                <xsl:if test="not(position() = last())">, </xsl:if>
            </xsl:for-each>
            <xsl:text>]</xsl:text>
        </p>
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
            <xsl:for-each select="titres/Titre">
                <xsl:element name="h4">
                    <xsl:attribute name="class">
                        <xsl:call-template name="statut_langue">
                            <xsl:with-param name="code" select="caractéristique[@attribut='langue']/@valeur"/>
                        </xsl:call-template>
                    </xsl:attribute>
                    <xsl:value-of select="caractéristique[@attribut='titre']/@valeur"/>
                </xsl:element>
            </xsl:for-each>
            <table>
                <xsl:for-each select="contenus/Contenu/caractéristique[@attribut='contenu']/contenu/groupe">
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
            <xsl:for-each select="titres/Titre">
                <xsl:element name="h4">
                    <xsl:attribute name="class">
                        <xsl:call-template name="statut_langue">
                            <xsl:with-param name="code" select="caractéristique[@attribut='langue']/@valeur"/>
                        </xsl:call-template>
                    </xsl:attribute>
                    <xsl:value-of select="caractéristique[@attribut='titre']/@valeur"/>
                </xsl:element>
            </xsl:for-each>
            <xsl:for-each select="contenus/Contenu">
                <xsl:element name="span">
                    <xsl:attribute name="class">
                        <xsl:variable name="statut">
                            <xsl:call-template name="statut_langue">
                                <xsl:with-param name="code" select="caractéristique[@attribut='langue']/@valeur"/>
                            </xsl:call-template>
                        </xsl:variable>
                        <xsl:value-of select="concat(@id, ' ', $statut)"/>
                    </xsl:attribute>
                    <xsl:choose>
                        <xsl:when test="caractéristique[@attribut='contenu']/contenu">
                            <xsl:apply-templates select="node()"/>
                        </xsl:when>
                        <xsl:otherwise>
                            <xsl:value-of select="caractéristique[@attribut='contenu']/@valeur"/>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:element>
                <xsl:text> </xsl:text>
            </xsl:for-each>
        </div>
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
            <xsl:when test="$code = $lang1">
                <xsl:value-of select="'lang1'"/>
            </xsl:when>
            <xsl:when test="$code = $lang2">
                <xsl:value-of select="'lang2'"/>
            </xsl:when>
            <xsl:when test="$code = $langn">
                <xsl:value-of select="'langn'"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
