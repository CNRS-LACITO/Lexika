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
        \newenvironment{entrée}[1]{\addcontentsline{toc}{subsection}{#1}\hspace*{-1cm}\textbf{\pfra{\textcolor{<xsl:value-of select="$couleurfra"/>}{#1}}}\markright{#1}}{}
        \newenvironment{sous-entrée}[1]{\addcontentsline{toc}{subsubsection}{#1}\pdéf{■}~\textbf{\pfra{\textcolor{<xsl:value-of select="$couleurfra"/>}{#1}}}}{}
        \newenvironment{exemple}{\pdéf{¶}\nua}{}
        \newcommand{\vedette}[1]{\pnua{\textbf{#1}}}
        \newcommand{\homonyme}[1]{\pdéf{\textcolor{Red}{\textsuperscript{#1}}}}
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
        <xsl:apply-templates select="Général/OrdreLexicographiqueInverse"/>
    </xsl:template>

    <xsl:template match="OrdreLexicographiqueInverse">
        <xsl:apply-templates select="Élément"/>
    </xsl:template>

    <xsl:template match="Élément/Élément">
        <xsl:variable name="expression_rationnelle_graphèmes">
            <xsl:call-template name="créer_expression_rationnelle_graphèmes">
                <xsl:with-param name="graphèmes" select="."/>
            </xsl:call-template>
        </xsl:variable>
        <xsl:variable name="bloc_entrées">
            <xsl:apply-templates select="/RessourceLexicale/Dictionnaire//Sens[not(ancestor::Sous-entréeLexicale)]/Glose[@langue='fra' and regexp:match(translate(., '-', ''), $expression_rationnelle_graphèmes, 'i')]">
                <xsl:sort select="." lang="fr"/>
            </xsl:apply-templates>
        </xsl:variable>
        <xsl:if test="$bloc_entrées != ''">
            <xsl:text>\newpage</xsl:text>
            <xsl:text>&#10;&#13;</xsl:text>
            <xsl:text>\lettrine{</xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>}</xsl:text>
            <xsl:value-of select="$bloc_entrées"/>
        </xsl:if>
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
        <xsl:if test="ancestor::Groupe/ClasseGrammaticale|ancestor::EntréeLexicale/ClasseGrammaticale">
            <xsl:apply-templates select="(ancestor::Groupe/ClasseGrammaticale|ancestor::EntréeLexicale/ClasseGrammaticale)[1]"/>
        </xsl:if>
        <xsl:apply-templates select="ancestor::EntréeLexicale/Lemme/ReprésentationDeForme"/>
        <xsl:if test="ancestor::EntréeLexicale/NuméroDHomonyme">
            <xsl:apply-templates select="ancestor::EntréeLexicale/NuméroDHomonyme"/>
        </xsl:if>
        <xsl:if test="ancestor::Groupe">
            <xsl:apply-templates select="ancestor::Groupe"/>
        </xsl:if>
        <xsl:if test="ancestor::Sens/NuméroDeSens">
            <xsl:apply-templates select="ancestor::Sens/NuméroDeSens"/>
        </xsl:if>
        <xsl:if test="ancestor::EntréeLexicale/Lemme/Région">
            <xsl:apply-templates select="ancestor::EntréeLexicale/Lemme/Région"/>
        </xsl:if>
        <!-- <xsl:if test="ancestor::Sous-entréeLexicale/Lemme/Variante|ancestor::EntréeLexicale/Lemme/Variante">
            <xsl:apply-templates select="ancestor::Sous-entréeLexicale/Lemme/Variante|ancestor::EntréeLexicale/Lemme/Variante"/>
        </xsl:if> -->
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
