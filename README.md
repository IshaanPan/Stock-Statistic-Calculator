For a give time period, it computes CAGR through:
final_price=initial_price*(1+CAGR)**(total_days/252).

It assumes a trading year has 252 days. The largest current limitation of the code is in how total_days is computed. Since yahoo finance simply leaves days blank for non-trading days, ffill was used. But this artificially 
puts 0% daily returns on days that wouldn't have had them otherwise, and inflates the total_days count, thereby effect the CAGR (and the standard deviation calculation). The annual standard deviation is computed by simply
finding the standard deviation of the daily fluctuations over the given timeframe and multiplying it by sqrt(252). This assumes that log of the price P(t) is normally distributed, and thus its variance scales linearly
time (and because std=sqrt(variance)), the annual_std becomes sqrt(252).
