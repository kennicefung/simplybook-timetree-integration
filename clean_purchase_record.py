import gsheet_client

# remove the not yet paid transaction from google sheet
# which inserted from Zapier

def main():
	gsheet_client.remove_not_yet_paid_record()

if __name__ == '__main__':
	main()