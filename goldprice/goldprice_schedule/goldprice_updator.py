# from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from goldprice.views import get_tableData_karat,history_of_ounce, gold_price_charts_data, silver_price_data, silver_chart_data


def start():
  scheduler = BackgroundScheduler()
  # weather = WeatherViewset()
  scheduler.add_job(get_tableData_karat, "interval", minutes=2,id="goldprice_001",replace_existing=True)
  scheduler.add_job(silver_price_data, "interval", minutes=2,id="goldprice_000.1",replace_existing=True)
  scheduler.add_job(gold_price_charts_data, "interval", minutes=2,id="goldprice_003",replace_existing=True)
  scheduler.add_job(silver_chart_data, "interval", minutes=2,id="goldprice_004",replace_existing=True)
  scheduler.add_job(history_of_ounce, "interval", minutes=2,id="goldprice_005",replace_existing=True)
  scheduler.start()
