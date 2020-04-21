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
        \newenvironment{entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsection}{#1\homonyme{#2}}\hspace*{-1cm}\textbf{\Large\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#1}~\homonyme{#2}}}\markright{#1\homonyme{#2}}}{}
        \newenvironment{sous-entrée}[2]{\hypertarget{#2}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1}\pdéf{■}~\textbf{\Large\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#1}}}}{}
        \newenvironment{glose}{}{}
        \newenvironment{exemple}{\pdéf{¶}\nua}{}
        \newcommand{\nomscientifique}[1]{\pfra{\emph{#1}}}
        \newcommand{\homonyme}[1]{\pdéf{\textcolor{Red}{#1}}}
        \newcommand{\région}[1]{\pfra{\textcolor{Gray}{\pdéf{[}#1\pdéf{]}}}}
        \newcommand{\variante}[1]{\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{\pdéf{(}#1\pdéf{)}}}}
        \newcommand{\groupe}[1]{\pdéf{\cerclé{#1}}}
        \newcommand{\classe}[1]{\pfra{\textcolor{Blue}{\emph{#1}}}}
        \newcommand{\sens}[1]{\pdéf{\cerclé{#1}}}
        \newcommand{\relationsémantique}[2]{\pfra{\emph{#1}~:~}\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#2}}}
        \newcommand{\lien}[2]{\hyperlink{#1}{\pnua{#2}}}
        \setcounter{secnumdepth}{4}
        \titleformat{\subsubsection}{\large\bfseries}{\thesubsubsection}{1em}{}
        \titleformat{\paragraph}{\large\bfseries}{\theparagraph}{1em}{}
        \titlespacing*{\paragraph}
        {\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}
        \titlespacing*{\paragraph}
        {0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}

        \begin{document}
        \begin{multicols}{2}
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:apply-templates select="InformationsGlobales"/>
        \end{multicols}
        \end{document}
    </xsl:template>

    <xsl:template match="InformationsGlobales">
        <xsl:apply-templates select="Général/OrdreThématique/Hiérarchie"/>
    </xsl:template>

    <xsl:template match="Hiérarchie">
        <xsl:apply-templates select="Élément">
            <xsl:with-param name="profondeur" select="1"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="Élément">
        <xsl:param name="profondeur"/>
        <xsl:text>\</xsl:text>
        <xsl:call-template name="section">
            <xsl:with-param name="profondeur" select="$profondeur"/>
        </xsl:call-template>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="Valeur"/>
        <xsl:text>}</xsl:text>
        <xsl:text>&#10;&#13;</xsl:text>
        <xsl:if test="Identifiant">
            <xsl:variable name="domainesémantique" select="Identifiant"/>
            <xsl:apply-templates select="/RessourceLexicale/Dictionnaire/EntréeLexicale[.//DomaineSémantique=$domainesémantique]">
                <xsl:with-param name="domainesémantique" select="$domainesémantique"/>
            </xsl:apply-templates>
        </xsl:if>
        <xsl:apply-templates select="Enfants">
            <xsl:with-param name="profondeur" select="$profondeur + 1"/>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template name="section">
        <xsl:param name="profondeur"/>
        <xsl:choose>
            <xsl:when test="$profondeur=1">
                <xsl:text>section</xsl:text>
            </xsl:when>
            <xsl:when test="$profondeur=2">
                <xsl:text>subsection</xsl:text>
            </xsl:when>
            <xsl:when test="$profondeur=3">
                <xsl:text>subsubsection</xsl:text>
            </xsl:when>
            <xsl:when test="$profondeur=4">
                <xsl:text>paragraph</xsl:text>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="EntréeLexicale">
        <xsl:param name="domainesémantique"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{entrée}</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
        <xsl:text>}{</xsl:text>
        <xsl:if test="NuméroDHomonyme">
            <xsl:value-of select="NuméroDHomonyme"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="@identifiant"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="Lemme/Région">
            <xsl:apply-templates select="Lemme/Région"/>
        </xsl:if>
        <xsl:if test="Lemme/Variante">
            <xsl:text>&#10;</xsl:text>
            <xsl:text>\variante{%</xsl:text>
            <xsl:for-each select="Lemme/Variante">
                <xsl:apply-templates select="."/>
                <xsl:if test="not(position() = last())">, </xsl:if>
            </xsl:for-each>
             <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:if test="Groupe">
            <xsl:apply-templates select="Groupe[.//DomaineSémantique=$domainesémantique]">
                <xsl:with-param name="domainesémantique" select="$domainesémantique"/>
            </xsl:apply-templates>
        </xsl:if>
        <xsl:if test="ClasseGrammaticale">
            <xsl:apply-templates select="ClasseGrammaticale"/>
        </xsl:if>
        <xsl:apply-templates select="Sens[DomaineSémantique=$domainesémantique]"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
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
        <xsl:if test="Lemme/Région">
            <xsl:apply-templates select="Lemme/Région"/>
        </xsl:if>
        <xsl:if test="ClasseGrammaticale">
            <xsl:apply-templates select="ClasseGrammaticale"/>
        </xsl:if>
        <xsl:apply-templates select="Sens"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{sous-entrée}</xsl:text>
    </xsl:template>

    <xsl:template match="Groupe">
        <xsl:param name="domainesémantique"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\groupe{</xsl:text>
        <xsl:value-of select="NomDeGroupe"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="ClasseGrammaticale">
            <xsl:apply-templates select="ClasseGrammaticale"/>
        </xsl:if>
        <xsl:apply-templates select="Sens[DomaineSémantique=$domainesémantique]"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
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
        <xsl:apply-templates select="Région"/>
    </xsl:template>

    <xsl:template match="ClasseGrammaticale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\classe{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Sens">
        <xsl:if test="NuméroDeSens">
            <xsl:apply-templates select="NuméroDeSens"/>
        </xsl:if>
        <xsl:if test="ClasseGrammaticale">
            <xsl:apply-templates select="ClasseGrammaticale"/>
        </xsl:if>
        <xsl:apply-templates select="Glose[@langue = 'fra']"/>
        <xsl:apply-templates select="NomScientifique"/>
        <xsl:apply-templates select="Exemple[1]"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
        <xsl:apply-templates select="RelationSémantique"/>
    </xsl:template>

    <xsl:template match="NuméroDeSens">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\sens{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
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
        <xsl:if test="Région">
            <xsl:apply-templates select="Région"/>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:for-each select="ReprésentationDeTexte">
            <xsl:text>\p</xsl:text>
            <xsl:value-of select="@langue"/>
            <xsl:text>{</xsl:text>
            <xsl:apply-templates select="."/>
            <xsl:text>}</xsl:text>
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

    <xsl:template match="lien">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\lien{</xsl:text>
        <xsl:value-of select="@cible"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <!--<xsl:template match="style">-->
        <!--<xsl:text>\style</xsl:text>-->
        <!--<xsl:value-of select="@type"/>-->
        <!--<xsl:text>{</xsl:text>-->
        <!--<xsl:value-of select="."/>-->
        <!--<xsl:text>}</xsl:text>-->
    <!--</xsl:template>-->

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

</xsl:stylesheet>
