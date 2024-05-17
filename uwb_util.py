# import serial
from serial import Serial
import serial.tools.list_ports as list_ports
import re
import os

# これはデータクラスと考える
class UWB:
    def __init__(self, anc_id, tag_id):
        self.anc_id = anc_id
        self.tag_id = tag_id
        self.distance = None

    def GetRangeData(self,result_dict):
        self.distance = result_dict["Range_data"]

# ここはリポジトリクラスと考えたほうが良さそう
# ここで実装するクラスはそのまま値を返すだけのクラスにする
# 値の保持はしない
class UWBUtil:
    # 初期化
    def __init__(self) -> None:
        # androidの場合1つでいいから要らなそうだけど、一応配列で持っておく
        # self.comport_list = []

        # ???
        # self.distance_list = []
        # ???
        # self.current_anker_points_list = []
        # self._getAllCom_try1()
        pass

    # public! 全てのCOMポートを持つ配列を返す
    def getAllSerialList(self) -> list:
        self._Get_ALLCom()
        return self.comport_list

    # private! 全てのCOMポートを取得
    def getAllCom(self) -> list | None:
        port_list = list_ports.comports()
        comport_list = []
        if len(port_list) <= 0:
            print("No COM")
            return None
        else:
            print("ALL COM")
            for port in port_list:
                print("port:",list(port)[0])
                uwb_serial = Serial()
                uwb_serial.port = list(port)[0]
                uwb_serial.baudrate = 115200
                comport_list.append(uwb_serial)
                # この書き方だとエラーが出るので、コメントアウト
                # ser = Serial(list(port)[0], 115200)
                # comport_list.append(ser)
            return comport_list


    # private!別のcomポート取得方法
    def getUwbCom(self) -> Serial | None:
        uwb_serial = Serial()
        uwb_serial.baudrate = 115200
        all_ports = os.listdir('/dev')
        if "cu.SLAB_USBtoUART" in all_ports:
            # port_index : int = all_ports.index("cu.SLAB_USBtoUART")
            # print(port_index)
            # print(all_ports[port_index])
            uwb_serial.port = '/dev/cu.SLAB_USBtoUART'
            uwb_serial.open()
            print("port open")
            return uwb_serial
        else :
            print("no port")
            return None


    # def Get_UWBdataANC(input_string):
    #     data_dict = {}
    #     # キーと値を抽出して辞書に保存する
    #     pattern = re.compile(r'([^=,]+):([^=,]+)')
    #     matches = pattern.findall(input_string)
    #     for match in matches:
    #         key = match[0].strip()
    #         value = match[1].strip()
    #         # 値が "(...)" の形式であれば、括弧内のデータのみを抽出
    #         if key == "range" or key == "rssi":
    #             value = Pattern_RangeRssi(key=key, input_string=input_string)
    #         data_dict[key] = value
    #     return data_dict

    #選択したUWBアンカーからデータを取得
    # 今回はtagだけ使う予定なので必要ない
    # def ReadDataByAnchor(self, port: Serial):
    #     # try:
    #         #for _serial in serial_list:
    #         line = port.readline().decode('UTF-8').replace('\n', '')

    #         # uwbアンカーからデータを取得する


    #         '--------------------ここまでやってる--------------------------'
        #     result = Get_UWBdataANC(line)
        #     Set_UWBdataANC(result)

        #     if result != {}:
        #         print("result:",line)
        #     elif result == {}:
        #         print("[LOG]:",line)
        #     print(type(line))
        # except Exception as e:
        #     print(e.args)
        #     pass
    #TagをPCに接続して使用する場合
    # def getTagData(ser : Serial) -> dict:
    #     line = str(ser.readline().hex())
    #     raw_result = Split_RawData(line)
    #     result = Get_UWBdataTAG(raw_data=raw_result)
    #     #print("result:",result)
    #     return result




if __name__ == '__main__':
    uwbUtil = UWBUtil()
    print(uwbUtil.getAllCom())
