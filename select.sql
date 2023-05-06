-- 最近20条弹幕
SELECT
    id,
    uname AS 用户,
    msg AS 内容
FROM
    danmaku
WHERE
    room_id = 3472667
    AND msg != '菜'
ORDER BY
    create_time DESC
LIMIT
    20;

-- 统计每个人发了多少个弹幕
SELECT
    uname,
    COUNT(uname) as count
FROM
    danmaku
WHERE
    room_id = 3472667
    AND msg != '菜'
    AND create_time >= '2023-01-01'
GROUP BY
    uname
ORDER BY
    count DESC;

-- 最近10个礼物
SELECT
    id,
    uname AS 用户,
    gift_name AS 礼物,
    gift_num AS 数量,
    price AS 价值
FROM
    gift
WHERE
    room_id = 3472667
ORDER BY
    create_time DESC
LIMIT
    10;

-- 最近10个礼物（付费）
SELECT
    id,
    uname AS 用户,
    gift_name AS 礼物,
    gift_num AS 数量,
    price AS 价值
FROM
    gift
WHERE
    room_id = 3472667
    and paid = true
ORDER BY
    create_time DESC
LIMIT
    10;

-- 最近10个舰长
SELECT
    id,
    uname AS 用户昵称,
    guard_level AS 等级,
    guard_num AS 数量,
    gift_name AS 名称,
    price AS 价格,
    start_time AS 开始时间,
    end_time AS 结束时间
FROM
    guard
WHERE
    room_id = 3472667
ORDER BY
    id DESC
LIMIT
    10;

-- 最近10个SC
SELECT
    id,
    uname AS 用户昵称,
    message AS 消息,
    price AS 价格,
    start_time AS 开始时间,
    end_time AS 结束时间
FROM
    super_chat
WHERE
    room_id = 3472667
ORDER BY
    create_time DESC
LIMIT
    10;

-- 最近10次直播
SELECT
    id,
    title AS 标题,
    area_name AS 分区,
    parent_area_name AS 父分区,
    start_time AS 开播时间,
    end_time AS 关播时间,
    DATE_PART('minute', end_time - start_time) AS 直播时间_分钟
FROM
    live_time
WHERE
    room_id = 3472667
ORDER BY
    start_time DESC
LIMIT
    10;