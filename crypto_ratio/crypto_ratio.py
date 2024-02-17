#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import logging
from logging.handlers import RotatingFileHandler

def setUpLogger(log_out = 1) -> logging.Logger:
    logger = logging.getLogger("crypto_ratio")
    logger.setLevel(logging.DEBUG)
    if log_out == 1:
      file_handler = RotatingFileHandler(filename="/var/log/crypto_ratio.log", maxBytes=1000*1000, backupCount=10)
      file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]:%(message)s'))
      logger.addHandler(file_handler)
    elif log_out == 2:
      console_handler = logging.StreamHandler()
      console_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(module)s][%(levelname)s]:%(message)s'))
      logger.addHandler(console_handler)
    return logger
logger = setUpLogger()

TRADING_PERCENTAGE_THRESHOLD = 6

coins = ("BTC", "ETH")
currentCoinInvest = "ETH"
lastTradedRatio = 13.4502

def getData() -> 'dict[str, float]':
	btc = -1
	eth = -1
	etcbtc = -1
	data_btc = None
	data_eth = None
	try:
		data_btc = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=BTC').json()
		data_eth = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=ETH').json()
		return {
		'BTCEUR': float(data_btc['data']['rates']['EUR']),
		'ETHEUR': float(data_eth['data']['rates']['EUR']),
		'BTCETH': float(data_btc['data']['rates']['ETH'])
	}
	except Exception as e:
		logger.error(e)
		raise e

def formatMessage(btc: float, eth: float, ratio: float, percentage: float, shouldTrade: bool) -> str:
    return (
    f'{"BTC-EUR"+("*" if currentCoinInvest == "BTC" else ""):<19} = {btc:.4f} €\n'
    f'{"ETH-EUR"+("*" if currentCoinInvest == "ETH" else ""):<19} = {eth:.4f} €\n'
    f'{"BTC-ETH":<19} = {ratio:.4f}\n'
    f'{"Change":<19} = {percentage:.4f}%\n'
    f'{"Should Trade(" + str(TRADING_PERCENTAGE_THRESHOLD) + "%)":<19} = {"Yes" if shouldTrade else "No"}'
)

def send_notification(msg: bytes) -> int:
    response: requests.Response = requests.post(
        "https://ntfy.sh/stylneo-crypto",
        data=msg,
        headers={"Title": "Coinbase Crypto Trading Opportunity"},
    )

    return response.status_code

def main():
    # Get Yahoo Finance data
    data = getData()

    ratio = data['BTCETH']
    percentage =  ((ratio / lastTradedRatio) - 1.0) * 100
    shouldTrade = (
        abs(percentage) > TRADING_PERCENTAGE_THRESHOLD and
		((percentage < 0 and currentCoinInvest == 'ETH') or (percentage > 0 and currentCoinInvest == 'BTC'))
    )

    logger.info(f"Ratio={ratio:07.4f},Percentage={percentage:05.2f}%,Treshold={TRADING_PERCENTAGE_THRESHOLD*(-1 if currentCoinInvest == 'ETH' else 1):>2}%,Trade={shouldTrade}")

    if shouldTrade:
        ret = send_notification(
            formatMessage(data['BTCEUR'], data['ETHEUR'], ratio, percentage, shouldTrade).encode("utf-8")
        )
        logger.debug(f'Notification responce status code={ret}')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        for l in traceback.format_exc().splitlines():
                logger.error(l)
        raise e
