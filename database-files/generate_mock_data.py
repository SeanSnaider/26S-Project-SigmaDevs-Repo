# Faker library: https://faker.readthedocs.io/en/master/
# Providers reference: https://faker.readthedocs.io/en/master/providers.html
# date_time provider: https://faker.readthedocs.io/en/master/providers/faker.providers.date_time.html
# person provider: https://faker.readthedocs.io/en/master/providers/faker.providers.person.html

from faker import Faker
import random

fake = Faker()
Faker.seed(42)
random.seed(42)

# lookup tables
tickers    = ['AAPL','MSFT','NVDA','GOOGL','AMZN','META','TSLA','JPM','V','MA',
              'SPY','QQQ','IWM','VTI','VOO']
exchanges  = ['NASDAQ','NYSE','NYSE Arca']
strat_types = ['Momentum','Mean Reversion','Rotation','Hedging','Long Only','Passive']
strat_params = ['lookback=30,stop=0.03','zscore=1.5,window=20','rebalance=10,max=0.35',
                'monthly_contrib=500','hold_forever=true','hedge_band=0.02,weekly']
analyst_firms = ['Goldman Sachs','Morgan Stanley','JPMorgan','Bank of America','Citigroup']
bench_sectors = ['Technology','Market','Small Cap','Bonds','Global']
bench_data = {
  'Technology': ('Nasdaq-100 Index','QQQ',441.30,'Equity Index'),
  'Market':     ('S&P 500 Index','SPY',518.24,'Equity Index'),
  'Small Cap':  ('Russell 2000','IWM',198.45,'Equity Index'),
  'Bonds':      ('US Agg Bond Index','AGG',96.82,'Bond Index'),
  'Global':     ('MSCI World Index','ACWI',107.55,'Equity Index'),
}
role_names = ['Quantitative Trader','Data Analyst','Portfolio Manager','Risk Analyst',
              'Beginner Investor','Financial Advisor','Retail Investor','Institutional Trader']
action_types = ['Uploaded trade log','Ran cleaning pipeline','Updated permissions',
                'Viewed market summary','Created portfolio','Executed trade','Logged in']
chart_types  = ['Line Chart','Bar Chart','Pie Chart','Area Chart','Scatter Plot','Heatmap']

# setup
print("USE PortIQ;")
print("SET FOREIGN_KEY_CHECKS = 0;")
for t in ["Benchmark","PerformanceRecord","RiskMetric","Strategy","Trade","AnalystRating",
          "Asset","StockPosition","PortfolioSnapshot","Portfolio","DashboardLayout",
          "DashBoard","Visualization","DataCleaningMethod","Dataset","ChatSession",
          "Customer","Permission","Role","Action","DailySummary","Users"]:
  print(f"DELETE FROM {t};")
print("SET FOREIGN_KEY_CHECKS = 1;")

# users
persona_users = [
  (1, 'Andrew',  'Rock',     'andrewrock',  'andrew.rock@portiq.com',      '1993-06-15 00:00:00'),
  (2, 'John',    'Data',     'johndata',    'john.data@portiq.com',        '1980-03-12 00:00:00'),
  (3, 'Katrina', 'Williams', 'kwilliams',   'katrina.williams@portiq.com', '1985-09-21 00:00:00'),
  (4, 'Jane',    'Doe',      'janedoe',     'jane.doe@portiq.com',         '1998-11-08 00:00:00'),
]
gen_users = []
for i in range(5, 31):
  f = fake.first_name()
  l = fake.last_name()
  gen_users.append((i, f, l, f"{f.lower()}{l.lower()}{i}",
                    f"{f.lower()}.{l.lower()}{i}@portiq.com",
                    f"{fake.date_of_birth(minimum_age=22, maximum_age=60)} 00:00:00"))
all_users = persona_users + gen_users
user_ids  = [u[0] for u in all_users]

