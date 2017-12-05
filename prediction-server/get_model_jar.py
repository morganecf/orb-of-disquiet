import sys
import datarobot as dr

'''
Download the model jar from DR. Make sure codegen FF is enabled.
'''

model_id = sys.argv[1]
project_id = sys.argv[2]
token = sys.argv[3]

dr.Client(token=token, endpoint='https://app.datarobot.com/api/v2')
model = dr.Model.get(project=project_id, model_id=model_id)
filename = '{}.jar'.format(model.id)
model.download_scoring_code(filename)
