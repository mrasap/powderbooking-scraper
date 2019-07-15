# powderbooking-scraper
Python scraper for the Powderbooking application. 


## How to use
This application requires a postgres database to function.

#### Python
1. Run your own postgres locally, update default values in the `config.py` file.
2. Create a virtual environment and install the requirements:    
`pip3 install -r requirements.txt`
3. Run the application:    
`python3 app.py [API]`
   - `[API]` as either `forecast` or `weather`

#### Docker-compose
1. Create an `.env` file from the `template.env` file with your information.
2. Run the docker-compose file from the compose folder:    
`sudo docker-compose up -d --build`
   - you can change the command of the dockerfile to either `forecast` or `weather`
3. Verify output from the app with:    
`sudo docker-compose logs app`
4. Drop the docker-compose services with:     
`sudo docker-compose down`
#### Helm chart
to be added.

## Used APIs

These are the APIs that I am getting my data from.

**NOTE:** 
All information with regards to the APIs is last retrieved and verified in summer 2018.

#### Open Weather Map

**Pricing:**   
free (up to 60/min calls)   
**url:** https://openweathermap.org/price    
**documentation:** https://openweathermap.org/current    
**Notes:**   
Includes rain and snow fall from last 3 hours (in mm)   
Updates every 2 hours

#### Weather unlocked

**Pricing:**    
7 days: free (up to 75/min calls)
**url:** https://developer.worldweatheronline.com/api/pricing.aspx    
**documentation:** https://developer.weatherunlocked.com/documentation/localweather/forecast      
**sample:** https://developer.worldweatheronline.com/api/docs/ski_sample.xml  
**Notes:**   
Could request multiple times per day    
3-hourly segment   
Updates every hour


## Unused APIs

These are APIs I have looked at, but currently not using.

#### World Weather Online

**Pricing:**   
7 days (5000/day): 28.73     
10 days (5000/day): 35.93   
14 days (5000/day): 43.13    
**url:** https://developer.worldweatheronline.com/api/pricing.aspx    
**documentation:** https://developer.worldweatheronline.com/api/docs/local-city-town-weather-api.aspx    
**Notes:**   
Would request it once per day       
Daily snowFall_mm
Hourly precipMM and chanceofrain -snow -frost -windy -sunshine -fog   

#### World Weather Online

**Pricing:**    
3 days (5000/day): 12.09   
5 days (5000/day): 20.19   
7 days (5000/day): 26.94   
**url:** https://developer.worldweatheronline.com/api/pricing.aspx    
**documentation:** https://developer.worldweatheronline.com/api/docs/ski-weather-api.aspx   
**sample:** https://developer.worldweatheronline.com/api/docs/ski_sample.xml  
**Notes:**   
Would request it once per day    
Hourly segment   
Includes top / mid / bottom   