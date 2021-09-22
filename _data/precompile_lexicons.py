import pandas as pd
lexicon_filename="comma_separated_TBESH_formatted.csv"
lexicons_config_filename="partiallexicons.csv"
partiallexicons=pd.read_csv(lexicons_config_filename, sep=",", keep_default_na=False)
lexicon=pd.read_csv(lexicon_filename, sep=",", usecols=["strongNumber", "morphology", "occurencesorder"], keep_default_na=False)
import re
lexicon["morphology"]=lexicon["morphology"].apply(lambda x: re.split(';|\|',x))
lexicon=lexicon.set_index("strongNumber")
partiallexicons["sets"]=partiallexicons["morpholist"]\
                            .apply(lambda x: x.split(";")) \
                            .apply(lambda x: set(x) )

values=[]
for i,row in partiallexicons.iterrows():
    if row["ordered"]=="ordered by frequency":
        indexlist=lexicon[lexicon["morphology"].apply(row["sets"].intersection).apply(len) >0].sort_values(by="occurencesorder").index
    else:
        indexlist=lexicon.index[lexicon["morphology"].apply(row["sets"].intersection).apply(len) >0]
    values+=[",".join(list(map(str, list(indexlist))))]
partiallexicons["links"]=values
partiallexicons[["nameid","links"]].set_index("nameid").to_csv("precompiled_lexicons.csv", sep=",")
