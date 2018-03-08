# -*- coding:utf-8 -*-

from . import scheduler
from apscheduler.triggers.interval import IntervalTrigger
from .UpdateSer import update_sku_statu,update_tag_statu,update_base_statu,update_singlep_statu,update_distrib_statu
from .UpdateQ import update_cx_q,update_yc_q,update_ych_q


# scheduler定时执行的函数，负责更新数据库中服务状态以及记录时间
def update_status():
    # global r

    update_tag_statu()
    update_sku_statu()
    update_distrib_statu()
    update_singlep_statu()
    update_base_statu()
    update_cx_q()
    update_yc_q()
    update_ych_q()




scheduler.add_job(func=update_status,
		  trigger=IntervalTrigger(seconds=120),
                  id = 'get_statu',
                  replace_existing=True
                  )
