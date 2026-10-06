; proof of replace_re_all evaluation with symbolic replacement
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)(declare-const y String)(declare-const z String)(declare-const w String)(declare-const n Int)(declare-const m Int)
(assert (= x "zabzab"))(assert (not (= (str.replace_re_all x (str.to_re "ab") y) (str.++ "z" y "z" y))))
(check-sat)