print("INSERT INTO Users (userID, first_name, last_name, username, email, passwordHash, birth_date) VALUES")
for idx, u in enumerate(all_users):
  comma = "," if idx < len(all_users) - 1 else ";"
  print(f"  ({u[0]}, '{u[1]}', '{u[2]}', '{u[3]}', '{u[4]}', 'hashed_pw_{u[0]}', '{u[5]}'){comma}")

# roles
persona_roles = [
  (101, 'Quantitative Trader',       1),
  (102, 'Data Analyst',              2),
  (103, 'Chief Information Officer', 3),
  (104, 'Beginner Investor',         4),
]
gen_roles = [(105 + i, random.choice(role_names), uid) for i, uid in enumerate(range(5, 31))]
all_roles = persona_roles + gen_roles
role_ids  = [r[0] for r in all_roles]

print("INSERT INTO Role (RoleID, name, user_id) VALUES")
for idx, r in enumerate(all_roles):
  comma = "," if idx < len(all_roles) - 1 else ";"
  print(f"  ({r[0]}, '{r[1]}', {r[2]}){comma}")

# permissions
print("INSERT INTO Permission (permission_id, Can_Read, Can_Write, Can_CREATE, table_id, role_id) VALUES")
for idx, rid in enumerate(role_ids):
  w = random.choice([True, False])
  c = w and random.choice([True, False])
  comma = "," if idx < len(role_ids) - 1 else ";"
  print(f"  ({1001+idx}, TRUE, {'TRUE' if w else 'FALSE'}, {'TRUE' if c else 'FALSE'}, {random.randint(1,10)}, {rid}){comma}")

# customers
print("INSERT INTO Customer (customer_id, name, role_id) VALUES")
sampled = random.sample(role_ids, 20)
for idx, rid in enumerate(sampled):
  role = next(r for r in all_roles if r[0] == rid)
  user = next(u for u in all_users if u[0] == role[2])
  comma = "," if idx < 19 else ";"
  print(f"  ({2001+idx}, '{user[1]} {user[2]}', {rid}){comma}")

# actions
print("INSERT INTO Action (action_id, action_type, date, user_id) VALUES")
for idx in range(50):
  dt    = fake.date_time_between(start_date='-6m', end_date='now')
  comma = "," if idx < 49 else ";"
  print(f"  ({3001+idx}, '{random.choice(action_types)}', '{dt}', {random.choice(user_ids)}){comma}")

# daily summaries
persona_summaries = [
  (4001, '2026-04-10 18:00:00', '2026-04-10 00:00:00',
   'Portfolio gained on strength in large-cap tech and broad market momentum.', 1),
  (4002, '2026-04-10 18:05:00', '2026-04-10 00:00:00',
   'ETL pipeline completed and all dataset validation checks passed.', 2),
  (4003, '2026-04-10 18:10:00', '2026-04-10 00:00:00',
   'Security review completed for role and permission changes.', 3),
  (4004, '2026-04-10 18:15:00', '2026-04-10 00:00:00',
   'Beginner dashboard summary generated with top movers and benchmark comparison.', 4),
]
gen_summaries = []
for i in range(46):
  dt = fake.date_time_between(start_date='-6m', end_date='now')
  gen_summaries.append((4005+i, str(dt), f"{dt.date()} 00:00:00", fake.sentence(nb_words=8), random.choice(user_ids)))
all_summaries = persona_summaries + gen_summaries

print("INSERT INTO DailySummary (summaryId, generated_at, summary_date, summary, user_id) VALUES")
for idx, s in enumerate(all_summaries):
  comma = "," if idx < len(all_summaries) - 1 else ";"
  print(f"  ({s[0]}, '{s[1]}', '{s[2]}', '{s[3]}', {s[4]}){comma}")

# chat sessions
fixed_sessions = [
  (5001, 'active', 'What moved my portfolio today?', 4),
  (5002, 'closed', 'Show me current portfolio P&L.', 1),
]
gen_sessions = []
for i in range(48):
  gen_sessions.append((5003+i, random.choice(['active','closed','closed']),
                       fake.sentence(nb_words=6), random.choice(user_ids)))
