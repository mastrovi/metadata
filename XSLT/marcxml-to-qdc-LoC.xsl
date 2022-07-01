<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:marc="http://www.loc.gov/MARC21/slim" xmlns:oai_qdc="http://dublincore.org/documents/dcmi-terms/
" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" exclude-result-prefixes="marc">
	<xsl:import href="http://www.loc.gov/standards/marcxml/xslt/MARC21slimUtils.xsl"/>
	<xsl:output method="xml" indent="yes"/>
	<!--
	Fixed 530 Removed type="original" from dc_relation 2010-11-19 tmee
	Fixed 500 fields. 2006-12-11 ntra
	Added ISBN and deleted attributes 6/04 jer
	-->
	<xsl:template match="/">
		<xsl:if test="marc:collection">
			<oai_qdc:qdcCollection
 xsi:schemaLocation="http://dublincore.org/documents/dcmi-terms/ http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd">
				<xsl:for-each select="marc:collection">
					<xsl:for-each select="marc:record">
						<oai_qdc:qdc>
							<xsl:apply-templates select="."/>
						</oai_qdc:qdc>
					</xsl:for-each>
				</xsl:for-each>
			</oai_qdc:qdcCollection>
		</xsl:if>
		<xsl:if test="marc:record">
			<oai_qdc:qdc
 xsi:schemaLocation="http://dublincore.org/documents/dcmi-terms/
 http://www.openarchives.org/OAI/2.0/OAI-PMH.xsd
">
				<xsl:apply-templates/>
			</oai_qdc:qdc>
		</xsl:if>
	</xsl:template>
	<xsl:template match="marc:record">
		<xsl:variable name="leader" select="marc:leader"/>
		<xsl:variable name="leader6" select="substring($leader,7,1)"/>
		<xsl:variable name="leader7" select="substring($leader,8,1)"/>
		<xsl:variable name="controlField008" select="marc:controlfield[@tag=008]"/>
		<xsl:for-each select="marc:datafield[@tag=245]">
			<dcterms_title>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abfghk</xsl:with-param>
				</xsl:call-template>
			</dcterms_title>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=100]|marc:datafield[@tag=110]|marc:datafield[@tag=111]|marc:datafield[@tag=700]|marc:datafield[@tag=710]|marc:datafield[@tag=711]|marc:datafield[@tag=720]">
			<dcterms_creator>
				<xsl:value-of select="."/>
			</dcterms_creator>
		</xsl:for-each>
		<dcterms_type>
			<xsl:if test="$leader7='c'">
				<!--Remove attribute 6/04 jer-->
				<!--<xsl:attribute name="collection">yes</xsl:attribute>-->
				<xsl:text>collection</xsl:text>
			</xsl:if>
			<xsl:if test="$leader6='d' or $leader6='f' or $leader6='p' or $leader6='t'">
				<!--Remove attribute 6/04 jer-->
				<!--<xsl:attribute name="manuscript">yes</xsl:attribute>-->
				<xsl:text>manuscript</xsl:text>
			</xsl:if>
			<xsl:choose>
				<xsl:when test="$leader6='a' or $leader6='t'">text</xsl:when>
				<xsl:when test="$leader6='e' or $leader6='f'">cartographic</xsl:when>
				<xsl:when test="$leader6='c' or $leader6='d'">notated music</xsl:when>
				<xsl:when test="$leader6='i' or $leader6='j'">sound recording</xsl:when>
				<xsl:when test="$leader6='k'">still image</xsl:when>
				<xsl:when test="$leader6='g'">moving image</xsl:when>
				<xsl:when test="$leader6='r'">three dimensional object</xsl:when>
				<xsl:when test="$leader6='m'">software, multimedia</xsl:when>
				<xsl:when test="$leader6='p'">mixed material</xsl:when>
			</xsl:choose>
		</dcterms_type>
		<xsl:for-each select="marc:datafield[@tag=655]">
			<dcterms_type>
				<xsl:value-of select="."/>
			</dcterms_type>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=260]">
			<dcterms_publisher>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">ab</xsl:with-param>
				</xsl:call-template>
			</dcterms_publisher>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=260]/marc:subfield[@code='c']">
			<dc_date>
				<xsl:value-of select="."/>
			</dc_date>
		</xsl:for-each>
		<dcterms_language>
			<xsl:value-of select="substring($controlField008,36,3)"/>
		</dcterms_language>
		<xsl:for-each select="marc:datafield[@tag=856]/marc:subfield[@code='q']">
			<dc_format>
				<xsl:value-of select="."/>
			</dc_format>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=520]">
			<dcterms_description>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</dcterms_description>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=521]">
			<dcterms_description>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</dcterms_description>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[500&lt;= @tag and @tag&lt;= 599 ][not(@tag=506 or @tag=530 or @tag=540 or @tag=546)]">
			<dcterms_description>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</dcterms_description>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=600]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=610]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=611]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=630]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=650]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=653]">
			<dcterms_subject>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdq</xsl:with-param>
				</xsl:call-template>
			</dcterms_subject>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=752]">
			<dcterms_spatial>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcd</xsl:with-param>
				</xsl:call-template>
			</dcterms_spatial>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=530]">
			<dc_relation>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">abcdu</xsl:with-param>
				</xsl:call-template>
			</dc_relation>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=760]|marc:datafield[@tag=762]|marc:datafield[@tag=765]|marc:datafield[@tag=767]|marc:datafield[@tag=770]|marc:datafield[@tag=772]|marc:datafield[@tag=773]|marc:datafield[@tag=774]|marc:datafield[@tag=775]|marc:datafield[@tag=776]|marc:datafield[@tag=777]|marc:datafield[@tag=780]|marc:datafield[@tag=785]|marc:datafield[@tag=786]|marc:datafield[@tag=787]">
			<dc_relation>
				<xsl:call-template name="subfieldSelect">
					<xsl:with-param name="codes">ot</xsl:with-param>
				</xsl:call-template>
			</dc_relation>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=856]">
			<edm_is_shown_at>
				<xsl:value-of select="marc:subfield[@code='u']"/>
			</edm_is_shown_at>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=020]">
			<edm_is_shown_at>
				<xsl:text>URN:ISBN:</xsl:text>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</edm_is_shown_at>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=506]">
			<dc_right>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</dc_right>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=540]">
			<dc_right>
				<xsl:value-of select="marc:subfield[@code='a']"/>
			</dc_right>
		</xsl:for-each>
		<!--</oai_qdc:qdc>-->
	</xsl:template>
</xsl:stylesheet>