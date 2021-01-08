var express = require('express');
var fs = require('fs');
var ejs = require('ejs');
var path = require('path');
var http = require('http');
var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var routes = require('./routes/index');
var users = require('./routes/users');
var app = express();
var http = require('http').Server(app);
var Gpio = require('onoff').Gpio;

var relay = new Gpio(18, 'out');

var web_port = process.env.PORT || 8004;

app.use(express.static(__dirname + '/public'));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname + 'index.html'));
});

app.get('/list',function(req,res)
{
	fs.readFile('list.html','utf8',function(error,data)
	{
		if(error)
		{
			console.log('read file error');
		}
		else
		{
			res.send(data);
			res.writeHead(200, {'Content-Type': 'text/plain'});
			res.end('Pan Left\n');
		}
	})
});

app.get('/edit/:id',function(req,res)
{
	fs.readFile('edit.html','utf8',function(error,data)
	{
		mySqlClient.query('select * from products where id = ?',
		[req.params.id], function(error,result)
		{
			if(error)
			{
				console.log('read file error');
			}
			else
			{
				res.send(ejs.render(data,{ product:result[0] }));
				
			}
		});
	});
});

app.get('/delete/:id',function(req,res)
{
	mySqlClient.query('delete from products where id = ?',
	[req.params.id],function(error,result)
	{
		if(error)
		{
			console.log('delete error');
		}
		else
		{
			console.log('delete id = %d',req.params.id);
			res.redirect('/');	// return main
		}
	});
});

app.post( '/edit/:id', function(req, res)
{
	var body = req.body;
	
	mySqlClient.query( 'update products set name=?, modelnumber=?, series=? where id=?',
	[body.name,body.modelnumber,body.series,body.id],function(error,result)
	{
		if(error)
		{
			console.log('update error: ', error.message);
		}
		else
		{
			res.redirect('/');
		}
	});
});
app.get('/open_door', function(req,res){
    console.log("Door is openned");
    relay.writeSync(1);
    setTimeout(function() {
        relay.writeSync(0);
    }, 500);
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Door Open.\n');
});



app.use('/', routes);
app.use('/users', users);

http.listen(web_port, function(){
console.log('listening on *:' + web_port);
});
