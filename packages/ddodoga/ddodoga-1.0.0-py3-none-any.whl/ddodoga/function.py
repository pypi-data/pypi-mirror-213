def hiprint():
    print("hello")
    print("pypiex")

def showSamsung():
    import yfinance as yf

    ticker = '005930.KS'
    data = yf.download(tickers=ticker, period='10y', interval='1d')
    # 데이터 출력
    print(data)

showSamsung()