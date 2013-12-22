set -e
./create_db.py
./score_athletes.py
./report_db.py 
cp *.html ~/Dropbox/Public/ScoringSystem
