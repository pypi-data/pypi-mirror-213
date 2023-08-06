from rechtspraak import *
from rechtspraak_metadata import *
df = get_rechtspraak(max_ecli=200,save_file='n')
df_2 = get_rechtspraak_metadata(save_file='n',dataframe=df)
b=2
pass