; replace_re with nullable regex prepends
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(declare-const n Int)
(declare-const m Int)
(assert (not (= (str.replace_re x (re.* (str.to_re "a")) y) (str.++ y x))))
(check-sat)
