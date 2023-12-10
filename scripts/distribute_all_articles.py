import json
import random
from pathlib import Path 

DATASET_NAME = 'movie_data.json'

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
        if i == n-1:
            out.append(dataset[i*k:])
        else:
            out.append(dataset[i*k:(i+1)*k])
    return out

def main():
    movie_dataset_filepath = Path(__file__).parent/'data'/DATASET_NAME
    movie_data = json.loads(load_movie_data(movie_dataset_filepath))
    random.shuffle(movie_data)
    sublists = split_into_sublists(4, movie_data)
    for index, sublist in enumerate(sublists):
        write_to_file(f'all_articles_part{index+1}.tsv', sublist)

if __name__ == "__main__":
    main()