from chargemaster_parsers.parsers import ChargeMasterEntry, UCSDChargeMasterParser

import tempfile
import json
import pytest
import io

@pytest.fixture
def parser():
    yield UCSDChargeMasterParser()

def test_ndc(parser):
    row = [{'PROCEDURE': '100','Code Type': 'ERX', 'Code': 'HCPCS 00002007', 'NDC': '00121-0657-11', 'Rev Code': '0250 - PHARMACY - GENERAL CLASSIFICATION', 'PROCEDURE_DESCRIPTION': 'ACETAMINOPHEN 160 MG/5ML OR SOLN', 'QUANTITY': '10.15 mL', 'IP_PRICE': '1.87',
           'REIMB_MIN': 'Variable', 'REIMB_MAX': 'Variable', 'KAISER SOUTH': '1.25', 'UC MC HBGFMD': '0.22', 'HEALTH NET HMO UNLISTED IPA ; HEALTH NET MID COUNTY PHY MED GRP ; HEALTH NET PPO': '1.42', 'BLUE CROSS UC CARE': '0.84', 'BLUE SHIELD PPO ; BLUE SHIELD OUT OF STATE BC/BS': '1.27', 'UHC WEST MID COUNTY PHY MED GRP': '1.23', 'BLUE CROSS DISTINCTION (TRANSPLANT)': '0', 'BLUE SHIELD SCRIPPS COASTAL MED GRP ; BLUE SHIELD HMO UNLISTED IPA ; BLUE SHIELD IMPERIAL COUNTY MED GRP ; BLUE SHIELD PCAMG': '1.27', 'UHC PPO ATLANTA GA ; UHC PPO SALT LAKE CITY UT': '0.91', 'GREAT WEST PPO ; CIGNA UNLISTED PPO': '1.24', 'BLUE SHIELD COVERED CALIFORNIA PPO': '0.99', 'UCSD STUDENT HEALTH': '0.87', 'NIPPON LIFE INSURANCE CO OF AMERICA ; AETNA HMO UNLISTED IPA ; AETNA MANAGED CHOICE ; AETNA SHARP COMMUNITY MED GRP ; AETNA UNLISTED PPO ; GEHA PO BOX 981707 ; MERITAIN HEALTH PO BOX 853921 ; AETNA CHOICE POS II': '1', 'UHC NAVIGATE': 'Variable', 'OPTUM TRANSPLANT': '0.97', 'HEALTH NET PRIMECARE RIVERSIDE MED GRP': '1.22', 'CIGNA LIFESOURCE': '1.12', 'BLUE CROSS SHARP COMMUNITY MED GRP ; BLUE CROSS SHARP REES STEALY': '1.23', 'UHC PPO QUALCOMM': '0.78', 'UHC WEST SHARP COMMUNITY MED GRP': '0.99', 'BLUE CROSS HOUSE STAFF PRUDENT BUYER': '0.84', 'BLUE CROSS SELECT PPO ; ANTHEM BLUE CROSS PPO PRUDENT BUYER ; BLUE CROSS OUT OF STATE BC/BS ; FEDERAL EMPLOYEES� - FEP ; SCRIPPS HEALTH COMP ; ANTHEM BLUE CROSS EPO': '0', 'AETNA PRIMECARE MED GROUP': '1.22'}]

    expected_reimbursement = {
        'KAISER SOUTH': 1.25,
        'UC MC HBGFMD': 0.22,
        'HEALTH NET HMO UNLISTED IPA': 1.42,
        'HEALTH NET MID COUNTY PHY MED GRP': 1.42,
        'HEALTH NET PPO': 1.42,
        'BLUE CROSS UC CARE': 0.84,
        'BLUE SHIELD PPO': 1.27,
        'BLUE SHIELD OUT OF STATE BC/BS': 1.27,
        'UHC WEST MID COUNTY PHY MED GRP': 1.23,
        'BLUE CROSS DISTINCTION (TRANSPLANT)': 0,
        'BLUE SHIELD SCRIPPS COASTAL MED GRP': 1.27,
        'BLUE SHIELD HMO UNLISTED IPA': 1.27,
        'BLUE SHIELD IMPERIAL COUNTY MED GRP': 1.27,
        'BLUE SHIELD PCAMG': 1.27,
        'UHC PPO ATLANTA GA': 0.91,
        'UHC PPO SALT LAKE CITY UT': 0.91,
        'GREAT WEST PPO': 1.24,
        'CIGNA UNLISTED PPO': 1.24, 
        'BLUE SHIELD COVERED CALIFORNIA PPO': 0.99,
        'UCSD STUDENT HEALTH': 0.87,
        'NIPPON LIFE INSURANCE CO OF AMERICA': 1.0,
        'AETNA HMO UNLISTED IPA': 1.0, 
        'AETNA MANAGED CHOICE': 1.0, 
        'AETNA SHARP COMMUNITY MED GRP': 1.0, 
        'AETNA UNLISTED PPO': 1.0, 
        'GEHA PO BOX 981707': 1.0, 
        'MERITAIN HEALTH PO BOX 853921': 1.0, 
        'AETNA CHOICE POS II': 1.0, 
        'OPTUM TRANSPLANT': 0.97,
        'HEALTH NET PRIMECARE RIVERSIDE MED GRP': 1.22,
        'CIGNA LIFESOURCE': 1.12,
        'BLUE CROSS SHARP COMMUNITY MED GRP': 1.23,
        'BLUE CROSS SHARP REES STEALY': 1.23, 
        'UHC PPO QUALCOMM': 0.78,
        'UHC WEST SHARP COMMUNITY MED GRP': 0.99,
        'BLUE CROSS HOUSE STAFF PRUDENT BUYER': 0.84,
        'BLUE CROSS SELECT PPO': 0.0,
        'ANTHEM BLUE CROSS PPO PRUDENT BUYER': 0,
        'BLUE CROSS OUT OF STATE BC/BS': 0,
        'FEDERAL EMPLOYEES - FEP': 0.0,
        'SCRIPPS HEALTH COMP': 0.0,
        'ANTHEM BLUE CROSS EPO': 0.0,
        'AETNA PRIMECARE MED GROUP': 1.22
    }


    expected_result = [
        ChargeMasterEntry(
            ndc_code = "00121-0657-11",
            hcpcs_code = "00002007",
            procedure_identifier = "100",
            nubc_revenue_code = "0250",
            procedure_description = "ACETAMINOPHEN 160 MG/5ML OR SOLN",
            plan = plan,
            expected_reimbursement = reimbursement,
            quantity = "10.15 mL",
        )
        for plan, reimbursement in expected_reimbursement.items()
    ]

    actual_result = list(parser.parse_artifacts({UCSDChargeMasterParser.ARTIFACT_URL : io.BytesIO(json.dumps(row).encode('utf-8'))}))
    assert sorted(expected_result) == sorted(actual_result)

