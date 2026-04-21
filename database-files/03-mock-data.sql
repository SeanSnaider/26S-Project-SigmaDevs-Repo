USE PortIQ;

-- =========================================================
-- PortIQ mock-data.sql
-- Seed data aligned to the final PortIQ schema and the four
-- project personas: Andrew Rock, John Data, Katrina Williams,
-- and Jane Doe.
--
-- This file is intentionally written in foreign-key-safe order.
-- It also clears existing rows first so it can be re-run.
-- =========================================================

SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM Benchmark;
DELETE FROM PerformanceRecord;
DELETE FROM RiskMetric;
DELETE FROM Strategy;
DELETE FROM Trade;
DELETE FROM AnalystRating;
DELETE FROM Asset;
DELETE FROM StockPosition;
DELETE FROM PortfolioSnapshot;
DELETE FROM Portfolio;
DELETE FROM DashboardLayout;
DELETE FROM DashBoard;
DELETE FROM Visualization;
DELETE FROM DataCleaningMethod;
DELETE FROM Dataset;
DELETE FROM ChatSession;
DELETE FROM Customer;
DELETE FROM Permission;
DELETE FROM Role;
DELETE FROM Action;
DELETE FROM DailySummary;
DELETE FROM Users;

SET FOREIGN_KEY_CHECKS = 1;

-- =========================================================
-- 1. USERS
-- =========================================================
INSERT INTO Users (first_name, last_name, username, email, passwordHash, birth_date, userID)
VALUES
('Andrew',  'Rock',      'andrewrock',  'andrew.rock@portiq.com',    'hashed_pw_andrew',  '1993-06-15 00:00:00', 1),
('John',    'Data',      'johndata',    'john.data@portiq.com',      'hashed_pw_john',    '1980-03-12 00:00:00', 2),
('Katrina', 'Williams',  'kwilliams',   'katrina.williams@portiq.com','hashed_pw_katrina','1985-09-21 00:00:00', 3),
('Jane',    'Doe',       'janedoe',     'jane.doe@portiq.com',       'hashed_pw_jane',    '1998-11-08 00:00:00', 4);

-- =========================================================
-- 2. ROLE / PERMISSION / ADMIN SUPPORT DATA
-- =========================================================
INSERT INTO Role (name, RoleID, user_id)
VALUES
('Quantitative Trader', 101, 1),
('Data Analyst',        102, 2),
('Chief Information Officer', 103, 3),
('Beginner Investor',   104, 4);

INSERT INTO Permission (Can_Read, Can_Write, Can_CREATE, table_id, permission_id, role_id)
VALUES
(TRUE,  TRUE,  TRUE,  1, 1001, 101),
(TRUE,  TRUE,  TRUE,  2, 1002, 102),
(TRUE,  TRUE,  TRUE,  3, 1003, 103),
(TRUE,  FALSE, FALSE, 4, 1004, 104);

INSERT INTO Customer (name, customer_id, role_id)
VALUES
('Andrew Rock', 2001, 101),
('Jane Doe',    2002, 104);

INSERT INTO Action (action_type, date, action_id, user_id)
VALUES
('Uploaded trade log',        '2026-04-10 09:15:00', 3001, 1),
('Ran cleaning pipeline',     '2026-04-10 10:05:00', 3002, 2),
('Updated permissions',       '2026-04-10 10:45:00', 3003, 3),
('Viewed market summary',     '2026-04-10 18:30:00', 3004, 4);

INSERT INTO DailySummary (generated_at, summary_date, summary, summaryId, user_id)
VALUES
('2026-04-10 18:00:00', '2026-04-10 00:00:00', 'Portfolio gained on strength in large-cap tech and broad market momentum.', 4001, 1),
('2026-04-10 18:05:00', '2026-04-10 00:00:00', 'ETL pipeline completed and all dataset validation checks passed.', 4002, 2),
('2026-04-10 18:10:00', '2026-04-10 00:00:00', 'Security review completed for role and permission changes.', 4003, 3),
('2026-04-10 18:15:00', '2026-04-10 00:00:00', 'Beginner dashboard summary generated with top movers and benchmark comparison.', 4004, 4);

INSERT INTO ChatSession (status, messages, session_id, user_id)
VALUES
('active',  'What moved my portfolio today?', 5001, 4),
('closed',  'Show me current portfolio P&L.', 5002, 1),
('closed',  'Summarize the recent portfolio risk exposure for Q1.', 5003, 3),
('closed',  'Are there any anomalies in the recent trade logs?', 5004, 3),
('closed',  'What permissions does the Data Analyst role currently have?', 5005, 3),
('closed',  'Which users have create permissions across all roles?', 5006, 3),
('closed',  'Generate a brief security audit summary for April.', 5007, 3),
('closed',  'What is the current total portfolio value across all users?', 5008, 3),
('closed',  'Identify any strategies with negative daily PNL.', 5009, 3),
('closed',  'Summarize system activity for April 10.', 5010, 3),
('closed',  'What datasets are currently managed by the Data Analyst?', 5011, 3),
('active',  'Are there any high-risk strategies that should be reviewed?', 5012, 3);

