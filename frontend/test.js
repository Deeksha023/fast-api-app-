console.log("Hello, World!");

/*
let x = 10;
console.log(x);
const y = 20;
console.log(y);
console.log(x + y);
function add(x, y) {
    return x + y;
}
*/
const arr =[10,20,30,40,50];
//console.log(arr[0]);
//console.log(arr[1]);
//console.log(arr[2]);
//console.log(arr[3]);
//console.log(arr[4]);

//dictionary
const dict = {
    "name": "John","age": 30,"city": "New York"
};
console.log(dict.name);
console.log(dict.age);
console.log(dict.city);

// console.log(a);
// console.log(b);
// console.log(c);
// console.log(d);
// console.log(e);


// rest and spread
// spread operator --> ...

let a = [10, 20];
let b = [30, 40];

console.log(...a, ...b);
console.log([...a, ...b]);

// Template literals
const varA = 10; // Renamed to avoid syntax errors with 'let a' above
const varB = 20; // Renamed to avoid syntax errors with 'let b' above
console.log(`The sum of ${varA} and ${varB} is ${varA+varB}`);