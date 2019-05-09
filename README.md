# travel-project-report
This code transforms all travel data into appropriate views for analysis. There are currently three views that can be downloaded.   


**by_quarter:** This data is aggregated by quarter. It mergges on consumer level travel data by DOT and merged on award data by city-pairs

**by_trip:** This is an aggregate level view of trip level data. It merges on total trip exepenses. and calculates flight cost based on segment level data

**by_segment:** flight route and cost by segement of trip. 

**by_person:** this data is aggregated by person by year.  It is good for analysis with credit card transactions

**train_plane:** this data merges train and plane reservation. It combines origin and destination of both into similar columns and price into one column. This leads to complications because people sometimes take multiple modes per trip, in those circumstances they are dropped. This is only a dataset where people took either train or plane. 

### if you want to run the whole program 
step 1. clone repo

step 2. download data from drive and insert data folder into repository

step 3. ```pipenv install```
```pipenv shell``` 
```pipenv run python save_data.py```
          
          


### if you want to just do analysis

step 1. clone repo

step 2. download data from drive and insert data folder into repository


