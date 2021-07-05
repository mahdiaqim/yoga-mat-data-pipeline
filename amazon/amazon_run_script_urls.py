import datetime
import sys
from time import sleep, time

from scraper_amazon import get_all_links_to_each_mat_in_each_page, get_driver, write_to_file, connect_to_base

# main block
# set variables
def run_process(page_number, filename, browser):
    if connect_to_base(browser, page_number):
        sleep(2)
        all_links = get_all_links_to_each_mat_in_each_page(browser, current_page)
        write_to_file(all_links, filename)
    else:
        print("Error connecting to hacker news")
start_time = time()
current_page = 1
output_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
output_filename = f"Amazon_output_{output_timestamp}.csv"

browser = get_driver()

while current_page <= 20:
    print(f"Scraping page #{current_page}...")
    run_process(current_page, output_filename, browser)
    current_page = current_page + 1
 # exit
browser.quit()
end_time = time()
elapsed_time = end_time - start_time
print(f"Elapsed run time: {elapsed_time} seconds")
