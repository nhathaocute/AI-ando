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
            "bạn muốn chọn bất động sản nào trong những lựa chọn sau: nhà ở, căn hộ, đất nền",
            "bạn muốn xem bất động sản ở khu vực nào? tôi chỉ có thể trả lời bạn trong các lĩnh vực: nhà ở, căn hộ, đất nền.",
            "Bạn muốn biết thông tin về nhà ở, căn hộ, đất nền?",
            "Bạn cần thông tin chi tiết về loại hình bất động sản nào? nhà ở, căn hộ, đất nền.",
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
                response = "Tôi sẽ tìm thông tin về đất cho bạn. Xin vui lòng cho biết loại (đất nền hay đất mặt tiền), quận và giá bạn quan tâm."

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
    
class XacNhanGiaDatAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_giadat"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        giadat_entity = next(tracker.get_latest_entity_values("giadat"), None)
        print(giadat_entity)

        if giadat_entity:
            if giadat_entity == "quan ninh kieu" or giadat_entity == "quận ninh kiều":
                response = "Theo thông tin của tôi giá đất ở quận ninh kiều dao động trong khoảng từ 35 triệu/m² đến 120 triệu/m² tùy theo từng khu vực đông dân hay thưa thớt khác nhau và nó có thể tăng hoặc giảm hơn dự đoán của tôi."
                dispatcher.utter_message(text=response)
            elif giadat_entity == "quan cai rang" or giadat_entity == "quận cái răng":
                response = "Theo thông tin của tôi giá đất ở quận cái răng dao động trong khoảng từ 10 triệu/m² đến 100 triệu/m² tùy theo từng khu vực đông dân hay thưa thớt khác nhau và nó có thể tăng hoặc giảm hơn dự đoán của tôi."
                dispatcher.utter_message(text=response)
            elif giadat_entity == "quan binh thuy" or giadat_entity == "quận bình thủy":
                response = "Theo thông tin của tôi giá đất ở quận bình thủy dao động trong khoảng từ 4 triệu/m² đến 50 triệu/m² tùy theo từng khu vực đông dân hay thưa thớt khác nhau và nó có thể tăng hoặc giảm hơn dự đoán của tôi."
                dispatcher.utter_message(text=response)
            elif giadat_entity == "quan thot not" or giadat_entity == "quận thốt nốt":
                response = "Theo thông tin của tôi giá đất ở quận thốt nốt dao động trong khoảng từ 5 triệu/m² đến 10 triệu/m² tùy theo từng khu vực đông dân hay thưa thớt khác nhau và nó có thể tăng hoặc giảm hơn dự đoán của tôi."
                dispatcher.utter_message(text=response)
            else:
                response = "Tôi không thể xác định nơi mà bạn yêu cầu"
                dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Tôi không thể xác nơi mà bạn yêu cầu")
        
        return [SlotSet("giadat", giadat_entity)]

    
class TimTTLoaiBDSAction(Action):

    def name(self) -> Text:
        return "action_loai_bds"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        lbds_entity = next(tracker.get_latest_entity_values("lbds"), None)
        print(lbds_entity)

        if lbds_entity == "đất nền" or lbds_entity == "dat nen":
            response = "Đất nền là loại bất động sản được sử dụng để xây dựng các công trình nhà ở hoặc cơ sở kinh doanh. Thường được sử dụng để phân lô, bán lẻ hoặc đầu tư."
        elif lbds_entity == "đất mặt tiền" or lbds_entity == "dat mat tien":
            response = "đất mặt tiền là đất trống, chưa có cơ sở hạ tầng hoặc công trình xây dựng nào được xây dựng trên đó."
        elif lbds_entity == "nhà phố" or lbds_entity == "nha pho":
            response = "Nhà phố là loại bất động sản là các căn nhà đơn lập, liền kề, thường được xây dựng trên một khu đất nhỏ và chia thành các căn riêng biệt."
        elif lbds_entity == "nhà gia đình" or lbds_entity == "nha gia dinh":
            response = "Nhà gia đình là những căn nhà dành cho một gia đình sống, thường có diện tích đất rộng và nhiều phòng để phục vụ cho nhu cầu của gia đình."
        elif lbds_entity == "căn hộ chung cư" or lbds_entity == "can ho chung cu":
            response = "Căn hộ chung cư là các căn hộ nằm trong các tòa nhà cao tầng, có thể chia thành nhiều căn hộ riêng lẻ và chia sẻ các tiện ích chung của tòa nhà."
        elif lbds_entity == "căn hộ dịch vụ" or lbds_entity == "can ho dich vu":
            response = "Căn hộ dịch vụ là các căn hộ được thiết kế và trang bị đầy đủ tiện nghi, dành cho thuê ngắn hạn hoặc dài hạn, thường đi kèm với các dịch vụ tiện ích như dọn dẹp hàng ngày, bảo trì, an ninh, vv."
        else:
            response = "Xin lỗi, tôi không thể giải thích loại bất động sản này."

        # Phản hồi cho người dùng
        dispatcher.utter_message(response)

        return []
