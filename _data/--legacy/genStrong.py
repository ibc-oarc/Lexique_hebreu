## This script generates dictionary entries in the folder w/

def beautify_title(phon):
    """Normalizes phonetic information
    """
    return phon.replace("ǝ","<sup>ǝ</sup>").replace("î","ī").replace("û","ū").replace("â","ā").replace("ê","ē").replace("ô","ō")


def list_notnull(l):
    """Removes empty strings from a list
    """
    if "" in l: l.remove("")
    return l


def lang_full(x):
    """Returns full name for the languages (Aramaic or Hebrew)
    """
    if x=="H": return "Hebrew"
    if x=="A": return "Aramaic"

def stn(x):
    """Intelligent conversion from number to string
    """
    if x=="":return ""
    else: return str(int(float(x)))

def plur_linear(s):
    lis=s.split("|")
    if len(lis)==1: return s
    return " ".join(["""<sup style="color:gray;">{}</sup>""".format(str(i))+word for i,word in zip(range(1,len(lis)+1),lis)])
        
def nav_next(ind):
    """Navigation between lexicon entries, gives next entry
    """
    if ind==8674: return "9000"
    if ind==9012: return "1"
    return str(ind+1)

def nav_prev(ind):
    """Navigation between lexicon entries, gives previous entry
    """
    if ind==9000: return "8674"
    if ind==1: return "9012"
    return str(ind-1)
    
    
    
def plur_vertical(s):
    lis=s.split("|")
    if len(lis)==1: return s
    return "<br>".join(["""<strong>{}</strong> """.format(chr(ord('A')-1+i))+word for i,word in zip(range(1,len(lis)+1),lis)])


def wrapper(line, arg):
    if arg=="":return ""
    else: return line.format(arg)

def wrapper2(line, arg1, arg2):
    if arg2=="":return ""
    else: return line.format(arg1, arg2)
    
    
    
def force_to_int(value):
    """Given a value, returns the value as an int if possible.
    Otherwise returns None.
    """
    try:
        return int(value)
    except ValueError:
        return -1

##############################
#######  Start here ##########
##############################


