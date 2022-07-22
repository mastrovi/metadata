#!/usr/local/bin/perl -w
#
# Program to take an argument and search
# a file, printing instances of it

open(ERROR, ">error.txt");

print "What file do you want to split\? ";

chomp($file = <>);

print "\n\n ";

print 'What is the base CDM URL (include https:// and the part of the URL prior to /digital/collection)?. Use the most recent version of the standard CDM url format. ';


chomp($baseurl = <>); 





open (CONCAT, ">concatenated-xml.txt") || die "cannot open file - $!";
 
open (ERROR, ">delete.txt");

open(INFO, $file) or die "can't open $file";

@txt = <INFO>;      #read data into an array

chomp @txt;         #get rid of all the many \n's taken into the array
$txt = "@txt";      #read entire array into one scalar--
		    #one long string, in effect

if ($txt =~ /u\?/)
	{
$txt =~ s,/u\?/(.*?)\,(.*?)</edm_is_shown_at>,/digital/collection/$1/id/$2</edm_is_shown_at>,g;
}
if ($txt=~ /cdm/)
{
$txt =~ s,/cdm/ref/,/digital/,g;
$txt =~ s,/cdm/singleitem/,/digital/,g;
}

if ($txt =~ /http:/)
{
$txt =~ s,at>http:,at>https:,g;
}

print ERROR $txt;

@data = split(/<\/item>/, $txt); #create array split at each $search

for ($n=0; $n< $#data; $n++)    # $# is pre-def. as last array element
    {
$data[$n] =~ s,>\s+,>,g;
$data[$n] =~ s,\s+<,<,g;
$data[$n] =~ s,><,>\r\n<,g;

$data[$n] =~ s,<edm_is_shown_at>$baseurl/digital/collection/(.*?)/id/(.*?)</edm_is_shown_at>,<edm_is_shown_at>$baseurl/digital/collection/$1/id/$2</edm_is_shown_at>,g;
$collection = $1;
$item = $2;

$baseurl =~ s,/digital/collection,,;

$data[$n] =~ s,<iiif_partner_url nil="true"/>,<iiif_partner_url>$baseurl/iiif/2/$collection:$item/manifest.json</iiif_partner_url>,g;

print CONCAT "$data[$n]";
print CONCAT "</item>\n";

    }
print CONCAT "</items>";  
close INFO;
        #and close the "for" loop
