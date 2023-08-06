"""Align two texts."""
from pathlib import Path
import numpy as np
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import joblib

from absl import app, flags
from logzero import logger

# from tinybee.cmat2tset import cmat2tset
from tinybee.cos_matrix2 import cos_matrix2

# from tinybee.lowess_pairs import lowess_pairs
# from tinybee.gen_row_align import gen_row_align
# from tinybee.interpolate_pset import interpolate_pset
# from tinybee.gen_iset import gen_iset

from tinybee.find_pairs import find_pairs
from tinybee.gen_aset import gen_aset
from tinybee.align_texts import align_texts

from tinybee.embed_text import embed_text

FLAGS = flags.FLAGS
flags.DEFINE_boolean("debug", False, "print debug messages.", short_name="d")


def main(argv):
    """Run main.

    pset1 = find_pairs(cmat)
        cmat2tset
        validity check based on iset
            iset = gen_iset(cmat, verbose=verbose)
                lowess_pairs or dbscan_pairs
                    yhat = lowess_pairs(cmat)
                pset = gen_row_align(yhat, src_len, tgt_len)
                interpolate_pset
    aset = gen_aset(pset1, src_len, tgt_len)
    texts = align_texts(aset, src_text, tgt_text)

    """
    # logger.info(__file__)
    logger.info(argv[1:])

    # logger.debug("debug: %s", argv[1:])

    # zh = joblib.load(r"data/shzh600.lzma")
    # en = joblib.load(r"data/shen600.lzma")
    # cmat = cos_matrix2(en, zh[:500])

    # hlm-ch1 para corr?

    # text en: 4566141, zh 716377
    # para en: 24506 zh  2767
    # hlm_zh = joblib.load("data/hlm_zh.lzma")
    # hlm_en = joblib.load("data/hlm_en.lzma")
    # hlmpara_en = hlm_en.splitlines()[:160]
    # hlmpara_zh = hlm_zh.splitlines()[:80]

    hlm_emb_en_file = "data/hlm_emb_en160.lzma"
    hlm_emb_zh_file = "data/hlm_emb_zh80.lzma"

    # hlm ch1
    fileen = "data/hlm-ch1-en.txt"
    filezh = "data/hlm-ch1-zh.txt"
    hlmpara_en = Path(fileen).read_text("utf8").splitlines()
    hlmpara_zh = Path(filezh).read_text("utf8").splitlines()

    hlm_emb_en_file = "data/hlm_ch1_en_emb.lzma"
    hlm_emb_zh_file = "data/hlm_ch1_zh_emb.lzma"

    if Path(hlm_emb_en_file).exists():
        hlm_emb_en = joblib.load(hlm_emb_en_file)
    else:
        hlm_emb_en = embed_text(hlmpara_en)
        joblib.dump(hlm_emb_en, hlm_emb_en_file, ("lzma", 3))

    if Path(hlm_emb_zh_file).exists():
        hlm_emb_zh = joblib.load(hlm_emb_zh_file)
    else:
        hlm_emb_zh = embed_text(hlmpara_zh)
        joblib.dump(hlm_emb_zh, hlm_emb_zh_file, ("lzma", 3))

    hlm_emb_en = np.array(hlm_emb_en)
    hlm_emb_zh = np.array(hlm_emb_zh)

    # hlm ch1 para
    # logger.info("\n\t hlm ch1 para")
    cmat = cos_matrix2(hlm_emb_en, hlm_emb_zh)
    cmat = np.array(cmat)

    # ax = sns.heatmap(cmat, cmap='gist_earth_r')
    # ax.invert_yaxis()

    # cmat = joblib.load(r"data/cmat.lzma")
    # cmat = np.array(cmat)

    logger.info("cmat.shape: %s", cmat.shape)

    _ = """
    from tinybee.cmat2tset import cmat2tset

    # tset = cmat2tset(cmat)

    from tinybee.lowess_pairs import lowess_pairs
    yhat = lowess_pairs(cmat)
    df0 = pd.DataFrame(yhat, columns=["y00", "yargmax", "ymax"])
    fig, ax = plt.subplots()
    sns.scatterplot(data=df0, x="y00", y="yargmax", size="ymax", sizes=(1, 110))

    if "get_ipython" not in globals():
        plt.show(block=True)

    src_len, tgt_len = cmat.shape
    # pset: pair set, outliers eiminated
    pset = gen_row_align(yhat, src_len, tgt_len)
    df1 = pd.DataFrame(pset, columns=["y00", "yargmax", "ymax"])
    fig, ax = plt.subplots()
    sns.scatterplot(data=df1, x="y00", y="yargmax", size="ymax", sizes=(1, 110), ax=ax)

    if "get_ipython" not in globals():
        plt.show(block=True)

    # *pairs, _ = zip(*pset)
    # pairs = [*zip(*pairs)]
    # iset = interpolate_pset(pairs, tgt_len)

    iset = interpolate_pset(pset, tgt_len)
    df2 = pd.DataFrame(iset, columns=["y00", "yargmax"])
    fig, ax = plt.subplots()
    sns.scatterplot(data=df2, x="y00", y="yargmax", ax=ax)

    if "get_ipython" not in globals():
        plt.show(block=True)
    """

    _ = """
    iset = gen_iset(cmat)
    # align based on iset and cmat/tset
    if FLAGS.debug:
        matplotlib.use("TkAgg")
        # plt.ion()

        df2 = pd.DataFrame(iset, columns=["y00", "yargmax"])
        fig, ax = plt.subplots()
        sns.scatterplot(data=df2, x="y00", y="yargmax")
        plt.show(block=True)
    # """

    # src_emb = embed_text(src_text)
    # tgt_emb = embed_text(src_text)
    # cmat = cos_matrix2(src_emb, tgt_emb)
    # cmat = np.array(cmat)

    # cmat, tset, -dbscan fit-> ypred pset,
    #                   interpolate iset, aset, align text
    # tset = cmat2tset(cmat)
    #       db = DBSCAN(eps=eps, min_samples=min_samples)
    #       db.fit(tset)
    #       y_pred = db.fit_predict(tset)  # >-1, clustered
    #           db.components_, db.n_features_in_ (no of clusters)

    # directly go for pset
    # pset1 = find_pairs(cmat)  # pair set with metrics
    # df4 = pd.DataFrame(pset1, columns=["y00", "yargmax", "ymax"])
    # fig, ax = plt.subplots()
    # sns.scatterplot(data=df4, x="y00", y="yargmax", size="ymax", sizes=(1, 110), ax=ax)

    # aset = gen_aset(pset1, src_len, tgt_len)

    # align_texts(aset, src_text, tgt_text)  # -> texts


if __name__ == "__main__":
    # plt.ioff() # matplotlib.rcParam

    # print(plt.style.available)

    # main()
    app.run(main)
