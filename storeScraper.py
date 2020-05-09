import selenium
import requests
import os
import io
from PIL import Image
import hashlib
import time
from selenium import webdriver

DRIVER_PATH = "C:\\Users\\Clifford Xu\\Documents\\programming_projects\\Webscraper\\chromedriver.exe"


def get_image_urls(query: str, max_links:int, wd: webdriver, sleep_seconds: int=1):

    search_url = "https://www.farfetch.com/shopping/men/{q}/items.aspx?view=180&scale=284&q={q}"

    wd.get(search_url.format(q=query))


    image_urls = set()
    image_count = 0
    results_start = 0
    count=0
    while image_count < max_links:

        thumbnail_results = wd.find_elements_by_css_selector("img._fc8ffc")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results.")
        for img in thumbnail_results:
            wd.execute_script("arguments[0].scrollIntoView();", img)
            print(img.get_attribute("src"))
            time.sleep(sleep_seconds)
            image_urls.add(img.get_attribute("src"))

            image_count = len(image_urls)
            if len(image_urls) >= max_links:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            time.sleep(1)
            next_button = wd.find_element_by_css_selector("a._cf3b6e._6297d2._e7b42f")
            if next_button:
                wd.execute_script("document.querySelector('a._cf3b6e._6297d2._e7b42f').click();")
                time.sleep(1)
                continue

    return image_urls
def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term:str,driver_path:str,target_path='./images',number_images=500):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = get_image_urls(search_term, number_images, wd=wd, sleep_seconds=0.5)

    for elem in res:
        persist_image(target_folder,elem)

search_term = "off-white"
search_and_download(search_term=search_term,
                     driver_path=DRIVER_PATH)

