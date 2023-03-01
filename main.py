from fastapi import FastAPI
from typing import List
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json


app = FastAPI()


async def get_code_from_gamesrader()->List[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.gamesradar.com/genshin-impact-codes-redeem/') as response:
                json_content = await response.text()
                soup=BeautifulSoup(json_content,'html.parser')
                lis = soup.select('.article .text-copy b, .article .text-copy strong, .news-article .text-copy b, .news-article .text-copy strong, .review-article .text-copy b, .review-article .text-copy strong, .static-article .text-copy b, .static-article .text-copy strong')  
                codes = [li.text.strip() for li in lis if li.text.strip().isupper()]
    except Exception as e:
        print(f"Error in get_code_from_gamesrader: {e}")
        return []

    return codes                    

async def get_code_from_programguide() -> List[str]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://progameguides.com/genshin-impact/genshin-impact-codes/') as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')
        lis = soup.select('div.entry-content li:not(:has(a)):has(strong)')

        codes = [li.strong.text.strip() for li in lis if li.strong.text.strip().isupper()]

    except Exception as e:
        print(f"Error in get_code_from_progameguides: {e}")
        return []

    return codes

async def get_code_from_gipn() -> List[str]:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://raw.githubusercontent.com/ataraxyaffliction/gipn-json/main/gipn-update.json') as response:
            json_content = await response.text()
            json_content =  json.loads(json_content)
    
            codes = json_content.get('CODES', {})
    available_codes = [code['code'] for code in codes if not code.get('is_expired', True)]
    return available_codes

async def get_code_from_pockettactics() -> List[dict]:
    codes = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.pockettactics.com/genshin-impact/codes') as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'html.parser')
        entries = soup.select('div.entry-content > ul > li:not(:has(a)) > strong:not(:has(a))')

        for entry in entries:
            code = entry.get_text().strip()
            if code and code == code.upper():
                description = entry.parent.get_text().split('–')[1].replace('(new!)', '').strip()
                codes.append({'code': code, 'description': description})

    except Exception as e:
        print(f"Error in get_code_from_pockettactics: {e}")
        return []

    return codes

@app.get("/")
async def root():
    return {"message": "Welcome to the Genshin Impact redeem code API! Please visit /codes for codes."}



@app.get("/codes")
async def read_codes() -> List[dict]:
    pocket_codes,program_codes,gipn,games_radar = await asyncio.gather(get_code_from_pockettactics(),get_code_from_programguide(),get_code_from_gipn(),get_code_from_gamesrader())
    old_codes = ['GENSHINGIFT', 'XBRSDNF6BP4R', 'FTRUFT7AT5SV']
    new_codes = [code for code in pocket_codes if code['code'] not in old_codes]    
    filtered_codes = [code for code in new_codes if code['code'] in gipn and code['code'] in program_codes and code['code'] in games_radar]
    monkey_code={"code":"SSRCJ8HSV7UM","description":"10k Mora, 10x Adventure's Experience, 5x Fine Enhancement Ore, 5x Fisheman's Toast, 5 Goulash"}
    if len(filtered_codes) == 0:
        new_codes.append(monkey_code)
        return new_codes
    filtered_codes.append(monkey_code)
    return filtered_codes

if __name__ == "__main__":
    import uvicorn
    import uvloop
    uvloop.install()
    uvicorn.run(app)
