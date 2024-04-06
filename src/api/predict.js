const { PythonShell } = require("python-shell");

async function predict(betAmount, balance) {
  return new Promise((resolve, reject) => {
    const options = {
      mode: "text",
      pythonOptions: ["-u"],
      scriptPath: "src/api",
      args: [betAmount, balance],
    };

    PythonShell.run("ai_model.py", options, (err, results) => {
      if (err) {
        console.error(err);
        reject(err);
      } else {
        resolve(results);
      }
    });
  });
}

module.exports = { predict };
