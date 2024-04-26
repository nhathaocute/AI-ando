// Sự kiện khi trang web đã được tải hoàn toàn
window.addEventListener("DOMContentLoaded", (e) => {
  // Lấy các phần tử cần thiết từ DOM
  var header = document.querySelector(".header");
  var chatRoom = document.querySelector(".chat-room");
  var typeArea = document.querySelector(".type-area");
  var btnAdd = document.querySelector(".button-add");
  var others = document.querySelector(".others");
  var emojiBox = document.querySelector(".emoji-button .emoji-box");
  var emojiButton = document.querySelector(".others .emoji-button");
  var emojis = document.querySelectorAll(".emoji-box span");
  var inputText = $(".inputText"); // Sử dụng jQuery selector
  var btnSend = document.querySelector(".button-send");
  var messageArea = document.querySelector(".message.message-right");

  // Sự kiện khi người dùng nhấn Enter hoặc click nút "Send"
  inputText.keypress(function (event) {
    if (event.which === 13 || event.keyCode === 13) {
      sendMessage();
    }
  });

  btnSend.addEventListener("click", (e) => {
    sendMessage();
  });

  // Hàm gửi tin nhắn
  function sendMessage() {
    let userMessage = $(".inputText").val(); // Lấy giá trị của input
    if (!userMessage) {
      return;
    }

    $(".inputText").val(""); // Xóa nội dung input sau khi gửi

    // Thêm tin nhắn của người dùng vào khung chat
    $("#chat-widget-messages").append(
      `<div class='message message-right'>
        <div class='avatar-wrapper avatar-small'>
          <img src='static/img/hao.jpg' alt='' />
        </div>
        <div id='ms-right' class='bubble bubble-light'>${userMessage}</div>
      </div>`
    );
    const chatRoom = document.getElementById("chat-widget-messages");
    chatRoom.scrollTop = chatRoom.scrollHeight;

    // Gửi yêu cầu AJAX đến máy chủ và xử lý phản hồi
    axios
      .post(
        "http://127.0.0.1:3000/webhook",
        { message: userMessage },
        { headers: { "Content-Type": "application/json" } }
      )
      .then((response) => {
        let botResponse = response.data.response;
        console.log("Bot Response:", botResponse); // Hiển thị phản hồi từ máy chủ

        // Hiển thị phản hồi từ máy chủ trong khung chat

        // Kiểm tra nếu botResponse là "bye", thêm nút button

        // chon loai
        if (botResponse.includes("nhà ở, căn hộ, đất nền")) {
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div class='avatar-wrapper avatar-small'>
                <img src='static/img/loc.jpg' alt='' />
              </div>
              <div class='bubble bubble-light'>${botResponse}</div>
            </div>`
          );
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div id="response-buttons" class='bubble bubble-light'>
                <button id="traloi" onclick='sendResponse("nhà ở")'>nhà ở</button>
                <button id="traloi" onclick='sendResponse("căn hộ")'>căn hộ</button>
                <button id="traloi" onclick='sendResponse("đất nền")'>đất nền</button>
              </div>
            </div>`
          );
        } else {
          // Hiển thị phản hồi từ máy chủ trong khung chat mà không có nút button
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div class='avatar-wrapper avatar-small'>
                <img src='static/img/loc.jpg' alt='' />
              </div>
              <div class='bubble bubble-light'>${botResponse}</div>
            </div>`
          );
        }

        // chon thong tin dat
        if (
          botResponse.includes(
            "vui lòng cho biết loại (đất nền hay đất mặt tiền), quận và giá bạn quan tâm"
          )
        ) {
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div id="response-buttons" class='bubble bubble-light'>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất nền ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm đất nền ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất mặt tiền ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm đất mặt tiền ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất nền ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm đất nền ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất mặt tiền ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm đất mặt tiền ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất nền ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm đất nền ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất mặt tiền ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm đất mặt tiền ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất nền ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm đất nền ở quận bình thủy có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm đất mặt tiền ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm đất mặt tiền ở quận bình thủy có giá khoảng 700 triệu</button>
                </div>
            </div>`
          );
        } else if (
          botResponse.includes(
            "vui lòng cho biết loại (nhà phố hay nhà gia đình), quận và giá bạn quan tâm"
          )
        ) {
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div id="response-buttons" class='bubble bubble-light'>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà phố ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm nhà phố ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà gia đình ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm nhà gia đình ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà phố ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm nhà phố ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà gia đình ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm nhà gia đình ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà phố ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm nhà phố ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà gia đình ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm nhà gia đình ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà phố ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm nhà phố ở quận bình thủy có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm nhà gia đình ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm nhà gia đình ở quận bình thủy có giá khoảng 700 triệu</button>
                </div>
            </div>`
          );
        } else if (
          botResponse.includes(
            "vui lòng cho biết loại (căn hộ chung cư hay căn hộ dịch vụ), quận và giá bạn quan tâm"
          )
        ) {
          $("#chat-widget-messages").append(
            `<div class='message message-left'>
              <div id="response-buttons" class='bubble bubble-light'>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ chung cư ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ chung cư ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ dịch vụ ở quận ninh kiều có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ dịch vụ ở quận ninh kiều có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ chung cư ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ chung cư ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ dịch vụ ở quận cái răng có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ dịch vụ ở quận cái răng có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ chung cư ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ chung cư ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ dịch vụ ở quận phong điền có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ dịch vụ ở quận phong điền có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ chung cư ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ chung cư ở quận bình thủy có giá khoảng 700 triệu</button>
                <button id="traloi" onclick='sendResponse1("tôi muốn tìm căn hộ dịch vụ ở quận bình thủy có giá khoảng 700 triệu")'>tôi muốn tìm căn hộ dịch vụ ở quận bình thủy có giá khoảng 700 triệu</button>
                </div>
            </div>`
          );
        }
        // Cuộn xuống cuối khung chat
        const chatRoom = document.getElementById("chat-widget-messages");
        chatRoom.scrollTop = chatRoom.scrollHeight;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  btnSend.addEventListener("click", (e) => {
    var mess = inputText.value;
    var bubble = document.createElement("div");
    bubble.className += " bubble bubble-dark";
    bubble.textContent = mess;
    messageArea?.appendChild(bubble);
    inputText.value = "";
    $(".inputText").focus();
  });
  // Sự kiện click cho các emoji
  for (var emoji of emojis) {
    emoji.addEventListener("click", (e) => {
      e.stopPropagation();
      emojiBox.classList.remove("emoji-show");
      others.classList.remove("others-show");
      inputText.val(inputText.val() + e.target.textContent); // Thêm emoji vào input khi click vào nút emoji
    });
  }
});
window.addEventListener("DOMContentLoaded", (e) => {
  // Lấy đối tượng input
  var inputText = document.querySelector(".inputText");

  // Tập trung vào ô input khi trang được tải hoàn toàn
  inputText.focus();
});
// Hàm để gửi nội dung từ nút button vào input của chatbot
function sendResponse(response) {
  $(".inputText").val(response); // Gán nội dung của nút button vào input
  $("#response-buttons").remove();
  $(".button-send").click();
  $(".inputText").focus();
}
function sendResponse1(response) {
  $(".inputText").val(response); // Gán nội dung của nút button vào input
  $("#response-buttons").remove();
  $(".inputText").focus();
}
