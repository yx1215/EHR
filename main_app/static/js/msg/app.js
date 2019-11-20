$(function () {
    // $('.ui.modal')
    //   .modal()
    // ;
    //
    // var clipboard = new Clipboard('.copyable');
    //
    // $customShortId = $('#customShortid');
    // $shortId = $('#shortid');
    // $customTheme = 'check';
    // $placeholder_old = '请等待分配临时邮箱';
    // $placeholder_new = '请输入不带后缀邮箱账号';
    // $customShortId.on('click',function() {
    //   var self = $(this);
    //   var editEnable = true;
    //   $shortId.prop('disabled', false);
    //   if(self.hasClass('edit')) {
    //     $shortId.val('');
    //     self.removeClass('edit');
    //     self.toggleClass($customTheme);
    //     $shortId.prop('placeholder', $placeholder_new);
    //   } else {
    //     $shortId.prop('disabled', true);
    //     self.removeClass('check');
    //     self.toggleClass('edit');
    //     $shortId.prop('placeholder',$placeholder_old);
    //     $mailUser = $shortId.val();
    //     var mailaddress = $mailUser + '@' + location.hostname;
    //     setMailAddress($mailUser);
    //     $shortId.val(mailaddress);
    //     window.location.reload();
    //   }
    // });


    $maillist = $('#maillist');

    $maillist.on('click', 'tr', function () {
        var mail = $(this).data('mail');
        $('#mailcard .header').text(mail.headers.subject || 'No Subject');
        $('#mailcard .content:last').html(mail.html);
        // $('#mailcard i').click(function () {
        //     $('#raw').modal('show');
        // });
        // $('#raw .header').text('RAW');
        // $('#raw .content').html($('<pre>').html($('<code>').addClass('language-json').html(JSON.stringify(mail, null, 2))));
        Prism.highlightAll();
    });

    const socket = io('http://localhost:3000');

    // var setMailAddress = function (id) {
    //     localStorage.setItem('shortid', id);
    //     var mailaddress = id + '@' + location.hostname;
    //     $('#shortid').val(mailaddress).parent().siblings('button').find('.mail').attr('data-clipboard-text', mailaddress);
    // };
    //
    // $('#refreshShortid').click(function () {
    //     socket.emit('request shortid', true);
    // });

    socket.on('connect', function () {
        // if (('localStorage' in window)) {
        //     var shortid = localStorage.getItem('shortid');
        //     if (!shortid) {
        //         socket.emit('request shortid', true);
        //     } else {
        //         socket.emit('set shortid', shortid);
        //     }
        // }
    });

    // socket.on('shortid', function (id) {
    //     setMailAddress(id);
    // });

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


    const example_mail = {
        "html": "gfuygouiygouygou",
        "text": "gfuygouiygouygou",
        "headers": {
            "from": "uerfygeriuy",
            "date": "Wed, 23 Oct 2019 21:57:44 +0800",
            "subject": "Fwd: Test Hyml",
        },
        "to": "bkvdprtkr@xkx.me"
    };


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
    // const usernamebtn = document.querySelector("#setusernamebutton");


    $.getJSON( "http://localhost:5000/auth/api/email", function( data ) {
        const email = data.email
        username = email
        socket.emit('set_username', email)
        $("#usernametext").text(email)
    });

    socket.on("previous_messages", (pm) => {
        if (pm !== null) {
            for (const m of pm) {
                maketrandprepend(m);
            }
        }


    });

    // usernamebtn.addEventListener("click", function (evt) {
    //     username = document.querySelector("#setusername").value;
    //     socket.emit('set_username', data.email)
    // });


});
