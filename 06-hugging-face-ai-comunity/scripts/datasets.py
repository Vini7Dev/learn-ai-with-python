
from datasets import load_dataset

def execute():
    dataset_stream = load_dataset('imdb', streaming=True)

    for row in dataset_stream:
        print(row)
        input()

    '''
    # dataset = load_dataset('imdb')
    print(dataset)
    input()
    train_dataset = dataset['train']
    print(train_dataset[7])
    input()
    print(train_dataset['label'])
    input()
    print(train_dataset[7]['label'])
    '''

    '''
    # dataset = load_dataset('imdb')
    train_dataset = dataset['train']
    df_dataset = train_dataset.to_pandas()
    print(df_dataset)
    '''
