
var express = require('express')
var http = require('http')
var path = require('path')
var mongoose = require('mongoose')

var app = express()
var securityGroups = [{id: 1, name: 'aws-sg-mngr-db'}]

app.set('appName', 'hello-world');
app.set('port', process.env.PORT || 3000);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

// TODO: how do I decouple this model code from the app?
mongoose.connect('mongodb://localhost/aws-sg-mngr')
var NO_EXPIRATION = -1;
// Do rules have identifiers or are they uniquely identified by the security group they're in, along with port, protocol, and source?
// - IsInbound: true for ingress rule, false for egress rule
// - Source: CIDR, segurity group (?ID?)
// - Port: numeric, set, or range?
// - Protocol: ? either TCP or UDP ?
var Rule = mongoose.model('rule', { description: String, userId: Number, isInbound: Boolean, source: String, port: Number, protocol: String, expiration: Number})
// 
var SecurityGroup = mongoose.model('securitygroup', { name: String, awsId: String,  rules: ??? Rule list syntax ??? })

app.all('/', function(req, res) {
	res.render(
		'index',
		{msg: 'Hello world!'}
		);
})

app.get('/securitygroup/:id', function(req, res, next){
	res.render('securitygroup', securityGroups)
})

var server = http.createServer(app);
// console.info('server started on port;
var boot = function(){
	server.listen(app.get('port'), function () {
		console.log('Express.js server listening on port ' + app.get('port'));
	});
}
var shutdown = function(){
	server.close();
}

if (require.main === module) {
	boot();
} else {
	console.info('Running app as a module')
	exports.boot = boot;
	exports.shutdown = shutdown;
	exports.port = app.get('port');
	exports.mongoose = mongoose;
}


// ===


// var express = require('express');

// var http = require('http');
// var path = require('path');

// var app = express();

// app.set('port', process.env.PORT || 3000);
// app.set('views', path.join(__dirname, 'views'));
// app.set('view engine', 'jade');

// app.all('/', function(req, res) {
//   res.render('index', {msg: 'Welcome to the Practical Node.js!'})
// })

// // http.createServer(app).listen(app.get('port'), function(){
//   // console.log('Express server listening on port ' + app.get('port'));
// // });

// var server = http.createServer(app);
// var boot = function () {
//   server.listen(app.get('port'), function(){
//     console.info('Express server listening on port ' + app.get('port'));
//   });
// }
// var shutdown = function() {
//   server.close();
// }
// if (require.main === module) {
//   boot();
// } else {
//   console.info('Running app as a module')
//   exports.boot = boot;
//   exports.shutdown = shutdown;
//   exports.port = app.get('port');
// }