# RSS reader
RSS reader is a command-line utility which receives RSS URL and prints results in human-readable
format.

[The source for this project is available here](https://github.com/PolinaYud/Final-Task).


### Installation
$ pip install rss-reader-palina-yudzina

### Usage
$ rss-reader (-h | --help)

    Show help message and exit

$ rss-reader <RSS-SOURCE-LINK>

    Print rss feeds in human-readable format

$ rss-reader --version

    Print version info

$ rss-reader --json

    Print result as JSON in stdout

$ rss-reader --verbose

    Outputs verbose status messages
    
$ rss-reader--limit LIMIT

    Limit news topics, if this parameter provided

$ rss-reader --date DATE

    Gets a date in %Y%m%d format. Print news from the specified date
    and source (<RSS-SOURCE-LINK>), if it specified

$ rss-reader.py --to-pdf PATH_TO_PDF

    Gets file path. Convert news to pdf and save them to pdf file on the specified path

$ rss-reader.py --to-html PATH_TO_HTML

    Gets file path. Convert news to html and save them to html file on the specified path


    

Utility provide the following interface:

usage: rss_reader.py [-h] [--version] [--json] [--verbose] [--limit LIMIT] source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided

#JSON structure:

{

 [
 
           {      
             "feed_title": feed title,                         
             "title": news title,
             "summary": news content,
             "date": news publication date,
             "link": news link },
           
           {  
             "feed_title": feed title,             
             "title": news title,
             "summary": news content,
             "date": news publication date,
             "link": news link },

           ...
         
 ]
}
