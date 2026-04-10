-- 车辆定损APP数据库初始化脚本
-- 创建车型表
CREATE TABLE IF NOT EXISTS vehicles (
    id VARCHAR(50) PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    series VARCHAR(50) NOT NULL,
    year_range VARCHAR(50) NOT NULL,
    displacement VARCHAR(50),
    transmission VARCHAR(50),
    body_type VARCHAR(50),
    vin_prefix VARCHAR(20),
    vehicle_class VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建配件表
CREATE TABLE IF NOT EXISTS parts (
    id VARCHAR(50) PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    oe_number VARCHAR(50) NOT NULL,
    spec VARCHAR(100),
    applicable_brands VARCHAR(200),
    price FLOAT DEFAULT 0,
    unit VARCHAR(20),
    notes TEXT,
    is_safety_part BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建车型-配件关联表
CREATE TABLE IF NOT EXISTS vehicle_parts (
    id VARCHAR(50) PRIMARY KEY,
    vehicle_id VARCHAR(50) NOT NULL,
    part_id VARCHAR(50) NOT NULL,
    install_position VARCHAR(100),
    factory_price FLOAT,
    is_safety BOOLEAN DEFAULT FALSE,
    replace_rule TEXT
);

-- 创建损伤关联规则表
CREATE TABLE IF NOT EXISTS damage_rules (
    id VARCHAR(50) PRIMARY KEY,
    main_damage VARCHAR(200) NOT NULL,
    damage_type VARCHAR(50),
    related_parts JSON,
    rule_description TEXT,
    priority INTEGER DEFAULT 1
);

-- 创建损伤记录表
CREATE TABLE IF NOT EXISTS damage_records (
    id VARCHAR(50) PRIMARY KEY,
    image_url VARCHAR(500),
    vehicle_id VARCHAR(50),
    detections JSON,
    must_replace_parts JSON,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建报价单表
CREATE TABLE IF NOT EXISTS quotes (
    id VARCHAR(50) PRIMARY KEY,
    damage_record_id VARCHAR(50),
    vehicle_id VARCHAR(50),
    parts_total FLOAT,
    labor_total FLOAT,
    total_amount FLOAT,
    parts_detail JSON,
    labor_detail JSON,
    city VARCHAR(50),
    notes TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_vehicles_brand ON vehicles(brand);
CREATE INDEX idx_vehicles_series ON vehicles(series);
CREATE INDEX idx_parts_category ON parts(category);
CREATE INDEX idx_parts_oe ON parts(oe_number);
CREATE INDEX idx_damage_rules_main ON damage_rules(main_damage);
