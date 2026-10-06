; replace_re_all with nullable a*: only non-empty matches replaced
; EXPECT: unsat
(set-logic ALL)
(declare-const x String)
(declare-const y String)
(declare-const n Int)
(assert (not (and (= (str.replace_re_all "bab" (re.* (str.to_re "a")) "X") "bXb") (= (str.replace_re_all "" (re.* (str.to_re "a")) "X") "") (= (str.replace_re_all "ab" (str.to_re "") "X") "ab"))))
(check-sat)
