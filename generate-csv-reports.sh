python3 report_by_query.py --count=5 -t "EMA 8x21 Pullback" -q "(last_close > 20) and (day_0_ema_60 < day_0_ema_50 < day_0_ema_45 < day_0_ema_40 < day_0_ema_35 < day_0_ema_21 < day_0_ema_8) and (vol_ema_3 > vol_ema_5 > vol_ema_7) and (last_low > day_0_ema_21) and (last_low < day_0_ema_8) and (adx_14 < 30) and (adx_9 > adx_14 > adx_21)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "8x21" -q "(last_close > 20) and (last_close > day_0_ema_8) and (day_0_ema_8 > day_0_ema_21) and (day_1_ema_8 < day_1_ema_21)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Ema21 Bounce" -q "(last_close > 20) and (day_0_ema_8 > day_0_ema_21) and (day_0_ema_8 > day_0_ema_21) and (last_high < day_0_ema_8) and (last_low > day_0_ema_21) and (daily_strat_candle.str.contains('.*-red-green$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Power of 3 Daily" -q "(last_close > 20) and (power_of_3_daily == True)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Power of 3 Weekly" -q "(last_close > 20) and (power_of_3_week_1 == True) and (last_close < day_0_boll_21_2)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "⬆ 5D Volume" -q "(last_close > 20) and (last_volume > day_2_volume > day_3_volume > day_4_volume > day_5_volume > day_6_volume > day_7_volume > day_8_volume > day_9_volume)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "⬆ 4D Vol/R-G-G Candles" -q "(last_close > 20) and (last_volume > day_2_volume > day_3_volume > day_4_volume) and (daily_strat_candle.str.contains('red-green-green$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "⬆ 2W Vol/GG Candles" -q "(last_close > 20) and (week_0_volume > week_1_volume > week_2_volume > week_3_volume and (week_1_strat.str.contains('2d-2d-2u$')) and (week_1_strat_candle.str.contains('.*-green-green$')))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "123 Pullbacks(Daily)" -q "(last_close > 20) and (adx_14 > 35) and (pdi_14 > mdi_14) and (daily_strat.str.contains('2d-2d-2u$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "123 Pullbacks(week_1)" -q "(last_close > 20) and (adx_14 > 35) and (pdi_14 > mdi_14) and (week_1_strat.str.contains('2d-2d-2u$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Mean Rev 50 LowerBB" -q "(last_close > 20) and (daily_strat_candle.str.contains('.*-red-green$')) and (last_close < day_0_boll_50_3_lb)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Mean Rev LowerBB" -q "(last_close > 20) and (daily_strat_candle.str.contains('.*-green$')) and (last_close < day_0_boll_21_2_lb)" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Mean Reversion 21 LowerBB" -q "(last_close > 20) and (last_close < day_0_boll_21_3_lb) and (daily_strat_candle.str.contains('.*-green$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Squeeze Up" -q "(last_close > 20) and (daily_strat.str.contains('.*-2u$')) and (daily_strat_candle.str.contains('.*-green$')) and (week_1_strat.str.contains('.*-1$')) and (week_1_strat_candle.str.contains('.*-green$'))" -o "smooth_30" -e
python3 report_by_query.py --count=5 -t "Momentum Trending" -q "(last_close > 20) and (last_close > day_0_ema_3 > day_0_ema_5 > day_0_ema_7 > day_0_ema_9 > day_0_ema_11 > day_0_ema_13 > day_0_ema_30 > day_0_ema_35 > day_0_ema_40 > day_0_ema_45 > day_0_ema_50 > day_0_ema_55 > day_0_ema_60)" -o "smooth_30" -e
