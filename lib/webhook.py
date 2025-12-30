import requests
import json

#test_webhook_url = ""
webhook_url = ""
class Messages:
    @staticmethod
    def errormsg(time, error):
        msg = {
            "text": f"{time}시 통계가 실패하였습니다. 확인 바랍니다.\n{error}"
        }
        requests.post(webhook_url, json=msg)
        
    @staticmethod
    def successmsg(time):
        msg = {
            "text": f"e학습터 {time}시 통계 완료했습니다."
        }
        requests.post(webhook_url, json=msg)
        
    @staticmethod
    def temp(time, user, user_time, inbound, outbound, avg):
        msg = {
            "text": f"\n동시접속자 : {user}명, 시간 : {user_time}\n- - - - - - - - - - - - - - - - - - - - - - - - - - -\n구분\t\tCPU(%)\t\tMemory(%)\ne학습터\t\t평균\t최대\t평균\t최대\nWEB\t\t{avg[0]: .2f}  \t{avg[6]}  \t{avg[3]: .2f}  \t{avg[9]}\nWAS\t\t{avg[1]: .2f}  \t{avg[7]}  \t{avg[4]: .2f}  \t{avg[10]}\nDB\t\t\t{avg[2]: .2f}  \t{avg[8]}  \t{avg[5]: .2f}  \t{avg[11]}\n\nInbound :{inbound: .3f}G, Outbound :{outbound: .3f}G\n\ne학습터 {time}시 통계 완료했습니다."
        }
        msg2 = {
            "text": f"{avg[0]:.2f}%,{avg[6]}%,{avg[3]:.2f}%,{avg[9]}%\n{avg[1]:.2f}%,{avg[7]}%,{avg[4]:.2f}%,{avg[10]}%\n{avg[2]:.2f}%,{avg[8]}%,{avg[5]:.2f}%,{avg[11]}%"
        }
        requests.post(webhook_url, json=msg)