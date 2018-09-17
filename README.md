# Software Jobs in America 

A little local website that can show several map plots of software engineer jobs for every state and nationwide, a bar chart of different programming languages demand, and another bar chart of job distribution by state.

This project can be divided into 4 parts: 

1. Data scraping
2. Data processing
3. Ploting
4. Build web page

*requirements.txt*: Virtual environment requirement.

> : )     : p    : D
>
>Highly recommend download all of the cache files, and use saved caches to do the following steps. If you running the program without those caches , it will take very long time to make new requests. 
>
>If you still want to make new requests without my caches to see if it works, I wrote a sample demo for just scraping several pages with the same logic as the original program(take only several minus to run). All files start with 'sample' is related to it.
>
>__*sample_for_data_process.py*__ is a demo for data accessing(only scrap 25 jobs). It combined the files of 
>
>get_all_intro_pages.py  <———> part1 in sample_for_data_process.py
>
>get_all_detail_pages.py <———> part2 in sample_for_data_process.py
>
>get_company_coordinate.py  <———> part3 in sample_for_data_process.py
>
>And save all information into ./data_process/sample_jobs.sqlite
>
>------------
>
>There are two options to check the whole database:
>
>1. *./data_process/jobs.sqlite* is well prepared, you could just look at it.
>2. If you want to regenerate *./data_process/jobs.sqlite*. STEP A: run get_all_intro_pages.py; STEP B: run get_all_detail_pages.py; type in yes to rewrite the database. STEP C: run get_company_coordinate.py to get geolat, geolon and fill the spaces in table Company in  *./data_process/jobs.sqlite* 
>
>-----
>
>Besides, seems like the [Careerbuilder website](https://www.careerbuilder.com/jobs-software-engineer) has made some changes after I scraped it on Mar. 28th. When I was collecting my database, there were 100 pages of searching results in total. However, there are only 12 pages, and about 300+ jobs showing on the website for now. In order to get the original 100 pages and 2500+ jobs, I found another website [Careerbuilder-landing](https://www.careerbuilder.com/landing/software-engineer) , which seems just like the pages I scraped. So in the sample file, I use the new website.

## 1. Data scraping 

All of the data comes from [CareerBuilder-SoftwareEngineer](https://www.careerbuilder.com/jobs-software-engineer), there are 100 pages in total and 25 jobs in each page. 

Files are under **data_process** folder named like *get_<something>.py*

__*get_all_intro_pages.py*__  

Scrap and crawl all 100 first search level pages. And saved detail url of every job into *./caches/detail_urls.text*. Caches of all those pages are saved in *./pages_cache.json*

__*get_all_detail_pages.py*__  

1. Scrap and crawl all 2500 deeper search level pages. (Valid detail pages is less than 2500 because some jobs are expired, so the website change those detail pages into "The requested job has expired" —— all of the invalid urls are saved into *./caches/error_url.text*) Caches of all detail pages are saved into *./caches/detail_pages0.json* to *./caches/detail_pages24.json*. (To avoid obtaining one single huge cache file.)
2. Create jobs.sqlite and fill out Jobs Table and Company Table, left GeoLat and Geolon in Company as NULL.

__*get_company_coodinate.py*__ 

1. Converting addresses (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates via [Google Maps API](https://developers.google.com/maps/documentation/geocoding/intro#Geocoding) , the keywords are from Address column in Table Company. You have to apply for an api key and copy it into your own secret file name as 'secrets.py'. 

   *Secrets_example.py* is an template for it. However, if the 'caches' folder and all of the cache files are under it, you won't need to fill the api key.

2. Fill out GeoLat and Geolon in Table Company.

__*get_prog_language.py*__

Scrap [Top 100+ Most populat Programming Languages](https://www.whoishostingthis.com/resources/programming/) and save them into *prog_language.txt*

__Tip for scraping:__

1. So as to deal with the anti-scraping mechanism (like block ip, refuse request made by a program), I add Referer and User-Agent in header, and change ip every time when making new requests, in order to act like a human using browser. In addition, *proxy_ip.py* is used for generating random proxy ip from website https://www.sslproxies.org/ .

2. There is a limit each day for Google Maps API(less than 2500 requests per day)

   [Google Maps Geocoding API Usage Limits](https://developers.google.com/maps/documentation/geocoding/usage-limits)

## 2. Data processing

File under **data_process** folder.

__*save_description_for_word_cloud.py*__

Save job descriptions of all jobs into *jobDescription.txt* 

Word cloud 'use-map2.png' is generated by https://wordart.com/

## 3. Ploting

Files under **data_process** folder named like *plot_something.py*

Plots are generated via plotly,(please make sure Plotly is already setup in your computer, [Tutorial for Plotly](https://plot.ly/python/getting-started/)) in order to use plotly-mapbox, you also have to apply for a mapbox_access_token and copy it into your own *secrets.py* file, *Secrets_example.py* is an template for it.

 [Scatter Plots on Mapbox in Python Tutorial](https://plot.ly/python/scattermapbox/) 

[Mapbox Access Token](https://www.mapbox.com/studio)

__*plot_all_jobs.py*__

Running this file, you could plot all jobs (in the Table Jobs from *jobs.sqlite*) on a single map.

__*plot_job_by_state.py*__

Running this file will create an interactive command line application for plotting jobs. You could type in <the abbreviation of the state name> you want or  <exit> to quit the program. 

The Class *JobinStateClass.py* is used here to create instances for each state, and were saved in a dictionary named geo_by_state (key=abbreviation of a state, value=state instance).

__*plot_num_of_jobs_by_state*__

Running this file, you could generate a single bar chart, showing job distribution for each state in percentage. 

$$\frac{num\_of\_jobs\_in\_a\_state}{sum\_of\_jobs\_of\_all\_states} $$

__*plot_top5_jobdescription*__

Running this file, you could generate a single bar chart, showing top 30 popular programming languages. 

Popularity information is obtained by counting the number of appearance of each programing language in job description.

## 4. Web application

Files under **web_app** folder.

__*jobs_app.py*__

The main application program.

All plots are embedded as html in templates folder.
