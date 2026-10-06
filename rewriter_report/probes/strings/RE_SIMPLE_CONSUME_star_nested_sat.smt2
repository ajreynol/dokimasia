; ab++x in (a b*)*: x=b gives abb in (ab*)*, x not in it
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "ab" x) (re.* (re.++ (str.to_re "a") (re.* (str.to_re "b"))))))
(assert (not (str.in_re x (re.* (re.++ (str.to_re "a") (re.* (str.to_re "b")))))))
(check-sat)
