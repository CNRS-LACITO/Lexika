<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xsl:output method="text"/>

    <xsl:template match="/">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="LexicalResource">
        \usepackage[paperwidth=185mm,paperheight=260mm,top=16mm,bottom=16mm,left=15mm,right=20mm]{geometry}
        \usepackage{multicol}
        \setlength{\columnseprule}{1pt}
        \setlength{\columnsep}{1.5cm}
        \usepackage{color}
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyheadoffset{3.4em}
        \fancyhead[LE,LO]{\rightmark}
        \fancyhead[RE,RO]{\leftmark}
        \usepackage[bookmarks=true,colorlinks,linkcolor=blue]{hyperref}
        \hypersetup{bookmarks=false,bookmarksnumbered,bookmarksopenlevel=5,bookmarksdepth=5,xetex,colorlinks=true,linkcolor=blue,citecolor=blue}
        \usepackage{fontspec}
        \usepackage{natbib}
        \usepackage{booktabs}
        \usepackage{polyglossia}
        \setmainfont{Liberation Serif}
        \newfontfamily{\fra}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\cmn}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{SimSun}
        \newfontfamily{\jya}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{EB Garamond}
        \newfontfamily{\policelien}[Mapping=tex-text,Ligatures=Common,Scale=MatchUppercase]{Liberation Serif}
        \newcommand{\cerclé}[1]{\raisebox{0pt}{\textcircled{\raisebox{-1pt} {#1}}}}
        \newcommand{\caractère}[1]{\begin{center}\textbf{\Large #1}\end{center}}
        \newenvironment{entrée}{}{\newline}
        \newenvironment{sous-entrée}{\newline ■ }{}
        \newcommand{\vedette}[1]{\textbf{\Large #1}}
        \newcommand{\classe}[1]{\textit{#1. }}
        \newcommand{\acception}[1]{\cerclé{#1} }
        \newenvironment{définition}{}{\hspace{5pt}}
        \newenvironment{exemple}{¶ }{\hspace{5pt}}
        \newenvironment{relation-sémantique}{}{}
        \newcommand{\synonyme}[1]{\cmn ~【同义词】~#1}
        \newcommand{\loanword}[1]{\cmn ~【外来语】~#1}
        \newcommand{\morphology}[1]{\cmn ~【参考】~#1}
        \newcommand{\confer}[1]{\cmn ~【比较】~#1}
        \XeTeXlinebreaklocale "zh"
        \XeTeXlinebreakskip = 0pt plus 1pt
        \lhead{\firstmark}
        \rhead{\botmark}
        <xsl:text>&#xd;</xsl:text>
        \begin{document}
        \begin{multicols}{2}
        <xsl:apply-templates/>
        \end{multicols}
        \end{document}
    </xsl:template>

    <xsl:template match="Lexicon">
        <xsl:for-each select="LexicalEntry">
            <xsl:variable name="caractère" select="substring(translate(Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)"/>
            <xsl:if test="$caractère != substring(translate(preceding-sibling::LexicalEntry[1]/Lemma/feat[@att='lexeme']/@val, '_^', ''), 1, 1)">
                \caractère{<xsl:value-of select="$caractère"/>}
            </xsl:if>
            <xsl:apply-templates select="."/>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="LexicalEntry">
        <xsl:text>&#10;</xsl:text>
        <!--***<xsl:value-of select="ancestor::node()"/>***-->
        \begin{entrée}
        <xsl:apply-templates/>
        <xsl:apply-templates select="../LexicalSubentry[RelatedForm[feat[@att='target' and @val=current()/@id]]]"/>
        \end{entrée}
    </xsl:template>

    <xsl:template match="Lemma">
        \vedette{\hypertarget{<xsl:value-of select="ancestor::LexicalEntry/@id"/>}{<xsl:value-of select="feat[@att='lexeme']/@val"/>}}
        \markboth{<xsl:value-of select="feat[@att='lexeme']/@val"/>}{}
    </xsl:template>
    
    <xsl:template match="feat[@att='partOfSpeech']">
        \classe{<xsl:value-of select="@val"/>}
    </xsl:template>
    
    <xsl:template match="Sense">
        <xsl:text>&#10;</xsl:text>
            <xsl:if test="feat[@att='senseNumber' and @val!='0']">
            \acception{<xsl:value-of select="feat[@att='senseNumber' and @val!='0']/@val"/>}
            </xsl:if>
        <xsl:apply-templates select="Definition"/>
        <xsl:apply-templates select="Context"/>
        <xsl:apply-templates select="SenseRelation"/>
    </xsl:template>
    
    <xsl:template match="Definition">
        <xsl:text>&#10;</xsl:text>
        \begin{définition}
        \<xsl:value-of select="feat[@att='language']/@val"/><xsl:text> </xsl:text><xsl:value-of select="feat[@att='gloss']/@val"/>
        \end{définition}
        <xsl:apply-templates/>
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

    <xsl:template match="SenseRelation">
        <xsl:text>&#10;</xsl:text>
        \begin{relation-sémantique}
        \<xsl:value-of select="feat[@att='type']/@val"/>{<xsl:apply-templates/>}
        \end{relation-sémantique}
    </xsl:template>

    <xsl:template match="LexicalSubentry">
        \begin{sous-entrée}
        <xsl:apply-templates/>
        \end{sous-entrée}
    </xsl:template>

    <xsl:template match="lien|link">
        \hyperlink{<xsl:value-of select="@cible|@target"/>}{\textit{\policelien<xsl:text> </xsl:text><xsl:value-of select="."/>}}
    </xsl:template>

    <xsl:template match="non_lien">
        \policelien<xsl:text> </xsl:text><xsl:value-of select="."/>
    </xsl:template>

</xsl:stylesheet>
