import pandas as pd
import argparse
from sklearn.model_selection import train_test_split


def split_data(df, tr_size):
    '''
    PURPOSE
    Splits song data into train and test sets, maintaining category distribution
    INPUT
    df          DataFrame, data to be split
    tr_size     Double, designates portion of data to be used as train data
    OUTPUT
    tr          DataFrame, training data
    te          DataFrame, testing data
    '''

    genres = df.groupby(['category'])
    genre_names = list(genres.groups.keys())

    tr_list = []
    te_list = []

    for genre in genre_names:
        gdf = genres.get_group(genre)
        tr, te = train_test_split(gdf, train_size = tr_size)
        # tr = upsample(tr, n_want)
        tr_list.append(tr)
        te_list.append(te)

    tr = pd.concat(tr_list)
    te = pd.concat(te_list)

    return tr, te


def frequency_by_field(dataset, data_name, field):
	'''
	PURPOSE
	For given dataset field, provide frequency distribution
	INPUT
	dataset    DataFrame for analysis
	dataname   str, a name to output to denote the dataset
	field      str, field to breakdown
	OUTPUT
	prints absolute and proportional breakdown of designated value for designated dataset
	'''

	count = dataset[field].value_counts()
	proportion = dataset[field].value_counts()/len(dataset)
	print('==== ' + data_name + ' ' + field.upper() + ' BREAKDOWN:')
	df = pd.DataFrame({'COUNT':count, 'PROPORTION':proportion})
	print(df, '\n')


def split_stats(origin_data, compare_data, origin_data_name):
	'''
	PURPOSE
	Report statistics on data split
	INPUT
	origin_data       DataFrame, original (pre-split) df
	compare_data      DataFrame, comparison df
	origin_data_name  str, dataset name (example='RAW DATA')
	OUTPUT
	printed summary of results
	'''

	if origin_data_name == 'RAW DATA':
		print(origin_data_name, '|', str(len(origin_data)), 'records')
	else:
		percentage = str(len(origin_data)/len(compare_data)*100) + '%'
		print(origin_data_name, '|', str(len(origin_data)), 'records |', percentage)


def dataset_stats(raw_data, train_data, test_data):
    '''
    PURPOSE
    Wrapper function around split_stats to report statistics on multiple dataset fields
    INPUT
    raw_data    DataFrame, original (pre-split) df
    train_data  DataFrame, train df
    test_data   DataFrame, test df
    OUTPUT
    printed summary of results
    '''

    frequency_by_field(raw_data, 'RAW DATA', 'category')
    frequency_by_field(train_data, 'TRAIN DATA', 'category')
    frequency_by_field(test_data, 'TEST DATA', 'category')
    split_stats(raw_data, raw_data, 'RAW DATA')
    split_stats(train_data, raw_data, 'TRAIN DATA')
    split_stats(test_data, raw_data, 'TEST DATA')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='split data into test and train',)
    parser.add_argument('raw_data')
    parser.add_argument('-f', '--frac_train', default=0.8,
                    help = 'designate how much of the data is to be used as train data')

    # read args
    args = parser.parse_args()
    data_path = args.raw_data
    frac_train = float(args.frac_train)

    # output args
    print('data_path={}'.format(data_path))
    print('frac_train={}'.format(frac_train))

    # construct output filepaths
    tr_outpath = data_path[:-4] + '_tr.csv'
    te_outpath = data_path[:-4] + '_te.csv'

    # load data
    raw_data = pd.read_csv(data_path)

    # split data
    tr, te = split_data(raw_data, frac_train)

    # output data
    te.to_csv(te_outpath, index = False)
    tr.to_csv(tr_outpath, index = False)

    # output stats
    dataset_stats(raw_data, tr, te)

    # output paths
    print('Training data outputted to {}'.format(tr_outpath))
    print('Testing data outputted to {}'.format(te_outpath))
