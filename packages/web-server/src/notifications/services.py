import sib_api_v3_sdk
import os

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.environ.get("SIB_API_KEY")

# create an instance of the API class
api_instance = sib_api_v3_sdk.SMTPApi(sib_api_v3_sdk.ApiClient(configuration))


def mail(to_name, to_email, params):
    # params = {
    #     "title": "Email H1 title",
    #     "subject": "Email subject",
    #     "body": "Email body",
    #     "cta_text": "Call to action text",
    #     "cta_url": "https://app.preemptor.ai/#/assignment/{}".format(assignment_id),
    # }
    params["subject"] = params["title"]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"name": to_name, "email": to_email}], template_id=1, params=params,
    )
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Mail", api_response)
    except Exception as e:
        print("Mailerror", e)
