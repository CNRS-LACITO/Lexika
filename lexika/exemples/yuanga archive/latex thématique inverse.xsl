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
        \newenvironment{entrée}[1]{\addcontentsline{toc}{subsection}{#1}\hspace*{-1cm}\textbf{\pfra{\textcolor{<xsl:value-of select="$couleurfra"/>}{#1}}}\markright{#1}}{}
        \newenvironment{sous-entrée}[1]{\addcontentsline{toc}{subsubsection}{#1}\pdéf{■}~\textbf{\pfra{\textcolor{<xsl:value-of select="$couleurfra"/>}{#1}}}}{}
        \newenvironment{exemple}{\pdéf{¶}}{}
        \newcommand{\vedette}[1]{\textbf{#1}}
        \newcommand{\homonyme}[1]{\textcolor{Red}{\textsuperscript{#1}}}
        \newcommand{\région}[1]{\textcolor{Gray}{[#1]}}
        \newcommand{\variante}[1]{\textcolor{<xsl:value-of select="$couleurnua"/>}{(#1)}}
        \newcommand{\groupe}[1]{\cerclé{#1}}
        \newcommand{\classe}[1]{\pfra{\textcolor{Blue}{\emph{#1}}}}
        \newcommand{\sens}[1]{\cerclé{#1}}
        \newcommand{\relationsémantique}[2]{\emph{#1}~:~\pnua{\textcolor{<xsl:value-of select="$couleurnua"/>}{#2}}}
        \newcommand{\lien}[2]{\hyperlink{#1}{\pnua{#2}}}
        \setcounter{secnumdepth}{4}
        \titleformat{\subsubsection}{\large\bfseries}{\thesubsubsection}{1em}{}
        \titleformat{\paragraph}{\large\bfseries}{\theparagraph}{1em}{}
        \titlespacing*{\paragraph}
        {\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}
        \titlespacing*{\paragraph}
        {0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}

        \begin{document}
        �introduction
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
            <xsl:apply-templates select="/RessourceLexicale/Dictionnaire//Sens/Glose[../DomaineSémantique=$domainesémantique and @langue='fra']">
                <xsl:with-param name="domainesémantique" select="$domainesémantique"/>
                <xsl:sort select="." lang="fr"/>
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

    <xsl:template match="Groupe">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\groupe{</xsl:text>
        <xsl:value-of select="NomDeGroupe"/>
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
        <xsl:text>\variante{%</xsl:text>
        <xsl:apply-templates select="ReprésentationDeForme"/>
        <xsl:apply-templates select="Région"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="ClasseGrammaticale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\classe{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="NuméroDeSens">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\sens{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="NuméroDHomonyme">
        <xsl:text>\homonyme{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Glose">
        <xsl:param name="domainesémantique"/>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{entrée}</xsl:text>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
        <xsl:if test="ancestor::Groupe/ClasseGrammaticale|ancestor::Sous-entréeLexicale/ClasseGrammaticale|ancestor::EntréeLexicale/ClasseGrammaticale">
            <xsl:apply-templates select="(ancestor::Groupe/ClasseGrammaticale|ancestor::Sous-entréeLexicale/ClasseGrammaticale|ancestor::EntréeLexicale/ClasseGrammaticale)[1]"/>
        </xsl:if>
        <xsl:apply-templates select="ancestor::Sous-entréeLexicale/Lemme/ReprésentationDeForme|ancestor::EntréeLexicale/Lemme/ReprésentationDeForme"/>
        <xsl:if test="ancestor::Sous-entréeLexicale/NuméroDHomonyme|ancestor::EntréeLexicale/NuméroDHomonyme">
            <xsl:apply-templates select="ancestor::Sous-entréeLexicale/NuméroDHomonyme|ancestor::EntréeLexicale/NuméroDHomonyme"/>
        </xsl:if>
        <xsl:if test="ancestor::Groupe">
            <xsl:apply-templates select="ancestor::Groupe"/>
        </xsl:if>
        <xsl:if test="ancestor::Sens/NuméroDeSens">
            <xsl:apply-templates select="ancestor::Sens/NuméroDeSens"/>
        </xsl:if>
        <xsl:if test="ancestor::Sous-entréeLexicale/Lemme/Région|ancestor::EntréeLexicale/Lemme/Région">
            <xsl:apply-templates select="ancestor::Sous-entréeLexicale/Lemme/Région|ancestor::EntréeLexicale/Lemme/Région"/>
        </xsl:if>
        <xsl:if test="ancestor::Sous-entréeLexicale/Lemme/Variante|ancestor::EntréeLexicale/Lemme/Variante">
            <xsl:apply-templates select="ancestor::Sous-entréeLexicale/Lemme/Variante|ancestor::EntréeLexicale/Lemme/Variante"/>
        </xsl:if>
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\end{entrée}</xsl:text>
        <xsl:text>&#10;&#13;</xsl:text>
    </xsl:template>

    <xsl:template match="ReprésentationDeForme">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\vedette{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>


</xsl:stylesheet>
