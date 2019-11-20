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
    let html;
    if (msgObj.read) {
        html = `
<a class="dropdown-item d-flex align-items-center" href="#">
    <div>
        <div class="text">${msgObj.text}</div>
        <div class="small text-gray-500">${msgObj.sender} · ${msgObj.time}</div>
    </div>
</a>
`
    } else {
        html = `
<a class="dropdown-item d-flex align-items-center" href="#">
    <div class="font-weight-bold">
        <div class="text">${msgObj.text}</div>
        <div class="small text-gray-500">${msgObj.sender} · ${msgObj.time}</div>
    </div>
</a>
`
    }

    $("#messagehtml").append(html)

}



$.getJSON("/auth/api/email", function(data) {
    $.getJSON("http://localhost:3000/api/msg/"+data.email, function(data1) {
        setMessageNumber(data1.length)
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



