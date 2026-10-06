; substr(x++y++"ab", 0, len x) strips end
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr (str.++ x y "ab") 0 (str.len x)) x)))
(check-sat)
