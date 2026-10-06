; star of (str.to_re z) is not fixed length 1
; EXPECT: sat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (= (str.len z) 1))
(assert (str.in_re (str.++ x y) (re.* (str.to_re (str.++ z z)))))
(assert (not (str.in_re x (re.* (str.to_re (str.++ z z))))))
(check-sat)
