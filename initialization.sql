-- 创建数据库
CREATE DATABASE bilibili_live;

-- 添加数据库注释
COMMENT ON DATABASE bilibili_live IS '哔哩哔哩直播间';

-- 连接到数据库
\c bilibili_live;

-- 创建表 弹幕
CREATE TABLE danmaku (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 用户昵称
    uname VARCHAR(50),
    -- 用户UID
    uid VARCHAR(20),
    -- 弹幕内容
    msg VARCHAR(100),
    -- 时间戳
    create_time TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE danmaku IS '哔哩哔哩直播间';

COMMENT ON COLUMN danmaku.id IS 'ID 自增主键';

COMMENT ON COLUMN danmaku.room_id IS '房间ID';

COMMENT ON COLUMN danmaku.uname IS '用户昵称';

COMMENT ON COLUMN danmaku.uid IS '用户UID';

COMMENT ON COLUMN danmaku.msg IS '弹幕内容';

COMMENT ON COLUMN danmaku.create_time IS '时间戳';

COMMENT ON COLUMN danmaku.raw_data IS '原始数据';

-- 创建表 礼物
CREATE TABLE gift (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 用户昵称
    uname VARCHAR(50),
    -- 用户UID
    uid VARCHAR(20),
    -- 礼物名称
    gift_name VARCHAR(50),
    -- 数量
    gift_num INTEGER,
    -- 是否是付费道具
    paid BOOLEAN,
    -- 支付金额(1000 = 1元 = 10电池),盲盒:爆出道具的价值
    price INTEGER,
    -- 时间戳
    create_time TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE gift IS '礼物';

COMMENT ON COLUMN gift.id IS 'ID 自增主键';

COMMENT ON COLUMN gift.room_id IS '房间ID';

COMMENT ON COLUMN gift.uname IS '用户昵称';

COMMENT ON COLUMN gift.uid IS '用户UID';

COMMENT ON COLUMN gift.gift_name IS '礼物名称';

COMMENT ON COLUMN gift.gift_num IS '数量';

COMMENT ON COLUMN gift.paid IS '是否是付费道具';

COMMENT ON COLUMN gift.price IS '支付金额(1000 = 1元 = 10电池),盲盒:爆出道具的价值';

COMMENT ON COLUMN gift.create_time IS '时间戳';

COMMENT ON COLUMN gift.raw_data IS '原始数据';

-- 创建表 付费留言
CREATE TABLE super_chat (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 用户昵称
    uname VARCHAR(50),
    -- 用户UID
    uid VARCHAR(20),
    -- 留言内容
    message VARCHAR(200),
    -- 支付金额(元)
    price INTEGER,
    -- 开始时间
    start_time TIMESTAMP,
    -- 结束时间
    end_time TIMESTAMP,
    -- 时间戳
    create_time TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE super_chat IS '付费留言';

COMMENT ON COLUMN super_chat.id IS 'ID 自增主键';

COMMENT ON COLUMN super_chat.room_id IS '房间ID';

COMMENT ON COLUMN super_chat.uname IS '用户昵称';

COMMENT ON COLUMN super_chat.uid IS '用户UID';

COMMENT ON COLUMN super_chat.message IS '留言内容';

COMMENT ON COLUMN super_chat.price IS '支付金额(元)';

COMMENT ON COLUMN super_chat.start_time IS '开始时间';

COMMENT ON COLUMN super_chat.end_time IS '结束时间';

COMMENT ON COLUMN super_chat.create_time IS '时间戳';

COMMENT ON COLUMN super_chat.raw_data IS '原始数据';

-- 创建表 大航海
CREATE TABLE guard (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 用户昵称
    uname VARCHAR(50),
    -- 用户UID
    uid VARCHAR(20),
    -- 大航海等级
    guard_level INTEGER,
    -- 大航海数量
    guard_num INTEGER,
    -- 大航海单位
    gift_name VARCHAR(20),
    -- 价格
    price INTEGER,
    -- 开始时间
    start_time TIMESTAMP,
    -- 结束时间
    end_time TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE guard IS '大航海';

COMMENT ON COLUMN guard.id IS 'ID 自增主键';

COMMENT ON COLUMN guard.room_id IS '房间ID';

COMMENT ON COLUMN guard.uname IS '用户昵称';

COMMENT ON COLUMN guard.uid IS '用户UID';

COMMENT ON COLUMN guard.guard_level IS '大航海等级';

COMMENT ON COLUMN guard.guard_num IS '大航海数量';

COMMENT ON COLUMN guard.gift_name IS '大航海单位';

COMMENT ON COLUMN guard.price IS '价格';

COMMENT ON COLUMN guard.start_time IS '开始时间';

COMMENT ON COLUMN guard.end_time IS '结束时间';

COMMENT ON COLUMN guard.raw_data IS '原始数据';

-- 创建表 直播时间
CREATE TABLE live_time (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 直播间标题
    title VARCHAR(40),
    -- 分区名称
    area_name VARCHAR(20),
    -- 父区域名称
    parent_area_name VARCHAR(20),
    -- 开始时间（开始直播）
    start_time TIMESTAMP,
    -- 结束时间（关闭直播）
    end_time TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE live_time IS '直播时间';

COMMENT ON COLUMN live_time.id IS 'ID 自增主键';

COMMENT ON COLUMN live_time.room_id IS '房间ID';

COMMENT ON COLUMN live_time.title IS '直播间标题';

COMMENT ON COLUMN live_time.area_name IS '分区名称';

COMMENT ON COLUMN live_time.parent_area_name IS '父区域名称';

COMMENT ON COLUMN live_time.start_time IS '开始时间（开始直播）';

COMMENT ON COLUMN live_time.end_time IS '结束时间（关闭直播）';

COMMENT ON COLUMN live_time.raw_data IS '原始数据';

-- 创建表 其他事件
CREATE TABLE other (
    -- ID 自增主键
    id BIGSERIAL PRIMARY KEY NOT NULL,
    -- 房间ID
    room_id INTEGER NOT NULL,
    -- 类型
    type VARCHAR(20),
    -- 时间戳
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 原始数据
    raw_data JSON NOT NULL
);

-- 表及字段的注释
COMMENT ON TABLE other IS '其他事件';

COMMENT ON COLUMN other.id IS 'ID 自增主键';

COMMENT ON COLUMN other.room_id IS '房间ID';

COMMENT ON COLUMN other.type IS '类型';

COMMENT ON COLUMN other.create_time IS '时间戳';

COMMENT ON COLUMN other.raw_data IS '原始数据';