#!/usr/bin/env python3
"""
SQLite数据库初始化脚本
将PostgreSQL数据转换为SQLite格式
"""

import sqlite3
import os
from pathlib import Path

# 项目路径
project_dir = Path(__file__).parent
backend_dir = project_dir / "backend"
db_path = backend_dir / "cardamage.db"

def init_database():
    """初始化SQLite数据库"""
    print("=" * 60)
    print("车辆定损APP - 数据库初始化")
    print("=" * 60)
    
    # 删除旧数据库
    if db_path.exists():
        print(f"\n删除旧数据库: {db_path}")
        db_path.unlink()
    
    # 创建新数据库
    print(f"\n创建新数据库: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建表结构
    print("\n创建数据表...")
    
    # 1. 车型表
    cursor.execute('''
    CREATE TABLE vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. 配件表
    cursor.execute('''
    CREATE TABLE parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        base_price REAL DEFAULT 0,
        labor_hours REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 3. 车型-配件关联表
    cursor.execute('''
    CREATE TABLE vehicle_parts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER,
        part_id INTEGER,
        part_number TEXT,
        price REAL,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id),
        FOREIGN KEY (part_id) REFERENCES parts(id)
    )
    ''')
    
    # 4. 只换不修规则表
    cursor.execute('''
    CREATE TABLE damage_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_id INTEGER,
        damage_type TEXT,
        damage_severity TEXT,
        action TEXT DEFAULT 'repair',
        threshold REAL,
        description TEXT,
        FOREIGN KEY (part_id) REFERENCES parts(id)
    )
    ''')
    
    # 5. 定损记录表
    cursor.execute('''
    CREATE TABLE damage_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_id INTEGER,
        image_path TEXT,
        damage_type TEXT,
        damage_severity TEXT,
        confidence REAL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
    )
    ''')
    
    # 6. 报价单表
    cursor.execute('''
    CREATE TABLE quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id INTEGER,
        total_parts REAL DEFAULT 0,
        total_labor REAL DEFAULT 0,
        total_amount REAL DEFAULT 0,
        status TEXT DEFAULT 'draft',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (record_id) REFERENCES damage_records(id)
    )
    ''')
    
    # 7. 报价单项表
    cursor.execute('''
    CREATE TABLE quote_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_id INTEGER,
        part_id INTEGER,
        part_name TEXT,
        quantity INTEGER DEFAULT 1,
        unit_price REAL,
        labor_hours REAL,
        action TEXT,
        amount REAL,
        FOREIGN KEY (quote_id) REFERENCES quotes(id)
    )
    ''')
    
    print("[OK] 数据表创建完成")
    
    # 插入示例数据
    print("\n插入示例数据...")
    
    # 插入车型数据
    vehicles = [
        ("大众", "朗逸", 2024, "轿车"),
        ("大众", "帕萨特", 2024, "轿车"),
        ("丰田", "卡罗拉", 2024, "轿车"),
        ("丰田", "凯美瑞", 2024, "轿车"),
        ("本田", "雅阁", 2024, "轿车"),
        ("本田", "CR-V", 2024, "SUV"),
        ("日产", "轩逸", 2024, "轿车"),
        ("日产", "奇骏", 2024, "SUV"),
        ("比亚迪", "秦PLUS", 2024, "轿车"),
        ("比亚迪", "宋PLUS", 2024, "SUV"),
        ("特斯拉", "Model 3", 2024, "轿车"),
        ("特斯拉", "Model Y", 2024, "SUV"),
    ]
    cursor.executemany('INSERT INTO vehicles (brand, model, year, category) VALUES (?, ?, ?, ?)', vehicles)
    print(f"[OK] 插入 {len(vehicles)} 款车型")
    
    # 插入配件数据
    parts = [
        ("前保险杠", "外观件", 800, 2.0),
        ("后保险杠", "外观件", 750, 2.0),
        ("左前车门", "外观件", 1200, 3.0),
        ("右前车门", "外观件", 1200, 3.0),
        ("左后车门", "外观件", 1100, 3.0),
        ("右后车门", "外观件", 1100, 3.0),
        ("引擎盖", "外观件", 1500, 3.5),
        ("后备箱盖", "外观件", 1000, 2.5),
        ("左前大灯", "灯具", 600, 0.5),
        ("右前大灯", "灯具", 600, 0.5),
        ("左后尾灯", "灯具", 400, 0.5),
        ("右后尾灯", "灯具", 400, 0.5),
        ("前挡风玻璃", "玻璃", 1200, 2.0),
        ("后挡风玻璃", "玻璃", 800, 2.0),
        ("左后视镜", "外观件", 500, 1.0),
        ("右后视镜", "外观件", 500, 1.0),
        ("左前翼子板", "外观件", 800, 2.5),
        ("右前翼子板", "外观件", 800, 2.5),
        ("中网", "外观件", 600, 1.0),
        ("前防撞梁", "结构件", 500, 3.0),
    ]
    cursor.executemany('INSERT INTO parts (name, category, base_price, labor_hours) VALUES (?, ?, ?, ?)', parts)
    print(f"[OK] 插入 {len(parts)} 种配件")
    
    # 插入只换不修规则
    rules = [
        (1, "crack", "severe", "replace", 0.8, "前保险杠裂纹严重，建议更换"),
        (1, "dent", "severe", "replace", 0.9, "前保险杠凹陷严重，建议更换"),
        (2, "crack", "severe", "replace", 0.8, "后保险杠裂纹严重，建议更换"),
        (3, "dent", "severe", "replace", 0.85, "车门凹陷严重，建议更换"),
        (4, "dent", "severe", "replace", 0.85, "车门凹陷严重，建议更换"),
        (7, "dent", "severe", "replace", 0.9, "引擎盖凹陷严重，建议更换"),
        (8, "dent", "severe", "replace", 0.85, "后备箱盖凹陷严重，建议更换"),
        (13, "crack", "any", "replace", 1.0, "挡风玻璃裂纹必须更换"),
        (14, "crack", "any", "replace", 1.0, "后挡风玻璃裂纹必须更换"),
    ]
    cursor.executemany('INSERT INTO damage_rules (part_id, damage_type, damage_severity, action, threshold, description) VALUES (?, ?, ?, ?, ?, ?)', rules)
    print(f"[OK] 插入 {len(rules)} 条只换不修规则")
    
    # 提交事务
    conn.commit()
    
    # 验证数据
    print("\n验证数据...")
    cursor.execute('SELECT COUNT(*) FROM vehicles')
    vehicle_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM parts')
    part_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM damage_rules')
    rule_count = cursor.fetchone()[0]
    
    print(f"  车型: {vehicle_count} 款")
    print(f"  配件: {part_count} 种")
    print(f"  规则: {rule_count} 条")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("数据库初始化完成!")
    print(f"数据库文件: {db_path}")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    init_database()
