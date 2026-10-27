const rl = require("readline").createInterface({ input: process.stdin, output: process.stdout });

function printAll(x) {
  for (const item of x) console.log(item);
  return x;
}

rl.question("Values: ", (line) => {
  arr_name = line.split(" ");
  printAll(arr_name);
  rl.close();
});