all_sessions = fixed_sessions + gen_sessions
session_ids  = [s[0] for s in all_sessions]

print("INSERT INTO ChatSession (session_id, status, messages, user_id) VALUES")
for idx, s in enumerate(all_sessions):
  comma = "," if idx < len(all_sessions) - 1 else ";"
  print(f"  ({s[0]}, '{s[1]}', '{s[2]}', {s[3]}){comma}")

# datasets
persona_datasets = [
  (1001, 'Raw Trading Data',        'CSV',              2),
  (1002, 'Cleaned Trading Data',    'Processed Table',  2),
  (1003, 'Portfolio Dashboard Feed','Dashboard Source', 2),
  (1004, 'Jane Beginner Feed',      'Dashboard Source', 2),
]
gen_datasets = [(1005+i, fake.bs().title()[:45], random.choice(['CSV','JSON','Excel','API Feed']), 2)
                for i in range(26)]
all_datasets = persona_datasets + gen_datasets
dataset_ids  = [d[0] for d in all_datasets]

print("INSERT INTO Dataset (dataset_id, name, type, user_id) VALUES")
for idx, d in enumerate(all_datasets):
  comma = "," if idx < len(all_datasets) - 1 else ";"
  print(f"  ({d[0]}, '{d[1]}', '{d[2]}', {d[3]}){comma}")

# data cleaning methods
persona_dcm = [
  (6001, 1, 'drop_duplicates=true',           'Duplicate Removal', 1001),
  (6002, 2, 'remove_nulls=true',              'Null Removal',      1001),
  (6003, 3, 'standardize_ticker_format=true', 'Formatting',        1001),
  (6004, 1, 'winsorize_outliers=0.01',        'Outlier Handling',  1002),
  (6005, 2, 'normalize_numeric_fields=true',  'Normalization',     1002),
]
method_types = ['Duplicate Removal','Null Removal','Formatting','Outlier Handling','Normalization']
method_params = {'Duplicate Removal':'drop_duplicates=true','Null Removal':'remove_nulls=true',
                 'Formatting':'standardize_format=true','Outlier Handling':'winsorize=0.01',
                 'Normalization':'normalize=true'}
gen_dcm = []
for i in range(45):
  mt = random.choice(method_types)
  gen_dcm.append((6006+i, random.randint(1,5), method_params[mt], mt, random.choice(dataset_ids)))
all_dcm = persona_dcm + gen_dcm

print("INSERT INTO DataCleaningMethod (method_id, method_order, parameter, method_type, CleaningDataSet) VALUES")
for idx, d in enumerate(all_dcm):
  comma = "," if idx < len(all_dcm) - 1 else ";"
  print(f"  ({d[0]}, {d[1]}, '{d[2]}', '{d[3]}', {d[4]}){comma}")

# visualizations
persona_viz = [
  (7001, 'Andrew Performance Trend', 'Line Chart', 1003),
  (7002, 'Andrew Asset Allocation',  'Pie Chart',  1003),
  (7003, 'John Dataset Quality',     'Bar Chart',  1002),
  (7004, 'Jane Portfolio Overview',  'Area Chart', 1004),
]
gen_viz = [(7005+i, fake.bs().title()[:45], random.choice(chart_types), random.choice(dataset_ids))
           for i in range(26)]
all_viz = persona_viz + gen_viz
viz_ids = [v[0] for v in all_viz]

print("INSERT INTO Visualization (visualization_id, title, chart_type, VizDataSet) VALUES")
for idx, v in enumerate(all_viz):
  comma = "," if idx < len(all_viz) - 1 else ";"
  print(f"  ({v[0]}, '{v[1]}', '{v[2]}', {v[3]}){comma}")

# dashboards
persona_dash = [
  (8001, 'Andrew Trading Dashboard', True,  7001),
  (8002, 'Andrew Allocation View',   True,  7002),
  (8003, 'John Admin Dashboard',     True,  7003),
  (8004, 'Jane Beginner Dashboard',  True,  7004),
]
gen_dash = [(8005+i, fake.bs().title()[:45], random.choice([True,True,False]), random.choice(viz_ids))
            for i in range(26)]
