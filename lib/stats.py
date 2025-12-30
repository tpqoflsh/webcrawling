from oauth2client.service_account import ServiceAccountCredentials

import warnings
import gspread
import datetime
import statistics

warnings.filterwarnings(action='ignore')

class Stat():
    def __init__(self, elements):
        self.elements = elements
        self.web_cpu_avg = []
        self.web_cpu_max = []
        self.was_cpu_avg = []
        self.was_cpu_max = []
        self.db_cpu_avg = []
        self.db_cpu_max = []
        self.web_mem_avg = []
        self.web_mem_max = []
        self.was_mem_avg = []
        self.was_mem_max = []
        self.db_mem_avg = []
        self.db_mem_max = []

    def printer(self, user, time:  str, inb, outb):
        stat = [
            statistics.mean(self.web_cpu_avg), statistics.mean(self.was_cpu_avg), statistics.mean(self.db_cpu_avg),
            statistics.mean(self.web_mem_avg), statistics.mean(self.was_mem_avg),statistics.mean(self.db_mem_avg),
            max(self.web_cpu_max), max(self.was_cpu_max), max(self.db_cpu_max),
            max(self.web_mem_max), max(self.was_mem_max), max(self.db_mem_max)
            ]
        
        print(f"\n동시접속자 : {user}명, 시간 : {time}\n")
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - -\n구분\t\tCPU(%)\t\tMemory(%)")
        print("e학습터\t\t평균\t최대\t평균\t최대")
        print(f"WEB\t\t{stat[0]: .2f}\t{stat[6]}\t{stat[3]: .2f}\t{stat[9]}")
        print(f"WAS\t\t{stat[1]: .2f}\t{stat[7]}\t{stat[4]: .2f}\t{stat[10]}")
        print(f"DB\t\t{stat[2]: .2f}\t{stat[8]}\t{stat[5]: .2f}\t{stat[11]}\n")
        print(f'Inbound :{inb: .3f}G, Outbound :{outb: .3f}G\n')
        
        return stat
        
    def web_process(self, instance):
        for x, j in enumerate(instance.split('\n')):
            if x % 2 == 0:
                for y, k in enumerate(j.split()):
                    if y // 5 >= 1 and y % 5 == 0:
                        self.web_mem_avg.append(float(k))
                    elif y // 6 >= 1 and y % 6 == 0:
                        self.web_mem_max.append(float(k))
            else:
                for z, h in enumerate(j.split()):
                    if z // 8 >= 1 and z % 8 == 0:
                        self.web_cpu_avg.append(float(h))
                    elif z // 9 >= 1 and z % 9 == 0:
                        self.web_cpu_max.append(float(h))
                        
    def was_process(self, instance):
        for x, j in enumerate(instance.split('\n')):
            if x % 2 == 0:
                for y, k in enumerate(j.split()):
                    if y // 5 >= 1 and y % 5 == 0:
                        self.was_mem_avg.append(float(k))
                    elif y // 6 >= 1 and y % 6 == 0:
                        self.was_mem_max.append(float(k))
            else:
                for z, h in enumerate(j.split()):
                    if z // 8 >= 1 and z % 8 == 0:
                        self.was_cpu_avg.append(float(h))
                    elif z // 9 >= 1 and z % 9 == 0:
                        self.was_cpu_max.append(float(h))
                        
    def db_process(self, instance):
        for x, j in enumerate(instance.split('\n')):
            if x % 2 == 0:
                for y, k in enumerate(j.split()):
                    if y // 5 >= 1 and y % 5 == 0:
                        self.db_mem_avg.append(float(k))
                    elif y // 6 >= 1 and y % 6 == 0:
                        self.db_mem_max.append(float(k))
            else:
                for z, h in enumerate(j.split()):
                    if z // 8 >= 1 and z % 8 == 0:
                        self.db_cpu_avg.append(float(h))
                    elif z // 9 >= 1 and z % 9 == 0:
                        self.db_cpu_max.append(float(h))
                        
    def arrange(self):
        for i in self.elements:
            if "web" in i and "webfilter" not in i:
                self.web_process(i)
            elif "was" in i:
                self.was_process(i)
            elif "db" in i:
                self.db_process(i)

today = datetime.date.today()
today_title = f'{str(today).split("-")[1]}월 {str(today).split("-")[2]}일 통계 현황'

class SpreadSheet(Stat):
    def __init__(self, user, time, inbound, outbound):
        super().__init__(None)
        self.user = user
        self.time = time
        self.inbound = inbound
        self.outbound = outbound
        self.spread_key = "1"  # sheet ID
        self.json_key_path = "bustling.json"  # google service auth json file
    
    def certify(self):
        scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        ]
        credential = ServiceAccountCredentials.from_json_keyfile_name(self.json_key_path, scope)
        ss = gspread.authorize(credential)
        
        return ss.open_by_key(self.spread_key)
    
    def init_sheet(self, doc):
        if today_title != doc.get_worksheet(0).title:
            sheet = self.create_sheet(doc, doc.get_worksheet(0).id, today_title)
            return sheet
        else:
            sheet = doc.worksheet(today_title)
            return sheet
    
    @staticmethod
    def create_sheet(doc, id, title):
        delete_ranges = [['D10:F11'],['D15:H16'],['D27:G29'],['I27:L30'],['D37:G39'],['I37:L40'],['D32'],['D42']]
        doc.duplicate_sheet(id,insert_sheet_index=0,new_sheet_name=title)
        sheet = doc.worksheet(title)
        sheet.update('L3', f'{today.year}. {str(today).split("-")[1]}. {str(today).split("-")[2]}')
        for delete_range in delete_ranges:
            sheet.batch_clear(delete_range)
        return sheet
    
    def update_sheet(self, sheet, avg, now_time):
        if now_time >= 17:
            sheet.update('D11',self.user)
            sheet.update('F11',self.time)
            sheet.update('D37',avg[0]/100)
            sheet.update('E37',avg[6]/100)
            sheet.update('F37',avg[3]/100)
            sheet.update('G37',avg[9]/100)
            sheet.update('D38',avg[1]/100)
            sheet.update('E38',avg[7]/100)
            sheet.update('F38',avg[4]/100)
            sheet.update('G38',avg[10]/100)
            sheet.update('D39',avg[2]/100)
            sheet.update('E39',avg[8]/100)
            sheet.update('F39',avg[5]/100)
            sheet.update('G39',avg[11]/100)
            sheet.update('D42',f"{self.inbound: .3f}G(In) / {self.outbound: .3f}G(Out)")
        else:
            sheet.update('D10',self.user)
            sheet.update('F10',self.time)
            sheet.update('D27',avg[0]/100)
            sheet.update('E27',avg[6]/100)
            sheet.update('F27',avg[3]/100)
            sheet.update('G27',avg[9]/100)
            sheet.update('D28',avg[1]/100)
            sheet.update('E28',avg[7]/100)
            sheet.update('F28',avg[4]/100)
            sheet.update('G28',avg[10]/100)
            sheet.update('D29',avg[2]/100)
            sheet.update('E29',avg[8]/100)
            sheet.update('F29',avg[5]/100)
            sheet.update('G29',avg[11]/100)
            sheet.update('D32',f"{self.inbound: .3f}G(In) / {self.outbound: .3f}G(Out)")