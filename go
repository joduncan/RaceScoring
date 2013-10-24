set -e
./create_db.py
./report_db.py 
cp *.html ~/Dropbox/Public/ScoringSystem
