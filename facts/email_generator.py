from guerrillamail import GuerrillaMailSession
from faker import Faker
from utils import *


session = GuerrillaMailSession()
fake = Faker()


def generate_email_address():
    name = f'{fake.name()}.{fake.job()}'.replace(' ','')
    session.set_email_address(name)
    print("email_address : ",session.get_session_state()['email_address'])
    return session.get_session_state()['email_address']


def get_otp():
    email_list = session.get_email_list()
    def loop(email_list):
        for i in range(30):
            print("len-email_list >>>>",len(email_list))
            if len(email_list) >= 2:
                otp = str(email_list[0].subject[:7]).strip()
            else:
                otp = None
                timer()
                email_list = session.get_email_list()
        print('otp >>>',otp)
        return otp

    otp = loop(email_list)
    if not otp:
        otp = loop(email_list)

    print("otp :",otp)
    return otp


# generate_email_address()
# get_otp()