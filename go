set -e
./create_db.py
./score_athletes.py
./report_db.py 
cp html/*.html ~/Dropbox/Public/ScoringSystem
