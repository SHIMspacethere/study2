const operations = {
  '>=': (n, m) => n >= m,
  '<=': (n, m) => n <= m,
  '>!': (n, m) => n > m,
  '<!': (n, m) => n < m,
};

function solution(ineq, eq, n, m) {
  const op = operations[ineq + eq];
  console.log(op)
  return Number(op(n, m));
}


console.log(solution('<', '=', 3, 4));

// 방법3-2.
const squared = array.map(n => n * n);
console.log(squared);