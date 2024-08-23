# Chat with a website

Use this open-source template to create a database of any website and query the results using gpt-3.5-turbo (or any model you have access to)
*Not included is a .env file which you will need to put your chatGPT API key in the format of: API_KEY = <your api key>

# Setup

Setup your virtual environment for python and import the required libraries (if you don't already have them): 
```
pip install <requests, json, os, MongoClient **, chromadb **, json, beautifulsoup4 **, urllib.parse, urljoin, urlparse, urldefrag, time>
```

** - important for this project

After Installing, create .env file with your API key (refer to line 4)


1. Run gpt-test.py to make sure your API key is valid

2. Edit and run
         docker compose -f docker-compose.yml
  to setup your MongoDB container

3. Edit web-scapper.py starting at line 64 with your own parameters:
```
base_url = 'https://www.toronto.ca/'
max_depth = 5  # Set the desired recursion depth
mongo_uri = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
mongo_db = 'web_scraper'  # Replace with your MongoDB database name
```
4. Run web-scapper.py and let it populate your MongoDB database

5. Edit mongoDB connection details in to_croma.py and run (optionally you can change data{} dict to better suit your needs)

6. Ask a question!

![image](https://github.com/user-attachments/assets/617a9ad5-c89a-47fd-9355-03b4ba121f63)
![image](https://github.com/user-attachments/assets/b406c840-0690-45d5-9836-559647124c19)


If you have any questions, contact me at kshpurov@gmail.com!


