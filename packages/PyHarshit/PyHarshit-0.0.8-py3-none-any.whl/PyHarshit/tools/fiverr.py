import csv 
import time 
from datetime import datetime 
from math import ceil 
from selenium.webdriver.common.by import By

def export_gig_reviews_data_to_csv(driver, csv_filename):
    headers = ['Username', 'Country', 'Time']
    total_reviews = driver.find_elements(By.CLASS_NAME, "review-item-component-wrapper")

    if not len(total_reviews):
        print("No reviews to export")
        return None

    print("Total reviews data to export: ", len(total_reviews))
    with open(f'{csv_filename}.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)

        i = 1
        for review in total_reviews:
            try:
                print("Review number: ", i)
                i += 1

                review_data = review.text.splitlines()
                if not len(review_data):
                    continue
                username = review_data[0]
                if len(username) == 1:
                    data = [review_data[1], review_data[2], review_data[4]]
                else:
                    data = [review_data[0], review_data[1], review_data[3]]
                csvwriter.writerow(data)

            except Exception as ex:
                print("ERROR - export_gig_reviews_data_to_csv: ", ex)

    return "SUCCESS"
