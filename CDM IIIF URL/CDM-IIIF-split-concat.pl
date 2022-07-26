#!/usr/local/bin/perl -w
#
# Program to take an argument and search
# a file, printing instances of it

open(ERROR, ">error.txt");
print "What file do you want to split\?";
chomp($file = <>);
print "\n\n";
print 'What is the base CDM URL (include https:// and the part of the URL prior to /digital/collection)?. Use the most recent version of the standard CDM url format. ';
chomp($baseurl = <>);
$baseurl =~ s,http\:,https\:,g;
$newfile  = "$file";
$newfile =~ s,\.xml,-iiif\.xml,;

open (CONCAT, ">$newfile") || die "cannot open file - $!";
open(INFO, $file) or die "can't open $file";
@txt = <INFO>;      #read data into an array
chomp @txt;         #get rid of all the many \n's taken into the array
$txt = "@txt";      #read entire array into one scalar--one long string
$txt =~ s,at\>http\:,at\>https\:,g;

if ($txt =~ /u\?/)
	{
	$txt =~ s,u\?\/,digital\/collection\/,g;
	$txt =~ s,collection\/(.*?)\,(.*?)\<\/edm,collection\/$1\/id\/$2\<\/edm,g;
	}
if ($txt=~ /cdm/)
	{
	$txt =~ s,\/cdm\/ref\/,\/digital\/,g;
	$txt =~ s,\/cdm\/singleitem\/,\/digital\/,g;
	}
if ($txt =~ /rec/)
	{
	$txt =~ s,\/rec\/.*?<\/edm_is_shown_at>,<\/edm_is_shown_at>,g;
	}
if ($txt =~ /singleitem/)
	{
	$txt =~ s,singleitem\/,,g;
	}
@data = split(/\<\/item\>/, $txt); #create array split at each $search
for ($n=0; $n< $#data; $n++)    # $# is pre-def. as last array element
    {
	$data[$n] =~ s,>\s+,>,g;
	$data[$n] =~ s,\s+<,<,g;
	$data[$n] =~ s,><,>\r\n<,g;
	print ERROR "$baseurl\r\n";

		if ($data[$n] =~ /_type\>MovingImage/) #ignores MovingImage records
			{
				print CONCAT "$data[$n]";
				print CONCAT "\<\/item\>\n";
			}
		elsif ($data[$n] =~ /_type\>Sound/) #ignores Sound records
			{
				print CONCAT "$data[$n]";
				print CONCAT "\<\/item\>\n";
			}

		elsif ($data[$n] =~ /application\/pdf/) #ignores PDFs
			{
				print CONCAT "$data[$n]";
				print CONCAT "\<\/item\>\n";
			}
		else
			{

				$data[$n] =~ s,\<edm_is_shown_at\>$baseurl\/digital\/collection\/(.*?)\/id\/(.*?)\<\/edm_is_shown_at\>,\<edm_is_shown_at\>$baseurl\/digital\/collection\/$1\/id\/$2\<\/edm_is_shown_at\>,g;
				$collection = $1;
				$item = $2;
				$data[$n] =~ s,\<edm_is_shown_at\>(.*?)\<\/edm_is_shown_at\>,\<edm_is_shown_at\>$1\<\/edm_is_shown_at\>,g;
				$edmat = $1;
				print ERROR "$edmat\r\n$collection\r\n$item\r\n";
				$data[$n] =~ s,\<iiif_partner_url nil="true"\/\>,\<iiif_partner_url\>$baseurl\/iiif\/2\/$collection\:$item/manifest.json\<\/iiif_partner_url\>,g;
				print CONCAT "$data[$n]";
				print CONCAT "<\/item>\n";
			}
    }
print CONCAT "\<\/items\>";
close INFO;
#and close the "for" loop
