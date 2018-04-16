Mar. 28:

get new proxy ip list every 20 minutes,
select random proxy ip address from ip list.

Got 100 pages HTML, saved in `pages_cache.json`

Save all urls of detail page into a file `detail_urls.text`

Save detail pages HTML in 25 files.
    detail_pages0: 100 pages
    detail_pages1-23: 101 pages
    detail_pages24: less than 101 pages

Save the website url of detail pages with error (website with zero job title) occured into `error_url.text`

Mar. 31:

Save all info in to 2 tables:
    1. Jobs
    2. Companys

Apr. 7:
    Get geo coordinate of all companies.  (use GOOGLE MAP API)
    Save query caches to 'company_coordinate.json'
    update geo coordinate in Table Company.

    
