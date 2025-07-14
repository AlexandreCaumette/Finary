import streamlit as st
import polars as pl
from stores.store_patrimoine import get_df_patrimoine
from stores.store_revenu import get_df_revenu
import datetime


def calcul_patrimoine_actuel() -> float:
    return get_df_patrimoine().select(pl.sum("amount")).item()


def calcul_epargne_annuelle_actuelle() -> float:
    return get_df_patrimoine().select(pl.sum("deposit")).item()


def calcul_nombre_sources_patrimoine() -> float:
    return get_df_patrimoine().select(pl.count("id_patrimoine")).item()


def calcul_revenu_actuel() -> float:
    return get_df_revenu().select(pl.sum("montant_revenu")).item()


def calcul_taux_epargne_actuel() -> float:
    return calcul_epargne_annuelle_actuelle() / calcul_revenu_actuel()


def calcul_df_patrimoine_projete(years: int) -> pl.DataFrame:
    df_patrimoine = get_df_patrimoine()

    now = datetime.datetime.now()

    df_patrimoine = df_patrimoine.with_columns(
        pl.datetime(year=now.year, month=now.month, day=now.day).alias("date")
    )

    labels = df_patrimoine.select(pl.col("label").unique()).to_series().to_list()

    for year in range(1, years + 1):
        for label in labels:
            previous_date = datetime.datetime(
                year=now.year + year - 1, month=now.month, day=now.day
            )

            df_year = df_patrimoine.filter(
                pl.col("date").eq(previous_date) & pl.col("label").eq(label)
            )

            df_year = df_year.with_columns(
                pl.datetime(year=now.year + year, month=now.month, day=now.day).alias(
                    "date"
                )
            )
            df_year = df_year.with_columns(
                (
                    pl.col("amount") * (1 + pl.col("return") / 100) + pl.col("deposit")
                ).alias("amount")
            )

            df_patrimoine = pl.concat([df_patrimoine, df_year], how="vertical")

    return df_patrimoine


def calcul_patrimoine_projete(years: int) -> float:
    df_patrimoine_projete = calcul_df_patrimoine_projete(years)

    now = datetime.datetime.now()
    date_projection = datetime.datetime(
        year=now.year + years, month=now.month, day=now.day
    )

    return (
        df_patrimoine_projete.filter(pl.col("date").eq(date_projection))
        .select(pl.sum("amount"))
        .item()
    )


def calcul_revenu_projete(years: int):
    return 0
