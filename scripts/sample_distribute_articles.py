import random
import json
from pathlib import Path
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
    
def main():
    movie_data_path = Path(__file__).parent.parent/'data'/MOVIE_DATA_FILENAME
    movie_data = json.loads(load_movie_data(movie_data_path))
    with open('open_coding.json', 'w', encoding='utf-8') as f:
        json.dump(movie_data, f)
    open_coding_dataset = random.sample(movie_data, k = 200)

    movie_articles_tsv_path = Path(__file__).parent.parent/'data'/DATASET_NAME
    write_to_file(movie_articles_tsv_path, movie_data)
    movie_data_json_path = Path(__file__).parent.parent/'data'/OPEN_CODING_DATASET_FILENAME
    write_to_file(movie_data_json_path, open_coding_dataset)

    open_coding_sublists = split_into_sublists(4, open_coding_dataset)

    for i, sublist in enumerate(open_coding_sublists):
        print(len(sublist))
        write_to_file(f'open_coding{i+1}.tsv', sublist)

if __name__ == '__main__':
    main()