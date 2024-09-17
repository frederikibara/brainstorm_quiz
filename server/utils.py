from datetime import datetime, timedelta

def get_last_n_days_dates(n):
    today = datetime.today()
    return [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(n)]
