import urllib.request
import json
import os
import ssl

# test model


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(
        ssl, '_create_unverified_context', None
    ):
        ssl._create_default_https_context = ssl._create_unverified_context


# this line is needed if you use self-signed certificate in
# your scoring service.
allowSelfSignedHttps(True)

# Request data goes here
data = {
    "input_data": [
        [
            0, 171, 80, 34, 23, 43.50972593, 1.213191354, 21
        ],
        [
            6, 73, 61, 35, 24, 18.74367404, 1.074147566, 75
        ],
        [
            4, 115, 50, 29, 243, 34.69215364, 0.741159926, 59
        ]
    ]
}

body = str.encode(json.dumps(data))

url = 'https://oediabetes2.brazilsouth.inference.ml.azure.com/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = 'OQyGBcw2GpPIYxRW3WomgxUg1YgRdsgk'
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")

# The azureml-model-deployment header will force the request to go to
# a specific deployment.
# Remove this header to have the request observe the endpoint traffic rules
headers = {'Content-Type': 'application/json', 'Authorization': (
    'Bearer ' + api_key), 'azureml-model-deployment': 'deployeddiabetes2'}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp,
    # which areuseful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
