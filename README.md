# The Orb of Disquiet
An emotionally sensitive Hue bulb.

### Run prediction server

This will load the jar model and listen for incoming text.

Sentiment models: `java jar -m 5a207fa7eeb38c357a32689f.jar`

Hub models: `java jar -m <best-hub-model.jar>`

### Run simple Python client
This fetches sentiment predictions on command line text input

`python2.7 simple_prediction_client.py`

### Run Slack client
This fetches sentiment predictions on incoming Slack messages

`python2.7 slack_prediction_client.py`

### Run Slack --> Hue client
This fetches sentiment predictions on incoming Slack messages and changes Hue accordingly.

`python2.7 slack_sentiment_to_hue.py`

### Run responsive Slack Python client
This fetches sentiment predictions on incoming Slack messages and sends them back to the channel

TODO: probably need rtmbot 
