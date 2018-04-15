--话题表
create table zhihu_topic 
(topic_uuid varchar(200) primary key comment '主键',
topic_id varchar(200) comment '话题编号',
topic_name varchar(200) comment '话题名称',
topic_link varchar(200) comment '话题链接',
follow_number int(10) comment '关注人数',
question_number int(10) comment '问题数',
topic_describe varchar(2000) comment '话题描述',
parent_topic_id varchar(1000) comment '父级话题编号',
children_topic_id varchar(1000) comment '子级话题编号',
store_time datetime comment '入库时间',
topic_level int(10) comment '话题层级'
) comment = '知乎话题表';