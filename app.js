const express = require('express');
const app = express();
const fs = require('fs');
const bodyParser = require("body-parser");
const { exec } = require('child_process');
const { stdout, stderr } = require('process');
const flash = require('connect-flash')

//Requiring express sessions
app.use(require('express-session')({
    secret: process.env.SECRET || "Please change me",
    resave: false,
    saveUninitialized: false
}));

app.set('view engine', 'ejs');
app.use(express.static(__dirname + "/public"));

app.use(bodyParser.urlencoded({extended: true}));
app.use(flash());
app.use(function(req, res, next) {
    res.locals.error = req.flash('error');
    res.locals.success = req.flash('success');
    next();
});

app.get('/', function (req, res) {
    fs.readFile('config.dis', 'utf8', function(err, data) {
        if(err){
            console.log("Failed to open config.dis: " + err.message);
            req.flash('error', 'Konfigurationsdatei konnte nicht geöffnet werden.');
            return res.render('index', {config: null});
        }
        fs.readFile('cron.dis', 'utf8', function(err, cron){
            if(err){
                console.log("Failed to open cron.dis: " + err.message);
                req.flash('error', 'Crontabdatei konnte nicht geöffnet werden.');
                return res.render('index', {config: JSON.parse(data), cron: null});

            }
            return res.render('index', {config: JSON.parse(data), cron: cron});
        });
    });
});

app.post('/clear', function(req, res) {
    console.log("Trying to clear the screen...");
    exec('python3 clear.py && crontab -r', (err, stdout, stderr) => {
        if(err || stderr){
            console.log("Failed: " + err.message);
            console.log("Stderr: " + stderr);
        }else {
            console.log("Stdout: " + stdout);
        }
    });

    return res.redirect('/');
});

app.post('/update', function(req, res) {
    console.log("Trying to update the screen...");
    exec('python3 main.py', (err, stdout, stderr) => {
        if(err || stderr){
            console.log("Failed: " + err.message);
            console.log("Stderr: " + stderr);
        }else {
            console.log("Stdout: \n" + stdout);
        }
    });
    return res.redirect('/');
});

app.post('/cron', function(req, res) {
    console.log("Updating crontab...");
    console.log("Writing to file...");
    fs.writeFile('cron.dis', req.body['cron'], function(err) {
        if(err){
            console.log("Failed to write file: " + err);
        } else{
            //Write correct crontab file
            fs.writeFile('crontab.dis', req.body['cron'] + " cd ~/Documents/display && python3 main.py >> display.log\n", function(err){ 
                if(err){
                    console.log("Failed to write file: " + err);
                } else{
                    console.log("Saved new crontab to file successfully. Updating crontab...");
                    exec('crontab crontab.dis', (err, stdout, stderr) => {
                        if(err){
                            console.log("Failed: " + err.message);
                        }else{
                            console.log("Command ran successfully.");
                            console.log("Stdout: " + stdout);
                            console.log("Stderr: " + stderr);
                            return res.redirect('/');
                        }
                    });
                }
            });
        }
    });
    return res.redirect('/');
});

app.post('/', function(req, res) {
    fs.writeFile('config.dis', JSON.stringify(req.body), function(err) {
        if(err){
            console.log("Failed to write to file: " + err);
        }
    });
    return res.redirect('/');
});


const port = process.env.PORT || 3000;
app.listen(port, function() {
    console.log("Server started. Listening on port " + port);
})