-- =========================================================
-- 3. JOHN DATA: DATASETS / CLEANING / VISUALIZATION / LAYOUT
-- =========================================================
INSERT INTO Dataset (dataset_id, name, type, user_id)
VALUES
(1001, 'Raw Trading Data',        'CSV',              2),
(1002, 'Cleaned Trading Data',    'Processed Table',  2),
(1003, 'Portfolio Dashboard Feed','Dashboard Source', 2),
(1004, 'Jane Beginner Feed',      'Dashboard Source', 2);

INSERT INTO DataCleaningMethod (method_order, parameter, method_type, method_id, CleaningDataSet)
VALUES
(1, 'drop_duplicates=true',                 'Duplicate Removal', 6001, 1001),
(2, 'remove_nulls=true',                    'Null Removal',      6002, 1001),
(3, 'standardize_ticker_format=true',       'Formatting',        6003, 1001),
(1, 'winsorize_outliers=0.01',              'Outlier Handling',  6004, 1002),
(2, 'normalize_numeric_fields=true',        'Normalization',     6005, 1002);

INSERT INTO Visualization (title, chart_type, visualization_id, VizDataSet)
VALUES
('Andrew Performance Trend', 'Line Chart', 7001, 1003),
('Andrew Asset Allocation',  'Pie Chart',  7002, 1003),
('John Dataset Quality',     'Bar Chart',  7003, 1002),
('Jane Portfolio Overview',  'Area Chart', 7004, 1004);

INSERT INTO DashBoard (title, visibility, dashboard_id, VizDash)
VALUES
('Andrew Trading Dashboard', TRUE, 8001, 7001),
('Andrew Allocation View',   TRUE, 8002, 7002),
('John Admin Dashboard',     TRUE, 8003, 7003),
('Jane Beginner Dashboard',  TRUE, 8004, 7004);

INSERT INTO DashboardLayout (name, source, layout_id, layout_dash)
VALUES
('Quant Trader Main Layout', 'Figma', 9001, 8001),
('Quant Trader Allocation Layout', 'Figma', 9002, 8002),
('Data Analyst Builder Layout',    'Figma', 9003, 8003),
('Beginner Guided Layout',         'Figma', 9004, 8004);

-- =========================================================
-- 4. PORTFOLIOS
-- =========================================================
INSERT INTO Portfolio (portfolio_name, created_at, total_value, confidence, currency, portfolio_id, user_id)
VALUES
('Andrew Main Portfolio',      '2026-01-01 09:00:00', 1487520, 'High',   'USD', 101, 1),
('Jane Beginner Portfolio',    '2026-02-01 10:00:00',  245800, 'Medium', 'USD', 102, 4);

INSERT INTO PortfolioSnapshot (snapshot_date, insight_narrative, daily_change_pct, ttlv_value, snapshot_id, SessionID, port_id)
VALUES
('2026-04-10 16:00:00', 'Andrew portfolio outperformed broad market on strength in tech holdings.',  0.84, 1487520.35, 11001, 5002, 101),
('2026-04-10 16:05:00', 'Jane portfolio showed moderate gains and tracked close to the S&P 500.',    0.31,  245800.12, 11002, 5001, 102);

-- =========================================================
-- 5. STOCK POSITIONS / ASSETS
-- =========================================================
INSERT INTO StockPosition (avg_cost, unrealized_PNL, price_target, acquired_date, market_value, qty_held, position_id, port_id)
VALUES
(180.50, 15200.75, 230.00, '2025-12-01 00:00:00', 106240.00, 500, 12001, 101),
(400.25,  8200.40, 460.00, '2025-11-15 00:00:00', 107167.50, 250, 12002, 101),
(650.10, 27550.90, 980.00, '2026-01-20 00:00:00', 270336.00, 300, 12003, 101),
(505.30,  4550.10, 560.00, '2026-02-10 00:00:00',  51824.00, 100, 12004, 101),
(195.00,  1400.00, 230.00, '2026-02-12 00:00:00',  21248.00, 100, 12005, 102),
(510.00,   824.00, 540.00, '2026-02-15 00:00:00',  10364.00,  20, 12006, 102);

INSERT INTO Asset (asset_type, ticker, total_market, asset_name, exchange, asset_id, pos_id)
VALUES
('Equity', 'AAPL', 2800000000000, 'Apple Inc.',                 'NASDAQ',   13001, 12001),
('Equity', 'MSFT', 3100000000000, 'Microsoft Corporation',      'NASDAQ',   13002, 12002),
('Equity', 'NVDA', 2200000000000, 'NVIDIA Corporation',         'NASDAQ',   13003, 12003),
('ETF',    'SPY',  550000000000,  'SPDR S&P 500 ETF Trust',     'NYSE Arca',13004, 12004),
('Equity', 'AAPL', 2800000000000, 'Apple Inc.',                 'NASDAQ',   13005, 12005),
('ETF',    'SPY',  550000000000,  'SPDR S&P 500 ETF Trust',     'NYSE Arca',13006, 12006);

