import pandas as pd
import numpy as np

print('Reading files...')
twitter = pd.read_csv('../twitter-sentiment140.csv', encoding='latin-1').text
hub = pd.read_csv('hub_comments.tsv', delimiter='\t').text

n = hub.shape[0]
num_twitter = twitter.shape[0]

print('Taking twitter sample...')
twitter_sample = pd.DataFrame(columns=['label', 'text'])
twitter_sample.text = twitter.sample(frac=n / num_twitter)
twitter_sample.label = np.zeros(n)

print('Merging...')
data = pd.DataFrame(columns=['label', 'text'])
data.text = hub
data.label = np.ones(n)

out = data.append(twitter_sample)

print('Saving...')
out.to_csv('twitter_vs_hub.csv')
