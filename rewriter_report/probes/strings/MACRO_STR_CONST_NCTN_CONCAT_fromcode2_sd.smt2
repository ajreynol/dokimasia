; contains("abc", str.from_code(n)++"c"++str.from_code(m)) false? (needs 2 chars around c)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (str.contains "abc" (str.++ (str.from_code n) "c" (str.from_code m) "a")))
(check-sat)
