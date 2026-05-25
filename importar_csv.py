import pandas as pd
import sqlite3

df = pd.read_csv("registros.csv", dtype=str)

df.columns = [
    'bautizado',
    'folio',
    'partida',
    'fecha_bautismo',
    'fecha_nacimiento',
    'padres',
    'padrinos',
    'celebrante'
]

conn = sqlite3.connect("parroquia.db")

df.to_sql(
    "bautismos",
    conn,
    if_exists="append",
    index=False
)

conn.close()

print("Importación completada.")