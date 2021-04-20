# What is this?

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This is a Discord bot used for making scraping the CPHUB Beginner Contests Ranklist and push them into the GitHub. Made mainly using requests_html and BeautifulSoup4 and discord.py .



## Installation

<!---
> **Use Python 3.7 or later**
--->
Clone the repository and install the requirements.

``` 
git clone https://github.com/akshith6212/scraper.git
```

**Dependencies**

Install the necessary dependencies from [requirements.txt](requirements.txt)

``` 
pip install -r requirements.txt
```



## Usage:

Run the main.py to activate the bot.

```
python main.py
```

**Note**:

>Make sure you have given the tokens for both github and discord.



## Commands

- $start link
  - Starts scraping if and only if the link is valid.

- $push 
  - Starts pushing the changes made to the given git repository.

- $help 
  - For displaying this message.



## References:

- [Freecodecamp tutorial to create discord bot using python](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) 
- [Corey Schafer tutorial for BeautifulSoup](https://www.youtube.com/watch?v=ng2o98k983k)  
- [Corey Schafer tutorial for requests-html](https://www.youtube.com/watch?v=a6fIbtFB46g) 
- [requests-html official docs](https://docs.python-requests.org/projects/requests-html/en/latest/)

