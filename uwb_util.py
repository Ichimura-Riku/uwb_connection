# import serial
import struct
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

    # private! 全てのCOMポートを取得
    def getAllSerialComPort(self) -> list | None:
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
    def getUwbSerialComPort(self) -> Serial | None:
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

    # TagをPCに接続して使用する場合
    def getTagData(self, uwb_serial : Serial) -> dict:
        hex_data = str(uwb_serial.readline().hex())
        raw_result = self.splitRawData(hex_data=hex_data)
        result = self.getUwbDataTAG(raw_data=raw_result)
        #print("result:",result)
        return result

    def splitRawData(self, hex_data):
    # 16進数文字列を2バイトずつに分割する
        try:
            split_data = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
        except:
            print("error")
            #split_data =
        return split_data

    def getUwbDataTAG(self, raw_data):
        result_dict = {"Anker_id":None,
                    "Tag_id": None,
                    "Range_data":None}
        #print(raw_data)
        anc_data = bytes.fromhex(raw_data[0])
        decoded_string = anc_data.decode('utf-8')

        if decoded_string == "A":
            result_dict["Anker_id"] = 0
        elif decoded_string == "B":
            result_dict["Anker_id"] = 1
        elif decoded_string == "C":
            result_dict["Anker_id"] = 2
        try:
            result_dict["Tag_id"] = int(int(raw_data[1]))
        except:
            result_dict["Tag_id"] = "?"
        range_data = self.getRangedata(raw_data[3:-1])
        result_dict["Range_data"] = range_data

        return result_dict
    def getRangedata(self, raw_range):
        data = "".join(raw_range)
        # ヘキサデシマル文字列をバイト列に変換
        binary_data = bytes.fromhex(data)
        try:
        # 'f'は32ビットの浮動小数点数を表すフォーマット文字
            decimal_number = struct.unpack('<f', binary_data)[0]
        except:
            decimal_number = 0.0

        value = "{:.4f}".format(decimal_number)
        return value



if __name__ == '__main__':
    uwbUtil = UWBUtil()
    uwb_serial = uwbUtil.getUwbSerialComPort()
    while True:
        print(uwbUtil.getTagData(uwb_serial=uwb_serial))

