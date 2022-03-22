import logging
import azure.functions as func
import psycopg2
import os as app
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info(
        'Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database

    dbConnection = psycopg2.connect(user="ushionguyen@techconfdb",
                                    password="Abcd1234@@@@",
                                    host="techconfdb.postgres.database.azure.com",
                                    port="5432",
                                    database="techconfdb")
    cursor = dbConnection.cursor()

    try:
        # TODO: Get notification message and subject from database using the notification_id
        notification_query = '''SELECT subject, message 
                                FROM Notification
                                WHERE id = %s;'''
        cursor.execute(notification_query, (notification_id,))

        # TODO: Get attendees email and name
        notification = cursor.fetchone()
        subject = notification[0]
        message = notification[1]

        # TODO: Loop through each attendee and send an email with a personalized subject
        attendees_query = 'SELECT first_name, email FROM Attendee;'
        cursor.execute(attendees_query)
        attendees = cursor.fetchall() 
        for attendee in attendees:
            first_name = attendee[0]
            email = attendee[1]
            custom_subject = '{}: {}'.format(first_name, subject)
            send_email(email, custom_subject, message)

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        completed_date = datetime.utcnow()
        status = 'Notified {} attendees'.format(len(attendees))
        notification_update_query = '''UPDATE Notification 
                                SET completed_date = %s, status = %s 
                                WHERE id = %s;'''
        cursor.execute(notification_update_query, (completed_date, status, notification_id))
        dbConnection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if(dbConnection):
            cursor.close()
            dbConnection.close()
            print("PostgreSQL connection is closed")

def send_email(email, subject, body):
    if not app.config.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=app.config.get('EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message)