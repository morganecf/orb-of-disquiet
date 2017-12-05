# The Orb of Disquiet
An emotionally sensitive Hue bulb.

### Run prediction server
This will load the jar model and listen for incoming text. Jar is used instead of my own model because DR models are superior, but DR predictions via the API are too slow for this use case. Run the server with:  

```
java -jar prediction_server.jar -m <model jar filename>.jar
```  

Rotten Tomatoes sentiment (regression GLM blender): `5a207fa7eeb38c357a32689f.jar`  
Rotten Tomatoes sentiment (classification): `<best-RT-classification-model.jar>`  
Reddit sentiment: `<best-reddit-model.jar>`  
Hub models: `<best-hub-model.jar>`

### Simple Python client
This fetches sentiment predictions on command line text input  
```
python simple_prediction_client.py
```  

### Slack client
This fetches sentiment predictions on incoming Slack messages  
```
python slack_prediction_client.py
```  

### Simple speech recognition  
Predicts sentiment on incoming speech reognized by the Google Speech API.  
```
python simple_voice_predictions.py
```  

### Slack --> Hue
This fetches sentiment predictions on incoming Slack messages and changes Hue accordingly.  
```
python slack_to_hue.py
```  

### Run responsive Slack Python client
This fetches sentiment predictions on incoming Slack messages and sends them back to the channel  
TODO: probably need rtmbot 
