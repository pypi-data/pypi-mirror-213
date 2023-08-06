import ttdatasdk
import datetime

"""账号认证"""
username = 'admin'
password = 'admin'
ttdatasdk.auth(username, password)

"""使用 token 认证账号"""
# ttdatasdk.auth_by_token(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTY4MzExNTIwMn0.ojW0pJTrCsNx8FVaIgSOPnTNm5gb8AschV8FOoqZEUg")

# 获取因子数据
# factor_list = ['float_share', 'pe', 'pe_ttm', 'ma_5', 'ema_5', 'dv_ratio']
factor_list = ['open', 'high', 'low', 'close', 'volume', 'amount']
# 获取unit='1d'的数据
df = ttdatasdk.get_factor(stock_pool=['000300.SH'], trade_date='2023-03-29', factor_list=factor_list)
print(df)
# 获取unit='1m'的数据
df = ttdatasdk.get_factor(sec_code_list=['000001.SZ'], end_date='2023-03-29', factor_list=factor_list, count=5, unit='1m', dividend_type='front')
print(df)

# ret = ttdatasdk.submit(strategy_code="rpc_strategy_demo", run_backtest=False)
# ret = ttdatasdk.submit(strategy_code="rpc_strategy_demo", file_path='rpc_test_strategy2.py', run_backtest=False)
# print(ret)


# 获取历史数据，可查询多个标的单个数据字段
current_dt = datetime.datetime.strptime('2023-03-29 14:58:00', '%Y-%m-%d %H:%M:%S')
# current_dt = datetime.datetime.now()
print(current_dt)
stock_list = ['601236.SH', '000002.SZ']
# # 截止昨日同一分钟
end_datetime = (current_dt + datetime.timedelta(days=-1)).strftime('%Y-%m-%d %H:%M:%S')
df = ttdatasdk.get_history(5, unit='1m', end_datetime=end_datetime, field='close', security_list=stock_list, dividend_type='front')
print(df)

# 截止昨日
end_date = (current_dt + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
df = ttdatasdk.get_history(5, unit='1d', end_date=end_date, field='close', security_list=stock_list)
print(df)


# 获取历史数据，可查询单个标的多个数据字段
sec_code = '000001.SZ'
end_datetime = (current_dt + datetime.timedelta(minutes=-1)).strftime('%Y-%m-%d %H:%M:%S')
df = ttdatasdk.get_attribute_history(security=sec_code, count=5, unit='1m', end_datetime=end_datetime, fields=['open', 'close'])
print(df)