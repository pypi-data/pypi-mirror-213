import BBFinance as bb
import yfinance as yf
yf.pdr_override()

bb.get_beta('BBDC4.SA')


stock = yf.Ticker('VALE3.SA')
info = stock.info #DADO Q VEM COMO UM DICIONARIO, SE NAO FOR UM DICIONARIO VAI APRESENTAR TICKER INVALIDO







