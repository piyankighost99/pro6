import requests
import time
from bs4 import BeautifulSoup
import csv

telegram_bot_token = '6940889605:AAFQuf9smrtxLCvx7vv6yZiplarr1mpDXTE'
telegram_channel_username = '@kaljobs'

url = 'https://etcareers.com/jobs'
response = requests.get(url)
html_code = response.content

def scrape_website(html_code):
    soup = BeautifulSoup(html_code, "html.parser")
    jobs = []
    items = soup.find_all("article", class_="media well listing-item listing-item__jobs listing-item__featured")

    for item in items:
        job_title = item.select_one('.listing-item__title a').text.strip()
        location = item.select_one('.listing-item__info--item-location').text.strip()
        details = item.select_one('.listing-item__desc').text.strip()
        work_hours = item.select_one('.listing-item__employment-type').text.strip()
        date_posted = item.select_one('.listing-item__date').text.strip()

        jobs.append({
            "Job Title": job_title,
            "Location": location,
            "Details": details,
            "Work Hours": work_hours,
            "Date Posted": date_posted,
        })

    return jobs

def send_message_to_telegram(message):
    send_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        "chat_id": telegram_channel_username,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(send_message_url, data=data)
    if response.status_code != 200:
        print("Failed to send message to Telegram channel.")
    else:
        print("Message sent successfully.")

def write_jobs_to_csv(jobs):
    with open('top_jobs.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Job Title', 'Location', 'Details', 'Work Hours', 'Date Posted'])
        for job_info in jobs:
            writer.writerow([job_info['Job Title'], job_info['Location'], job_info['Details'], job_info['Work Hours'], job_info['Date Posted']])

job_data = scrape_website(html_code)
write_jobs_to_csv(job_data)

for job_info in job_data:
    caption = f"<b><i><u>{job_info['Job Title']}</u></i></b>\n"
    caption += f"<b><i><u>Location:</u></i></b> {job_info['Location']}\n"
    caption += f"<b><i><u>Details:</u></i></b> {job_info['Details']}\n"
    caption += f"<b><i><u>Work Hours:</u></i></b> {job_info['Work Hours']}\n"
    caption += f"<b><i><u>Date Posted:</u></i></b> {job_info['Date Posted']}"

    print(f"Sending message to Telegram: {caption}")

    send_message_to_telegram(caption)

    time.sleep(60)