all_dash = persona_dash + gen_dash
dash_ids = [d[0] for d in all_dash]

print("INSERT INTO DashBoard (dashboard_id, title, visibility, VizDash) VALUES")
for idx, d in enumerate(all_dash):
  comma = "," if idx < len(all_dash) - 1 else ";"
  print(f"  ({d[0]}, '{d[1]}', {'TRUE' if d[2] else 'FALSE'}, {d[3]}){comma}")

# dashboard layouts
persona_layout = [
  (9001, 'Quant Trader Main Layout',       'Figma', 8001),
  (9002, 'Quant Trader Allocation Layout', 'Figma', 8002),
  (9003, 'Data Analyst Builder Layout',    'Figma', 8003),
  (9004, 'Beginner Guided Layout',         'Figma', 8004),
]
gen_layout = [(9005+i, fake.bs().title()[:45], random.choice(['Figma','CSS','Tailwind']), dash_ids[4+i])
              for i in range(26)]
all_layout = persona_layout + gen_layout

print("INSERT INTO DashboardLayout (layout_id, name, source, layout_dash) VALUES")
for idx, l in enumerate(all_layout):
  comma = "," if idx < len(all_layout) - 1 else ";"
  print(f"  ({l[0]}, '{l[1]}', '{l[2]}', {l[3]}){comma}")

# portfolios
persona_portfolios = [
  (101, 'Andrew Main Portfolio',   '2026-01-01 09:00:00', 1487520, 'High',   'USD', 1),
  (102, 'Jane Beginner Portfolio', '2026-02-01 10:00:00',  245800, 'Medium', 'USD', 4),
]
gen_portfolios = []
for i in range(37):
  uid = random.choice(user_ids)
  val = random.randint(10000, 2000000)
  conf = random.choice(['Low','Medium','High'])
  dt   = fake.date_time_between(start_date='-2y', end_date='-6m')
  gen_portfolios.append((103+i, f"{fake.last_name()} Portfolio", str(dt), val, conf, 'USD', uid))
all_portfolios = persona_portfolios + gen_portfolios
port_ids = [p[0] for p in all_portfolios]

print("INSERT INTO Portfolio (portfolio_id, portfolio_name, created_at, total_value, confidence, currency, user_id) VALUES")
for idx, p in enumerate(all_portfolios):
  comma = "," if idx < len(all_portfolios) - 1 else ";"
  print(f"  ({p[0]}, '{p[1]}', '{p[2]}', {p[3]}, '{p[4]}', '{p[5]}', {p[6]}){comma}")

# portfolio snapshots
snap_sessions = session_ids[:len(port_ids)]

print("INSERT INTO PortfolioSnapshot (snapshot_id, snapshot_date, insight_narrative, daily_change_pct, ttlv_value, SessionID, port_id) VALUES")
for i, (sess_id, pid) in enumerate(zip(snap_sessions, port_ids)):
  dt    = fake.date_time_between(start_date='-3m', end_date='now')
  comma = "," if i < len(port_ids) - 1 else ";"
  print(f"  ({11001+i}, '{dt}', '{fake.sentence(nb_words=8)}', "
        f"{round(random.uniform(-2.5,3.5),2)}, {round(random.uniform(10000,2000000),2)}, "
        f"{sess_id}, {pid}){comma}")

