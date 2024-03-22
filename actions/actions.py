from typing import Any, Text, Dict, List
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class extractNhaEntity(Action):

    def name(self) -> Text:
        return "action_extract_nha_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bds_entity = next(tracker.get_latest_entity_values('bds'), None)

        if bds_entity:
            dispatcher.utter_message(text=f"{bds_entity} là bất động sản bạn muốn ")
        else:
            dispatcher.utter_message(text=f"tôi chưa nhận được phản hồi chọn bds")

        return[]

class chonBDSAction(Action):

    def name(self) -> Text:
        return "action_chon_bds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        responses = [
            "bạn muốn chọn bds nào?",
            "bạn muốn xem nhà ở khu vực nào?",
            "có gì tôi có thể giúp bạn về việc chọn bds không?",
            "Bạn muốn biết thông tin về căn hộ hay nhà đất?",
            "Bạn có muốn tìm hiểu thêm về môi trường sống xung quanh không?",
            "Có phải bạn đang tìm kiếm bất động sản để mua hay thuê?",
            "Bạn có muốn tham khảo một số dự án bất động sản đang hot không?",
            "Bạn cần thông tin chi tiết về loại hình bất động sản nào?",
        ]
        
        response = random.choice(responses)
        dispatcher.utter_message(text=response)
        
        return[]


class xacNhanBDSAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_bds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        bds_entity = next(tracker.get_latest_entity_values('bds'), None)

        responses = [
            f"tôi sẽ tìm thông tin về {bds_entity} cho bạn",
            f"chờ một chút, tôi đang tìm thông tin về {bds_entity}",
            f"ok, tôi sẽ kiểm tra thông tin về {bds_entity} ngay lập tức"
        ]

        if bds_entity:
            response = random.choice(responses)
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="tôi chưa nhận được phản hồi chọn bds")

        return[]
