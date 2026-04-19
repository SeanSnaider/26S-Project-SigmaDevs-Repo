-- Database: PortIQ (DDL)

DROP DATABASE IF EXISTS PortIQ;
CREATE DATABASE IF NOT EXISTS PortIQ;
USE PortIQ;

CREATE TABLE if not exists Users(
    first_name varchar(100),
    last_name varchar(100),
    username varchar (50) NOT NULL Unique,
    email varchar (50) NOT NULL Unique,
    passwordHash VARBINARY(256) NOT NULL,
    birth_date DATETIME,
    is_encrypted BOOLEAN NOT NULL default false,
    userID int PRIMARY KEY
);
CREATE unique index idx_email on Users(email);

CREATE Table if not exists DailySummary (
    generated_at DATETIME,
    summary_date DATETIME,
    summary TEXT,
    summaryId int PRIMARY KEY,
    user_id int NOT NULL,
    CONSTRAINT user_summary
        FOREIGN KEY (user_id) REFERENCES Users(userID) 
        ON DELETE CASCADE
);

CREATE TABLE if not exists Action (
    action_type VARCHAR(50),
    date DATETIME,
    action_id INT PRIMARY KEY,
    user_id int NOT NULL,
    CONSTRAINT user_action
                          FOREIGN KEY (user_id) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE if not exists Role (
    name VARCHAR(50),
    RoleID INT PRIMARY KEY auto_increment,
    user_id int NOT NULL,
    CONSTRAINT user_role
                          FOREIGN KEY (user_id) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE if not exists Permission (
    Can_Read BOOLEAN,
    Can_Write BOOLEAN,
    Can_CREATE BOOLEAN,
    table_id INT,
    permission_id INT PRIMARY KEY,
    role_id INT NOT NULL,
    CONSTRAINT role_permission
        FOREIGN KEY (role_id) REFERENCES Role(RoleID)
        ON DELETE CASCADE
);

CREATE TABLE if not exists Customer (
    name VARCHAR(50),
    customer_id INT PRIMARY KEY,
    role_id INT NOT NULL,
    CONSTRAINT role_customers
                          FOREIGN KEY (role_id) REFERENCES Role(RoleID)
                          ON DELETE CASCADE
);

CREATE TABLE if not exists ChatSession (
    status VARCHAR(50),
    messages TEXT,
    session_id INT PRIMARY KEY,
    user_id int NOT NULL,
    CONSTRAINT user_session
                          FOREIGN KEY (user_id) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE if not exists Dataset(
    name VARCHAR(50),
    type VARCHAR(50),
    dataset_id INT PRIMARY KEY auto_increment,
    user_id int NOT NULL,
    CONSTRAINT user_dataset
                          FOREIGN KEY (user_id) REFERENCES Users(userID) ON DELETE CASCADE
);


CREATE TABLE if not exists DataCleaningMethod(
    method_order INT,
    parameter TEXT,
    method_type VARCHAR(50),
    method_id INT PRIMARY KEY,
    CleaningDataSet INT NOT NULL ,
    CONSTRAINT dataset_clean
        FOREIGN KEY (CleaningDataSet) REFERENCES Dataset(dataset_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists Visualization(
    title VARCHAR(50),
    chart_type VARCHAR(50),
    visualization_id INT PRIMARY KEY,
    VizDataSet INT NOT NULL ,
    CONSTRAINT viz_dataset
        FOREIGN KEY (VizDataSet) REFERENCES Dataset(dataset_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists DashBoard(
    title VARCHAR(50),
    visibility BOOLEAN,
    dashboard_id INT PRIMARY KEY,
    VizDash INT NOT NULL ,
    CONSTRAINT viz_dashboard
        FOREIGN KEY (VizDash) REFERENCES Visualization(visualization_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists DashboardLayout(
    name VARCHAR(50),
    source VARCHAR(50),
    layout_id INT PRIMARY KEY,
    layout_dash INT NOT NULL,
    CONSTRAINT layout_dashboard
        FOREIGN KEY (layout_dash) REFERENCES DashBoard(dashboard_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists Portfolio(
    portfolio_name VARCHAR(50),
    created_at DATETIME,
    total_value INT,
    confidence VARCHAR(50),
    currency VARCHAR(50),
    portfolio_id INT PRIMARY KEY,
    user_id int NOT NULL,
    CONSTRAINT user_port
        FOREIGN KEY (user_id) REFERENCES Users(userID) ON DELETE CASCADE
);


CREATE TABLE if not exists PortfolioSnapshot (
    snapshot_date DATETIME,
    insight_narrative TEXT,
    daily_change_pct FLOAT,
    ttlv_value FLOAT,
    snapshot_id INT PRIMARY KEY,
    SessionID int NOT NULL UNIQUE,
    port_id INT NOT NULL,
    CONSTRAINT port_snap
            FOREIGN KEY (port_id) REFERENCES Portfolio(portfolio_id)
            ON DELETE CASCADE
);

CREATE TABLE if not exists StockPosition(
    avg_cost FLOAT,
    unrealized_PNL FLOAT,
    price_target FLOAT,
    acquired_date DATETIME,
    market_value FLOAT,
    qty_held FLOAT,
    position_id INT PRIMARY KEY,
    port_id INT NOT NULL,
    CONSTRAINT prot_pos
        FOREIGN KEY (port_id) REFERENCES Portfolio(portfolio_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists Asset(
    asset_type VARCHAR(50),
    ticker VARCHAR(50),
    total_market FLOAT,
    asset_name VARCHAR(50),
    exchange VARCHAR(50),
    asset_id INT PRIMARY KEY,
    pos_id INT UNIQUE,
    CONSTRAINT pos_asset
        FOREIGN KEY (pos_id) REFERENCES StockPosition(position_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists AnalystRating(
    rating INT,
    rating_date DATETIME,
    analyst_firm VARCHAR(50),
    rate_id INT PRIMARY KEY,
    asset_rating INT NOT NULL,
    CONSTRAINT assetanalyst
        FOREIGN KEY (asset_rating) REFERENCES Asset(asset_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists Trade (
    trade_type VARCHAR(50),
    trade_date DATETIME,
    quantity FLOAT,
    price Decimal(15,2),
    trade_id INT PRIMARY KEY,
    trade_asset INT NOT NULL,
    CONSTRAINT trade_asset
        FOREIGN KEY (trade_asset) REFERENCES Asset(asset_id)
        ON DELETE CASCADE
);

Create Table if not exists Strategy(
    strategy_name VARCHAR(50),
    strategy_type VARCHAR(50),
    created_at DATETIME,
    parameter VARCHAR(50),
    status VARCHAR(50),
    strategy_id INT PRIMARY KEY,
    trade_strat INT NOT NULL,
       CONSTRAINT trade_strat
        FOREIGN KEY (trade_strat) REFERENCES Trade(trade_id)
        ON DELETE CASCADE,
    port_strat INT NOT NULL,
    CONSTRAINT port_strat
        FOREIGN KEY (port_strat) REFERENCES Portfolio(portfolio_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists RiskMetric(
    sharpe_ratio FLOAT,
    volatility FLOAT,
    drawdown FLOAT,
    calculated_at DATETIME,
    riskmetric_id INT PRIMARY KEY,
    risk_strat INT NOT NULL,
    CONSTRAINT risk_strat
                       FOREIGN KEY (risk_strat) REFERENCES Strategy(strategy_id)
                       ON DELETE CASCADE
);

CREATE TABLE if not exists PerformanceRecord(
    port_value FLOAT,
    cumulative_PNL FLOAT,
    daily_PNL FLOAT,
    record_date DATETIME,
    performance_id INT PRIMARY KEY,
    strat_perf INT NOT NULL,
    CONSTRAINT strat_perf
                       FOREIGN KEY (strat_perf) REFERENCES Strategy(strategy_id)
                       ON DELETE CASCADE
);

CREATE TABLE if not exists Benchmark(
    sector VARCHAR(50),
    current_value Decimal(15,2),
    benchmark_name VARCHAR(50),
    benchmark_type VARCHAR(50),
    ticker VARCHAR(50),
    description text,
    benchmark_id INT PRIMARY KEY,
    strat_bench INT NOT NULL,
    CONSTRAINT strat_bench
                       FOREIGN KEY (strat_bench) REFERENCES Strategy(strategy_id)
                       ON DELETE CASCADE
);
