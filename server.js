const express = require('express')
const bodyParser = require('body-parser');
const app = express()
var ob = {}
ob.coaqi=""
ob.o3aqi=""
ob.no2aqi=""
ob.c6h6aqi=""
ob.coCon=""
ob.o3Con=""
ob.no2Con=""
ob.c6h6Con=""

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

app.get('/',function (req,res){
	res.render('index',{ob});

})
app.post('/', function (req, res) {
	console.log(req.body.city);
	res.render('index',{ob});
})
app.get('/myco', function(req, res){ 
    var coCon = req.query.co; //co is the name of your input box
    var coaqi = (coCon*100)/10.31;
    ob.coaqi=coaqi;
    ob.coCon=coCon;
    res.render('index',{ob})
    //res.send('co AQI = '+ coaqi); 
})
app.get('/myo3', function(req, res){ 
    var o3Con = req.query.o3; //co is the name of your input box
    var o3aqi = (o3Con*100)/196;
    ob.o3aqi=o3aqi;
    ob.o3Con=o3Con;
    res.render('index',{ob})
    //res.send('O3 AQI = '+ o3aqi);
})
app.get('/myno2', function(req, res){ 
    var no2Con = req.query.no2; //co is the name of your input box
    var no2aqi = (no2Con*100)/226.04;
    ob.no2aqi=no2aqi;
    ob.no2Con=no2Con;
    res.render('index',{ob})
    //res.send('NO2 AQI = '+ no2aqi);
})
app.get('/myc6h6', function(req, res){ 
    var c6h6Con = req.query.c6h6; //co is the name of your input box
    var c6h6aqi = (c6h6Con*100)/5;
    ob.c6h6aqi=c6h6aqi;
    ob.c6h6Con=c6h6Con;
    res.render('index',{ob})
    //res.send('C6H6 AQI = '+ c6h6aqi);
})

app.listen(3000,function(){
	console.log('Example app listening to port 3000')
})

app.get('/name',function(req,res){
	var spawn =require("child_process").spawn;
	var process = spawn('python',["./code.py"]);
	process.stdout.on('data',function(data){
		res.send(data.toString());
	})
})