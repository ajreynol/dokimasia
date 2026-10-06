; len-based: x++w = y++x++z with len y >= len w? (eq len unify prefix)
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (not (= (= (str.++ "a" x) (str.++ y "a" x z)) (and (= y "") (= z "")))))
(check-sat)
