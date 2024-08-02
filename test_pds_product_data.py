from __future__ import print_function

import copy

import requests
import ast
import time
import datetime
import calendar
import os
import json
import math


def monthdelta(date, delta):
    m, y = (date.month + delta) % 12, date.year + ((date.month) + delta - 1) // 12
    if not m: m = 12
    d = min(date.day, calendar.monthrange(y, m)[1])
    return date.replace(day=d, month=m, year=y)


def get_term_values(term):
    MMM_to_int = {name: num for num, name in enumerate(calendar.month_abbr) if num}

    if term.startswith("Q"):
        term = term.replace("Q1", "Mar")
        term = term.replace("Q2", "Jul")
        term = term.replace("Q3", "Sep")
        term = term.replace("Q4", "Dec")

    try:
        if "W" in term:
            term_list = term.split("-")
            term_year = "%02d" % (int(''.join(term_list[1])))
            term_month_raw = MMM_to_int[(''.join(list(term_list[0])[3:]))]
            term_month = "%02d" % (term_month_raw,)
            return {"year": term_year, "month": term_month}
        term_data = list(term)
        if term.isdigit():
            term_year = "%02d" % (int(''.join(term_data[-2:])))
            term_month = 00
            return {"year": term_year, "month": term_month}
        if len(term_data) < 7:
            term_year = "%02d" % (int(''.join(term_data[-2:])))
            term_month_raw = MMM_to_int[(''.join(term_data[:3]))]
            term_month = "%02d" % (term_month_raw,)
            return {"year": term_year, "month": term_month}
        else:
            term_year = int(''.join(term_data[:4]))
            term_month = "%02d" % (int(''.join(term_data[4:6])))
            return {"year": term_year, "month": term_month}
    except ValueError as e:
        print("ValueError: {}".format(""))
        return None
    except KeyError:
        print("KeyError: {}".format(term))
        return None


def get_alias_term_values(alias):
    MMM_to_int = {name: num for num, name in enumerate(calendar.month_abbr) if num}

    if alias.startswith("Q"):
        alias = alias.replace("Q1", "Mar")
        alias = alias.replace("Q2", "Jul")
        alias = alias.replace("Q3", "Sep")
        alias = alias.replace("Q4", "Dec")

    if "W" in alias:
        try:
            alias_list = alias.split("-") if "-" in str(alias) else alias.split(" ")
            alias_year = "%02d" % (int(''.join(alias_list[1]))) if int(''.join(alias_list[1])) > 22 else "%02d" % (int(''.join(alias_list[3])))
            alias_month_raw = MMM_to_int[(''.join(list(alias_list[0])[3:]))] if (len(alias_list[0]) == 3 and alias_list[0].isdigit == False) else MMM_to_int[(''.join(list(alias_list[2])))]
            alias_month = "%02d" % (alias_month_raw,) if int("%02d" % (alias_month_raw,)) <= 12 else"%02d" % (int(''.join(alias_list[1])))
            return {"year": alias_year, "month": alias_month}
        except:
            print("get_alias_term_values Error: {}".format(alias))

    if len(alias.split("-")) > 1:
        alias = alias.split("-")[0]

    term_data = [" ", alias] if len(alias) == 5 else alias

    if len(term_data) == 2 or len(term_data) == 3:
        mmmyy_list = list(term_data[1])
        term_year = "%02d" % (int(''.join(mmmyy_list[-2:])))  #  if len(term_data[3]) >= 3 else (int(term_data[1]))
        term_month = "%02d" % MMM_to_int[''.join(mmmyy_list[:3])]
        return {"year": term_year, "month": term_month}
    elif len(term_data.split(" ")) > 4:
        term_year = int(''.join(list(term_data)[12:14]))
        term_month = "%02d" % (int(''.join(list(term_data)[5:7])))
        return {"year": term_year, "month": term_month}
    else:
        try:
            term_year = int(''.join(list(term_data)[:4]))
            term_month = "%02d" % (int(''.join(list(term_data)[4:6])))
            return {"year": term_year, "month": term_month}
        except:
            term_year = int("20" + ''.join(list(term_data)[-2:]))
            term_month_raw = MMM_to_int[(''.join(term_data.split(" ")[1][0:3]))]
            term_month = "%02d" % (term_month_raw,)
            return {"year": term_year, "month": term_month}


def get_date_values(date):

    try:
        data = list(str(date))
        year = int("".join(data[:4]))
        month = int("".join(data[4:6]))
        day = int("".join(data[-2:]))
        return datetime.datetime(year, month, day)
    except ValueError as e:
        print("ValueError: {}".format(""))
        return None


def get_tocom_contract_month(sec_id):
    try:
        contract_month_data = list(sec_id.split("_")[-1])
        contract_year = "%02d" % (int(''.join(contract_month_data[:2])),)
        contract_month = "%02d" % (int(''.join(contract_month_data[2:4]).zfill(2)),)
        contract_day = "%02d" % (int(''.join(contract_month_data[4:6]).zfill(2)),)
        yyyymmdd = int("".join(("20" + str(contract_year), str(contract_month), str(contract_day))))
        return {"year": contract_year, "month": contract_month, "day": contract_day, "yyyymmdd": yyyymmdd}
    except ValueError as e:
        print("ValueError: {}".format(""))
        return None


