# Terminal News Reader

## Description

Tired of flashing autoplay ads ruining your online news-reading experience?

Read the news in your terminal instead with Terminal News Reader!

Up and down arrows navigate through the headlines, enter selects an article, j scrolls down through the contents, k scrolls up, q quits.

## Setup 

First, run the following commands in Bash or Zsh:

(tested November 3rd 2024 on WSL Windows 11 Zsh)

```
git clone https://github.com/wharvex/terminal-news-reader.git
cd terminal-news-reader
cp ./news_keys_example.json ~/news_keys.json
cp ./news_sample1.json ~/
```

Next, visit https://newsapi.org/register and register for an API key.

Once you have your key, paste it into the appropriate place in `~/news_keys.json`.

## Run

Run the following commands in Bash or Zsh in the repo root to create a Python virtual environment, install the necessary packages, and run the program.

(tested November 3rd 2024 on WSL Windows 11 Zsh)

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python news_reader.py
```

