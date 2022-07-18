from rest_framework.request import Request
from polaris.models import Transaction, Asset


def toml_integration(request, *args, **kwargs):
    asset = Asset.objects.first()
    return {
        "DOCUMENTATION": {
            "ORG_NAME": "Blck DEV",
            "ORG_DBA": "Tontine",
            "ORG_URL": "http://localhost:8000",
            "ORG_LOGO": "https://www.freepik.com/free-vector/glowing-neon-style-bitcoin-background-with-circuit-lines_18309040.htm",
            "ORG_DESCRIPTION": "We make tontine easier",
            "ORG_PHYSICAL_ADDRESS": "Campus EPT, Thies - SENEGAL",
            "ORG_PHONE_NUMBER": "+221 77 805 47 97",
            "ORG_KEYBASE": "blckdevs",
            "ORG_GITHUB": "blck-dev",
            "ORG_OFFICIAL_EMAIL": "blck.dev.tontines@gmail.com"
        },
        "PRINCIPALS": [{
            "name": "Abdou Yaya",
            "email": "saabdouyaya@ept.sn",
            "twitter": "esprit_bayesien",
            "github": "abdoufermat5"
        }],
        "CURRENCIES": [{
            "code": asset.code,
            "issuer": asset.issuer,
            "status": "test",
            "display_decimals": 2,
            "name": "XOF tontine",
            "desc": "Participate to a tontine with your XOF tontine token!!",
            "image": "https://static.thenounproject.com/png/2292360-200.png"
        }]
    }
