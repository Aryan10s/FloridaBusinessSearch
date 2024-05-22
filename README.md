Basic Architecture:
 
This Project consists of a Frontend(made in Reactjs) and a Backend(made in Python) with Postgres as the Database. The User interacts with the Web UI. The Web UI is connected through backend via the FASTAPI framework of Python. The Backend also connects with PostgreSQL database in order to store and retrieve data.


FrontEnd:

The Frontend is made in ReactJs framework. It uses Bootstrap, Ant_Design and Material UI in order to make the Web UI as interactive as possible. It consists of 2 routes, login and operations. Login is also connected through the Backend via FASTAPI, and you can find the credentials in backend folder in config/app_configuration.yaml. On Successful login, you will be navigated to operations routes. There you can find a textbox for writing your Queries. Also in the Navbar you will find the option to see the list of Available documents, and on click of any of those documents you will get the complete details of it,

Steps to run the Frontend:

1) Open Terminal, move inside Frontend Directory, run command "npm i".
2) Then Move inside Business-search Directory, run command "npm i".
3) After the dependencies are installed run command "npm run dev", to start the development server.
4) For running in deployement server, first run command "npm run build".
5) Then run command, "serve s dist -l 3000"

BackEnd:

The Backend is made in Python FASTAPI framework. For Web Scraping it uses a python library called BeautifulSoup. It consists of 4 APIs for login, web page crawling, retieving all crawled web pages, and retrieving the data of a selected crawled page, all present in the main.py module. All the helping functions of the main APIs can be found in the utils.py module. The api_router file contains the mounting of all the routers. generate_logs module will be helpful when running the microservice on nohup for debugging purposes. The schema_classes module, contains the format of the data needed to hit the API call successfully. The connection string for PostgreSQL needs to be taken from the .env file which the user needs to create indicating their SQL Databse server connection. All the functions and APIs, wherever required is backed by extensive Exception Handling. 

Steps to run the Backend:
1) Open Terminal, move inside backend Directory, run the command "pip install -r requirements.txt"
2) For Debugging purposes, run the command "uvicorn api_router:app --host 0.0.0.0 --port 8000"
3) For Stable Deploymenty, run the command "nohup uvicorn api_router:app --host 0.0.0.0 --port 8000 &"

Note: All the Deployments command are given to deploy the project on localhost only. One more thing I could have done in frontend for better code quality/effeciency was put API's domain name in config, but due to time constraints, I wasn't able to do it. 
