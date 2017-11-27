import requests
import ast


class TestErisMarketData():
    def __init__(self):

        base_urls = ["http://pds-upgrade.elasticbeanstalk.com", "http://pds-test.elasticbeanstalk.com",
                     "http://pds-dev.debesys.net", "http://pds-int-dev-sim.debesys.net",
                     "http://pds-int-stage-cert.debesys.net", "http://pds-int-stage-sim.debesys.net",
                     "http://pds-ext-prod-cert.debesys.net", "http://pds.debesys.net",
                     "http://pds-ext-uat-cert.debesys.net"]

        self.headers = {'content-type': 'application/json'}
        self.market = "HKEX"
        self.base_url = base_urls[2]

    def parse_pds_output(self, url):
        request = requests.get(url, headers=self.headers)
        output = request._content
        while ":false" in output:
            output = output.replace(":false", ":\"false\"")
        while ":true" in output:
            output = output.replace(":true", ":\"true\"")
        full_output = ast.literal_eval(output)
        try:
            output = full_output["instruments"]
        except:
            try:
                output = full_output["data"]["globalData"]["markets"]
            except:
                output = full_output["instrument"]

        return output

    def get_market_id(self, market):
        market_ids_url = self.base_url + "/api/1/systemdata?type=market"
        market_ids = self.parse_pds_output(market_ids_url)
        for market_id in market_ids:
            if market in str(market_id):
                return str(market_id["i"])
        else:
            print ("Market, \"{0}\" does not seem to exist.".format(market))

    def test_market_data(self):

        new_products = ["ALI", "AVI", "BAI", "CGN", "CHO", "CHQ", "CKP", "CRR", "CTY", "DIG", "EVG", "FOS", "GAC", "GOM", "HTS", "HUD", "POL", "SMC", "SOA", "SOH", "SUN", "MHI"]

        url = "https://pds-dev.debesys.net/api/1/instruments?marketIds=" + self.get_market_id(self.market)
        instruments = self.parse_pds_output(url)

        # if any(prod in instruments for prod in new_products):
        #     print prod

        print "len(instruments) =", len(instruments)
            #
            #     # contract_elements = {"l": "Last Trading Date"}
            #     # contract_elements = {"cr": "CouponRate", "l": "Last Trading Date"}
            # #     contract_fields = {"cr": 0, "l": 0}
            # #     missing_contract_fields = {"cr": [], "l": []}
            # #     number_of_spots = 0
            # #
        for instrument in instruments:
            prod_code = instrument["a"].split(' ')[0]
            if prod_code in new_products:
                print prod_code
            # instr_url = "https://pds-dev.debesys.net/api/1/instruments/" + str(instrument["i"]) + "?slim=false"
            # instr = self.parse_pds_output(instr_url)
            #
            #         print '\n'
            #         print instr

            #
            #         if "FLEX SPOT" in instr["a"]:
            #             number_of_spots += 1
            #
            #         target = instr.keys()
            #         for field in contract_fields.keys():
            #             if field not in target:
            #                 if instr["a"] not in missing_contract_fields[field]:
            #                     missing_contract_fields[field].append(instr["a"])
            #             else:
            #                 contract_fields[field] += 1
            #
            #     for element in contract_elements.keys():
            #         total_expected = len(instruments) - number_of_spots if element == "l" else len(instruments)
            #         logger.result("Contracts containing {}"
            #                       .format(contract_elements[element]),
            #                       total_expected, contract_fields[element])
            #         if len(missing_contract_fields[element]) > 0:
            #             missing_contract_fields[element].sort()
            #             for contract in missing_contract_fields[element]:
            #                 if "FLEX SPOT" not in contract:
            #                     print contract
            #
            # def test_tick_info(self):
            #     url = "https://pds-dev.debesys.net/api/1/instruments?marketIds=" + self.get_market_id(self.market)
            #     instruments = self.parse_pds_output(url)
            #     uses_display_factor = False
            #
            #     ticksize_count = 0
            #     display_factor_count = 0
            #     numerator_count = 0
            #     denominator_count = 0
            #     for instrument in instruments:
            #         instrument_id = instrument['i']
            #         tickinfo_url = "https://pds-dev.debesys.net/api/1/instruments/tickinfo?instrumentIds=" + str(instrument_id)
            #         tickinfo = self.parse_pds_output(tickinfo_url)
            #         for tick_detail in tickinfo:
            #             ticksize_count = ticksize_count + tick_detail.keys().count("ts")
            #             display_factor_count = display_factor_count + tick_detail.keys().count("f")
            #             numerator_count = numerator_count + tick_detail.keys().count("tn")
            #             denominator_count = denominator_count + tick_detail.keys().count("td")
            #
            #     # ***********************************************************
            #     logger.step("Ensure tick info exists for all instruments")
            #     # ***********************************************************
            #
            #     logger.result("Ticksize in Instruments. {} have the property, out of a total of {} instruments".format(
            #         ticksize_count, len(instruments)), True, ticksize_count == len(instruments))
            #     if uses_display_factor:
            #         logger.result(
            #             "Display factor in Instruments. {} have the property, out of a total of {} instruments".format(
            #                 display_factor_count, len(instruments)), True, display_factor_count == len(instruments))
            #     else:
            #         logger.result(
            #             "Display factor in Instruments. {} have the property, out of a total of {} instruments".format(
            #                 display_factor_count, 0), True, display_factor_count == 0)
            #     logger.result("Numerator in Instruments. {} have the property, out of a total of {} instruments".format(
            #         numerator_count, len(instruments)), True, numerator_count == len(instruments))
            #     logger.result("Denominator in Instruments. {} have the property, out of a total of {} instruments".format(
            #         denominator_count, len(instruments)), True, denominator_count == len(instruments))


runme = TestErisMarketData()
runme.test_market_data()
