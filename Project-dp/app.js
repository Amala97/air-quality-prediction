var PythonShell = require(‘python-shell’);
app.get(‘/dalembert’, callD_alembert);
function callD_alembert(req, res) {
  var options = {
    args:
    [
      req.query.funds, // starting funds
      req.query.size, // (initial) wager size
      req.query.count, // wager count — number of wagers per sim
      req.query.sims // number of simulations
    ]
  }
  PythonShell.run(‘./d_alembert.py’, options, function (err, data) {
    if (err) res.send(err);
    res.send(data.toString())
  });
}