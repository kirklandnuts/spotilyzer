import pandas as pd
import sys

GENRES = ['Pop', 'Electronic/Dance', 'Hip-Hop', 'Rock', 'Indie', 'R&B', 'Metal', 'Soul', 'Romance', 'Jazz']


if __name__ == "__main__":
    DATA_PATH = sys.argv[1]
    DATA_OUTPATH = DATA_PATH[:-4] + '_cleaned.csv'

    print('Data path: {}'.format(DATA_PATH))
    print('==== Loading data')
    df = pd.read_csv(DATA_PATH)

    # Getting rid of songs from non-genre categories (chill, party, etc)
    print('==== Excluding songs belonging to non-genre categories')
    df = df[df.category.isin(GENRES)]

    # Getting rid of duplicates
    print('==== Dropping duplicate songs')
    df = df.drop_duplicates(df.columns.difference(['category']), keep = False)

    df.to_csv(DATA_OUTPATH)
    print('==== Clean data outputted to \"{}\"'.format(DATA_OUTPATH))
