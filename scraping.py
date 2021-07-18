# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():

    # Set the executable path and initialize Splinter
    # Initiate headless driver for deployment    executable_path = {'executable_path': ChromeDriverManager().install()}
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
     
    news_title, news_p = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_info": hemispheres_images(browser)
    }
    return data 
  
# ### Visit the NASA Mars News Site
def mars_news(browser):

# Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

   # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_title
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
        news_p
    except AttributeError:
        return None, None

    return news_title, news_p

       # ### JPL Space Images Featured Image
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup

    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    img_url_rel

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url


    # ### Mars Facts
def mars_facts():
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.head()

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    return df.to_html()
def hemispheres_images(browser):
    # visit URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemisphereDict = {}
        hemisphereDict['img_title'] = browser.find_by_css('a.itemLink h3')[i].text
        browser.find_by_css('a.itemLink h3')[i].click()
        hemisphereDict['img_url'] = browser.find_by_text('Sample')['href']
        browser.back()
        hemisphere_image_urls.append(hemisphereDict)
    # return hemispheres
    browser.quit()
    # Return to main page
    browser.back()



    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls
    


    # 5. return the browser
    browser.back()


# def hemisphere_images(browser):
#     # 1. Use browser to visit the URL 
#     url = 'https://marshemispheres.com/'
#     browser.visit(url)

#     # 2. Create a list to hold the images and titles.
#     hemisphere_image_urls = []

#     # Parse the data
#     html = browser.html
#     main_page_soup = soup(html, 'html.parser')

#     # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     # Find the number of pictures to scan
#     pics_scan = len(main_page_soup.select("div.item"))
#     # len(pics_scan)
#     pics_scan


#     # # 2. Create a list to hold the images and titles.
#     hemisphere_image_urls = []

#     # # Parse the data
#     # html = browser.html
#     # main_page_soup = soup(html, 'html.parser')

#     # # 3. Write code to retrieve the image urls and titles for each hemisphere.
#     # # Find the number of pictures to scan
#     # pics_scan = len(main_page_soup.select("div.item"))

#     # for loop over the link of each sample picture
#     for i in range(pics_scan):
#         # Create an empty dict to hold the search results
#         results = {}
#         # Find link to picture and open it
#         link_image = main_page_soup.select("div.description a")[i].get('href')
#         browser.visit(f'https://marshemispheres.com/{link_image}')
        
#         # Parse new html page with soup
#         html = browser.html
#         sample_image_soup = soup(html, 'html.parser')
#         # Get the full image link
#         img_link = "https://marshemispheres.com/"+ sample_image_soup.select_one("div.downloads ul li a").get('href')
#         # Get the full image title
#         img_title = sample_image_soup.select_one("h2.title").get_text()
#         # Add extracts to the results dict
#         results = {
#             'img_link': img_link, 'title': img_title}

        
#         # Append results dict to hemisphere image urls list
#         hemisphere_image_urls.append(results)
        


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



