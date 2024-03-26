from typing import Any, Text, Dict, List
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


from rasa_sdk.events import SlotSet

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
            "bạn muốn chọn bất động sản nào trong những lựa chọn sau: nhà, căn hộ, cửa hàng, đất.",
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



class XacNhanBDSAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_bds"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        bds_entity = next(tracker.get_latest_entity_values("bds"), None)

        if bds_entity:
            if bds_entity == "đất":
                response = "Tôi sẽ tìm thông tin về đất cho bạn. Xin vui lòng cho biết quận bạn quan tâm."

                dispatcher.utter_message(text=response)
                # Kích hoạt intent "dat" khi bds_entity là "đất"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "dat", "confidence": 1.0}}}]
            elif bds_entity == "nhà ở":
                response = "OK, tôi sẽ kiểm tra thông tin về nhà ngay lập tức."
                dispatcher.utter_message(text=response)
                # Kích hoạt intent "huyen" khi bds_entity là "nhà ở"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "huyen", "confidence": 1.0}}}]
            elif bds_entity == "căn hộ":
                response = "Chờ một chút, tôi đang tìm thông tin về căn hộ."
                dispatcher.utter_message(text=response)
                # Kích hoạt intent "dat" khi bds_entity là "căn hộ"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "dat", "confidence": 1.0}}}]
            elif bds_entity == "cửa hàng":
                response = "Được, tôi sẽ tìm kiếm thông tin về cửa hàng cho bạn."
                dispatcher.utter_message(text=response)
                # Kích hoạt intent "dat" khi bds_entity là "cửa hàng"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "dat", "confidence": 1.0}}}]
            else:
                response = "Tôi không thể xác định loại bất động sản bạn chọn."
                dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được phản hồi về loại bất động sản.")
        
        # Câu lệnh return [] ở đây là trong phạm vi của hàm run
        return [SlotSet("bds", bds_entity)]




class XacNhanDatAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_dat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dat_entity = next(tracker.get_latest_entity_values('dat_e'), None)
        price_entity = next(tracker.get_latest_entity_values('price'), None)

        if dat_entity and price_entity:
            if dat_entity == "ninh kieu" and price_entity == "500":
                print(dat_entity)
                response = "Theo thông tin của bạn, bạn quan tâm đến bất động sản ở quận Ninh Kiều với mức giá 500 triệu. Tôi sẽ tìm kiếm thông tin cho bạn."
            elif dat_entity == "cai rang" and price_entity == "600":
                response = "Dựa vào yêu cầu của bạn, bạn muốn tìm kiếm bất động sản ở quận Cái Răng với mức giá 600 triệu. Tôi sẽ bắt đầu tìm kiếm ngay."
            else:
                response = f"Bạn quan tâm đến bất động sản ở quận {dat_entity} với mức giá khoảng {price_entity}. Tôi sẽ tìm kiếm thông tin cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("dat_e", dat_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về quận và mức giá.")
            return []

