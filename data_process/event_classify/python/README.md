# ABOUT

These scripts finish tasks to classified news/weibo and detect
individual events from the classified set.

# HOWTO

## Data Input:

* t_lable_group_comp_1: gives the messages filtered by `news` type
from the original database.

* t_lable_group_comp_4: gives the message filtered by `weibo` type
from the original database.

## Workflow:

    $ python classify_news.py
    $ python detect_events.py
    $ python classify_weibo.py