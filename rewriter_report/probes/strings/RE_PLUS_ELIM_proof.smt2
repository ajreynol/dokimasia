; re.+ eliminated to R ++ R*
; EXPECT: unsat
(set-logic QF_SLIA)
(declare-const x String)
(declare-const y String)
(declare-const z String)
(declare-const w String)
(assert (not (= (str.in_re x (re.+ (re.range "a" "c"))) (str.in_re x (re.++ (re.range "a" "c") (re.* (re.range "a" "c")))))))
(check-sat)
