#%%
import datetime
import sys
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor, wait

from scraper_amazon_urls import get_driver_headless, write_to_file_Link, connect_to_base


def run_process_pages(page_number, filename):
    browser = get_driver_headless()
    all_links = []
    if connect_to_base(browser, page_number):
        sleep(10) 
        try:
            links = browser.find_elements_by_xpath('//*[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')
            for i in links:
                all_links.append(i.get_attribute("href"))
            print('len_all_links, Page_number', len(all_links), page_number)
        except Exception as e:
            print('Error getting URLs', i, '\n', e)
    
        write_to_file_Link(all_links, filename)
        print('writing to csv page number', page_number)
        browser.quit()
    else:
        print("Error connecting to hacker news")
        browser.quit()

if __name__ == "__main__":

    # # headless mode?
    # headless = False
    # if len(sys.argv) > 1:
    #     if sys.argv[1] == "headless":
    #         print("Running in headless mode")
    #         headless = True

    # set variables
    start_time =  time()
    output_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"Amazon_output_Urls{output_timestamp}.csv"
    futures = []

    # multithreading
    with ThreadPoolExecutor() as executor:
        for number in range(230,250):
            futures.append(
                executor.submit(run_process_pages, number, output_filename)
            )

    wait(futures)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")



# %%
