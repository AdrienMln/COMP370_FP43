import json
from matplotlib import pyplot as plt
import pandas as pd 

def BackLashtoPositive():
    

    movie_name = ['Priscilla', 'Saltburn', 'THG', 'Thanksgiving', 'The Holdovers', 'The Marvels']
    ratio = [1,1,2,8/17,3/7,20/2]

    plt.bar(movie_name, ratio)
    plt.title('Backlash to Positive Review ratio per movie')
    plt.xlabel('Movie')
    plt.ylabel('ratio')
    plt.xticks(rotation=45, fontsize=8)
    plt.show
    plt.savefig("example.png") 
    

def main():
    BackLashtoPositive()

if __name__ == "__main__":
    main()

