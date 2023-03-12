import io
import json
import typing
import requests
from config import settings
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time

HUGGING_FACE_API_TOKEN = settings().hugging_face_token
HUGGING_FACE_API = settings().hugging_face_api
EASY_OCR_API = settings().easy_ocr_api
EASY_OCR_TOKEN = settings().easy_ocr_token

def image_recognition(file: typing.ByteString):
    potential_objects = []
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}
    response = requests.request("POST", HUGGING_FACE_API, headers=headers, data=file)
    decoded_result = json.loads(response.content.decode("utf-8"))
    for row in decoded_result:
        potential_objects.append({'label': row['label'], 'score': row['score']})

    return potential_objects

def text_extraction(file: typing.ByteString):
    headers = {"username": 'szuhan', 'apikey': EASY_OCR_TOKEN}
    text_lines = []
    try:    
        response = requests.post(EASY_OCR_API, headers=headers, files={"file": file}).json()
    except Exception as e:
        return {"error": response['error']}

    for row in response['result']:
        text_lines.append({"label": row['text'], "score": row['score']})

    return text_lines

def mcft_ocr(file: typing.ByteString):
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "76e2b9cfc7b3469f8682319340416672"
    endpoint = "https://tribes-mvp.cognitiveservices.azure.com/"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    '''
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriing style text (not shown).
    '''
    text_lines = []

    # Call API with URL and raw response (allows you to get the operation location)
    image = io.BytesIO(file)

    read_response = computervision_client.read_in_stream(
            image=image,
            mode="Printed",
            raw=True
        )

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]
    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                for row in line.words:
                    text_lines.append({'label': row.text, 'score': row.confidence})
    return text_lines



def mcft_image_categorisation(file):
    '''
    Authenticate
    Authenticates your credentials and creates a client.
    '''
    subscription_key = "76e2b9cfc7b3469f8682319340416672"
    endpoint = "https://tribes-mvp.cognitiveservices.azure.com/"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    '''
    END - Authenticate
    '''

    '''
    OCR: Read File using the Read API, extract text - remote
    This example will extract text in an image, then print results, line by line.
    This API call can also extract handwriing style text (not shown).
    '''
    text_lines = []

    # Call API with URL and raw response (allows you to get the operation location)
    image = io.BytesIO(file)
    try:
        read_response = computervision_client.tag_image_in_stream(
            image=image,
            language='en', 
        )
    except Exception as e:
        raise e

    # Print the detected text, line by line
    if len(read_response.tags) > 0:
        for text_result in read_response.tags:
            text_lines.append({'label': text_result.name, 'score': text_result.confidence})
                
    return text_lines