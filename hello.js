const rl = require("readline").createInterface({ input: process.stdin, output: process.stdout });

function printAll(x) {
  for (const item of x) console.log(item);
  return x;
}

rl.question("Values: ", (line) => {
  const arr_name = line.trim().split(/\s+/);
  printAll(arr_name);
  rl.close();
});