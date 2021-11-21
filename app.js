const express = require('express');
const app = express();
const fs = require('fs');
const bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({extended: true}));

app.get('/', function (req, res) {
    res.render('index');
});

app.post('/', function(req, res) {
    var cal = req.body.ical;

    fs.writeFile('config.dis', cal, function(err) {
        if(err){
            console.log("Failed to write to file: " + err);
        }
    })
    return res.redirect('/');
})

app.set('view engine', 'ejs');

const port = process.env.PORT || 3000;
app.listen(port, function() {
    console.log("Server started. Listening on port " + port);
})