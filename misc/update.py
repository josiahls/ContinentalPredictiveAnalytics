import pandas as pd
from sqlalchemy import create_engine


class Updater:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://ssdi:dorodchi@159.89.93.134/ssdi')

    def termination(self):
        df = pd.read_excel('UNCC_Termination pre 2017.xlsx')
        with self.engine.connect() as conn, conn.begin():
            df.to_sql("attrition", conn, if_exists="replace")


if __name__ == "__main__":
    myUpdater = Updater()
    myUpdater.termination()
