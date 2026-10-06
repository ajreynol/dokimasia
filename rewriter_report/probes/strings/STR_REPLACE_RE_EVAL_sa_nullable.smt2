; replace_re with nullable regex replaces empty match at 0
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (= (str.replace_re "abc" (re.* (str.to_re "b")) "Q") "Qabc")))
(check-sat)