# stock positions
persona_positions = [
  (12001, 180.50, 15200.75, 230.00, '2025-12-01 00:00:00', 106240.00, 500, 101),
  (12002, 400.25,  8200.40, 460.00, '2025-11-15 00:00:00', 107167.50, 250, 101),
  (12003, 650.10, 27550.90, 980.00, '2026-01-20 00:00:00', 270336.00, 300, 101),
  (12004, 505.30,  4550.10, 560.00, '2026-02-10 00:00:00',  51824.00, 100, 101),
  (12005, 195.00,  1400.00, 230.00, '2026-02-12 00:00:00',  21248.00, 100, 102),
  (12006, 510.00,   824.00, 540.00, '2026-02-15 00:00:00',  10364.00,  20, 102),
]
gen_positions = []
for i in range(59):
  cost = round(random.uniform(50, 800), 2)
  qty  = random.randint(10, 500)
  mval = round(cost * qty * random.uniform(0.9, 1.3), 2)
  dt   = fake.date_time_between(start_date='-2y', end_date='-1m')
  gen_positions.append((12007+i, cost, round(random.uniform(-5000,30000),2),
                        round(cost*random.uniform(1.05,1.4),2), str(dt), mval, qty,
                        random.choice(port_ids)))
all_positions = persona_positions + gen_positions
pos_ids = [p[0] for p in all_positions]
pos_to_port = {p[0]: p[7] for p in all_positions}

print("INSERT INTO StockPosition (position_id, avg_cost, unrealized_PNL, price_target, acquired_date, market_value, qty_held, port_id) VALUES")
for idx, p in enumerate(all_positions):
  comma = "," if idx < len(all_positions) - 1 else ";"
  print(f"  ({p[0]}, {p[1]}, {p[2]}, {p[3]}, '{p[4]}', {p[5]}, {p[6]}, {p[7]}){comma}")

# assets
persona_assets = [
  (13001, 'Equity', 'AAPL', 2800000000000, 'Apple Inc.',            'NASDAQ',    12001),
  (13002, 'Equity', 'MSFT', 3100000000000, 'Microsoft Corporation', 'NASDAQ',    12002),
  (13003, 'Equity', 'NVDA', 2200000000000, 'NVIDIA Corporation',    'NASDAQ',    12003),
  (13004, 'ETF',    'SPY',   550000000000, 'SPDR S&P 500 ETF Trust','NYSE Arca', 12004),
  (13005, 'Equity', 'AAPL', 2800000000000, 'Apple Inc.',            'NASDAQ',    12005),
  (13006, 'ETF',    'SPY',   550000000000, 'SPDR S&P 500 ETF Trust','NYSE Arca', 12006),
]
gen_assets = []
ticker_list = tickers
for i, pos_id_val in enumerate([p[0] for p in gen_positions]):
  atype  = random.choice(['Equity','Equity','Equity','ETF'])
  ticker = random.choice(ticker_list)
  gen_assets.append((13007+i, atype, ticker, random.randint(10000000000, 3000000000000),
                     ticker, random.choice(exchanges), pos_id_val))
all_assets = persona_assets + gen_assets
asset_ids  = [a[0] for a in all_assets]

print("INSERT INTO Asset (asset_id, asset_type, ticker, total_market, asset_name, exchange, pos_id) VALUES")
for idx, a in enumerate(all_assets):
  comma = "," if idx < len(all_assets) - 1 else ";"
  print(f"  ({a[0]}, '{a[1]}', '{a[2]}', {a[3]}, '{a[4]}', '{a[5]}', {a[6]}){comma}")

# analyst ratings
persona_ratings = [
  (14001, 5, '2026-04-08 00:00:00', 'Goldman Sachs',  13001),
  (14002, 4, '2026-04-08 00:00:00', 'Morgan Stanley', 13002),
  (14003, 5, '2026-04-08 00:00:00', 'JPMorgan',       13003),
  (14004, 4, '2026-04-08 00:00:00', 'Bank of America',13004),
]
gen_ratings = []
for i in range(61):
  dt = fake.date_time_between(start_date='-6m', end_date='now')
  gen_ratings.append((14005+i, random.randint(1,5), str(dt),
                       random.choice(analyst_firms), random.choice(asset_ids)))
all_ratings = persona_ratings + gen_ratings

print("INSERT INTO AnalystRating (rate_id, rating, rating_date, analyst_firm, asset_rating) VALUES")
for idx, r in enumerate(all_ratings):
  comma = "," if idx < len(all_ratings) - 1 else ";"
  print(f"  ({r[0]}, {r[1]}, '{r[2]}', '{r[3]}', {r[4]}){comma}")

