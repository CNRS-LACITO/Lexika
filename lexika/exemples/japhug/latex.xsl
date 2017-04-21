<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:variable name="dossier_audio" select="'AudioJaphug'"/>
    <xsl:variable name="format_audio" select="'mp3'"/>
    <xsl:variable name="inclure_audio" select="false()"/>
    <xsl:variable name="nombres" select="'0123456789'"/>
    <xsl:variable name="indices" select="'₀₁₂₃₄₅₆₇₈₉'"/>

    <xsl:variable name="fra">OliveGreen</xsl:variable>
    <xsl:variable name="eng">Sepia</xsl:variable>
    <xsl:variable name="cmn">black</xsl:variable>
    <xsl:variable name="nru">Blue</xsl:variable>
    <xsl:variable name="bod">black</xsl:variable>
    <!--<xsl:variable name="fra">black</xsl:variable>-->
    <!--<xsl:variable name="eng">black</xsl:variable>-->
    <!--<xsl:variable name="cmn">black</xsl:variable>-->
    <!--<xsl:variable name="nru">black</xsl:variable>-->
    <!--<xsl:variable name="bod">black</xsl:variable>-->

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="LexicalResource">
        \documentclass[twoside,11pt]{article}
        \title{�titre}
        \author{�auteur}
        \usepackage[paperwidth=185mm,paperheight=260mm,top=16mm,bottom=16mm,left=15mm,right=20mm]{geometry}
        \usepackage{multicol}
        \setlength{\columnseprule}{1pt}
        \setlength{\columnsep}{1.5cm}
        \usepackage{changepage}
        \usepackage{color}
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
        \setotherlanguages{french,english}
        \setmainfont{Liberation Serif}
        \usepackage{media9}
        \usepackage{fontawesome}
        \usepackage{totcount}
        \newcounter{compteur}
        \setcounter{compteur}{0}
        \regtotcounter{compteur}
        \newfontfamily{\prin}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\cmn}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{WenQuanYi Micro Hei}
        \newfontfamily{\jya}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Gentium Plus}
        \newcommand{\pprin}[1]{\begin{french}{\prin #1}\end{french}}
        \newcommand{\pfra}[1]{\begin{french}{\fra #1}\end{french}}
        \newcommand{\pcmn}[1]{{\cmn #1}}
        \newcommand{\pjya}[1]{{\jya #1}}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-0.5pt} {\footnotesize{\pjya{#1}}}}}}
        \newcommand{\caractère}[1]{\phantomsection\addcontentsline{toc}{section}{#1}{\begin{center}\textbf{\Large\pjya{#1}}\end{center}}}
        \newenvironment{entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsection}{#1\homonyme{#2}}\hspace*{-1cm}\textbf{\Large\pjya{#1\homonyme{#2}}}}{\stepcounter{compteur}}
        \newenvironment{sous-entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1\homonyme{#2}}\begin{adjustwidth}{0.3cm}{}\pprin{■} \textbf{\Large\pjya{#1\homonyme{#2}}}}{\end{adjustwidth}}
        \newcommand{\homonyme}[1]{#1}
        \newcommand{\variante}[1]{\textbf{\pjya{#1}}}
        \newcommand{\classe}[1]{\textit{#1.}}
        \newcommand{\paradigme}[1]{#1}
        \newcommand{\acception}[1]{\cerclé{#1}}
        \newenvironment{définition}{}{\hspace{5pt}}
        \newenvironment{déclaration}{}{}
        \newenvironment{exemple}{\pprin{¶} }{\hspace{5pt}}
        \newenvironment{relation-sémantique}{}{}
        \newenvironment{forme-mot}{}{}
        \newcommand{\synonyme}[1]{\pcmn{~【同义词】~#1}}
        \newcommand{\antonyme}[1]{\pcmn{~【反义词】~#1}}
        \newcommand{\confer}[1]{\pcmn{~【参考】~#1}}
        \newcommand{\étymologie}[1]{\pcmn{~【借词】~#1}}
        \newcommand{\use}[1]{\pcmn{~【用法】~#1}}
        \newcommand{\grammar}[1]{\textsc{#1}}
        \newcommand{\ComponentA}[1]{\cerclé{I} #1}
        \newcommand{\ComponentB}[1]{\cerclé{II} #1}
        \newcommand{\stylefv}[1]{\pjya{#1}}
        \newcommand{\stylefn}[1]{\pcmn{#1}}
        \newcommand{\écouter}[1]{\includemedia[activate=onclick,addresource=#1.<xsl:value-of select="$format_audio"/>,flashvars={source=#1.<xsl:value-of select="$format_audio"/>&amp;autoPlay=true&amp;autoRewind=true&amp;loop=false&amp;hideBar=true&amp;volume=1.0&amp;balance=0.0}]{\faicon{volume-down}}{APlayer.swf}}
        \addmediapath{<xsl:value-of select="$dossier_audio"/>}
        \newenvironment{bottompar}{\par\vspace*{\fill}}{\clearpage}
        \newcommand{\ital}[1]{{\normalfont\textit{#1}}}
        \newcommand{\caps}[1]{{\normalfont\textsc{#1}}}
        \XeTeXlinebreaklocale "zh"
        \XeTeXlinebreakskip = 0pt plus 1pt
        <xsl:text>&#xd;</xsl:text>
        \begin{document}
        �introduction
        \begin{multicols}{2}
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:apply-templates/>
        \end{multicols}
        \end{document}
    </xsl:template>

    <xsl:template match="Lexicon">
        <xsl:for-each select="LexicalEntry">
            <xsl:variable name="caractère" select="substring(translate(Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)"/>
            <xsl:if test="$caractère != substring(translate(preceding-sibling::LexicalEntry[1]/Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)">
                <xsl:text>\newpage</xsl:text>
                <xsl:text>\caractère{</xsl:text>
                <xsl:value-of select="$caractère"/>
                <xsl:text>}</xsl:text>
                <xsl:text>&#xa;&#xd;</xsl:text>
            </xsl:if>
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="LexicalEntry">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{entrée}</xsl:text>
        <xsl:apply-templates/>
        <xsl:apply-templates select="../LexicalSubentry[RelatedForm[feat[@att='target' and @val=current()/@id]]]"/>
        <xsl:text>\end{entrée}</xsl:text>
        <xsl:text>&#xa;&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="Lemma">
        <xsl:text>{</xsl:text>
        <xsl:value-of select="feat[@att='lexeme']/@val"/>
        <xsl:text>}{</xsl:text>
        <xsl:if test="../feat[@att='homonymeNumber']">
            <xsl:value-of select="translate(../feat[@att='homonymeNumber']/@val, $nombres, $indices)"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="../@id"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="FormRepresentation[feat[@att='allophone']]">
            <xsl:text>(</xsl:text>
            <xsl:for-each select="FormRepresentation[feat[@att='allophone']]">
                <xsl:text>\variante{</xsl:text>
                <xsl:value-of select="feat[@att='allophone']/@val"/>
                <xsl:text>}</xsl:text>
                <xsl:if test="not(position() = last())">
                    <xsl:text>,</xsl:text>
                </xsl:if>
            </xsl:for-each>
            <xsl:text>)</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="Media[feat[@att='type' and @val='audio'] and feat[@att='chemin']]">
        <xsl:if test="$inclure_audio">
            <xsl:text>&#xa;&#xd;</xsl:text>
            <xsl:text>\écouter{</xsl:text>
            <xsl:choose>
                <xsl:when test="eat[@att='qualité'='faible']">
                    <xsl:value-of select="concat('8_', feat[@att='chemin']/@val)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="feat[@att='chemin']/@val"/>
                </xsl:otherwise>
            </xsl:choose>
            <xsl:text>}</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="feat[@att='partOfSpeech']">
        <xsl:text>&#10;</xsl:text>
        <xsl:text> \classe{</xsl:text>
        <xsl:value-of select="@val"/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="Sense">
        <xsl:text>&#10;</xsl:text>
        <xsl:if test="feat[@att='senseNumber' and @val!='0']">
            <xsl:text>\acception{</xsl:text>
            <xsl:value-of select="feat[@att='senseNumber' and @val!='0']/@val"/>
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Paradigm"/>
        <xsl:apply-templates select="Definition"/>
        <xsl:apply-templates select="Context"/>
        <xsl:apply-templates select="SenseRelation"/>
    </xsl:template>

    <xsl:template match="Paradigm">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\paradigme{\textit{</xsl:text>
        <xsl:value-of select="feat[@att='name']/@val"/>
        <xsl:text>:} \p</xsl:text>
        <xsl:value-of select="feat[@att='language']/@val"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="feat[@att='paradigm']/@val"/>
        <xsl:text>}} </xsl:text>
    </xsl:template>

    <xsl:template match="Definition[feat[@att='gloss']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{définition}</xsl:text>
        <xsl:text>\p</xsl:text>
        <xsl:value-of select="feat[@att='language']/@val"/>
        <xsl:text>{</xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates select="feat"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat[@att='gloss']/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}</xsl:text>
        <xsl:apply-templates select="Statement"/>
        <xsl:text>\end{définition}</xsl:text>
    </xsl:template>

    <xsl:template match="Context[feat[@att='type' and @val='example']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{exemple}</xsl:text>
        <xsl:for-each select="TextRepresentation">
            <xsl:choose>
                <xsl:when test="feat/content">
                    <xsl:text>\p</xsl:text>
                    <xsl:value-of select="feat[@att='language']/@val"/>
                    <xsl:text>{</xsl:text>
                    <xsl:apply-templates select="feat"/>
                    <xsl:text>}</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>\p</xsl:text>
                    <xsl:value-of select="feat[@att='language']/@val"/>
                    <xsl:text>{</xsl:text>
                    <xsl:value-of select="feat[@att='writtenForm']/@val"/>
                    <xsl:text>}</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:for-each>
        <xsl:text>\end{exemple}</xsl:text>
    </xsl:template>

    <xsl:template match="Statement[feat[@att='note'] and feat[@att='type' and @val='grammar']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{déclaration}</xsl:text>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="feat[@att='type']/@val"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="feat[@att='note']/@val"/>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{déclaration} </xsl:text>
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
        <xsl:text>\begin{déclaration}</xsl:text>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="feat[@att='type']/@val"/>
        <xsl:text>{</xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat[@att='note']/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{déclaration} </xsl:text>
    </xsl:template>

    <xsl:template match="Statement[feat[@att='etymology']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{déclaration}</xsl:text>
        <xsl:text>\étymologie{\pjya{</xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates select="feat"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}}</xsl:text>
        <xsl:text>\end{déclaration} </xsl:text>
    </xsl:template>

    <xsl:template match="SenseRelation">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{relation-sémantique}</xsl:text>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="translate(translate(translate(feat[@att='type']/@val, ' ', ''), '1', 'A'), '2', 'B')"/>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{relation-sémantique} </xsl:text>
    </xsl:template>

    <xsl:template match="WordForm">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{forme-mot}</xsl:text>
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
        <xsl:text>:</xsl:text>
        <xsl:text>\pjya{</xsl:text>
        <xsl:value-of select="FormRepresentation/feat[@att='writtenForm']/@val"/>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{forme-mot}</xsl:text>
    </xsl:template>

    <xsl:template match="LexicalSubentry">
        <xsl:text>\begin{sous-entrée}</xsl:text>
        <xsl:apply-templates/>
        <xsl:text>\end{sous-entrée}</xsl:text>
    </xsl:template>

    <xsl:template match="lien|link">
        <xsl:text>\hyperlink{</xsl:text>
        <xsl:value-of select="@cible|@target"/>
        <xsl:text>}{ \textit{\pjya{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}}}</xsl:text>
    </xsl:template>

    <xsl:template match="non_lien">
        <xsl:text>\pjya{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="style">
        <xsl:text>\style</xsl:text>
        <xsl:value-of select="@type"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

</xsl:stylesheet>
