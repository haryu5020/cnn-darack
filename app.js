
/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , http = require('http')
  , multer = require('multer')
  , bodyParser = require('body-parser')
  , path = require('path');

var _storage = multer.diskStorage({
	  destination: function (req, file, cb) {
	    cb(null, 'uploads/');
	  },
	  filename: function (req, file, cb) {
	    cb(null, file.originalname);
	  }	
});

var upload = multer({ storage: _storage });

var app = express();

// all environments
app.set('port', process.env.PORT || 15000);
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('.html', require('ejs').__express);
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(bodyParser.urlencoded({ extended: false}));
app.locals.pretty = true;
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(path.join(__dirname, 'public')));
app.use('/uploads', express.static('uploads'));
// development only
if ('development' === app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', function(req, res){
	res.render('main.html');
});
app.post('/upload', upload.single('imagefile'), function(req, res){
	res.send('Uploaded : ' + req.file.filename);
});


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});
