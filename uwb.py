
# これはデータクラスと考える
class UwbData:
    def __init__(self, anc_id, tag_id):
        self.anc_id = anc_id
        self.tag_id = tag_id
        self.distance = None

    # def setRangeData(self,tag_data: dict):
    #     self.distance = tag_data["Range_data"]