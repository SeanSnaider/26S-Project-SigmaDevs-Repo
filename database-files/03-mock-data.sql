-- Mock Data for PortIQ
USE PortIQ;

-- ============================================================
-- Users
-- ============================================================
INSERT INTO Users (first_name, last_name, username, email, passwordHash, birth_date, userID) VALUES
('James',   'Mitchell', 'jmitchell', 'j.mitchell@portiq.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', '1975-03-12', 1),
('Sarah',   'Chen',     'schen',     's.chen@portiq.com',     'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '1988-07-22', 2),
('Michael', 'Torres',   'mtorres',   'm.torres@portiq.com',   'b3a8e0e1f9ab1bfe3a36f231f676f78bb28a2028c6ee72dd7e0e65db0a5f2c25', '1982-11-05', 3),
('Emily',   'Watson',   'ewatson',   'e.watson@portiq.com',   '6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b', '1990-04-18', 4),
('David',   'Park',     'dpark',     'd.park@portiq.com',     'd4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35', '1995-09-30', 5);

-- ============================================================
-- Role  (auto_increment on RoleID — specify explicitly so FKs align)
-- ============================================================
INSERT INTO Role (RoleID, name, user_id) VALUES
(1, 'CIO',               1),
(2, 'Senior Analyst',    2),
(3, 'Portfolio Manager', 3),
(4, 'Risk Analyst',      4),
(5, 'Data Analyst',      5);

-- ============================================================
-- Permission  (Can_Read, Can_Write, Can_CREATE, table_id, permission_id, role_id)
-- ============================================================
INSERT INTO Permission VALUES
(1, 1, 1,  1,  1, 1),
(1, 1, 1,  2,  2, 1),
(1, 1, 1,  3,  3, 1),
(1, 1, 0,  4,  4, 2),
(1, 1, 0,  5,  5, 2),
(1, 0, 0,  6,  6, 3),
(1, 1, 1,  7,  7, 3),
(1, 0, 0,  8,  8, 4),
(1, 0, 0,  9,  9, 4),
(1, 1, 0, 10, 10, 5);

-- ============================================================
-- Customer  (name, customer_id, role_id)
-- ============================================================
INSERT INTO Customer VALUES
('Blackrock Capital',     1, 1),
('Vanguard Group',        2, 2),
('Fidelity Investments',  3, 3),
('State Street Corp',     4, 4),
('T. Rowe Price',         5, 5);

-- ============================================================
-- DailySummary  (generated_at, summary_date, summary, summaryId, user_id)
-- ============================================================
INSERT INTO DailySummary VALUES
('2026-04-18 08:00:00', '2026-04-18', 'Market showed strong recovery driven by the tech sector. Growth portfolio up 2.3% led by NVDA and MSFT. Recommend holding current positions.', 1, 1),
('2026-04-17 08:00:00', '2026-04-17', 'Mixed session as inflation data came in slightly above expectations. Bond allocation acted as an effective hedge. No position changes warranted.', 2, 1),
('2026-04-18 08:00:00', '2026-04-18', 'Tech sector outperformed broader market. AAPL and META both up over 3%. Reviewing position sizing for Q2 rebalance.', 3, 2),
('2026-04-18 08:00:00', '2026-04-18', 'Conservative positioning paid off as small-caps sold off. Portfolio outperformed benchmark by 1.2% on a risk-adjusted basis.', 4, 3),
('2026-04-18 08:00:00', '2026-04-18', 'New data pipeline completed successfully. Updated visualizations are ready for CIO review on the executive dashboard.', 5, 5);

-- ============================================================
-- Action  (action_type, date, action_id, user_id)
-- ============================================================
INSERT INTO Action VALUES
('LOGIN',            '2026-04-18 09:00:00',  1, 1),
('VIEW_PORTFOLIO',   '2026-04-18 09:05:00',  2, 1),
('GENERATE_REPORT',  '2026-04-18 09:20:00',  3, 1),
('LOGIN',            '2026-04-18 09:10:00',  4, 2),
('GENERATE_REPORT',  '2026-04-18 09:30:00',  5, 2),
('LOGIN',            '2026-04-18 08:45:00',  6, 3),
('EXECUTE_TRADE',    '2026-04-18 10:00:00',  7, 3),
('VIEW_PORTFOLIO',   '2026-04-18 10:15:00',  8, 3),
('LOGIN',            '2026-04-18 09:30:00',  9, 4),
('RUN_RISK_MODEL',   '2026-04-18 09:45:00', 10, 4),
('LOGIN',            '2026-04-18 08:30:00', 11, 5),
('UPLOAD_DATASET',   '2026-04-18 08:50:00', 12, 5),
('LOAD_DATASET',     '2026-04-18 08:55:00', 13, 5),
('DEPLOYED_PIPELINE','2026-04-18 11:00:00', 14, 1);

-- ============================================================
-- ChatSession  (status, messages, session_id, user_id)
-- ============================================================
INSERT INTO ChatSession VALUES
('active',  'User: What is my portfolio performance today?\nAI: Your Growth Portfolio is up 2.3% today, driven by NVDA (+4.1%) and MSFT (+2.8%). Total value is $2,916,750.',  1, 1),
('closed',  'User: Show me tech sector exposure.\nAI: You currently have 45% allocation in the tech sector across all portfolios, with NASDAQ-listed equities making up the majority.',  2, 1),
('active',  'User: Analyze the NVDA position.\nAI: NVDA is your top performer with 34% unrealized gains. Current market value is $875K with a strong buy rating from Goldman Sachs.',    3, 2),
('closed',  'User: Run risk assessment for Q2.\nAI: Current portfolio Sharpe ratio is 1.42, within your target range. Max drawdown sits at -12%, well under the -20% threshold.',        4, 3),
('active',  'User: Generate allocation visualization.\nAI: The portfolio allocation pie chart has been updated on the CIO Executive Dashboard. Refresh to view the latest snapshot.',       5, 5);

-- ============================================================
-- Dataset  (name, type, user_id) — dataset_id auto_increment → 1-5
-- ============================================================
INSERT INTO Dataset (name, type, user_id) VALUES
('Q1 2026 Portfolio Data',    'CSV',     1),
('Tech Sector Analysis',      'JSON',    2),
('Risk Assessment Q1 2026',   'CSV',     4),
('Market Benchmark Data',     'CSV',     3),
('Performance History 2025',  'PARQUET', 5);

-- ============================================================
-- DataCleaningMethod  (method_order, parameter, method_type, method_id, CleaningDataSet)
-- ============================================================
INSERT INTO DataCleaningMethod VALUES
(1, '{"fill_method": "forward_fill"}',          'fill_missing',    1, 1),
(2, '{"threshold": 3.0}',                       'remove_outliers', 2, 1),
(1, '{"columns": ["price","volume"]}',           'normalize',       3, 2),
(1, '{"fill_method": "column_mean"}',           'fill_missing',    4, 3),
(2, '{"window": 5, "min_periods": 1}',          'rolling_average', 5, 4);

-- ============================================================
-- Visualization  (title, chart_type, visualization_id, VizDataSet)
-- ============================================================
INSERT INTO Visualization VALUES
('Portfolio Allocation',    'pie_chart',    1, 1),
('Performance Over Time',   'line_chart',   2, 1),
('Sector Exposure',         'bar_chart',    3, 2),
('Risk vs Return',          'scatter_plot', 4, 3),
('Benchmark Comparison',    'line_chart',   5, 4);

-- ============================================================
-- DashBoard  (title, visibility, dashboard_id, VizDash)
-- ============================================================
INSERT INTO DashBoard VALUES
('CIO Executive Dashboard',   1, 1, 1),
('Performance Dashboard',     1, 2, 2),
('Sector Analysis Dashboard', 1, 3, 3),
('Risk Dashboard',            0, 4, 4),
('Benchmark Dashboard',       1, 5, 5);

-- ============================================================
-- DashboardLayout  (name, source, layout_id, layout_dash)
-- ============================================================
INSERT INTO DashboardLayout VALUES
('Full Width',     'grid_12',   1, 1),
('Split View',     'grid_6_6',  2, 2),
('Triple Column',  'grid_4_4_4',3, 3),
('Left Heavy',     'grid_8_4',  4, 4),
('Standard',       'grid_12',   5, 5);

-- ============================================================
-- Portfolio  (portfolio_name, created_at, total_value, confidence, currency, portfolio_id, user_id)
-- ============================================================
INSERT INTO Portfolio VALUES
('Growth Portfolio',   '2024-01-15', 2850000, 'High',   'USD', 1, 1),
('Tech Focus Fund',    '2024-03-01', 1200000, 'High',   'USD', 2, 2),
('Balanced Growth',    '2024-01-15', 3500000, 'Medium', 'USD', 3, 3),
('Conservative Income','2024-06-01',  950000, 'Low',    'USD', 4, 4);

-- ============================================================
-- PortfolioSnapshot (snapshot_date, insight_narrative, daily_change_pct, ttlv_value, snapshot_id, SessionID, port_id)
-- ============================================================
INSERT INTO PortfolioSnapshot VALUES
('2026-04-18 16:00:00', 'Strong performance driven by NVDA and MSFT. Tech overweight is paying off in the current risk-on environment.',          2.30,  2916750.00, 1, 101, 1),
('2026-04-17 16:00:00', 'Slight pullback as rate concerns resurfaced. Holding all positions — fundamentals remain intact for the thesis.',        -0.80, 2847150.00, 2, 102, 1),
('2026-04-18 16:00:00', 'Tech positions outperforming broader market. AAPL up 3.1%, META up 4.2%. Considering trimming META near resistance.',    1.90,  1222800.00, 3, 103, 2),
('2026-04-18 16:00:00', 'Balanced approach limiting downside. Fixed income allocation providing stability during equity volatility.',              0.40,  3513800.00, 4, 104, 3),
('2026-04-18 16:00:00', 'Dividend stocks holding steady with low volatility. AT&T and VZ generating expected yield. XOM benefiting from oil.',   0.20,   952900.00, 5, 105, 4);

-- ============================================================
-- StockPosition (avg_cost, unrealized_PNL, price_target, acquired_date, market_value, qty_held, position_id, port_id)
-- ============================================================
INSERT INTO StockPosition VALUES
-- Growth Portfolio (port_id=1)
(485.50,  45250.00,  950.00, '2024-03-15',  875000.00,  800.00,  1, 1),  -- NVDA
(320.75,  38400.00,  480.00, '2024-02-10',  680000.00, 1500.00,  2, 1),  -- MSFT
(155.20,  22800.00,  220.00, '2024-01-20',  425000.00, 2400.00,  3, 1),  -- AMZN
(128.50,  18500.00,  185.00, '2024-01-15',  355000.00, 2000.00,  4, 1),  -- GOOGL
-- Tech Focus Fund (port_id=2)
(175.30,  28900.00,  230.00, '2024-03-01',  425000.00, 2000.00,  5, 2),  -- AAPL
(420.00,  35000.00,  580.00, '2024-04-01',  385000.00,  700.00,  6, 2),  -- META
(210.75,  15600.00,  280.00, '2024-05-15',  215000.00,  800.00,  7, 2),  -- TSLA
-- Balanced Growth (port_id=3)
(440.20,  52000.00,  550.00, '2024-01-15',  875000.00, 1800.00,  8, 3),  -- SPY
(345.80,  28500.00,  420.00, '2024-02-01',  620000.00, 1600.00,  9, 3),  -- BRK.B
(155.40,  12800.00,  185.00, '2024-03-01',  310000.00, 1800.00, 10, 3),  -- JNJ
(142.60,   8900.00,  165.00, '2024-01-20',  480000.00, 3000.00, 11, 3),  -- PG
-- Conservative Income (port_id=4)
( 19.50,   3200.00,   22.00, '2024-06-01',  180000.00, 8500.00, 12, 4),  -- T
( 41.20,   5800.00,   48.00, '2024-06-15',  320000.00, 7200.00, 13, 4),  -- VZ
(105.30,  12500.00,  125.00, '2024-07-01',  425000.00, 3800.00, 14, 4);  -- XOM

-- ============================================================
-- Asset (asset_type, ticker, total_merket, asset_name, exchange, asset_id, pos_id)
-- pos_id is UNIQUE — one asset per position
-- ============================================================
INSERT INTO Asset VALUES
('Equity', 'NVDA',  2850000000000.00, 'NVIDIA Corporation',          'NASDAQ',  1,  1),
('Equity', 'MSFT',  3200000000000.00, 'Microsoft Corporation',        'NASDAQ',  2,  2),
('Equity', 'AMZN',  2100000000000.00, 'Amazon.com Inc',               'NASDAQ',  3,  3),
('Equity', 'GOOGL', 2400000000000.00, 'Alphabet Inc Class A',         'NASDAQ',  4,  4),
('Equity', 'AAPL',  3500000000000.00, 'Apple Inc',                    'NASDAQ',  5,  5),
('Equity', 'META',  1300000000000.00, 'Meta Platforms Inc',           'NASDAQ',  6,  6),
('Equity', 'TSLA',   850000000000.00, 'Tesla Inc',                    'NASDAQ',  7,  7),
('ETF',    'SPY',    450000000000.00, 'SPDR S&P 500 ETF Trust',       'NYSE',    8,  8),
('Equity', 'BRK.B',  780000000000.00, 'Berkshire Hathaway Class B',   'NYSE',    9,  9),
('Equity', 'JNJ',    385000000000.00, 'Johnson & Johnson',            'NYSE',   10, 10),
('Equity', 'PG',     365000000000.00, 'Procter & Gamble Co',          'NYSE',   11, 11),
('Equity', 'T',      125000000000.00, 'AT&T Inc',                     'NYSE',   12, 12),
('Equity', 'VZ',     145000000000.00, 'Verizon Communications Inc',   'NYSE',   13, 13),
('Equity', 'XOM',    520000000000.00, 'Exxon Mobil Corporation',      'NYSE',   14, 14);

-- ============================================================
-- AnalystRating (rating, rating_date, analyst_firm, rate_id, asset_rating)
-- rating scale: 1=Strong Sell, 2=Underperform, 3=Hold, 4=Buy, 5=Strong Buy
-- ============================================================
INSERT INTO AnalystRating VALUES
(5, '2026-04-15', 'Goldman Sachs',    1,  1),
(5, '2026-04-10', 'Morgan Stanley',   2,  2),
(4, '2026-04-12', 'JP Morgan',        3,  3),
(4, '2026-04-08', 'Bank of America',  4,  4),
(5, '2026-04-15', 'Wells Fargo',      5,  5),
(4, '2026-04-11', 'Goldman Sachs',    6,  6),
(3, '2026-04-14', 'Morgan Stanley',   7,  7),
(4, '2026-04-10', 'Vanguard Research',8,  8),
(5, '2026-04-09', 'JP Morgan',        9,  9),
(3, '2026-04-07', 'Bank of America', 10, 10),
(4, '2026-04-06', 'Goldman Sachs',   11, 11),
(2, '2026-04-15', 'Morgan Stanley',  12, 12),
(3, '2026-04-12', 'JP Morgan',       13, 13),
(4, '2026-04-10', 'Wells Fargo',     14, 14);

-- ============================================================
-- Trade (trade_type, trade_date, quantity, price, trade_id, trade_asset)
-- ============================================================
INSERT INTO Trade VALUES
('BUY',  '2024-03-15', 800.00,  485.50,  1,  1),   -- NVDA initial
('BUY',  '2024-02-10', 1500.00, 320.75,  2,  2),   -- MSFT initial
('BUY',  '2024-01-20', 2400.00, 155.20,  3,  3),   -- AMZN initial
('BUY',  '2024-01-15', 2000.00, 128.50,  4,  4),   -- GOOGL initial
('BUY',  '2024-03-01', 2000.00, 175.30,  5,  5),   -- AAPL initial
('BUY',  '2024-04-01',  700.00, 420.00,  6,  6),   -- META initial
('BUY',  '2024-05-15',  800.00, 210.75,  7,  7),   -- TSLA initial
('BUY',  '2024-01-15', 1800.00, 440.20,  8,  8),   -- SPY initial
('BUY',  '2024-02-01', 1600.00, 345.80,  9,  9),   -- BRK.B initial
('BUY',  '2024-03-01', 1800.00, 155.40, 10, 10),   -- JNJ initial
('BUY',  '2024-01-20', 3000.00, 142.60, 11, 11),   -- PG initial
('BUY',  '2024-06-01', 8500.00,  19.50, 12, 12),   -- T initial
('BUY',  '2024-06-15', 7200.00,  41.20, 13, 13),   -- VZ initial
('BUY',  '2024-07-01', 3800.00, 105.30, 14, 14),   -- XOM initial
('SELL', '2026-03-20',  100.00, 875.00, 15,  1),   -- NVDA partial trim
('BUY',  '2026-04-05',  200.00, 820.00, 16,  1),   -- NVDA add on dip
('SELL', '2026-04-10',   50.00, 268.00, 17,  7),   -- TSLA reduce
('BUY',  '2026-04-15',  500.00, 198.50, 18,  5);   -- AAPL add

-- ============================================================
-- Strategy (strategy_name, strategy_type, created_at, parameter, status, strategy_id, trade_strat, port_strat)
-- ============================================================
INSERT INTO Strategy VALUES
('NVDA Momentum Play',   'Momentum',     '2024-03-15', '{"lookback_days":90,"entry_threshold":0.15}', 'active', 1,  1, 1),
('MSFT Growth Core',     'Growth',       '2024-02-10', '{"target_pe":35,"revenue_growth":0.12}',      'active', 2,  2, 1),
('SPY Hedge Overlay',    'Hedging',      '2024-01-15', '{"beta":1.2,"hedge_ratio":0.30}',             'active', 3,  8, 3),
('Income Value Play',    'Value',        '2024-06-01', '{"min_div_yield":0.05,"max_payout":0.60}',    'active', 4, 12, 4),
('AAPL Core Long',       'Growth',       '2024-03-01', '{"target_pe":28,"add_threshold":0.10}',       'active', 5,  5, 2),
('Balanced Alpha',       'Multi-Factor', '2024-01-15', '{"alpha_target":0.02,"max_volatility":0.12}', 'active', 6,  9, 3);

-- ============================================================
-- RiskMetric (sharpe_ratio, volatility, drawdown, calculated_at, riskmetric_id, risk_strat)
-- ============================================================
INSERT INTO RiskMetric VALUES
(1.85, 0.32, -0.12, '2026-04-18', 1, 1),
(1.62, 0.28, -0.09, '2026-04-18', 2, 2),
(0.95, 0.18, -0.07, '2026-04-18', 3, 3),
(0.72, 0.12, -0.04, '2026-04-18', 4, 4),
(1.43, 0.25, -0.11, '2026-04-18', 5, 5),
(1.28, 0.20, -0.08, '2026-04-18', 6, 6);

-- ============================================================
-- PerformanceRecord (port_value, cumulative_PNL, daily_PNL, record_date, performance_id, strat_perf)
-- ============================================================
INSERT INTO PerformanceRecord VALUES
( 875000.00,  45250.00, 2012.50, '2026-04-18', 1, 1),
( 680000.00,  38400.00, 1088.00, '2026-04-18', 2, 2),
(3513800.00, 102200.00, 1405.52, '2026-04-18', 3, 3),
( 952900.00,  21500.00,  190.58, '2026-04-18', 4, 4),
( 425000.00,  28900.00,  807.50, '2026-04-18', 5, 5),
(3513800.00,  98400.00, 1054.14, '2026-04-17', 6, 6);

-- ============================================================
-- Benchmark (sector, current_value, benchmark_name, benchmark_type, ticker, description, benchmark_id, strat_bench)
-- ============================================================
INSERT INTO Benchmark VALUES
('Technology',    21850.25, 'NASDAQ Composite',       'Market Index', 'COMP',    'Technology-heavy composite tracking 3,000+ listed stocks',      1, 1),
('Technology',    21850.25, 'NASDAQ 100',              'Market Index', 'NDX',     'Top 100 non-financial NASDAQ-listed companies by market cap',    2, 2),
('Broad Market',   5248.50, 'S&P 500',                 'Market Index', 'SPX',     'Primary benchmark for US large-cap equity performance',          3, 3),
('Utilities',       998.75, 'Utilities Select Sector', 'Sector ETF',   'XLU',     'Tracks the utilities sector of the S&P 500 index',              4, 4),
('Technology',    21850.25, 'S&P 500 Tech Sector',     'Sector Index', 'SPLRCT',  'Technology sector sub-index of the S&P 500',                    5, 5),
('Broad Market',   5248.50, 'Russell 1000',             'Market Index', 'RUI',     'Tracks the 1,000 largest US publicly traded companies',         6, 6);
