; ab++x++y = x++cd++w <=> ab++x = x++cd and y = w
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (= (str.++ "ab" x y) (str.++ x "cd" w)) (and (= (str.++ "ab" x) (str.++ x "cd")) (= y w)))))
(check-sat)
