# genshin-redeem-code
`genshin-redeem-code` is a Python web scraper that extracts Genshin Impact redeemable codes from various websites.


# Usage
make a get request to the following url: `https://genshin-redeem-code.vercel.app/codes`

it will return a json object with the following structure:
```
[
    {
        "code": "code",
        "description": "description
    },
    ...   
]
```

# Installation
```
git clone https://github.com/GauravM512/genshin-redeem-code
cd genshin-redeem-code
pip install -r requirements.txt
python main.py
```



# Contributing
If you want to contribute, you can add more websites to the `sites` list in `main.py` and make a pull request.