books=["Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "Isaiah", "Jeremiah", "Ezekiel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Psalms", "Proverbs", "Job", "Song of Songs", "Ruth", "Lamentations", "Ecclesiastes", "Esther", "Daniel", "Ezra", "Nehemiah", "1 Chronicles", "2 Chronicles"]




import pandas as pd
print('Loading indexing information...\r',end="")    
index=pd.read_csv("_data/verses_index.csv",sep="\t")
# 23211	39	36	21
# number	book	chapter	verse

print('Loading verses...\r',end="")    
df=pd.read_csv("_data/TBESH_formatted.csv",sep="\t").fillna("")
df.columns = ["strongNumber", "void1", "hebWord", "lang", "void2", "void3", "void4", "root", "etym1", "etymWord1", "etym2", "etymWord2", "etym3", "etymWord3", "void5", "etymDesc", "void6", "occurences", "variants", "morphology", "heading", "content", "phonemes"]

#  0	strongNumber
#  1	void1
#  2	hebWord
#  3	lang
#  4	void2
#  5	void3
#  6	void4
#  7	root
#  8	etym1
#  9	etymWord1
# 10	etym2
# 11	etymWord2
# 12	etym3
# 13	etymWord3
# 14	void5
# 15	etymDesc
# 16	void6
# 17	occurences
# 18	variants
# 19	morphology
# 20	heading
# 21	content
# 22	phonemes

print('Transforming columns...\r',end="")    
df["phonemes"]=df["phonemes"].apply(beautify_title)
df["heading"]=df["heading"].apply(plur_linear)
df["strongNumberInt"]=df["strongNumber"].apply(lambda x: x[1:]).apply(int)
df["root"]=df["root"].apply(stn)
df["lang"]=df["lang"].apply(lang_full)
df["etym1"]=df["etym1"].apply(stn)
df["etym2"]=df["etym2"].apply(stn)
df["etym3"]=df["etym3"].apply(stn)
df["nav_prev"]=df["strongNumberInt"].apply(nav_prev)
df["nav_next"]=df["strongNumberInt"].apply(nav_next)
df["morphology"]=df["morphology"].apply(plur_linear)
df["morphology"]=df["morphology"].apply(plur_vertical)

print('Transforming columns 2...\r',end="")    
df["etym1template"] = df[["etym1", "etymWord1"]].apply(lambda x: wrapper2("""<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", x["etym1"], x["etymWord1"]), axis=1)
df["etym2template"] = df[["etym2", "etymWord2"]].apply(lambda x: wrapper2("""<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", x["etym2"], x["etymWord2"]), axis=1)
df["etym3template"] = df[["etym3", "etymWord3"]].apply(lambda x: wrapper2("""<a class="shadow" href="/w/{}"><span id="bh">{}</span></a>""", x["etym3"], x["etymWord3"]), axis=1)

df["etymTemplate"]=df["etym1template"]+df["etym2template"]+df["etym3template"]

print('Transforming placeholders...\r',end="")    
df["placeholder1"] = df["etymTemplate"].apply(lambda x: wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Roots:</span> {} """, x))
print('Transforming placeholders 2...\r',end="")    
df["placeholder2"] = df["root"].apply(lambda x: wrapper("""({})""", x))
print('Transforming placeholders 3...\r',end="")    
df["placeholder3"] = df["variants"].apply(lambda x: wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Variants:</span> {}
""", x))
print('Transforming placeholders 4...\r',end="")    
df["placeholder4"] = df["morphology"].apply(lambda x: wrapper(""" | <span style="color: rgba(0, 0, 0, 0.75)">Morphology:</span> {} """, x))
print('Transforming placeholders 5...\r',end="")    
df["placeholder5"] = df[["phonemes","content"]].apply(lambda x: wrapper("""</p><p>{}</p>
""", """<span style="font-family: sans-serif;font-weight: bold;">{}</span><br>{}""".format(x["phonemes"],x["content"])), axis=1)
print('Preparing links ...\r',end="")    

##############################
#### Preparing links #########
##############################

df["occurences"]=df["occurences"].apply(lambda x: x.split(","))
one_occurence_by_line=df[["strongNumber","occurences"]].explode("occurences")
one_occurence_by_line["occurences"]=one_occurence_by_line["occurences"].apply(force_to_int)

links_fetched = one_occurence_by_line.merge(index,left_on="occurences",right_on="number").dropna(axis=0)
links_fetched["link"]=links_fetched[["number","chapter","verse"]].apply(lambda x: """<span id="toc"><span style="color:darkgray;"> </span><a class="shadow" href="https://bh.seveleu.com/v/{}.html">{}:{}</a></span>""".format(x["number"],x["chapter"],x["verse"]).format(x["chapter"],x["verse"]), axis=1)
links_fetched=links_fetched.drop(["occurences","number","chapter","verse"], axis=1)

links_by_book = links_fetched.groupby(["strongNumber","book"])["link"].apply(", ".join)
links_by_book=links_by_book.reset_index(level=1)
links_by_book["book"]=links_by_book["book"].apply(lambda x: """<span id="toc" style="font-family:sans-serif;">{}</span>""".format(books[x-1]))
links_by_book["link"]=links_by_book["book"]+links_by_book["link"]
links_by_book=links_by_book.drop(["book"], axis=1)

links_by_Strong_number = pd.DataFrame({"links": links_by_book["link"].groupby("strongNumber").apply(" ".join)})

df=df.merge(links_by_Strong_number, left_on="strongNumber", right_index=True, how="left").fillna({"links":""})

#############################
#### Generating files #######
#############################


with open("LexiconEntryTemplate.html", "r") as fin:
    lexiconEntryTemplate = fin.read()

df["htmlcontent"]=df[["phonemes", "hebWord", "heading", "strongNumberInt", "root", "nav_prev", "nav_next", "lang", "etymDesc", "placeholder1", "placeholder2", "placeholder3", "placeholder4", "placeholder5", "links"]].apply(lambda x: lexiconEntryTemplate.format(x["phonemes"], x["hebWord"], x["heading"], x["strongNumberInt"], x["root"], x["phonemes"], x["hebWord"], x["heading"], x["strongNumberInt"], x["nav_prev"], x["nav_next"], x["phonemes"], x["hebWord"], x["heading"], x["lang"], x["etymDesc"], x["placeholder1"] , x["placeholder2"], x["placeholder3"] , x["placeholder4"] , x["placeholder5"] , x["nav_prev"], x["nav_next"], x["links"]), axis=1)

df["currentfilename"] = df["strongNumberInt"].apply(str).apply(lambda x: "w/{}.html".format(x))

def writeToFile(dfline):
    with open(dfline["currentfilename"], 'w+') as fout1:
        fout1.write(dfline["htmlcontent"])

print("Generating files : ")


df[["currentfilename", "htmlcontent"]].apply(writeToFile, axis=1)



df=df.sort_values(by=["strongNumber"], axis=0)

massIndividualEntry="""<span id="toc"><span style="color:darkgray;">{}</span><a class="shadow" href="/w/{}.html">{} <span id="bh">{}</span></a></span>"""

df["MassLexiconLayout"]=df[["strongNumberInt","phonemes","hebWord"]].apply(lambda x: massIndividualEntry.format(x["strongNumberInt"],x["strongNumberInt"],x["phonemes"],x["hebWord"]), axis=1)


with open("LexiconMassTemplate.html", "r") as fin:
    lexiconMassTemplate = fin.read()

lexiconcontent = lexiconMassTemplate.format("".join(list(df["MassLexiconLayout"])))

with open("lexicon.html","w+") as fout:
    fout.write(lexiconcontent)
