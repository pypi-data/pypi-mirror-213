from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_last_hour():
    return datetime.now() - relativedelta(hours=1)