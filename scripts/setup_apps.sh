cd trading-utils || exit
#pip3 install -r requirements/base.txt --user
bash ./scripts/start_screen.sh crypto-ma-trade-bot 'python3 crypto_ma_trade_bot.py'
bash ./scripts/start_screen.sh tele-links 'python3 tele_links.py'
#bash ./scripts/start_screen.sh tele-twitter 'python3 tele_twitter.py'
bash ./scripts/start_screen.sh options-price-tracker 'python3 options_price_tracker.py -t SPX,XHB,XLC,XLY,XLP,XLE,XLF,XLV,XLI,XLB,XLR,XLK,XME,XOP,GDX,IYR,XLU'
bash ./scripts/start_screen.sh tele-stock-rider-bot 'python3 tele_stock_rider_bot.py'
bash ./scripts/start_screen.sh tele-theta-gang-bot 'python3 tele_theta_gang_bot.py'