# trades
persona_trades = [
  (15001, 'BUY',  '2026-04-05 09:35:00', 100, 212.48, 13001),
  (15002, 'BUY',  '2026-04-04 10:15:00',  50, 428.67, 13002),
  (15003, 'BUY',  '2026-04-03 11:05:00',  80, 901.12, 13003),
  (15004, 'SELL', '2026-04-02 14:40:00',  25, 518.24, 13004),
  (15005, 'BUY',  '2026-04-06 09:50:00',  10, 212.48, 13005),
  (15006, 'BUY',  '2026-04-06 10:20:00',   5, 518.20, 13006),
]
gen_trades = []
for i, aid in enumerate(asset_ids[6:]):
  dt = fake.date_time_between(start_date='-1y', end_date='now')
  gen_trades.append((15007+i, random.choice(['BUY','BUY','BUY','SELL']),
                     str(dt), random.randint(1,200), round(random.uniform(50,900),2), aid))
all_trades = persona_trades + gen_trades
trade_ids  = [t[0] for t in all_trades]

print("INSERT INTO Trade (trade_id, trade_type, trade_date, quantity, price, trade_asset) VALUES")
for idx, t in enumerate(all_trades):
  comma = "," if idx < len(all_trades) - 1 else ";"
  print(f"  ({t[0]}, '{t[1]}', '{t[2]}', {t[3]}, {t[4]}, {t[5]}){comma}")

# strategies
asset_to_port = {a[0]: pos_to_port[a[6]] for a in all_assets}
persona_strategies = [
  (16001, 'Tech Momentum',       'Momentum',       '2026-01-10 09:00:00', 'lookback=30,stop=0.03',     'active',   15001, 101),
  (16002, 'Mean Reversion',      'Mean Reversion', '2026-01-15 10:00:00', 'zscore=1.5,window=20',      'active',   15002, 101),
  (16003, 'AI Growth Rotation',  'Rotation',       '2026-02-01 09:30:00', 'rebalance=10,max=0.35',     'active',   15003, 101),
  (16004, 'Legacy ETF Hedge',    'Hedging',        '2025-12-20 15:00:00', 'hedge_band=0.02,weekly',    'inactive', 15004, 101),
  (16005, 'Beginner Core Growth','Long Only',      '2026-02-10 10:30:00', 'monthly_contrib=500',       'active',   15005, 102),
  (16006, 'Beginner Market ETF', 'Passive',        '2026-02-12 11:00:00', 'hold_forever=true',         'active',   15006, 102),
]
gen_strategies = []
for i, tid in enumerate(trade_ids[6:]):
  trade    = all_trades[6 + i]
  asset_id = trade[5]
  pid      = asset_to_port.get(asset_id, random.choice(port_ids))
  stype    = random.choice(strat_types)
  dt       = fake.date_time_between(start_date='-2y', end_date='-1m')
  gen_strategies.append((16007+i, f"{stype} {i+1}", stype, str(dt),
                          random.choice(strat_params),
                          random.choice(['active','active','inactive']),
                          tid, pid))
all_strategies = persona_strategies + gen_strategies
strategy_ids   = [s[0] for s in all_strategies]

print("INSERT INTO Strategy (strategy_id, strategy_name, strategy_type, created_at, parameter, status, trade_strat, port_strat) VALUES")
for idx, s in enumerate(all_strategies):
  comma = "," if idx < len(all_strategies) - 1 else ";"
  print(f"  ({s[0]}, '{s[1]}', '{s[2]}', '{s[3]}', '{s[4]}', '{s[5]}', {s[6]}, {s[7]}){comma}")

