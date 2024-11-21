import base64
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import zlib

from adjustText import adjust_text
from io import BytesIO, StringIO


def make_plot(sequence, spectrum_tsv, adjust):
    matplotlib.use('Agg')

    # uncompress spectrum
    spectrum_tsv = base64.b64decode(spectrum_tsv)
    spectrum_tsv = zlib.decompress(spectrum_tsv).decode('utf-8')

    # remove escape characters
    spectrum_tsv = spectrum_tsv.replace("\\n", "\n")
    df = pd.read_csv(StringIO(spectrum_tsv))

    # Create a new column 'color' based on 'ion_name'
    def get_color(ion_name):
        if pd.isna(ion_name):
            return '#a1a1a1'
        elif ion_name.startswith(('a', 'b', 'c', 'x', 'y', 'z')):
            return 'red' if ion_name.startswith(('a', 'b', 'c')) else 'blue'
        else:
            return '#a1a1a1'

    df['color'] = df['ion_name'].apply(get_color)
    df = df.sort_values(by=['color'], ascending=True)

    plt.figure(figsize=(12, 8))

    bar_width = 2

    # Plot the bar plot
    plt.bar(df['mz'], df['intensity'], color=df['color'], width=bar_width)

    texts = []
    for mz, intensity, ion_name in zip(df['mz'], df['intensity'], df['ion_name']):
        if isinstance(ion_name, str) and ion_name[0] in ['a', 'b', 'c', 'x', 'y', 'z'] and intensity > 0.01:
            texts.append(plt.text(mz, intensity, ion_name, size=6))
    if adjust:
        adjust_text(texts, arrowprops=dict(arrowstyle="-", color='k', lw=0.5))

    plt.xlabel('m/z')
    plt.ylabel('intensity')
    plt.title(sequence)
    plt.grid(which='major', axis='y', zorder=0)

    # Convert the plot to a base64-encoded image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode()

    return plot_data
