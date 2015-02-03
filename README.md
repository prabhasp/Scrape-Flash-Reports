## Scraping Flash School Reports
This project is about scraping the Flash School Reports in Nepal to create an
easily machine-readable dataset about the schools in Nepal.

It is also partially a learning project to learn the [scrapy](http://scrapy.org)
scraping platform.


### Getting started
 * Install [scrapy](http://doc.scrapy.org/en/latest/intro/install.html#intro-install)
 * Optional: Follow the [scrapy Intro tutorial](http://doc.scrapy.org/en/latest/intro/tutorial.html)

Get the data! After cloning this repository and cd-ing into the correct directory,
```
cd scrape_flash_reports
mkdir data
```
To get the districts / vdc lists, you can run:
```
scrapy crawl districts -o data/districts.csv
scrapy crawl vdcs -o data/vdcs.csv
```

To test that each school is being parsed properly, try:
```
scrapy parse 'http://202.70.77.75:8080/flash/schoolreport/reportshow.php?d=69&v=002&s=690020002&t=&yr=2070' --spider=schools --callback=parse_school_page
```

To scrape all the schools (untested), you can run:
```
scrapy crawl schools -o data/schools.csv -s JOBDIR=crawls/schools-1
```
This crawl can be stopped using CTRL-C and re-started, and should re-start from where it was. This is untested, but the documentation is from [here](http://doc.scrapy.org/en/latest/topics/jobs.html)

### Contributors
Contributors to this project:
 * Bikram Adhikari (@meadhikari)
 * Sakar Pudasaini (@karkhana)
 * Prabhas Pokharel (@prabhasp)
