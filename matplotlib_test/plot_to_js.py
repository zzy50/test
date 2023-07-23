import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame as DF

def draw_lineplot(df1: DF, df2: DF, df3: DF, year_list: list, fixed_ylim: int, title_txt: str, save_path: str) -> None:

    fig, ax = plt.subplots(figsize=(20, 7))
    fig.set_facecolor('white')

    ax.plot(df1["TIME"], df1["TRAFFIC"], marker='o', label=year_list[0], alpha=0.3, color="grey", linestyle='--')
    max_value = df1["TRAFFIC"].max()
    for x, y in zip(ax.get_xticks(), df1["TRAFFIC"].values):
        ax.text(x=x, y=y+(max_value*0.01), s=y, color='grey', size=15, alpha=0.35)

    ax.plot(df2["TIME"], df2["TRAFFIC"], marker='o', label=year_list[1], alpha=0.7, color="orange", linestyle='--') 
    max_value = df2["TRAFFIC"].max()
    for x, y in zip(ax.get_xticks(), df2["TRAFFIC"].values):
        ax.text(x=x, y=y+(max_value*0.01), s=y, color='orange', size=15, alpha=0.35)

    ax.plot(df3["TIME"], df3["TRAFFIC"], marker='o', label=year_list[2], color='red') 
    max_value = df3["TRAFFIC"].max()
    for x, y in zip(ax.get_xticks(), df3["TRAFFIC"].values):
        ax.text(x=x, y=y+(max_value*0.01), s=y, color='red', size=15, alpha=1)

    ax.legend(loc=[0.90,0.82], fontsize=18)
    ax.set_xlabel("시간", fontsize=19)
    ax.set_ylabel("교통량", fontsize=19)
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fixed_ylim: ax.set_ylim(top=fixed_ylim)

    plt.sca(ax)
    plt.yticks(fontsize=20)
    plt.xticks(np.arange(24), fontsize=20)

    plt.title(title_txt, fontsize=25, pad=20)
    plt.tight_layout()
    plt.grid(True, linestyle='--')
    plt.ioff()
    plt.savefig(save_path)
    # print(f"Output >>> {save_path}")
    plt.close(fig)



def foo(df3):
    fig, ax = plt.subplots(figsize=(20, 7))
    fig.set_facecolor('white')
    ax.plot(df3["TIME"], df3["TRAFFIC"], marker='o', color='red') 
    max_value = df3["TRAFFIC"].max()
    for x, y in zip(ax.get_xticks(), df3["TRAFFIC"].values):
        ax.text(x=x, y=y+(max_value*0.01), s=y, color='red', size=15, alpha=1)

    ax.legend(loc=[0.90,0.82], fontsize=18)
    ax.set_xlabel("시간", fontsize=19)
    ax.set_ylabel("교통량", fontsize=19)
    ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    if fixed_ylim: ax.set_ylim(top=fixed_ylim)

    plt.sca(ax)
    plt.yticks(fontsize=20)
    plt.xticks(np.arange(24), fontsize=20)

    plt.title(title_txt, fontsize=25, pad=20)
    plt.tight_layout()
    plt.grid(True, linestyle='--')
    plt.ioff()
    plt.savefig(save_path)
    # print(f"Output >>> {save_path}")
    plt.close(fig)