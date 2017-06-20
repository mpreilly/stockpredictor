from yahoo_finance import Share
import csv
from datetime import date
from datetime import timedelta
import random

def get_random_stocks(num_train_stocks, num_test_stocks):
    all_companies = []
    training_stocks = []
    testing_stocks = []

    with open('data/companylist.csv','rb') as f:
        reader = csv.reader(f)
        for row in reader:
            all_companies.append(row.pop(0))

    for i in range(0, num_train_stocks):
        training_stocks.append(all_companies.pop(random.randint(1, len(all_companies)-1)))

    for i in range(0,num_test_stocks):
        testing_stocks.append(all_companies.pop(random.randint(1, len(all_companies)-1)))

    return training_stocks, testing_stocks


# def gather_historical(stocks, start_date, end_date):
