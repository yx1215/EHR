const express = require("express");
const app = express();
const server = require("http").Server(app);
const io = require("socket.io")(server);
var cors = require('cors');

app.use(express.static('public'));
app.use(cors());


const example_mail = {
    "html": "hi there",
    "text": "gfuygouiygouygou",
    "headers": {
        "from": "doctorx",
        "date": "Wed, 23 Oct 2019 21:57:44 +0800",
        "subject": "",
    },
    "to": "bkvdprtkr@xkx.me"
};


allmessages = {"test1@nyu.edu": [example_mail], "test2@nyu.edu": [example_mail, example_mail]};

id2user = {};
user2id = {};


io.on('connect', (socket) => {
    console.log('connected', socket.id);
    socket.on('set_username', (username) => {
        let usersocketid = socket.id;
        id2user[usersocketid] = username;
        user2id[username] = [usersocketid];
        socket.emit("previous_messages", allmessages[username]);
    });

    socket.on("new_message_sent", (obj) => {
        if (allmessages[obj.to] !== undefined) {
            allmessages[obj.to].push(obj)
        } else {
            allmessages[obj.to] = [obj]
        }

        let socketId = user2id[obj.to];
        io.to(socketId).emit('new_message_received', obj);
    })
});

app.get('/api/msg/:email', (req, res) => {
    res.send(allmessages[req.params.email])
});


server.listen(3000);
