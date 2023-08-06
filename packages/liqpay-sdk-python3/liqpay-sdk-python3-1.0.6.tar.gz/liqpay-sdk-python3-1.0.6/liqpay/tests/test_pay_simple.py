# coding=utf-8
import unittest
from liqpay import LiqPay, ParamValidationError


class TestLiqPaySimple(unittest.TestCase):
    def setUp(self):
        self.liqpay = LiqPay("", "")
        self.maxDiff = None

    def test_api(self):
        self.assertTrue(self.liqpay.api("payment/status", {"payment_id": "3940"}))

    def test_gen_form(self):
        with open("button.html", "r") as f:
            expected_form_out = f.read()

        # test unicode issue with ru symbols
        params = {
            "amount": "3940",
            "currency": "UAH",
            "description": "тест",
            "test": "cccc",
            "language": "en",
        }

        self.assertEqual(self.liqpay.cnb_form(params), expected_form_out)

        # ru symbols in unicode
        params.update(description="тест")
        self.assertEqual(self.liqpay.cnb_form(params), expected_form_out)

        # test gen_form without required param
        del params["amount"]
        self.assertRaises(ParamValidationError, self.liqpay.cnb_form, params)


if __name__ == "__main__":
    unittest.main()
