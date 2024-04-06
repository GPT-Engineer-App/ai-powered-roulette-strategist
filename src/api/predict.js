const { PythonShell } = require("python-shell");

async function predict(betAmount, balance) {
  return new Promise((resolve, reject) => {
    const options = {
      mode: "text",
      pythonOptions: ["-u"], 
      scriptPath: "src/api",
      args: [betAmount, balance, "play"],
    };

    PythonShell.run("ai_model.py", options, (err, results) => {
      if (err) {
        console.error(err);
        reject(err);
      } else {
        resolve(results[0]);
      }
    });
  });
}

async function train(epochs, layers, nodes, activations) {
  return new Promise((resolve, reject) => {
    const options = {
      mode: "text",
      pythonOptions: ["-u"],
      scriptPath: "src/api", 
      args: [epochs, layers, nodes.join(","), activations.join(","), "train"],
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

module.exports = { predict, train };
