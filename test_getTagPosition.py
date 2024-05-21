from serial import Serial
import serial.tools.list_ports as list_ports
from collections import deque
# from Uwb_util import (Get_ALLCom,ReadData,ReadTagData,DistanceData,PredictBirch,PredictKMeans)
from uwb import UwbData
from uwb_util import UwbUtil


# メイン関数
def TAG_main(uwbUtil: UwbUtil):
    # 接続されている全てのシリアルポートを取得してるっぽい
    all_uwb_serial: list[Serial] = [uwbUtil.getUwbSerialComPort()]

    # 複数の場合
    # all_uwb_serial: list[Serial] = uwbUtil.getAllSerialComPort()
    # [print(uwb_serial.name) for uwb_serial in all_uwb_serial]

    while True:

        # それぞれのポートから取得した情報をuwbUtil.setTagDataを実行してuwbStateにセットしていく
        [uwbUtil.setTagData(uwb_serial = uwb_serial) for uwb_serial in all_uwb_serial if uwb_serial != None]


        # 出力
        print("----------------------------------------")
        for uwbData_instance_i in uwbUtil.uwbState.uwbData_instance_list:
            uwbData_instance: UwbData = uwbData_instance_i
            print(f"tag: {uwbData_instance.tag_id}, anc: {uwbData_instance.anc_id}" , uwbData_instance.distance)
        print("----------------------------------------")






if __name__ == '__main__':
    # 今はtag1だけ使うので、tag1だけにする
    uwb_tag_map: list[dict]= [{"anc":0,"tag":2},{"anc":1,"tag":2},{"anc":2,"tag":2}]
    # queueの最大長を60に設定。これは必要ないと思っている。
    # max_queue_length: int = 60
    #uwbのインスタンスを配列で格納。
    # uwb_instance_list: list[UwbData] = [UwbData(uwb["anc"], uwb["tag"]) for uwb in UWB_DATA]
    # uwbUtilのインスタンスを生成。全てのメソッドを込める予定
    # uwbUtil = UwbUtil(instance_list=uwb_instance_list)
    uwbUtil = UwbUtil(uwb_tag_map= uwb_tag_map)
    # メイン関数の実行。ここがそもそもmain
    TAG_main(
        uwbUtil=uwbUtil
        )