def test_bad_quote_and_null(parser):
    row = """[{
        "PROCEDURE": "Where "Variable" exists, a rate may have been negotiated for this service, but the terms of reimbursement prevent the generation of a single fixed rate for this item or service package",
        "CODE_TYPE": null,
        "CODE": null,
        "NDC": null,
        "REV_CODE": null,
        "PROCEDURE_DESCRIPTION": null,
        "QUANTITY": null,
        "OP_PRICE": null,
        "REIMB_MIN": null,
        "REIMB_MAX": null,
        "AETNA BEHAVIORIAL HEALTH ": null,
        "AETNA MANAGED CHOICE ; AETNA UNLISTED PPO ; GEHA PO BOX 981707 ; MERITAIN HEALTH PO BOX 27267 ; MERITAIN HEALTH PO BOX 853921 ; AETNA CHOICE POS II ": null,
        "AFFORDABLE HEALTH ; ANTHEM BLUE CROSS PPO PRUDENT BUYER ; BLUE CROSS HMO UNLISTED IPA ; BLUE CROSS SCRIPPS COASTAL ; BLUE CROSS OUT OF STATE BC/BS ; FEDERAL EMPLOYEES  - FEP ; SCRIPPS HEALTH COMP ; ANTHEM BLUE CROSS EPO ; BLUE CROSS  IMPERIAL COUNTY MED G": null,
        "ANTHEM BLUE CROSS BH ": null,
        "BLUE CROSS HOUSE STAFF PRUDENT BUYER ": null,
        "BLUE CROSS UC CARE ": null,
        "BLUE SHIELD COVERED CALIFORNIA PPO ": null,
        "BLUE SHIELD HMO UNLISTED IPA ; BLUE SHIELD IMPERIAL COUNTY MED GRP ": null,
        "BLUE SHIELD MHSA BH ": null,
        "BLUE SHIELD OUT OF STATE BC/BS ; BLUE SHIELD PPO ": null,
        "CIGNA PPO PO BOX 182223 ; GREAT WEST PPO ; CIGNA UNLISTED PPO ; CIGNA PPO PO BOX 188061 ": null,
        "HEALTH NET COVERED CA PPO ": null,
        "HEALTH NET PPO ; HEALTH NET HMO UNLISTED IPA ; HEALTH NET COVERED CALIFORNIA PCAMG ; HEALTH NET COVERED CA HMO DIRECT NETWORK ": null,
        "KAISER NORTH ; KAISER SOUTH ": null,
        "KAISER RAD ONC ": null,
        "OPTUM EAP & BH ": null,
        "OPTUM TRANSPLANT ": null,
        "SHARP HEALTH PLAN SCMG ; SHARP HEALTH PLAN GRAYBILL MED GRP ; SHARP HEALTH PLAN SHARP REES STEALY ": null,
        "STUDENT RESOURCES ; UHC UNLISTED PPO ; UHC PPO ATLANTA GA ; UHC PPO SALT LAKE CITY UT ; UMR - PO BOX 30541 SALT LAKE CITY ": null,
        "UC MC CC33D5SKQ ": null,
        "UC MC HBGHFZ ; UC MC HBGJBI ": null,
        "UCSD STUDENT HEALTH ": null,
        "UHC NAVIGATE ": null,
        "UHC PPO QUALCOMM ": null,
        "UHC WEST MERCY PHY MED GRP ; UHC WEST SHARP REES STEALY ; UHC WEST SHARP COMMUNITY MED GRP ": null,
        "UNLISTED HMO NON CONTRACTED ; UNLISTED PPO NON CONTRACTED ": null
    }]""".strip()

    expected_result = []

    actual_result = list(parser.parse_artifacts({UCSDChargeMasterParser.ARTIFACT_URL : io.BytesIO(row.encode('utf-8'))}))
    assert sorted(expected_result) == sorted(actual_result)

