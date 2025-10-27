from PIL import Image, ImageDraw, ImageFont
import os
from typing import List, Dict, Any
from datetime import datetime

IMAGE_DIR = "cache"
IMAGE_FILENAME = "summary.png"
IMAGE_PATH = os.path.join(IMAGE_DIR, IMAGE_FILENAME)

IMAGE_WIDTH = 900
IMAGE_HEIGHT = 1200

BG_COLOR = (40, 44, 52)
TEXT_COLOR = (255, 255, 255)
HEADER_FONT_SIZE = 36
BODY_FONT_SIZE = 24


async def generate_summary_image( total_countries: int, top_5_gdp_countries: List[Dict[str, Any]], last_refresh_timestamp: datetime):
    os.makedirs(IMAGE_DIR, existsok=True)
    
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color = BG_COLOR)
    d = ImageDraw.Draw(img)
    title_text = "Country Data Summary"
    d.text((50,50), title_text, fill=TEXT_COLOR)
    
    d.text((50, 120), f"Total Countries: {total_countries}", fill=TEXT_COLOR)
    
    y_offset = 180
    d.text((50, y_offset), "Top 5 Countries Estimated GDP:", fill=TEXT_COLOR)
    y_offset += 40
    
    if top_5_gdp_countries:
        for i, country in enumerate(top_5_gdp_countries):
            d.text((50, y_offset), f"{i+1}. {country['name']} - ${country['estimated_gdp']}", fill=TEXT_COLOR)
            y_offset += 40
    else:
        d.text((50, y_offset), "No data available", fill=TEXT_COLOR)
    
    y_offset += 40
    d.text((50, y_offset), f"Last Refreshed: {last_refresh_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", fill=TEXT_COLOR)
    img.save(IMAGE_PATH)

async def fetch_stored_summary_image():
    pass