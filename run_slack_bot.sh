java -jar prediction-server/prediction_server.jar -m prediction-server/5a207fa7eeb38c357a32689f.jar -p 9000 &
java -jar prediction-server/prediction_server.jar -m prediction-server/5a26b9a790db4f1c808e4b93.jar -p 9090 &

cd slack-bot/
rtmbot

# java -jar prediction-server/prediction_server.jar -m prediction-server/5a207fa7eeb38c357a32689f.jar -p 9000 &
# until java -jar prediction-server/prediction_server.jar -m prediction-server/5a26b9a790db4f1c808e4b93.jar -p 9090 | grep -m 1 "Waiting for connection..."; do : ; done
# echo "Starting slack bot"
# prediction-server/rtmbot

