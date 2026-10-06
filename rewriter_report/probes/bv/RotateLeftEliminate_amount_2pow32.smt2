; differential: rotate_left 2^32 on width 3 (= rotate by 1, since 2^32 mod 3 = 1). Not a rewrite bug: binary dc8ad24031's parser
; saturates the index to 4294967295 (mod 3 = 0) and answers sat; HEAD (c403bf1c3e) rejects indices >= 2^32 with a parse error; z3 rejects too.
; EXPECT: unsat
(set-logic QF_BV)
(declare-const x (_ BitVec 3))
(assert (not (= ((_ rotate_left 4294967296) x) (concat ((_ extract 1 0) x) ((_ extract 2 2) x)))))
(check-sat)
