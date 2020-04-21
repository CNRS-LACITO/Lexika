<?xml version="1.0" encoding="utf-8" ?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0" xmlns:exslt="http://exslt.org/common" xmlns:regexp="http://exslt.org/regular-expressions">
    <xsl:output method="text" encoding="utf-8" indent="yes"/>

    <xsl:variable name="languev">jya</xsl:variable>
    <xsl:variable name="langue1">cmn</xsl:variable>
    <xsl:variable name="langue2">fra</xsl:variable>

    <xsl:variable name="nombres" select="'0123456789'"/>
    <xsl:variable name="indices" select="'₀₁₂₃₄₅₆₇₈₉'"/>

    <xsl:variable name="dossier_audio" select="'/run/media/benjamin/848A-5DEB/Lacito/AudioJaphug'"/>
    <xsl:variable name="format_audio" select="'mp3'"/>
    <xsl:variable name="inclure_audio" select="false()"/>

    <xsl:variable name="couleurfra">OliveGreen</xsl:variable>
    <xsl:variable name="couleureng">Sepia</xsl:variable>
    <xsl:variable name="couleurcmn">black</xsl:variable>
    <xsl:variable name="couleurjya">Blue</xsl:variable>
    <xsl:variable name="couleurbod">black</xsl:variable>
    <!--<xsl:variable name="fra">black</xsl:variable>-->
    <!--<xsl:variable name="eng">black</xsl:variable>-->
    <!--<xsl:variable name="cmn">black</xsl:variable>-->
    <!--<xsl:variable name="jya">black</xsl:variable>-->
    <!--<xsl:variable name="bod">black</xsl:variable>-->

    <xsl:variable name="langues">
        <langue><xsl:value-of select="$languev"/></langue>
        <langue><xsl:value-of select="$langue1"/></langue>
        <langue><xsl:value-of select="$langue2"/></langue>
    </xsl:variable>

    <xsl:template match="RessourceLexicale">
        \documentclass[twoside,11pt]{article}
        \title{�titre}
        \author{�auteur}
        \usepackage[paperwidth=185mm,paperheight=260mm,top=16mm,bottom=16mm,left=15mm,right=20mm]{geometry}
        \usepackage{multicol}
        \setlength{\columnseprule}{1pt}
        \setlength{\columnsep}{1.5cm}
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
        \usepackage{media9}
        \setdefaultlanguage{french}
        \setotherlanguages{french,english}
        \setmainfont{Charis SIL}
        \usepackage{media9}
        \usepackage{graphicx}
        \usepackage{totcount}
        \newcounter{compteur}
        \setcounter{compteur}{0}
        \regtotcounter{compteur}
        \newfontfamily{\prin}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newfontfamily{\jya}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Charis SIL}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\cmn}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{AR PL UMing CN}
        \newfontfamily{\eng}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newcommand{\pprin}[1]{\begin{<xsl:value-of select="$langue1"/>}{\prin #1}\end{<xsl:value-of select="$langue1"/>}}
        \newcommand{\pjya}[1]{{\jya\textcolor{<xsl:value-of select="$couleurjya"/>}{#1}}}
        \newcommand{\pfra}[1]{\begin{french}{\fra\textcolor{<xsl:value-of select="$couleurfra"/>}{#1}}\end{french}}
        \newcommand{\pcmn}[1]{{\cmn\textcolor{<xsl:value-of select="$couleurcmn"/>}{#1}}}
        \newcommand{\peng}[1]{\begin{english}{\eng\textcolor{<xsl:value-of select="$couleureng"/>}{#1}}\end{english}}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-0.5pt} {\footnotesize{\pjya{#1}}}}}}
        \newcommand{\caractère}[1]{\phantomsection\addcontentsline{toc}{section}{#1}{\begin{center}\textbf{\Large\pjya{#1}}\end{center}}}
        \newenvironment{entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsection}{#1\homonyme{#2}}\hspace*{-0.5cm}\textbf{\Large\pjya{#1 \homonyme{#2}}}\markright{#1 \homonyme{#2}}}{\stepcounter{compteur}}
        \newenvironment{sous-entrée}[2]{\hypertarget{#2}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1}\hspace*{-0.3cm}\pprin{■} \textbf{\Large\pjya{#1}}}{}
        <!-- \newenvironment{sous-entrée}[3]{\par\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1 \homonyme{#2}}\begin{adjustwidth}{0.3cm}{}\pprin{■} \textbf{\Large\pjya{#1\homonyme{#2}}}}{\end{adjustwidth}} -->
        \newcommand{\homonyme}[1]{#1}
        \newcommand{\variante}[1]{\small \pjya{#1}}
        \newcommand{\classe}[1]{\textcolor{PineGreen}{#1} }
        \newcommand{\paradigme}[2]{#1 : \pjya{#2} }
        \newcommand{\relationsémantique}[2]{\pcmn{【#1】}\pjya{#2} }
        \newcommand{\forme}[2]{#1 : \pjya{#2} }
        \newcommand{\sens}[1]{ \cerclé{#1} }
        \newenvironment{définition}{}{\hspace{5pt}}
        \newenvironment{déclaration}{}{}
        \newenvironment{exemple}{\pprin{¶} }{\hspace{5pt}}
        \newenvironment{informationencyclopédique}{}{\hspace{5pt}}
        \newcommand{\étiquette}[1]{\pcmn{~【同义词】~\pjya{#1}} }
        \newcommand{\synonyme}[1]{\pcmn{~【同义词】~\pjya{#1}} }
        \newcommand{\antonyme}[1]{\pcmn{~【反义词】~\pjya{#1}} }
        \newcommand{\confer}[1]{\pcmn{~【参考】~\pjya{#1}} }
        \newcommand{\emprunt}[1]{\pcmn{~【借词】~#1} }
        \newcommand{\étymologie}[1]{\pcmn{~【词源】~\pjya{#1}} }
        \newcommand{\utilisation}[1]{\pcmn{~【用法】#1} }
        \newcommand{\grammaire}[1]{\textsc{#1} }
        \newcommand{\lien}[2]{\hyperlink{#1}{\pjya{#2}}}
        \newcommand{\stylefv}[1]{\pjya{#1}}
        \newcommand{\stylefn}[1]{\pcmn{#1}}
        \newcommand{\stylefi}[1]{\textit{#1}}
        \newcommand{\stylefg}[1]{\textsc{#1}}
        \newcommand{\caps}[1]{\pprin{\textsc{#1}}}
        \newcommand{\ital}[1]{\pprin{\textit{#1}}}
        \newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}
        \newcommand{\écouterélevée}[1]{\includemedia[activate=onclick,addresource=#1.<xsl:value-of select="$format_audio"/>,flashvars={source=#1.<xsl:value-of select="$format_audio"/>&amp;autoPlay=true&amp;autoRewind=true&amp;loop=false&amp;hideBar=true&amp;volume=1.0&amp;balance=0.0}]{ \includegraphics[height=8pt]{../images/volume.png}}{APlayer.swf}}
        \newcommand{\écouterfaible}[1]{\includemedia[activate=onclick,addresource=8_#1.<xsl:value-of select="$format_audio"/>,flashvars={source=#1.<xsl:value-of select="$format_audio"/>&amp;autoPlay=true&amp;autoRewind=true&amp;loop=false&amp;hideBar=true&amp;volume=1.0&amp;balance=0.0}]{ \includegraphics[height=8pt]{../images/volume.png}}{APlayer.swf}}
        \addmediapath{<xsl:value-of select="$dossier_audio"/>}
        \XeTeXlinebreaklocale "zh"
        \XeTeXlinebreakskip = 0pt plus 1pt
        \ExplSyntaxOn
        % Code spécial pour la gestion générique des césures applicable aux formes de surface
        \RenewDocumentCommand{\formedesurface}{m}
        {
            % nouvelle variable « expression »
            \tl_set:Nn \expression { #1 }
            % remplace ˩˧˥ par ˩˧˥\-
            \regex_replace_all:nnN { (\B[˩˧˥]) } { \1\c{-} } \expression
            % renvoie la séquence totale
            {\tl_use: {\hspace{0.5cm}/\pjya{\expression}/\hspace{0.5cm}}}
        }
        \ExplSyntaxOff
        <xsl:text>&#xd;</xsl:text>
        \begin{document}
        �introduction
        \pagenumbering{arabic}
        \setcounter{page}{1}
        \setlength{\parindent}{0pt}
        \begin{multicols}{2}
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:apply-templates/>
        \end{multicols}
        \end{document}
    </xsl:template>

    <xsl:template match="InformationsGlobales">
    </xsl:template>

    <xsl:template name="lettrine">
    </xsl:template>

    <xsl:template name="index">
    </xsl:template>

    <xsl:template match="Dictionnaire">
        <xsl:for-each select="EntréeLexicale">
            <xsl:variable name="caractère" select="substring(translate(Lemme/ReprésentationDeForme, '_^-‐‑*=', ''), 1, 1)"/>
            <xsl:if test="$caractère != substring(translate(preceding-sibling::EntréeLexicale[1]/Lemme/ReprésentationDeForme, '_^-‐‑*=', ''), 1, 1)">
                <xsl:text>\newpage</xsl:text>
                <xsl:text>\caractère{</xsl:text>
                <xsl:value-of select="$caractère"/>
                <xsl:text>}</xsl:text>
                <xsl:text>&#xa;&#xd;</xsl:text>
            </xsl:if>
            <xsl:apply-templates select="."/>
        </xsl:for-each>

    </xsl:template>

    <xsl:template match="EntréeLexicale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{entrée}</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
        <xsl:if test="Lemme/Variante">
            <xsl:text>/</xsl:text>
            <xsl:apply-templates select="Lemme/Variante"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:if test="NuméroDHomonyme">
            <xsl:apply-templates select="NuméroDHomonyme"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="translate(@identifiant, '_', '')"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="$inclure_audio">
            <xsl:apply-templates select="Audio"/>
        </xsl:if>
        <xsl:if test="ClasseGrammaticale">
            <xsl:text>&#160;</xsl:text>
            <xsl:apply-templates select="ClasseGrammaticale"/>
            <xsl:text>&#160;</xsl:text>
        </xsl:if>
        <xsl:if test="Note[Type='grammaire']">
            <xsl:text>&#160;</xsl:text>
            <xsl:apply-templates select="Note[Type='grammaire']"/>
            <xsl:text>&#160;</xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Sens"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
        <xsl:apply-templates select="Étymologie"/>
        <xsl:text>\end{entrée}</xsl:text>
        <xsl:text>&#xa;&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="Sous-entréeLexicale">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{sous-entrée}</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="Lemme/ReprésentationDeForme"/>
        <xsl:if test="Lemme/Variante">
            <xsl:text>/</xsl:text>
            <xsl:apply-templates select="Lemme/Variante"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="translate(@identifiant, '_', '')"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="$inclure_audio">
            <xsl:apply-templates select="Audio"/>
        </xsl:if>
        <xsl:if test="ClasseGrammaticale">
            <xsl:text>&#160;</xsl:text>
            <xsl:apply-templates select="ClasseGrammaticale"/>
            <xsl:text>&#160;</xsl:text>
        </xsl:if>
        <xsl:if test="Note[Type='grammaire']">
            <xsl:text>&#160;</xsl:text>
            <xsl:apply-templates select="Note[Type='grammaire']"/>
            <xsl:text>&#160;</xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Sens"/>
        <xsl:apply-templates select="Étymologie"/>
        <xsl:text>\end{sous-entrée}</xsl:text>
        <xsl:text>&#xa;&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="NuméroDHomonyme">
        <xsl:value-of select="translate(., $nombres, $indices)"/>
    </xsl:template>

    <xsl:template match="Variante">
        <xsl:text>\variante{</xsl:text>
        <xsl:value-of select="ReprésentationDeForme"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="ClasseGrammaticale">
        <xsl:text>&#10;\classe{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Note[Type='grammaire']">
        <xsl:text>&#10;\grammaire{</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Sens">
        <xsl:if test="NuméroDeSens">
            <xsl:apply-templates select="NuméroDeSens"/>
        </xsl:if>
        <xsl:apply-templates select="Paradigme"/>
        <xsl:apply-templates select="Définition"/>
        <xsl:apply-templates select="Exemple"/>
        <xsl:apply-templates select="RelationSémantique"/>
        <xsl:apply-templates select="FormeDeMot"/>
        <xsl:apply-templates select="Sous-entréeLexicale"/>
    </xsl:template>

    <xsl:template match="NuméroDeSens">
        <xsl:text>\sens{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Définition">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{définition}</xsl:text>
        <xsl:text>\p</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte/@langue"/>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="ReprésentationDeTexte"/>
        <xsl:text>}</xsl:text>
        <xsl:apply-templates select="Déclaration"/>
        <xsl:text>\end{définition}</xsl:text>
    </xsl:template>

    <xsl:template match="Exemple">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{exemple}</xsl:text>
        <xsl:for-each select="ReprésentationDeTexte">
            <xsl:text>\p</xsl:text>
            <xsl:value-of select="@langue"/>
            <xsl:text>{</xsl:text>
            <xsl:apply-templates select="."/>
            <xsl:text>}</xsl:text>
            <xsl:if test="not(position() = last())">
                <xsl:text>\hspace{5pt}</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>\end{exemple}</xsl:text>
    </xsl:template>

    <xsl:template match="InformationEncyclopédique">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{informationencyclopédique}</xsl:text>
        <xsl:for-each select="ReprésentationDeTexte">
            <xsl:text>\p</xsl:text>
            <xsl:value-of select="@langue"/>
            <xsl:text>{</xsl:text>
            <xsl:apply-templates select="."/>
            <xsl:text>}</xsl:text>
            <xsl:if test="not(position() = last())">
                <xsl:text>\hspace{5pt}</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>\end{information_encyclopédique}</xsl:text>
    </xsl:template>

    <xsl:template match="Paradigme">
        <xsl:text>\paradigme{</xsl:text>
        <xsl:value-of select="CatégorieParadigmatique"/>
        <xsl:text>}{</xsl:text>
            <xsl:value-of select="ReprésentationDeForme"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="RelationSémantique">
        <xsl:text>\relationsémantique{</xsl:text>
        <xsl:call-template name="traduction">
            <xsl:with-param name="expression" select="Type"/>
        </xsl:call-template>
        <xsl:text>}{\lien{</xsl:text>
        <xsl:value-of select="translate(Cible/@cible, '_', '')"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="translate(Cible, $nombres, $indices)"/>
        <xsl:text>}}</xsl:text>
    </xsl:template>

    <xsl:template match="FormeDeMot">
        <xsl:text>\forme{</xsl:text>
        <xsl:choose>
            <xsl:when test="Personne='première'">
                <xsl:text>1</xsl:text>
            </xsl:when>
            <xsl:when test="Personne='deuxième'">
                <xsl:text>2</xsl:text>
            </xsl:when>
            <xsl:when test="Personne='troisième'">
                <xsl:text>3</xsl:text>
            </xsl:when>
        </xsl:choose>
        <xsl:choose>
            <xsl:when test="Nombre='singulier'">
                <xsl:text>s</xsl:text>
            </xsl:when>
            <xsl:when test="Nombre='pluriel'">
                <xsl:text>p</xsl:text>
            </xsl:when>
        </xsl:choose>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="ReprésentationDeForme"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymologie">
        <xsl:text>\étymologie{</xsl:text>
            <xsl:apply-templates select="Étymon"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Étymon">
        <xsl:apply-templates select="ReprésentationDeForme"/>
    </xsl:template>

    <xsl:template match="ReprésentationDeForme">
        <xsl:value-of select="translate(., '_', '')"/>
    </xsl:template>

    <xsl:template match="Audio">
        <xsl:choose>
            <xsl:when test="Qualité='élevée'">
                <xsl:text>\écouterélevée{</xsl:text>
                <xsl:value-of select="CheminDAccès"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>\écouterfaible{</xsl:text>
                <xsl:value-of select="CheminDAccès"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="lien">
        <xsl:text>\lien{</xsl:text>
        <xsl:value-of select="@cible|@target"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="translate(., $nombres, $indices)"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="style">
        <xsl:text>\style</xsl:text>
        <xsl:value-of select="@type"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template name="traduction">
        <xsl:param name="expression"/>
        <xsl:choose>
            <xsl:when test="$expression='renvoi'">
                <xsl:text>参考</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='synonyme'">
                <xsl:text>同义词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='antonyme'">
                <xsl:text>反义词</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="$expression"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
