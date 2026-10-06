; star of non-fixed-length RE must not distribute: xy=ab in (ab)* but x,y not
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (str.in_re (str.++ x y) (re.* (str.to_re "ab"))))
(assert (not (str.in_re x (re.* (str.to_re "ab")))))
(check-sat)
