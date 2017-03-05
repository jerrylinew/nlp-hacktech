// var express = require("express");
// var app = express();
// app.use('/', express.static(__dirname));
// app.listen(process.env.PORT || 3000, function() { console.log('listening')});

const path = require("path")


const express = require('express');
const app = express();
const url = require("url");
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'pug');
var bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

var data;

app.post('/data', (req, res)=>{
    data = req.body;
    console.log(data)
})

app.get('/', function(req, res){
    console.log(data)
    res.render('index.pug', {'data': data.data});
})


// app.use((req, res, next)=>{
//   res.status(404);
//   if(req.accepts('html')){
//     res.render('404.html', {url: req.url});
//     return;
//   }
// })

app.listen(process.env.PORT || 3000, ()=>{
  console.log("Listening");
})