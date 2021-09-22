import pandas as pd
import yaml

lexicon_filename="comma_separated_TBESH_formatted.csv"
index_filename="verses_index.csv"
biblebooks_filename="biblebooks.csv"

def force_to_int(value):
    """Converts a value to int or returns None.
    """
    try:
        return int(value)
    except ValueError:
        return -1
        
lexicon=pd.read_csv(lexicon_filename, sep=",", usecols=["strongNumber", "occurences"], dtype={"occurences":str}, keep_default_na=False)


index=pd.read_csv(index_filename, sep=",")
books=list(pd.read_csv(biblebooks_filename, sep=",")["bookname"])


with open("../_includes/template_link.html","r") as fin:
    template_link=fin.read().rstrip()
with open("../_includes/template_book.html","r") as fin:
    template_book=fin.read().rstrip()
with open("../_config.yml", "r") as fin:
    dic=yaml.safe_load(fin)

lexicon["occurences"]=lexicon["occurences"].apply(lambda x: x.split(","))
one_occurence_by_line=lexicon[["strongNumber","occurences"]].explode("occurences")
one_occurence_by_line["occurences"]=one_occurence_by_line["occurences"].apply(force_to_int)
one_occurence_by_line=one_occurence_by_line.sort_values(by=["strongNumber","occurences"])

template_link=template_link.replace("{{{{site.readersite}}}}", dic["readersite"]).replace("{{{{site.readersiteprefix}}}}", dic["readersiteprefix"])
print(template_link)
links_fetched = one_occurence_by_line.merge(index,left_on="occurences",right_on="number").dropna(axis=0)
links_fetched["link"]=links_fetched[["number","chapter","verse"]].apply(lambda x: template_link.format(x["number"],x["chapter"],x["verse"]).format(x["chapter"],x["verse"]), axis=1)
links_fetched=links_fetched.drop(["occurences","number","chapter","verse"], axis=1)

links_by_book = links_fetched.groupby(["strongNumber","book"])["link"].apply(", ".join)
links_by_book=links_by_book.reset_index(level=1)
links_by_book["book"]=links_by_book["book"].apply(lambda x: template_book.format(books[x-1]))
links_by_book["link"]=links_by_book["book"]+links_by_book["link"]
links_by_book=links_by_book.drop(["book"], axis=1)

links_by_Strong_number = pd.DataFrame({"links": links_by_book["link"].groupby("strongNumber").apply(" ".join)})
links_by_Strong_number["links"]=links_by_Strong_number["links"].apply(lambda x: x.replace("</a></span>, ","</a>, </span>"))

print(links_by_Strong_number["links"].loc[2])
links_by_Strong_number.to_csv("precompiled_links.csv", sep=",")
