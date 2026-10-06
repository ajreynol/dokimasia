; contains("abc", str.from_code(n)++"ab") is satisfiable only with from_code empty or ...
; EXPECT: sat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains "abc" (str.++ (str.from_code n) "bc")))
(check-sat)
