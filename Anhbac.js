function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const message = document.getElementById("message");
  const qrDiv = document.getElementById("qrcode");

  if (username === "Dchou" && password === "01062025") {
    message.textContent = "";
    document.getElementById("login-form").style.display = "none";
    startCountdown(100); // 10 giây đếm ngược

    qrDiv.style.display = "block";
    generateQRCode(`Gửi bé nhất ${username} 
        \n
        \n Vậy là cũng đã hơn 1 tháng một chút xíu chúng ta yêu nhau, đây là lần đầu tiên anh viết thư cho em dưới hình thức lạ hoắc này
        \n Có lẽ khoảng thời gian vừa qua anh có chút mệt mỏi về học tập công việc nhưng khi nói chuyện và gặp em, nụ cười của anh lại hiện ra vì sự hạnh phúc, hào hứng khi em đến bên anh
        \n Cảm ơn em đã đến bên anh, anh mong sẽ tạo thêm nhiều điều bất ngờ hơn thế này cho người anh yêu nhất <3 `);
  } else {
    message.textContent = "Tên đăng nhập hoặc mật khẩu sai!";
  }
  if (username === "đinhtrong" && password === "02081995") {
    message.textContent = "";
    document.getElementById("login-form").style.display = "none";
    startCountdown(100); // 10 giây đếm ngược

    qrDiv.style.display = "block";
    generateQRCode(`Xin chào ${username}!`);
  } else {
    message.textContent = "Tên đăng nhập hoặc mật khẩu sai!";
  }
  if (username === "biayciii" && password === "Anhbac2@@5") {
    message.textContent = "";
    document.getElementById("login-form").style.display = "none";
    startCountdown(100); // 10 giây đếm ngược

    qrDiv.style.display = "block";
    generateQRCode(`Xin chào ${username}!`);
  } else {
    message.textContent = "Tên đăng nhập hoặc mật khẩu sai!";
  }
}

function generateQRCode(text) {
    
  QRCode.toCanvas(document.getElementById('canvas'), text, function (error) {
    if (error) console.error(error);
  });

  new QRCode(qrDiv, {
    text: text,
    width: 200,
    height: 200
  });
}
function startCountdown(seconds) {
  const qrDiv = document.getElementById("qrcode");
  const timer = document.createElement("p");
  timer.id = "timer";
  qrDiv.appendChild(timer);

  let timeLeft = seconds;
  timer.textContent = `Quay lại sau ${timeLeft} giây`;

  const interval = setInterval(() => {
    timeLeft--;
    timer.textContent = `Quay lại sau ${timeLeft} giây`;

    if (timeLeft <= 0) {
      clearInterval(interval);
      // Ẩn QR, hiển thị lại form
      qrDiv.style.display = "none";
      document.getElementById("login-form").style.display = "block";
      timer.remove();
    }
  }, 1000);
}
