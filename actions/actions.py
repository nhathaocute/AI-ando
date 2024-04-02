from typing import Any, Text, Dict, List
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, ActionExecuted

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
            "bạn muốn chọn bất động sản nào trong những lựa chọn sau: nhà ở, căn hộ, cửa hàng, đất nền",
            "bạn muốn xem bất động sản ở khu vực nào? tôi chỉ có thể trả lời bạn trong các lĩnh vực: nhà ở, căn hộ, cửa hàng, đất nền.",
            "Bạn muốn biết thông tin về căn hộ, nhà ở, đất nền hay cửa hàng?",
            "Bạn cần thông tin chi tiết về loại hình bất động sản nào? căn hộ, nhà ở, đất nền hay cửa hàng.",
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
        print(bds_entity)

        if bds_entity:
            if bds_entity == "đất nền" or bds_entity == "dat nen":
                response = "Tôi sẽ tìm thông tin về đất cho bạn. Xin vui lòng cho biết loại (đất nền hay đất chưa sử dụng), quận và giá bạn quan tâm."

                dispatcher.utter_message(text=response)
                # Kích hoạt intent "dat" khi bds_entity là "đất"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "dat", "confidence": 1.0}}}]
            elif bds_entity == "nhà ở" or bds_entity == "nha o":
                response = "OK, tôi sẽ kiểm tra thông tin về nhà ngay lập tức. Xin vui lòng cho biết loại (nhà phố hay nhà gia đình), quận và giá bạn quan tâm."
                dispatcher.utter_message(text=response)
                # Kích hoạt intent "huyen" khi bds_entity là "nhà ở"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "nha", "confidence": 1.0}}}]
            elif bds_entity == "căn hộ" or bds_entity == "can ho":
                response = "Chờ một chút, tôi đang tìm thông tin về căn hộ. Xin vui lòng cho biết loại (căn hộ chung cư hay căn hộ dịch vụ), quận và giá bạn quan tâm."
                dispatcher.utter_message(text=response)
                # Kích hoạt intent "dat" khi bds_entity là "căn hộ"
                return [SlotSet("bds", bds_entity), {"event": "user", "parse_data": {"intent": {"name": "can_ho", "confidence": 1.0}}}]
            else:
                response = "Tôi không thể xác định loại bất động sản bạn chọn."
                dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được phản hồi về loại bất động sản.")
        
        return [SlotSet("bds", bds_entity)]



class XacNhanDatAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_dat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dat_entity = next(tracker.get_latest_entity_values('dat_e'), None)
        print(dat_entity)
        price_entity = next(tracker.get_latest_entity_values('price'), None)
        print(price_entity)
        property_type_entity = next(tracker.get_latest_entity_values('property_type'), None)
        print(property_type_entity)


        if dat_entity and price_entity:
            if dat_entity == "ninh kieu" and 400 <= int(price_entity) <= 500:
                print(dat_entity)
                response = "<p>hihi <img src='static/img/canho_1.jpg' alt='' /> <img src='static/img/canho_2.jpg' alt='' /></p>"
            elif dat_entity == "cai rang" and 400 <= int(price_entity) <= 600:
                response = '''  <li> mức giá 680 triệu </li>
                                <li> diện tích 37m2 </li>
                                - 1 phòng ngủ
                                - Vị trí đắc địa KĐT Hưng Phú, mặt tiền Võ Nguyên Giáp, TP Cần Thơ, thuận tiện di chuyển
                                <a class='click-link' href='https://google.com' target='_blank'>bấm vào để xem</a>
                                <p>hihi <img src='static/img/canho_1.jpg' alt='' /> <img src='static/img/canho_2.jpg' alt='' /></p>'''
            elif dat_entity == "thot not" and 400 <= int(price_entity) <= 800 and property_type_entity == "đất nền":
                response = '''Đất nằm trên Lộ nhựa Xẻo Đế 4m, ngang 7.65 nở hậu 8m, có 2m cặp bờ sông, cách lộ vòng cung 300m, cách chợ Base 500m, gần UBND Trường Lạc, Ô môn, gần trung tâm VHTT, gần trường học cấp 1&2, khu dân cư đông đúc.
                            </br>
                            Diện tích: 126m²
                            Mặt tiền: 7,65 m
                            Mức giá: 790 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-923-phuong-truong-lac/ban-nen-100m-odt-nhua-4m-view-song-cach-cho-base-500m-gia-790tr-lh-van-pr39398686' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/25/20240325102600-2990_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/200x200/2024/03/24/20240324112231-78ba_wm.jpg' alt='' />
                            '''
            elif dat_entity == "thot not" and price_entity == "800" and property_type_entity == "đất chưa sử dụng":
                response = '''<li></li>'''

            else:
                response = f"theo thông tin của bạn ở quận {dat_entity} với mức giá khoảng {price_entity} triệu hiện tại chưa có bất động sản nào được tìm thấy bạn vui lòng chọn địa điểm khác và giá khác để tôi có thể tư vấn cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("dat_e", dat_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về loại đất, quận và mức giá. bạn vui lòng cung cấp thêm thông tin để tôi có thể tư vấn kỹ hơn cho bạn.")
            return []
        
class XacNhanNhaAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_nha"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nha_entity = next(tracker.get_latest_entity_values('nha_e'), None)
        print(nha_entity)
        price_entity = next(tracker.get_latest_entity_values('price'), None)

        if nha_entity and price_entity:
            if nha_entity == "ninh kieu" and price_entity == "500":
                print(nha_entity)
                response = "Theo thông tin của bạn, bạn quan tâm đến nhà ở quận Ninh Kiều với mức giá 500 triệu. Tôi sẽ tìm kiếm thông tin cho bạn."
            elif nha_entity == "cai rang" and price_entity == "600":
                response = "Dựa vào yêu cầu của bạn, bạn muốn tìm kiếm nhà ở quận Cái Răng với mức giá 600 triệu. Tôi sẽ bắt đầu tìm kiếm ngay."
            else:
                response = f"Bạn quan tâm đến nhà ở quận {nha_entity} với mức giá khoảng {price_entity}. Tôi sẽ tìm kiếm thông tin cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("nha_e", nha_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về quận và mức giá.")
            return []
    
class XacNhanDatAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_canho"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        can_ho_entity = next(tracker.get_latest_entity_values('can_ho_e'), None)
        print(can_ho_entity)
        price_entity = next(tracker.get_latest_entity_values('price'), None)

        if can_ho_entity and price_entity:
            if can_ho_entity == "ninh kieu" and price_entity == "500":
                print(can_ho_entity)
                response = "<p>hihi <img src='static/img/canho_1.jpg' alt='' /></p><p>hihi <img src='static/img/canho_2.jpg' alt='' /></p>"
            elif can_ho_entity == "cai rang" and price_entity == "600":
                response = "Dựa vào yêu cầu của bạn, bạn muốn tìm kiếm căn hộ ở quận Cái Răng với mức giá 600 triệu. Tôi sẽ bắt đầu tìm kiếm ngay."
            else:
                response = f"Bạn quan tâm đến căn hộ ở quận {can_ho_entity} với mức giá khoảng {price_entity}. Tôi sẽ tìm kiếm thông tin cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("can_ho_e", can_ho_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về quận và mức giá.")
            return []
        

