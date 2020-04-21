<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" encoding="utf-8" indent="yes"/>

    <xsl:template match="Données">
        <html>
            <head>
                <style type="text/css">
                    .entrée, .groupe, .sens, .définition, .exemple {

                    }

                    .sous-entrée {
                        margin-left: 20px;
                    }

                    .entrée .vedette {
                        font-size: 150%;
                        color: blue;
                        font-weight: bold;
                    }

                    .sous-entrée .vedette {
                        font-size: 110%;
                        color: darkblue;
                    }

                    .homonyme {
                        color: red;
                        font-size: 75%;
                        position:relative;
                        bottom: -0.3em;
                    }

                    .classe_grammaticale {
                        color: green;
                    }

                    .phonétique {

                    }

                    .nom_groupe {
                        color: purple;
                    }

                    .numéro_sens {
                        color: orange;
                    }

                    .texte_définition {
                        margin-left: 20px;
                    }

                    .texte_exemple {
                        margin-left: 30px;
                        font-style: italic;
                    }

                    .relation_sémantique {
                        margin-left: 20px;
                        font-style: italic;
                    }

                    .note {
                        color: blue;
                        font-size: 75%;
                        margin-left: 40px;
                        font-style: italic;
                    }

                    .langue {
                        color: grey;
                        font-variant: small-caps;
                    }

                    .type {
                        color: indigo;
                    }

                    a {
                        color: darkgreen;
                        font-weight: bold;
                    }

                    .encadré {
                        display: inline-block;
                        border-style: solid;
                        margin: 10px;
                        padding: 10px;
                    }

                    .encadré h4, .encadré h5 {
                        text-align: center;
                    }

                    .tableau {
                        border-spacing: 25px 0;
                    }

                    tr:nth-child(even){
                        background-color: #f2f2f2;
                    }

                    .lien_brisé {
                        color: red;
                    }
                </style>
                <title>
                    <xsl:value-of select="Dictionnaire/caractéristique[@attribut='nom']/@valeur"/>
                    -
                    <xsl:value-of select="Dictionnaire/caractéristique[@attribut='auteur']/@valeur"/>
                </title>
            </head>
            <body>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="Entrée">
        <div class="entrée">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
                <p>
                    <span class="vedette">
                        <xsl:value-of select="caractéristique[@attribut='vedette']/@valeur"/>
                    </span>
                    <xsl:if test="caractéristique[@attribut='homonyme']">
                        <span class="homonyme">
                            <xsl:value-of select="caractéristique[@attribut='homonyme']/@valeur"/>
                        </span>
                    </xsl:if>
                    <xsl:if test="caractéristique[@attribut='forme_citation']">
                        <span class="forme_citation">
                             (<xsl:value-of select="caractéristique[@attribut='forme_citation']/@valeur"/>)
                        </span>
                    </xsl:if>
                    <xsl:if test="caractéristique[@attribut='phonétique']">
                        <span class="phonétique">
                            <xsl:text> </xsl:text>
                            [<xsl:value-of select="caractéristique[@attribut='phonétique']/@valeur"/>]
                        </span>
                    </xsl:if>
                    <span class="classe_grammaticale">
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="caractéristique[@attribut='classe_grammaticale']/@valeur"/>
                    </span>
                </p>
                <xsl:apply-templates select="groupes"/>
                <xsl:apply-templates select="sous-entrées"/>
                <xsl:apply-templates select="définitions"/>
                <xsl:apply-templates select="exemples"/>
                <xsl:apply-templates select="relations_sémantiques"/>
                <xsl:apply-templates select="sens"/>
                <xsl:apply-templates select="tableaux"/>
        </div>
    </xsl:template>

    <xsl:template match="Groupe">
        <div class="groupe">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="nom_groupe">
                <xsl:value-of select="caractéristique[@attribut='nom']/@valeur"/>
            </span>
            <xsl:apply-templates select="groupes"/>
        </div>
    </xsl:template>

    <xsl:template match="Sens">
        <div class="sens">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="numéro_sens">
                <xsl:value-of select="caractéristique[@attribut='acception']/@valeur"/>
            </span>
            <xsl:apply-templates select="définitions"/>
            <xsl:apply-templates select="relations_sémantiques"/>
            <xsl:apply-templates select="sous-entrées"/>
        </div>
    </xsl:template>

    <xsl:template match="Sous-entrée">
        <div class="sous-entrée">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
                <p>
                    <span class="vedette">
                        <xsl:value-of select="caractéristique[@attribut='vedette']/@valeur"/>
                    </span>
                    <xsl:if test="caractéristique[@attribut='homonyme']">
                        <span class="homonyme">
                            <xsl:value-of select="caractéristique[@attribut='homonyme']/@valeur"/>
                        </span>
                    </xsl:if>
                    <xsl:if test="caractéristique[@attribut='phonétique']">
                        <span class="phonétique">
                            <xsl:text> </xsl:text>
                            [<xsl:value-of select="caractéristique[@attribut='phonétique']/@valeur"/>]
                        </span>
                    </xsl:if>
                    <span class="classe_grammaticale">
                        <xsl:text> </xsl:text>
                        <xsl:value-of select="caractéristique[@attribut='classe_grammaticale']/@valeur"/>
                    </span>
                </p>
                <xsl:apply-templates select="définitions"/>
                <xsl:apply-templates select="exemples"/>
                <xsl:apply-templates select="relations_sémantiques"/>
                <xsl:apply-templates select="tableaux"/>
        </div>
    </xsl:template>

    <xsl:template match="Définition">
        <div class="définition">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="texte_définition">
                <span class="langue">
                    <xsl:value-of select="caractéristique[@attribut='langue']/@valeur"/>
                    <xsl:text> : </xsl:text>
                </span>
                <xsl:choose>
                    <xsl:when test="caractéristique/contenu">
                        <xsl:apply-templates select="caractéristique"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="caractéristique[@attribut='définition']/@valeur"/>
                    </xsl:otherwise>
                </xsl:choose>
            </span>
        </div>
    </xsl:template>

    <xsl:template match="Exemple">
        <div class="exemple">
            <xsl:attribute name="id">
                <xsl:value-of select="./@id"/>
            </xsl:attribute>
            <span class="texte_exemple">
                <span class="langue">
                    <xsl:value-of select="caractéristique[@attribut='langue']/@valeur"/>
                    <xsl:text> : </xsl:text>
                </span>
            <xsl:value-of select="caractéristique[@attribut='exemple']/@valeur"/>
            </span>
        </div>
        <xsl:apply-templates select="notes"/>
    </xsl:template>

    <xsl:template match="RelationSémantique">
        <p>
            <span class="relation_sémantique">
                <span class="type">
                    <xsl:value-of select="caractéristique[@attribut='type']/@valeur"/>
                    <xsl:text> : </xsl:text>
                </span>
                <xsl:apply-templates select="node()"/>
            </span>
        </p>
    </xsl:template>

    <xsl:template match="Note">
        <p>
            <span class="note">
                <span class="langue">
                    <xsl:value-of select="caractéristique[@attribut='langue']/@valeur"/>
                    <xsl:text> : </xsl:text>
                </span>
            <xsl:value-of select="caractéristique[@attribut='commentaire']/@valeur"/>
            </span>
        </p>
    </xsl:template>

    <xsl:template match="Tableau">
        <div class="encadré">
            <h4 class="tableau">
                <xsl:value-of select="titres/Titre/caractéristique[@attribut='langue' and @valeur='fra']/ancestor::Titre/caractéristique[@attribut='titre']/@valeur"/>
            </h4>
            <h5>
                [<xsl:value-of select="titres/Titre/caractéristique[@attribut='langue' and @valeur='mlv']/ancestor::Titre/caractéristique[@attribut='titre']/@valeur"/>]
            </h5>
            <table class="tableau">
                <xsl:for-each select="caractéristique[@attribut='contenu']/contenu/groupe">
                    <tr>
                        <xsl:for-each select="élément">
                            <td>
                                <xsl:value-of select="."/>
                            </td>
                        </xsl:for-each>
                    </tr>
                </xsl:for-each>
            </table>
        </div>
    </xsl:template>

    <xsl:template match="lien">
        <xsl:element name="a">
            <xsl:attribute name="href">
                <xsl:text>résultat.xml#</xsl:text>
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
    <!--<xsl:template match="caractéristique[@attribut='cible']">-->
        <!--++<xsl:element name="a">-->
            <!--<xsl:attribute name="href">-->
                <!--<xsl:text>résultat.xml#</xsl:text>-->
                <!--<xsl:value-of select="@valeur"/>-->
            <!--</xsl:attribute>-->
            <!--<xsl:value-of select="@valeur"/>-->
        <!--</xsl:element>++-->
    <!--</xsl:template>-->
</xsl:stylesheet>