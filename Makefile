venv:
	if [ -d twittersentiment ]; then \
		source twittersentiment/bin/activate; \
	else \
		python3 -m venv twittersentiment; \
		source twittersentiment/bin/activate; \
		python3 -m pip install -r reqs.txt; \
	fi

getModel:
	python3 -c "import stanza, os; stanza.download(lang='en', model_dir=os.getenv('TS_DATA'))" \
		|| echo "did you set TS_DATA ?"


run: venv getModel
	python3 sentiment.py
