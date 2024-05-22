from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from utils import *
from schema_classes import *
from generate_log import *
import json
config_path = os.getcwd()
app_configurations = yaml.safe_load(
    open(config_path + "/config/app_configurations.yaml"))

second_level_html = app_configurations['second_level_html']

second_level = config_path + second_level_html

user = app_configurations['user']
password = app_configurations['password']


router = APIRouter(
    prefix="/api",
    tags=["/api"]
)


@router.post("/initiate-crawling", description="starts gathering data and stores it in a Database.")
def initiateCrawling(config: CrawlingConfig):
    try:
        query = config.query
        main_url, exec_status = getURL(query)
        if exec_status==True:
            main_file = second_level
            second_level_status = save_html_from_url(main_url,main_file)
            if second_level_status==True:
                db_level_status = insert_into_db(main_file,query)
                if db_level_status==True:
                    result = {'status': 'success',
                      'message': 'Data Scraped Succesfully.', 'data':[]}
                    return JSONResponse(status_code=status.HTTP_200_OK, content=result)
                else:
                    result = {'status': "failed",
                  "message": "Something went wrong. Please try again later.", "data": []}
                    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
            else:
                result = {'status': "failed",
                  "message": "Something went wrong. Please try again later.", "data": []}
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
        else:
            result = {'status': "failed",
                  "message": "Something went wrong. Please try again later.", "data": []}
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
    except Exception as e:
        result = {'status': "failed",
                  "message": "Something went wrong. Please try again later." + " " + str(e), "data": []}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=result)

@router.post("/get-data", description="API for getting the data of a particular business")
def getData(config: GetDataConfig):
    try:
        business_name = config.business_name
        data,exec_status = getFromDB(business_name)
        if exec_status==True:
            result = {'status': 'success',
                        'message': 'Data Fetched Succesfully.', 'data':data}
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
        else:
            result = {'status': "failed",
                  "message": "Something went wrong. Please try again later.", "data": []}
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
    except Exception as e:
        result = {'status': "failed",
                  "message": "Something went wrong. Please try again later." + " " + str(e), "data": []}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
    
@router.post("/login", description="API to verify user login credentials")
def login(config : UserLoginConfig):
    try:
        user_name = config.user_name
        user_password = config.password
        if user_name==user and user_password==password:
            result = {'status': 'success',
                      'message': 'Logged In Succesfully.', 'data':[]}
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
        else:
            result = {'status': "failed",
                  "message": "Wrong Credentials!.", "data": []}
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=result)
    
    except Exception as e:
        result = {'status': "failed",
                  "message": "Something went wrong. Please try again later." + " " + str(e), "data": []}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)

@router.get("/get-business-names",description="API to get all business names")
def getNames():
    try:
        data, exec_status = getBusinessNames()
        if exec_status==True:
            result = {'status': 'success',
                      'message': 'Business Names Fetched Succesfully.', 'data':data}
            return JSONResponse(status_code=status.HTTP_200_OK, content=result)
        else:
            result = {'status': "failed",
                  "message": "Something went wrong. Please try again later.", "data": []}
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
    except Exception as e:
        result = {'status': "failed",
                  "message": "Something went wrong. Please try again later." + " " + str(e), "data": []}
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=result)
