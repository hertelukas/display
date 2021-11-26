const express = require('express');
const app = express();
const fs = require('fs');
const bodyParser = require("body-parser");
const { exec } = require('child_process');
const { stdout, stderr } = require('process');

app.use(bodyParser.urlencoded({extended: true}));

app.get('/', function (req, res) {
    fs.readFile('config.dis', 'utf8', function(err, data) {
        if(err){
            //TODO handle error
            return;
        }
        return res.render('index', {config: JSON.parse(data)});

    });
});

app.post('/clear', function(req, res) {
    exec('python3 clear.py', (err, stdout, stderr) => {
        if(err){
            //TODO handle error
        }
    });
    return res.redirect('/');
});

app.post('/', function(req, res) {
    fs.writeFile('config.dis', JSON.stringify(req.body), function(err) {
        if(err){
            console.log("Failed to write to file: " + err);
        }
    })
    return res.redirect('/');
});

app.set('view engine', 'ejs');
app.use(express.static(__dirname + "/public"));

const port = process.env.PORT || 3000;
app.listen(port, function() {
    console.log("Server started. Listening on port " + port);
})