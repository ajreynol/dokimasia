; ab++x in (ab|a b)++c* ; union branches agree -> consume; x=c sat
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(assert (str.in_re (str.++ "ab" x) (re.++ (re.union (str.to_re "ab") (re.++ (str.to_re "a") (re.range "b" "b"))) (re.* (str.to_re "c")))))
(assert (= x "c"))
(check-sat)
