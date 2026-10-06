; x in range a..c iff 97<=code x<=99
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.range "a" "c")) (and (<= 97 (str.to_code x)) (<= (str.to_code x) 99)))))
(check-sat)
