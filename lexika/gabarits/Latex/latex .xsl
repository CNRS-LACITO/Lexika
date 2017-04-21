<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:variable name="dossier_audio" select="'AudioJaphug'"/>
    <xsl:variable name="format_audio" select="'mp3'"/>
    <xsl:variable name="inclure_audio" select="false"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="LexicalResource">
        \documentclass[twoside,11pt]{article}
        \title{$titre}
        \author{$auteur}
        \usepackage[paperwidth=185mm,paperheight=260mm,top=16mm,bottom=16mm,left=15mm,right=20mm]{geometry}
        \usepackage{multicol}
        \setlength{\columnseprule}{1pt}
        \setlength{\columnsep}{1.5cm}
        \usepackage{changepage}
        \setlength\parindent{-0.5em}
        \usepackage{color}
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyheadoffset{3.4em}
        \fancyhead[LE,LO]{\rightmark}
        \fancyhead[RE,RO]{\leftmark}
        \usepackage[bookmarks=true,colorlinks,linkcolor=blue]{hyperref}
        \hypersetup{bookmarks=false,bookmarksnumbered,bookmarksopenlevel=5,bookmarksdepth=5,xetex,colorlinks=true,linkcolor=blue,citecolor=blue}
        \usepackage[all]{hypcap}
        \usepackage{fontspec}
        \usepackage{natbib}
        \usepackage{booktabs}
        \usepackage{polyglossia}
        \setdefaultlanguage{french}
        \setmainfont{Liberation Serif}
        \usepackage{media9}
        \usepackage{fontawesome}
        \newfontfamily{\policedéfaut}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\cmn}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{SimSun}
        \newfontfamily{\jya}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\api}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Charis SIL}
        \newcommand{\pfra}[1]{{\fra #1}}
        \newcommand{\pcmn}[1]{{\cmn #1}}
        \newcommand{\pjya}[1]{{\jya #1}}
        \newcommand{\papi}[1]{{\api #1}}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-0.5pt} {\footnotesize{\policedéfaut #1}}}}}
        \newcommand{\caractère}[1]{\begin{center}\textbf{\Large #1}\end{center}}
        \newenvironment{entrée}{\par}{}
        \newenvironment{sous-entrée}{\begin{adjustwidth}{0.3cm}{}\policedéfaut ■ }{\end{adjustwidth}}
        \newcommand{\vedette}[1]{\textbf{\Large #1}}
        \newcommand{\homonyme}[1]{$$_{#1}$$}
        \newcommand{\variante}[1]{\textbf{#1}}
        \newcommand{\classe}[1]{ \textit{#1. }}
        \newcommand{\paradigme}[1]{#1 }
        \newcommand{\acception}[1]{ \cerclé{#1} }
        \newenvironment{définition}{}{\hspace{5pt}}
        \newenvironment{déclaration}{}{}
        \newenvironment{exemple}{¶ }{\hspace{5pt}}
        \newenvironment{relation-sémantique}{}{}
        \newenvironment{forme-mot}{}{}
        \newcommand{\synonyme}[1]{\pcmn{ ~【同义词】~#1}}
        \newcommand{\antonyme}[1]{\pcmn{ ~【反义词】~#1}}
        \newcommand{\confer}[1]{\pcmn{ ~【参考】~#1}}
        \newcommand{\étymologie}[1]{\pcmn{ ~【借词】~#1}}
        \newcommand{\use}[1]{\pcmn{ ~【用法】~#1}}
        \newcommand{\grammar}[1]{\textsc{#1}}
        \newcommand{\ComponentA}[1]{\cerclé{I} #1}
        \newcommand{\ComponentB}[1]{\cerclé{II} #1}
        \newcommand{\fv}[1]{{\papi{ #1}}}
        \newcommand{\fn}[1]{{\pcmn{ #1}}}
        \newcommand{\écouter}[1]{\includemedia[activate=onclick,addresource=#1.<xsl:value-of select="$format_audio"/>,flashvars={source=#1.<xsl:value-of select="$format_audio"/>&amp;autoPlay=true&amp;autoRewind=true&amp;loop=false&amp;hideBar=true&amp;volume=1.0&amp;balance=0.0}]{\faicon{volume-down}}{APlayer.swf}}
        \addmediapath{<xsl:value-of select="$dossier_audio"/>}
        \newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}
        \newcommand{\ital}[1]{{\normalfont\textit{#1}}}
        \newcommand{\caps}[1]{{\normalfont\textsc{#1}}}
        \usepackage{totcount}
        \newcounter{entrycounter}\setcounter{entrycounter}{0}\regtotcounter{entrycounter}%Compteur du nombre d'entrées
        \XeTeXlinebreaklocale "zh"
        \XeTeXlinebreakskip = 0pt plus 1pt
        <xsl:text>&#xd;</xsl:text>
        \begin{document}
        $introduction
        \begin{multicols}{2}
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:apply-templates/>
        \end{multicols}
        $tableaux
        \end{document}
    </xsl:template>

    <xsl:template match="Lexicon">
        <xsl:for-each select="LexicalEntry">
            <xsl:variable name="caractère" select="substring(translate(Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)"/>
            <xsl:if test="$caractère != substring(translate(preceding-sibling::LexicalEntry[1]/Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)">
                \newpage
                \caractère{<xsl:value-of select="$caractère"/>}
            </xsl:if>
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="LexicalEntry">
        <xsl:text>&#10;</xsl:text>
        \begin{entrée}
        <xsl:apply-templates/>
        <xsl:apply-templates select="../LexicalSubentry[RelatedForm[feat[@att='target' and @val=current()/@id]]]"/>
        \end{entrée}
    </xsl:template>

    <xsl:template match="Lemma">
        \vedette{\hypertarget{<xsl:value-of select="ancestor::LexicalEntry/@id"/>}{\policedéfaut<xsl:text> </xsl:text><xsl:value-of select="feat[@att='lexeme']/@val"/>}}
        \markboth{<xsl:value-of select="feat[@att='lexeme']/@val"/>}{}
        <xsl:if test="ancestor::LexicalEntry/feat[@att='homonymeNumber']">
            \homonyme{<xsl:value-of select="ancestor::LexicalEntry/feat[@att='homonymeNumber']/@val"/>}
        </xsl:if>
        <xsl:if test="FormRepresentation[feat[@att='allophone']]">
            <xsl:text> (%</xsl:text>
            <xsl:for-each select="FormRepresentation[feat[@att='allophone']]">
                \variante{<xsl:value-of select="feat[@att='allophone']/@val"/>}%
                <xsl:if test="not(position() = last())">, </xsl:if>
            </xsl:for-each>
            <xsl:text>) </xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="Media[feat[@att='type' and @val='audio'] and feat[@att='chemin']]">
        <xsl:if test="$inclure_audio">
            \écouter{<xsl:value-of select="feat[@att='chemin']/@val"/>}
        </xsl:if>
    </xsl:template>

    <xsl:template match="feat[@att='partOfSpeech']">
        <xsl:text>&#10;</xsl:text>
        \classe{<xsl:value-of select="@val"/>}
    </xsl:template>

    <xsl:template match="Sense">
        <xsl:text>&#10;</xsl:text>
            <xsl:if test="feat[@att='senseNumber' and @val!='0']">
            \acception{<xsl:value-of select="feat[@att='senseNumber' and @val!='0']/@val"/>}
            </xsl:if>
        <xsl:apply-templates select="Paradigm"/>
        <xsl:apply-templates select="Definition"/>
        <xsl:apply-templates select="Context"/>
        <xsl:apply-templates select="SenseRelation"/>
    </xsl:template>

    <xsl:template match="Paradigm">
        <xsl:text>&#10;</xsl:text>
        \paradigme{\textit{<xsl:value-of select="feat[@att='name']/@val"/> :} \<xsl:value-of select="feat[@att='language']/@val"/><xsl:text> </xsl:text><xsl:value-of select="feat[@att='paradigm']/@val"/>}
    </xsl:template>

    <xsl:template match="Definition">
        <xsl:text>&#10;</xsl:text>
        \begin{définition}
        \<xsl:value-of select="feat[@att='language']/@val"/><xsl:text> </xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates select="feat"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat[@att='gloss']/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:apply-templates select="Statement"/>
        \end{définition}
    </xsl:template>

    <xsl:template match="Context[feat[@att='type' and @val='example']]">
        <xsl:text>&#10;</xsl:text>
        \begin{exemple}
        <xsl:for-each select="TextRepresentation">
            <xsl:choose>
                <xsl:when test="feat/content">
                    \<xsl:value-of select="feat[@att='language']/@val"/><xsl:text> </xsl:text><xsl:apply-templates select="feat"/>
                </xsl:when>
                <xsl:otherwise>
                    \<xsl:value-of select="feat[@att='language']/@val"/><xsl:text> </xsl:text><xsl:value-of select="feat[@att='writtenForm']/@val"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        \end{exemple}
    </xsl:template>

    <xsl:template match="Statement[feat[@att='note'] and feat[@att='type' and @val='grammar']]">
        <xsl:text>&#10;</xsl:text>
        \begin{déclaration}
        \<xsl:value-of select="feat[@att='type']/@val"/>{<xsl:value-of select="feat[@att='note']/@val"/>}
        \end{déclaration}
    </xsl:template>

    <!--<xsl:template match="Statement[feat[@att='encyclopedicInformation']]">-->
        <!--<xsl:text>&#10;</xsl:text>-->
        <!--\begin{déclaration}-->
        <!--\<xsl:value-of select="feat[@att='type']/@val"/>{-->
        <!--<xsl:choose>-->
            <!--<xsl:when test="feat/content">-->
                <!--<xsl:apply-templates/>-->
            <!--</xsl:when>-->
            <!--<xsl:otherwise>-->
                <!--<xsl:value-of select="feat[@att='note']/@val"/>-->
            <!--</xsl:otherwise>-->
        <!--</xsl:choose>-->
        <!--}-->
        <!--\end{déclaration}-->
    <!--</xsl:template>-->

    <xsl:template match="Statement[feat[@att='note'] and feat[@att='type' and @val='use']]">
        <xsl:text>&#10;</xsl:text>
        \begin{déclaration}
        \<xsl:value-of select="feat[@att='type']/@val"/>{
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat[@att='note']/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        }
        \end{déclaration}
    </xsl:template>

    <xsl:template match="Statement[feat[@att='etymology']]">
        <xsl:text>&#10;</xsl:text>
        \begin{déclaration}
        <xsl:text> \étymologie{\fv{</xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates select="feat"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}}</xsl:text>
        \end{déclaration}
    </xsl:template>

    <xsl:template match="SenseRelation">
        <xsl:text>&#10;</xsl:text>
        \begin{relation-sémantique}
        \<xsl:value-of select="translate(translate(translate(feat[@att='type']/@val, ' ', ''), '1', 'A'), '2', 'B')"/>{<xsl:apply-templates/>}
        \end{relation-sémantique}
    </xsl:template>

    <xsl:template match="WordForm">
        <xsl:text>&#10;</xsl:text>
        \begin{forme-mot}
        <xsl:choose>
            <xsl:when test="feat[@att='person']/@val='first person'">
                <xsl:text>1</xsl:text>
            </xsl:when>
            <xsl:when test="feat[@att='person']/@val='second person'">
                <xsl:text>2</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>3</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:choose>
            <xsl:when test="feat[@att='grammaticalNumber']/@val='singular'">
                <xsl:text>s</xsl:text>
            </xsl:when>
            <xsl:otherwise>
                <xsl:text>p</xsl:text>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text> : </xsl:text>
        \fv{<xsl:value-of select="FormRepresentation/feat[@att='writtenForm']/@val"/>}
        \end{forme-mot}
    </xsl:template>

    <xsl:template match="LexicalSubentry">
        \begin{sous-entrée}
        <xsl:apply-templates/>
        \end{sous-entrée}
    </xsl:template>

    <xsl:template match="lien|link">
        \hyperlink{<xsl:value-of select="@cible|@target"/>}{\textit{<xsl:text> </xsl:text>\fv{<xsl:value-of select="."/>}}}
    </xsl:template>

    <xsl:template match="non_lien">
        <xsl:text> </xsl:text>\fv{<xsl:value-of select="."/>}
    </xsl:template>

    <xsl:template match="style">
         \<xsl:value-of select="@type"/>{<xsl:value-of select="."/>}
    </xsl:template>

</xsl:stylesheet>
