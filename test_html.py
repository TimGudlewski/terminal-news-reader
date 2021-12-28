import requests
import html2text

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

def get_html(url):
    try:
        r = requests.get(url, headers=headers)
        return r.text
    except:
        pass

text_maker = html2text.HTML2Text()
text_maker.ignore_links = True
text_maker.ignore_images = True
text_maker.bypass_tables = False

my_url = "https://www.foxsports.com.au/cricket/domestic-cricket/big-bash/live-bbl-cricket-scores-2021-adelaide-strikers-vs-brisbane-heat-how-to-live-stream-supercoach-updates-scorecard-commentary/news-story/880d053eefef5fe6dd48d3a882409818"

html = get_html(my_url)
text = text_maker.handle(html)
print(text)
    