# risk metrics
persona_risk = [
  (17001, 1.42, 0.18, 0.11, '2026-04-10 16:00:00', 16001),
  (17002, 1.18, 0.14, 0.08, '2026-04-10 16:00:00', 16002),
  (17003, 1.56, 0.22, 0.13, '2026-04-10 16:00:00', 16003),
  (17004, 0.62, 0.10, 0.05, '2026-04-10 16:00:00', 16004),
  (17005, 0.74, 0.12, 0.06, '2026-04-10 16:00:00', 16005),
  (17006, 0.68, 0.09, 0.04, '2026-04-10 16:00:00', 16006),
]
print("INSERT INTO RiskMetric (riskmetric_id, sharpe_ratio, volatility, drawdown, calculated_at, risk_strat) VALUES")
gen_risk = []
for i, sid in enumerate(strategy_ids[6:]):
  dt = fake.date_time_between(start_date='-1m', end_date='now')
  gen_risk.append((17007+i, round(random.uniform(0.3,2.2),2),
                   round(random.uniform(0.05,0.35),2), round(random.uniform(0.02,0.20),2),
                   str(dt), sid))
all_risk = persona_risk + gen_risk
for idx, r in enumerate(all_risk):
  comma = "," if idx < len(all_risk) - 1 else ";"
  print(f"  ({r[0]}, {r[1]}, {r[2]}, {r[3]}, '{r[4]}', {r[5]}){comma}")

# performance records
persona_perf = [
  (18001, 642310.55, 125430.80,  8450.25, '2026-04-10 10:20:09', 16001),
  (18002, 518904.20,  84210.65,  3125.40, '2026-04-10 01:15:12', 16002),
  (18003, 326305.60,  56320.10,  4278.90, '2026-04-10 06:29:11', 16003),
  (18004, 124000.00,  12040.10,  -950.75, '2026-04-10 04:01:00', 16004),
  (18005, 132500.55,   8400.45,   220.30, '2026-04-10 02:08:34', 16005),
  (18006, 113299.57,   2924.12,   101.22, '2026-04-10 11:12:59', 16006),
]
gen_perf = []
for i, sid in enumerate(strategy_ids[6:]):
  dt = fake.date_time_between(start_date='-1m', end_date='now')
  gen_perf.append((18007+i, round(random.uniform(50000,2000000),2),
                   round(random.uniform(-10000,200000),2), round(random.uniform(-5000,10000),2),
                   str(dt), sid))
all_perf = persona_perf + gen_perf

print("INSERT INTO PerformanceRecord (performance_id, port_value, cumulative_PNL, daily_PNL, record_date, strat_perf) VALUES")
for idx, p in enumerate(all_perf):
  comma = "," if idx < len(all_perf) - 1 else ";"
  print(f"  ({p[0]}, {p[1]}, {p[2]}, {p[3]}, '{p[4]}', {p[5]}){comma}")

# benchmarks
persona_bench = [
  (19001, 'Technology', 441.30, 'Nasdaq-100 Index', 'Equity Index', 'QQQ', 'Technology-heavy U.S. large-cap benchmark', 16001),
  (19002, 'Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            16002),
  (19003, 'Technology', 441.30, 'Nasdaq-100 Index', 'Equity Index', 'QQQ', 'Technology-heavy U.S. large-cap benchmark', 16003),
  (19004, 'Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            16004),
  (19005, 'Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            16005),
  (19006, 'Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            16006),
]
gen_bench = []
for i, sid in enumerate(strategy_ids[6:]):
  sector = random.choice(bench_sectors)
  bname, bticker, bval, btype = bench_data[sector]
  gen_bench.append((19007+i, sector, round(bval+random.uniform(-5,5),2),
                    bname, btype, bticker,
                    f"{sector} benchmark reference", sid))
all_bench = persona_bench + gen_bench

print("INSERT INTO Benchmark (benchmark_id, sector, current_value, benchmark_name, benchmark_type, ticker, description, strat_bench) VALUES")
for idx, b in enumerate(all_bench):
  comma = "," if idx < len(all_bench) - 1 else ";"
  print(f"  ({b[0]}, '{b[1]}', {b[2]}, '{b[3]}', '{b[4]}', '{b[5]}', '{b[6]}', {b[7]}){comma}")

# To run:
# cd database-files && python generate_mock_data.py > 03-mock-data.sql
