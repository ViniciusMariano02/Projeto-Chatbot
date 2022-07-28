document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("input");
    inputField.addEventListener("keydown", (e) => {
      if (e.code === "Enter") {
        let input = inputField.value;
        inputField.value = "";

        $.ajax({
          url: "",
          type: "get",
          contentType: "application/json",
          data: {
            input_text: input,
          },
          success: function (response) {
            
            addChat(input, response);
            
            
          }
        })
      }
    });
  });
  
  function addChat(input, response) {

    console.log(typeof response.res)

    
    

    
    const messagesContainer = document.getElementById("messages");
  
    let userDiv = document.createElement("div");
    userDiv.id = "user";
    userDiv.className = "user response";
    userDiv.innerHTML = `<img src="/static/chatbot/user.png" class="avatar"><span>${input}</span>`;
    messagesContainer.appendChild(userDiv);
  
    let botDiv = document.createElement("div");
    let botImg = document.createElement("img");
    let botText = document.createElement("span");
    botDiv.id = "bot";
    botImg.src = "static/chatbot/bot-mini.png";
    botImg.className = "avatar";
    botDiv.className = "bot response";
    botText.innerText = "Digitando...";
    
    botDiv.appendChild(botText);
    botDiv.appendChild(botImg);
    messagesContainer.appendChild(botDiv);
    
    //let botList = document.createElement("ul")

    // Keep messages at most recent
    messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;
    
    // Fake delay to seem "real"
    setTimeout(() => {
      botText.innerText = `${response.res}`;
      textToSpeech(response.res);
    }, 2000);
  }




/*document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("input");
    inputField.addEventListener("keydown", (e) => {
        if (e.code === "Enter") {
            let input = inputField.value;
            inputField.value = "";
            
            $.ajax({
                url: '',
                type: 'get',
                contentType: 'application/json',
                data: {
                    input_text: input
                },
                success: function(response){
                    $('.bot-message').text(response.res)
                    
                }
            })

        }
    });
});
*/



/*
$(document).ready(function () {

    jQuery('#input').keypress(function(event){

        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            alert('You pressed a "enter" key in textbox');
            
            result = event
            console.log(event)

            $.ajax({
                url: '',
                type: 'get',
                contentType: 'application/json',
                data: {
                    input_text: 'Ok' //$(this).text()
                },
                success: function(response){
                    $('.messages').text(response.nome)
                }
            })
        }
    
    });

*/

/*
$('.btn').click(function() {
    $.ajax({
        url: '',
        type: 'get',
        contentType: 'application/json',
        data: {
            button_text: $(this).text()
        },
        success: function(response){
            $('.btn').text(response.nome)
        }
    })

})





})
*/