// var express = require("express");
// var app = express();
// app.use('/', express.static(__dirname));
// app.listen(process.env.PORT || 3000, function() { console.log('listening')});

const express = require('express');
const app = express();
const url = require("url");
app.use(express.static(__dirname));
app.set('view engine', 'html')

app.get('/', (req, res, next)=>{
  res.render('index.html');
  res.redirect(url.parse(req.url).pathname);
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