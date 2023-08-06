import pandas as pd
import requests
import pickle


def get_finlab_data(dataset):
    url = f"https://github.com/twfxjjbw/stockinfo/raw/main/{dataset}.bin"
    r = requests.get(url)
    return pickle.loads(r.content)


if __name__ == "__main__":
    df = get_finlab_data("price:收盤價")
    print(df)
