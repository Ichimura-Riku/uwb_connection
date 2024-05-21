import struct
from serial import Serial
import serial.tools.list_ports as list_ports
from uwb import UwbData
import os

# ここはリポジトリクラスと考えたほうが良さそう
# ここで実装するクラスはそのまま値を返すだけのクラスにする
# 値の保持はしない

class UwbState:
    def __init__(self, uwb_tag_map: list[dict]) -> None:
        self.uwbData_instance_list : list[UwbData] = [UwbData(uwb["anc"], uwb["tag"]) for uwb in uwb_tag_map]

    def setRangeData(self, tag_data: dict) -> None:
        for instance_i  in self.uwbData_instance_list:
            # どうしても型を明示したい病気なので、変数宣言
            instance : UwbData = instance_i
            if instance.anc_id == tag_data["Anchor_id"] and instance.tag_id == tag_data["Tag_id"]:
                instance.distance = tag_data["Range_data"]

class UwbUtil:

    # 初期化
    def __init__(self, uwb_tag_map: list[dict]) -> None:
        # androidの場合1つでいいから要らなそうだけど、一応配列で持っておく
        # self.comport_list = []
        self.uwbState: UwbState = UwbState(uwb_tag_map=uwb_tag_map)
        # ???
        # self.distance_list = []
        # ???
        # self.current_anchor_points_list = []
        # self._getAllCom_try1()
        pass


    # 全てのCOMポートを取得
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


    # 別のcomポート取得方法
    def getUwbSerialComPort(self) -> Serial | None:
        uwb_serial = Serial()
        uwb_serial.baudrate = 115200
        all_ports = os.listdir('/dev')
        if "cu.SLAB_USBtoUART" in all_ports:
            # port_index : int = all_ports.index("cu.SLAB_USBtoUART")
            # print(port_index)
            # print(all_ports[port_index])
            uwb_serial.port = '/dev/tty.SLAB_USBtoUART'
            uwb_serial.open()
            return uwb_serial
        else :
            print("no port")
            return None

    # TagをPCに接続して使用する場合
    def setTagData(self, uwb_serial : Serial) :
        hex_data: str = str(uwb_serial.readline().hex())

        print(hex_data)
        raw_result: list[str] = self.__splitRawData(hex_data=hex_data)
        tag_data: dict[str, None] = self.__getUwbDataTAG(raw_data=raw_result)
        #print("tag_data:",tag_data)
        self.uwbState.setRangeData(tag_data)


    def __splitRawData(self, hex_data: str) -> list[str]:
    # 16進数文字列を2バイトずつに分割する
        try:
            split_data = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
        except:
            print("error")
            #split_data =
        return split_data

    def __getUwbDataTAG(self, raw_data: list[str]) -> dict:
        result_dict = {"Anchor_id":None,
                    "Tag_id": None,
                    "Range_data":None}
        #print(raw_data)
        try:
            anc_data = bytes.fromhex(raw_data[0])
            decoded_string = anc_data.decode('utf-8')
        except Exception as e:
            print(e)
            decoded_string = "?"
        # print(decoded_string)

        if decoded_string == "A":
            result_dict["Anchor_id"] = 0
        elif decoded_string == "B":
            result_dict["Anchor_id"] = 1
        elif decoded_string == "C":
            result_dict["Anchor_id"] = 2
        try:
            result_dict["Tag_id"] = int(int(raw_data[1]))
        except:
            result_dict["Tag_id"] = "?"
        range_data: str = self.__getRangeData(raw_range=raw_data[3:-1])
        result_dict["Range_data"] = range_data

        return result_dict
    def __getRangeData(self, raw_range: list[str]):
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

    # 各UWBインスタンスのtag_data(距離データ)を更新
    # こいつはgetTagData()内の最後で直接呼び出していい説がある