class TimTTDuongBDSAction(Action):

    def name(self) -> Text:
        return "action_duong_bds"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        lbds_entity = next(tracker.get_latest_entity_values("dia_diem"), None)
        print(lbds_entity)

        if lbds_entity == "đường nguyễn văn cừ":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>BÁN NỀN CÓ NHÀ LẦU (cũ) 2MT NGUYỄN ĐỆ, PHƯỜNG AN HÒA, NKCT</h2>
                            <li>BÁN NỀN CÓ NHÀ LẦU (cũ) 2MT NGUYỄN ĐỆ, PHƯỜNG AN HÒA, NKCT
                                - Diện tích : 6x16,35 (100m²) ODT 100%
                                - DTSD: 123m²
                                - Sổ hồng hoàn công
                                - Hướng : Tây bắc - Đông bắc
                                - Hẻm trước và sau : 4m
                                - Vị trí nhà đẹp Kv an ninh,gần chợ,trường học ....
                            </li>
                            </br>
                            Diện tích: 100 m²
                            Mức giá: 4,15 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-phuong-an-hoa-2/b-nen-co-nha-lau-cu-2mt-nguyen-de-nkct-pr39623158' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417165048-88b5_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417165048-5345_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417165049-dd02_wm.jpg' alt='' />
                            <h3>hoặc</h3>
                            </br>
                            <h2>Bán dãy trọ 16 phòng tại đường Nguyễn Văn Cừ Cần Thơ</h2>
                            <li>
                            Bán dãy trọ 16 phòng tại đường Nguyễn Văn Cừ - Cần Thơ.
                            - Vị trí: Hẻm thông 311, Đường Nguyễn Văn Cừ, P. An Hoà, Q. Ninh Kiều, TP. Cần Thơ.
                            - Diện tích tổng khu: 14 x 24,5m = 342,9m².
                            - Pháp lý: Thổ cư 100%.
                            - Hướng: Tây Bắc.
                            - Lộ: 2 mặt tiền, ô tô tới phía trước.
                            - Giá mới: 11tỷ9.
                            </li>
                            </br>
                            Diện tích: 342,9 m²
                            Mức giá: 11,9 tỷ
                            Mặt tiền: 14 m
                            Số phòng: 16 phòng
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-rieng-duong-nguyen-van-cu-1-phuong-an-hoa-2/ban-day-tro-16-phong-tai-can-tho-pr39642656' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/20/20240420101258-ac86_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/20/20240420101259-3862_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường nguyễn văn linh":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Bán nhà mặt tiền đường Lê Bình. Phường Hưng Lợi, Q Ninh Kiều, TP Cần Thơ</h2>
                            <li>
                            Bán nhà mặt tiền đường Lê Bình. Phường Hưng Lợi, Q Ninh Kiều, TP Cần Thơ.
                            ĐC: Đường Lê Bình, Phường Hưng Lợi, Q Ninh Kiều, TP Cần Thơ.
                            + Diện tích: 5,05m x 15,1m = 73,8m².
                            + Kết cấu: Nhà 1 trệt 2 lầu, đã hoàn công.
                            + DT sàn: 211,2m².
                            + Giá bán: 10,5 tỷ (thương lượng).
                            + Vị trí: Nhà thích hợp, kinh doanh mua bán.
                            </li>
                            </br>
                            Diện tích: 73,8 m²
                            Mặt tiền: 5,05 m
                            Mức giá: 10,5 tỷ
                            Số tầng: 3 tầng
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-mat-pho-duong-le-binh-phuong-hung-loi/ban-tien-q-ninh-kieu-tp-can-tho-pr39639358' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419192728-7f0c_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419192728-c881_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường hoàng quốc việt":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường mạc thiên tích":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Bán nhà 4 tầng mặt tiền Mạc Thiên Tích giá chỉ 4,5 tỷ. Đối diện chợ Xuân Khánh</h2>
                            <li>
                            Bán nhà 4 tầng mặt tiền Mạc Thiên Tích giá chỉ 4,5 tỷ. Đối diện chợ Xuân Khánh.
                            + Diện tích đất: 2,8 x 11 = 30,2m².
                            + Diện tích sử dụng: 130 m² (1 trệt 3 lầu).
                            + Lộ nhựa 5m, lề 3,3m.
                            + 4 toilet (mỗi tầng 1 toilet), 3 phòng tắm kính cường lực.
                            + 3 máy nước nóng & 3 máy lạnh.
                            + Vị trí tiện ích: Gần sông thoáng mát (cách 4 căn nhà là tới đường Nguyễn Thị Minh Khai), đối diện hông chợ Xuân Khánh, xéo trường tiểu học Tô Hiến Thành, trước nhà đang làm đường nối với Vincom và công viên tiểu cảnh.
                            + Giá: 4,5 tỷ (thương lượng).
                            </li>
                            </br>
                            Diện tích: 30,2 m²  
                            Mặt tiền: 2,8 m
                            Mức giá: 4,5 tỷ
                            Số tầng: 4 tầng
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-mat-pho-pho-mac-thien-tich-phuong-xuan-khanh/ban-4-tang-tien-gia-chi-4-5-ty-doi-dien-cho-khanh-pr39639554' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419200536-f565_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419200537-0c30_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419200536-241b_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419200537-6691_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường 3 tháng 2" or lbds_entity == "đường 3/2":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>NHÀ LẦU LỬNG RỘNG MÊNH MÔNG - VỊ TRÍ ĐẸP - HẺM 694 ĐƯỜNG 3/2, NINH KIỀU, CẦN THƠ</h2>
                            <li>Giá: 2 tỷ 650 triệu (thương lượng)
                            NHÀ LẦU LỬNG RỘNG MÊNH MÔNG - VỊ TRÍ ĐẸP - HẺM 694 ĐƯỜNG 3/2, NINH KIỀU, CẦN THƠ
                            ----------------------------------------
                            - Diện tích: 5 17,8 = 88,7m² - Hướng: Đông Bắc.
                            - Pháp lý: Đất thổ cư 65m², CLN 23,7m². Nhà đã có sổ hồng hoàn công.
                            - Lộ giới: Lộ 4m đã nâng cấp
                            - Kết cấu: Nhà lầu lửng, mâm đúc, mới đẹp, thoáng mát và nhiều ánh sáng - Gồm: Sân đậu xe có cổng rào, phòng khách, phòng ăn, bếp, 2 phòng ngủ, 2 toilet, phòng thờ,... Xung quanh có đủ các tiện ích sống: Công viên, trường học, chợ, siêu thị, bệnh viện, trung tâm mua sắm, khu vui chơi giải trí,....
                            </li>
                            </br>
                            Diện tích: 88,7 m²
                            Mức giá: 2,65 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-rieng-duong-3-2-2-phuong-an-binh-2/-lau-lung-rong-menh-mong-vi-tri-dep-hem-694-3-2-ninh-kieu-can-tho-pr39646230' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/20/20240420161308-9e6c_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/20/20240420161306-81ac_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/20/20240420161305-4ce8_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường 30 tháng 4" or lbds_entity == "đường 30 tháng tư" or lbds_entity == "đường 30/tư":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Nhà siêu đẹp full nội thất hẻm 553 Đường 30/4, phường Hưng Lợi, quận Ninh Kiều, Cần Thơ</h2>
                            <li>Bán nhà mới xây tuyệt đẹp hẻm 553 Đường 30/4, P. Hưng Lợi, Q. Ninh Kiều, Cần Thơ.
                            - Diện tích: 10m x 4m = 40m.
                            - Diện tích sử dụng 80m.
                            - Lộ giới: 3m.
                            - Pháp lý: Sổ hồng thổ cư 100%, GPXD chính.
                            - Hướng: Tây Bắc.
                            - Nhà gồm: Phòng khách, bếp, 2 toillet, sân đậu xe máy, 2 phòng ngủ, sân phơi,... Tặng toàn bộ nội thất có sẵn trong nhà.
                            - Vị trí Cách trục chính 15m, cách đường 30/4 100m, ngay Trung tâm phường Hưng Lợi, bán kính 500m đầy đủ mọi tiện ích.
                            - Giá bán: 2 tỷ 490 triệu (thương lượng).</li>
                            </br>
                            Diện tích: 40 m²
                            Mặt tiền: 10 m
                            Mức giá: 2,49 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-rieng-duong-30-4-1-phuong-hung-loi/-sieu-dep-full-noi-that-hem-553-30-4-quan-ninh-kieu-can-tho-pr39616179' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417081736-7c1d_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417081708-c42b_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417081708-7e92_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417081708-9b88_wm.jpg ' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/17/20240417081708-1ab1_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "đường trần hoàng na":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Bán nền thổ cư DT 4,2 x 13=52m2 hẻm 50 trần hoàng na p hưng lợi giá 1 tỷ 450</h2>
                            <li>Nền thổ cư Hưng Lợi Q Ninh Kiều. TP Cần Thơ.
                                Cần bán nhanh nền thổ cư 52m².
                                Nền thổ cư - hẻm 60 Trần Hoàng Na. P Hưng Lợi Q Ninh Kiều TP Cần Thơ.
                                Diện tích 4.2 x 12.6=52m².
                                Thổ cư 100%.
                                Mặt tiền hẻm 3,5m cách Trần Hoàng Na 150m.
                                Nền 2 mặt tiền, tiện xây nhà ở, hoặc mua đầu tư tích lũy lâu dài.
                                Vị trí: Bán kinh 1,5km đầy đủ tiện ích, trường học các cấp, Vincom Plaza Xuân Khánh 1Km, trường ĐTCT, Bv Đa khoa QT VinMec, bến xe Cần Thơ 500m...
                                Giá 1,45 tỷ (Thương lượng chính chủ).
                            </li>
                            </br>
                            Diện tích: 52 m²
                            Mức giá: 1,45 tỷ
                            Mặt tiền: 4,2 m
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tran-hoang-na-phuong-hung-loi/gia-dinh-can-ban-nhanh-nen-tho-cu-q-ninh-kieu-tp-can-tho-gia-9-chu-pr38995715' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/08/20240308055636-f661_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/08/20240308055636-95a3_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/08/20240308055635-ac16_wm.jpg' alt='' />
                            <h3>hoặc</h3>
                            </br>
                            <h2>Giá cực sốc MT Trần Hoàng Na, P. Hưng Lợi, Ninh Kiều, Cần Thơ gần BV Đa khoa Cần Thơ 120m2 (SHR)</h2>
                            <li>
                            Giá cực sốc giá thỏa thuận MT Trần Hoàng Na, P. Hưng Lợi, Ninh Kiều, Cần Thơ gần BV Đa khoa Cần Thơ 120m (SHR).
                                - Giá chốt.
                                - Diện tích 120m² (ngang 6m dài 20m). Trong đó có 120m² thổ cư, bao giấy phép xây dựng.
                                - Vị trí đắc địa gần trường cao đẳng Cần Thơ, Bệnh viện ĐK Cần Thơ, khách sạn, nhà trọ, dân cư đông đúc.
                                - Không dính quy hoạch.
                                - Đường hiện hữu 12m.
                                - Đất 100% được thổ cư - sổ hồng riêng sang tên công chứng ngay.
                                - Thích hợp để đầu tư và kinh doanh.
                            </li>
                            </br>
                            Diện tích: 120 m²
                            Mức giá: Thỏa thuận
                            Mặt tiền: 6 m
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tran-hoang-na-phuong-hung-loi/gia-cuc-soc-mt-p-ninh-kieu-can-tho-gan-bv-da-khoa-can-tho-550tr-120m2-shr-pr39627220' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/18/20240418105842-0f27_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/18/20240418105842-0f27_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "hẻm 51":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>NHÀ TRỆT LỮNG hẻm 51 GẦN ĐẠI HỌC CẦN THƠ LỘ TRƯỚC NHÀ 4m</h2>
                            <li>Nhà trệt lững hẻm 51 gần Đại học Cần Thơ
                                Bán: 1 tỷ 290 tr (thương lượng)
                                - Vị trí: Hẻm 51, Đường 3/2 P. Xuân Khánh, Ninh Kiều
                                - Dt: 4 x 8,5 = 33,6m². Dtsd: 45m2
                                - PL: CLN (Có xác nhận 3.0) - Lên TC (khoảng 100 tr)
                                - Hẻm 4m - Ô tô tới nhà
                                - Hướng: Tây Bắc
                                - Kết cấu : Sân đậu xe, phòng khách, 2 phòng ngủ
                                Nhà nằm sát vách Đại Học CT, KV rất an ninh,
                                nhà rất phù hợp cho: Học sinh, SV, GĐ CBCC trẻ,...
                            </li>
                            </br>
                            Diện tích: 33,6 m²
                            Mức giá: 1,29 tỷ
                            Mặt tiền: 4 m
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tran-hoang-na-phuong-hung-loi/gia-dinh-can-ban-nhanh-nen-tho-cu-q-ninh-kieu-tp-can-tho-gia-9-chu-pr38995715' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421000155-be4f_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421000155-6112_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421000155-5638_wm.jpg' alt='' />
                            <h3>hoặc</h3>
                            </br>
                            <h2>Bán nền mặt tiền đường bờ Hồ Bún Xáng (hẻm 51)</h2>
                            <li>
                            Bán nền mặt tiền đường bờ Hồ Bún Xáng (hẻm 51).
                            ĐC: Đường Bờ Hồ Búng Xáng, Phường An Khánh, Q Ninh Kiều, TP Cần Thơ.
                            + Diện tích: 7,51m x 24,5m = 152,7m².
                            + Kết cấu: Nền nhà trệt.
                            + Giá bán: 12,5 tỷ (thương lượng).
                            + Vị trí: Nhà thích hợp, kinh doanh mua bán.
                            </li>
                            </br>
                            Diện tích: 152,7 m²
                            Mức giá: 12,5 tỷ
                            Mặt tiền: 7,51 m
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-ho-bun-xang-phuong-an-khanh-1/ban-nen-mat-tien-bo-bung-hem-51-pr39639372' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419193126-135b_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/19/20240419193126-4034_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "khu dân cư 91b":
            response = '''<h3>dưới đây là một số bất động sản gần đó:</h3>
                            </br>
                            <h2>Bán nhà trệt 2 lầu đường B11 KDC 91B có hẻm kỹ thuật</h2>
                            <li>
                            Nhà 1 trệt 2 lầu cao cấp đường B11 KDC 91B có hẻm kĩ thuật bên hông và sau rất thoáng mát - cách Mặt tiền Trần Hoàng Na 50m.
                            Thiết kế đẹp với 1 phòng khách - bếp - 3 phòng ngủ - 1 phòng thờ - 4WC - nhà nội thất cao cấp gỗ căm se, bồn tắm, gạch nhập khẩu, năng lượng mặt trời, máy lạnh,... - nhà gió lộng mát quanh năm với rất nhiều cửa sổ tạo sự thoải mái ko ngột ngạt,.... Đảm bảo sẽ làm hài lòng những vị khách khó tính.
                            Dt: 4 x 16 m, sổ hồng hoàn công.
                            Lộ giới 7m - lề 3m.
                            Giá: 5 tỷ 800 tr (thương lượng).
                            Hỗ trợ vay ngân hàng lãi suất ưu đãi.
                            Gặp Tài.
                            </li>
                            </br>
                            Diện tích: 64 m²
                            Mặt tiền: 4 m
                            Mức giá: 5,8 tỷ     
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-nha-rieng-duong-b11-phuong-an-khanh-1/ban-tret-2-lau-kdc-91b-co-hem-ky-thuat-pr39576548' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125614-fbeb_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125614-cfe9_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125615-7a30_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125615-65a9_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125614-1ea7_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125615-3390_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412125615-efaf_wm.jpg' alt='' />
                            '''
        elif lbds_entity == "khu dân cư hồng loan":
            response = '''xin lỗi tôi chưa tìm thấy bất động sản ở khu vực này
                            '''
        elif lbds_entity == "hẻm 132":
            response = '''xin lỗi tôi chưa tìm thấy bất động sản ở khu vực này
                            '''
        else:
            response = "Xin lỗi, tôi không thể tìm được bất động sản gần khu vực này"


        dispatcher.utter_message(response)

        return []



class XacNhanDatAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_dat"

    @staticmethod
    def convert_price_to_number(price_str: Text) -> float:
    # Chuyển đổi từ tiếng Việt sang số
        vietnamese_numbers = {
            "một": "1",
            "hai": "2",
            "ba": "3",
            "bốn": "4",
            "năm": "5",
            "sáu": "6",
            "bảy": "7",
            "tám": "8",
            "chín": "9",
            "mươi": "0",  # Bổ sung cho trường hợp "mười" để tránh lỗi ValueError
        }
        for word, num in vietnamese_numbers.items():
            price_str = price_str.replace(word, num)

        # Xóa các ký tự không cần thiết và chuyển đổi thành chữ thường
        price_str = price_str.lower().replace(" ", "").replace("tỷ", "").replace("ty", "")

        # Xóa dấu phẩy nếu có
        price_str = price_str.replace(",", "")

        # Nếu có dấu chấm thì chuyển thành phần nguyên và phần thập phân
        if "." in price_str or "," in price_str:
            integer_part, decimal_part = price_str.split(".")
            if integer_part.isdigit() and decimal_part.isdigit():
                # Nếu cả phần nguyên và phần thập phân đều là số, kết hợp lại và chuyển đổi thành float
                return float(integer_part + decimal_part) * 1000  # Chuyển từ tỷ sang triệu
            else:
                return 0.0
        elif "triệu" in price_str:
            # Nếu chuỗi chứa từ "triệu", xóa từ đó và chuyển đổi thành số float
            price_str = price_str.replace("triệu", "").replace("trieu", "")
            if "." in price_str or "," in price_str:
                integer_part, decimal_part = price_str.split(".")
                if integer_part.isdigit() and decimal_part.isdigit():
                    return float(integer_part + decimal_part)
                else:
                    return 0.0
            elif price_str.isdigit():
                return float(price_str)
            else:
                return 0.0
        elif price_str.isdigit():
            # Nếu chuỗi chỉ chứa các chữ số, chuyển đổi thành số float
            return float(price_str) * 1000  # Chuyển từ tỷ sang triệu
        else:
            # Nếu không, trả về 0
            return 0.0

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
            dat_entity = dat_entity.lower().strip()
            price_value = self.convert_price_to_number(price_entity)

            print('price_value =', price_value)
            if (300 <= int(price_value) <= 800
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat nen", "đất nền"]):
               
                response = '''<h3>đây là một số bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Sang nhượng gấp lô đất Đ. Hoàng Quốc Việt, An Khánh, Ninh Kiều. Cần Thơ 120m2. SHR sang tên</h2>
                            <li>
                             Lô đất kế bên sân bóng mini 442, nằm ngay mặt tiền Đường Hoàng Quốc Việt. Phường An Khánh, Ninh Kiều, Cần Thơ.
                                Diện tích 120m².
                                Bao phí sang tên.
                                Đất full thổ 100%, pháp lý rỏ ràng, sổ hồng riêng sang tên ngay.
                                Khu vực dân cư đông đúc thích hợp kinh doanh buôn bán, xây dựng đinh cư lâu dài. Tiện ích bán kính 2km gần chợ An Bình, chợ Nổi Cái Răng, Bách Hoá Xanh, Điện Máy Xanh, bệnh viện Y Học Cổ Truyền, trường THPT Nguyễn Việt Hồng,...
                            </li>
                            </br>
                            Diện tích: 120 m²
                            Mức giá: 750 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-khanh-1/sg-nhuong-gap-lo-d-khh-ninh-kieu-c-tho-120m2-550tr-shr-sg-ten-pr39520536' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/08/20240408192703-e2fe_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/08/20240408192702-051d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là một số bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Gia đình đi Mỹ cần bán gấp lô đất cạnh khu biệt thự Cồn Khương 178m2 giá chỉ 999 triệu</h2>
                            <li>
                             Gia đình đi Mỹ cần bán gấp lô đất tại vị trí đắc địa số 1 thành phố Cần Thơ, vừa thích hợp đầu tư, vừa an cư, nghỉ dưỡng..
Diện tích 178m² (88m² sử dụng và 90m đường đi) giá chỉ 999 triệu.
Vị trí đất ngay khu trung tâm Cồn Khương, sát bên khu biệt thự đẳng cấp nhất Cần Thơ.
Dễ dàng kết nối đến trung tâm tỉnh ủy Cần Thơ với đầy đủ các tiện ích thành phố như: Vincom Cần Thơ, Sense City, Bến Ninh Kiều, hệ thống trường học các cấp, trường đại học Cần Thơ, Đại Học Y Dược Cần Thơ, khu resort nghỉ dưỡng cao cấp..
Hiện tại cần bán gấp trong tháng ba, giá chốt nhanh 999 triệu.
                            </li>
                            </br>
                            Diện tích: 178 m²
                            Mặt tiền: 8 m
                            Mức giá: 999 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-phuong-cai-the/gia-dinh-di-my-can-ban-gap-lo-canh-khu-biet-thu-con-khuong-178m2-gia-chi-999-trieu-pr39186892' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/02/28/20240228161110-e877_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/02/28/20240228161110-0d7b_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là một số bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất nền trung tâm TP. Cần Thơ - Cạnh Lotte</h2>
                            <li>
                             Chính chủ bán nền siêu đẹp full ODT - cách MT Nguyễn Văn Cừ - P. An Hòa - Quận Ninh Kiều (40m) - cao ráo không ngập - hẻm nâng cấp đô thị.
- Diện tích: 82.5m² (5.5x15).
- Hướng: Đông Bắc.
- Pháp lý: Sổ hồng.
- Lộ giới hẻm: Trên giấy 2,7m - thực tế đã nâng cấp lên 5m (đoạn trước nền 6m).
- Sử dụng: Cất nhà ở định cư lâu dài.
- Tiện ích: Hẻm đối diện UBND P. An hòa, gần CA quận Ninh Kiều, chợ An Hòa, ST Vincom Plaza, Lotte, các trường cấp 1,2,3, cao đẳng, đại học (công nghệ, y dược)...
                            </li>
                            </br>
                            Diện tích: 82,5 m²
                            Mặt tiền: 5,5 m
                            Mức giá: 3,72 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-nguyen-van-cu-1-phuong-an-hoa-2/-nen-trung-tam-tp-can-tho-canh-lotte-pr39687558' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/25/20240425090813-f2c8_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/25/20240425090827-d05e_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat nen", "đất nền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán nền đẹp 205m2 - sổ hồng đất vườn - 590tr - gần bến xe trung tâm TP Cần Thơ - Cái Răng - Cần Thơ</h2>
                            <li>
                             Chu gửi nền giá rẻ nhất Cái Răng - sổ hồng 205m² - 590tr.
Đã bán 1 nền còn 1 nền duy nhất thích hợp đầu tư lâu dài.
Bán nền đẹp 205m² - sổ hồng đất vườn - gần bến xe trung tâm TP Cần Thơ - Tại P. Thường Thạnh, Q. Cái Răng, Tp. Cần Thơ.
Vị trí: Cách KDC Hồng Loan và Bến xe và Cầu Trần Hoàng Na chỉ tầm 2.5km.
- DT đất: 10 x 20 = 205m².
- Lộ đất 2,5m - nền vuông đẹp.
- Pháp lý: Sổ hồng đất vườn CLN, sang tên ngay.
- Vị trí: Nền cách gần KDC Hồng Loan, Cầu Trần Hoàng Na sắp thông xe, nền cách bến xe Trung Tâm và Khu Hồng Loan chỉ ~2.5km. Thích hợp cất nhà ở sân vườn, mua đầu tư dài hạn.
Giá bán chỉ: 590 triệu. (GD TL gặp chính chủ).
(Giá củ 680 triệu, đã giảm 90 triệu ra nhanh).
                            </li>
                            </br>
                            Diện tích: 205 m²
                            Mặt tiền: 10 m
                            Mức giá: 590 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hang-gon-phuong-thuong-thanh/ban-nen-dep-205m2-so-hong-vuon-590tr-gan-ben-xe-trung-tam-tp-can-tho-cai-rang-can-tho-pr39499602' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/04/20240404125746-a604_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/04/20240404125750-ec50_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Chính chủ bán đất ở Hưng Thạnh - Cái Răng, full thổ cư giá chỉ 850 triệu, liên hệ Thảo 0772 881 ***</h2>
                            <li>
                             Địa chỉ: Khu vực 5, phường Hưng Thạnh, quận Cái Răng, TP Cần Thơ.
Diện tích: 62,2m², full thổ cư.
Nền đã bơm cát, lộ trước nền 3,5m, kế bên Khu dân cư Hồng Loan (cách con kênh 6m có cầu bắt qua), xung quanh nền đã cất nhà.
Nền đất đang trong khu quy hoạch treo (dự án công viên cây xanh), cho cấp giấy phép xây dựng tạm.
Nền gần Trường ĐH Tây Đô, gần Bệnh Viện Đại Học Nam Cần Thơ, gần bến xe.
Giá bán: 850 triệu.
                            </li>
                            </br>
                            Diện tích: 62,2 m²
                            Mức giá: 850 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-phuong-hung-thanh/chinh-chu-ban-o-cai-rang-full-tho-cu-gia-chi-790tr-lien-he-thao-0772881989-pr37228187' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2023/05/15/20230515114930-2f47_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2023/05/15/20230515114931-20c7_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Nền 121,5m2 - khu Xây Dựng (giáp khu dân cư Nam Long)</h2>
                            <li>
                             Bán nền khu Xây Dựng (Giáp khu dân cư Nam Long) - P. Hưng Thạnh - Q. Cái Răng - TP. Cần Thơ.
Nền diện tích: Ngang 6m dài 21,24m = 121,5m² (Thổ cư 100%).
Pháp lý: Sổ hồng - sang tên ngay.
Hướng: Đông Bắc.
Lộ giới: 15m.
Giá bán: 3,7 tỷ (Thương lượng với chủ đất).
                            </li>
                            </br>
                            Diện tích: 121,5 m²
                            Mặt tiền: 6 m
                            Mức giá: 3,7 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-3-8-phuong-hung-thanh/nen-121-5m2-khu-xay-dung-giap-khu-dan-cu-nam-long-pr39489516' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/03/20240403135941-634a_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/03/20240403140001-e0ff_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat nen", "đất nền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Nền đối diện BV Nhi Đồng cần bán gấp DT 4,5x17m, CLN LG 5m. LH 0976 331 ***</h2>
                            <li>
                             Hàng ngộp giá chỉ 450tr/ nền.
Nền đối diện BV Nhi Đồng, cách Nguyễn Văn Cừ 400m.
Diện tích 4.5m x17m đất vườn.
Lộ giới 5m, hướng Đông Nam.
                            </li>
                            </br>
                            Diện tích: 77 m²
                            Mặt tiền: 5 m
                            Mức giá: 450 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-nguyen-van-cu-1-phuong-long-tuyen/nen-doi-dien-bv-nhi-dong-can-ban-gap-dt-4-5x17-cln-lg-5m-lh-pr39663051' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422223856-1b98_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422223856-70b8_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán nền thổ cư cấp phép xây dựng 1T1L - gần ĐH FPT, Nhi Đồng Cần Thơ giá 1 tỷ 50 triệu</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 49,5 m²
                            Mặt tiền: 9.63 m
                            Mức giá: 1,05 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-ta-thi-phi-phuong-long-tuyen/ban-nen-tho-cu-cap-phep-xay-dung-1t1l-gan-dh-fpt-nhi-dong-can-tho-gia-1-ty-50-trieu-pr39538260' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/08/20240408224627-9774_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/08/20240408224626-d872_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán 186,5m2 đất thổ cư, Rạch Ngã Bát, P. Long Tuyền, TP Cần Thơ, 2.7 tỷ</h2>
                            <li>
                             Bán đất full thổ cư, Rạch Ngã Bát, P. Long Tuyền, TP. Cần Thơ.
- Lộ bê tông 4m, đối diện rạch thoáng mát.
- Diện tích: 7,47 x 26 = 186,5m² (nở hậu 8,6m).
Giá bán: 2,7 tỷ.
- Pháp lý sổ hồng full thổ cư.
* Vị trí nền bán kính 1km gồm có BV Nhi Đồng, đại học FPT, BV SIS, đại học Nam Cần Thơ,...
                            </li>
                            </br>
                            Diện tích: 186,5 m²
                            Mặt tiền: 7,47 m
                            Mức giá: 2,7 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-ta-thi-phi-phuong-long-tuyen/ban-186-5m2-tho-cu-rach-nga-bat-p-tp-can-tho-2-7-ty-pr39489400' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/03/20240403134907-f15c_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/03/20240403134907-75af_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat nen", "đất nền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán nền thổ cư đường bê tông 2m xã Tân Thới</h2>
                            <li>
                             Cần tiền bán nền thuộc - Tân Thới - Phong Điền - Tp Cần Thơ.
Ngan 5,3m.
Dài 26m.
Thổ cư + cây lâu năm.
Nền 2 mặt tiền lộ 2 m + thêm mặt tiền sông cầu nhiếm (lộ giới đã hợp dân dự mở 4M).
Khu dân cư đông đúc bán kính 600m trường học mầm non cắp 1, 2, chợ cầu nhiếm bách hoá xanh thích hợp định cư lâu dài.
Giá 450 triệu.
                            </li>
                            </br>
                            Diện tích: 137,8 m²
                            Mặt tiền: 5 m
                            Mức giá: 450 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-xa-tan-thoi/ban-nen-tho-cu-duong-be-tong-2m-ca-thoi-pr39662673' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422212123-a19d_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/200x200/2024/04/22/20240422212123-a11b_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán nền đường số 18 thị trấn Phong Điền</h2>
                            <li>
                             Bán 2 nền đường Số 18 TTTM. Phong Điền, TPCT.
- Diện tích: 5x12 = 60m² giá 1,250 tỷ.
- Diện tích: 5x18 = 90m² giá 1,690 tỷ.
* Vị trí cách chợ chỉ 200m tiện kinh doanh mua bán.
                            </li>
                            </br>
                            Diện tích: 60 m²  
                            Mức giá: 1,25 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-so-18-thi-tran-phong-dien/ban-nen-18-dien-pr39590471' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/14/20240414081805-8bed_wm.jpg' alt='' />
                             '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat nen", "đất nền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Chỉ 1 tỷ 450tr đã sở hữu nền ĐS 16 TTTM huyện Phong Điền TP Cần Thơ (Cách Nguyễn Văn Cừ 100m)</h2>
                            <li>
                             Bán nền số 16 đường số 08 TTTM Phong Điền (cách Nguyễn Văn Cừ đúng 100m).
- Diện tích: 4 x 19.5 = 78m².
- Sổ hồng thổ cư.
                            </li>
                            </br>
                            Diện tích: 78 m²
                            Mặt tiền: 4 m
                            Mức giá: 1,45 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-so-16-thi-tran-phong-dien/chi-1-ty-450tr-da-huu-nen-ds-16-tttm-huyen-tp-can-tho-cach-nguyen-van-cu-100m-pr39570029' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/12/20240412081631-bb1a_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/200x200/2024/04/12/20240412081631-bb1a_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Siêu phẩm đất nền 100m2 trục Trần Hoàng Na, Ninh Kiều giá 690tr gần trường học, bệnh viện SHR</h2>
                            <li>
                             - Vị trí: Mặt tiền trục đường Trần Hoàng Na, Ninh Kiều, Cần Thơ.
Gần các trường cao đẳng, đại học, gần bệnh viện nhi Cần Thơ, bệnh viện trung ương Đa Khoa Cần Thơ, dân cư đông, sắp khánh thành cầu Trần Hoàng Na rút ngắn đường tới bến xe trung tâm và kết nối nhiều tuyến đường thuận tiện. Đầu tư siêu lợi nhuận.
DT: 100m² 5x20m, full thổ, xây dựng tự do.
- Sổ hồng riêng, công chứng trong ngày.
- Hạ tầng hoàn thiện 100%, đường rộng thông tứ phía.
giá 690tr
                            </li>
                            </br>
                            Diện tích: 100 m²
                            Mặt tiền: 5 m
                            Mức giá: 690 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tran-hoang-na-phuong-an-binh-2/sieu-pham-nen-100m2-mt-ninh-kieu-can-tho-chi-600tr-gan-truong-hoc-benh-vien-shr-pr39340918' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/20/20240320190019-881c_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/20/20240320190008-03e5_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán đất thổ hẻm 42 Trần Việt Châu</h2>
                            <li>
                             Bán đất thổ cư hẻm 42 Trần Việt Châu, Phường An Hòa, Quận Ninh Kiều.
DT: 5.2m x 8,35m= 45m² đất thổ cư (nở hậu 5,5m.
Thế đất vô cùng đẹp hẻm thông xe ba gác vị trí lô đất cách hẻm chính 42 trần việt châu xe ô tô, xe tải chỉ 15m.
Nền đất cao ráo đã có sẵn nền bê tông cốt thép kiên cố và đã cấp giấy phép xây dựng 2 lầu luôn. Mua về chỉ việc xây dựng hok tốn tiền nền móng, giấy phép xd.
Vị trí dân cư đông đúc sung túc.
Chợ An Hòa, trường học các cấp, bệnh viện trong bán kính chưa đầy 1km.
Giá bán: 1 tỷ 270tr.
                            </li>
                            </br>
                            Diện tích: 45 m²
                            Mức giá: 1,27 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tran-viet-chau-phuong-tan-an-1/ban-tho-cu-2-mat-tien-hem-truoc-sau-hem-42-chau-pr39368804' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/20/20240320212113-9631_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/21/20240321082201-8f54_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán đất tặng 3 căn nhà trọ gần chợ Tầm Vu, Hưng Lợi, Ninh Kiều, Cần Thơ</h2>
                            <li>
                             Hàng hiếm giảm giá bán thửa đất gần chợ Tầm Vu, Hưng Lợi, Ninh Kiều, Cần Thơ. DT 340 m². CLN. Thích hợp phân làm 3 nền, xây nhà trọ. Nở hậu.
Cách chợ Tầm Vu khoảng 200m, chỉ cách 1 nền nữa là thông ra hẻm 246 xe hơi ra chơ Tầm Vu, khi bờ kè hoàn thiện buôn bán sung túc sẽ tăng giá tốt.
Hiện tại cơ 3 phòng xây có gác đúc đã cho thuê.
Đã đăng ký lên thổ cư từ năm 2023.
Đã xây tường rào kiên cố xung quanh cao 2.5 mét.
Giá 4 tỷ 280 triệu.
                            </li>
                            </br>
                            Diện tích: 340 m²
                            Mặt tiền: 6 m
                            Mức giá: 4,28 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-tam-vu-phuong-hung-loi/bam-tang-3-can-nha-tro-gan-cho-ninh-kieu-can-tho-pr39317324' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/03/14/20240314195017-ea42_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422142631-543d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Bán nền thổ cư giá rẻ KV5 phường Ba Láng, quận Cái Răng, Cần Thơ, cách Quốc Lộ 61C chỉ 1km</h2>
                            <li>
                             Bán gấp nền thổ cư KV5, phường Ba Láng, quận Cái Răng, TP Cần Thơ, view sông thoáng mát.
* Giá bán chỉ 650 triệu.
+ Diện tích: 76.5m² (4.3m x 18m)
+ Sổ hồng thổ cư 100%.
+ Hướng: Đông Bắc.
Vị trí cách khu di tích Giàn Gừa 300m, cách Quốc Lộ 61C chỉ 1km cách cầu Ba Láng 2km...
                            </li>
                            </br>
                            Diện tích: 76,5 m²
                            Mặt tiền: 5 m
                            Mức giá: 650 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-quoc-lo-61c-phuong-ba-lang/n-nen-tho-cu-gia-re-kv5-quan-cai-rang-can-tho-cach-chi-1km-pr38773709' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2023/12/12/20231212183133-d92c_wm.jpeg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/200x200/2023/12/12/20231212183151-70d5_wm.jpeg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Chính chủ cần bán nhanh nền đường Lộ Hậu Kênh Thạnh Đông, P. Phú Thứ, Q. Cái Răng, TP. Cần Thơ</h2>
                            <li>
                             Diện tích: 189.7m² (5 x 37.91m), (CLN, lộ hoàn thành là được lên thổ cư).
Giá bán: 1 tỷ 150 (thương lượng khách thiện chí).
- Lộ giới: 12m.
- Vị trí & tiện ích: Đi đường Trương Vĩnh Nguyên tới cầu Xẻo Lá, chưa qua cầu quẹo phải, vô tầm 2.5km tới lộ 12m đang làm quẹo trái qua chạy 500m là tới nền, lộ đang làm nối Bến Bạ - Cái Chanh.
- Vị trí tiềm năng, cách chợ Cái Chanh 10 phút, chợ Cái Răng 20 phút, trường học cấp 1, trường mầm non..
- Đường đang thi công lại cuối năm 2024 dự kiến thông xe.
- Mặt tiền, và hẻm xe hơi (có thể đi 2 đường) song song với đường cao tốc Long Xuyên Cần Thơ.
- Phù hợp với nhu cầu định cư lâu dài, đầu tư sinh lời.
- Khu dân cư đông đúc. Giao thông thuận tiện.
- Pháp lý đầy đủ, thủ tục sang tên nhanh chóng.
- Tiềm năng lớn: Đất luôn tăng giá theo tình hình hiện tại chung của BĐS của khu vực, bảo đảm sinh lời.
                            </li>
                            </br>
                            Diện tích: 189,7 m²
                            Mặt tiền: 5 m
                            Mức giá: 1,15 tỷ
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-phuong-phu-thu/chinh-chu-can-ban-nhanh-nen-duong-lo-hau-kenh-thanh-dong-p-q-cai-rang-tp-can-tho-pr39660232' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422154116-0f9e_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/22/20240422154115-4dd0_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and dat_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["dat mat tien", "đất mặt tiền"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''

            else:
                response = f"theo thông tin của bạn ở quận {dat_entity} với mức giá khoảng {price_entity} hiện tại chưa có bất động sản nào được tìm thấy bạn vui lòng chọn địa điểm khác và giá khác để tôi có thể tư vấn cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("dat_e", dat_entity), SlotSet("price", price_value)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về loại đất, quận và mức giá. bạn vui lòng cung cấp thêm thông tin để tôi có thể tư vấn kỹ hơn cho bạn.")
            return []
        
class XacNhanNhaAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_nha"
    
    @staticmethod
    def convert_price_to_number(price_str: Text) -> float:
    # Chuyển đổi từ tiếng Việt sang số
        vietnamese_numbers = {
            "một": "1",
            "hai": "2",
            "ba": "3",
            "bốn": "4",
            "năm": "5",
            "sáu": "6",
            "bảy": "7",
            "tám": "8",
            "chín": "9",
            "mươi": "0",  # Bổ sung cho trường hợp "mười" để tránh lỗi ValueError
        }
        for word, num in vietnamese_numbers.items():
            price_str = price_str.replace(word, num)

        # Xóa các ký tự không cần thiết và chuyển đổi thành chữ thường
        price_str = price_str.lower().replace(" ", "").replace("tỷ", "").replace("ty", "")

        # Xóa dấu phẩy nếu có
        price_str = price_str.replace(",", "")

        # Nếu có dấu chấm thì chuyển thành phần nguyên và phần thập phân
        if "." in price_str or "," in price_str:
            integer_part, decimal_part = price_str.split(".")
            if integer_part.isdigit() and decimal_part.isdigit():
                # Nếu cả phần nguyên và phần thập phân đều là số, kết hợp lại và chuyển đổi thành float
                return float(integer_part + decimal_part) * 1000  # Chuyển từ tỷ sang triệu
            else:
                return 0.0
        elif "triệu" in price_str:
            # Nếu chuỗi chứa từ "triệu", xóa từ đó và chuyển đổi thành số float
            price_str = price_str.replace("triệu", "").replace("trieu", "")
            if "." in price_str or "," in price_str:
                integer_part, decimal_part = price_str.split(".")
                if integer_part.isdigit() and decimal_part.isdigit():
                    return float(integer_part + decimal_part)
                else:
                    return 0.0
            elif price_str.isdigit():
                return float(price_str)
            else:
                return 0.0
        elif price_str.isdigit():
            # Nếu chuỗi chỉ chứa các chữ số, chuyển đổi thành số float
            return float(price_str) * 1000  # Chuyển từ tỷ sang triệu
        else:
            # Nếu không, trả về 0
            return 0.0


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        nha_entity = next(tracker.get_latest_entity_values('nha_e'), None)
        print(nha_entity)
        price_entity = next(tracker.get_latest_entity_values('price'), None)
        property_type_entity = next(tracker.get_latest_entity_values('property_type_nha'), None)

        if nha_entity and price_entity:
            nha_entity = nha_entity.lower().strip()
            price_value = self.convert_price_to_number(price_entity)
            if (300 <= int(price_value) <= 800
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-phuong-hung-thanh/chinh-chu-ban-o-cai-rang-full-tho-cu-gia-chi-790tr-lien-he-thao-0772881989-pr37228187' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2023/05/15/20230515114930-2f47_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2023/05/15/20230515114931-20c7_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nhà gia đình", "nha gia dinh"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nha pho", "nhà phố"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nha pho", "nhà phố"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nha pho", "nhà phố"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nha pho", "nhà phố"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and nha_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["nha pho", "nhà phố"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='' target='_blank'>bấm vào để xem</a>
                            <img src='' alt='' />
                            <img src='' alt='' /> 
                            '''
            
            else:
                response = f"Bạn quan tâm đến nhà ở quận {nha_entity} với mức giá khoảng {price_entity}. Tôi sẽ tìm kiếm thông tin cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("nha_e", nha_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về loại nhà, quận và mức giá. bạn vui lòng cung cấp thêm thông tin để tôi có thể tư vấn kỹ hơn cho bạn.")
            return []
    
