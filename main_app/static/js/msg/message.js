function setMessageNumber(n) {
    const obj = $('#messagesDropdown > span');
    if (n === 0) {
        obj.hide();
    } else {
        obj.show();
        obj.text(n);
    }
}


function appendMessage(msgObj) {
    const ele = document.createElement("a");
    ele.className = "dropdown-item d-flex align-items-center";
    const elediv = document.createElement("div");
    if (!msgObj.read){
        elediv.className = "font-weight-bold";
    }
    ele.appendChild(elediv);

    function creatChild(elediv, className, textContent){
        const child = document.createElement("div");
        child.className = className;
        child.textContent = textContent;
        elediv.appendChild(child);
    }
    
    creatChild(elediv, "text", msgObj.text);
    creatChild(elediv, "small text-gray-500",`${msgObj.sender} · ${msgObj.time}`);

    $("#messagehtml").append(ele);
}



$.getJSON("/auth/api/email", function(data) {
    $.getJSON("http://127.0.0.1:3000/api/msg/"+data.email, function(data1) {
        setMessageNumber(data1.length);
        for (let i of data1){
            appendMessage({text: i.text, read: 0, sender: i.headers.from, time: i.headers.date})
        }



        // console.log(data1)
    });


    // console.log(data)
});

//
// appendMessage({text: "fewr", read: 1, sender: "fere", time: "58m"})
// appendMessage({text: "fefewrfefwr", read: 0, sender: "frefreerfre", time: "5444448m"})


$(".dropdown-item.d-flex.align-items-center").on('click', function (event) {
    console.log(event.currentTarget)
});



