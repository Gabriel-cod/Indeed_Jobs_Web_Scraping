# Indeed Jobs Web Scraping
### Target
#### Develop a Web Scraper to get jobs on Indeed.com, trough user keywords, and load the information into an SQL database.
### Development Steps
#### Initially, the structure on which the search for vacancies would be based was developed. For this process, I used a ready-made url that, when accessed, the user would already be directed to the page where job vacancies for the profession mentioned in the web address are presented, thus defining a model to be changed only for the profession indicated in the url. With this model url, it was possible to use a dynamic variable to add the profession collected and processed, when starting the program.
#### After this process, I developed a search system using Scrapy's own mechanisms such as Request, used to make requests to the informed web address. From this definition, a function is indicated to process and store the data. In this second definition, I created a search system using XPATH, which we identified as if it were the identity of each HTML element on the website. Based on this identity of the elements, I located an XPATH common to each extraction item of interest.
#### Finally, I structured a logic to perform the previous process on all available search pages and developed a simple graphical interface in the app.py file to obtain the necessary data for the search.
### The Error
#### With the search and data collection system developed, I carried out tests and found a persistent error that prevented data extraction and storage. From there, I did some research and after some time concluded that the error found was caused by a block on the Indeed website. This blocking was applied to the proxy on the computer used and if the app was run on another device, this blocking would be done in the same way.
#### With that in mind, I found a solution to avoid this block by changing the search proxy used in the extraction. To do this, there is a web service named ScrapeOPS that allows us to change our browser's proxy securely at each execution, through an API Key. To implement this protection, I used the settings located in the vagas_indeed_spider.py file which is in the following path : vagas_scraper/vagas_scraper/spiders/vagas_indeed_spider.py.
#### Within this file, we can find a variable called "custom_settings" where some settings are defined to be applied to the developed service. In this variable, it is possible to find a value with the name "SCRAPEOPS_API_KEY", which we must insert our API Key obtained after logging into the ScrapeOPS website, for the program to work correctly.
## User Guide
### Which file to execute?
#### The main file that must be executed is app.py. When executing this file, a graphical interface will open in which you will be asked for the name of the profession that must be searched to find jobs.
### Mandatory Settings
#### For the extraction process to work correctly, it is necessary to change the value of the variable "SCRAPEOPS_API_KEY" which is inside another variable called "custom_settings" in the file with a path defined as vacancies_scraper/vagas_scraper/spiders/vagas_indeed_spider.py.
