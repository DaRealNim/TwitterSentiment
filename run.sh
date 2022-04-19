#!/usr/bin/env sh

#set -x

echo "reading env"

if [ -d twittersentiments ]
then
	. twittersentiments/bin/activate
else
	echo "No venv, pls run install.sh"
	return 1
fi

if [ -f .model_data_dir ]
then
	. ./.model_data_dir
else
	echo "Model data not found pls run install.sh"
	return 1
fi

export DATA_DIR
python3 sentiment.py
