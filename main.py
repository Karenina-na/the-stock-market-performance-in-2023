from K_lines import get_k_history
import pandas as pd
import os
import sys
import datetime

class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        # yyyy-mm-dd-hh:mm:ss.log
        filename = datetime.datetime.now().strftime('%Y-%m-%d-%H_%M_%S') + ".log"
        path = "./logs/"
        if not os.path.exists(path):
            os.makedirs(path)
        self.log = open(path + filename, "w", encoding="utf-8")

    def __del__(self):
        self.log.close()

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


sys.stdout = Logger()

if __name__ == "__main__":
    all_data = pd.read_csv('trading_data_2024-05-22.csv', encoding='utf-8-sig')
    codes = all_data['代码'].values
    names = all_data['名称'].values

    start_date = '20230101'
    end_date = '20231201'

    save_path = './data'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for code, name in zip(codes, names):
        code = str(code)
        # 如果不足6位，前面补0
        code = code.zfill(6)
        print(code, name)
        df = get_k_history(str(code), beg = start_date, end = end_date)
        name_tra = name.replace('*', '')
        df.to_csv(f'{save_path}/{code}_{name_tra}.csv', encoding='utf-8-sig', index=None)