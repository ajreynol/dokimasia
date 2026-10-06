; substr("ab"++x, 3+len y, n) = substr(x, 1+len y, n)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr (str.++ "ab" x) (+ 3 (str.len y)) n) (str.substr x (+ 1 (str.len y)) n))))
(check-sat)
