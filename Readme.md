This is a simple Python Web Scraper that scrapes prices off Amazon.in and stores it in a sqlite db.

I often found it difficult to keep track of the prices of varous products that I had an eye on.
So I created this python script.

Usage:
- You need to add the product ids from the Amazon link as comma seperated values in the AsinList.csv file.
	eg : https://www.amazon.in/OnePlus-Midnight-Black-128GB-Storage/dp/B07DJHY82F/ here B07DJHY82F is the product id
- You can then view the extracted data stored in AmazonScrappedProducts.db

I have added a cron job in my machine so that this script executes every hour storing the details in the database.
