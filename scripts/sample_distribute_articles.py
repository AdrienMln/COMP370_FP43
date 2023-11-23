import random
import json
OPEN_CODING_DATASET_FILENAME = 'open_coding_dataset.tsv'
DATASET_NAME = 'movie_articles.tsv'
MOVIE_DATA_FILENAME = 'movie_data.json'

def load_movie_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read()
        return json.loads(content)
    
def write_to_file(output_fname, data):
    with open(output_fname, 'w', encoding='utf-8') as f:
        f.write('Article Title\tDescription\tCoding\n')
        for article in data:
            f.write(f"{article['title']}\t{article['description']}\t\s\n")

def split_into_sublists(n, dataset):
    k = len(dataset) // n
    out = []
    for i in range(n):
        out.append(dataset[i*k:(i+1)*k])
    return out
    
movie_data = json.loads(load_movie_data(MOVIE_DATA_FILENAME))
with open('open_coding.json', 'w', encoding='utf-8') as f:
    json.dump(movie_data, f)
open_coding_dataset = random.sample(movie_data, k = 200)

write_to_file(DATASET_NAME, movie_data)
write_to_file(OPEN_CODING_DATASET_FILENAME, open_coding_dataset)

open_coding_sublists = split_into_sublists(4, open_coding_dataset)

for i, sublist in enumerate(open_coding_sublists):
    print(len(sublist))
    write_to_file(f'open_coding{i+1}.tsv', sublist)