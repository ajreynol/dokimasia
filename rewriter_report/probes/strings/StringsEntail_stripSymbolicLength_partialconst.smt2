; substr("abc"++x, 0, 2+len y): partial constant strip
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (str.substr (str.++ "abc" x) 0 (+ 2 (str.len y))) (str.++ "ab" (str.substr (str.++ "c" x) 0 (str.len y))))))
(check-sat)
