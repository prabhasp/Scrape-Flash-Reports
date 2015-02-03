## Scraping Flash Education Reports

### How to get the data yourself
The following are the commands to download the `data` yourself:

```
mkdir data
scrapy crawl DistrictLister -o data/districts.csv
scrapy crawl VDCLister -o data/vdcs.csv
```
