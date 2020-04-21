<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:variable name="langue" select="'cmn'"/>

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
        \setdefaultlanguage{french}
        \setotherlanguages{french,english}
        \setmainfont{Charis SIL}
        \usepackage{media9}
        \usepackage{totcount}
        \newcounter{compteur}
        \setcounter{compteur}{0}
        \regtotcounter{compteur}
        \newfontfamily{\prin}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Gentium}
        \newfontfamily{\nru}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Charis SIL}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\cmn}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{AR PL UMing CN}
        \newfontfamily{\eng}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newfontfamily{\bod}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Gentium}
        \newcommand{\pprin}[1]{\begin{<xsl:value-of select="$langue"/>}{\prin #1}\end{<xsl:value-of select="$langue"/>}}
        \newcommand{\pnru}[1]{{\nru\textcolor{<xsl:value-of select="$nru"/>}{#1}}}
        \newcommand{\pfra}[1]{\begin{french}{\fra\textcolor{<xsl:value-of select="$fra"/>}{#1}}\end{french}}
        \newcommand{\pcmn}[1]{{\cmn\textcolor{<xsl:value-of select="$cmn"/>}{#1}}}
        \newcommand{\peng}[1]{\begin{english}{\eng\textcolor{<xsl:value-of select="$eng"/>}{#1}}\end{english}}
        \newcommand{\pbod}[1]{{\bod\textcolor{<xsl:value-of select="$bod"/>}{#1}}}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-0.5pt} {\footnotesize{\pnru{#1}}}}}}
        \newcommand{\caractère}[1]{\phantomsection\addcontentsline{toc}{section}{#1}{\begin{center}\textbf{\Large\pnru{#1}}\end{center}}}
        \newenvironment{entrée}[3]{\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsection}{#1\homonyme{#2}}\hspace*{-0.5cm}\textbf{\Large\pnru{#1 \homonyme{#2}}}\markright{#1 \homonyme{#2}}}{\stepcounter{compteur}\newline}
        \newenvironment{sous-entrée}[3]{\par\hypertarget{#3}{}\phantomsection\addcontentsline{toc}{subsubsection}{#1 \homonyme{#2}}\begin{adjustwidth}{0.3cm}{}\pprin{■} \textbf{\Large\pnru{#1\homonyme{#2}}}}{\end{adjustwidth}}
        \newcommand{\homonyme}[1]{#1}
        \newcommand{\formedesurface}[1]{\hspace{0.5cm}/\pnru{#1}/\hspace{0.5cm}}
        \newcommand{\formephonétique}[1]{\pnru{\textit{#1}}}
        \newcommand{\ton}[1]{\cmn{声调类：}\prin{#1}\hspace{0.5cm}}
        \newcommand{\classe}[1]{ \pcmn{\textcolor{PineGreen}{#1} }}
        \newcommand{\paradigme}[1]{#1 }
        \newcommand{\sens}[1]{ \cerclé{#1} }
        \newenvironment{définition}{}{\hspace{5pt}}
        \newenvironment{déclaration}{}{}
        \newenvironment{exemple}{\pprin{¶} }{\hspace{5pt}}
        \newenvironment{relationsémantique}{}{}
        \newenvironment{forme-mot}{}{}
        \newcommand{\synonyme}[1]{\pcmn{~【同义词】~\pnru{#1}}}
        \newcommand{\antonyme}[1]{\pcmn{~【反义词】~\pnru{#1}}}
        \newcommand{\confer}[1]{\pcmn{~【参考】~\pnru{#1}}}
        \newcommand{\emprunt}[1]{\pcmn{~【借词】~#1}}
        \newcommand{\étymologie}[1]{\pcmn{~【词源】~#1}}
        \newcommand{\utilisation}[1]{\pcmn{~【用法】#1}}
        \newcommand{\grammaire}[1]{\textsc{#1}}
        \newcommand{\stylefv}[1]{\pnru{#1}}
        \newcommand{\stylefn}[1]{\pcmn{#1}}
        \newcommand{\stylefi}[1]{\textit{#1}}
        \newcommand{\stylefg}[1]{\textsc{#1}}
        \XeTeXlinebreaklocale "zh"
        \XeTeXlinebreakskip = 0pt plus 1pt
        % % Code spécial pour la gestion générique des césures applicable aux formes de surface
        %\ExplSyntaxOn
        %\RenewDocumentCommand{\formedesurface}{m}
        %{
        %    % nouvelle variable « expression »
        %    \tl_set:Nn \expression { #1 }
        %    % remplace ˩˧˥ par ˩˧˥\-
        %    \regex_replace_all:nnN { (\B[˩˧˥]) } { \1\c{-} } \expression
        %    % renvoie la séquence totale
        %    {\tl_use: {\hspace{0.5cm}/\pnru{\expression}/\hspace{0.5cm}}}
        %}
        %\ExplSyntaxOff
        <xsl:text>&#xd;</xsl:text>
        \begin{document}
        �introduction
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

    <xsl:template match="Dictionnaire">
        <xsl:for-each select="EntréeLexicale">
            <xsl:variable name="caractère" select="substring(translate(Lemme/FormeÉcrite, '_^-‐‑*=', ''), 1, 1)"/>
            <xsl:if test="$caractère != substring(translate(preceding-sibling::EntréeLexicale[1]/Lemme/FormeÉcrite, '_^-‐‑*=', ''), 1, 1)">
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
        <xsl:apply-templates/>
        <xsl:text>\end{entrée}</xsl:text>
        <xsl:text>&#xa;&#xd;</xsl:text>
    </xsl:template>

    <xsl:template match="Lemme">
        <xsl:text>{</xsl:text>
        <xsl:value-of select="FormeÉcrite"/>
        <xsl:text>}{</xsl:text>
        <xsl:if test="../NuméroDHomonyme">
            <xsl:value-of select="translate(../NuméroDHomonyme, $nombres, $indices)"/>
        </xsl:if>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="../@identifiant"/>
        <xsl:text>}</xsl:text>
        <xsl:if test="FormeDeSurface">
            <xsl:text>\formedesurface{</xsl:text>
            <xsl:value-of select="FormeDeSurface"/>
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:if test="FormePhonétique">
            <xsl:text>\formephonétique{</xsl:text>
            <xsl:value-of select="FormePhonétique"/>
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:text>\newline</xsl:text>
        <xsl:if test="ancestor::EntréeLexicale/ClasseGrammaticale">
            <xsl:text>&#10;</xsl:text>
            <xsl:text>\classe{</xsl:text>
            <xsl:call-template name="traduction">
                <xsl:with-param name="expression" select="ancestor::EntréeLexicale/ClasseGrammaticale"/>
            </xsl:call-template>
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:if test="Ton">
            <xsl:text>\ton{</xsl:text>
            <xsl:value-of select="Ton"/>
            <xsl:text>}</xsl:text>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="ClasseGrammaticale">
    </xsl:template>

    <xsl:template match="Étymologie">
        <xsl:text>\étymologie{</xsl:text>
        <xsl:for-each select="Étymon">
            <xsl:value-of select="."/>
            <xsl:if test="not(position() = last())">
                <xsl:text>,</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:text>}</xsl:text> 
    </xsl:template>
    
    <xsl:template match="Sens">
        <xsl:text>&#10;</xsl:text>
        <xsl:if test="NuméroDeSens">
            <xsl:text>\sens{</xsl:text>
            <xsl:value-of select="NuméroDeSens"/>
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:apply-templates select="Définition"/>
        <xsl:apply-templates select="Exemple"/>
        <xsl:apply-templates select="RelationSémantique"/>
        <xsl:apply-templates select="Paradigme"/>
    </xsl:template>

    <xsl:template match="Définition">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{définition}</xsl:text>
        <xsl:text>\p</xsl:text>
        <xsl:value-of select="ReprésentationDeTexte/@langue"/>
        <xsl:text>{</xsl:text>
        <xsl:apply-templates select="ReprésentationDeTexte"/>
        <xsl:text>}</xsl:text>
        <xsl:apply-templates select="Statement"/>
        <xsl:text>\end{définition}</xsl:text>
    </xsl:template>

    <xsl:template match="Exemple">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{exemple}</xsl:text>
        <xsl:for-each select="ReprésentationDeTexte">
            <xsl:text>\p</xsl:text>
            <xsl:value-of select="@langue"/>
            <xsl:text>{</xsl:text>
            <xsl:value-of select="."/>
            <xsl:text>}</xsl:text>
            <xsl:if test="not(position() = last())">
                <xsl:text>\hspace{5pt}</xsl:text>
            </xsl:if>
        </xsl:for-each>
        <xsl:if test="Déclaration[Type = 'ton']">
            <xsl:text>\pcmn{（}\ton{</xsl:text>
            <xsl:value-of select="Déclaration[Type = 'ton']"/>
            <xsl:text>}\pcmn{）}</xsl:text>
        </xsl:if>
        <xsl:text>\end{exemple}</xsl:text>
    </xsl:template>

    <xsl:template match="Statement[feat[@att='note'] and feat[@att='type' and @val='use']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{déclaration}</xsl:text>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="feat[@att='type']/@val"/>
        <xsl:text>{</xsl:text>
        <xsl:call-template name="traduction">
            <xsl:with-param name="expression" select="feat[@att='note']/@val"/>
        </xsl:call-template>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{déclaration}</xsl:text>
    </xsl:template>

    <xsl:template match="Statement[feat[@att='étymologie']]">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{déclaration}</xsl:text>
        <xsl:text> \étymologie{\pnru{</xsl:text>
        <xsl:choose>
            <xsl:when test="feat/content">
                <xsl:apply-templates select="feat"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="feat/@val"/>
            </xsl:otherwise>
        </xsl:choose>
        <xsl:text>}} </xsl:text>
        <xsl:text>\end{déclaration}</xsl:text>
    </xsl:template>

    <xsl:template match="RelationSémantique">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\begin{relationsémantique}</xsl:text>
        <xsl:text>\</xsl:text>
        <xsl:value-of select="@langue"/>
        <xsl:text>{</xsl:text>
        <xsl:if test="@langue">
            <xsl:text>\p</xsl:text>
            <xsl:value-of select="@langue"/>
            <xsl:text>{</xsl:text>
        </xsl:if>
        <xsl:apply-templates/>
        <xsl:if test="@langue">
            <xsl:text>}</xsl:text>
        </xsl:if>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{relationsémantique}</xsl:text>
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
        <xsl:text>\pcmn{ : }</xsl:text>
        <xsl:text>\pnru{</xsl:text>
        <xsl:value-of select="ReprésentationDeForme/feat[@att='writtenForm']/@val"/>
        <xsl:text>}</xsl:text>
        <xsl:text>\end{forme-mot}</xsl:text>
    </xsl:template>

    <xsl:template match="Paradigme">
        <xsl:text>&#10;</xsl:text>
        <xsl:text>\paradigme{\pcmn</xsl:text>
        <xsl:text>{</xsl:text>
        <xsl:call-template name="traduction">
            <xsl:with-param name="expression" select="feat[@att='name']/@val"/>
        </xsl:call-template>
        <xsl:text>：} \p</xsl:text>
        <xsl:value-of select="@langue"/>
        <xsl:text>{</xsl:text>
        <xsl:value-of select="feat[@att='paradigm']/@val"/>
        <xsl:text>}}</xsl:text>
        <xsl:apply-templates select="ParadigmComment"/>
    </xsl:template>

    <xsl:template match="ParadigmComment">
        <xsl:if test="$langue=feat[@att='language']/@val">
            <xsl:text>(\p</xsl:text>
            <xsl:value-of select="feat[@att='language']/@val"/>
            <xsl:text>{</xsl:text>
            <xsl:value-of select="feat[@att='comment']/@val"/>
            <xsl:text>}</xsl:text>
            <xsl:text>)</xsl:text>
        </xsl:if>
    </xsl:template>

    <xsl:template match="lien|link">
        <xsl:text>\hyperlink{</xsl:text>
        <xsl:value-of select="@cible|@target"/>
        <xsl:text>}{</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text>}</xsl:text>
    </xsl:template>

    <xsl:template match="non_lien">
        <xsl:value-of select="."/>
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
            <xsl:when test="$expression='adj'">
                <xsl:text>形容词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='adv'">
                <xsl:text>助词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='clf'">
                <xsl:text>量词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='clitic'">
                <xsl:text>附着词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='cnj'">
                <xsl:text>连接词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='disc.PTCL'">
                <xsl:text>语气助词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='ideo'">
                <xsl:text>状貌词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='intj'">
                <xsl:text>感叹词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='lnk'">
                <xsl:text>连词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='n'">
                <xsl:text>名词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='neg'">
                <xsl:text>否定词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='num'">
                <xsl:text>数词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='post'">
                <xsl:text>后置词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='pref'">
                <xsl:text>前缀</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='prep'">
                <xsl:text>介词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='pro'">
                <xsl:text>代词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='suff'">
                <xsl:text>后缀</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='v'">
                <xsl:text>动词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='classifier'">
                <xsl:text>量词</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='PHONO'">
                <xsl:text>音系资料</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='PROVERBE'">
                <xsl:text>谚语</xsl:text>
            </xsl:when>
            <xsl:when test="$expression='archaic'">
                <xsl:text>古语</xsl:text>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