class TestPDSData:
    """Various PDS test tools to provide test coverage for odds & ends and one-off PDS tests

    To use, pick the module you want to run and update the runme line at the bottom to execute it directly.
    This class does not require the nimbus framework. Use __init__ to configure your test.

    pdsdomain       Environment where the test will run
    market          Market that will be tested
    prod_list       List of products (product code format) that will be tested; leave empty to test all products
    product_types   Product Types / Security Types that will be tested
    debug           Debug logging
    """

    def __init__(self):

        self.debug = False

        self.pdsdomain = "int-stage-cert"
        self.market = "SGX"
        self.market_stats = {0: {}, 1: {}}

        pds_url = "".join(["https://pds-", self.pdsdomain, ".trade.tt"])
        self.base_url = pds_url

        self.headers = {'content-type': 'application/json'}

        self.product_types = self.get_product_type_dict()
        # self.product_types = {34: 'FUT'}  # , 43: 'MLEG'}  # 34: 'FUT', 43: 'MLEG', 51: 'OPT', 43: MLEG, 77: TBOND, 200: STRA, 203: CUR}
        self.all_products = []
        self.all_product_ids = []
        self.all_instrument_ids = []
        self.all_instrument_overview = []
        self.all_sec_exch_ids = {}
        self.month_codes = {'F': '01', 'G': '02', 'H': '03', 'J': '04', 'K': '05', 'M': '06',
                            'N': '07', 'Q': '08', 'U': '09', 'V': '10', 'X': '11', 'Z': '12'}

        # ndaqeu_to_nasdaqned_futures.csv
        # self.prod_list = ["8TRA", "F8TRA", "AAK", "FAAK", "ABB", "FABB", "AKERBP", "FAKERB", "AKSO", "FAKSO", "ALFA", "FALFA", "ASSAB", "FASSAB", "ATCOA", "FATCOA", "AXFO", "FAXFO", "AZN", "FAZN", "BAKKA", "FBAKKA", "BALDB", "FBALDB", "BETSB", "FBETSB", "BILL", "FBILL", "BOLI", "FBOLI", "CARLB", "FCARLB", "CAST", "FCAST", "CHR", "FCHR", "COLOB", "FCOLOB", "DANSKE", "FDANSK", "DNB", "FDNBN", "DNO", "FDNO", "DNORD", "FDNORD", "DOM", "FDOM", "DSV", "FDSV", "EKTAB", "FEKTAB", "ELUXB", "FELUXB", "EMBRAC", "FEMBRA", "EPIA", "FEPIA", "EQNR", "FEQNR", "EQT", "FEQT", "ERICB", "FERICB", "ESSITB", "FESSIT", "EVO", "FEVO", "FABG", "FFABG", "FINGB", "FFINGB", "FLS", "FFLS", "FRO", "FFRO", "GEN", "FGEN", "GETIB", "FGETIB", "GJF", "FGJFN", "GN", "FGN", "HEXB", "FHEXB", "HMB", "FHMB", "HOLMB", "FHOLMB", "HPOL", "FHPOL", "HUSQB", "FHUSQB", "ICA", "FICA", "IJ", "FIJ", "INDUC", "FINDUC", "INVEB", "FINVEB", "ISS", "FISS", "JM", "FJM", "JYSK", "FJYSK", "KINB", "FKINB", "KIND", "FKIND", "LUMI", "FLUMI", "LUN", "FLUN", "LUPE", "FLUPE", "MAERSK", "FMAERS", "MOWI", "FMOWI", "MTGB", "FMTGB", "NAS", "FNAS", "NCC", "FNCC", "NDASE", "FNDASE", "NHY", "FNHYN", "NIBE", "FNIBE", "NOD", "FNOD", "NOKI", "FNOKIA", "NOVOB", "FNOVOB", "NZYMB", "FNZYMB", "OMXC25", "FXC25", "OMXDIV", "FXDIV", "OMXESG", "FXESG", "OMXO20", "FXO20", "OMXS30", "FXS30", "OMXSB", "FMXSB", "ORK", "FORKN", "ORSTED", "FORSTE", "PCELL", "FPCELL", "PGS", "FPGSN", "PNDORA", "FPNDOR", "REC", "FRECN", "S30MIN", "F0MIN", "SAAB", "FSAAB", "SAND", "FSAND", "SAS", "FSAS", "SCAB", "FSCAB", "SCHA", "FSCHA", "SEBA", "FSEBA", "SECUB", "FSECUB", "SHBA", "FSHBA", "SKAB", "FSKAB", "SKFB", "FSKFB", "SOBI", "FSOBI", "SSABA", "FSSABA", "STB", "FSTBN", "STER", "FSTER", "SUBC", "FSUBCN", "SWEDA", "FSWEDA", "SWMA", "FSWMA", "SYDB", "FSYDB", "TEL", "FTELN", "TEL2B", "FTEL2B", "TGS", "FTGS", "TIGO", "FTIGO", "TLSN", "FTLSN", "TRELB", "FTRELB", "TRYG", "FTRYG", "VINX30", "FNX30", "VOLVB", "FVOLVB", "VWS", "FVWS", "WDH", "FWDH", "XXL", "FXXL", "YAR", "FYARN"]
        # ndaqeu_to_nasdaqned_options.csv
        # self.prod_list = ["8TRA", "O8TRA", "AAK", "OAAK", "ABB", "OABB", "ALFA", "OALFA", "ASSAB", "OASSAB", "ATCOA", "OATCOA", "AXFO", "OAXFO", "AZN", "OAZN", "BALDB", "OBALDB", "BETSB", "OBETSB", "BILL", "OBILL", "BOLI", "OBOLI", "CARLB", "OCARLB", "CAST", "OCAST", "CHR", "OCHR", "COLOB", "OCOLOB", "DANSKE", "ODANSK", "DNORD", "ODNORD", "DOM", "ODOM", "DSV", "ODSV", "EKTAB", "OEKTAB", "ELUXB", "OELUXB", "EMBRAC", "OEMBRA", "EPIA", "OEPIA", "EQNR", "OEQNR", "EQT", "OEQT", "ERICB", "OERICB", "ESSITB", "OESSIT", "EVO", "OEVO", "FABG", "OFABG", "FINGB", "OFINGB", "FLS", "OFLS", "GEN", "OGEN", "GETIB", "OGETIB", "GN", "OGN", "HEXB", "OHEXB", "HMB", "OHMB", "HOLMB", "OHOLMB", "HPOL", "OHPOL", "HUH1V", "OHUH1V", "HUSQB", "OHUSQB", "ICA", "OICA", "IJ", "OIJ", "INDUC", "OINDUC", "INVEB", "OINVEB", "ISS", "OISS", "JM", "OJM", "JYSK", "OJYSK", "KINB", "OKINB", "KIND", "OKIND", "KRA1V", "OKRA1V", "LUMI", "OLUMI", "LUN", "OLUN", "LUPE", "OLUPE", "MAERSK", "OMAERS", "METSB", "OMETSB", "MOCORP", "OMOCOR", "MTGB", "OMTGB", "NCC", "ONCC", "NDASE", "ONDASE", "NELES", "ONELES", "NHY", "ONHYN", "NIBE", "ONIBE", "NOKI", "ONOKIA", "NOKIA", "ONOKIA", "NOVOB", "ONOVOB", "NRE1V", "ONRE1V", "NZYMB", "ONZYMB", "OMXC25", "OXC25", "OMXO20", "OXO20", "OMXS30", "OXS30", "ORSTED", "OORSTE", "OUT1V", "OOUT1V", "PCELL", "OPCELL", "PNDORA", "OPNDOR", "SAAB", "OSAAB", "SAND", "OSAND", "SAS", "OSAS", "SCAB", "OSCAB", "SEBA", "OSEBA", "SECUB", "OSECUB", "SHBA", "OSHBA", "SKAB", "OSKAB", "SKFB", "OSKFB", "SOBI", "OSOBI", "SSABA", "OSSABA", "STER", "OSTER", "SWEDA", "OSWEDA", "SWMA", "OSWMA", "SYDB", "OSYDB", "TEL2B", "OTEL2B", "TIGO", "OTIGO", "TLSN", "OTLSN", "TRELB", "OTRELB", "TRYG", "OTRYG", "VOLVB", "OVOLVB", "VWS", "OVWS", "WDH", "OWDH", "WRT1V", "OWRT1V", "XACT", "OXACT", "YTY1V", "OYTY1V"]
        # ndaqeu_to_nasdaqned_others.csv
        self.prod_list = ["ZIHF", ]  # , "SBM", "SBN", "SBP", "SBQ", "SBS", "SBT", "SBV", "SBW", "SBX", "SBY", "SBZ", "SC0", "SC1", "SC2", "SC3", "SC4", "SC5", "SC6", "SC7", "SC8", "SC9", "SCA", "SCB", "SCC", "SCD", "SCE", "SCF", "SCG", "SCJ", "SCK", "SCL", "SCN", "SCP", "SCQ", "SCR", "SCS", "SCT", "SCV", "SCW", "SCX", "SCY", "SCZ", "SD0", "SD1", "SD2", "SD3", "SD4", "SD5", "SD6", "SD7", "SD8", "SD9", "SDA", "SDB", "SDC", "SDD", "SDE", "SDG", "SDH", "SDJ", "SDK", "SDL", "SDM", "SDN", "SDP", "SDR", "SDT", "SDV", "SDW", "SDY", "SDZ", "SE0", "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE8", "SE9", "SEA", "SEB", "SEC", "SED", "SEE", "SEF", "SEG", "SEH", "SEJ", "SEK", "SEL", "SEM", "SEN", "SEP", "SEQ", "SER", "SES", "SET", "SEV", "SEW", "SEX", "SEY", "SEZ", "SF0", "SF1", "SF2", "SF3", "SF4", "SF5", "SF6", "SF7", "SF8", "SF9", "SFA", "SFB", "SFC", "SFD", "SFE", "SFF", "SFG", "SFH", "SFJ", "SFK", "SFL", "SFM", "SFN", "SFP", "SFQ"]  # "EY", "EYO", "O3", "O3O"]  # "CX01F", "CX03F", "CX11F", "CX13F"]  # "8TRA_C", "28TRA", "8TRA_F", "W8TRA", "AAK_C", "2AAK", "AAK_F", "WAAK", "ABB_C", "2ABB", "ABB_F", "WABB", "AKERBP_C", "2AKERB", "AKERBP_F", "WAKERB", "AKSO_C", "2AKSO", "AKSO_F", "WAKSO", "ALFA_C", "2ALFA", "ALFA_F", "WALFA", "ASSAB_C", "2ASSAB", "ASSAB_F", "WASSAB", "ATCOA_C", "2ATCOA", "ATCOA_F", "WATCOA", "AXFO_C", "2AXFO", "AXFO_F", "WAXFO", "AZN_C", "2AZN", "AZN_F", "WAZN", "BAKKA_C", "2BAKKA", "BAKKA_F", "WBAKKA", "BALDB_C", "2BALDB", "BALDB_F", "WBALDB", "BETSB_C", "2BETSB", "BETSB_F", "WBETSB", "BILL_C", "2BILL", "BILL_F", "WBILL", "BOLI_C", "2BOLI", "BOLI_F", "WBOLI", "CARLB_C", "2CARLB", "CAST_C", "2CAST", "CAST_F", "WCAST", "CHR_C", "2CHR", "COLOB_C", "2COLOB", "DANSKE_C", "2DANSK", "DNB_C", "2DNBN", "DNB_F", "WDNBN", "DNORD_C", "2DNORD", "DNO_C", "2DNO", "DNO_F", "WDNO", "DOM_C", "2DOM", "DOM_F", "WDOM", "DSV_C", "2DSV", "EKTAB_C", "2EKTAB", "EKTAB_F", "WEKTAB", "ELI1V_F", "WELI1V", "ELUXB_C", "2ELUXB", "ELUXB_F", "WELUXB", "EMBRAC_C", "2EMBRA", "EMBRAC_F", "WEMBRA", "EPIA_C", "2EPIA", "EPIA_F", "WEPIA", "EQNR_C", "2EQNR", "EQNR_F", "WEQNR", "EQT_C", "2EQT", "EQT_F", "WEQT", "ERICB_C", "2ERICB", "ERICB_F", "WERICB", "ESSITB_C", "2ESSIT", "ESSITB_F", "WESSIT", "EVO_C", "2EVO", "EVO_F", "WEVO", "FABG_C", "2FABG", "FABG_F", "WFABG", "FINGB_C", "2FINGB", "FINGB_F", "WFINGB", "FLS_C", "2FLS", "FRO_C", "2FRO", "FRO_F", "WFRO", "FUM1V_F", "WFUM1V", "GEN_C", "2GEN", "GETIB_C", "2GETIB", "GETIB_F", "WGETIB", "GJF_C", "2GJFN", "GJF_F", "WGJFN", "GN_C", "2GN", "HEXB_C", "2HEXB", "HEXB_F", "WHEXB", "HMB_C", "2HMB", "HMB_F", "WHMB", "HOLMB_C", "2HOLMB", "HOLMB_F", "WHOLMB", "HPOL_C", "2HPOL", "HPOL_F", "WHPOL", "HUH1V_F", "WHUH1V", "HUSQB_C", "2HUSQB", "HUSQB_F", "WHUSQB", "ICA_C", "2ICA", "ICA_F", "WICA", "IJ_C", "2IJ", "IJ_F", "WIJ", "INDUC_C", "2INDUC", "INDUC_F", "WINDUC", "INVEB_C", "2INVEB", "INVEB_F", "WINVEB", "ISS_C", "2ISS", "JM_C", "2JM", "JM_F", "WJM", "JYSK_C", "2JYSK", "KINB_C", "2KINB", "KINB_F", "WKINB", "KIND_C", "2KIND", "KIND_F", "WKIND", "KNEBV_F", "WKNEBV", "KRA1V_F", "WKRA1V", "LUMI_C", "2LUMI", "LUMI_F", "WLUMI", "LUN_C", "2LUN", "LUPE_C", "2LUPE", "LUPE_F", "WLUPE", "MAERSK_C", "2MAERS", "METSB_F", "WMETSB", "MOCORP_F", "WMOCOR", "MOWI_C", "2MOWI", "MOWI_F", "WMOWI", "MTGB_C", "2MTGB", "MTGB_F", "WMTGB", "NAS_C", "2NAS", "NAS_F", "WNAS", "NCC_C", "2NCC", "NCC_F", "WNCC", "NDAFI_F", "WNDAFI", "NDASE_C", "2NDASE", "NDASE_F", "WNDASE", "NELES_F", "WNELES", "NESTE_F", "WNESTE", "NHY_C", "2NHYN", "NHY_F", "WNHYN", "NIBE_C", "2NIBE", "NIBE_F", "WNIBE", "NOD_C", "2NOD", "NOD_F", "WNOD", "NOK1V_F", "WNOK1V", "NOKI_C", "2NOKIA", "NOKI_F", "WNOKIA", "NOVOB_C", "2NOVOB", "NRE1V_F", "WNRE1V", "NZYMB_C", "2NZYMB", "ORK_C", "2ORKN", "ORK_F", "WORKN", "ORSTED_C", "2ORSTE", "OUT1V_F", "WOUT1V", "PCELL_C", "2PCELL", "PCELL_F", "WPCELL", "PGS_C", "2PGSN", "PGS_F", "WPGSN", "PNDORA_C", "2PNDOR", "REC_C", "2RECN", "REC_F", "WRECN", "SAAB_C", "2SAAB", "SAAB_F", "WSAAB", "SAMAS_F", "WSAMAS", "SAND_C", "2SAND", "SAND_F", "WSAND", "SAS_C", "2SAS", "SAS_F", "WSAS", "SCAB_C", "2SCAB", "SCAB_F", "WSCAB", "SCHA_C", "2SCHA", "SCHA_F", "WSCHA", "SEBA_C", "2SEBA", "SEBA_F", "WSEBA", "SECUB_C", "2SECUB", "SECUB_F", "WSECUB", "SHBA_C", "2SHBA", "SHBA_F", "WSHBA", "SKAB_C", "2SKAB", "SKAB_F", "WSKAB", "SKFB_C", "2SKFB", "SKFB_F", "WSKFB", "SOBI_C", "2SOBI", "SOBI_F", "WSOBI", "SSABA_C", "2SSABA", "SSABA_F", "WSSABA", "STB_C", "2STBN", "STB_F", "WSTBN", "STERV_F", "WSTERV", "STER_C", "2STER", "STER_F", "WSTER", "SUBC_C", "2SUBCN", "SUBC_F", "WSUBCN", "SWEDA_C", "2SWEDA", "SWEDA_F", "WSWEDA", "SWMA_C", "2SWMA", "SWMA_F", "WSWMA", "SYDB_C", "2SYDB", "TEL2B_C", "2TEL2B", "TEL2B_F", "WTEL2B", "TEL_C", "2TELN", "TEL_F", "WTELN", "TGS_C", "2TGS", "TGS_F", "WTGS", "TIE1V_F", "WTIE1V", "TIGO_C", "2TIGO", "TIGO_F", "WTIGO", "TLS1V_F", "WTLS1V", "TLSN_C", "2TLSN", "TLSN_F", "WTLSN", "TRELB_C", "2TRELB", "TRELB_F", "WTRELB", "TRYG_C", "2TRYG", "UPM1V_F", "WUPM1V", "VOLVB_C", "2VOLVB", "VOLVB_F", "WVOLVB", "VWS_C", "2VWS", "WDH_C", "2WDH", "WRT1V_F", "WWRT1V", "XXL_C", "2XXL", "XXL_F", "WXXL", "YAR_C", "2YARN", "YAR_F", "WYARN", "YTY1V_F", "WYTY1V"]

        # self.prod_list = ["OM-PT|OM-GD", "GLDM|PLTM", "OPTCD|OGDCD", "GLDD|PLTD",
        #                    "OTSR2|ORSS3", "RSS3|TSR2", "CKER|CGAS", "CGAS|CKRO", "CRUD|GASO", "GAS|DBAI",
        #                    "CRUD|GSOL", "GAO|DBAI", "CRUD|KERO", "KRO|DBAI", "GSOL|GASO", "GAS|GAO",
        #                    "GSOL|KERO", "KRO|GAO", "KERO|GASO", "GAS|KRO", "TWBL|TEBL", "EEB|EWB",
        #                    "TWPL|TEPL", "EEP|EWP"]
        # self.prod_list = ["JGBL", "JBL", "TWBL", "EWB", "TEBL", "EEB", "TWPL", "EWP", "TEPL", "EEP", "OTGCN", "CORN",
        #                   "FTC50", "FT50", "CGAS", "CKER", "CKRO", "GSOL", "GAO", "GASO", "GAS", "KERO", "KRO",
        #                   "NKDIV", "NKDV", "CRUD", "DBAI", "TPX30", "C30", "TPDIV", "OTSR2", "TSR2"]
        # self.prod_list = ["GASO", "GAS", "KERO", "KRO", "GSOL", "GAO", "CRUD", "DBAI", "CKER", "CKRO", "TWBL", "EWB",
        #                   "TEBL", "EEB", "TWPL", "EWP", "TEPL", "EEP", "TBGA", "TBGO", "TBKE", "TLGA", "TLGO", "TLKE"]

    def get_combo_type_dict(self):

        combo_type_dict = {}

        combo_type_url = self.base_url + "/api/1/systemdata?type=instrument&request_id=pds_market_explorer-pds-int-dev-cert.trade.tt--9942abfa-3459-46dd-a88d-32488fbe6c85"
        request = requests.get(combo_type_url, headers=self.headers)
        output = request._content
        full_output = ast.literal_eval(output)
        all_combo_types = full_output["data"]["instrumentData"]["comboTypes"]
        for combo_type in all_combo_types:
            combo_type_dict[combo_type["i"]] = combo_type["n"]

        return combo_type_dict

    def get_product_type_dict(self):

        product_type_dict = {}

        product_type_url = self.base_url + "/api/1/systemdata?type=producttype"
        request = requests.get(product_type_url, headers=self.headers)
        output = request._content
        full_output = ast.literal_eval(output)
        all_product_types = full_output["data"]["productData"]["prodTypes"]
        for product_type in all_product_types:
            product_type_dict[product_type["i"]] = product_type["n"]

        return product_type_dict

    def get_third_wed_of_every_month(self, year):

        current_year = year
        third_wednesdays = []

        for month in range(1, 13):

            first_day_of_month_datestamp = datetime.date(current_year, month, 1)
            first_weekday_of_month = datetime.date.weekday(first_day_of_month_datestamp)

            if first_weekday_of_month == 2:
                weekday1 = first_day_of_month_datestamp + datetime.timedelta(14)
            elif first_weekday_of_month > 2:
                weekday1 = first_day_of_month_datestamp - datetime.timedelta(first_weekday_of_month - 2)
                if datetime.date.timetuple(weekday1)[1] < month:
                    weekday1 = weekday1 + datetime.timedelta(7)
                weekday1 = weekday1 + datetime.timedelta(14)
            elif first_weekday_of_month < 2:
                weekday1 = first_day_of_month_datestamp + datetime.timedelta(2 - first_weekday_of_month)
                weekday1 = weekday1 + datetime.timedelta(14)

            datestamp = '/'.join([str(weekday1).split('-')[1],
                                  str(weekday1).split('-')[2],
                                  str(weekday1).split('-')[0]])

            third_wednesdays.append(datestamp)

        return third_wednesdays

    def parse_pds_output(self, url, http_request=True):
        if http_request:
            request_successful = False
            output = None
            request_attempt_count = 1
            while not request_successful:
                if request_attempt_count == 60:
                    print("= "*40)
                    print("All attempts to get data from the following url have been failing for the past 20 minutes!")
                    print("Giving up. Error code = {}".format(request.status_code))
                    print(url)
                    print("= "*40)
                    break
                try:
                    request = requests.get(url, headers=self.headers)
                except:
                    print("ERROR :" + url)
                request_successful = True if request.status_code == 200 else False
                if not request_successful:
                    time.sleep(20)
                request_attempt_count += 1
            output = request._content
        else:
            output = url

        while ":false" in output:
            output = output.replace(":false", ":\"false\"")
        while ":true" in output:
            output = output.replace(":true", ":\"true\"")
        try:
            full_output = ast.literal_eval(output)
        except:
            print(output)
            assert("^^ ERROR! ^^")
        if len(full_output) > 9:
            output = full_output
        else:
            try:
                output = full_output["instruments"]
            except:
                try:
                    output = full_output["products"]
                except:
                    try:
                        output = full_output["data"]["globalData"]["markets"]
                    except:
                        try:
                            output = full_output["product"]
                        except:
                            try:
                                output = full_output["instrument"]
                            except:
                                try:
                                    output = full_output["data"]["globalData"]["secExch"]
                                except:
                                    try:
                                        output = full_output["data"]["productData"]["currencies"]
                                    except:
                                        try:
                                            output = full_output["records"]
                                        except:
                                            try:
                                                # output = full_output["count"]
                                                output = full_output["answers"]
                                            except:
                                                pass

        return output

    def get_market_id(self, market):

        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        for market_id in market_ids:
            if market == market_id["n"]:
                return str(market_id["i"])
        else:
            print("Market, \"{0}\" does not seem to exist.".format(market))

    def get_time_tuple(self, date_str):

        try:
            pattern = '%Y-%m-%d %H:%M:%S'
            date_list = list(str(date_str))
            year = ''.join(date_list[0:4])
            month = ''.join(date_list[4:6])
            day = 1 if len(date_list) == 6 else ''.join(date_list[6:])
            if len(day) > 2:
                day = ''.join(list(day)[:2])
            try:
                d2 = datetime.datetime(int(year), int(month), int(day), 0, 0, 0, 0)
            except ValueError as e:
                print("ValueError: {}".format((year, month, day, 0, 0, 0, 0)))
                print("\n{}".format(date_str))
            time_tuple = time.localtime(time.mktime(time.strptime("{}".format(d2), pattern)))
        except ValueError as e:
            print("ValueError:\n{}".format(date_str))
            return list("NoneNone")

        return time_tuple

    def get_all_product_ids(self, dev=False):

        if dev:
            self.market = "_".join((self.market, "DEV"))
        else:
            self.market = self.market

        if "market" not in self.market_stats[0]:
            self.market_stats[0]["market"] = self.market
        else:
            self.market_stats[1]["market"] = self.market

        for product_type in self.product_types:
            base_url = "".join(["https://pds-", self.pdsdomain, ".trade.tt"])
            prod_url = base_url + "/api/1/products?marketIds=" + self.get_market_id(self.market) + \
                       "&productTypeIds=" + str(product_type) + "&slim=false"
            products = self.parse_pds_output(prod_url)

            self.all_products.extend(products)

            for product in products:
                if not product['s'].isdigit():
                    if len(self.prod_list) > 0:
                        for item in self.prod_list:
                            if product["s"].split(" ")[0].startswith(item):
                                if len(item) == len(product["s"].split(" ")[0]):
                                    self.all_product_ids.append(str(product["i"]))
                    else:
                        self.all_product_ids.append(str(product["i"]))

        if "market" in self.market_stats[0] and "market" not in self.market_stats[1]:
            self.market_stats[0]["product_count"] = len(self.all_product_ids)
        else:
            self.market_stats[1]["product_count"] = len(self.all_product_ids)

            # for product in products:
            #     if product['s'].isdigit() and product['s'] in ["225", "400", "8801"]:
            #         if len(self.prod_list) > 0:
            #             for item in self.prod_list:
            #                 if product["s"].split(" ")[0].startswith(item):
            #                     if len(item) == len(product["s"].split(" ")[0]):
            #                         self.all_product_ids.append(str(product["i"]))
            #         else:
            #             self.all_product_ids.append(str(product["i"]))

    def get_all_instrument_ids(self):

        get_product_id = self.product_id_generator()

        while True:
            try:
                product_id = str(next(get_product_id))

                instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id + "&slim=false"
                instrument_list = self.parse_pds_output(instr_list_url)
                for instrument in instrument_list:
                    self.all_instrument_ids.append(str(instrument["i"]))
                    self.all_instrument_overview.append(instrument)
            except StopIteration as e:
                break

    def get_security_exch_ids(self):

        market_id = self.get_market_id(self.market)

        sec_exch_list_url = self.base_url + "/api/1/systemdata?type=securityexchange"
        sec_exch_list = self.parse_pds_output(sec_exch_list_url)
        for sec_exch in sec_exch_list:
            if sec_exch["m"] == int(market_id):
                self.all_sec_exch_ids[sec_exch["i"]] = sec_exch["n"]
        pass

    def product_id_generator(self):
        """Pass product id of the current product to be analysed."""
        for product_id in self.all_product_ids:
            yield product_id

    def instrument_id_generator(self):
        """Pass instrument id of the current instrument to be analysed."""
        for instrument_id in self.all_instrument_ids:
            yield instrument_id

    def instrument_overview_generator(self):
        """Pass instrument id of the current instrument to be analysed."""
        for instrument_overview in self.all_instrument_overview:
            yield instrument_overview

    def translate_instrument_data(self, instrument):

        # instrument_definition = {"Alias": "a", "name": "n", "exp_date": "exp", "product_type": "pt",
        #                          "last_trading_date": "l", "maturity_date": "e", "RIC_Code": "ric", "SecurityId": "d",
        #                          "strike": "x", "term": "term", "tick_size": "ts", "product_name": "ps",
        #                          "Combination_Type": "c"}

        instrument_definition = {"Name": "n", "Alias": "a", "Id": "i", "ProductId": "p", "MarketId": "m",
                                 "MaturityDate": "e", "Strike": "x", "OptionCodeId": "oc", "SeriesKey": "sk",
                                 "UserDefined": "ud", "CTDisplayOrder": "cdo", "PTDisplayOrder": "pdo",
                                 "ProductTypeId": "pt", "ModRevision": "rev", "IsEphemeral": "eph", "ISIN": "isn",
                                 "SyntheticTag": "stag", "State": "state", "StateAttrib": "stateAttrib", "Symbol": "s",
                                 "SecurityId": "d", "UnderId": "uii", "VersionId": "iv", "ProductVersionId": "pv",
                                 "SymbolSfx": "ss", "StartDate": "st", "LastTradingDate": "l", "TickValue": "tv",
                                 "TickSize": "ts", "PointValue": "v", "DisplayFactor": "f", "MinTradeVol": "mv",
                                 "MaxTradeVol": "xv", "QOfMeasure": "qm", "UOfMeasure": "um", "MDepth": "md",
                                 "IDepth": "id", "ComboTypeId": "c", "OptionSchemeId": "os", "StrikeCurrencyId": "xc",
                                 "ExpiryId": "et", "TenorId": "tt", "Tenor": "t", "SupportsImplieds": "si",
                                 "TradesInFlow": "tf", "DeliveryId": "di", "DispFormatId": "df", "TickTableId": "tk",
                                 "MatchAlgo": "ma", "IsDaily": "dp", "NumBlocks": "nb", "OrigCSize": "cs",
                                 "ContMult": "cm", "MinLotSize": "ls", "MainFraction": "mf", "SubFraction": "sf",
                                 "PriceDec": "pd", "TickSizeNum": "tn", "TickSizeDenom": "td", "CalcImplieds": "ci",
                                 "PriorityMin": "pmn", "PriorityMax": "pmx", "SeriesTerm": "te",
                                 "MarketSegmentId": "msi", "RoundLotQty": "rlq", "IsDeleted": "del",
                                 "DecShiftQty": "dsq", "DecShiftPrc": "dsp", "RICCode": "ric",
                                 "FirstDeliveryDate": "fdd", "ProductSymbol": "ps", "SecurityExchangeId": "se",
                                 "PriceTopic": "ptop", "LockMask0": "lck0", "PriceDisplayTypeId": "pdt",
                                 "CouponRate": "cr", "IsNotTradable": "notrd", "StepSize": "ssi", "FunctionId": "fi",
                                 "ContractInfo": "cin", "Term": "term", "LockMask1": "lck1", "ValueDate": "vd",
                                 "PriceRatio": "pr", "ExChannelId": "excid", "ProductCurrencyType": "pc",
                                 "RollingAlias": "ra", "StepSizeMultiple": "ssim", "ProductImpliedRules": "pir",
                                 "ExchangeTicker": "excht", "CFICode": "cfi", "PromptType": "ptype",
                                 "RollingPromptDate": "rpd", "linkedInstrumentId": "lii", "ExpiryDate": "exp",
                                 "dui": "400", "TermDate": "termd", "DisplayFactorStr": "fs", "ProductFamilyId": "pfi",
                                 "PriceFormula": "pf", "SyntheticId": "sii", "OpaqueData": "od", "UserId": "uui",
                                 "SynInstrIsDeleted": "siidel", "IsPriceInTicks": "pit", "SynInstrState": "siistate",
                                 "UpdateTS": "uts", "UpdateSource": "ups", "UniName": "un", "DeliveryUnit": "du",
                                 "InsertTS": "its", "MetaData": "data", "AliasType": "at", "SequenceId": "seq",
                                 "LegListId": "lli", "BloombergCode": "bbc", "BloombergExchangeCode": "bec",
                                 "OpenFIGICode": "ofc", "IsShared": "isShared",
                                 "SharedToCompanyId": "sharedToCompanyId"}

        if "term" not in instrument:
            instrument_definition["Term"] = "lt"

        for k, v in instrument_definition.items():
            if v not in instrument:
                instrument_definition[k] = None
            if instrument_definition[k] is not None:
                try:
                    if v == "exp":
                        instrument_definition[k] = str(instrument[v]).replace("000000", "")
                    elif v == "e":
                        instrument_definition[k] = str(instrument[v])
                    else:
                        instrument_definition[k] = instrument[v]
                except TypeError as e:
                    print("instrument_definition TypeError:", k, v)

        if "data" in instrument:
            try:
                data = "".join(instrument["data"])
                metadata = ast.literal_eval(data)
                for k, v in metadata.items():
                    instrument_definition[k] = v
            except:
                data = instrument["data"].split(",")
                for data_item in data:
                    if len(data_item) > 0:
                        instrument_definition[data_item.split("=")[0]] = data_item.split("=")[1]

        return instrument_definition

    def translate_product_data(self, product):

        # product_definition = {"Symbol": "s", "Name": "n", "MIC_Code": "mc", "Currency": "c", "Security_Type": "t",
        #                       "Security_Exchange": "x", "Asset_Class": "ass"}

        product_definition = {"MarketId": "m", "Id": "i", "FamilyId": "f", "Symbol": "s", "Name": "n", "Alias": "a",
                              "TypeId": "t", "PTDisplayOrder": "pdo", "ModRevision": "rev", "PartitionId": "pid",
                              "TradesInFlow": "tf", "IsInterProduct": "ip", "State": "state",
                              "StateAttrib": "stateAttrib", "VersionId": "v", "CurrencyId": "c", "GroupId": "g",
                              "SecExchId": "x", "ProductComplex": "pc", "IsDeleted": "del", "MICCode": "mc",
                              "PriceTopic": "ptop", "MarketTypeId": "mti", "LockMask0": "lck0",
                              "PriceDisplayTypeId": "pdt", "AlternateSymbol": "as", "MatchAlgo": "ma",
                              "StrikeDisplayFactor": "sdf", "ImpliedRules": "ir", "ExChannelId": "excid",
                              "altSymbols": "ass", "FinraEligible": "fe", "AssetClassId": "ac",
                              "SubAssetClassId": "sac", "StrikePriceDec": "spd",
                              "RequireUnderlying": "ru", "MDepth": "md", "IDepth": "id",
                              "DaysToChangeTickSize": "d2cts", "IsTradeAtSettlementProduct": "tasp",
                              "SettlementPeriodInSec": "sps", "IsInverse": "inv", "MetaData": "data",
                              "BloombergCode": "bbc", "BloombergExchangeCode": "bec", "UpdateTS": "uts",
                              "UpdateSource": "ups", "InsertTS": "its"}

        for k, v in product_definition.items():
            if v not in product:
                product_definition[k] = None
            if product_definition[k] is not None:
                try:
                    if v == "t":
                        product_definition[k] = self.product_types[product[v]]
                    else:
                        product_definition[k] = product[v]
                except TypeError as e:
                    return product

        return product_definition

    def verify_exp_date_vs_sq_date_for_tocom(self):

        group_a_prods = ["CGAS", "CKER", "GASO", "GSOL", "KERO", "OTGCN", "OTSR2"]
        group_b_prods = ["CRUD", "TBGA", "TBGO", "TBKE", "TLGA", "TLGO", "TLKE"]
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        contract_month_exp_mismatch = []
        maturity_exp_mismatch = []
        cdd_incorrect = []
        term_incorrect = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                product_type = self.product_types[str(instrument_definition["ProductTypeId"])]

                product_name = instrument_definition["ProductSymbol"]
                if product_name not in group_a_prods:
                    for group_a_prod in group_a_prods:
                        if group_a_prod in product_name:
                            group_a_prods.append(product_name)
                            break
                if product_name not in group_b_prods:
                    for group_b_prod in group_b_prods:
                        if group_b_prod in product_name:
                            group_b_prods.append(product_name)
                            break

                term = instrument_definition["Term"]
                last_trading_date = instrument_definition["LastTradingDate"]
                term_values = get_term_values(term)
                term_yyyy_mm = int("".join(("20", str(term_values["year"]), str(term_values["month"]))))
                maturity_date = int(instrument_definition["MaturityDate"])
                cdd = instrument_definition["cdd"] if "cdd" in instrument_definition else None
                try:
                    name = instrument_definition["Name"]
                    exp_date = instrument_definition["ExpiryDate"]
                    if len(str(exp_date)) > 8:
                        exp_date = int(''.join(list(str(exp_date))[:8]))
                except TypeError as e:
                    print("TypeError:\ninstrument_definition: {}\nname: {}\nexp_date: {}\nmaturity_date: {}\n"
                          .format(instrument_definition, name, exp_date, maturity_date))
                if product_type == "MLEG":
                    if "legs" not in instrument:
                        print("url: {}".format(url))
                        print("FAIL: {0} {1} exp date {2} has no legs!".format(name, product_type, exp_date))
                    else:
                        exp_date = None
                        if len(instrument["legs"]) > 1:
                            leg_ltds = []
                            for leg in instrument["legs"]:
                                leg_ltds.append(leg["ltd"])
                                exp_date = min(leg_ltds)

                expected_cdd_date = None
                if product_type == "MLEG" or (product_name not in group_a_prods and product_name not in group_b_prods):
                    expected_cdd_date = get_date_values(int("".join(list(str(exp_date))[:6])))
                else:
                    maturity_date_values = get_date_values(maturity_date)
                    if product_name in group_a_prods:
                        expected_cdd_date = monthdelta(maturmaturity_date_valuesity_date_values, 1)
                    else:
                        expected_cdd_date = monthdelta(maturity_date_values, -1)
                    # expected_exp_date = int("".join([str(expected_exp_date.year), str(expected_exp_date.month).zfill(02), str(expected_exp_date.day).zfill(02)]))

                # if expected_exp_date != exp_date:
                #     maturity_exp_mismatch.append((product_name, product_type, maturity_date, exp_date))
                if expected_cdd_date is None:
                    print(instrument_definition)
                expected_cdd_date = int("".join([str(expected_cdd_date.year), str(expected_cdd_date.month).zfill(02)]))
                actual_cdd_date = None if cdd is None else int("".join(list(cdd)[:6]))
                if expected_cdd_date != actual_cdd_date:
                    cdd_incorrect.append((product_name, product_type, cdd, exp_date))

                # if term_yyyy_mm == int("".join(list(str(last_trading_date))[:6])):
                #     if product_name in group_a_prods:
                #         pass
                #     else:
                #         print("url: {}".format(url))
                #         print("FAIL: {0} {1} term {2} and last trading date {3} should not match"
                #               .format(product_name, product_type, term_yyyy_mm, "".join(list(str(exp_date))[:6])))

                if term_yyyy_mm == int("".join(list(str(maturity_date))[:6])):
                    if product_name in group_a_prods:
                        pass
                    else:
                        print("url: {}".format(url))
                        print("FAIL: {0} {1} term {2} and maturity {3} should not match"
                              .format(product_name, product_type, term_yyyy_mm, "".join(list(str(maturity_date))[:6])))

                if self.get_time_tuple(exp_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} is a weekend day".format(name, exp_date))
                elif self.get_time_tuple(maturity_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} maturity {1} is a weekend day".format(name, maturity_date))
            except StopIteration as e:
                print("\nFinished.")
                break

        if len(contract_month_exp_mismatch) > 0:
            print("\nFAIL! {} instruments have mismatched Contract Month and Expiration Date:"
                  .format(len(contract_month_exp_mismatch)))
            for contract_month_mismatch in contract_month_exp_mismatch:
                print(contract_month_mismatch)

        if len(maturity_exp_mismatch) > 0:
            print("\nFAIL! {} instruments incorrectly have Maturity (Tag 541) and Expiration Date that match:"
                  .format(len(maturity_exp_mismatch)))
            for maturity_mismatch in maturity_exp_mismatch:
                print(maturity_mismatch)

        if len(cdd_incorrect) > 0:
            print("\nFAIL! {} instruments have incorrect CDD (Tag 200):"
                  .format(len(cdd_incorrect)))
            for cdd in cdd_incorrect:
                print(cdd)

        if len(term_incorrect) > 0:
            print("\nFAIL! {} instruments have incorrect Term:".format(len(term_incorrect)))
            for term_incorrect_instr in term_incorrect:
                print(term_incorrect_instr)

    def verify_product_data(self):

        print("\n\nVerifying {} CDDs, RIC Codes and Bloomberg Codes in {}...".format(self.market, self.pdsdomain))

        group_a_prods = ["CGAS", "CKRO", "GAS", "GAO", "KRO", "CORN", "TSR2", "LNG"]
        group_b_prods = ["DBAI", "EEB", "EEP", "EWB", "EWP"]
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        contract_month_exp_mismatch = []
        maturity_exp_mismatch = []
        incorrect_cdds = []
        term_incorrect = []
        unneeded_cdds = []
        missing_cdds = []
        all_ric_codes = []
        instruments_with_no_ric_code = []
        instruments_with_dup_ric_code = []
        instruments_with_incorrect_ric_code = []
        all_bloomberg_codes = []
        instruments_with_no_bloomberg_code = []
        instruments_with_dup_bloomberg_code = []
        instruments_with_incorrect_dates = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                if self.debug:
                    print("DEBUG:", url)
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                product_type = self.product_types[instrument_definition["ProductTypeId"]]

                product_name = instrument_definition["ProductSymbol"]
                if product_name not in group_a_prods:
                    for group_a_prod in group_a_prods:
                        if group_a_prod in product_name:
                            group_a_prods.append(product_name)
                            break
                if product_name not in group_b_prods:
                    for group_b_prod in group_b_prods:
                        if group_b_prod in product_name:
                            group_b_prods.append(product_name)
                            break

                alias = instrument_definition["Alias"]
                ric = instrument_definition["RICCode"]
                bbc = instrument_definition["BloombergCode"]
                ltd = instrument_definition["LastTradingDate"]
                name = instrument_definition["Name"]
                exp_date = instrument_definition["ExpiryDate"]
                exp_date_yyyy_mm = exp_date[:6]
                exp_date_yyyy_mm_dd = exp_date[:8]
                ric_month = list(ric)[-2] if ric is not None else "None"

                # Get Maturity
                try:
                    maturity_date = int(instrument_definition["MaturityDate"])
                    maturity_yyyy_mm = "".join(list(str(maturity_date))[:6])
                except:
                    print("Error getting Maturity Date:", url)

                # Get Term
                term = instrument_definition["Term"]
                term_yyyy_mm, alias_term_yyyy_mm, term_values = None, None, None

                if self.market == "MEFF":
                    alias_term = get_alias_term_values(alias.split(" ")[1])
                else:
                    try:
                        alias_term = alias.split(" ")[1] if len(alias.split(" ")[1]) > 2 and str(alias.split(" ")[1]).isdigit() else get_alias_term_values(alias)
                    except IndexError:
                        print(url)
                if "W" in str(alias_term):
                    print("Skipping this instrument. alias_term = {}".format(alias_term))
                    continue

                if term is not None:
                    alias_term_dict = alias_term.split("-")[0] if "-" in alias_term else alias_term
                    alias_term_dict = alias_term.split(":+")[0] if ":+" in alias_term else alias_term
                    alias_term_yyyy_mm = "".join(
                        ["20", str(alias_term_dict['year']), str(alias_term_dict['month'])]) if len(
                        str(alias_term_dict['year'])) == 2 \
                        else "".join([str(alias_term_dict['year']), str(alias_term_dict['month'])])
                    try:
                        term_values = get_term_values(term)
                        if len(str(term_values["year"])) == 4:
                            term_yyyy_mm = "".join((str(term_values["year"]), str(term_values["month"])))
                        else:
                            term_yyyy_mm = "".join(("20", str(term_values["year"]), str(term_values["month"])))
                    except TypeError:
                        print("TypeError:")
                        print("term:", term, "term_values:", term_values)
                        print(url)

                    # Verify Term Value
                    if term_yyyy_mm != alias_term_yyyy_mm:
                        term_incorrect.append([alias, term])


                # Get CDD
                cdd = None
                if alias_term_yyyy_mm != exp_date_yyyy_mm and "cdd" not in instrument_definition:
                    missing_cdds.append(alias)
                else:
                    if "cdd" in instrument_definition:

                        # If Expiry Month Year != Contract Name Month Year then CDD is needed for correct Tag 200 value
                        cdd_yyyy_mm = None
                        if "cdd" is not None:
                            cdd = instrument_definition["cdd"]
                            cdd_yyyy_mm = "".join(list(cdd)[:6])
                            if cdd_yyyy_mm != alias_term_yyyy_mm:
                                incorrect_cdds.append([alias, cdd, maturity_date, exp_date, url])

                        # Verify CDD has correct value
                        try:
                            if len(str(exp_date)) > 8:
                                exp_date = int(''.join(list(str(exp_date))[:8]))
                        except TypeError as e:
                            print("TypeError:\ninstrument_definition: {}\nname: {}\nexp_date: {}\nmaturity_date: {}\n"
                                  .format(instrument_definition, name, exp_date, maturity_date))
                        if product_type == "MLEG":
                            if "legs" not in instrument:
                                print("url: {}".format(url))
                                print("FAIL: {0} {1} exp date {2} has no legs!".format(name, product_type, exp_date))
                            else:
                                exp_date = None
                                if len(instrument["legs"]) > 1:
                                    leg_ltds = []
                                    for leg in instrument["legs"]:
                                        leg_ltds.append(leg["ltd"])
                                        exp_date = min(leg_ltds)

                        # Determine expected CDD
                        expected_cdd_date = None
                        actual_cdd_date = None if cdd is None else int("".join(list(cdd)[:6]))

                        # Case 1: Expiry and Contract / Alias Monthyear are the same
                        if product_type == "MLEG" or (product_name not in group_a_prods and product_name not in group_b_prods):
                            expected_cdd_date = get_date_values(int("".join(list(str(exp_date))[:6])))
                        else:
                            maturity_date_values = get_date_values(maturity_date)
                            if product_name in group_a_prods:
                                expected_cdd_date = monthdelta(maturity_date_values, 1)
                            else:
                                expected_cdd_date = monthdelta(maturity_date_values, -1)
                            # expected_exp_date = int("".join([str(expected_exp_date.year), str(expected_exp_date.month).zfill(02), str(expected_exp_date.day).zfill(02)]))

                        # if expected_exp_date != exp_date:
                        #     maturity_exp_mismatch.append((product_name, product_type, maturity_date, exp_date))
                        if alias_term_yyyy_mm == exp_date_yyyy_mm:
                            if expected_cdd_date is None:
                                print(instrument_definition)
                            expected_cdd_date = int("".join([str(expected_cdd_date.year), str(expected_cdd_date.month).zfill(02)]))

                            if expected_cdd_date != actual_cdd_date:
                                incorrect_cdds.append((alias, cdd, maturity_date, exp_date, url))

                        # Case 2: Expiry and Contract / Alias Monthyear are different
                        if alias_term_yyyy_mm != exp_date_yyyy_mm:
                            expected_cdd_date = int("".join([str(alias_term_yyyy_mm[:4]), str(alias_term_yyyy_mm[4:6]).zfill(02)]))
                            if expected_cdd_date != actual_cdd_date:
                                incorrect_cdds.append((alias, cdd, maturity_date, exp_date, url))

                    if self.get_time_tuple(exp_date)[6] > 4:
                        print("url: {}".format(url))
                        print("FAIL: {0} exp date {1} is a weekend day".format(name, exp_date))
                    elif self.get_time_tuple(maturity_date)[6] > 4:
                        print("url: {}".format(url))
                        print("FAIL: {0} maturity {1} is a weekend day".format(name, maturity_date))

                    # Verify Date Fields
                    if ltd != exp_date_yyyy_mm_dd:
                        instruments_with_incorrect_dates.append([alias, "LTD:", ltd, "Expiry:", exp_date_yyyy_mm_dd, "Maturity:", maturity_date])
                    elif ltd != maturity_date:
                        instruments_with_incorrect_dates.append([alias, "LTD:", ltd, "Expiry:", exp_date_yyyy_mm_dd, "Maturity:", maturity_date])
                    elif exp_date_yyyy_mm_dd != maturity_date:
                        instruments_with_incorrect_dates.append([alias, "LTD:", ltd, "Expiry:", exp_date_yyyy_mm_dd, "Maturity:", maturity_date])

                    # Verify RIC Code
                    if ric is None:
                        instruments_with_no_ric_code.append(": ".join([alias, url]))
                    else:
                        if self.month_codes[ric_month] != alias_month:
                            instruments_with_incorrect_ric_code.append(": ".join([alias, url]))
                        else:
                            all_ric_codes.append(": ".join([alias, url]))
                    if ric in all_ric_codes:
                        instruments_with_dup_ric_code.append(": ".join([alias, url]))

                    # Verify BBG Code
                    if bbc is None:
                        instruments_with_no_bloomberg_code.append(": ".join([alias, url]))
                    if bbc in all_bloomberg_codes:
                        instruments_with_dup_bloomberg_code.append(": ".join([alias, url]))
                    else:
                        all_bloomberg_codes.append(": ".join([alias, url]))

                    # Verify RIC Code
                    if ric is None:
                        instruments_with_no_ric_code.append(": ".join([alias, url]))
                    else:
                        if self.month_codes[ric_month] != alias_month:
                            instruments_with_incorrect_ric_code.append(": ".join([alias, url]))
                        else:
                            all_ric_codes.append(": ".join([alias, url]))
                    if ric in all_ric_codes:
                        instruments_with_dup_ric_code.append(": ".join([alias, url]))

                    # Verify BBG Code
                    if bbc is None:
                        instruments_with_no_bloomberg_code.append(": ".join([alias, url]))
                    if bbc in all_bloomberg_codes:
                        instruments_with_dup_bloomberg_code.append(": ".join([alias, url]))
                    else:
                        all_bloomberg_codes.append(": ".join([alias, url]))

            except StopIteration as e:
                break

        if "ext" in self.pdsdomain:
            if len(instruments_with_no_ric_code) > 0:
                print("\nFAIL: {} instruments are missing RIC code:".format(len(instruments_with_no_ric_code)))
                instruments_with_no_ric_code.sort()
                for i in instruments_with_no_ric_code:
                    print("*", i)

            if len(instruments_with_dup_ric_code) > 0:
                print("\nFAIL: {} duplicate RIC codes were found:".format(len(instruments_with_dup_ric_code)))
                instruments_with_dup_ric_code.sort()
                for i in instruments_with_dup_ric_code:
                    print("*", i)

            if len(instruments_with_incorrect_ric_code) > 0:
                print("\nFAIL: {} incorrect RIC codes were found:".format(len(instruments_with_incorrect_ric_code)))
                instruments_with_incorrect_ric_code.sort()
                for i in instruments_with_incorrect_ric_code:
                    print("*", i)

            if len(instruments_with_no_bloomberg_code) > 0:
                print("\nFAIL: {} instruments are missing Bloomberg code:".format(len(instruments_with_no_bloomberg_code)))
                instruments_with_no_bloomberg_code.sort()
                for i in instruments_with_no_bloomberg_code:
                    print("*", i)

            if len(instruments_with_dup_bloomberg_code) > 0:
                print("\nFAIL: {} duplicate Bloomberg codes were found:".format(len(instruments_with_dup_bloomberg_code)))
                instruments_with_dup_bloomberg_code.sort()
                for i in instruments_with_dup_bloomberg_code:
                    print("*", i)

        if len(contract_month_exp_mismatch) > 0:
            print("\nFAIL! {} instruments have mismatched Contract Month and Expiration Date:"
                  .format(len(contract_month_exp_mismatch)))
            for contract_month_mismatch in contract_month_exp_mismatch:
                print(contract_month_mismatch)

        if len(maturity_exp_mismatch) > 0:
            print("\nFAIL! {} instruments incorrectly have Maturity (Tag 541) and Expiration Date that match:"
                  .format(len(maturity_exp_mismatch)))
            for maturity_mismatch in maturity_exp_mismatch:
                print(maturity_mismatch)

        if len(incorrect_cdds) > 0:
            print("\nFAIL! {} instruments have incorrect CDD (Tag 200) (alias, cdd, maturity_date, exp_date, url):".format(len(incorrect_cdds)))
            for incorrect_cdd in incorrect_cdds:
                print(incorrect_cdd)

        if len(unneeded_cdds) > 0:
            print("\nFAIL! {} instruments have CDD where not needed:".format(len(unneeded_cdds)))
            for unneeded_cdd in unneeded_cdds:
                print(unneeded_cdd)

        if len(term_incorrect) > 0:
            print("\nFAIL! {} instruments have incorrect Term:".format(len(term_incorrect)))
            for term_incorrect_instr in term_incorrect:
                print(term_incorrect_instr)

        if len(instruments_with_incorrect_dates) > 0:
            print("\nFAIL! {} instruments have incorrect Date:".format(len(instruments_with_incorrect_dates)))
            for instruments_with_incorrect_dates_instr in instruments_with_incorrect_dates:
                print(instruments_with_incorrect_dates_instr)

        else:
            print("\nFinished.")

    # if term_yyyy_mm == int("".join(list(str(last_trading_date))[:6])):
    #     if product_name in group_a_prods:
    #         pass
    #     else:
    #         print("url: {}".format(url))
    #         print("FAIL: {0} {1} term {2} and last trading date {3} should not match"
    #               .format(product_name, product_type, term_yyyy_mm, "".join(list(str(exp_date))[:6])))
    #
    # if term_yyyy_mm == int("".join(list(str(maturity_date))[:6])):
    #     if product_name in group_a_prods:
    #         pass
    #     else:
    #         print("url: {}".format(url))
    #         print("FAIL: {0} {1} term {2} and maturity {3} should not match"
    #               .format(product_name, product_type, term_yyyy_mm, "".join(list(str(maturity_date))[:6])))

    def xverify_exp_date_vs_sq_date_for_tocom(self):

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                product_type = self.product_types[str(instrument_definition["ProductTypeId"])]
                product_name = instrument_definition["ProductSymbol"]
                security_id = instrument_definition["SecurityId"]
                term = instrument_definition["Term"]
                try:
                    name = instrument_definition["Name"]
                    exp_date = instrument_definition["ExpiryDate"]
                    if len(str(exp_date)) > 8:
                        exp_date = int(''.join(list(str(exp_date))[:8]))
                    maturity_date = int(instrument_definition["MaturityDate"])
                except TypeError as e:
                    print("TypeError:\ninstrument_definition: {}\nname: {}\nexp_date: {}\nmaturity_date: {}\n"
                          .format(instrument_definition, name, exp_date, maturity_date))
                if product_type == "MLEG":
                    # if not hasattr(instrument, "legs"):
                    if "legs" not in instrument:
                        print("url: {}".format(url))
                        print("FAIL: {0} {1} exp date {2} has no legs!".format(name, product_type, exp_date))
                    else:
                        exp_date = None
                        if len(instrument["legs"]) > 1:
                            leg_ltds = []
                            for leg in instrument["legs"]:
                                leg_ltds.append(leg["ltd"])
                                exp_date = min(leg_ltds)
                if self.market not in ("OSE"):
                    if exp_date != maturity_date:
                        print("url: {}".format(url))
                        print("FAIL: {0} {1} exp date {2} and maturity {3} do not match".format(product_name,
                                                                                                product_type,
                                                                                                exp_date,
                                                                                                maturity_date))
                else:
                    if exp_date == maturity_date:
                        print("url: {}".format(url))
                        print("FAIL: {0} {1} exp date {2} and maturity {3} are the same".format(product_name,
                                                                                                product_type,
                                                                                                exp_date,
                                                                                                maturity_date))
                    else:
                        term_values = get_term_values(term)
                        term_mm_yy = "".join((str(term_values["year"]),
                                              str(term_values["month"])))
                        contract_month_values = get_tocom_contract_month(security_id)
                        contract_month_mm_yy = "".join((str(contract_month_values["year"]),
                                                        str(contract_month_values["month"])))
                        if term_mm_yy != contract_month_mm_yy:
                            print("url: {}".format(url))
                            print("FAIL: {0} {1} term {2} and contract month {3} do not match".format(product_name,
                                                                                                      product_type,
                                                                                                      term_mm_yy,
                                                                                                      contract_month_mm_yy))
                if self.get_time_tuple(exp_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} is a weekend day".format(name, exp_date))
                elif self.get_time_tuple(maturity_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} maturity {1} is a weekend day".format(name, maturity_date))
            except StopIteration as e:
                print("\nFinished.")
                break

    def verify_ltd_vs_maturity_date_for_lme(self):

        # DEB-105349 ps_lme: fix last trading date
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                name = instrument_definition["Name"]
                ltd = instrument_definition["LastTradingDate"]
                maturity_date = instrument_definition["MaturityDate"]
                if str(ltd) != str(maturity_date):
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} and maturity {2} do not match".format(name, ltd, maturity_date))
                elif self.get_time_tuple(ltd)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} is a weekend day".format(name, ltd))
                elif self.get_time_tuple(maturity_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} maturity {1} is a weekend day".format(name, maturity_date))
            except StopIteration as e:
                print("\n\nFinished.")
                break

    def verify_correction_in_expiry_date_changes(self):

        # DEB-129985 Correction in Expiry Date changes in Euronext , JPX [new] ,  FENICS
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                ltd = instrument_definition["LastTradingDate"]
                maturity_date = instrument_definition["MaturityDate"]
                exp = "".join(list(instrument_definition["ExpiryDate"][:8]))
                if ltd:
                    if str(exp) != str(ltd) or exp is None:
                        print("url: {}".format(url))
                        print("FAIL: {0} exp date {1} and ltd {2} do not match".format(alias, exp, ltd))
                else:
                    if str(exp) != str(maturity_date) or exp is None:
                        print("url: {}".format(url))
                        print("FAIL: {0} exp date {1} and maturity {2} do not match".format(alias, exp, maturity_date))
                if self.get_time_tuple(ltd)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} is a weekend day".format(alias, ltd))
                elif self.get_time_tuple(maturity_date)[6] > 4:
                    print("url: {}".format(url))
                    print("FAIL: {0} maturity {1} is a weekend day".format(alias, maturity_date))
            except StopIteration as e:
                print("\n\nFinished.")
                break

    # KRX #
    def verify_krx_spreads_ComboTypeID(self):

        # DEB-129985 Correction in Expiry Date changes in Euronext , JPX [new] ,  FENICS

        self.product_types = {"43": "MLEG"}
        self.market = "KRX"
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_overview = self.instrument_overview_generator()

        missing_ComboTypeIDs = []
        incorrect_ComboTypeIDs = []
        instrument_count = 0

        while True:
            try:
                instrument_overview = str(next(get_instrument_overview))
                instrument = self.parse_pds_output(instrument_overview, http_request=False)
                instrument_definition = self.translate_instrument_data(instrument)
                combo_type_id = instrument_definition['ComboTypeId']
                alias = instrument_definition['Alias']
                instr_id = str(instrument_definition['Id'])
                instr_url = self.base_url + "/api/1/instruments?instrumentIds=" + instr_id + "&slim=false"
                if combo_type_id is None:
                    missing_ComboTypeIDs.append(alias + " : " + instr_url)
                else:
                    if "Inter" in alias:
                        if combo_type_id != 15:
                            incorrect_ComboTypeIDs.append(alias + " : " + instr_url)
                    else:
                        if combo_type_id != 16:
                            incorrect_ComboTypeIDs.append(alias + " : " + instr_url)
                instrument_count += 1
            except StopIteration as e:
                print("\n\nFinished.")
                break

        result_file = open(r"/Users/cmaurer/result_file.txt", "w")
        if len(missing_ComboTypeIDs) > 0:
            missing_ComboTypeIDs.sort()
            result_file.write("WARNING! Out of a total of {} instruments, {} are missing ComboTypeID\n".format(instrument_count, len(missing_ComboTypeIDs)))
            print("WARNING! Out of a total of {} instruments, {} are missing ComboTypeID!".format(instrument_count, len(missing_ComboTypeIDs)))
            for missing_ComboTypeID in missing_ComboTypeIDs:
                result_file.write(missing_ComboTypeID + "\n")
                print(missing_ComboTypeID)
        if len(incorrect_ComboTypeIDs) > 0:
            incorrect_ComboTypeIDs.sort()
            result_file.write("WARNING! Out of a total of {} instruments, {} have incorrect ComboTypeID\n".format(instrument_count, len(incorrect_ComboTypeIDs)))
            print("WARNING! The following {} instruments are incorrect ComboTypeID!".format(instrument_count, len(incorrect_ComboTypeIDs)))
            for incorrect_ComboTypeID in incorrect_ComboTypeIDs:
                result_file.write(incorrect_ComboTypeID + "\n")
                print(incorrect_ComboTypeID)
        result_file.close()

    def verify_krx_spread_ratios(self):
        # Identify combo instruments that have incorrect ratio +1:-1

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        instruments_with_incorrect_spread_ratio = []

        print("\n\nVerifying KRX Spread Ratios in {}...".format(self.pdsdomain))

        while True:
            try:
                failed = False
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                symbol = instrument_definition["Symbol"]
                if "legs" in instrument:
                    front_leg = instrument["legs"][0]
                    back_leg = instrument["legs"][1]
                    if symbol.startswith("BM"):  # KTB Spreads (BMA, BM3, BM5) are the only ones that are not "Reverse Spreads"
                        if front_leg['r'] == -1 and back_leg['r'] == 1:
                            failed = True
                    else:
                        if front_leg['r'] == 1 and back_leg['r'] == -1:
                            failed = True
                if failed:
                    instruments_with_incorrect_spread_ratio.append(": ".join([alias, url]))
            except StopIteration as e:
                print("\n\nFinished.")
                break

        if len(instruments_with_incorrect_spread_ratio) > 0:
            print("\nFAIL: {} instruments have incorrect Spread Ratio:".format(len(instruments_with_incorrect_spread_ratio)))
            instruments_with_incorrect_spread_ratio.sort()
            for i in instruments_with_incorrect_spread_ratio:
                print("*", i)

    def verify_jpx_instrument_download(self):

        # DEB-129985 Correction in Expiry Date changes in Euronext , JPX [new] ,  FENICS

        self.product_types = {"43": "MLEG"}
        self.market = "JPX"
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_overview = self.instrument_overview_generator()

        instrument_count = 0

        while True:
             try:
                instrument_overview = str(next(get_instrument_overview))
                instrument = self.parse_pds_output(instrument_overview, http_request=False)
                instrument_definition = self.translate_instrument_data(instrument)
                sec_id = instrument_definition['SecurityId']
                print("".join(['"', sec_id.replace(" ", ""), '",']))
                instrument_count += 1
             except StopIteration as e:
                print("\n\ninstrument_count = {}.".format(instrument_count))
                print("\n\nFinished.")
                break

    def verify_hkex_maturity_date(self):

        # DEB-117650 HKEX: upload maturity data into metadata fields
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        incorrect_maturity_dates = []
        weekend_maturity_dates = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                name = instrument_definition["Name"]
                ltd = str(instrument_definition["LastTradingDate"])
                maturity_date = instrument_definition["MaturityDate"]
                if self.market == "HKEX":
                    if "data" in instrument:
                        maturity_day = instrument_definition["mat_day"].zfill(2)
                        maturity_month = instrument_definition["mat_month"].zfill(2)
                        maturity_year = instrument_definition["mat_year"]
                    maturity_date = "".join(
                        (maturity_year, maturity_month, maturity_day)) if "data" in instrument else "Metadata Missing"
                exp_date = instrument_definition["ExpiryDate"]
                exp_date_yyyymmdd = str(''.join(list(str(exp_date))[:8]))
                validation = {}
                validation["Name"] = name
                validation["test_date"] = exp_date_yyyymmdd
                validation["MaturityDate"] = maturity_date if self.market == "HKEX" else ltd
                if validation["test_date"] != validation["MaturityDate"]:
                    incorrect_maturity_dates.append(validation)
                if self.get_time_tuple(maturity_date)[6] > 4:
                    weekend_maturity_dates.append(validation)
            except StopIteration as e:
                print("\n\nFinished.")
                break

        test_date_str = "Expiry Date" if self.market == "HKEX" else "Last Trading Date"

        if len(incorrect_maturity_dates) > 0:
            print("\nFAIL! {} instruments have a Maturity Date that does not match Expiry Date:"
                  .format(len(incorrect_maturity_dates)))
            print("||" + "||".join(("Name", test_date_str, "Maturity Date")) + "||")
            for incorrect_maturity_date in incorrect_maturity_dates:
                print("|" + "|".join([incorrect_maturity_date["Name"],
                                      incorrect_maturity_date["test_date"],
                                      incorrect_maturity_date["MaturityDate"]]) + "|")

        if len(weekend_maturity_dates) > 0:
            print("\nFAIL! {} instruments have a Maturity Date that falls on a weekend:"
                  .format(len(weekend_maturity_dates)))
            print("||" + "||".join(("Name", test_date_str, "Maturity Date")) + "||")
            for weekend_maturity_date in weekend_maturity_dates:
                print("|" + "|".join([weekend_maturity_date["Name"],
                                      weekend_maturity_date["test_date"],
                                      weekend_maturity_date["MaturityDate"]]) + "|")

    def verify_tfx_maturity_date(self):

        # DEB-116024 tfx mds rewrite : check maturity and last trading date of instruments.
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        incorrect_maturity_dates = []
        weekend_maturity_dates = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                name = instrument_definition["Name"]
                ltd = str(instrument_definition["LastTradingDate"])
                maturity_date = instrument_definition["MaturityDate"]
                validation = {"Name": name, "ltd": ltd, "MaturityDate": maturity_date}
                if ltd != maturity_date:
                    incorrect_maturity_dates.append(validation)
                if self.get_time_tuple(maturity_date)[6] > 4:
                    weekend_maturity_dates.append(validation)
            except StopIteration as e:
                print("\n\nFinished.")
                break

        if len(incorrect_maturity_dates) > 0:
            print("\nFAIL! {} instruments have a Maturity Date that does not match Expiry Date:"
                  .format(len(incorrect_maturity_dates)))
            print("||" + "||".join(("Name", "Last Trading Date", "Maturity Date")) + "||")
            for incorrect_maturity_date in incorrect_maturity_dates:
                print("|" + "|".join([incorrect_maturity_date["Name"],
                                      incorrect_maturity_date["ltd"],
                                      incorrect_maturity_date["MaturityDate"]]) + "|")

        if len(weekend_maturity_dates) > 0:
            print("\nFAIL! {} instruments have a Maturity Date that falls on a weekend:"
                  .format(len(weekend_maturity_dates)))
            print("||" + "||".join(("Name", "Last Trading Date", "Maturity Date")) + "||")
            for weekend_maturity_date in weekend_maturity_dates:
                print("|" + "|".join([weekend_maturity_date["Name"],
                                      weekend_maturity_date["ltd"],
                                      weekend_maturity_date["MaturityDate"]]) + "|")

    def verify_expiry_mx_corra_futures(self):

        # DEB-115810 Fix Expiry on MX CORRA futures
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                product_type = self.product_types[str(instrument_definition["ProductTypeId"])]
                alias = instrument_definition["Alias"]
                name = instrument_definition["Name"]
                exp = instrument_definition["ExpiryDate"]
                maturity_date = instrument_definition["MaturityDate"]
                term = instrument["legs"][0]["lt"] if product_type == "MLEG" else instrument_definition["Term"]
                term_month = get_term_values(term)["month"]
                term_year = "20" + get_term_values(term)["year"]
                term_date = self.get_time_tuple(term_year + term_month)
                term_date_float = time.mktime(term_date)
                following_year = time.localtime(term_date_float + 31536000).tm_year  # 31536000 s in a year
                third_wednesdays = self.get_third_wed_of_every_month(int(term_year))
                third_wednesdays.extend(self.get_third_wed_of_every_month(int(following_year)))
                expected = None
                for thirdwed in third_wednesdays:
                    thirdwed_list = thirdwed.split("/")
                    comparison_value = (thirdwed_list[0], thirdwed_list[-1])
                    if comparison_value == (term_month, term_year):
                        match_index = third_wednesdays.index(thirdwed)
                        expected_thirdwed = third_wednesdays[match_index + 3]
                        expected_thirdwed_float = time.mktime(self.get_time_tuple(
                            expected_thirdwed[-4:] + expected_thirdwed[:2] + expected_thirdwed[3:5]))
                        expected = time.localtime(expected_thirdwed_float - 86400)  # 86400 s in a month
                        break
                expected_exp_date = "".join(
                    (str(expected.tm_year), str(expected.tm_mon).zfill(2), str(expected.tm_mday).zfill(2))) + "235959"
                if exp != expected_exp_date:
                    print("url: {}".format(url))
                    print("FAIL: {0} exp date {1} does not match expected {2}".format(name, exp, expected_exp_date))
            except StopIteration as e:
                print("\n\nFinished.")
                break

    def verify_ltd_for_curveglobal(self):

        # DEB-104962 OSN should expire same day as SON

        year = time.localtime()[0]
        third_wednesdays = self.get_third_wed_of_every_month(year)

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                pass_fail = "PASS"
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                name = instrument_definition["Name"]
                last_trading_date = str(instrument_definition["LastTradingDate"])
                actual = last_trading_date

                if "legs" in instrument and len(instrument["legs"]) > 1:
                    instrument_definition = self.translate_instrument_data(instrument["legs"][0])

                term_yearmonth = []
                term_year = ["2", "0"]
                term_year.extend(list(instrument_definition["Term"])[-2:])
                term_year_int = int("".join(term_year))
                term_month_lookup = datetime.datetime.strptime("".join(list(instrument_definition["Term"])[:3]), '%b')
                term_month = str(term_month_lookup.month).zfill(2)
                term_yearmonth.extend(term_year)
                term_yearmonth.extend(term_month)

                if ("/" + str(term_year_int)) not in str(third_wednesdays):
                    third_wednesdays.extend(self.get_third_wed_of_every_month(term_year_int))

                for third_wednesday in third_wednesdays:
                    third_wednesday_yearmonth = []
                    third_wednesday_year = list(third_wednesday)[-4:]
                    third_wednesday_month = list(third_wednesday)[:2]
                    third_wednesday_yearmonth.extend(third_wednesday_year)
                    third_wednesday_yearmonth.extend(third_wednesday_month)
                    if third_wednesday_yearmonth == term_yearmonth:
                        third_wednesday_index = third_wednesdays.index(third_wednesday)

                        expected_list = list(third_wednesdays[third_wednesday_index + 1])
                        expected = expected_list[-4:]
                        expected.extend(expected_list[:2])
                        expected.extend(expected_list[3:5])
                        expected = "".join(expected)

                if actual != expected:
                    pass_fail = "FAIL"
                    print("{0}: {1} LTD {2} does not match expected {3}".format(pass_fail, name, actual, expected))
                elif actual == expected:
                    print("{0}: {1} LTD {2} matches expected {3}".format(pass_fail, name, actual, expected))
                if self.get_time_tuple(actual)[6] > 4:
                    print("{0}: {1} LTD {2} is a weekend day".format(pass_fail, name, actual))
                if pass_fail == "FAIL":
                    print("url: {}".format(url))
            except StopIteration as e:
                print("\n\nFinished.")
                break

    def verify_alias_for_tocom(self):

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        incorrect_cdds = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instruments = self.parse_pds_output(url)
                instrument = instruments[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                term = instrument_definition["Term"]
                name = instrument_definition["Name"]
                if "cdd" not in instrument_definition:
                    instrument_definition["cdd"] = None
                cdd = instrument_definition["cdd"]
                if "-" in alias:
                    alias_date = (alias.split("-")[1]).split(" ")[-1] if len(alias.split("-")) == 2 and len(
                        alias.split(" ")) == 2 else (alias.split("-")[1]).split(" ")[-1]
                elif ":" in alias:
                    alias_date = (alias.split(":")[1]).split(" ")[-1]
                else:
                    alias_date = (alias.split(" ")[-1])
                # if alias_date != term:
                #     print("url: {}".format(url))
                #     print("FAIL: {0} Alias date {1} and term date {2} do not match".format(alias, alias_date, term))

                cdd_yyyy_mm = "".join(list(cdd)[:6]) if cdd is not None else None
                alias_term = alias.split(" ")[1]
                if "W" in alias_term:
                    print("Skipping this instrument. alias_term = {}".format(alias_term))
                    continue
                alias_term = alias_term.split("-")[0] if "-" in alias_term else alias_term
                alias_term = alias_term.split(":+")[0] if ":+" in alias_term else alias_term
                alias_term_dict = get_term_values(alias_term)
                alias_term_yyyy_mm = "".join(["20", str(alias_term_dict['year']), str(alias_term_dict['month'])])
                if cdd_yyyy_mm != alias_term_yyyy_mm:
                    incorrect_cdds.append([alias, cdd])

            except StopIteration as e:
                break

        if len(incorrect_cdds) > 0:
            print("WARNING! {} instruments have incorrect CDD!".format(len(incorrect_cdds)))
            for incorrect_cdd in incorrect_cdds:
                print(incorrect_cdd)
        else:
            print("\n\nFinished.")

    def verify_tick_size_for_sgx_msci_contracts(self):

        new_spec_tick_size = {'NAU': 0.05, 'NCH': 0.01, 'NEAXC': 0.05, 'NEAXK': 0.05, 'NEA': 0.01, 'NEMEA': 0.01,
                              'NEXC': 0.05, 'NEXK': 0.05, 'NLATA': 0.01, 'NEM': 0.01, 'EM': 0.01, 'NHK': 0.5,
                              'NMD': 0.01, 'NID': 0.01, 'NJY': 0.05, 'NMY': 0.01, 'NNZ': 0.01, 'NPXJ': 0.05,
                              'NPC': 0.05, 'NPH': 0.01, 'NSG': 0.01, 'NSP': 0.05, 'NTH': 0.01, 'NVN': 0.01}

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(get_instrument_id.next())
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                tick_denom = instrument_definition["TickSizeDenom"]
                actual_tick_size = instrument_definition["TickSize"]
                expected_tick_size = new_spec_tick_size[instrument["ps"]]
                if actual_tick_size != expected_tick_size:
                    print("url: {}".format(url))
                    print("FAIL: {} actual tick size {} and expected {} do not match".format(instrument["n"],
                                                                                             actual_tick_size,
                                                                                             expected_tick_size))
            except StopIteration as e:
                print("\n\nFinished.")
                break

    def verify_tick_denom_matches_price_conversion_factor(self):

        logfile_path = r'/Users/cmaurer/'
        all_instruments = {}
        all_logfiles = os.listdir(logfile_path)
        for logfile in all_logfiles:
            if 'pdsu_sgx' in logfile:
                f = open(logfile_path + logfile, 'r')
                for line in f.readlines():
                    if 'PriceConversionFactor' in line and 'JSON:' in line:
                        payload = line.split('JSON:')[1]
                        output = json.loads(payload)
                        for record in output['products'][0]['instruments']:
                            alias = record['instr']['a']
                            pcf_dict = ast.literal_eval(record['instr']['data'])
                            pcf = pcf_dict['PriceConversionFactor']
                            if alias not in all_instruments:
                                all_instruments[alias] = pcf

        f.close()

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        test_count = 0

        while True:
            try:
                instrument_id = str(get_instrument_id.next())
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                tick_denom = str(instrument_definition["TickSizeDenom"])
                actual_tick_size = instrument_definition["TickSize"]
                if alias in all_instruments:
                    test_count += 1
                    if tick_denom != all_instruments[alias]:
                        print("url: {}".format(url))
                        print("FAIL: {} Ticksize DR {} and PriceConversionFactor {} do not match".format(alias,
                                                                                                         tick_denom,
                                                                                                         all_instruments[alias]))
            except StopIteration as e:
                print("\n\nTested {} instruments.".format(test_count))
                break

    def verify_tick_table(self):

        group_a_prods = ["SBH", "SBJ", "SBK", "SBL", "SBM", "SBN", "SBP", "SBQ", "SBS", "SBT", "SBV", "SBW", "SBX", "SBY", "SBZ", "SC0", "SC1", "SC2", "SC3", "SC4", "SC5", "SC6", "SC7", "SC8", "SC9", "SCA", "SCB", "SCC", "SCD", "SCE", "SCF", "SCG", "SCJ", "SCK", "SCL", "SCN", "SCP", "SCQ", "SCR", "SCS", "SCT", "SCV", "SCW", "SCX", "SCY", "SCZ", "SD0", "SD1", "SD2", "SD3", "SD4", "SD5", "SD6", "SD7", "SD8", "SD9", "SDA", "SDB", "SDC", "SDD", "SDE", "SDG", "SDH", "SDJ", "SDK", "SDL", "SDM", "SDN", "SDP", "SDR", "SDT", "SDV", "SDW", "SDY", "SDZ", "SE0", "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE8", "SE9", "SEA", "SEB", "SEC", "SED", "SEE", "SEF", "SEG", "SEH", "SEJ", "SEK", "SEL", "SEM", "SEN", "SEP", "SEQ", "SER", "SES", "SET", "SEV", "SEW", "SEX", "SEY", "SEZ", "SF0", "SF1", "SF2", "SF3", "SF4", "SF5", "SF6", "SF7", "SF8", "SF9", "SFA", "SFB", "SFC", "SFD", "SFE", "SFF", "SFG", "SFH", "SFJ", "SFK", "SFL", "SFM", "SFN", "SFP", "SFQ"]
        group_b_prods = ["DBAI", "EEB", "EEP", "EWB", "EWP"]
        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        instruments_with_incorrect_tick_table = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                if self.debug:
                    print("DEBUG:", url)
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                product_type = self.product_types[instrument_definition["ProductTypeId"]]

                product_name = instrument_definition["ProductSymbol"]
                expected_tick_table = None
                if product_name in group_a_prods:
                    expected_tick_table = "140"

                alias = instrument_definition["Alias"]
                term = instrument_definition["Term"]
                tick_table = str(instrument_definition['TickTableId'])
                if tick_table is not None and expected_tick_table is not None:
                    if tick_table != expected_tick_table:
                        instruments_with_incorrect_tick_table.append({"alias": alias, "tick_table": tick_table, "expected_tick_table": expected_tick_table, "url": url})

            except StopIteration as e:
                break

        if len(instruments_with_incorrect_tick_table) > 0:
            print("\nFAIL! {} instruments have incorrect tick table:"
                  .format(len(instruments_with_incorrect_tick_table)))
            for instr in instruments_with_incorrect_tick_table:
                print(instr["alias"], "expected:", instr["expected_tick_table"], "actual:", instr["tick_table"], "url:", instr["url"])
        else:
            print("\nFinished.")

    def find_greater_than_one_leg_ratio(self):
        # Look for combo instruments that have at least one leg with ratio greater than 1

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                if "legs" in instrument:
                    for leg in instrument["legs"]:
                        if leg["rx"] > 1:
                            print(url)
                            print(instrument_definition)
            except StopIteration as e:
                print("\n\nFinished.")
                break

    def verify_descriptions_are_not_blank(self):
        # Verify there are no products without a Description

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        products_with_no_description = []

        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition['Symbol']
                if product_definition['Name'] is None:
                    products_with_no_description.append(" ".join([symbol, product_definition["TypeId"]]))
            except StopIteration as e:
                print("\n\nFinished.")
                break

        if len(products_with_no_description) > 0:
            products_with_no_description.sort()
            for p in products_with_no_description:
                print("* {}".format(p))

    def verify_mic_code(self):
        # Verify there are no products without a Description

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        instruments_with_incorrect_mic_code = []
        instruments_with_missing_mic_code = []
        mic_codes = None
        if self.market == "TFX":
            mic_codes = {"EY": "XTFF", "EYO": "XTFF", "AL": "TFX", "AY": "XTFF", "AYO": "XTFF", "BL": "TFX",
                         "BY": "XTFF", "BYO": "XTFF", "EL": "TFX", "FY": "TFX"}
        elif self.market == "HKEX":
            mic_codes = "XHKF"
        elif self.market == "JPX":
            mic_codes = {"225": "XOSE", "225M": "XOSE", "225W": "XOSE", "400": "XOSE", "BANK": "XOSE", "C30": "XOSE",
                         "CORN": "XOSE", "DJIA": "XOSE", "FT50": "XOSE", "GLD": "XOSE", "GLDD": "XOSE", "GLDM": "XOSE",
                         "JBL": "XOSE", "JBLM": "XOSE", "JBM": "XOSE", "JBS": "XOSE", "MOTH": "XOSE", "NKDV": "XOSE",
                         "NVI": "XOSE", "PALD": "XOSE", "PLT": "XOSE", "PLTD": "XOSE", "PLTM": "XOSE", "REDB": "XOSE",
                         "REIT": "XOSE", "RNP": "XOSE", "RSS3": "XOSE", "SILV": "XOSE", "SOYB": "XOSE", "TAIX": "XOSE",
                         "TPX": "XOSE", "TPXM": "XOSE", "TSR2": "XOSE", "CGAS": "XTKT", "CKRO": "XTKT", "DBAI": "XTKT",
                         "EEB": "XTKT", "EEP": "XTKT", "EWB": "XTKT", "EWP": "XTKT", "GAO": "XTKT", "GAS": "XTKT",
                         "KRO": "XTKT", "8801": "XOSE", "CMEP": "XOSE", "RSS3|TSR2": "XOSE", "EEB|EWB": "XTKT",
                         "GAS|KRO": "XTKT", "KRO|GAO": "XTKT", "EEP|EWP": "XTKT", "GLDD|PLTD": "XOSE",
                         "CGAS|CKRO": "XTKT", "GLDM|PLTM": "XOSE", "GAO|DBAI": "XTKT", "KRO|DBAI": "XTKT",
                         "GAS|DBAI": "XTKT", "GAS|GAO": "XTKT", "LNG": "XTKT"}
        elif self.market == "SGX":
            mic_codes = "XSIM"
        elif self.market == "SGX_GIFT":
            mic_codes = "INSE"
        elif self.market == "KRX":
            mic_codes = "XKFE"

        print("\n\nVerifying {} MIC Codes in {}...".format(self.market, self.pdsdomain))

        while True:
            try:
                fail = False
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition["Symbol"]
                product_type = product_definition["TypeId"]
                mic_code = product_definition["MICCode"]
                if mic_code is None:
                    instruments_with_missing_mic_code.append(" ".join([symbol, product_type]))
                if type(mic_codes) == dict and symbol not in mic_codes:
                    try:
                        if mic_code not in mic_codes:  # and mic_code.isdigit():
                            pass
                        elif mic_code != mic_codes[symbol]:
                            fail = True
                    except KeyError:
                        print("Expected Result not defined for {}.".format(symbol))
                else:
                    if mic_code != mic_codes:
                        fail = True
                if fail:
                    if len(mic_codes) == 0:
                        mic_codes[symbol] = "None"
                    if type(mic_codes) == dict:
                        error_str = "{} {} MIC Code: Expected: {} Actual: {}".format(symbol, product_type,
                                                                                     mic_codes[symbol], mic_code)
                    else:
                        error_str = "{} {} MIC Code: Expected: {} Actual: {}".format(symbol, product_type,
                                                                                     mic_codes, mic_code)
                    instruments_with_incorrect_mic_code.append(error_str)
            except StopIteration as e:
                break

        if len(instruments_with_incorrect_mic_code) > 0:
            print("FAIL: The following products have missing or incorrect MIC code:")
            instruments_with_incorrect_mic_code.sort()
            for p in instruments_with_incorrect_mic_code:
                print("* {}".format(p))

        elif len(instruments_with_missing_mic_code) > 0:
            print("FAIL: {} products have missing MIC code:".format(str(len(instruments_with_missing_mic_code))))
            instruments_with_missing_mic_code.sort()
            for p in instruments_with_missing_mic_code:
                print("* {}".format(p))
        else:
            print("\n\nFinished.")
        print("Tested {} Products and {} Instruments".format(str(len(self.all_product_ids)), str(len(self.all_instrument_overview))))

    def get_instrument_count(self):
        # Get a total instrument count
        # prods = ['C30', 'EWB', 'TPXM', 'JBLM', 'EEB', 'JBS', 'KRO|GAO', 'CGAS', 'CORN', 'PLT', 'GLDM', 'GLDD', 'GLDM|PLTM', 'FT50', 'RSS3|TSR2', 'PLTM', 'GAS|GAO', 'EEP', 'CGAS|CKRO', 'RSS3']  # , 'TAIX', 'PALD', 'GAS|KRO', 'NVI', 'REIT', 'TPX', 'GAO|DBAI', 'EEP|EWP', '400', 'GAS', 'REDB', 'DJIA', 'TSR2', 'GLD', 'CKRO', 'EEB|EWB', 'SILV', 'KRO', '225', 'EWP', 'PLTD', 'KRO|DBAI', 'SOYB', 'DBAI', 'JBM', 'JBL', 'BANK', 'GAO', 'MOTH', 'NKDV', '225M', '225W', 'RNP', 'GLDD|PLTD', 'GAS|DBAI']
        prods = ['MHI', ]

        for p in prods:
            self.prod_list = [p, ]
            total_instruments = {}
            all_envs = ("int-dev-cert", "int-stage-cert")
            # all_envs = ("int-dev-cert", "int-stage-cert", "ext-uat-cert", "ext-prod-live")
            for env in all_envs:
                instrument_count = 0
                total_instruments[env] = 0
                pds_url = "".join(["https://pds-", env, ".trade.tt"])
                self.base_url = pds_url
                self.get_all_product_ids()
                get_product_id = self.product_id_generator()
                while True:
                    try:
                        product_id = str(next(get_product_id))
                        instrument_count_url = pds_url + "/api/1/instruments/instrumentcount?ProductId=" + str(product_id)
                        print(env, instrument_count_url)
                        instrument_count_data = self.parse_pds_output(instrument_count_url)
                        instrument_count_dict = ast.literal_eval(instrument_count_data)
                        instrument_count += instrument_count_dict["ic"]
                    except StopIteration as e:
                        total_instruments[env] = instrument_count
                        self.all_product_ids = []
                        break

            print("\n\nFinished.")
            print(self.prod_list)
            print(self.product_types.values())

            print("Total instrument count = {}".format(str(total_instruments)))

    def generate_pmerge(self):
        # Get a total instrument count
        new_point_value = raw_input("If you need a point value update, enter it here: ")
        new_product_name = raw_input("If you need a product name, enter it here: ")

        print("PLTM,2,0,80,0,1,1,0,0,1,0,JPY, , ,Mini Platinum Futures Spreads")
        print("CMEP,1,0,10000,0,1,1,0,0,5,100,JPY,,,CME Group Petroleum Index Futures")
        self.get_all_product_ids()
        curreny_url = self.base_url + "/api/1/systemdata?type=currency"
        curreny_lookup = self.parse_pds_output(curreny_url)
        this_market_currencies = {}

        mds_pmerge_format = False
        pmg_values_list = []
        pmg_file_list = []
        pmg_product_types = {34 : 1, 43 : 2, 51: 3, 200: 4, 20 : 5, 77 : 6}
        pmg_product_type_strings = {'1': 'Futures', '2': 'Spreads', '3': 'Options', '4': 'Options', '6': 'Bonds'}
        if mds_pmerge_format:
            print("idPMerge,AllProduct_Symbol,Market_idMarket,ProductType_idProductType,AllInstrument_idInstrument,PointValue,TickSizeNumerator,TickSizeDenominator,TickValue,CurrencyType_idCurrencyType,PriceDecimalsCount,ProductName")

        for product in self.all_products:
            if product['s'] in self.prod_list or len(self.prod_list) == 0:
                # Product Data
                product_definition = self.translate_product_data(product)
                id = str(product_definition['Id'])

                symbol = product_definition['Symbol']  # Product Symbol
                ptype = str(pmg_product_types[product['t']]) if self.market != "JPX" else product['t']  # Product Type
                name = str(product_definition['Name'])  # Description

                #Get Currency
                currency = None
                currency_id = product_definition['CurrencyId']
                if currency_id in this_market_currencies:
                    currency_code = this_market_currencies[currency_id]
                else:
                    for currency_record in curreny_lookup:
                        if 'i' not in currency_record:
                            pass
                        else:
                            if currency_record['c'] == currency_id:
                                currency_code = currency_record['a']
                                this_market_currencies[currency_id] = currency_record['a']

                currency = currency_code  # Currency

                # Instrument Data
                instr_list_url = self.base_url + "/api/1/instruments?productIds=" + id + "&slim=false"
                instrument_list = self.parse_pds_output(instr_list_url)
                if len(instrument_list) > 0:

                    instrumentId = instrument_list[0]
                    instrument_definition = self.translate_instrument_data(instrumentId)

                    point_value = str(int(instrument_definition['PointValue']))  # Point Value
                    tickValue = str(int(instrument_definition['TickValue']))  # Tick Value
                    tick_numerator = str(instrument_definition['TickSizeNum'])  # Tick Size Numerator
                    tick_denominator = str(instrument_definition['TickSizeDenom'])  # Tick Size Denominator
                    marketTypeId = str(instrument_definition['MarketId'])  # Market ID
                    priceDisplayDecimals = str(int(instrument_definition['PriceDec'])) if self.market in ['CME', 'TFEX', 'JPX'] else '0'  # Point Value Decimals
                    round_lot_qty = str(instrument_definition['RoundLotQty'])  # Round Lot Quantity
                    price_format = str(instrument_definition['DispFormatId'])  # Tick Fractional
                    price_display_type = str(instrument_definition['PriceDisplayTypeId'])  # Price Display Type
                    tick_table = str(instrument_definition['TickTableId'])  # Tick Table Name

                    # Generate Currently-Published Output Rows
                    pmg_values_line = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}'.format(
                        symbol, ptype, '0', point_value, priceDisplayDecimals, ' ', ' ', ' ', ' ', tick_numerator,
                        tick_denominator, currency, ' ', ' ', name)
                    pmg_values_list.append(pmg_values_line)

                    # Set correct Product Name based on user input value
                    adjusted_productName = None
                    if len(new_product_name) > 0:
                        adjusted_productName = " ".join([new_product_name, pmg_product_type_strings[ptype]])

                    # Set correct point value based on priceDisplayDecimals value
                    adjusted_point_value = None
                    if len(new_point_value) > 0:
                        adjusted_point_value = "".join([str(new_point_value), "0" * int(priceDisplayDecimals)])

                    # Generate PMG file Output Rows
                    # if self.market == 'JPX':
                    #     point_value = int(point_value) * int("1" + "7".zfill(int(priceDisplayDecimals)).replace("7", "0")) if int(priceDisplayDecimals) > 0 else point_value

                    output_point_value = adjusted_point_value if adjusted_point_value is not None else point_value
                    output_product_name = adjusted_productName if adjusted_productName is not None else name

                    if mds_pmerge_format:
                        self.get_market_id(self.market)
                        point_value = int(point_value)
                        pmg_file_line = ' ,{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'.format(
                            symbol, self.get_market_id(self.market), ptype, 'NULL', int(output_point_value), tick_numerator, tick_denominator, 'NULL', currency_id, 'NULL', output_product_name)
                    else:
                        pmg_file_line = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14}'.format(
                            symbol, ptype, '0', int(output_point_value), priceDisplayDecimals, ' ', ' ', ' ', ' ', tick_numerator,
                            tick_denominator, currency, ' ', ' ', output_product_name)
                    pmg_file_list.append(pmg_file_line)

        print("\n\nCurrently-Published pmerge values.")

        pmg_values_list.sort()
        for pmg_values_list_item in pmg_values_list:
            print(pmg_values_list_item)

        print("\n\nPMG File values.")

        pmg_file_list.sort()
        for pmg_file_list_item in pmg_file_list:
            print(pmg_file_list_item)

        print("Total product count = {}".format(str(len(self.all_products))))
        print("\n\nFinished.")

    def verify_ric_code_is_not_blank(self):
        # Verify there are no products without a Description

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        instruments_with_no_ric_code = []

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                if instrument_definition["RICCode"] is None:
                    instruments_with_no_ric_code.append(alias)
                    # else:
                    #     print("PASS: {} RIC Code = {}".format(alias, instrument_definition["RICCode"]))
            except StopIteration as e:
                print("\n\nFinished.")
                break

        if len(instruments_with_no_ric_code) > 0:
            print("FAIL: The following instruments have no RIC Code:")
            instruments_with_no_ric_code.sort()
            for i in instruments_with_no_ric_code:
                print("* {}".format(i))

    def verify_cme_SOFR_spreads_have_correct_combo_id(self):
        # Verify there are no CME SOFR Spreads with Combo ID = None

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        combo_type_is_wrong = []

        combo_type_dict = self.get_combo_type_dict()

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                name = instrument_definition["Name"]
                alias = instrument_definition["Alias"]
                combo_type = instrument_definition["ComboTypeId"]
                if ":AB" in name:
                    if combo_type != 20 or "Pack" not in alias:
                        combo_type_is_wrong.append((name, str("Pack" in alias), combo_type_dict[combo_type], url))
                elif ":FB" in name:
                    if combo_type != 21 or "Bundle" not in alias:
                        combo_type_is_wrong.append((name, str("Bundle" in alias), combo_type_dict[combo_type], url))
            except StopIteration as e:
                print("\n\nFinished.")
                break

        if len(combo_type_is_wrong) > 0:
            print("FAIL: {} instruments have incorrect Combination Type Info".format(len(combo_type_is_wrong)))
            print("||{}||".format("||".join(("Name", "Correct Combo displayed in Alias", "Combo Type", "URL"))))
            combo_type_is_wrong.sort()
            for combo_type in combo_type_is_wrong:
                print("|{}|".format(" | ".join(combo_type)))

    def verify_ric_and_bbc_code(self):
        # Verify RIC Code is correct

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        all_ric_codes = []
        instruments_with_no_ric_code = []
        instruments_with_dup_ric_code = []
        instruments_with_incorrect_ric_code = []
        all_bloomberg_codes = []
        instruments_with_no_bloomberg_code = []
        instruments_with_dup_bloomberg_code = []

        print("\n\nVerifying {} RIC and Bloomberg Codes in {}...".format(self.market, self.pdsdomain))

        while True:
            try:
                alias, ric = None, None
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                ric = instrument_definition["RICCode"]
                bbc = instrument_definition["BloombergCode"]
                alias_month = get_alias_term_values(alias.split(" ")[1])['month']
                ric_month = list(ric)[-2]
                maturity_date = instrument_definition["MaturityDate"]
                maturity_month = list(maturity_date)[4:6]
                if ric is None:
                    instruments_with_no_ric_code.append(": ".join([alias, url]))
                if ric in all_ric_codes:
                    instruments_with_dup_ric_code.append(": ".join([alias, url]))
                if self.month_codes[ric_month] != alias_month:
                    instruments_with_incorrect_ric_code.append(": ".join([alias, url]))
                else:
                    all_ric_codes.append(": ".join([alias, url]))

                if bbc is None:
                    instruments_with_no_bloomberg_code.append(": ".join([alias, url]))
                if bbc in all_bloomberg_codes:
                    instruments_with_dup_bloomberg_code.append(": ".join([alias, url]))
                else:
                    all_bloomberg_codes.append(": ".join([alias, url]))

            except StopIteration as e:
                break

        if len(instruments_with_no_ric_code) > 0:
            print("\nFAIL: {} instruments are missing RIC code:".format(len(instruments_with_no_ric_code)))
            instruments_with_no_ric_code.sort()
            for i in instruments_with_no_ric_code:
                print("*", i)

        if len(instruments_with_dup_ric_code) > 0:
            print("\nFAIL: {} duplicate RIC codes were found:".format(len(instruments_with_dup_ric_code)))
            instruments_with_dup_ric_code.sort()
            for i in instruments_with_dup_ric_code:
                print("*", i)

        if len(instruments_with_incorrect_ric_code) > 0:
            print("\nFAIL: {} incorrect RIC codes were found:".format(len(instruments_with_incorrect_ric_code)))
            instruments_with_incorrect_ric_code.sort()
            for i in instruments_with_incorrect_ric_code:
                print("*", i)

        if len(instruments_with_no_bloomberg_code) > 0:
            print("\nFAIL: {} instruments are missing Bloomberg code:".format(len(instruments_with_no_bloomberg_code)))
            instruments_with_no_bloomberg_code.sort()
            for i in instruments_with_no_bloomberg_code:
                print("*", i)

        if len(instruments_with_dup_bloomberg_code) > 0:
            print("\nFAIL: {} duplicate Bloomberg codes were found:".format(len(instruments_with_dup_bloomberg_code)))
            instruments_with_dup_bloomberg_code.sort()
            for i in instruments_with_dup_bloomberg_code:
                print("*", i)

        print("\n\nFinished.")
        print("Tested {} Products and {} Instruments".format(str(len(self.all_product_ids)), str(len(self.all_instrument_overview))))

    def verify_exchange_ticker(self):
        # Verify Exchange Ticker is correct

        self.get_all_product_ids()
        self.get_all_instrument_ids()
        get_instrument_id = self.instrument_id_generator()
        all_tickers = {}
        instruments_with_no_ticker = []
        instruments_with_dup_ticker = {}

        print("\n\nVerifying Exchange Tickers...")

        while True:
            try:
                instrument_id = str(next(get_instrument_id))
                url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                instrument = self.parse_pds_output(url)
                instrument = instrument[0]
                instrument_definition = self.translate_instrument_data(instrument)
                alias = instrument_definition["Alias"]
                ticker = instrument_definition["ExchangeTicker"]
                # if " " in ticker:
                #     print(alias, ":", [ticker])
                if ticker is None:
                    instruments_with_no_ticker.append(alias)
                if ticker in all_tickers.values():
                    for k, v in all_tickers.iteritems():
                        if v == ticker:
                            instruments_with_dup_ticker[ticker] = (alias, k)
                else:
                    all_tickers[alias] = ticker

            except StopIteration as e:
                break

        if len(instruments_with_no_ticker) + len(instruments_with_dup_ticker) > 0:
            if len(instruments_with_no_ticker) > 0:
                print("FAIL: {} instruments are missing Exchange Ticker:".format(len(instruments_with_no_ticker)))
                instruments_with_no_ticker.sort()
                for missing_ticker in instruments_with_no_ticker:
                    print("*", missing_ticker)
            if len(instruments_with_dup_ticker) > 0:
                print("FAIL: {} Duplicate Exchange Tickers were found:".format(len(instruments_with_dup_ticker)))
                for dup_key, dup_value in instruments_with_dup_ticker.iteritems():
                    print("*", dup_key, dup_value)
        else:
            print("\n\nFinished.")

    def verify_descriptions_are_consistent(self):
        # Verify that each product's Description is consistent across product types

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        list_of_symbols = []
        all_descriptions = {}

        print("\n\nVerifying Product Descriptions in {}...".format(self.pdsdomain))

        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition['Symbol']
                if symbol not in list_of_symbols:
                    list_of_symbols.append(symbol)
                if product_definition['Name'] is None:
                    product_definition['Name'] = "<BLANK>"
                if symbol not in all_descriptions:
                    all_descriptions[symbol] = [" = ".join([product_definition["TypeId"],
                                                            product_definition['Name']])]
                else:
                    for list_items in all_descriptions[symbol]:
                        if product_definition['Name'] not in list_items:
                            all_descriptions[symbol].append(" = ".join([product_definition["TypeId"],
                                                                        product_definition['Name']]))
            except StopIteration as e:
                break

        for s in list_of_symbols:
            if len(all_descriptions[s]) > 1:
                print("||{}|| || ||".format(s))
                for p in all_descriptions[s]:
                    print("| |{}|{}|".format(p.split(" = ")[0], p.split(" = ")[1]))
        print("\n\nFinished.")

    def create_jpx_description_mapping(self):

        jpx_product_map = {"GASO": "GAS", "KERO": "KRO", "GSOL": "GAO", "CRUD": "DBAI", "CGAS": "CGAS", "CKER": "CKRO",
                           "TWBL": "EWB", "TEBL": "EEB", "TWPL": "EWP", "TEPL": "EEP", "BANK": "BANK", "DJIA": "DJIA",
                           "FTC50": "FT50", "JGBM": "JBM", "JGBL": "JBL", "JGBLM": "JBLM", "JGBSL": "JBS",
                           "JN400": "400", "MOTHE": "MOTH", "NK225": "225", "NK225M": "225M", "NK225W": "225W",
                           "NKDIV": "NKDV", "NKVI": "NVI", "OGDCD": "GLDD", "OGOLD": "GLD", "OM-GD": "GLDM",
                           "OPALL": "PALD", "OPLAT": "PLT", "OM-PT": "PLTM", "OPTCD": "PLTD", "ORSS3": "RSS3",
                           "OSILV": "SILV", "OTGAB": "REDB", "OTGCN": "CORN", "OTGSB": "SOYB", "OTSR2": "TSR2",
                           "REIT": "REIT", "RNP": "RNP", "TPX30": "C30", "TAIEX": "TAIX", "TOPIX": "TPX",
                           "TOPIXM": "TPXM", "OM-PT|OM-GD": "GLDM|PLTM", "OPTCD|OGDCD": "GLDD|PLTD",
                           "OTSR2|ORSS3": "RSS3|TSR2", "CKER|CGAS": "CGAS|CKRO", "CRUD|GASO": "GAS|DBAI",
                           "CRUD|GSOL": "GAO|DBAI", "CRUD|KERO": "KRO|DBAI", "GSOL|GASO": "GAS|GAO",
                           "GSOL|KERO": "KRO|GAO", "KERO|GASO": "GAS|KRO", "TWBL|TEBL": "EEB|EWB",
                           "TWPL|TEPL": "EEP|EWP", "TBGA": None, "TLGA": None, "TBKE": None, "TLKE": None, "TBGO": None,
                           "TLGO": None, "T30D": None, "TPDIV": None, "TBGO|GSOL": None, "TLKE|TLGA": None,
                           "TLKE|CKER": None, "TLKE|CGAS": None, "TLGO|TLKE": None, "TLGO|TLGA": None,
                           "TLGO|CKER": None, "TLGO|CGAS": None, "TLGA|CKER": None, "TLGA|CGAS": None,
                           "TBKE|TBGA": None, "TBKE|KERO": None, "TBKE|GSOL": None, "TBKE|GASO": None,
                           "TBGA|GASO": None, "TBGA|GSOL": None, "TBGA|KERO": None, "TBGO|GASO": None,
                           "TBGO|GSOL": None, "TBGO|KERO": None, "TBGO|TBGA": None, "TBGO|TBKE": None,
                           "CRUD|TBGA": None, "CRUD|TBGO": None, "CRUD|TBKE": None, "1306": "1306", "1308": "1308", "1309": "1309", "1320": "1320", "1321": "1321", "1328": "1328", "1330": "1330", "1343": "1343", "1540": "1540", "1591": "1591", "1605": "1605", "1615": "1615", "1671": "1671", "1801": "1801", "1803": "1803", "1808": "1808", "1812": "1812", "1925": "1925", "1928": "1928", "1944": "1944", "1963": "1963", "2002": "2002", "2432": "2432", "2502": "2502", "2503": "2503", "2531": "2531", "2651": "2651", "2768": "2768", "2802": "2802", "2914": "2914", "3249": "3249", "3269": "3269", "3279": "3279", "3382": "3382", "3402": "3402", "3405": "3405", "3407": "3407", "3436": "3436", "3462": "3462", "3632": "3632", "3861": "3861", "3863": "3863", "4005": "4005", "4062": "4062", "4063": "4063", "4183": "4183", "4188": "4188", "4307": "4307", "4324": "4324", "4452": "4452", "4502": "4502", "4503": "4503", "4519": "4519", "4523": "4523", "4543": "4543", "4568": "4568", "4631": "4631", "4661": "4661", "4676": "4676", "4689": "4689", "4704": "4704", "4716": "4716", "4739": "4739", "4901": "4901", "4902": "4902", "4911": "4911", "5020": "5020", "5108": "5108", "5201": "5201", "5202": "5202", "5214": "5214", "5333": "5333", "5401": "5401", "5406": "5406", "5411": "5411", "5631": "5631", "5706": "5706", "5711": "5711", "5713": "5713", "5801": "5801", "5802": "5802", "5803": "5803", "5901": "5901", "5938": "5938", "6178": "6178", "6273": "6273", "6301": "6301", "6302": "6302", "6305": "6305", "6326": "6326", "6367": "6367", "6460": "6460", "6471": "6471", "6479": "6479", "6501": "6501", "6502": "6502", "6503": "6503", "6592": "6592", "6594": "6594", "6674": "6674", "6701": "6701", "6702": "6702", "6703": "6703", "6723": "6723", "6724": "6724", "6752": "6752", "6753": "6753", "6758": "6758", "6762": "6762", "6770": "6770", "6806": "6806", "6857": "6857", "6861": "6861", "6902": "6902", "6952": "6952", "6954": "6954", "6963": "6963", "6971": "6971", "6976": "6976", "6981": "6981", "6988": "6988", "7011": "7011", "7012": "7012", "7013": "7013", "7181": "7181", "7182": "7182", "7201": "7201", "7202": "7202", "7203": "7203", "7259": "7259", "7261": "7261", "7267": "7267", "7269": "7269", "7272": "7272", "7731": "7731", "7733": "7733", "7741": "7741", "7751": "7751", "7752": "7752", "7911": "7911", "7912": "7912", "7974": "7974", "8001": "8001", "8002": "8002", "8031": "8031", "8035": "8035", "8053": "8053", "8058": "8058", "8113": "8113", "8252": "8252", "8253": "8253", "8267": "8267", "8306": "8306", "8308": "8308", "8309": "8309", "8316": "8316", "8411": "8411", "8473": "8473", "8591": "8591", "8601": "8601", "8604": "8604", "8630": "8630", "8725": "8725", "8750": "8750", "8766": "8766", "8795": "8795", "8801": "8801", "8802": "8802", "8830": "8830", "8951": "8951", "8952": "8952", "8953": "8953", "8954": "8954", "8955": "8955", "8957": "8957", "8961": "8961", "8967": "8967", "8972": "8972", "8976": "8976", "8984": "8984", "9005": "9005", "9020": "9020", "9021": "9021", "9022": "9022", "9062": "9062", "9064": "9064", "9101": "9101", "9104": "9104", "9107": "9107", "9142": "9142", "9201": "9201", "9202": "9202", "9301": "9301", "9404": "9404", "9432": "9432", "9433": "9433", "9434": "9434", "9437": "9437", "9501": "9501", "9502": "9502", "9503": "9503", "9504": "9504", "9506": "9506", "9508": "9508", "9531": "9531", "9532": "9532", "9613": "9613", "9735": "9735", "9766": "9766", "9831": "9831", "9983": "9983", "9984": "9984"}
        prod_types = {"FUT": "1", "MLEG": "2", "OPT": "3",}

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        list_of_symbols = []

        print("\n\nGenerating Product Descriptions...")

        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition['Symbol']
                symbol = jpx_product_map[symbol] if symbol in jpx_product_map and jpx_product_map[symbol] is not None else symbol
                product_type = product_definition['TypeId']
                if product_type == 'STRA':
                    continue
                if product_definition['Name'] is None:
                    product_definition['Name'] = ""
                try:
                    list_of_symbols.append("".join([symbol, ",", prod_types[product_type], ",,,,,,,,,,,,,", product_definition['Name']]))
                except TypeError:
                    print("TypeError:", symbol, product_definition['Name'])

            except StopIteration as e:
                break

        for s in list_of_symbols:
            print(s)
        print("\n\nFinished.")
        print("\n\nProcessed {} products.".format(str(len(list_of_symbols))))

    def get_currency_codes(self):

        curr_url = self.base_url + "/api/1/currencyrates?request_id=pds_market_explorer-" + self.base_url.replace(
            "https://", "")
        currencies = self.parse_pds_output(curr_url)
        for currency in currencies:
            if currency["ft"] == "ZWL":
                print(",".join([currency["tt"], str(currency["ti"])]))

    def search_products(self):

        for query in self.prod_list:
            url = self.base_url + "/api/1/instrumentsearch?query=" + query + "&marketIds=" + self.get_market_id(
                self.market) + "&request_id=pds_market_explorer-pds-ext-uat-cert.trade.tt--eeeeecb0-a628-48f2-ae65-fc5a1399ba44"
            print(url)
            output = self.parse_pds_output(url)
            for o in output:
                print(o['a'])

                # print("Found {0} records in PDS for {1}".format(output, query))

    def verify_security_id(self):
        # Verify there are no products with missing or incorrect Security ID

        self.get_all_product_ids()
        self.get_security_exch_ids()
        get_product_id = self.product_id_generator()
        instruments_with_incorrect_security_id = []
        instruments_with_missing_security_id = []
        security_ids = None
        if self.market == "TFX":
            security_ids = {}
        elif self.market == "HKEX":
            security_ids = {}
        elif self.market == "JPX":
            security_ids = {}
        elif self.market == "SGX":
            security_ids = {"AMF": "NZX", "BTR": "NZX", "MKP": "NZX", "SMP": "NZX", "WMP": "NZX", "AJ": "SFX",
                            "AU": "SFX", "CY": "SFX", "EC": "SFX", "IDR": "SFX", "INR": "SFX", "INX": "SFX",
                            "IU": "SFX", "KJ": "SFX", "KRW": "SFX", "KU": "SFX", "MUC": "SFX", "MYR": "SFX",
                            "MYS": "SFX", "PHP": "SFX", "SND": "SFX", "SY": "SFX", "TD": "SFX", "TU": "SFX",
                            "TWD": "SFX", "UC": "SFX", "UJ": "SFX", "US": "SFX", "UY": "SFX", "YS": "SFX", "1MF": "COM",
                            "3MF": "COM", "ACF": "COM", "BZF": "COM", "BZNF": "COM", "CCF": "COM", "COH": "COM",
                            "COHF": "COM", "EE": "COM", "EF": "COM", "FEF": "COM", "GOF": "COM", "LICF": "COM",
                            "LIHF": "COM", "LP": "COM", "LPF": "COM", "M42F": "COM", "M58F": "COM", "M65F": "COM",
                            "MEGF": "COM", "MF5F": "COM", "MTF": "COM", "MXF": "COM", "NJF": "COM", "PXF": "COM",
                            "PXNF": "COM", "RB": "COM", "RBF": "COM", "RT": "COM", "SMCF": "COM", "TF": "COM",
                            "VCF": "COM", "AJRT": "IDX", "CN": "IDX", "EAXJ": "IDX", "EEM": "IDX", "EEMA": "IDX",
                            "EJP": "IDX", "EJRT": "IDX", "FAXJ": "IDX", "FCH": "IDX", "FEM": "IDX", "FEMA": "IDX",
                            "FID": "IDX", "FMY": "IDX", "FNAU": "IDX", "FNAXJ": "IDX", "FNEA": "IDX", "FNEM": "IDX",
                            "FNEMK": "IDX", "FNID": "IDX", "FNJP": "IDX", "FNMY": "IDX", "FNNZ": "IDX", "FNPH": "IDX",
                            "FNSA": "IDX", "FNTH": "IDX", "FNTW": "IDX", "FNVN": "IDX", "FPH": "IDX", "FTH": "IDX",
                            "FVN": "IDX", "GIN": "IDX", "GINB": "IDX", "GINF": "IDX", "GINI": "IDX", "IN": "IDX",
                            "INB": "IDX", "JB": "IDX", "JG": "IDX", "ND": "IDX", "NK": "IDX", "NR": "IDX", "NS": "IDX",
                            "NSG": "IDX", "NSP": "IDX", "NAU": "IDX", "NEAXC": "IDX", "NEAXK": "IDX", "NEM": "IDX",
                            "NEMEA": "IDX", "NID": "IDX", "NJP": "IDX", "NNZ": "IDX", "NPH": "IDX", "NTH": "IDX",
                            "NTW": "IDX", "NVN": "IDX", "NU": "IDX", "SGP": "IDX", "SRT": "IDX", "ST": "IDX",
                            "TWN": "IDX", "YAHY": "IDX", "YARE": "IDX", "YCDD": "IDX", "YCLI": "IDX", "YDBS": "IDX",
                            "YGEN": "IDX", "YKEP": "IDX", "YOCB": "IDX", "YSTT": "IDX", "YTBE": "IDX", "YTGL": "IDX",
                            "YUOB": "IDX", "YWIL": "IDX", "YYZJ": "IDX", "ZACE": "IDX", "ZADS": "IDX", "ZAPN": "IDX",
                            "ZARB": "IDX", "ZAXS": "IDX", "ZBAF": "IDX", "ZBHA": "IDX", "ZBHI": "IDX", "ZBJA": "IDX",
                            "ZBOS": "IDX", "ZBPC": "IDX", "ZCIP": "IDX", "ZCOA": "IDX", "ZDRR": "IDX", "ZEIM": "IDX",
                            "ZGAI": "IDX", "ZGRA": "IDX", "ZHCL": "IDX", "ZHDB": "IDX", "ZHDB": "IDX", "ZHMC": "IDX",
                            "ZHND": "IDX", "ZHPC": "IDX", "ZHUV": "IDX", "ZICI": "IDX", "ZIHF": "IDX", "ZIIB": "IDX",
                            "ZINF": "IDX", "ZIOC": "IDX", "ZITC": "IDX", "ZKMB": "IDX", "ZLPC": "IDX", "ZLT": "IDX",
                            "ZMM": "IDX", "ZMSI": "IDX", "ZNTP": "IDX", "ZONG": "IDX", "ZPWG": "IDX", "ZRIL": "IDX",
                            "ZSBI": "IDX", "ZSEA": "IDX", "ZSUN": "IDX", "ZTAT": "IDX", "ZTCS": "IDX", "ZTEC": "IDX",
                            "ZTSM": "IDX", "ZTTM": "IDX", "ZUPL": "IDX", "ZUTC": "IDX", "ZVED": "IDX", "ZWPR": "IDX",
                            "ZYES": "IDX", "ZZEE": "IDX"}
        elif self.market == "SGX_GIFT":
            security_ids = {}
        elif self.market == "KRX":
            security_ids = {}

        print("\n\nVerifying {} Security IDs in {}...".format(self.market, self.pdsdomain))

        while True:
            try:
                fail = False
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition["Symbol"]
                product_type = product_definition["TypeId"]
                mic_code = product_definition["MICCode"]
                security_id = product_definition["SecExchId"]
                security_id_str = self.all_sec_exch_ids[security_id]
                if security_id is None:
                    security_ids[symbol] = "None"
                    fail = True
                if symbol not in security_ids:
                    if security_id != 39:
                        fail = True
                else:
                    if security_id_str != security_ids[symbol]:
                        fail = True
                if fail:
                    if type(security_ids) == dict:
                        error_str = "{} {} Security ID: Expected: {} Actual: {}".format(symbol, product_type,
                                                                                        security_ids[symbol],
                                                                                        security_id_str)
                    else:
                        error_str = "{} {} Security ID: Expected: {} Actual: {}".format(symbol, product_type,
                                                                                        security_ids[symbol],
                                                                                        security_id_str)
                    instruments_with_incorrect_security_id.append(error_str)
            except StopIteration as e:
                break

        if len(instruments_with_incorrect_security_id) > 0:
            print("FAIL: The following products have missing or incorrect MIC code:")
            instruments_with_incorrect_security_id.sort()
            for p in instruments_with_incorrect_security_id:
                print("* {}".format(p))

        elif len(instruments_with_missing_security_id) > 0:
            print("FAIL: {} products have missing MIC code:".format(str(len(instruments_with_missing_security_id))))
            instruments_with_missing_security_id.sort()
            for p in instruments_with_missing_security_id:
                print("* {}".format(p))
        else:
            print("\n\nFinished.")
        print("Tested {} Products.".format(str(len(self.all_product_ids))))

    def verify_tocom_to_ose(self):

        for query in self.prod_list:
            for prod_type in self.product_types:
                ose_query = "".join(["O", query])
                tocom_expiries = []
                ose_expiries = []
                tocom_url = self.base_url + "/api/1/instrumentsearch?query=" + query + "&marketIds=68&productTypeIds=" + prod_type + "&request_id=pds_market_explorer-pds-ext-uat-cert.trade.tt--eeeeecb0-a628-48f2-ae65-fc5a1399ba44"
                ose_url = self.base_url + "/api/1/instrumentsearch?query=" + ose_query + "&marketIds=71&productTypeIds=" + prod_type + "&request_id=pds_market_explorer-pds-ext-uat-cert.trade.tt--eeeeecb0-a628-48f2-ae65-fc5a1399ba44"
                tocom_output = self.parse_pds_output(tocom_url)
                ose_output = self.parse_pds_output(ose_url)
                for tocom_expiry in tocom_output:
                    if tocom_expiry["a"].startswith(query):
                        tocom_expiries.append(tocom_expiry["a"])
                for ose_expiry in ose_output:
                    if ose_expiry["a"].startswith(ose_query):
                        ose_expiries.append(ose_expiry["a"])
                while len(ose_expiries) != len(tocom_expiries):
                    for ose_expiry in ose_expiries:
                        if ose_expiry.split(" ")[1] not in str(tocom_expiries):
                            ose_expiries.remove(ose_expiry)
                tocom_expiries.sort()
                ose_expiries.sort()

                for e in range(0, len(tocom_expiries)):
                    if tocom_expiries[e].split(" ")[1] != ose_expiries[e].split(" ")[1]:
                        print("Found discrepancy in {0}. {1} and {2} do not match.".format(query, tocom_expiries[e],
                                                                                           ose_expiries[e]))

    def verify_tocom_to_ose_instruments(self):
        # Verify that each instrument's Alias is consistent across two environments

        all_aliases_1 = {}
        all_aliases_2 = {}
        missing_from_1 = []
        missing_from_2 = []
        mismatched_aliases = []
        missing_aliases = []
        envs = []
        incorrect_sec_exchange = []

        test_pass_count = 1
        for dictionary in (all_aliases_1, all_aliases_2):
            if test_pass_count == 2:
                self.pdsdomain = "int-stage-cert"
            pds_url = "".join(["https://pds-", self.pdsdomain, ".trade.tt"])
            self.base_url = pds_url
            envs.append(self.pdsdomain)
            self.get_all_product_ids()
            get_product_id = self.product_id_generator()
            while True:
                try:
                    product_id = str(next(get_product_id))
                    prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                    product = self.parse_pds_output(prod_url)
                    product_definition = self.translate_product_data(product)
                    if "Invalid product" in product_definition:
                        print("ERROR! Product Does Not Exist in {}!".format(envs[1]))
                    else:
                        symbol = product_definition['Symbol']
                        prod_type = product_definition["TypeId"]
                        sec_exch = product_definition['Security_Exchange']
                        instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id
                        instrument_list = self.parse_pds_output(instr_list_url)
                        if test_pass_count == 1:
                            if len(instrument_list) > 0:
                                if symbol.startswith("O"):
                                    if sec_exch != 293:
                                        incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                                else:
                                    if sec_exch != 292:
                                        incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                        for instrument in instrument_list:
                            instrument_definition = self.translate_instrument_data(instrument)
                            alias = instrument_definition["Alias"]
                            name = instrument_definition["Name"]
                            instr = str(instrument["i"])
                            dictionary[name] = [alias, ''.join([self.base_url, "/api/1/instruments?instrumentIds=",
                                                                instr])]
                except StopIteration as e:
                    break
            test_pass_count += 1

        if all_aliases_1.keys() != all_aliases_2.keys():
            for k, v in all_aliases_1.items():
                if k not in all_aliases_2:
                    missing_from_2.append({k: v[0]})
            for k, v in all_aliases_2.items():
                if k not in all_aliases_1:
                    missing_from_1.append({k: v[0]})

        print("#" * 40)
        print("# Comparing {} to {}".format(envs[0], envs[1]))
        print("#" * 40 + "\n")

        if len(missing_from_2) > 0:
            print("\nFAIL! {} instruments are missing from {}:".format(len(missing_from_2), envs[1]))
            for missing_2 in missing_from_2:
                print(missing_2)
                for key in missing_2.keys():
                    all_aliases_1.pop(key)

        if len(missing_from_1) > 0:
            print("\nFAIL! {} instruments are missing from {}:".format(len(missing_from_1), envs[0]))
            for missing_1 in missing_from_1:
                print(missing_1)
                for key in missing_1.keys():
                    all_aliases_2.pop(key)

        for k, v in all_aliases_1.items():
            if all_aliases_1[k][0] != all_aliases_2[k][0]:
                alias1 = "<BLANK>" if len(all_aliases_1[k]) == 0 else all_aliases_1[k]
                alias2 = "<BLANK>" if len(all_aliases_2[k]) == 0 else all_aliases_2[k]
                mismatched_aliases.append({k: [alias1, alias2]})
                all_aliases_2.pop(k)

        for k, v in all_aliases_2.items():
            if all_aliases_2[k][0] != all_aliases_1[k][0]:
                alias1 = "<BLANK>" if len(all_aliases_1[k]) == 0 else all_aliases_1[k]
                alias2 = "<BLANK>" if len(all_aliases_2[k]) == 0 else all_aliases_2[k]
                mismatched_aliases.append({k: [alias1, alias2]})
                all_aliases_1.pop(k)

    def verify_instruments_across_two_envs(self):
        # Verify that each instrument's Alias is consistent across two environments

        all_aliases_1 = {}
        all_aliases_2 = {}
        missing_from_1 = []
        missing_from_2 = []
        mismatched_aliases = []
        mismatched_expiries = []
        missing_aliases = []
        envs = []
        incorrect_sec_exchange = []

        test_pass_count = 1
        for dictionary in (all_aliases_1, all_aliases_2):
            if test_pass_count == 2:
                self.pdsdomain = "int-stage-cert"
            pds_url = "".join(["https://pds-", self.pdsdomain, ".trade.tt"])
            self.base_url = pds_url
            envs.append(self.pdsdomain)
            self.get_all_product_ids()
            get_product_id = self.product_id_generator()
            while True:
                try:
                    product_id = str(next(get_product_id))
                    prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                    product = self.parse_pds_output(prod_url)
                    product_definition = self.translate_product_data(product)
                    if "Invalid product" in product_definition:
                        print("ERROR! Product Does Not Exist in {}!".format(envs[1]))
                    else:
                        symbol = product_definition['Symbol']
                        prod_type = product_definition["TypeId"]
                        sec_exch = product_definition['SecExchId']
                        instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id
                        instrument_list = self.parse_pds_output(instr_list_url)
                        # if test_pass_count == 1:
                        #     if len(instrument_list) > 0:
                        #         if symbol.startswith("O"):
                        #             if sec_exch != 293:
                        #                 incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                        #         else:
                        #             if sec_exch != 292:
                        #                 incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                        for instr in instrument_list:
                            instrument_id = str(instr["i"])
                            url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                            instrument = self.parse_pds_output(url)
                            instrument = instrument[0]
                            instrument_definition = self.translate_instrument_data(instrument)
                            alias = instrument_definition["Alias"]
                            name = instrument_definition["Name"]
                            exp = instrument_definition["ExpiryDate"]
                            instr = str(instrument["i"])
                            ric = instrument_definition["RICCode"]
                            dictionary[name] = [alias, exp, ric] #  , ''.join([self.base_url, "/api/1/instruments?instrumentIds=",
                                                                # instr])]
                except StopIteration as e:
                    break
            test_pass_count += 1

        if all_aliases_1.keys() != all_aliases_2.keys():
            for k, v in all_aliases_1.items():
                if k not in all_aliases_2:
                    missing_from_2.append({k: v[0]})
            for k, v in all_aliases_2.items():
                if k not in all_aliases_1:
                    missing_from_1.append({k: v[0]})

        for k, v in all_aliases_1.items():
            if v != all_aliases_2[k]:
                print("{} {} does not match {} {}".format(envs[1], v, envs[0], all_aliases_2[k]))

        print("#" * 40)
        print("# Comparing {} to {}".format(envs[0], envs[1]))
        print("#" * 40 + "\n")

        if len(missing_from_2) > 0:
            print("\nFAIL! {} instruments are missing from {}:".format(len(missing_from_2), envs[1]))
            for missing_2 in missing_from_2:
                print(missing_2)
                # for key in missing_2.keys():
                #     all_aliases_1.pop(key)

        if len(missing_from_1) > 0:
            print("\nFAIL! {} instruments are missing from {}:".format(len(missing_from_1), envs[0]))
            for missing_1 in missing_from_1:
                print(missing_1)
                # for key in missing_1.keys():
                #     all_aliases_2.pop(key)

        for k, v in all_aliases_1.items():
            if k in all_aliases_2:
                if all_aliases_1[k][0] == all_aliases_2[k][0]:
                    if all_aliases_1[k][1] != all_aliases_2[k][1]:
                        mismatched_expiries.append({k: [all_aliases_1[k][1], all_aliases_2[k][1]]})
                    all_aliases_2.pop(k)
            else:
                continue

        for k, v in all_aliases_2.items():
            if k in all_aliases_1:
                if all_aliases_2[k][0] == all_aliases_1[k][0]:
                    if all_aliases_2[k][1] != all_aliases_1[k][1]:
                        mismatched_expiries.append({k: [all_aliases_2[k][1], all_aliases_1[k][1]]})
            else:
                continue

        if len(mismatched_aliases) > 0:
            print("\nFAIL! {} Alias mismatches detected:".format(len(mismatched_aliases)))
            for mismatch in mismatched_aliases:
                for k, v in mismatch.items():
                    print("* Series Key / Name: {}".format(k))
                    for i in v:
                        print("** {}: {}".format(i[0], i[1]))
                        # print("{}:\n{}\n{}".format(k, mismatch[k][0], mismatch[k][1]))

        if len(mismatched_expiries) > 0:
            print("\nFAIL! {} Expiry Date mismatches detected:".format(len(mismatched_expiries)))
            for mismatch in mismatched_expiries:
                for k, v in mismatch.items():
                    print("* Series Key / Name: {}".format(k))
                    for i in v:
                        print(i)

        if len(missing_aliases) > 0:
            print("\nFAIL! {} missing Aliases detected:".format(len(missing_aliases)))
            for missing_alias in missing_aliases:
                print(missing_alias)

        if len(incorrect_sec_exchange) > 0:
            print("\nFAIL! {} products have Security Exchange set incorrectly:".format(len(incorrect_sec_exchange)))
            for incorrect_sec_exchange_id in incorrect_sec_exchange:
                print(incorrect_sec_exchange_id)

        print("\n\nFinished.")

    def verify_environment_diff(self):
        # Verify that each instrument's Alias is consistent across two environments

        symbol_chg_map =  {"GF50": "GF"}

        # symbol_chg_map =  {"GASO": "GAS", "KERO": "KRO", "GSOL": "GAO", "CRUD": "DBAI", "CGAS": "CGAS", "CKER": "CKRO",
        #                    "TWBL": "EWB", "TEBL": "EEB", "TWPL": "EWP", "TEPL": "EEP", "BANK": "BANK", "DJIA": "DJIA",
        #                    "FTC50": "FT50", "JGBM": "JBM", "JGBL": "JBL", "JGBLM": "JBLM", "JGBSL": "JBS",
        #                    "JN400": "400", "MOTHE": "MOTH", "NK225": "225", "NK225M": "225M", "NK225W": "225W",
        #                    "NKDIV": "NKDV", "NKVI": "NVI", "OGDCD": "GLDD", "OGOLD": "GLD", "OM-GD": "GLDM",
        #                    "OPALL": "PALD", "OPLAT": "PLT", "OM-PT": "PLTM", "OPTCD": "PLTD", "ORSS3": "RSS3",
        #                    "OSILV": "SILV", "OTGAB": "REDB", "OTGCN": "CORN", "OTGSB": "SOYB", "OTSR2": "TSR2",
        #                    "REIT": "REIT", "RNP": "RNP", "TPX30": "C30", "TAIEX": "TAIX", "TOPIX": "TPX",
        #                    "TOPIXM": "TPXM", "OM-PT|OM-GD": "GLDM|PLTM", "OPTCD|OGDCD": "GLDD|PLTD",
        #                    "OTSR2|ORSS3": "RSS3|TSR2", "CKER|CGAS": "CGAS|CKRO", "CRUD|GASO": "GAS|DBAI",
        #                    "CRUD|GSOL": "GAO|DBAI", "CRUD|KERO": "KRO|DBAI", "GSOL|GASO": "GAS|GAO",
        #                    "GSOL|KERO": "KRO|GAO", "KERO|GASO": "GAS|KRO", "TWBL|TEBL": "EEB|EWB",
        #                    "TWPL|TEPL": "EEP|EWP", "TBGA": None, "TLGA": None, "TBKE": None, "TLKE": None, "TBGO": None,
        #                    "TLGO": None, "T30D": None, "TPDIV": None, "TBGO|GSOL": None, "TLKE|TLGA": None,
        #                    "TLKE|CKER": None, "TLKE|CGAS": None, "TLGO|TLKE": None, "TLGO|TLGA": None,
        #                    "TLGO|CKER": None, "TLGO|CGAS": None, "TLGA|CKER": None, "TLGA|CGAS": None,
        #                    "TBKE|TBGA": None, "TBKE|KERO": None, "TBKE|GSOL": None, "TBKE|GASO": None,
        #                    "TBGA|GASO": None, "TBGA|GSOL": None, "TBGA|KERO": None, "TBGO|GASO": None,
        #                    "TBGO|GSOL": None, "TBGO|KERO": None, "TBGO|TBGA": None, "TBGO|TBKE": None,
        #                    "CRUD|TBGA": None, "CRUD|TBGO": None, "CRUD|TBKE": None, "1306": "1306", "1308": "1308", "1309": "1309", "1320": "1320", "1321": "1321", "1328": "1328", "1330": "1330", "1343": "1343", "1540": "1540", "1591": "1591", "1605": "1605", "1615": "1615", "1671": "1671", "1801": "1801", "1803": "1803", "1808": "1808", "1812": "1812", "1925": "1925", "1928": "1928", "1944": "1944", "1963": "1963", "2002": "2002", "2432": "2432", "2502": "2502", "2503": "2503", "2531": "2531", "2651": "2651", "2768": "2768", "2802": "2802", "2914": "2914", "3249": "3249", "3269": "3269", "3279": "3279", "3382": "3382", "3402": "3402", "3405": "3405", "3407": "3407", "3436": "3436", "3462": "3462", "3632": "3632", "3861": "3861", "3863": "3863", "4005": "4005", "4062": "4062", "4063": "4063", "4183": "4183", "4188": "4188", "4307": "4307", "4324": "4324", "4452": "4452", "4502": "4502", "4503": "4503", "4519": "4519", "4523": "4523", "4543": "4543", "4568": "4568", "4631": "4631", "4661": "4661", "4676": "4676", "4689": "4689", "4704": "4704", "4716": "4716", "4739": "4739", "4901": "4901", "4902": "4902", "4911": "4911", "5020": "5020", "5108": "5108", "5201": "5201", "5202": "5202", "5214": "5214", "5333": "5333", "5401": "5401", "5406": "5406", "5411": "5411", "5631": "5631", "5706": "5706", "5711": "5711", "5713": "5713", "5801": "5801", "5802": "5802", "5803": "5803", "5901": "5901", "5938": "5938", "6178": "6178", "6273": "6273", "6301": "6301", "6302": "6302", "6305": "6305", "6326": "6326", "6367": "6367", "6460": "6460", "6471": "6471", "6479": "6479", "6501": "6501", "6502": "6502", "6503": "6503", "6592": "6592", "6594": "6594", "6674": "6674", "6701": "6701", "6702": "6702", "6703": "6703", "6723": "6723", "6724": "6724", "6752": "6752", "6753": "6753", "6758": "6758", "6762": "6762", "6770": "6770", "6806": "6806", "6857": "6857", "6861": "6861", "6902": "6902", "6952": "6952", "6954": "6954", "6963": "6963", "6971": "6971", "6976": "6976", "6981": "6981", "6988": "6988", "7011": "7011", "7012": "7012", "7013": "7013", "7181": "7181", "7182": "7182", "7201": "7201", "7202": "7202", "7203": "7203", "7259": "7259", "7261": "7261", "7267": "7267", "7269": "7269", "7272": "7272", "7731": "7731", "7733": "7733", "7741": "7741", "7751": "7751", "7752": "7752", "7911": "7911", "7912": "7912", "7974": "7974", "8001": "8001", "8002": "8002", "8031": "8031", "8035": "8035", "8053": "8053", "8058": "8058", "8113": "8113", "8252": "8252", "8253": "8253", "8267": "8267", "8306": "8306", "8308": "8308", "8309": "8309", "8316": "8316", "8411": "8411", "8473": "8473", "8591": "8591", "8601": "8601", "8604": "8604", "8630": "8630", "8725": "8725", "8750": "8750", "8766": "8766", "8795": "8795", "8801": "8801", "8802": "8802", "8830": "8830", "8951": "8951", "8952": "8952", "8953": "8953", "8954": "8954", "8955": "8955", "8957": "8957", "8961": "8961", "8967": "8967", "8972": "8972", "8976": "8976", "8984": "8984", "9005": "9005", "9020": "9020", "9021": "9021", "9022": "9022", "9062": "9062", "9064": "9064", "9101": "9101", "9104": "9104", "9107": "9107", "9142": "9142", "9201": "9201", "9202": "9202", "9301": "9301", "9404": "9404", "9432": "9432", "9433": "9433", "9434": "9434", "9437": "9437", "9501": "9501", "9502": "9502", "9503": "9503", "9504": "9504", "9506": "9506", "9508": "9508", "9531": "9531", "9532": "9532", "9613": "9613", "9735": "9735", "9766": "9766", "9831": "9831", "9983": "9983", "9984": "9984"}

        incorrect_cdds = []
        incorrect_tick_value_strs = []
        product_family_id_mapping = []
        product_id_mapping = []
        instrument_id_mapping = []

        environments = ["int-dev-sim", "ext-prod-live"]  # If both environments are the same, will default to comparing
                                                         # market to market_dev
        all_products = {}
        all_instruments = {}
        total_instrument_count = 0
        env1_total_product_count = 0
        env2_total_product_count = 0
        tested_product_count = 0
        tested_instrument_count = 0

        env_count = 1
        for environment in environments:
            env_id = "".join(["env", str(env_count)])
            self.pdsdomain = environment
            if environments[0] == environments[1] and env_count > 1:
                self.get_all_product_ids(dev=True)
            else:
                self.get_all_product_ids()
            if environment == environments[0]:
                env1_total_product_count = len(self.all_product_ids)
            else:
                env2_total_product_count = len(self.all_product_ids)
            get_product_id = self.product_id_generator()

            while True:
                try:
                    product_id = str(next(get_product_id))
                    if env_id not in all_products:
                        all_products[env_id] = {product_id: None}
                    else:
                        all_products[env_id].update({product_id: None})
                except StopIteration as e:
                    self.all_product_ids = []
                    break
            if env_count == len(environments):
                break
            else:
                env_count += 1

        env_count = 1
        for environment in environments:
            env_id = "".join(["env", str(env_count)])
            # env_id = "".join(["env", str(environments.index(environment) + 1)])
            for prod_id in all_products[env_id]:
                prod_url = "https://pds-" + environment + ".trade.tt/api/1/products/" + prod_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                all_products[env_id][prod_id] = product_definition
            if env_count == len(environments):
                break
            else:
                env_count += 1

        product_ids_env1 = all_products['env1'].keys()
        product_ids_env2 = all_products['env2'].keys()
        product_list_env1_products = []
        product_list_env2_products = []
        try:
            for product_list_env1_item in all_products['env1']:
                product_list_env1_products.append(' '.join([all_products['env1'][product_list_env1_item]['Symbol'], all_products['env1'][product_list_env1_item]['TypeId']]))
            for product_list_env2_item in all_products['env2']:
                product_list_env2_products.append(' '.join([all_products['env2'][product_list_env2_item]['Symbol'], all_products['env2'][product_list_env2_item]['TypeId']]))
        except TypeError:
            print("env1:", product_list_env1_item)
            # print("https://pds-" + environments[0] + ".trade.tt/api/1/products/" + product_list_env1_item + "?slim=false")
            # print("env2:", product_list_env2_item, ":", all_products['env2'][product_list_env2_item])
            # print("https://pds-" + environments[1] + ".trade.tt/api/1/products/" + product_list_env2_item + "?slim=false")

        print("Comparing {} {} to {} {}".format(environments[0], self.market_stats[0]["market"],
                                                environments[1], self.market_stats[1]["market"]))
        matched_products = []
        for product_id_env1 in product_ids_env1:
            product_dict_env1 = all_products['env1'][product_id_env1]
            symbol_env1 = product_dict_env1['Symbol']
            prod_type_env1 = product_dict_env1['TypeId']

            # Determine whether the products from the 2 diff envs are the same
            for product_id_env2 in product_ids_env2:
                product_pass = True
                product_dict_env2 = all_products['env2'][product_id_env2]
                # try:
                #     if symbol_env1 not in product_dict_env2.values():
                #         print('Symbol {} is missing from {}:'.format(symbol_env1, environments[1]))
                #         print("https://pds-" + environments[0] + ".trade.tt/api/1/products?productIds=" + product_id_env1 + "&slim=false")
                #         continue
                # except AttributeError:
                #     print("AttributeError\n\n" + product_dict_env2)
                symbol_env2 = product_dict_env2['Symbol']
                prod_type_env2 = product_dict_env2["TypeId"]
                if (symbol_env2, prod_type_env2) not in matched_products:
                    if symbol_env2 == symbol_env1 and prod_type_env1 == prod_type_env2:
                        print("-"*30, "\n", symbol_env1, prod_type_env1, ":", symbol_env2, prod_type_env2)

                        tested_product_count += 1
                        tested_instrument_count_per_product = tested_instrument_count

                        product_family_id_mapping.append({'env1': str(product_dict_env1['FamilyId']), 'env2': str(product_dict_env2['FamilyId'])})
                        product_id_mapping.append({'env1': product_id_env1, 'env2': product_id_env2})
                        matched_products.append((symbol_env1, prod_type_env1))

                        try:
                            product_list_env1_products.remove(" ".join([symbol_env1, prod_type_env1]))
                        except:
                            print([symbol_env1, prod_type_env1])
                        try:
                            product_list_env2_products.remove(" ".join([symbol_env2, prod_type_env2]))
                        except:
                            print([symbol_env2, prod_type_env2])


                        # Product Comparison
                        mandatory_item_list = ['Name', 'MICCode', 'PriceTopic', 'Symbol']
                        if "|" in symbol_env1:
                            mandatory_item_list.append('IsInterProduct')

                        for mandatory_item in mandatory_item_list:
                            if mandatory_item not in product_dict_env2:
                                print("ERROR! Product {} is missing {}.".format(symbol_env2, mandatory_item))

                        for skip_item in ('FamilyId', 'Id', 'UpdateTS', 'IsTradeAtSettlementProduct',
                                          'RequireUnderlying', 'IsDeleted', 'InsertTS', 'PTDisplayOrder',
                                          'VersionId', 'StateAttrib', 'LockMask0', 'MarketId', 'ModRevision',
                                          'MarketTypeId', 'PriceTopic', 'ExChannelId', 'SecExchId',
                                          'BloombergCode', 'BloombergExchangeCode', 'altSymbols',
                                          'PriceDisplayTypeId'):
                            if skip_item in product_dict_env2:
                                product_dict_env2.pop(skip_item)
                            if skip_item in product_dict_env1:
                                product_dict_env1.pop(skip_item)

                        for env1_k, env1_v in product_dict_env1.iteritems():
                            if env1_k not in product_dict_env2:
                                product_dict_env2[env1_k] = None

                        for env2_k, env2_v in product_dict_env2.iteritems():
                            if env2_k not in product_dict_env1:
                                product_dict_env1[env2_k] = None

                        for env1_k, env1_v in product_dict_env1.iteritems():
                            # if env1_k == 'MICCode':
                            #     print("MIC CODE {}: {}".format(symbol_env2, product_dict_env1[env1_k]))
                            if env1_k == 'Symbol':
                                env2_value = product_dict_env2[env1_k]
                                env1_value = product_dict_env1[env1_k]
                            else:
                                env2_value = product_dict_env2[env1_k]
                                env1_value = product_dict_env1[env1_k]
                            if env2_value != env1_value:
                                product_pass = False
                                print("Error: Product {} value mismatch: {} != {}".format(env1_k,
                                                                                          product_dict_env1[env1_k],
                                                                                          product_dict_env2[env1_k]))
                        if not product_pass:
                            print("https://pds-" + environments[1] + ".trade.tt/api/1/products?productIds=" + product_id_env2 + "&slim=false")

                        # Instrument Comparison
                        instrument_counter = 0
                        instrument_url_env1 = "https://pds-" + environments[0] + ".trade.tt/api/1/instruments?productIds=" + product_id_env1
                        instrument_list_env1 = self.parse_pds_output(instrument_url_env1)
                        instrument_url_env2 = "https://pds-" + environments[1] + ".trade.tt/api/1/instruments?productIds=" + product_id_env2
                        instrument_list_env2 = self.parse_pds_output(instrument_url_env2)
                        instrument_list_env1_aliases = []
                        instrument_list_env2_aliases = []
                        for instrument_list_env1_item in instrument_list_env1:
                            instrument_list_env1_aliases.append(instrument_list_env1_item['a'])
                        for instrument_list_env2_item in instrument_list_env2:
                            instrument_list_env2_aliases.append(instrument_list_env2_item['a'])
                        for instrument_env1 in instrument_list_env1:
                            # limit instrument comparisons to just a couple of options (there are too many)
                            # break is in the instrument comparison block
                            if instrument_counter >= 2:
                                break
                            instrument_pass = True
                            instr_id_env1 = instrument_env1["i"]
                            instrument_data_env1 = "https://pds-" + environments[0] + ".trade.tt/api/1/instruments?instrumentIds=" + str(instr_id_env1) + "&slim=false"
                            instrument_def_env1 = self.parse_pds_output(instrument_data_env1)[0]
                            instrument_dict_env1 = self.translate_instrument_data(instrument_def_env1)
                            alias_env1 = instrument_dict_env1['Alias']

                            for instrument_env2 in instrument_list_env2:
                                instr_id_env2 = instrument_env2["i"]
                                instrument_data_env2 = "https://pds-" + environments[1] + ".trade.tt/api/1/instruments?instrumentIds=" + str(instr_id_env2) + "&slim=false"
                                instrument_def_env2 = self.parse_pds_output(instrument_data_env2)[0]
                                instrument_dict_env2 = self.translate_instrument_data(instrument_def_env2)
                                alias_env2 = instrument_dict_env2['Alias']

                                if alias_env2 not in instrument_list_env2_aliases:
                                    continue

                                # set alias_prod_chr
                                if "Inter-Product" in alias_env2:
                                    if "Inter-Product" in alias_env1:
                                        alias_prod_chr = "|".join((alias_env1.split(' - ')[1], alias_env1.split(' - ')[0]))
                                else:
                                    alias_prod_chr = alias_env1.split(' ')[0]

                                # define maturity
                                if 'legs' in instrument_def_env2 and 'legs' in instrument_def_env1:
                                    maturity_env2, maturity_env1 = [], []
                                    for combo_leg_env2 in instrument_def_env2['legs']:
                                        if 'e' in combo_leg_env2:
                                            maturity_env2.append(combo_leg_env2['e'])
                                        else:
                                            maturity_env2.append('None')
                                    for combo_leg_env1 in instrument_def_env1['legs']:
                                        if 'e' in combo_leg_env1:
                                            maturity_env1.append(combo_leg_env1['e'])
                                        else:
                                            maturity_env1.append('None')
                                else:
                                    maturity_env2 = instrument_dict_env2['MaturityDate']
                                    maturity_env1 = instrument_dict_env1['MaturityDate']

                                # set match_alias values
                                if "Inter-Product" in alias_env2:
                                    interprod_spr_leglist_env2 = alias_env2.replace(' Inter-Product', '').split(' - ')
                                    interprod_spr_leglist_env1 = alias_env1.replace(' Inter-Product', '').split(' - ')
                                    match_alias_env2 = (interprod_spr_leglist_env2[0], interprod_spr_leglist_env2[1])
                                    match_alias_env1 = (" ".join([interprod_spr_leglist_env1[0].split(' ')[0], interprod_spr_leglist_env1[0].split(' ')[1]]),
                                                       " ".join([interprod_spr_leglist_env1[1].split(' ')[0], interprod_spr_leglist_env1[1].split(' ')[1]]))
                                elif "W" in alias_env2.split(' ')[1]:
                                    match_alias_env2 = (alias_env2.split(' ')[0], alias_env2.split(' ')[1:])
                                    match_alias_env1 = (alias_prod_chr, alias_env1.split(' ')[1:])
                                elif prod_type_env1 != 'OPT' and 'JGBL' in alias_env1:
                                    match_alias_env2 = (alias_env2.split(' ')[0], alias_env2.split(' ')[1], str(maturity_env2))
                                    match_alias_env1 = (alias_prod_chr, alias_env1.split(' ')[1], str(maturity_env1))
                                elif prod_type_env1 != 'OPT' and any(prod_name in alias_env1 for prod_name in ('CRUD', 'TEBL', 'TEPL', 'TWBL', 'TWPL', 'CGAS', 'CKER', 'GASO', 'GSOL', 'KERO', 'OTGCN', 'OTSR2', 'NKDIV')):
                                    match_alias_env2 = (alias_env2.split(' ')[0], str(maturity_env2))
                                    match_alias_env1 = (alias_prod_chr, str(maturity_env1))
                                else:
                                    match_alias_env2 = [alias_env2.split(' ')[0], alias_env2.split(' ')[1], instrument_dict_env2['Strike']]
                                    match_alias_env1 = [alias_prod_chr, alias_env1.split(' ')[1], instrument_dict_env1['Strike']]
                                    if self.market not in ('SGX_GIFT', 'TFEX', 'TFEX_DEV'):
                                        match_alias_env2.append(instrument_dict_env2['SecurityId'].split('_')[0])
                                        match_alias_env1.append(instrument_dict_env1['SecurityId'].split('_')[0])

                                # Determine whether the instruments from the 2 diff envs are the same
                                if (match_alias_env2 == match_alias_env1):
                                    print("|", " | ".join([alias_env1, alias_env2]), "|")
                                    if prod_type_env1 != 'OPT':
                                        instrument_id_mapping.append(",".join(
                                            ["env1", alias_env1, instrument_dict_env1['SecurityId'], str(instr_id_env1),
                                             "env2", alias_env2, instrument_dict_env2['SecurityId'], str(instr_id_env2)]
                                        ))
                                    instrument_list_env1_aliases.remove(alias_env1)
                                    instrument_list_env2_aliases.remove(alias_env2)

                                    tested_instrument_count += 1

                                    for mandatory_item in ('Name', 'PriceTopic', 'SeriesKey', 'Symbol', 'UniName',
                                                           'RICCode', 'BloombergCode'):
                                        if mandatory_item not in instrument_dict_env2:
                                            print("ERROR! Instrument {} is missing {}.".format(alias_env2, mandatory_item))

                                    skip_instr_keys =['Name', 'MarketId', 'PriceTopic', 'ProductId', 'AliasType',
                                                      'Id', 'UserDefined', 'SeriesKey', 'VersionId',
                                                      'ProductFamilyId', 'ProductCurrencyType', 'ProductSymbol',
                                                      'UpdateTS', 'ModRevision', 'ProductVersionId', 'InsertTS',
                                                      'TradesInFlow', 'IsShared', 'IsNotTradable', 'IsEphemeral',
                                                      'UserId', 'PTDisplayOrder', 'UniName', 'IsDaily',
                                                      'StateAttrib', 'IsDeleted', 'SupportsImplieds', 'LegListId',
                                                      'Tenor', 'ExChannelId', 'PriceDisplayTypeId', 'tick_value_str',
                                                      'UpdateSource', 'CTDisplayOrder']
                                    if all(env_type in str(environments) for env_type in ['cert', 'live']):
                                        skip_instr_keys.extend(['RICCode', 'OpenFIGICode', 'BloombergCode',
                                                                'BloombergExchangeCode', 'MetaData', 'point_value_str'])
                                    if self.market == 'SGX_GIFT':
                                        skip_instr_keys.append('SecurityId')

                                    for skip_item in skip_instr_keys:
                                        if skip_item in instrument_dict_env2:
                                            instrument_dict_env2.pop(skip_item)
                                        if skip_item in instrument_dict_env1:
                                            instrument_dict_env1.pop(skip_item)

                                    # limit instrument comparisons to just a couple of options (there are too many)
                                    if instrument_env1["pt"] == 51:
                                        instrument_counter += 1

                                    # begin instrument field comparisons
                                    for env1_k, env1_v in instrument_dict_env1.iteritems():
                                        if env1_k not in instrument_dict_env2:
                                            instrument_dict_env2[env1_k] = None

                                    for env2_k, env2_v in instrument_dict_env2.iteritems():
                                        if env2_k not in instrument_dict_env1:
                                            instrument_dict_env1[env2_k] = None

                                    for env1_k, env1_v in instrument_dict_env1.iteritems():
                                        if env1_k == 'Alias':
                                            env2_value = ",".join(instrument_dict_env2[env1_k].split(' ')[1:])
                                            env1_value = ",".join(instrument_dict_env1[env1_k].split(' ')[1:])
                                        elif (env1_k == 'ExchangeTicker' or env1_k == 'SecurityId') and instrument_dict_env2[env1_k] is not None:
                                            if prod_type_env2 == "MLEG":
                                                try:
                                                    if len(list(instrument_dict_env2[env1_k].split("/")[0].split("_")[-1])) + len(list(instrument_dict_env1[env1_k].split("/")[0].split("_")[-1])) < 12:
                                                        env2_value = "/".join(("".join(list(instrument_dict_env2[env1_k].split("/")[0].split("_")[-1])[:4]),
                                                                              "".join(list(instrument_dict_env2[env1_k].split("/")[1].split("_")[-1])[:4])))
                                                    else:
                                                        #     env2_value = "/".join((instrument_dict_env2[env1_k].split("/")[0].split("_")[-1],
                                                        #                           instrument_dict_env2[env1_k].split("/")[1].split("_")[-1]))
                                                        # env1_value = "/".join((instrument_dict_env1[env1_k].split("/")[0].split("_")[-1],
                                                        #                       instrument_dict_env1[env1_k].split("/")[1].split("_")[-1]))
                                                        # env1_value = instrument_dict_env1[env1_k].split('_')[-1]
                                                        if self.market == "TFX":
                                                            env1_value = instrument_dict_env1[env1_k]
                                                            env2_value = instrument_dict_env2[env1_k]
                                                        elif "TFEX" not in self.market:
                                                            env2_value = "/".join((instrument_dict_env2[env1_k].split("/")[0].split("_")[-1],
                                                                                  instrument_dict_env2[env1_k].split("/")[1].split("_")[-1]))
                                                        else:
                                                            env2_value = "".join(list(instrument_dict_env2[env1_k])[-6:])
                                                    if "TFEX" not in self.market and self.market != "TFX":
                                                        env1_value = "/".join((instrument_dict_env1[env1_k].split("/")[0].split("_")[-1],
                                                                               instrument_dict_env1[env1_k].split("/")[1].split("_")[-1]))
                                                    else:
                                                        if env1_value is None:
                                                            env1_value = "".join(list(instrument_dict_env1[env1_k])[-6:])
                                                            # env1_value = instrument_dict_env1[env1_k].split('_')[-1]
                                                except (AttributeError, IndexError):
                                                    print('instrument_dict_env2:', instrument_dict_env2)
                                                    print('env1_k:', env1_k)
                                            else:
                                                env2_value = list(instrument_dict_env2[env1_k].split('_')[-1])[:3] if instrument_dict_env2[env1_k] is not None else "None"
                                                env1_value = list(instrument_dict_env1[env1_k].split('_')[-1])[:3] if instrument_dict_env1[env1_k] is not None else "None"
                                        elif env1_k == 'Symbol':
                                            if instrument_dict_env1[env1_k] is not None:
                                                env2_value = instrument_dict_env2[env1_k]
                                                env1_value = instrument_dict_env1[env1_k]
                                        elif env1_k == 'cdd':
                                            cdd_yyyy_mm = "".join(list(instrument_dict_env2[env1_k])[:6])\
                                                if instrument_dict_env2[env1_k] is not None else None
                                            alias_term = alias_env2.split(" ")[1]
                                            alias_term = alias_term.split("-")[0] if "-" in alias_term else alias_term
                                            alias_term_dict = get_term_values(alias_term)
                                            alias_term_yyyy_mm = "".join(["20", str(alias_term_dict['year']), str(alias_term_dict['month'])])
                                            if cdd_yyyy_mm != alias_term_yyyy_mm and "Inter-Product" not in alias_env1:
                                                incorrect_cdds.append([alias_env2,
                                                                       instrument_dict_env2[env1_k],
                                                                       instrument_dict_env2['MaturityDate'],
                                                                       instrument_dict_env2['ExpiryDate'],
                                                                       instrument_data_env2])
                                        else:
                                            env2_value = instrument_dict_env2[env1_k]
                                            env1_value = instrument_dict_env1[env1_k]
                                        if env2_value != env1_value:
                                            instrument_pass = False
                                            print("Error: Instrument {} value mismatch: {} != {}".format(env1_k,
                                                                                                         instrument_dict_env1[env1_k],
                                                                                                         instrument_dict_env2[env1_k]))

                                    if "MetaData" in instrument_dict_env2 and instrument_dict_env2["MetaData"] is not None:
                                        # Verify tick_value_str
                                        if "tick_value_str" in instrument_dict_env2["MetaData"]:
                                            tick_value_str_dict = ast.literal_eval(instrument_dict_env2["MetaData"])
                                            tick_value_str = tick_value_str_dict["tick_value_str"]
                                            if tick_value_str != str(int(instrument_dict_env2["TickValue"])):
                                                incorrect_tick_value_strs.append([alias_env2,
                                                                                  tick_value_str,
                                                                                  str(int(instrument_dict_env2["TickValue"])),
                                                                                  instrument_data_env2])

                                    if not instrument_pass:
                                        print(instrument_data_env2)

                                    break

                        total_instrument_count += len(instrument_url_env1)

            if tested_instrument_count_per_product == tested_instrument_count:
                print("\nWARNING! No matching {} instruments were found!".format(prod_type_env1))

        # for matched_product in matched_products:
        #     if matched_product[0] in jpx_product_map:
        #         jpx_product_map.pop(matched_product[0])
        if len(instrument_list_env1_aliases) + len(instrument_list_env2_aliases) + len(product_list_env1_products) + len(incorrect_cdds) + len(incorrect_tick_value_strs) > 0:
            if len(product_list_env1_products) > 0:
                print("WARNING! The following products were not matched!")
                for product_list_env1_products_item in product_list_env1_products:
                    print(product_list_env1_products_item)
            if len(instrument_list_env1_aliases) > 0:
                print("WARNING! The following {} {} instruments were not matched!".format(
                    environments[0], self.market_stats[0]["market"]))
                for instrument_list_env1_alias in instrument_list_env1_aliases:
                    print(instrument_list_env1_alias)
            if len(instrument_list_env2_aliases) > 0:
                print("WARNING! The following {} {} instruments were not matched!".format(
                    environments[1], self.market_stats[1]["market"]))
                for instrument_list_env2_alias in instrument_list_env2_aliases:
                    print(instrument_list_env2_alias)
            if len(incorrect_cdds) > 0:
                print("WARNING! {} instruments have incorrect CDD!".format(len(incorrect_cdds)))
                for incorrect_cdd in incorrect_cdds:
                    print(incorrect_cdd)
            if len(incorrect_tick_value_strs) > 0:
                print("WARNING! {} instruments have incorrect Tick Value String!".format(len(incorrect_tick_value_strs)))
                for incorrect_tick_value_str in incorrect_tick_value_strs:
                    print(incorrect_tick_value_str)
        else:
            print("\nTest Complete!")

        if env2_total_product_count != env1_total_product_count and environments[0] != environments[1]:
            print("WARNING! {} contains {} products while {} contains {} products.".format(
                environments[0], str(env1_total_product_count), environments[1], str(env2_total_product_count)))

        print("{} {} contains {} Products and {} Instruments".format(environments[0], self.market_stats[0]["market"],
                                                                     str(self.market_stats[0]["product_count"]),
                                                                     str(total_instrument_count)))
        print("{} {} contains {} Products and {} Instruments".format(environments[1], self.market_stats[1]["market"],
                                                                     str(self.market_stats[1]["product_count"]),
                                                                     str(total_instrument_count)))

        print("Tested {} Products and {} Instruments".format(str(tested_product_count),
                                                             str(tested_instrument_count)))

        ######################
        # parse output to show product-level overview of PointValue errors
        # grep -B 6 PointValue /Users/cmaurer/pre-go-live_pds_test.txt | grep "|" | awk -F '|' '{print $3}' | awk '{print $1 " " $3}' | sed 's/$/Future/g;s/CalendarFuture/Spread/g' | uniq

    def create_market_migration_instrument_map(self):
        # Verify that each instrument's Alias is consistent across two environments

        # ndaqeu_to_nasdaqned_futures.csv
        # product_map = {"8TRA": "F8TRA", "AAK": "FAAK", "ABB": "FABB", "AKERBP": "FAKERB", "AKSO": "FAKSO", "ALFA": "FALFA", "ASSAB": "FASSAB", "ATCOA": "FATCOA", "AXFO": "FAXFO", "AZN": "FAZN", "BAKKA": "FBAKKA", "BALDB": "FBALDB", "BETSB": "FBETSB", "BILL": "FBILL", "BOLI": "FBOLI", "CARLB": "FCARLB", "CAST": "FCAST", "CHR": "FCHR", "COLOB": "FCOLOB", "DANSKE": "FDANSK", "DNB": "FDNBN", "DNO": "FDNO", "DNORD": "FDNORD", "DOM": "FDOM", "DSV": "FDSV", "EKTAB": "FEKTAB", "ELUXB": "FELUXB", "EMBRAC": "FEMBRA", "EPIA": "FEPIA", "EQNR": "FEQNR", "EQT": "FEQT", "ERICB": "FERICB", "ESSITB": "FESSIT", "EVO": "FEVO", "FABG": "FFABG", "FINGB": "FFINGB", "FLS": "FFLS", "FRO": "FFRO", "GEN": "FGEN", "GETIB": "FGETIB", "GJF": "FGJFN", "GN": "FGN", "HEXB": "FHEXB", "HMB": "FHMB", "HOLMB": "FHOLMB", "HPOL": "FHPOL", "HUSQB": "FHUSQB", "ICA": "FICA", "IJ": "FIJ", "INDUC": "FINDUC", "INVEB": "FINVEB", "ISS": "FISS", "JM": "FJM", "JYSK": "FJYSK", "KINB": "FKINB", "KIND": "FKIND", "LUMI": "FLUMI", "LUN": "FLUN", "LUPE": "FLUPE", "MAERSK": "FMAERS", "MOWI": "FMOWI", "MTGB": "FMTGB", "NAS": "FNAS", "NCC": "FNCC", "NDASE": "FNDASE", "NHY": "FNHYN", "NIBE": "FNIBE", "NOD": "FNOD", "NOKI": "FNOKIA", "NOVOB": "FNOVOB", "NZYMB": "FNZYMB", "OMXC25": "FXC25", "OMXDIV": "FXDIV", "OMXESG": "FXESG", "OMXO20": "FXO20", "OMXS30": "FXS30", "OMXSB": "FMXSB", "ORK": "FORKN", "ORSTED": "FORSTE", "PCELL": "FPCELL", "PGS": "FPGSN", "PNDORA": "FPNDOR", "REC": "FRECN", "S30MIN": "F0MIN", "SAAB": "FSAAB", "SAND": "FSAND", "SAS": "FSAS", "SCAB": "FSCAB", "SCHA": "FSCHA", "SEBA": "FSEBA", "SECUB": "FSECUB", "SHBA": "FSHBA", "SKAB": "FSKAB", "SKFB": "FSKFB", "SOBI": "FSOBI", "SSABA": "FSSABA", "STB": "FSTBN", "STER": "FSTER", "SUBC": "FSUBCN", "SWEDA": "FSWEDA", "SWMA": "FSWMA", "SYDB": "FSYDB", "TEL": "FTELN", "TEL2B": "FTEL2B", "TGS": "FTGS", "TIGO": "FTIGO", "TLSN": "FTLSN", "TRELB": "FTRELB", "TRYG": "FTRYG", "VINX30": "FNX30", "VOLVB": "FVOLVB", "VWS": "FVWS", "WDH": "FWDH", "XXL": "FXXL", "YAR": "FYARN"}
        # ndaqeu_to_nasdaqned_options.csv
        # product_map = {"8TRA": "O8TRA", "AAK": "OAAK", "ABB": "OABB", "ALFA": "OALFA", "ASSAB": "OASSAB", "ATCOA": "OATCOA", "AXFO": "OAXFO", "AZN": "OAZN", "BALDB": "OBALDB", "BETSB": "OBETSB", "BILL": "OBILL", "BOLI": "OBOLI", "CARLB": "OCARLB", "CAST": "OCAST", "CHR": "OCHR", "COLOB": "OCOLOB", "DANSKE": "ODANSK", "DNORD": "ODNORD", "DOM": "ODOM", "DSV": "ODSV", "EKTAB": "OEKTAB", "ELUXB": "OELUXB", "EMBRAC": "OEMBRA", "EPIA": "OEPIA", "EQNR": "OEQNR", "EQT": "OEQT", "ERICB": "OERICB", "ESSITB": "OESSIT", "EVO": "OEVO", "FABG": "OFABG", "FINGB": "OFINGB", "FLS": "OFLS", "GEN": "OGEN", "GETIB": "OGETIB", "GN": "OGN", "HEXB": "OHEXB", "HMB": "OHMB", "HOLMB": "OHOLMB", "HPOL": "OHPOL", "HUH1V": "OHUH1V", "HUSQB": "OHUSQB", "ICA": "OICA", "IJ": "OIJ", "INDUC": "OINDUC", "INVEB": "OINVEB", "ISS": "OISS", "JM": "OJM", "JYSK": "OJYSK", "KINB": "OKINB", "KIND": "OKIND", "KRA1V": "OKRA1V", "LUMI": "OLUMI", "LUN": "OLUN", "LUPE": "OLUPE", "MAERSK": "OMAERS", "METSB": "OMETSB", "MOCORP": "OMOCOR", "MTGB": "OMTGB", "NCC": "ONCC", "NDASE": "ONDASE", "NELES": "ONELES", "NHY": "ONHYN", "NIBE": "ONIBE", "NOKI": "ONOKIA", "NOKIA": "ONOKIA", "NOVOB": "ONOVOB", "NRE1V": "ONRE1V", "NZYMB": "ONZYMB", "OMXC25": "OXC25", "OMXO20": "OXO20", "OMXS30": "OXS30", "ORSTED": "OORSTE", "OUT1V": "OOUT1V", "PCELL": "OPCELL", "PNDORA": "OPNDOR", "SAAB": "OSAAB", "SAND": "OSAND", "SAS": "OSAS", "SCAB": "OSCAB", "SEBA": "OSEBA", "SECUB": "OSECUB", "SHBA": "OSHBA", "SKAB": "OSKAB", "SKFB": "OSKFB", "SOBI": "OSOBI", "SSABA": "OSSABA", "STER": "OSTER", "SWEDA": "OSWEDA", "SWMA": "OSWMA", "SYDB": "OSYDB", "TEL2B": "OTEL2B", "TIGO": "OTIGO", "TLSN": "OTLSN", "TRELB": "OTRELB", "TRYG": "OTRYG", "VOLVB": "OVOLVB", "VWS": "OVWS", "WDH": "OWDH", "WRT1V": "OWRT1V", "XACT": "OXACT", "YTY1V": "OYTY1V"}
        # ndaqeu_to_nasdaqned_others.csv
        # product_map = {"8TRA_C": "28TRA", "8TRA_F": "W8TRA", "AAK_C": "2AAK", "AAK_F": "WAAK", "ABB_C": "2ABB", "ABB_F": "WABB", "AKERBP_C": "2AKERB", "AKERBP_F": "WAKERB", "AKSO_C": "2AKSO", "AKSO_F": "WAKSO", "ALFA_C": "2ALFA", "ALFA_F": "WALFA", "ASSAB_C": "2ASSAB", "ASSAB_F": "WASSAB", "ATCOA_C": "2ATCOA", "ATCOA_F": "WATCOA", "AXFO_C": "2AXFO", "AXFO_F": "WAXFO", "AZN_C": "2AZN", "AZN_F": "WAZN", "BAKKA_C": "2BAKKA", "BAKKA_F": "WBAKKA", "BALDB_C": "2BALDB", "BALDB_F": "WBALDB", "BETSB_C": "2BETSB", "BETSB_F": "WBETSB", "BILL_C": "2BILL", "BILL_F": "WBILL", "BOLI_C": "2BOLI", "BOLI_F": "WBOLI", "CARLB_C": "2CARLB", "CAST_C": "2CAST", "CAST_F": "WCAST", "CHR_C": "2CHR", "COLOB_C": "2COLOB", "DANSKE_C": "2DANSK", "DNB_C": "2DNBN", "DNB_F": "WDNBN", "DNORD_C": "2DNORD", "DNO_C": "2DNO", "DNO_F": "WDNO", "DOM_C": "2DOM", "DOM_F": "WDOM", "DSV_C": "2DSV", "EKTAB_C": "2EKTAB", "EKTAB_F": "WEKTAB", "ELI1V_F": "WELI1V", "ELUXB_C": "2ELUXB", "ELUXB_F": "WELUXB", "EMBRAC_C": "2EMBRA", "EMBRAC_F": "WEMBRA", "EPIA_C": "2EPIA", "EPIA_F": "WEPIA", "EQNR_C": "2EQNR", "EQNR_F": "WEQNR", "EQT_C": "2EQT", "EQT_F": "WEQT", "ERICB_C": "2ERICB", "ERICB_F": "WERICB", "ESSITB_C": "2ESSIT", "ESSITB_F": "WESSIT", "EVO_C": "2EVO", "EVO_F": "WEVO", "FABG_C": "2FABG", "FABG_F": "WFABG", "FINGB_C": "2FINGB", "FINGB_F": "WFINGB", "FLS_C": "2FLS", "FRO_C": "2FRO", "FRO_F": "WFRO", "FUM1V_F": "WFUM1V", "GEN_C": "2GEN", "GETIB_C": "2GETIB", "GETIB_F": "WGETIB", "GJF_C": "2GJFN", "GJF_F": "WGJFN", "GN_C": "2GN", "HEXB_C": "2HEXB", "HEXB_F": "WHEXB", "HMB_C": "2HMB", "HMB_F": "WHMB", "HOLMB_C": "2HOLMB", "HOLMB_F": "WHOLMB", "HPOL_C": "2HPOL", "HPOL_F": "WHPOL", "HUH1V_F": "WHUH1V", "HUSQB_C": "2HUSQB", "HUSQB_F": "WHUSQB", "ICA_C": "2ICA", "ICA_F": "WICA", "IJ_C": "2IJ", "IJ_F": "WIJ", "INDUC_C": "2INDUC", "INDUC_F": "WINDUC", "INVEB_C": "2INVEB", "INVEB_F": "WINVEB", "ISS_C": "2ISS", "JM_C": "2JM", "JM_F": "WJM", "JYSK_C": "2JYSK", "KINB_C": "2KINB", "KINB_F": "WKINB", "KIND_C": "2KIND", "KIND_F": "WKIND", "KNEBV_F": "WKNEBV", "KRA1V_F": "WKRA1V", "LUMI_C": "2LUMI", "LUMI_F": "WLUMI", "LUN_C": "2LUN", "LUPE_C": "2LUPE", "LUPE_F": "WLUPE", "MAERSK_C": "2MAERS", "METSB_F": "WMETSB", "MOCORP_F": "WMOCOR", "MOWI_C": "2MOWI", "MOWI_F": "WMOWI", "MTGB_C": "2MTGB", "MTGB_F": "WMTGB", "NAS_C": "2NAS", "NAS_F": "WNAS", "NCC_C": "2NCC", "NCC_F": "WNCC", "NDAFI_F": "WNDAFI", "NDASE_C": "2NDASE", "NDASE_F": "WNDASE", "NELES_F": "WNELES", "NESTE_F": "WNESTE", "NHY_C": "2NHYN", "NHY_F": "WNHYN", "NIBE_C": "2NIBE", "NIBE_F": "WNIBE", "NOD_C": "2NOD", "NOD_F": "WNOD", "NOK1V_F": "WNOK1V", "NOKI_C": "2NOKIA", "NOKI_F": "WNOKIA", "NOVOB_C": "2NOVOB", "NRE1V_F": "WNRE1V", "NZYMB_C": "2NZYMB", "ORK_C": "2ORKN", "ORK_F": "WORKN", "ORSTED_C": "2ORSTE", "OUT1V_F": "WOUT1V", "PCELL_C": "2PCELL", "PCELL_F": "WPCELL", "PGS_C": "2PGSN", "PGS_F": "WPGSN", "PNDORA_C": "2PNDOR", "REC_C": "2RECN", "REC_F": "WRECN", "SAAB_C": "2SAAB", "SAAB_F": "WSAAB", "SAMAS_F": "WSAMAS", "SAND_C": "2SAND", "SAND_F": "WSAND", "SAS_C": "2SAS", "SAS_F": "WSAS", "SCAB_C": "2SCAB", "SCAB_F": "WSCAB", "SCHA_C": "2SCHA", "SCHA_F": "WSCHA", "SEBA_C": "2SEBA", "SEBA_F": "WSEBA", "SECUB_C": "2SECUB", "SECUB_F": "WSECUB", "SHBA_C": "2SHBA", "SHBA_F": "WSHBA", "SKAB_C": "2SKAB", "SKAB_F": "WSKAB", "SKFB_C": "2SKFB", "SKFB_F": "WSKFB", "SOBI_C": "2SOBI", "SOBI_F": "WSOBI", "SSABA_C": "2SSABA", "SSABA_F": "WSSABA", "STB_C": "2STBN", "STB_F": "WSTBN", "STERV_F": "WSTERV", "STER_C": "2STER", "STER_F": "WSTER", "SUBC_C": "2SUBCN", "SUBC_F": "WSUBCN", "SWEDA_C": "2SWEDA", "SWEDA_F": "WSWEDA", "SWMA_C": "2SWMA", "SWMA_F": "WSWMA", "SYDB_C": "2SYDB", "TEL2B_C": "2TEL2B", "TEL2B_F": "WTEL2B", "TEL_C": "2TELN", "TEL_F": "WTELN", "TGS_C": "2TGS", "TGS_F": "WTGS", "TIE1V_F": "WTIE1V", "TIGO_C": "2TIGO", "TIGO_F": "WTIGO", "TLS1V_F": "WTLS1V", "TLSN_C": "2TLSN", "TLSN_F": "WTLSN", "TRELB_C": "2TRELB", "TRELB_F": "WTRELB", "TRYG_C": "2TRYG", "UPM1V_F": "WUPM1V", "VOLVB_C": "2VOLVB", "VOLVB_F": "WVOLVB", "VWS_C": "2VWS", "WDH_C": "2WDH", "WRT1V_F": "WWRT1V", "XXL_C": "2XXL", "XXL_F": "WXXL", "YAR_C": "2YARN", "YAR_F": "WYARN", "YTY1V_F": "WYTY1V"}

        # product_map = {"GASO": "GAS", "KERO": "KRO", "GSOL": "GAO", "CRUD": "DBAI", "CGAS": "CGAS", "CKER": "CKRO",
        #                    "TWBL": "EWB", "TEBL": "EEB", "TWPL": "EWP", "TEPL": "EEP", "BANK": "BANK", "DJIA": "DJIA",
        #                    "FTC50": "FT50", "JGBM": "JBM", "JGBL": "JBL", "JGBLM": "JBLM", "JGBSL": "JBS",
        #                    "JN400": "400", "MOTHE": "MOTH", "NK225": "225", "NK225M": "225M", "NK225W": "225W",
        #                    "NKDIV": "NKDV", "NKVI": "NVI", "OGDCD": "GLDD", "OGOLD": "GLD", "OM-GD": "GLDM",
        #                    "OPALL": "PALD", "OPLAT": "PLT", "OM-PT": "PLTM", "OPTCD": "PLTD", "ORSS3": "RSS3",
        #                    "OSILV": "SILV", "OTGAB": "REDB", "OTGCN": "CORN", "OTGSB": "SOYB", "OTSR2": "TSR2",
        #                    "REIT": "REIT", "RNP": "RNP", "TPX30": "C30", "TAIEX": "TAIX", "TOPIX": "TPX",
        #                    "TOPIXM": "TPXM", "OM-PT|OM-GD": "GLDM|PLTM", "OPTCD|OGDCD": "GLDD|PLTD",
        #                    "OTSR2|ORSS3": "RSS3|TSR2", "CKER|CGAS": "CGAS|CKRO", "CRUD|GASO": "GAS|DBAI",
        #                    "CRUD|GSOL": "GAO|DBAI", "CRUD|KERO": "KRO|DBAI", "GSOL|GASO": "GAS|GAO",
        #                    "GSOL|KERO": "KRO|GAO", "KERO|GASO": "GAS|KRO", "TWBL|TEBL": "EEB|EWB",
        #                    "TWPL|TEPL": "EEP|EWP", "TBGA": None, "TLGA": None, "TBKE": None, "TLKE": None, "TBGO": None,
        #                    "TLGO": None, "T30D": None, "TPDIV": None, "TBGO|GSOL": None, "TLKE|TLGA": None,
        #                    "TLKE|CKER": None, "TLKE|CGAS": None, "TLGO|TLKE": None, "TLGO|TLGA": None,
        #                    "TLGO|CKER": None, "TLGO|CGAS": None, "TLGA|CKER": None, "TLGA|CGAS": None,
        #                    "TBKE|TBGA": None, "TBKE|KERO": None, "TBKE|GSOL": None, "TBKE|GASO": None,
        #                    "TBGA|GASO": None, "TBGA|GSOL": None, "TBGA|KERO": None, "TBGO|GASO": None,
        #                    "TBGO|GSOL": None, "TBGO|KERO": None, "TBGO|TBGA": None, "TBGO|TBKE": None,
        #                    "CRUD|TBGA": None, "CRUD|TBGO": None, "CRUD|TBKE": None, "1306": "1306", "1308": "1308", "1309": "1309", "1320": "1320", "1321": "1321", "1328": "1328", "1330": "1330", "1343": "1343", "1540": "1540", "1591": "1591", "1605": "1605", "1615": "1615", "1671": "1671", "1801": "1801", "1803": "1803", "1808": "1808", "1812": "1812", "1925": "1925", "1928": "1928", "1944": "1944", "1963": "1963", "2002": "2002", "2432": "2432", "2502": "2502", "2503": "2503", "2531": "2531", "2651": "2651", "2768": "2768", "2802": "2802", "2914": "2914", "3249": "3249", "3269": "3269", "3279": "3279", "3382": "3382", "3402": "3402", "3405": "3405", "3407": "3407", "3436": "3436", "3462": "3462", "3632": "3632", "3861": "3861", "3863": "3863", "4005": "4005", "4062": "4062", "4063": "4063", "4183": "4183", "4188": "4188", "4307": "4307", "4324": "4324", "4452": "4452", "4502": "4502", "4503": "4503", "4519": "4519", "4523": "4523", "4543": "4543", "4568": "4568", "4631": "4631", "4661": "4661", "4676": "4676", "4689": "4689", "4704": "4704", "4716": "4716", "4739": "4739", "4901": "4901", "4902": "4902", "4911": "4911", "5020": "5020", "5108": "5108", "5201": "5201", "5202": "5202", "5214": "5214", "5333": "5333", "5401": "5401", "5406": "5406", "5411": "5411", "5631": "5631", "5706": "5706", "5711": "5711", "5713": "5713", "5801": "5801", "5802": "5802", "5803": "5803", "5901": "5901", "5938": "5938", "6178": "6178", "6273": "6273", "6301": "6301", "6302": "6302", "6305": "6305", "6326": "6326", "6367": "6367", "6460": "6460", "6471": "6471", "6479": "6479", "6501": "6501", "6502": "6502", "6503": "6503", "6592": "6592", "6594": "6594", "6674": "6674", "6701": "6701", "6702": "6702", "6703": "6703", "6723": "6723", "6724": "6724", "6752": "6752", "6753": "6753", "6758": "6758", "6762": "6762", "6770": "6770", "6806": "6806", "6857": "6857", "6861": "6861", "6902": "6902", "6952": "6952", "6954": "6954", "6963": "6963", "6971": "6971", "6976": "6976", "6981": "6981", "6988": "6988", "7011": "7011", "7012": "7012", "7013": "7013", "7181": "7181", "7182": "7182", "7201": "7201", "7202": "7202", "7203": "7203", "7259": "7259", "7261": "7261", "7267": "7267", "7269": "7269", "7272": "7272", "7731": "7731", "7733": "7733", "7741": "7741", "7751": "7751", "7752": "7752", "7911": "7911", "7912": "7912", "7974": "7974", "8001": "8001", "8002": "8002", "8031": "8031", "8035": "8035", "8053": "8053", "8058": "8058", "8113": "8113", "8252": "8252", "8253": "8253", "8267": "8267", "8306": "8306", "8308": "8308", "8309": "8309", "8316": "8316", "8411": "8411", "8473": "8473", "8591": "8591", "8601": "8601", "8604": "8604", "8630": "8630", "8725": "8725", "8750": "8750", "8766": "8766", "8795": "8795", "8801": "8801", "8802": "8802", "8830": "8830", "8951": "8951", "8952": "8952", "8953": "8953", "8954": "8954", "8955": "8955", "8957": "8957", "8961": "8961", "8967": "8967", "8972": "8972", "8976": "8976", "8984": "8984", "9005": "9005", "9020": "9020", "9021": "9021", "9022": "9022", "9062": "9062", "9064": "9064", "9101": "9101", "9104": "9104", "9107": "9107", "9142": "9142", "9201": "9201", "9202": "9202", "9301": "9301", "9404": "9404", "9432": "9432", "9433": "9433", "9434": "9434", "9437": "9437", "9501": "9501", "9502": "9502", "9503": "9503", "9504": "9504", "9506": "9506", "9508": "9508", "9531": "9531", "9532": "9532", "9613": "9613", "9735": "9735", "9766": "9766", "9831": "9831", "9983": "9983", "9984": "9984"}

        product_family_id_mapping = []
        product_id_mapping = []
        instrument_id_mapping = []
        incorrect_cdds = []
        incorrect_tick_value_strs = []
        all_products = {}
        all_instruments = []
        instrument_list_mkt1_aliases = []
        instrument_list_mkt2_aliases = []

        markets = ["NDAQ_EU", "NASDAQ_NED"]

        for market in markets:
            self.market = market
            self.get_all_product_ids()
            get_product_id = self.product_id_generator()

            while True:
                try:
                    product_id = str(next(get_product_id))
                    if market not in all_products:
                        all_products[market] = {product_id: None}
                    else:
                        all_products[market].update({product_id: None})
                except StopIteration as e:
                    self.all_product_ids = []
                    break

        for market in markets:
            for prod_id in all_products[market]:
                prod_url = self.base_url + "/api/1/products/" + prod_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                all_products[market][prod_id] = product_definition

        # market1
        src_mkt = markets[0]
        dest_mkt = markets[1]
        product_ids_mkt1 = all_products[src_mkt].keys()
        product_ids_mkt2 = all_products[dest_mkt].keys()
        product_list_mkt1_products = []
        product_list_mkt2_products = []
        try:
            for product_list_mkt1_item in all_products[src_mkt]:
                product_list_mkt1_products.append(' '.join([all_products[src_mkt][product_list_mkt1_item]['Symbol'], all_products[src_mkt][product_list_mkt1_item]['TypeId']]))
            for product_list_mkt2_item in all_products[dest_mkt]:
                product_list_mkt2_products.append(' '.join([all_products[dest_mkt][product_list_mkt2_item]['Symbol'], all_products[dest_mkt][product_list_mkt2_item]['TypeId']]))
        except TypeError:
            print(src_mkt + ":", product_list_mkt1_item)
            # print(self.base_url + "/api/1/products/" + product_list_mkt1_item + "?slim=false")
            # print("mkt2:", product_list_mkt2_item, ":", all_products[dest_mkt][product_list_mkt2_item])
            # print(self.base_url + "/api/1/products/" + product_list_mkt2_item + "?slim=false")

        matched_products = []
        for product_id_mkt1 in product_ids_mkt1:
            product_dict_mkt1 = all_products[src_mkt][product_id_mkt1]
            symbol_mkt1 = product_dict_mkt1['Symbol']
            prod_type_mkt1 = product_dict_mkt1['TypeId']

            for product_id_mkt2 in product_ids_mkt2:
                product_pass = True
                product_dict_mkt2 = all_products[dest_mkt][product_id_mkt2]
                if 'Symbol' not in product_dict_mkt2:
                    print('Symbol is missing from {} {} {}:'.format(self.pdsdomain, product_dict_mkt2['Name'],
                                                                    product_dict_mkt2['TypeId']))
                    print(self.base_url + "/api/1/products?productIds=" + product_id_mkt2 + "&slim=false")
                    continue
                symbol_mkt2 = product_dict_mkt2['Symbol']
                prod_type_mkt2 = product_dict_mkt2["TypeId"]
                if (symbol_mkt2, prod_type_mkt2) not in matched_products:
                    if (symbol_mkt2 == symbol_mkt1 or symbol_mkt2 == product_map[symbol_mkt1]) and prod_type_mkt1 == prod_type_mkt2:
                        print("-"*30, "\n", symbol_mkt1, prod_type_mkt1, ":", symbol_mkt2, prod_type_mkt2)
                        product_family_id_mapping.append({src_mkt: str(product_dict_mkt1['FamilyId']), dest_mkt: str(product_dict_mkt2['FamilyId'])})
                        product_id_mapping.append({src_mkt: product_id_mkt1, dest_mkt: product_id_mkt2})
                        matched_products.append((symbol_mkt1, prod_type_mkt1))

                        try:
                            product_list_mkt1_products.remove(" ".join([symbol_mkt1, prod_type_mkt1]))
                        except:
                            print([symbol_mkt1, prod_type_mkt1])
                        try:
                            product_list_mkt2_products.remove(" ".join([symbol_mkt2, prod_type_mkt2]))
                        except:
                            print([symbol_mkt2, prod_type_mkt2])

                        if prod_type_mkt1 != 'OPT':
                            # Product Comparison
                            mandatory_item_list = ['Name', 'MICCode', 'PriceTopic', 'Symbol']
                            if "|" in symbol_mkt1:
                                mandatory_item_list.append('IsInterProduct')

                            for mandatory_item in mandatory_item_list:
                                if mandatory_item not in product_dict_mkt2:
                                    print("ERROR! Product {} is missing {}.".format(symbol_mkt2, mandatory_item))

                            skip_prod_keys = ['FamilyId', 'Id', 'UpdateTS', 'IsTradeAtSettlementProduct',
                                              'RequireUnderlying', 'IsDeleted', 'InsertTS', 'PTDisplayOrder',
                                              'VersionId', 'StateAttrib', 'LockMask0', 'MarketId', 'ModRevision',
                                              'MarketTypeId', 'PriceTopic', 'ExChannelId', 'SecExchId',
                                              'BloombergCode', 'BloombergExchangeCode', 'altSymbols',
                                              'PriceDisplayTypeId']

                            for skip_item in skip_prod_keys:
                                if skip_item in product_dict_mkt2:
                                    product_dict_mkt2.pop(skip_item)
                                if skip_item in product_dict_mkt1:
                                    product_dict_mkt1.pop(skip_item)

                            for mkt1_k, mkt1_v in product_dict_mkt1.iteritems():
                                if mkt1_k not in product_dict_mkt2:
                                    product_dict_mkt2[mkt1_k] = None

                            for mkt2_k, mkt2_v in product_dict_mkt2.iteritems():
                                if mkt2_k not in product_dict_mkt1:
                                    product_dict_mkt1[mkt2_k] = None

                            for mkt1_k, mkt1_v in product_dict_mkt1.iteritems():
                                # if mkt1_k == 'MICCode':
                                #     print("MIC CODE {}: {}".format(symbol_mkt2, product_dict_mkt1[mkt1_k]))
                                if mkt1_k == 'Symbol':
                                    mkt2_value = product_dict_mkt2[mkt1_k]
                                    mkt1_value = product_dict_mkt1[mkt1_k]
                                else:
                                    mkt2_value = product_dict_mkt2[mkt1_k]
                                    mkt1_value = product_dict_mkt1[mkt1_k]
                                if mkt2_value != mkt1_value:
                                    product_pass = False
                                    print("Error: Product {} value mismatch: {} != {}".format(mkt1_k,
                                                                                              product_dict_mkt1[mkt1_k],
                                                                                              product_dict_mkt2[mkt1_k]))
                            if not product_pass:
                                print(self.base_url + "/api/1/products?productIds=" + product_id_mkt2 + "&slim=false")

                            # Instrument Comparison
                            instrument_url_mkt1 = self.base_url + "/api/1/instruments?productIds=" + product_id_mkt1
                            instrument_list_mkt1 = self.parse_pds_output(instrument_url_mkt1)
                            instrument_url_mkt2 = self.base_url + "/api/1/instruments?productIds=" + product_id_mkt2
                            instrument_list_mkt2 = self.parse_pds_output(instrument_url_mkt2)
                            for instrument_list_mkt1_item in instrument_list_mkt1:
                                instrument_list_mkt1_aliases.append(instrument_list_mkt1_item['a'])
                            for instrument_list_mkt2_item in instrument_list_mkt2:
                                instrument_list_mkt2_aliases.append(instrument_list_mkt2_item['a'])
                            for instrument_mkt1 in instrument_list_mkt1:
                                instrument_pass = True
                                instr_id_mkt1 = instrument_mkt1["i"]
                                instrument_data_mkt1 = self.base_url + "/api/1/instruments?instrumentIds=" + str(instr_id_mkt1) + "&slim=false"
                                instrument_def_mkt1 = self.parse_pds_output(instrument_data_mkt1)[0]
                                instrument_dict_mkt1 = self.translate_instrument_data(instrument_def_mkt1)
                                alias_mkt1 = instrument_dict_mkt1['Alias']

                                for instrument_mkt2 in instrument_list_mkt2:
                                    instr_id_mkt2 = instrument_mkt2["i"]
                                    instrument_data_mkt2 = self.base_url + "/api/1/instruments?instrumentIds=" + str(instr_id_mkt2) + "&slim=false"
                                    instrument_def_mkt2 = self.parse_pds_output(instrument_data_mkt2)[0]
                                    instrument_dict_mkt2 = self.translate_instrument_data(instrument_def_mkt2)
                                    alias_mkt2 = instrument_dict_mkt2['Alias']

                                    # set alias_prod_chr
                                    if "Inter-Product" in alias_mkt2:
                                        if "Inter-Product" in alias_mkt1:
                                            alias_prod_chr = "|".join((alias_mkt1.split(' - ')[1], alias_mkt1.split(' - ')[0]))
                                    else:
                                        alias_prod_chr = alias_mkt1.split(' ')[0] if symbol_mkt2 == symbol_mkt1 else product_map[alias_mkt1.split(' ')[0]]

                                    # define maturity
                                    if 'legs' in instrument_def_mkt2 and 'legs' in instrument_def_mkt1:
                                        maturity_mkt2, maturity_mkt1 = [], []
                                        for combo_leg_mkt2 in instrument_def_mkt2['legs']:
                                            maturity_mkt2.append(combo_leg_mkt2['e'])
                                        for combo_leg_mkt1 in instrument_def_mkt1['legs']:
                                            maturity_mkt1.append(combo_leg_mkt1['e'])
                                    else:
                                        maturity_mkt2 = instrument_dict_mkt2['MaturityDate']
                                        maturity_mkt1 = instrument_dict_mkt1['MaturityDate']

                                    # set match_alias values
                                    if "Inter-Product" in alias_mkt2:
                                        interprod_spr_leglist_mkt2 = alias_mkt2.replace(' Inter-Product', '').split(' - ')
                                        interprod_spr_leglist_mkt1 = alias_mkt1.replace(' Inter-Product', '').split(' - ')
                                        match_alias_mkt2 = (interprod_spr_leglist_mkt2[0], interprod_spr_leglist_mkt2[1])
                                        match_alias_mkt1 = (" ".join([interprod_spr_leglist_mkt1[0].split(' ')[0], interprod_spr_leglist_mkt1[0].split(' ')[1]]),
                                                           " ".join([interprod_spr_leglist_mkt1[1].split(' ')[0], interprod_spr_leglist_mkt1[1].split(' ')[1]]))
                                    elif "W" in alias_mkt2.split(' ')[1]:
                                        match_alias_mkt2 = (alias_mkt2.split(' ')[0], alias_mkt2.split(' ')[1:])
                                        match_alias_mkt1 = (alias_prod_chr, alias_mkt1.split(' ')[1:])
                                    elif prod_type_mkt1 != 'OPT' and 'JGBL' in alias_mkt1:
                                        match_alias_mkt2 = (alias_mkt2.split(' ')[0], alias_mkt2.split(' ')[1], str(maturity_mkt2))
                                        match_alias_mkt1 = (alias_prod_chr, alias_mkt1.split(' ')[1], str(maturity_mkt1))
                                    elif prod_type_mkt1 != 'OPT' and any(prod_name in alias_mkt1 for prod_name in ('CRUD', 'TEBL', 'TEPL', 'TWBL', 'TWPL', 'CGAS', 'CKER', 'GASO', 'GSOL', 'KERO', 'OTGCN', 'OTSR2', 'NKDIV')):
                                        match_alias_mkt2 = (alias_mkt2.split(' ')[0], str(maturity_mkt2))
                                        match_alias_mkt1 = (alias_prod_chr, str(maturity_mkt1))
                                    else:
                                        match_alias_mkt2 = [alias_mkt2.split(' ')[0], alias_mkt2.split(' ')[1], instrument_dict_mkt2['Strike'],  instrument_dict_mkt2['OptionCodeId']]
                                        if "NDAQ_EU" in str(markets) and symbol_mkt1 == "OMXDIV":
                                            match_alias_mkt1 = [alias_prod_chr, (alias_mkt1.split(' ')[1]).replace("Dec", "20"), instrument_dict_mkt1['Strike'],  instrument_dict_mkt1 ['OptionCodeId']]
                                        else:
                                            match_alias_mkt1 = [alias_prod_chr, alias_mkt1.split(' ')[1], instrument_dict_mkt1['Strike'],  instrument_dict_mkt1 ['OptionCodeId']]
                                        if "JPX" in str(markets):
                                            match_alias_mkt2.append(instrument_dict_mkt2['SecurityId'].split('_')[0])
                                            match_alias_mkt1.append(instrument_dict_mkt1['SecurityId'].split('_')[0])
                                    if (match_alias_mkt2 == match_alias_mkt1):
                                        print("|", " | ".join([alias_mkt1, alias_mkt2]), "|")
                                        if prod_type_mkt1 != 'OPT':
                                            instrument_id_mapping.append(
                                                {src_mkt: instr_id_mkt1, dest_mkt: instr_id_mkt2})
                                        instrument_list_mkt1_aliases.remove(alias_mkt1)
                                        all_instruments.append(instrument_list_mkt2_aliases.pop(instrument_list_mkt2_aliases.index(alias_mkt2)))

                                        for mandatory_item in ('Name', 'PriceTopic', 'SeriesKey', 'Symbol', 'UniName',
                                                               'RICCode', 'BloombergCode'):
                                            if mandatory_item not in instrument_dict_mkt2:
                                                print("ERROR! Instrument {} is missing {}.".format(alias_mkt2, mandatory_item))

                                        skip_instr_keys =['Name', 'MarketId', 'PriceTopic', 'ProductId', 'AliasType',
                                                          'Id', 'UserDefined', 'SeriesKey', 'VersionId',
                                                          'ProductFamilyId', 'ProductCurrencyType', 'ProductSymbol',
                                                          'UpdateTS', 'ModRevision', 'ProductVersionId', 'InsertTS',
                                                          'TradesInFlow', 'IsShared', 'IsNotTradable', 'IsEphemeral',
                                                          'UserId', 'PTDisplayOrder', 'UniName', 'IsDaily',
                                                          'StateAttrib', 'IsDeleted', 'SupportsImplieds', 'LegListId',
                                                          'Tenor', 'ExChannelId', 'PriceDisplayTypeId', 'tick_value_str',
                                                          'UpdateSource']
                                        if "NDAQ_EU" in markets or "NASDAQ_NED" in markets:
                                            skip_instr_keys.append('Symbol')
                                        # if all(env_type in str(environments) for env_type in ['cert', 'live']):
                                        #     skip_instr_keys.extend(['RICCode', 'OpenFIGICode', 'BloombergCode',
                                        #                             'BloombergExchangeCode'])
                                        for skip_item in skip_instr_keys:
                                            if skip_item in instrument_dict_mkt2:
                                                instrument_dict_mkt2.pop(skip_item)
                                            if skip_item in instrument_dict_mkt1:
                                                instrument_dict_mkt1.pop(skip_item)

                                        for mkt1_k, mkt1_v in instrument_dict_mkt1.iteritems():
                                            if mkt1_k not in instrument_dict_mkt2:
                                                instrument_dict_mkt2[mkt1_k] = None

                                        for mkt2_k, mkt2_v in instrument_dict_mkt2.iteritems():
                                            if mkt2_k not in instrument_dict_mkt1:
                                                instrument_dict_mkt1[mkt2_k] = None

                                        for mkt1_k, mkt1_v in instrument_dict_mkt1.iteritems():
                                            if mkt1_k == 'Alias':
                                                mkt2_value = ",".join(instrument_dict_mkt2[mkt1_k].split(' ')[1:])
                                                mkt1_value = ",".join(instrument_dict_mkt1[mkt1_k].split(' ')[1:])
                                            elif mkt1_k == 'ExchangeTicker' or mkt1_k == 'SecurityId':
                                                if prod_type_mkt2 == "MLEG" and ("/" in 'ExchangeTicker' or "/" in 'SecurityId'):
                                                    if len(list(instrument_dict_mkt2[mkt1_k].split("/")[0].split("_")[-1])) + len(list(instrument_dict_mkt1[mkt1_k].split("/")[0].split("_")[-1])) < 12:
                                                        mkt2_value = "/".join(("".join(list(instrument_dict_mkt2[mkt1_k].split("/")[0].split("_")[-1])[:4]),
                                                                              "".join(list(instrument_dict_mkt2[mkt1_k].split("/")[1].split("_")[-1])[:4])))
                                                    else:
                                                        mkt2_value = "/".join((instrument_dict_mkt2[mkt1_k].split("/")[0].split("_")[-1],
                                                                              instrument_dict_mkt2[mkt1_k].split("/")[1].split("_")[-1]))
                                                    mkt1_value = "/".join((instrument_dict_mkt1[mkt1_k].split("/")[0].split("_")[-1],
                                                                          instrument_dict_mkt1[mkt1_k].split("/")[1].split("_")[-1]))
                                                    # mkt1_value = instrument_dict_mkt1[mkt1_k].split('_')[-1]
                                                else:
                                                    mkt2_value = list(instrument_dict_mkt2[mkt1_k].split('_')[-1])[:3] if instrument_dict_mkt2[mkt1_k] is not None else "None"
                                                    mkt1_value = list(instrument_dict_mkt1[mkt1_k].split('_')[-1])[:3] if instrument_dict_mkt1[mkt1_k] is not None else "None"
                                            elif mkt1_k == 'Symbol':
                                                if instrument_dict_mkt1[mkt1_k] is not None:
                                                    mkt2_value = instrument_dict_mkt2[mkt1_k]
                                                    mkt1_value = instrument_dict_mkt1[mkt1_k]
                                            elif mkt1_k == 'cdd':
                                                cdd_yyyy_mm = "".join(list(instrument_dict_mkt2[mkt1_k])[:6])\
                                                    if instrument_dict_mkt2[mkt1_k] is not None else None
                                                alias_term = alias_mkt2.split(" ")[1]
                                                alias_term = alias_term.split("-")[0] if "-" in alias_term else alias_term
                                                alias_term_dict = get_term_values(alias_term)
                                                if alias_term_dict['month'] == 00:
                                                    alias_term_yyyy_mm = "".join(["20", str(alias_term_dict['year']), "".join((list(maturity_mkt2)[4:6]))])
                                                else:
                                                    alias_term_yyyy_mm = "".join(["20", str(alias_term_dict['year']), str(alias_term_dict['month'])])
                                                if cdd_yyyy_mm != alias_term_yyyy_mm and "Inter-Product" not in alias_mkt1:
                                                    incorrect_cdds.append([alias_mkt2,
                                                                           instrument_dict_mkt2[mkt1_k],
                                                                           instrument_dict_mkt2['MaturityDate'],
                                                                           instrument_dict_mkt2['ExpiryDate'],
                                                                           instrument_data_mkt2])
                                            else:
                                                mkt2_value = instrument_dict_mkt2[mkt1_k]
                                                mkt1_value = instrument_dict_mkt1[mkt1_k]
                                            if mkt2_value != mkt1_value:
                                                instrument_pass = False
                                                print("Error: Instrument {} value mismatch: {} != {}".format(mkt1_k,
                                                                                                             instrument_dict_mkt1[mkt1_k],
                                                                                                             instrument_dict_mkt2[mkt1_k]))

                                        # Verify tick_value_str
                                        if "tick_value_str" in instrument_dict_mkt2["MetaData"]:
                                            tick_value_str_dict = ast.literal_eval(instrument_dict_mkt2["MetaData"])
                                            tick_value_str = tick_value_str_dict["tick_value_str"]
                                            if tick_value_str != str(int(instrument_dict_mkt2["TickValue"])):
                                                incorrect_tick_value_strs.append([alias_mkt2,
                                                                                  tick_value_str,
                                                                                  str(int(instrument_dict_mkt2["TickValue"])),
                                                                                  instrument_data_mkt2])

                                        if not instrument_pass:
                                            print(instrument_data_mkt2)

                                        break

        for matched_product in matched_products:
            if matched_product[0] in product_map:
                product_map.pop(matched_product[0])
        if len(instrument_list_mkt1_aliases) + len(instrument_list_mkt2_aliases) + len(product_list_mkt1_products) + len(incorrect_cdds) + len(incorrect_tick_value_strs) > 0:
            if len(product_list_mkt1_products) > 0:
                print("WARNING! The following products were not matched!")
                for product_list_mkt1_products_item in product_list_mkt1_products:
                    print(product_list_mkt1_products_item)
            if len(instrument_list_mkt1_aliases) > 0:
                print("WARNING! The following {} instruments were not matched!".format(markets[0]))
                for instrument_list_mkt1_alias in instrument_list_mkt1_aliases:
                    print(instrument_list_mkt1_alias)
            if len(instrument_list_mkt2_aliases) > 0:
                print("WARNING! The following {} instruments were not matched!".format(markets[1]))
                for instrument_list_mkt2_alias in instrument_list_mkt2_aliases:
                    print(instrument_list_mkt2_alias)
            if len(incorrect_cdds) > 0:
                print("WARNING! {} instruments have incorrect CDD!".format(len(incorrect_cdds)))
                for incorrect_cdd in incorrect_cdds:
                    print(incorrect_cdd)
            if len(incorrect_tick_value_strs) > 0:
                print("WARNING! {} instruments have incorrect Tick Value String!".format(len(incorrect_tick_value_strs)))
                for incorrect_tick_value_str in incorrect_tick_value_strs:
                    print(incorrect_tick_value_str)
        else:
            print("Test Complete!")

        print("\nTested {} Products and {} Instruments".format(str(len(all_products[dest_mkt])), str(len(all_instruments))))

        print("\n{} Market Migration Map:".format(self.pdsdomain))
        print("\nproduct_family_id_mapping")
        print(product_family_id_mapping)
        print("\nproduct_id_mapping")
        print(product_id_mapping)
        print("\ninstrument_id_mapping")
        print(instrument_id_mapping)

        ######################
        # parse output to show product-level overview of PointValue errors
        # grep -B 6 PointValue /Users/cmaurer/pre-go-live_pds_test.txt | grep "|" | awk -F '|' '{print $3}' | awk '{print $1 " " $3}' | sed 's/$/Future/g;s/CalendarFuture/Spread/g' | uniq

    def verify_instrument_correctness(self):
        # Verify that each instrument's Alias is consistent across two environments

        all_aliases = {}
        missing_from_1 = []
        missing_from_2 = []
        mismatches = []
        missing_aliases = []
        envs = []
        incorrect_sec_exchange = []

        self.get_all_product_ids()
        self.get_security_exch_ids()
        get_product_id = self.product_id_generator()
        products_with_no_description = []
        products_with_no_assetclass = []

        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                description = product_definition['Name']
                symbol = product_definition['Symbol']
                prod_type = product_definition['TypeId']
                sec_exch = product_definition['SecExchId'] if 'SecExchId' in product_definition else None
                asset_class = product_definition['Asset_Class'] if 'Asset_Class' in product_definition else None
                if description is None:
                    products_with_no_description.append(" ".join([symbol, prod_type]))
                if asset_class is None:
                    products_with_no_assetclass.append(" ".join([symbol, prod_type]))
                instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id
                instrument_list = self.parse_pds_output(instr_list_url)
                if self.market == "OSE":
                    if len(instrument_list) > 0:
                        if symbol.startswith("O"):
                            if sec_exch != 293:
                                incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                        else:
                            if sec_exch != 292:
                                incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                elif self.market == "SGX":
                    if len(instrument_list) > 0:
                        if sec_exch == 39:
                            incorrect_sec_exchange.append((symbol, sec_exch, prod_url))
                for instrument in instrument_list:
                    instrument_definition = self.translate_instrument_data(instrument)
                    alias = None
                    alias = instrument_definition["Alias"]
                    name = instrument_definition["Name"]
                    instr = str(instrument["i"])
                    if alias is None:
                        missing_aliases.append((name,
                                                ''.join([self.base_url, "/api/1/instruments?instrumentIds=", instr])))
            except StopIteration as e:
                break

        if len(missing_aliases) > 0:
            print("\nFAIL! {} missing Aliases detected:".format(len(missing_aliases)))
            for missing_alias in missing_aliases:
                print(missing_alias)

        if len(incorrect_sec_exchange) > 0:
            print("\nFAIL! {} products have Security Exchange set incorrectly:".format(len(incorrect_sec_exchange)))
            for incorrect_sec_exchange_id in incorrect_sec_exchange:
                print(incorrect_sec_exchange_id)

        if len(products_with_no_description) > 0:
            print("\nFAIL! {} products have no Description:".format(len(products_with_no_description)))
            products_with_no_description.sort()
            for p in products_with_no_description:
                print("* {}".format(p))

        if len(products_with_no_assetclass) > 0:
            print("\nFAIL! {} products have no Asset Class:".format(len(products_with_no_assetclass)))
            products_with_no_assetclass.sort()
            for p in products_with_no_assetclass:
                print("* {}".format(p))

        print("\n\nFinished.")

    def find_instruments_with_quality_of_measure(self):
        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        all_markets = [market_ids[m_id]['n'] for m_id in range(len(market_ids))]

        for mkt in all_markets:
            if "_DEV" not in mkt and "_Dev" not in mkt and mkt != 'ASE' and mkt != 'LME':
                self.market = mkt
                found_qom = False

                for product_type in self.product_types:
                    prod_url = self.base_url + "/api/1/products?marketIds=" + self.get_market_id(self.market) + \
                               "&productTypeIds=" + str(product_type) + "&slim=false"
                    products = self.parse_pds_output(prod_url)

                    self.all_products.extend(products)

                    for product in products:
                        product_id = str(product["i"])

                        if found_qom:
                            break
                        # try:
                        instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id + "&slim=false"
                        instrument_list = self.parse_pds_output(instr_list_url)
                        instrument_list = instrument_list[:1]
                        for instrument in instrument_list:
                            instrument_id = str(instrument["i"])
                            url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                            instrument = self.parse_pds_output(url)
                            instrument = instrument[0]
                            instrument_definition = self.translate_instrument_data(instrument)
                            prod_type = self.product_types[instrument_definition['ProductTypeId']]
                            alias = instrument_definition['Alias']
                            qom = instrument_definition['QOfMeasure']
                            if qom is not None:
                                print(mkt, alias, prod_type, ': Quantity Of Measure =', qom, "".join([' -- https://pds-ext-prod-live.trade.tt/me/index.html#i', instrument_id]))
                                found_qom = True
                        # except StopIteration as e:
                        #     break

    def find_instruments_incorrectly_labeled_as_interproduct(self):
        # Verify there are no products without a Description

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        stock_options = []

        print("Alias, InterProduct, Leg List, URL")
        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition["Symbol"]
                name = product_definition["Name"]
                asset_class = product_definition["AssetClassId"]
                is_interproduct = product_definition['IsInterProduct']
                if is_interproduct:
                    instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id + "&slim=false"
                    instrument_list = self.parse_pds_output(instr_list_url)
                    for instrument in instrument_list:
                        instrument_legs = None
                        leg_list = []
                        instrument_id = str(instrument["i"])
                        url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                        instruments = self.parse_pds_output(url)
                        instrument = instruments[0]
                        instrument_legs = copy.deepcopy(instrument['legs'])
                        instrument_definition = self.translate_instrument_data(instrument)
                        alias = instrument_definition["Alias"]
                        term = instrument_definition["Term"]
                        name = instrument_definition["Name"]
                        for leg in instrument_legs:
                            leg_list.append(leg['ls'])
                        if leg_list.count(leg_list[0]) == len(instrument['legs']):
                            print("{}, {}, {}, {}".format(alias, is_interproduct, leg_list, url))


            except StopIteration as e:
                break

        stock_options.sort()
        for so in stock_options:
            print(so)

    def custom(self):
        # Verify there are no products without a Description

        self.get_all_product_ids()
        get_product_id = self.product_id_generator()
        stock_options = []

        print("Alias, InterProduct, Leg List, URL")
        while True:
            try:
                product_id = str(next(get_product_id))
                prod_url = self.base_url + "/api/1/products/" + product_id + "?slim=false"
                product = self.parse_pds_output(prod_url)
                product_definition = self.translate_product_data(product)
                symbol = product_definition["Symbol"]
                name = product_definition["Name"]
                asset_class = product_definition["AssetClassId"]
                instr_list_url = self.base_url + "/api/1/instruments?productIds=" + product_id + "&slim=false"
                instrument_list = self.parse_pds_output(instr_list_url)
                for instrument in instrument_list:
                    instrument_id = str(instrument["i"])
                    url = self.base_url + "/api/1/instruments?instrumentIds=" + instrument_id + "&slim=false"
                    instruments = self.parse_pds_output(url)
                    instrument = instruments[0]
                    instrument_definition = self.translate_instrument_data(instrument)
                    alias = instrument_definition["Alias"]
                    term = instrument_definition["Term"]
                    name = instrument_definition["Name"]

            except StopIteration as e:
                break

        stock_options.sort()
        for so in stock_options:
            print(so)

runme = TestPDSData()
# runme.verify_environment_diff()
# runme.verify_product_data()
# runme.custom()
runme.generate_pmerge()
# runme.custom()
