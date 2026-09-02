import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Data:
    def __init__(self, companies, start, end):
        self.companies_info=companies
        self.statistics=[]
        self.companies=[]
        for i in self.companies_info:
            self.companies.append(i[0])


        self.start=start
        self.end=end


    def load_companies(self):
        self.tickers = yf.Tickers(self.companies)
        self.data=yf.download(self.companies,self.start, end=self.end, interval='1d')


    def construct_data(self):
        self.results={}
        for i in self.companies:
            df=pd.DataFrame()
            self.results[i]=df

            key_open=('Open', i)
            key_close=('Close', i)
            df['Open']=self.data[key_open]
            df['Open'] = df['Open'].interpolate(method='ffill')
            df['Close']=self.data[key_close]
            df['Close'] = df['Close'].interpolate(method='ffill')
            df['Daily Return'] = df['Close'].pct_change()







    def statistic(self):
        for company in self.companies:
            df= self.results[company]
            df['Weekly_average'] = df['Close'].rolling(window=5, center=True).mean()
            df['Cumulative Growth'] = (1 + df['Daily Return']).cumprod() - 1 # this gives you how much money (dollar amount) u make assuming an initial investment of 1 dollar
                                                                            #1*(1+d1)*(1+d2)...-1

            daily_volatility=df['Daily Return'].std()
            annual_variance=daily_volatility**2*252

            df['Annual_std']=np.sqrt(annual_variance)
            valid_close_prices = df['Close'].dropna() #based on start and end dates, it could be possible that they are NaNs (non trading days). This is done to avoid NaN computations.
            #u have to create a new df bc all columns have to be the same length in a df.
            #if u do  df['Close']= df['Close'].dropna(), pandas essentially undoes the dropping bc it realises the length is now different from the other columns.


            if len(valid_close_prices) == 0:
                df['CAGR'] = None
                continue


            initial_price = valid_close_prices.iloc[0]
            final_price = valid_close_prices.iloc[-1]

            # Count only the days the stock actually traded
            total_days = len(valid_close_prices)

            # Calculate CAGR normally
            df['CAGR'] = (final_price / initial_price) ** (252 / total_days) - 1 #fp=ip*(1+CAGR)**(N/252),252 defines a trading year
            df['Arith_mean']=df['CAGR']+df['Annual_std']**2/2
            #CAGR is a compounded growth rate, it is not linear. Arithmetic mean is the average growth rate over some time period average of (+50, -20, +30,..)
            #CAGR is the slope of the line that connects the beginning and end of the log cumulative growth curve
            #Artihmetic mean = CAGR + Annual Std^2/2
            #CAGR is not the average of yearly returns (that is artihmetic mean), it is the median. Outliers skew the arithmetic mean higher.

    def export_statistics(self, export):
        results=[]
        for company, label in self.companies_info:
            sector=self.tickers.tickers[company].info['industry'] if label!="ETF" else "None"
            results.append({
                "Company": company,
                "Type": label,
                "Sector":  sector,
                "CAGR": self.results[company]['CAGR'].iloc[0],
                "Annual Std": self.results[company]['Annual_std'].iloc[0],
                "Arithm_mean": self.results[company]['Arith_mean'].iloc[0]
            })

        self.df_results = pd.DataFrame(results)
        self.df_results=self.df_results.sort_values(by='Type')

        title=f"{self.start} to {self.end}.csv" if self.end!=None else f"{self.start} to Now.csv"
        if export:
            self.df_results.to_csv(title, index=False)

    def plotting_statistics(self):
        for stat in self.statistics:

            plt.figure(figsize=(10, 6))

            y = []
            x = self.companies
            title = f"{stat} Comparison from {self.start} to {self.end}" if self.end != None else f"{stat} Comparison from {self.start} to Now"
            save = f"{stat} from {self.start} to {self.end}.png" if self.end != None else f"{stat} from {self.start} to Now.png"

            for company in self.companies:
                y.append(self.results[company][stat].iloc[0])

            plt.bar(x, y)
            plt.title(title)
            plt.xticks(rotation=45, ha='right')
            plt.xlabel("Companies")
            plt.savefig(save, dpi=300, bbox_inches='tight')

            plt.close()



    def plotting(self, var):
        for company in self.companies:
            days=[]
            for i in range(len(self.results[company][var])):
                days.append(i)

            plt.plot(days, self.results[company][var])
            plt.title(f"{var} for {company}")
            plt.show()

            # plt.plot(days, self.results[company]['Close'], label='close')
            # plt.plot(days, self.results[company]['Weekly_average'], label='average')
            # plt.title(f"Closing Price for {company}")
            # plt.legend()
            # plt.show()

    def plotting_specific(self, company, var):
        days = []
        for i in range(len(self.results[company][var])):
            days.append(i)
        plt.plot(days, self.results[company][var])


