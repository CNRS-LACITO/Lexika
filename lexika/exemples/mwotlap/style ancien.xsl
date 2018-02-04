<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:exslt="http://exslt.org/common">
    <xsl:output method="html" doctype-public="-//W3C//DTD HTML 4.01 Transitional//EN" encoding="utf-8" indent="yes"/>
    
    <xsl:variable name="minuscules" select="'abcdeēfghijklmm̄n̄noōpqrstuvwxyz'" />
    <xsl:variable name="majuscules" select="'ABCDEĒFGHIJKLMM̄N̄NOŌPQRSTUVWXYZ'" />
    
    <xsl:param name="racine"/>
    <xsl:param name="languen"/>
    <xsl:param name="langue1"/>
    <xsl:param name="langue2"/>
    <xsl:param name="langue3"/>
    <xsl:param name="caractère" select="'*'"/>
    <!--<xsl:variable name="langues" select="RessourceLexicale/InformationsGlobales/Langue[Code='mlv' or Code='fra' or Code='eng' or Code='bis']/Code"/>-->
    <xsl:variable name="langues">
        <langue><xsl:value-of select="$languen"/></langue>
        <langue><xsl:value-of select="$langue1"/></langue>
        <langue><xsl:value-of select="$langue2"/></langue>
        <langue><xsl:value-of select="$langue3"/></langue>
    </xsl:variable>   
             
    <xsl:template match="RessourceLexicale">
        <html>
            <head>
                <link rel="stylesheet" type="text/css" href="style.css"/>
                <title>
                    <xsl:value-of select="InformationsGlobales/Général/Nom"/>
                    –
                    <xsl:value-of select="InformationsGlobales/Général/Auteur"/>
                </title>
            </head>
            <body>
                <div id="dictionnaires">
                    <xsl:call-template name="dictionnaires"/>
                </div>
                <div id="lettrines">
                    <xsl:call-template name="lettrines"/>
                </div>
                <div id="index">
                    <xsl:call-template name="index"/>
                </div>
                <div id="corps">
                    <xsl:call-template name="dictionnaire"/>
                </div>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="InformationsGlobales">
        <xsl:for-each select="exslt:node-set($langues)">     
            <xsl:value-of select="."/>      
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template name="dictionnaires">
        <h1>
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="$racine"/>
                </xsl:attribute>
                <xsl:text>Accueil</xsl:text>
            </xsl:element>
        </h1>
        <h2>Mwotlap</h2>
        <ul>
            <li>
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:call-template name="adresse">
                            <xsl:with-param name="languen" select="'mlv'"/>
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
                    <xsl:attribute name="href">
                        <xsl:call-template name="adresse">
                            <xsl:with-param name="languen" select="'mlv'"/>
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
                    <xsl:attribute name="href">
                        <xsl:call-template name="adresse">
                            <xsl:with-param name="languen" select="'mlv'"/>
                            <xsl:with-param name="langue1" select="'fra'"/>
                            <xsl:with-param name="caractère" select="$caractère"/>
                        </xsl:call-template>
                    </xsl:attribute>
                    <xsl:text>Mtp – Fr</xsl:text>
                </xsl:element>
            </li>
            <li>
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:call-template name="adresse">
                            <xsl:with-param name="languen" select="'mlv'"/>
                            <xsl:with-param name="langue1" select="'eng'"/>
                            <xsl:with-param name="caractère" select="$caractère"/>
                        </xsl:call-template>
                    </xsl:attribute>
                    <xsl:text>Mtp – Eng</xsl:text>
                </xsl:element>
            </li>
        </ul>
        <h2>Teanu</h2>
        <ul>
            <li>Tea – Fr – Eng</li>
            <li>Tea – Eng – Fr</li>
            <li>Tea – Fr</li>
            <li>Tea – Eng</li>
        </ul>
    </xsl:template>

    <xsl:template name="lettrines">
        <ul>
            <li>
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:text>?caractère=*</xsl:text>
                    </xsl:attribute>
                    <xsl:text>Toutes</xsl:text>
                </xsl:element>
            </li>
            <xsl:for-each select="Dictionnaire/EntréeLexicale">
                <xsl:variable name="lettrine" select="substring(translate(translate(Lemme/FormeÉcrite, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)"/>
                <xsl:if test="$lettrine != substring(translate(translate(preceding-sibling::EntréeLexicale[1]/Lemme/FormeÉcrite, '_^~-([)]', ''), $majuscules, $minuscules), 1, 1)">
                    <li>
                        <xsl:element name="a">
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

    <xsl:template name="index">
        <xsl:for-each select="Dictionnaire/EntréeLexicale">
            <xsl:if test="$caractère = '*' or $caractère != '*' and substring(Lemme/FormeÉcrite, 1, 1) = $caractère">
                <xsl:element name="a">
                    <xsl:attribute name="href">
                        <xsl:text>#</xsl:text>
                        <xsl:value-of select="@identifiant"/>
                    </xsl:attribute>
                    <xsl:value-of select="Lemme/FormeÉcrite"/><sub class="homonyme"><xsl:value-of select="NuméroDHomonyme"/></sub><br/>
                </xsl:element>
            </xsl:if>
        </xsl:for-each>
    </xsl:template>

    <xsl:template name="dictionnaire">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="EntréeLexicale">
        <xsl:if test="$caractère = '*' or $caractère != '*' and substring(Lemme/FormeÉcrite, 1, 1) = $caractère">
            <div class="entrée">
                <xsl:attribute name="id">
                    <xsl:value-of select="@identifiant"/>
                </xsl:attribute>
                <p class="en-tête_entrée">
                    <span class="vedette">
                        <xsl:apply-templates select="Lemme/FormeÉcrite"/>
                    </span>
                    <xsl:if test="NuméroDHomonyme">                        
                        <xsl:apply-templates select="NuméroDHomonyme"/>
                    </xsl:if>
                    <xsl:if test="Lemme/FormeDeCitation">
                        <xsl:apply-templates select="Lemme/FormeDeCitation"/>
                    </xsl:if>
                    <!--<xsl:if test="Variante">
                        <xsl:text> (</xsl:text>
                        <span class="variante">
                            <xsl:for-each select="Variante">
                                <xsl:value-of select="Variante"/>
                                <xsl:if test="not(position() = last())">, </xsl:if>
                            </xsl:for-each>
                        </span>
                        <xsl:text>)</xsl:text>
                    </xsl:if>-->
                    <xsl:if test="Lemme/FormePhonétique">
                        <xsl:apply-templates select="Lemme/FormePhonétique"/>
                    </xsl:if>
                    <xsl:if test="ClasseGrammaticale">
                        <xsl:apply-templates select="ClasseGrammaticale"/>
                    </xsl:if>
                </p>
                <xsl:apply-templates select="Groupe|Sens|Sous-entrée"/>
                <xsl:apply-templates select="Encadré"/>
                <xsl:apply-templates select="Tableau"/>
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
                    <xsl:apply-templates select="Lemme/FormeÉcrite"/>
                </span>
                <xsl:if test="NuméroDHomonyme">                        
                    <xsl:apply-templates select="NuméroDHomonyme"/>
                </xsl:if>
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
            <xsl:apply-templates select="Encadré"/>
            <xsl:apply-templates select="Tableau"/>
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
            <xsl:choose>
                <xsl:when test="Définition">
                    <xsl:apply-templates select="Définition"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="Glose"/>
                </xsl:otherwise>
            </xsl:choose>            
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
                <xsl:apply-templates select="FormeÉcrite"/>
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
    
    <xsl:template match="FormeÉcrite">
        <xsl:value-of select="node()"/>
    </xsl:template>
    
    <xsl:template match="NuméroDHomonyme">
        <span class="homonyme">
            <xsl:value-of select="node()"/>
        </span>
    </xsl:template>
    
    <xsl:template match="FormeDeCitation">
        <span class="forme_citation">
            (<xsl:value-of select="node()"/>)
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
            <xsl:when test="$code = $languen">
                <xsl:value-of select="'languen'"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="adresse">
        <xsl:param name="languen"/>
        <xsl:param name="langue1"/>
        <xsl:param name="langue2"/>
        <xsl:param name="langue3"/>
        <xsl:param name="caractère"/>
        <xsl:value-of select="$racine"/>
        <xsl:text>?languen=</xsl:text>
        <xsl:value-of select="$languen"/>
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
