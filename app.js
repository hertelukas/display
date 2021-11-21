const express = require('express');
const app = express();

app.get('/', function (req, res) {
    res.render('index');
});

app.set('view engine', 'ejs');

const port = process.env.PORT || 3000;
app.listen(port, function() {
    console.log("Server started. Listening on port " + port);
})