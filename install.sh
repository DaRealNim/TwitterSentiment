#!/usr/bin/env sh

# debug
#set -x

echo "Installing dependencies in a venv..."
python3 -m venv twittersentiments
. twittersentiments/bin/activate
python3 -m pip install -r reqs.txt

echo "Downloading models..."
echo "Where would you like to store your model data ?:"
read -r data_path

if [ ! -d "$data_path" ]
then
	print "%s does not exist, creating..." "$data_path"
	mkdir -p "$data_path"
fi

python3 -c "import stanza, os; stanza.download(lang='fr', model_dir='$data_path')"
echo "DATA_DIR=$data_path" > .model_data_dir

echo "all done"
