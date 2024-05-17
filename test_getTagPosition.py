from serial import Serial
import serial.tools.list_ports as list_ports
from collections import deque
# from Uwb_util import (Get_ALLCom,ReadData,ReadTagData,DistanceData,PredictBirch,PredictKMeans)
from uwb import UWB
from uwb_util import UWBUtil


# メイン関数
def TAG_main(
        uwb_instance_list: list,
        uwbUtil: UWBUtil
        ):
    while True:
        # 接続されている全てのシリアルポートを取得してるっぽい
        uwb_serial: Serial = uwbUtil.getUwbSerialComPort()
        tmp_dict = uwbUtil.getTagData(uwb_serial=uwb_serial) if uwb_serial != None else None
        for uwb_serial in uwbUtil.getUwbSerialComPort:
            # タグデータの読み込み
            # データのアップデート
            tmp_dict = uwbUtil.getTagData(uwb_serial=uwb_serial)
            # pass





if __name__ == '__main__':
    # 今はtag1だけ使うので、tag1だけにする
    UWB_DATA = [{"anc":0,"tag":1},{"anc":1,"tag":1},{"anc":2,"tag":1}]
    # queueの最大長を60に設定。これは必要ないと思っている。
    # max_queue_length: int = 60
    #uwbのインスタンスを配列で格納。
    uwb_instance_list: list = [UWB(uwb["anc"], uwb["tag"]) for uwb in UWB_DATA]
    # uwbUtilのインスタンスを生成。全てのメソッドを込める予定
    uwbUtil = UWBUtil()
    # メイン関数の実行。ここがそもそもmain
    TAG_main(
        uwb_instance_list=uwb_instance_list,
        uwbUtil=uwbUtil
        )