INSERT INTO AnalystRating (rating, rating_date, analyst_firm, rate_id, asset_rating)
VALUES
(5, '2026-04-08 00:00:00', 'Goldman Sachs', 14001, 13001),
(4, '2026-04-08 00:00:00', 'Morgan Stanley', 14002, 13002),
(5, '2026-04-08 00:00:00', 'JPMorgan', 14003, 13003),
(4, '2026-04-08 00:00:00', 'Bank of America', 14004, 13004);

-- =========================================================
-- 6. TRADES / STRATEGIES / RISK / PERFORMANCE / BENCHMARKS
-- =========================================================
INSERT INTO Trade (trade_type, trade_date, quantity, price, trade_id, trade_asset)
VALUES
('BUY',  '2026-04-05 09:35:00', 100, 212.48, 15001, 13001),
('BUY',  '2026-04-04 10:15:00',  50, 428.67, 15002, 13002),
('BUY',  '2026-04-03 11:05:00',  80, 901.12, 15003, 13003),
('SELL', '2026-04-02 14:40:00',  25, 518.24, 15004, 13004),
('BUY',  '2026-04-06 09:50:00',  10, 212.48, 15005, 13005),
('BUY',  '2026-04-06 10:20:00',   5, 518.20, 15006, 13006);

INSERT INTO Strategy (strategy_name, strategy_type, created_at, parameter, status, strategy_id, trade_strat, port_strat)
VALUES
('Tech Momentum',       'Momentum',       '2026-01-10 09:00:00', 'lookback=30,stop_loss=0.03',     'active',   16001, 15001, 101),
('Mean Reversion',      'Mean Reversion', '2026-01-15 10:00:00', 'zscore=1.5,window=20',            'active',   16002, 15002, 101),
('AI Growth Rotation',  'Rotation',       '2026-02-01 09:30:00', 'rebalance=10,max_weight=0.35',    'active',   16003, 15003, 101),
('Legacy ETF Hedge',    'Hedging',        '2025-12-20 15:00:00', 'hedge_band=0.02,rebalance=weekly','inactive', 16004, 15004, 101),
('Beginner Core Growth','Long Only',      '2026-02-10 10:30:00', 'monthly_contrib=500',             'active',   16005, 15005, 102),
('Beginner Market ETF', 'Passive',        '2026-02-12 11:00:00', 'hold_forever=true',               'active',   16006, 15006, 102);

INSERT INTO RiskMetric (sharpe_ratio, volatility, drawdown, calculated_at, riskmetric_id, risk_strat)
VALUES
(1.42, 0.18, 0.11, '2026-04-10 16:00:00', 17001, 16001),
(1.18, 0.14, 0.08, '2026-04-10 16:00:00', 17002, 16002),
(1.56, 0.22, 0.13, '2026-04-10 16:00:00', 17003, 16003),
(0.62, 0.10, 0.05, '2026-04-10 16:00:00', 17004, 16004),
(0.74, 0.12, 0.06, '2026-04-10 16:00:00', 17005, 16005),
(0.68, 0.09, 0.04, '2026-04-10 16:00:00', 17006, 16006);

INSERT INTO PerformanceRecord (port_value, cumulative_PNL, daily_PNL, record_date, performance_id, strat_perf)
VALUES
(642310.55, 125430.80, 8450.25, '2026-04-10 10:20:09', 18001, 16001),
(518904.20,  84210.65, 3125.40, '2026-04-10 01:15:12', 18002, 16002),
(326305.60,  56320.10, 4278.90, '2026-04-10 06:29:11', 18003, 16003),
(124000.00,  12040.10, -950.75, '2026-04-10 04:01:00', 18004, 16004),
(132500.55,   8400.45,  220.30, '2026-04-10 02:08:34', 18005, 16005),
(113299.57,   2924.12,  101.22, '2026-04-10 11:12:59', 18006, 16006);

INSERT INTO Benchmark (sector, current_value, benchmark_name, benchmark_type, ticker, description, benchmark_id, strat_bench)
VALUES
('Technology', 441.30, 'Nasdaq-100 Index', 'Equity Index', 'QQQ', 'Technology-heavy U.S. large-cap benchmark', 19001, 16001),
('Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            19002, 16002),
('Technology', 441.30, 'Nasdaq-100 Index', 'Equity Index', 'QQQ', 'Technology-heavy U.S. large-cap benchmark', 19003, 16003),
('Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            19004, 16004),
('Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            19005, 16005),
('Market',     518.24, 'S&P 500 Index',    'Equity Index', 'SPY', 'Broad large-cap U.S. benchmark',            19006, 16006);

-- =========================================================
-- End of mock data
-- =========================================================
