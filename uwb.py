
# これはデータクラスと考える
class UWB:
    def __init__(self, anc_id, tag_id):
        self.anc_id = anc_id
        self.tag_id = tag_id
        self.distance = None

    def GetRangeData(self,result_dict):
        self.distance = result_dict["Range_data"]