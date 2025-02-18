from pathlib import Path
from datasets import Audio, load_dataset
import matplotlib.pyplot as plt
import soundfile
import IPython

def execute():
    # Loading data set
    dataset = load_dataset('ashraq/esc50')

    data = dataset['train']

    # Show sound bar graph
    idx_row = 1
    row = data[idx_row]
    plt.subplots(figsize=(30, 4))
    plt.plot(row['audio']['array'])
    plt.suptitle(row['category'])
    ## plt.show()

    # Saving audio files
    output_folder = Path('assets') / 'audios'
    output_folder.mkdir(exist_ok=True, parents=True)

    first_rows = data.select(range(10))

    for i, row in enumerate(first_rows):
        sound_object = row['category']
        sound_data = row['audio']['array']
        sampling_rate = row['audio']['sampling_rate']
        output_file = output_folder / f'{i}_{sound_object}.wav'

        # Save as file
        soundfile.write(
            file=output_file,
            data=sound_data,
            samplerate=sampling_rate,
        )
        # IPython.display.Audio(data=sound_data, rate=sampling_rate)

    # Adjuste different sampling rates
    sampling_rate = data[0]['audio']['sampling_rate']
    print(f'"Sampling Rate" Original: {sampling_rate}')

    data = data.cast_column('audio', Audio(sampling_rate=48000))
    new_sampling_rate = data[0]['audio']['sampling_rate']
    print(f'Novo "Sampling Rate": {new_sampling_rate}')
