from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from variables import CONFIG
from .t_t import get_tone

def generate_tone_function():
    authenticator = IAMAuthenticator(CONFIG["IBM_API_KEY"])
    tone_analyzer = ToneAnalyzerV3(
        version = CONFIG["IBM_TONE_VERSION"],
        authenticator = authenticator
    )

    tone_analyzer.set_service_url(CONFIG["IBM_SERVICE_URL"])

    return tone_analyzer

def get_tone_analysis(text_to_analyze):

    response = get_tone(text_to_analyze)
    return response