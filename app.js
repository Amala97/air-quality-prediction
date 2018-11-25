var pythonshell = require('python-shell');
//not used yet !!

	var options = {
		mode:'text',
		encoding:'utf8',
		pythonOptions ['-u'],
		scriptPath:'./',
		args:['hello_world'],
		pythonPath: '/'

	};

	var test = new pythonshell('test.py',options);
	test.on('message',function(message){
		console.log(message);
	})