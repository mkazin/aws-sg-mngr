var util = require('util');
var mongo = require('mongodb'),
	dbHost = '127.0.0.1',
	dbPort = 27017,
	dbName = 'local',
	collectionName = 'messages';

var Db = mongo.Db;
var Connection = mongo.Connection;
var Server = mongo.Server;
var db = new Db(dbName, new Server(dbHost, dbPort), {safe:true});

db.open(function(error, dbConnection){
	if (error) {
		console.error(error);
		process.exit(1);
	}
	console.log('db state: ', db._state);
	item = {
		name: 'Azat'
	}
	dbConnection.collection(collectionName).insert(item, function(error, item){
		if (error) {
			console.error(error);
			process.exit(1);
		}
		console.info('created/inserted: ', item);
		db.close();
		process.exit(0);
	})
	
})
