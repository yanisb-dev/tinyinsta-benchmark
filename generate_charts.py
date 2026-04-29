import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

def parse_time(val):
    val = str(val).strip()
    m = re.match(r'^([\d.]+)\s*ms$', val)
    if m:
        return float(m.group(1))
    try:
        return float(val)
    except ValueError:
        return np.nan

def make_barplot(csv_path, png_path, xlabel, title):
    df = pd.read_csv(csv_path)
    df['AVG_TIME_MS'] = df['AVG_TIME'].apply(parse_time)
    grouped = df.groupby('PARAM')['AVG_TIME_MS'].agg(['mean', 'std']).reset_index()
    grouped = grouped.sort_values('PARAM')
    grouped['mean_s'] = grouped['mean'] / 1000
    grouped['std_s'] = grouped['std'] / 1000

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(grouped))
    bars = ax.bar(x, grouped['mean_s'], yerr=grouped['std_s'],
                  capsize=5, color='#4285F4', edgecolor='black', linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(grouped['PARAM'].astype(int))
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Temps moyen par requête (s)')
    ax.set_title(title)
    ax.grid(axis='y', alpha=0.3)
    for bar, mean_val in zip(bars, grouped['mean_s']):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'{mean_val:.2f}s', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(png_path, dpi=150)
    print(f"[OK] {png_path}")
    plt.close()

if __name__ == '__main__':
    make_barplot(
        'out/conc.csv', 'out/conc.png',
        "Nombre d'utilisateurs concurrents",
        "Temps moyen par requête selon la concurrence"
    )
    print("conc.png généré !")

make_barplot(
    'out/fanout.csv', 'out/fanout.png',
    "Nombre de followees",
    "Temps moyen par requête selon le fanout"
)