class XacNhanCanHoAction(Action):

    def name(self) -> Text:
        return "action_xacnhan_canho"
    
    @staticmethod
    def convert_price_to_number(price_str: Text) -> float:
    # Chuyển đổi từ tiếng Việt sang số
        vietnamese_numbers = {
            "một": "1",
            "hai": "2",
            "ba": "3",
            "bốn": "4",
            "năm": "5",
            "sáu": "6",
            "bảy": "7",
            "tám": "8",
            "chín": "9",
            "mươi": "0",  # Bổ sung cho trường hợp "mười" để tránh lỗi ValueError
        }
        for word, num in vietnamese_numbers.items():
            price_str = price_str.replace(word, num)

        # Xóa các ký tự không cần thiết và chuyển đổi thành chữ thường
        price_str = price_str.lower().replace(" ", "").replace("tỷ", "").replace("ty", "")

        # Xóa dấu phẩy nếu có
        price_str = price_str.replace(",", "")

        # Nếu có dấu chấm thì chuyển thành phần nguyên và phần thập phân
        if "." in price_str or "," in price_str:
            integer_part, decimal_part = price_str.split(".")
            if integer_part.isdigit() and decimal_part.isdigit():
                # Nếu cả phần nguyên và phần thập phân đều là số, kết hợp lại và chuyển đổi thành float
                return float(integer_part + decimal_part) * 1000  # Chuyển từ tỷ sang triệu
            else:
                return 0.0
        elif "triệu" in price_str:
            # Nếu chuỗi chứa từ "triệu", xóa từ đó và chuyển đổi thành số float
            price_str = price_str.replace("triệu", "").replace("trieu", "")
            if "." in price_str or "," in price_str:
                integer_part, decimal_part = price_str.split(".")
                if integer_part.isdigit() and decimal_part.isdigit():
                    return float(integer_part + decimal_part)
                else:
                    return 0.0
            elif price_str.isdigit():
                return float(price_str)
            else:
                return 0.0
        elif price_str.isdigit():
            # Nếu chuỗi chỉ chứa các chữ số, chuyển đổi thành số float
            return float(price_str) * 1000  # Chuyển từ tỷ sang triệu
        else:
            # Nếu không, trả về 0
            return 0.0


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        can_ho_entity = next(tracker.get_latest_entity_values('can_ho_e'), None)
        print(can_ho_entity)
        price_entity = next(tracker.get_latest_entity_values('price'), None)
        print(price_entity)
        property_type_entity = next(tracker.get_latest_entity_values('property_type_canho'), None)
        print(property_type_entity)

        if can_ho_entity and price_entity:
            can_ho_entity = can_ho_entity.lower().strip()
            price_value = self.convert_price_to_number(price_entity)
            if (300 <= int(price_value) <= 800
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["can ho chung cu", "căn hộ chung cư"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["ninh kieu", "ninh kiều"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["cai rang", "cái răng"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["binh thuy", "bình thủy"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            elif (300 <= int(price_value) <= 800
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
               
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (801 <= int(price_value) <= 1200
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> '''
            elif (1201 <= int(price_value) <= 7000
                and can_ho_entity in ["phong dien", "phong điền"]
                and property_type_entity in ["căn hộ dịch vụ", "can ho dich vu"]):
                response = '''<h3>đây là bất động sản phù hợp với yêu cầu của bạn:</h3>
                            </br>
                            <h2>Đất ngộp bán gấp 115m2 đất mặt tiền đường Hoàng Quốc Việt,An Bình,Ninh Kiều,Cần Thơ.Gần cầu Cái Sơn</h2>
                            <li>
                             Nhà có việc bán nhanh đất MT đường Hoàng Quốc Việt.
                                Diện tích: 115m² ( ngang 5 dài 23 )
                                -Sổ hồng riêng, 100% đất thổ cư.
                                -Xung quanh đầy đủ tiện ích : BV đột quỵ tim mạch Cần Thơ, Cầu Cái Sơn, BV DK trung ương Cần Thơ, Đại học FPT,..
                                -Dân cư xung quanh ở đông đúc.
                                -Đường rộng rãi thông thoáng.
                                -Cơ sở hạ tầng cao.
                                -Hệ thống cầu đường, Cống rãnh thông thoáng không bị ngập, lụt.
                            </li>
                            </br>
                            Diện tích: 115 m²
                            Mặt tiền: 5 m
                            Mức giá: 600 triệu
                            </br>
                            <a class='click-link' href='https://batdongsan.com.vn/ban-dat-duong-hoang-quoc-viet-phuong-an-binh-2/-ngop-b-gap-115m2-mat-tien-ninh-kieu-c-tho-g-cau-cai-son-pr39649680' target='_blank'>bấm vào để xem</a>
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-c972_wm.jpg' alt='' />
                            <img src='https://file4.batdongsan.com.vn/resize/1275x717/2024/04/21/20240421103301-305d_wm.jpg' alt='' /> 
                            '''
            else:
                response = f"Bạn quan tâm đến {property_type_entity} ở quận {can_ho_entity} với mức giá khoảng {price_entity}. Tôi sẽ tìm kiếm thông tin cho bạn."
            dispatcher.utter_message(text=response)
            return [SlotSet("can_ho_e", can_ho_entity), SlotSet("price", price_entity)]
        else:
            dispatcher.utter_message(text="Tôi chưa nhận được đầy đủ thông tin về loại căn hộ, quận và mức giá. bạn vui lòng cung cấp thêm thông tin để tôi có thể tư vấn kỹ hơn cho bạn.")
            return []
        

