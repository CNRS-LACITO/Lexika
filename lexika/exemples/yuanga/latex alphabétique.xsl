<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:exslt="http://exslt.org/common" xmlns:regexp="http://exslt.org/regular-expressions">
    <xsl:output method="text" encoding="utf-8" indent="yes"/>

    <xsl:variable name="couleurfra">OliveGreen</xsl:variable>
    <xsl:variable name="couleurnua">Sepia</xsl:variable>

    <xsl:template match="RessourceLexicale">
        \documentclass[twoside,11pt]{article}
        \title{�titre}
        \author{�auteur}
        \usepackage[paperwidth=185mm,paperheight=260mm,top=16mm,bottom=16mm,left=15mm,right=20mm]{geometry}
        \usepackage{multicol}
        \setlength{\columnseprule}{1pt}
        \setlength{\columnsep}{1.5cm}
        \usepackage{titlesec}
        \usepackage{changepage}
        \usepackage[dvipsnames,table]{xcolor}
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyheadoffset{3.4em}
        \fancyhead[LE,LO]{\rightmark}
        \fancyhead[RE,RO]{\leftmark}
        \usepackage{hyperref}
        \hypersetup{pdftex,bookmarks=true,bookmarksnumbered,bookmarksopenlevel=5,bookmarksdepth=5,xetex,colorlinks=true,linkcolor=blue,citecolor=blue}
        \usepackage[all]{hypcap}
        \usepackage{fontspec}
        \usepackage{natbib}
        \usepackage{booktabs}
        \usepackage{polyglossia}
        \setdefaultlanguage{french}
        \setmainfont{Liberation Serif}
        \newfontfamily{\déf}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newfontfamily{\nua}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Charis SIL}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newcommand{\pdéf}[1]{\déf #1}
        \newcommand{\pfra}[1]{\fra #1}
        \newcommand{\pnua}[1]{\nua #1}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-0.5pt} {\footnotesize{\pdéf{#1}}}}}}
        \newcommand{\lettrine}[1]{\phantomsection\addcontentsline{toc}{section}{#1}{\begin{center}\textbf{\Large\pnua{#1}}\end{center}}}
        \newenvironment{entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsection}{#1\homonyme{#2}}\hspace*{-1cm}\textbf{\Large\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#1}~\homonyme{#2}}}\markright{#1\homonyme{#2}}}{}
        \newenvironment{sous-entrée}[2]{\hypertarget{#2}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1}\pdéf{■}~\textbf{\large\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#1}}}}{}
        \newenvironment{glose}{\pdéf{◊}}{}
        \newenvironment{exemple}{\pdéf{¶}\nua}{}
        \newcommand{\nomscientifique}[1]{\pfra{\emph{#1}}}
        \newcommand{\homonyme}[1]{\pdéf{\textcolor{Red}{#1}}}
        \newcommand{\formephonétique}[1]{\pdéf{/}\pnua{#1}\pdéf{/}}
        \newcommand{\région}[1]{\pfra{\textcolor{Green}{\pdéf{[}#1\pdéf{]}}}}
        \newcommand{\variante}[1]{\pnua{\textcolor{Sepia}{\pdéf{(}#1\pdéf{)}}}}
        \newcommand{\groupe}[1]{\pdéf{\cerclé{#1}}}
        \newcommand{\classe}[1]{\pfra{\textcolor{Blue}{\emph{#1}}}}
        \newcommand{\sens}[1]{\pdéf{\cerclé{#1}}}
        \newcommand{\domainesémantique}[1]{\pdéf{(}\pfra{\textit{#1}}\pdéf{)}}
        \newcommand{\relationsémantique}[2]{\pfra{\emph{#1}~:~}\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#2}}}
        \newcommand{\emprunt}[1]{\pfra{Empr.~:~}#1}
        \newcommand{\étymologie}[1]{\pfra{Étym.~:~}#1}
        \newcommand{\morphologie}[1]{\pfra{Morph.~:~}#1}
        \newcommand{\langue}[1]{\pfra{#1}}
        \newcommand{\étymon}[1]{\pfra{\textbf{#1}}}
        \newcommand{\glosecourte}[1]{\pfra{'#1'}}
        \newcommand{\auteur}[1]{\pfra{d'après \textsc{#1}}}
        \newcommand{\noteglose}[3]{\pfra{\textcolor{Gray}{Note (#2)~:~#1 '#3'}}}
        \newcommand{\note}[2]{\pfra{\textcolor{Gray}{Note (#2)~:~#1}}}
        \newcommand{\notesimple}[1]{\pfra{\textcolor{Gray}{Note~:~#1}}}
        \newcommand{\lien}[2]{\hyperlink{#1}{\pnua{#2}}}
        \setcounter{secnumdepth}{4}
        \titleformat{\paragraph}
        {\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}
        \titlespacing*{\paragraph}
        {0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}

        \begin{document}
        <xsl:text>&#10;</xsl:text>
        \begin{multicols}{2}
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:apply-templates select="InformationsGlobales"/>
        \end{multicols}
        \end{document}
    </xsl:template>

    <xsl:template match="InformationsGlobales">
        <xsl:apply-templates select="Général/OrdreLexicographique"/>
    </xsl:template>

    <xsl:template match="OrdreLexicographique">
        <xsl:apply-templates select="Élément"/>
    </xsl:template>

    <xsl:template match="Élément/Élément">
        <xsl:variable name="expression_rationnelle_graphèmes">
            <xsl:call-template name="créer_expression_rationnelle_graphèmes">
                <xsl:with-param name="graphèmes" select="."/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="bloc_entrées">
            <xsl:apply-templates select="/RessourceLexicale/Dictionnaire/EntréeLexicale[regexp:match(translate(Lemme/ReprésentationDeForme, '-', ''), $expression_rationnelle_graphèmes, 'i')]"/>
        </xsl:variable>
        <xsl:if test="$bloc_entrées != ''">
            <xsl:text>\newpage</xsl:text>
            <xsl:text>&#10;&#13;</xsl:text>
            <xsl:text>\lettrine{</xsl:text>
            <xsl:value-of select="."/>
            <xsl:call-template name="lettrine_variante">
                <xsl:with-param name="lettrine" select="."/>
            </xsl:call-template>
            <xsl:text>}</xsl:text>
            <xsl:value-of select="$bloc_entrées"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="EntréeLexicale">
        <xsl:text>\begin{entrée}</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="NuméroDHomonyme"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="@identifiant"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#13;</xsl:text>
        <xsl:apply-templates select="Lemme/FormePhonétique"/>
        <xsl:apply-templates select="Lemme/Région"/>
        <xsl:if test="Lemme/Variante">
            <xsl:text>&#10;</xsl:text>
            <xsl:text>\variante{%</xsl:text>
            <xsl:for-each select="Lemme/Variante">
                <xsl:apply-templates select="."/>
                <xsl:if test="not(position() = last())">, </xsl:if>
            </xsl:for-each>
             <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Groupe"/>
        <xsl:apply-templates select="ClasseGrammaticale"/>
        <xsl:apply-templates select="Sens"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
        <xsl:apply-templates select="Morphologie"/>
        <xsl:apply-templates select="Étymologie"/>
        <xsl:apply-templates select="Emprunt"/>
        <xsl:apply-templates select="Note"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{entrée}</xsl:text>
        <xsl:text>&#10;&#13;</xsl:text>
    </xsl:template>

    <xsl:template match="Sous-entréeLexicale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{sous-entrée}</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="@identifiant"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#13;</xsl:text>
        <xsl:apply-templates select="Lemme/FormePhonétique"/>
        <xsl:apply-templates select="Lemme/Région"/>
        <xsl:apply-templates select="ClasseGrammaticale"/>
        <xsl:apply-templates select="Sens"/>
        <xsl:apply-templates select="Note"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{sous-entrée}</xsl:text>
    </xsl:template>

    <xsl:template match="Groupe">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\groupe{</xsl:text>
        <xsl:value-of select="NomDeGroupe"/>
        <xsl:text>}</xsl:text>
        <xsl:apply-templates select="ClasseGrammaticale"/>
        <xsl:apply-templates select="Sens"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
    </xsl:template>

    <xsl:template match="FormePhonétique">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\formephonétique{</xsl:text>
        <xsl:value-of select="translate(., ':', 'ː')"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Région">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\région{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Variante">
        <xsl:text>&#10;</xsl:text>
        <xsl:apply-templates select="ReprésentationDeForme"/>
        <xsl:text>&#13;</xsl:text>
        <xsl:apply-templates select="FormePhonétique"/>
        <xsl:apply-templates select="Région"/>
    </xsl:template>

    <xsl:template match="ClasseGrammaticale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\classe{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Sens">
        <xsl:apply-templates select="NuméroDeSens"/>
        <xsl:apply-templates select="DomaineSémantique"/>
        <xsl:apply-templates select="ClasseGrammaticale"/>
        <xsl:apply-templates select="Glose[@langue = 'fra']"/>
        <xsl:apply-templates select="Note"/>
        <xsl:apply-templates select="NomScientifique"/>
        <xsl:apply-templates select="Exemple"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
        <xsl:apply-templates select="RelationSémantique"/>
    </xsl:template>

    <xsl:template match="NuméroDeSens">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\sens{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="DomaineSémantique">
        <xsl:text>&#10;</xsl:text>
        <xsl:choose>
            <xsl:when test="preceding-sibling::DomaineSémantique">
                <xsl:text>, </xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>\domainesémantique{</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:variable name="domainesémantique" select="."/>
        <xsl:value-of select="/RessourceLexicale/InformationsGlobales/Général/OrdreThématique/Hiérarchie//Élément[Identifiant=$domainesémantique]/Valeur"/>
        <xsl:choose>
            <xsl:when test="not(following-sibling::DomaineSémantique)">
                <xsl:text>}</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>%</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        
    </xsl:template>

    <xsl:template match="Glose">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{glose}</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\p</xsl:text>
        <xsl:value-of select="@langue"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{glose}</xsl:text>
    </xsl:template>

    <xsl:template match="Sens/Note">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\note{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}{glose}</xsl:text>
    </xsl:template>

    <xsl:template match="NomScientifique">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\nomscientifique{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Exemple">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{exemple}</xsl:text>
        <xsl:apply-templates select="Région"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:for-each select="ReprésentationDeTexte">
            <xsl:choose>
                <xsl:when test="position()=1">
                    <xsl:text>\textbf{\p</xsl:text>
                    <xsl:value-of select="@langue"/>
                    <xsl:text>{</xsl:text>
                    <xsl:apply-templates select="."/>
                    <xsl:text>}}</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>\p</xsl:text>
                    <xsl:value-of select="@langue"/>
                    <xsl:text>{</xsl:text>
                    <xsl:apply-templates select="."/>
                    <xsl:text>}</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:if test="not(position() = last())">
                <xsl:text>&#10;</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{exemple}</xsl:text>
    </xsl:template>

    <xsl:template match="ReprésentationDeForme">
        <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="RelationSémantique">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\relationsémantique{</xsl:text>
        <xsl:call-template name="traduction">
            <xsl:with-param name="expression" select="Type"/>
        </xsl:call-template>
        <xsl:text>}{\lien{</xsl:text>
        <xsl:value-of select="Cible/@cible"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="Cible"/>
        <xsl:text>}}</xsl:text>
        <xsl:apply-templates select="Glose[@langue = 'fra']"/>
    </xsl:template>

    <xsl:template match="Emprunt">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\emprunt{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymologie">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\étymologie{</xsl:text>
        <xsl:apply-templates select="Étymon"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymon">
        <xsl:if test="preceding-sibling::Étymon">
            <xsl:text>, </xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Langue"/>
        <xsl:apply-templates select="ReprésentationDeForme"/>
        <xsl:apply-templates select="Glose"/>
        <xsl:apply-templates select="Auteur"/>
    </xsl:template>

    <xsl:template match="Étymon/Glose|RelationSémantique/Glose">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\glosecourte{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymon/ReprésentationDeForme">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\étymon{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymon/Langue">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\langue{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Auteur">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\auteur{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Morphologie">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\morphologie{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Note">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\note{</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="Type"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Note[Type='général']">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\notesimple{</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Note[Glose]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\newline</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\noteglose{</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="Type"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="Glose"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="lien">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\lien{</xsl:text>
        <xsl:value-of select="@cible"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template name="lettrine_variante">
        <xsl:param name="lettrine"/>
        <xsl:if test="$lettrine = 'dr' or $lettrine = 'tr' or $lettrine = 'thr'">
            <xsl:text>&#10;</xsl:text>
            <xsl:text>(variante de GOs)</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template name="traduction">
        <xsl:param name="expression"/>
        <xsl:choose>
            <xsl:when test="$expression='renvoi'">
                <xsl:text>Cf.</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='synonyme'">
                <xsl:text>Syn.</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='antonyme'">
                <xsl:text>Ant.</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$expression"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template name="créer_expression_rationnelle_graphèmes">  <!-- forme : ^(x|y|z) -->
        <xsl:param name="graphèmes"/>
        <xsl:text>^</xsl:text>
        <xsl:call-template name="exclure_graphèmes_chevauchants">
            <xsl:with-param name="graphèmes" select="$graphèmes"/>
        </xsl:call-template>
        <xsl:text>(</xsl:text>
        <xsl:choose>
            <xsl:when test="Élément">
                <xsl:for-each select="$graphèmes/Élément">
                    <xsl:value-of select="."/>
                    <xsl:if test="not(position() = last())">
                        <xsl:text>|</xsl:text>
                    </xsl:if>
                </xsl:for-each>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$graphèmes"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>)</xsl:text>
    </xsl:template>

    <xsl:template name="exclure_graphèmes_chevauchants">  <!-- forme : ^(?!xz|yz)(x|y) -->
        <xsl:param name="graphèmes"/>
        <xsl:variable name="graphèmes_chevauchants">
            <xsl:call-template name="trouver_graphèmes_chevauchants">
                <xsl:with-param name="graphèmes" select="$graphèmes"/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:if test="$graphèmes_chevauchants != ''">
            <xsl:text>(?!</xsl:text>
            <xsl:for-each select="exslt:node-set($graphèmes_chevauchants)//Graphème">
                <xsl:value-of select="."/>
                <xsl:if test="not(position() = last())">
                    <xsl:text>|</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>)</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template name="trouver_graphèmes_chevauchants">  <!-- exemple : x et xz -->
        <xsl:param name="graphèmes"/>
        <xsl:element name="Graphèmes">
            <xsl:for-each select="/RessourceLexicale/InformationsGlobales/Général/OrdreLexicographique//Élément[not(Élément)]">  <!-- chaque graphème utilisé dans l'ordre lexicographique -->
                <xsl:variable name="graphème_comparé" select="."/>
                <xsl:for-each select="$graphèmes/Élément|$graphèmes[not(Élément)]">  <!-- chaque graphème formant la lettrine (formant un bloc d'entrées) -->
                    <xsl:if test="starts-with($graphème_comparé, .) and $graphème_comparé != .">
                        <Graphème>
                            <xsl:value-of select="$graphème_comparé"/>
                        </Graphème>
                    </xsl:if>
                </xsl:for-each>
            </xsl:for-each>
        </xsl:element>
    </xsl:template>


</xsl:stylesheet>