def test_hcps(parser):
    row = [{"PROCEDURE":"183430","Code Type":"SUP","Code":"HCPCS C1889","NDC":"0278 - MEDICAL/SURGICAL SUPPLIES AND DEVICES - OTHER IMPLANT","Rev Code":"ROD TI STRAIGHT 4.0 X 240MM","PROCEDURE_DESCRIPTION":"1","QUANTITY":"509.96","IP_PRICE":"Variable","REIMB_MIN":"Variable","REIMB_MAX":"341.67","KAISER SOUTH":"Variable","UC MC HBGFMD":"Variable","HEALTH NET HMO UNLISTED IPA ; HEALTH NET MID COUNTY PHY MED GRP ; HEALTH NET PPO":"227.95","BLUE CROSS UC CARE":"227.95","BLUE SHIELD PPO ; BLUE SHIELD OUT OF STATE BC/BS":"257.53","UHC WEST MID COUNTY PHY MED GRP":"Variable","BLUE CROSS DISTINCTION (TRANSPLANT)":"227.95","BLUE SHIELD SCRIPPS COASTAL MED GRP ; BLUE SHIELD HMO UNLISTED IPA ; BLUE SHIELD IMPERIAL COUNTY MED GRP ; BLUE SHIELD PCAMG":"249.52","UHC PPO ATLANTA GA ; UHC PPO SALT LAKE CITY UT":"210.1","GREAT WEST PPO ; CIGNA UNLISTED PPO":"177.98","BLUE SHIELD COVERED CALIFORNIA PPO":"236.62","UCSD STUDENT HEALTH":"229.48","NIPPON LIFE INSURANCE CO OF AMERICA ; AETNA HMO UNLISTED IPA ; AETNA MANAGED CHOICE ; AETNA SHARP COMMUNITY MED GRP ; AETNA UNLISTED PPO ; GEHA PO BOX 981707 ; MERITAIN HEALTH PO BOX 853921 ; AETNA CHOICE POS II":"255.69","UHC NAVIGATE":"Variable","OPTUM TRANSPLANT":"Variable","HEALTH NET PRIMECARE RIVERSIDE MED GRP":"Variable","CIGNA LIFESOURCE":"257.53","BLUE CROSS SHARP COMMUNITY MED GRP ; BLUE CROSS SHARP REES STEALY":"198.12","UHC PPO QUALCOMM":"270.02","UHC WEST SHARP COMMUNITY MED GRP":"227.95","BLUE CROSS HOUSE STAFF PRUDENT BUYER":"Variable","BLUE CROSS SELECT PPO ; ANTHEM BLUE CROSS PPO PRUDENT BUYER ; BLUE CROSS OUT OF STATE BC/BS ; FEDERAL EMPLOYEES� - FEP ; SCRIPPS HEALTH COMP ; ANTHEM BLUE CROSS EPO":"331.47","AETNA PRIMECARE MED GROUP":""}]

    expected_reimbursement = {
        'AETNA CHOICE POS II': 255.69,
        'AETNA HMO UNLISTED IPA': 255.69,
        'AETNA MANAGED CHOICE': 255.69,
        'AETNA SHARP COMMUNITY MED GRP': 255.69,
        'AETNA UNLISTED PPO': 255.69,
        'ANTHEM BLUE CROSS EPO': 331.47,
        'ANTHEM BLUE CROSS PPO PRUDENT BUYER': 331.47,
        'BLUE CROSS DISTINCTION (TRANSPLANT)': 227.95,
        'BLUE CROSS OUT OF STATE BC/BS': 331.47,
        'BLUE CROSS SELECT PPO': 331.47,
        'BLUE CROSS SHARP COMMUNITY MED GRP': 198.12,
        'BLUE CROSS SHARP REES STEALY': 198.12,
        'BLUE CROSS UC CARE': 227.95,
        'BLUE SHIELD COVERED CALIFORNIA PPO': 236.62,
        'BLUE SHIELD HMO UNLISTED IPA': 249.52,
        'BLUE SHIELD IMPERIAL COUNTY MED GRP': 249.52,
        'BLUE SHIELD OUT OF STATE BC/BS': 257.53,
        'BLUE SHIELD PCAMG': 249.52,
        'BLUE SHIELD PPO': 257.53,
        'BLUE SHIELD SCRIPPS COASTAL MED GRP': 249.52,
        'CIGNA LIFESOURCE': 257.53,
        'CIGNA UNLISTED PPO': 177.98,
        'FEDERAL EMPLOYEES - FEP': 331.47,
        'GEHA PO BOX 981707': 255.69,
        'GREAT WEST PPO': 177.98,
        'HEALTH NET HMO UNLISTED IPA': 227.95,
        'HEALTH NET MID COUNTY PHY MED GRP': 227.95,
        'HEALTH NET PPO': 227.95,
        'MERITAIN HEALTH PO BOX 853921': 255.69,
        'NIPPON LIFE INSURANCE CO OF AMERICA': 255.69,
        'SCRIPPS HEALTH COMP': 331.47,
        'UCSD STUDENT HEALTH': 229.48,
        'UHC PPO ATLANTA GA': 210.1,
        'UHC PPO QUALCOMM': 270.02,
        'UHC PPO SALT LAKE CITY UT': 210.1,
        'UHC WEST SHARP COMMUNITY MED GRP': 227.95
    }

    expected_result = [
        ChargeMasterEntry(
                procedure_identifier = "183430",
                procedure_description = "ROD TI STRAIGHT 4.0 X 240MM",
                nubc_revenue_code = "0278",
                hcpcs_code = "C1889",
                max_reimbursement = 341.67,
                plan = plan,
                expected_reimbursement = reimbursement,
                quantity = "509.96"
        )
        for plan, reimbursement in expected_reimbursement.items()
    ]

    actual_result = list(parser.parse_artifacts({UCSDChargeMasterParser.ARTIFACT_URL : io.BytesIO(json.dumps(row).encode('utf-8'))}))
    assert sorted(expected_result) == sorted(actual_result)

def test_institution_name(parser):
    assert UCSDChargeMasterParser.institution_name == "UCSD"
    assert parser.institution_name == "UCSD"

def test_artifact_urls(parser):
    assert UCSDChargeMasterParser.artifact_urls == UCSDChargeMasterParser.ARTIFACT_URLS
    assert parser.artifact_urls == UCSDChargeMasterParser.ARTIFACT_URLS