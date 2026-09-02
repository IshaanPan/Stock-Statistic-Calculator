<img width="300" height="300"  aligh="left" alt="CAGR from 2022-09-06 to Now" src="https://github.com/user-attachments/assets/22a5e5ac-c63a-496e-bf28-d61ee02d02af" />For a give time period, it computes CAGR through:
final_price=initial_price*(1+CAGR)**(total_days/252).

It assumes a trading year has 252 days. The largest current limitation of the code is in how total_days is computed. Since yahoo finance simply leaves days blank for non-trading days, ffill was used. But this artificially 
puts 0% daily returns on days that wouldn't have had them otherwise, and inflates the total_days count, thereby effect the CAGR (and the standard deviation calculation). The annual standard deviation is computed by simply
finding the standard deviation of the daily fluctuations over the given timeframe and multiplying it by sqrt(252). This assumes that log of the price P(t) is normally distributed, and thus its variance scales linearly
time (and because std=sqrt(variance)), the annual_std becomes sqrt(252). Additionally, CAGR can be unpredicted because dividends are not paid out and this is seen in the results for the chosen analysis, which is by default in the code. 

While the absolute values of these statistics are not 100% correct, general trends of macroscopic stock behaviour for different types of equities (stock and ETFs) is accurately covered. Additioanlly, the code can be used to 
generate plots and save output data for as many companies as user desired (given you know their yahoo finance tickers) and whatever time-scale. The default code analyses three different time scales, before the AI craze, after, and the last 3 months. It can be used to generate plots such as this:
<img width="300" height="300" aligh="left" alt="CAGR from 2018-09-06 to 2022-09-06" src="https://github.com/user-attachments/assets/554a780e-0f7c-4b16-a0bd-6295ba793d11" />




