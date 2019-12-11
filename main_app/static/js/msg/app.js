$(function () {

    $maillist = $('#maillist');

    $maillist.on('click', 'tr', function () {
        var mail = $(this).data('mail');
        $('#mailcard .header').text(mail.headers.subject || 'No Subject');
        $('#mailcard .content:last').html(mail.html);
        Prism.highlightAll();
    });

    const socket = io('http://127.0.0.1:3000');

    socket.on('connect', function () {

    });

    socket.on('new_message_received', function (mail) {
        if (('Notification' in window)) {
            if (Notification.permission === 'granted') {
                new Notification('New mail from ' + mail.headers.from);
            } else if (Notification.permission !== 'denied') {
                Notification.requestPermission(function (permission) {
                    if (permission === 'granted') {
                        new Notification('New mail from ' + mail.headers.from);
                    }
                })
            }
        }
        maketrandprepend(mail)
    });


    function maketrandprepend(mail) {
        $tr = $('<tr>').data('mail', mail);
        $tr
            .append($('<td>').text(mail.headers.from))
            .append($('<td>').text(mail.headers.subject || 'No Subject'))
            .append($('<td>').text((new Date(mail.headers.date)).toLocaleString()));
        $maillist.prepend($tr);
    }

    function handleClick(evt) {
        const msg = document.querySelector("#typemessage").value;
        const res = document.querySelector("#setrecipient").value;
        const sbj = document.querySelector("#setsubject").value;
        socket.emit('new_message_sent', {
            to: res, html: msg, text: msg,
            headers: {
                "from": username,
                "date": new Date(),
                "subject": sbj,
            }
        });
    }


    const btn = document.querySelector("#btn");
    btn.addEventListener("click", handleClick);

    let username;

    $.getJSON( "http://127.0.0.1:5000/auth/api/email", function( data ) {
        const email = data.email;
        username = email;
        socket.emit('set_username', email);
        $("#usernametext").text(email)
    });

    socket.on("previous_messages", (pm) => {
        if (pm !== null) {
            for (const m of pm) {
                maketrandprepend(m);
            }
        }

    });

});
