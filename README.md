# The Orb of Disquiet
An emotionally sensitive Hue bulb. Sentiment models predict sentiment on incoming data (speech or text) and change Hue color accordingly.  

### Run prediction server
This will load the jar model and listen for incoming text. Jar is used instead of my own model because DR models are superior, but DR predictions via the API are too slow for this use case. To run the server, run the command below. The default port is 9000.  

```
java -jar prediction_server.jar -m <model jar filename>.jar -p <port>
```  

Rotten Tomatoes sentiment (regression GLM blender - values 0 - 5): `5a207fa7eeb38c357a32689f.jar`  
Rotten Tomatoes sentiment (classification): `<best-RT-classification-model.jar>`  
Reddit sentiment: `<best-reddit-model.jar>`  
Hub model (classification GLM blender - with probabilities between 0 - 1): `5a26b9a790db4f1c808e4b93.jar`

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
This predicts sentiment on incoming Slack messages. Posts sentiment score in a thread and adds an emoji to the evaluated message. :vom: :cold_sweat: :neutral_face: :heart_eyes: :aheaga:  

In `slack-bot/`, simply run:  

```
rtmbot
```
