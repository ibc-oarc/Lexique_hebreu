# Lexique_hebreu
Lexique de l'hébreu biblique d'après Strong. Fait partie de la ressource « Hébreu biblique pour linguistes : Westminster Codex de Léningrad &amp; Lexique hébraïque » à https://lex.ibc.oarc.science/fr . Volet français d'un projet multilingue.

Générer avec :

`git clone https://github.com/ibc-oarc/Hebrew_lexicon_template ; ls ; rm -rf Hebrew_lexicon_template/.git ; rsync -a Hebrew_lexicon_template/ . --remove-source-files ; rm -rf Hebrew_lexicon_template/ ; pip install -r requirements.txt ; cd _data ; python precompile_lexicons.py ; python precompile_occurences.py ; cd .. ; RUBYOPT='-W0' bundle install; RUBYOPT='-W0' bundle exec jekyll build` (ou `serve`)
