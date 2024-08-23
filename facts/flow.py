from xpath import *
from utils import ELEMENT_TYPE


button = ELEMENT_TYPE[0]
textbox = ELEMENT_TYPE[1]


LOGIN_ELEMENTS = [
                    {'elementXpath':EMAIL,'element_type':textbox,'keys':'generate_email_address'},
                    {'elementXpath':CONTINUE_WITH_EMAIL,'element_type':button,'keys':None},
                    {'elementXpath':LOGIN_CODE,'element_type':textbox,'keys':'get_otp'},
                    {'elementXpath':LOGIN_BUTTON,'element_type':button,'keys':None},
                    {'elementXpath':HOW_U_KNOW,'element_type':button,'keys':None},
                    {'elementXpath':HOW_U_KNOW_CONTINUE_BUTTON,'element_type':button,'keys':None},
                    {'elementXpath':RESON,'element_type':button,'keys':None},
                    {'elementXpath':REASON_CONTINUE_BUTTON,'element_type':button,'keys':None},
                    {'elementXpath':USER_NAME,'element_type':textbox,'keys':'fake_name'},
                    {'elementXpath':PROFILE_CONTINUE_BUTTON,'element_type':button,'keys':None}
                ]


VIDEO_GENERATOR_ELEMENTS = [
                                {'elementXpath':PROMPT_TEXT_BOX,'element_type':textbox,'keys':'query_generator','timer':None},
                                {'elementXpath':GENERATE_VIDEO_BUTTON,'element_type':button,'keys':None,'timer':60},
                                {'elementXpath':AUDIENCE,'element_type':button,'keys':None,'timer':None},
                                {'elementXpath':PROMT_CONTINUE_BUTTON,'element_type':button,'keys':None,'timer':180},
                                {'elementXpath':EXPORT_DROPDOWN,'element_type':button,'keys':None,'timer':None},
                                {'elementXpath':EXPORT_BUTTON,'element_type':button,'keys':None,'timer':None},
                                {'elementXpath':WATERMARK,'element_type':button,'keys':None,'timer':None},
                                {'elementXpath':BRANDING,'element_type':button,'keys':None,'timer':None},
                                {'elementXpath':PUBLISH_BUTTON,'element_type':button,'keys':None,'timer':300},
                                {'elementXpath':DOWNLOAD_BUTTON,'element_type':button,'keys':None,'timer':None},
                            ]


LOGOUT_ELEMENTS = [
                    {'elementXpath':PROFILE_ICON,'element_type':button,'keys':None},
                    {'elementXpath':LOG_OUT,'element_type':button,'keys':None},
                ]
