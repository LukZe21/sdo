from email.message import EmailMessage
import smtplib
import ssl


email_sender = "ldzotsenidze4@gmail.com"

email_password = "rcom lgpg furx fkbz"


def send_emails(emails, category="", id="", name="", condition="", expiration_duration="", start_date="", end_date="", event_hoster=""):
    if category=='discount':
        subject = f'{condition}% ფასდაკლება {name}-ზე!'
        body = f"""
        ჩვენთან დაემატა ახალი ექსკლუზიური ფასდაკლება {name}-ზე\n

        შეთავაზების დეტალები:
        ფასდაკლება: {condition}\n
        დასრულების თარიღი: {expiration_duration}.

        არ გამოტოვო ეს სპეციალური შეთავაზება!
        გადადი ამ ბმულზე და ისარგებლე ამ ფასდაკლებით:
        https://www.studentsdayoffs.edu.ge/discounts/{id}
               """
    elif category=='event':
        subject = f'{name}'
        body = f"""
        ჩვენთან დაემატა ახალი ექსკლუზიური ივენთი - {name}\n

        დეტალები:
        დაწყების დრო: {start_date}\n
        დამთავრების დრო: {end_date}\n
        მასპინძელი: {event_hoster}.

        გადადი ამ ბმულზე და დარეგისტრირდი!:
        https://www.studentsdayoffs.edu.ge/events/{id}
        """

    for email in emails:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email, em.as_string())
