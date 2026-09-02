import yfinance as yf
from yahoo_scraper import Data
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore", category=FutureWarning)

companies=[('NVDA', 'Stock'), ('ABN.AS', 'Stock'), ('ING', 'Stock'), ('VUSA.DE', 'ETF'),
           ('AMAT', 'Stock'), ('AMD', 'Stock'), ('SPYE.DE', 'ETF'), ('ITEC.L', 'ETF'),
           ('STQ.PA', 'ETF'), ('ASML.AS', 'Stock'), ('TSM', 'Stock'), ('MU', 'Stock'), ('SU.PA', 'Stock')]

statistics=['CAGR', 'Annual_std']

end1="2022-09-06"
start1="2018-09-06"


start2="2022-09-06"
end2=None

starts=[start1, start2, "2026-06-06"]
ends=[end1, end2, None]


for i in range(len(starts)):
    info=Data(companies, starts[i], ends[i])
    info.load_companies()
    info.statistics=statistics
    info.construct_data()
    info.statistic()
    info.export_statistics(False)
    info.plotting_statistics()




#core clarifications:
#you assume that the price is P(t). The log of the price log(P(t)) ~ N(mu(t), sigma(t)). Sigma(t) grows with time for price. Variance scales linearly, std scale sqrt(t).
# derivation of uncertainty vs time comes from the assumption that log daily returns are iids.



#current limitations:
# 1) CAGR possibly underestimated due to divideneds not being accounted for. Results in negative CAGR for ABN/ING for 2018-2022
# 2) Mix of American and European Stocks, meaning trading days are convoluted resulting in NaNs. Ffill artificially puts a 0% return for these NaNs, possibly shrinking Annual Std.



