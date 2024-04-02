//Content Loaded
window.addEventListener("DOMContentLoaded", (e) => {
  var header = document.querySelector(".header");
  var chatRoom = document.querySelector(".chat-room");
  var typeArea = document.querySelector(".type-area");
  var btnAdd = document.querySelector(".button-add");
  var others = document.querySelector(".others");
  var emojiBox = document.querySelector(".emoji-button .emoji-box");
  var emojiButton = document.querySelector(".others .emoji-button");
  var emojis = document.querySelectorAll(".emoji-box span");
  var inputText = document.querySelectorAll(".inputText");
  var btnSend = document.querySelector(".button-send");
  var messageArea = document.querySelector(".message.message-right");
  //Header onclick event
  header.addEventListener("click", (e) => {
    if (typeArea.classList.contains("d-none")) {
      header.style.borderRadius = "20px 20px 0 0";
    } else {
      header.style.borderRadius = "20px";
    }
    typeArea.classList.toggle("d-none");
    chatRoom.classList.toggle("d-none");
  });
  //Button Add onclick event
  btnAdd.addEventListener("click", (e) => {
    others.classList.add("others-show");
  });
  //Emoji onclick event
  emojiButton.addEventListener("click", (e) => {
    emojiBox.classList.add("emoji-show");
  });

  // Bắt sự kiện khi người dùng nhấn Enter hoặc click vào nút "Send"
  $("#inputText").keypress(function (event) {
    if (event.which === 13 || event.keyCode === 13) {
      // Gửi tin nhắn của người dùng
      sendMessage();
    }
  });

  $(".button-send").click(function () {
    // Gửi tin nhắn của người dùng
    sendMessage();
  });

  function sendMessage() {
    let userMessage = $("#inputText").val();
    if (!userMessage) {
      // Nếu không có tin nhắn, không thực hiện gì cả
      return;
    }

    $("#inputText").val("");

    // Thêm tin nhắn của người dùng vào khung chat
    $("#chat-widget-messages").append(
      "<div class='message message-right'>" +
        "<div class='avatar-wrapper avatar-small'>" +
        "<img src='static/img/hao.jpg') }}' alt='' />" +
        "</div>" +
        "<div id='ms-right' class='bubble bubble-light'>" +
        userMessage +
        "</div>" +
        "</div>"
    );
    const chatRoom = document.getElementById("chat-widget-messages");
    chatRoom.scrollTop = chatRoom.scrollHeight;

    // Gửi yêu cầu AJAX đến máy chủ
    axios
      .post(
        "http://127.0.0.1:3000/webhook",
        {
          message: userMessage,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        // Xử lý phản hồi từ máy chủ
        console.log(response.data);
        let botResponse = response.data.response;

        //chu
        //HINHF ARNH

        // Hiển thị phản hồi từ máy chủ trong khung chat
        $("#chat-widget-messages").append(
          "<div class='message message-left'>" +
            "<div class='avatar-wrapper avatar-small'>" +
            "<img src='static/img/loc.jpg' alt='' />" +
            "</div>" +
            "<div class='bubble bubble-light'>" +
            botResponse +
            "</div>" +
            "</div>"
        );
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
    messageArea.appendChild(bubble);
    inputText.value = "";
  });
  for (var emoji of emojis) {
    emoji.addEventListener("click", (e) => {
      e.stopPropagation();
      emojiBox.classList.remove("emoji-show");
      others.classList.remove("others-show");
      inputText.value += e.target.textContent;
    });
  }
});
