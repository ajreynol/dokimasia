# Static analysis observations

Generated from [bugs.json](bugs.json) by `scripts/append_findings --render-only`.

This is observation history, not a list of confirmed defects or open reports.
Koine preserves the first claim and updates sighting dates. Disappearance does not close a finding.
[Archived run records](runs/) contain the source revisions, actual coverage and evidence keyed by id.
See [the analyzer guide](../analyzer.md) for evidence, limitations and the historical register.

197 observation(s).

| id | check | entity | first seen | last seen | original claim |
| --- | --- | --- | --- | --- | --- |
| dokimasia:b7c725366bc58a3e7f9cef2e | CI0002 | explicit-completeness | 2026-09-16 | 2026-09-16 | Proof completeness chain has an unsatisfied link: explicit-completeness |
| dokimasia:3072fb48c14d001cc274e901 | CI0003 | proof | 2026-09-16 | 2026-09-16 | Proof tester requests lazy proof checking: proof |
| dokimasia:173213b6603a250ad2b75ed5 | CI0004 | ci.yml#ubuntu:production-dbg | 2026-09-16 | 2026-09-16 | Proof-testing job excludes regression levels: ci.yml#ubuntu:production-dbg |
| dokimasia:869cd2d4ae060a2ff98e71fc | CI0004 | ci.yml#ubuntu:production-dbg-clang | 2026-09-16 | 2026-09-16 | Proof-testing job excludes regression levels: ci.yml#ubuntu:production-dbg-clang |
| dokimasia:888eee400926d4583357f20f | CI0004 | ci.yml#ubuntu:safe-mode | 2026-09-16 | 2026-09-16 | Proof-testing job excludes regression levels: ci.yml#ubuntu:safe-mode |
| dokimasia:bd1690ffc0df1a5bf82217c2 | CI0004 | ci.yml#ubuntu:stable-mode | 2026-09-16 | 2026-09-16 | Proof-testing job excludes regression levels: ci.yml#ubuntu:stable-mode |
| dokimasia:8b154bb60f20871edcf303cc | INFER0002 | strings:STRINGS_ARRAY_EQ_SPLIT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_EQ_SPLIT |
| dokimasia:11bb94abc4484e8472f017f4 | INFER0002 | strings:STRINGS_ARRAY_NTH_CONCAT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_CONCAT |
| dokimasia:f3f92720b02069052543680b | INFER0002 | strings:STRINGS_ARRAY_NTH_EXTRACT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_EXTRACT |
| dokimasia:7b9e963acac65d88cec7fb2b | INFER0002 | strings:STRINGS_ARRAY_NTH_REV | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_REV |
| dokimasia:b0ad0f9d2afd5fd6fb5bf0ea | INFER0002 | strings:STRINGS_ARRAY_NTH_TERM_FROM_UPDATE | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_TERM_FROM_UPDATE |
| dokimasia:f68d28963d60dea54aa863b8 | INFER0002 | strings:STRINGS_ARRAY_NTH_UNIT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_UNIT |
| dokimasia:dca3b12538797270b0bec244 | INFER0002 | strings:STRINGS_ARRAY_NTH_UPDATE | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_NTH_UPDATE |
| dokimasia:3e3fa71a344d11e8d6579df4 | INFER0002 | strings:STRINGS_ARRAY_UPDATE_BOUND | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_UPDATE_BOUND |
| dokimasia:b6a97c8195f7373ab43ce97e | INFER0002 | strings:STRINGS_ARRAY_UPDATE_CONCAT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_UPDATE_CONCAT |
| dokimasia:f3ceb699423f164cef2bc790 | INFER0002 | strings:STRINGS_ARRAY_UPDATE_CONCAT_INVERSE | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_UPDATE_CONCAT_INVERSE |
| dokimasia:dc4c6bd6cf28528daf9a4519 | INFER0002 | strings:STRINGS_ARRAY_UPDATE_UNIT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_ARRAY_UPDATE_UNIT |
| dokimasia:a66e545a268dfb3b04aaacb6 | INFER0002 | strings:STRINGS_CMI_SPLIT | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_CMI_SPLIT |
| dokimasia:5e022556c143d42605b9a458 | INFER0002 | strings:STRINGS_CONST_SEQ_PURIFY | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_CONST_SEQ_PURIFY |
| dokimasia:18701205c93a1ef5fedef361 | INFER0002 | strings:STRINGS_REGISTER_TERM | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_REGISTER_TERM |
| dokimasia:23dccb66b37c266332d4f66e | INFER0002 | strings:STRINGS_REGISTER_TERM_ATOMIC | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_REGISTER_TERM_ATOMIC |
| dokimasia:bfef2196d0cd4b91d2549843 | INFER0002 | strings:STRINGS_RE_EQ_ELIM_EQUIV | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_RE_EQ_ELIM_EQUIV |
| dokimasia:a20aa916d259de747cff9456 | INFER0002 | strings:STRINGS_UNIT_INJ_DEQ | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_UNIT_INJ_DEQ |
| dokimasia:0b92631b487d3a5a6c2023df | INFER0002 | strings:STRINGS_UNIT_INJ_OOB | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:STRINGS_UNIT_INJ_OOB |
| dokimasia:94722082985d5b16e32531be | INFER0002 | strings:UNKNOWN | 2026-09-16 | 2026-09-16 | Emitted inference has no case in a reconstructor with a trust fallback: strings:UNKNOWN |
| dokimasia:48bbfd8e0509e5c6a4841116 | INFERID0001 | ARITH_BB_LEMMA | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_BB_LEMMA |
| dokimasia:ba884af5b7c363bec2285036 | INFERID0001 | ARITH_BLACK_BOX | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_BLACK_BOX |
| dokimasia:86095146857e2eec9a618ee1 | INFERID0001 | ARITH_CONF_TRICHOTOMY | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_CONF_TRICHOTOMY |
| dokimasia:892fdc89ddc6cc9273cd08ce | INFERID0001 | ARITH_NL_COMPARISON | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_COMPARISON |
| dokimasia:41ddf38588474ad1250cf7b5 | INFERID0001 | ARITH_NL_COVERING_CONFLICT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_COVERING_CONFLICT |
| dokimasia:71e0d671e331820bf6f8312f | INFERID0001 | ARITH_NL_FACTOR | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_FACTOR |
| dokimasia:91a48c6e52031c18c88e8d9f | INFERID0001 | ARITH_NL_PIAND_ONE_REFINE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_PIAND_ONE_REFINE |
| dokimasia:9e2fdf0395196a6eba12b5d0 | INFERID0001 | ARITH_NL_POW2_MONOTONE_REFINE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_POW2_MONOTONE_REFINE |
| dokimasia:42c12264d9392bbcc4136424 | INFERID0001 | ARITH_NL_SIGN | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_SIGN |
| dokimasia:e95528018cfc776491aa7169 | INFERID0001 | ARITH_NL_T_INIT_REFINE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_T_INIT_REFINE |
| dokimasia:b19668a1c0b7c3bd43612ba9 | INFERID0001 | ARITH_NL_T_MONOTONICITY | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_T_MONOTONICITY |
| dokimasia:03f4a6e90295fc7c76863589 | INFERID0001 | ARITH_NL_T_PURIFY_ARG | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_T_PURIFY_ARG |
| dokimasia:0cabbd51f1ec28110ee3558f | INFERID0001 | ARITH_NL_T_TANGENT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_NL_T_TANGENT |
| dokimasia:9191c38d2cbb842ee17a7575 | INFERID0001 | ARITH_ROW_IMPL | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_ROW_IMPL |
| dokimasia:f865fd793df228210cc2ff88 | INFERID0001 | ARITH_SPLIT_DEQ | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARITH_SPLIT_DEQ |
| dokimasia:e40b8ce46e218805d1798f8e | INFERID0001 | ARRAYS_EQ_TAUTOLOGY | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARRAYS_EQ_TAUTOLOGY |
| dokimasia:a84aad5e8bf8b0a8bc02506d | INFERID0001 | ARRAYS_EXT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARRAYS_EXT |
| dokimasia:b6aea7cbe630974b56b898b3 | INFERID0001 | ARRAYS_READ_OVER_WRITE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: ARRAYS_READ_OVER_WRITE |
| dokimasia:876fdb2d8d9d8325caea0ba4 | INFERID0001 | BAGS_CARD | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: BAGS_CARD |
| dokimasia:72f8188bc5d7c76956c42fd8 | INFERID0001 | BAGS_NON_NEGATIVE_COUNT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: BAGS_NON_NEGATIVE_COUNT |
| dokimasia:25527f7ab9b9d4f2570b49d3 | INFERID0001 | BAGS_SKOLEM | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: BAGS_SKOLEM |
| dokimasia:e4f9fa0872c5b3304b6f03b9 | INFERID0001 | BV_BITBLAST_INTERNAL_BITBLAST_LEMMA | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: BV_BITBLAST_INTERNAL_BITBLAST_LEMMA |
| dokimasia:18d2706bcd8d2a292ddea71e | INFERID0001 | BV_BITBLAST_INTERNAL_EAGER_LEMMA | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: BV_BITBLAST_INTERNAL_EAGER_LEMMA |
| dokimasia:87dec850d99625f9b69ada50 | INFERID0001 | DATATYPES_SPLIT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: DATATYPES_SPLIT |
| dokimasia:389ed73b0ee4d3d442476ab0 | INFERID0001 | DATATYPES_SYGUS_MT_POS | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: DATATYPES_SYGUS_MT_POS |
| dokimasia:c81c7591c0007f5685e91bd8 | INFERID0001 | DATATYPES_SYGUS_SYM_BREAK | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: DATATYPES_SYGUS_SYM_BREAK |
| dokimasia:e1057be02151a423d84c7931 | INFERID0001 | DATATYPES_TESTER_CONFLICT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: DATATYPES_TESTER_CONFLICT |
| dokimasia:6fac0f82cdfff21edd110cfa | INFERID0001 | EQ_CONSTANT_MERGE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: EQ_CONSTANT_MERGE |
| dokimasia:ac2728230c681b4d4d9f7ff6 | INFERID0001 | FP_EQUATE_TERM | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: FP_EQUATE_TERM |
| dokimasia:6ee744fecea1e6ba34031aec | INFERID0001 | FP_PREPROCESS | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: FP_PREPROCESS |
| dokimasia:ff6d0f6e1c42281d3aba1e5d | INFERID0001 | FP_REGISTER_TERM | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: FP_REGISTER_TERM |
| dokimasia:aa5d9eb525081e60b35aa1dd | INFERID0001 | INPUT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: INPUT |
| dokimasia:cb8c03dba0384361aedd2281 | INFERID0001 | QUANTIFIERS_INST_SYQI | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: QUANTIFIERS_INST_SYQI |
| dokimasia:d4a870942cd27c82fd9d67a3 | INFERID0001 | SEP_LABEL_DEF | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SEP_LABEL_DEF |
| dokimasia:acb427da1855a61e3beff843 | INFERID0001 | SEP_NIL_NOT_IN_HEAP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SEP_NIL_NOT_IN_HEAP |
| dokimasia:e4a847443a1215fe08382510 | INFERID0001 | SETS_CARD_POSITIVE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_CARD_POSITIVE |
| dokimasia:fe5dca9a5b2ec0051eb00dc4 | INFERID0001 | SETS_CARD_SPLIT_EMPTY | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_CARD_SPLIT_EMPTY |
| dokimasia:ac0f2f5fa650726c290d77be | INFERID0001 | SETS_DOWN_CLOSURE | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_DOWN_CLOSURE |
| dokimasia:cf0bd16925f0081d772f79f6 | INFERID0001 | SETS_RELS_PRODUCT_SPLIT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_RELS_PRODUCT_SPLIT |
| dokimasia:fb65e81a6fc789d464c2ca9b | INFERID0001 | SETS_RELS_TCLOSURE_FWD | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_RELS_TCLOSURE_FWD |
| dokimasia:efe0dde93886dcd6ddc7d22f | INFERID0001 | SETS_RELS_TCLOSURE_UP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_RELS_TCLOSURE_UP |
| dokimasia:0c443aee3049f39bfcca30bb | INFERID0001 | SETS_RELS_TRANSPOSE_REV | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: SETS_RELS_TRANSPOSE_REV |
| dokimasia:893fcea3e1c9f2bacadd93e9 | INFERID0001 | STRINGS_F_ENDPOINT_EMP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: STRINGS_F_ENDPOINT_EMP |
| dokimasia:8963284bd9cccafa4238b830 | INFERID0001 | STRINGS_LEN_SPLIT_EMP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: STRINGS_LEN_SPLIT_EMP |
| dokimasia:7ce467bc8d3fd363b626e9f5 | INFERID0001 | STRINGS_N_CONST | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: STRINGS_N_CONST |
| dokimasia:475065c47b1bad9a8395cc8f | INFERID0001 | STRINGS_SSPLIT_VAR_PROP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: STRINGS_SSPLIT_VAR_PROP |
| dokimasia:f43497df02a9697b390583e8 | INFERID0001 | TABLES_GROUP_PART_COUNT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: TABLES_GROUP_PART_COUNT |
| dokimasia:d39e21592f36b915397f3ee4 | INFERID0001 | TABLES_PRODUCT_UP | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: TABLES_PRODUCT_UP |
| dokimasia:10c0ba597163030ce15b981a | INFERID0001 | THEORY_PP_SKOLEM_LEM | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: THEORY_PP_SKOLEM_LEM |
| dokimasia:22cf0988a173db1e781e3bc2 | INFERID0001 | UF_CARD_SPLIT | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: UF_CARD_SPLIT |
| dokimasia:803339c38b87e939492c738e | INFERID0001 | UF_DISTINCT_DEQ | 2026-09-16 | 2026-09-16 | Inference id has multiple detected production sites: UF_DISTINCT_DEQ |
| dokimasia:5f3af395aa04b590bb16110b | INFERID0002 | src/printer/printer.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/printer/printer.cpp#UNKNOWN |
| dokimasia:49fbb98f515ca646344e1b89 | INFERID0002 | src/prop/prop_engine.cpp#NONE | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/prop/prop_engine.cpp#NONE |
| dokimasia:2f7de4160667c4488324b03c | INFERID0002 | src/prop/prop_proof_manager.cpp#NONE | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/prop/prop_proof_manager.cpp#NONE |
| dokimasia:060abe1f0875af2bf985354c | INFERID0002 | src/prop/prop_proof_manager.h#NONE | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/prop/prop_proof_manager.h#NONE |
| dokimasia:9f64bf191263a49a8c8b83c3 | INFERID0002 | src/theory/arith/linear/simplex.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/arith/linear/simplex.cpp#UNKNOWN |
| dokimasia:61a324e5668cae61cd6df474 | INFERID0002 | src/theory/arrays/theory_arrays.cpp#NONE | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/arrays/theory_arrays.cpp#NONE |
| dokimasia:bb37803ad2a58b402255d956 | INFERID0002 | src/theory/datatypes/inference.h#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/datatypes/inference.h#UNKNOWN |
| dokimasia:22a4cda1a01e83e8ef43a136 | INFERID0002 | src/theory/quantifiers/instantiate.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/quantifiers/instantiate.cpp#UNKNOWN |
| dokimasia:2e78587e7c1bbf17ef17ce22 | INFERID0002 | src/theory/quantifiers/instantiate.h#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/quantifiers/instantiate.h#UNKNOWN |
| dokimasia:8b8ab3e3ba4920bee3bdab09 | INFERID0002 | src/theory/quantifiers/instantiation_list.h#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/quantifiers/instantiation_list.h#UNKNOWN |
| dokimasia:209b5cf9c916b6b175a25116 | INFERID0002 | src/theory/quantifiers_engine.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/quantifiers_engine.cpp#UNKNOWN |
| dokimasia:9571528b4476546ba891adef | INFERID0002 | src/theory/strings/core_solver.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/strings/core_solver.cpp#UNKNOWN |
| dokimasia:63c42bce6ef4d560907a3b13 | INFERID0002 | src/theory/strings/solver_state.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/strings/solver_state.cpp#UNKNOWN |
| dokimasia:fa5005075b9e4503180ad421 | INFERID0002 | src/theory/strings/theory_strings.cpp#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/theory/strings/theory_strings.cpp#UNKNOWN |
| dokimasia:ee81a9736c679ae9074ad50d | INFERID0002 | src/util/resource_manager.h#UNKNOWN | 2026-09-16 | 2026-09-16 | File produces an inference with a sentinel id: src/util/resource_manager.h#UNKNOWN |
| dokimasia:132aaa98bd050f26c10620c0 | MODE0001 | macrosQuantMode | 2026-09-16 | 2026-09-16 | Proof-unsupported option defaults on without a direct safe-mode override: macrosQuantMode |
| dokimasia:8f5e58e7909a78c7cb8ad149 | MODE0001 | stringLazyPreproc | 2026-09-16 | 2026-09-16 | Proof-unsupported option defaults on without a direct safe-mode override: stringLazyPreproc |
| dokimasia:c009b63a66996c7aae05c365 | RULE0002 | ARITH_POW2_DIV0 | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: ARITH_POW2_DIV0 |
| dokimasia:e051b4d7afac82ad8a5a9725 | RULE0002 | ARITH_POW2_INIT | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: ARITH_POW2_INIT |
| dokimasia:dec6d3277b9a15d18589f6b2 | RULE0002 | ARITH_POW2_LOWER_BOUND | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: ARITH_POW2_LOWER_BOUND |
| dokimasia:54846bee6697f952546d60cc | RULE0002 | ARITH_POW2_MONOTONE | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: ARITH_POW2_MONOTONE |
| dokimasia:b808c7dc9cbf3c9ae4ddbfa2 | RULE0002 | MACRO_BV_BITBLAST | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_BV_BITBLAST |
| dokimasia:9aa0ffddb63df6d66bcf26cc | RULE0002 | MACRO_REWRITE | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_REWRITE |
| dokimasia:d36945c78ef40a64dd5fe80d | RULE0002 | MACRO_SR_EQ_INTRO | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_SR_EQ_INTRO |
| dokimasia:6c35639df95d9115f1ef0e48 | RULE0002 | MACRO_SR_PRED_ELIM | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_SR_PRED_ELIM |
| dokimasia:ed2ac49c89fd2b0094cec8b6 | RULE0002 | MACRO_SR_PRED_INTRO | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_SR_PRED_INTRO |
| dokimasia:6a580e64a53ea16a17fef20f | RULE0002 | MACRO_SR_PRED_TRANSFORM | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_SR_PRED_TRANSFORM |
| dokimasia:c5f922e32a860e8dd72a043f | RULE0002 | MACRO_STRING_INFERENCE | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: MACRO_STRING_INFERENCE |
| dokimasia:e1f2f2d1c8e359a137b01475 | RULE0002 | SAT_REFUTATION | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: SAT_REFUTATION |
| dokimasia:0210b7aeb2404a824122767f | RULE0002 | TRUST | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: TRUST |
| dokimasia:51f59f19e507f706f0b395a7 | RULE0002 | TRUST_THEORY_REWRITE | 2026-09-16 | 2026-09-16 | Produced rule has a trusted checker registration: TRUST_THEORY_REWRITE |
| dokimasia:51e4165811fcedad526f015f | RW0001 | ARRAYS_EQ_RANGE_EXPAND | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: ARRAYS_EQ_RANGE_EXPAND |
| dokimasia:8c2152bf61ebbab62e315a84 | RW0001 | DT_MATCH_ELIM | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: DT_MATCH_ELIM |
| dokimasia:7ccc1213b8d583ec98cdbed4 | RW0001 | MACRO_ARITH_INT_EQ_CONFLICT | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_ARITH_INT_EQ_CONFLICT |
| dokimasia:b7515a3752aa6d258e32a719 | RW0001 | MACRO_ARITH_INT_GEQ_TIGHTEN | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_ARITH_INT_GEQ_TIGHTEN |
| dokimasia:1b332b1708f899970bc9013a | RW0001 | MACRO_ARITH_STRING_PRED_ENTAIL | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_ARITH_STRING_PRED_ENTAIL |
| dokimasia:66e7c5dfab612268f1aa51aa | RW0001 | MACRO_ARRAYS_NORMALIZE_CONSTANT | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_ARRAYS_NORMALIZE_CONSTANT |
| dokimasia:408b7cee84560eb3206799e9 | RW0001 | MACRO_ARRAYS_NORMALIZE_OP | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_ARRAYS_NORMALIZE_OP |
| dokimasia:0f77bbc1fb40868f3dd28b8b | RW0001 | MACRO_BOOL_BV_INVERT_SOLVE | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BOOL_BV_INVERT_SOLVE |
| dokimasia:f5663103d3b0d810072649b1 | RW0001 | MACRO_BOOL_EQ_CONST_EQ | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BOOL_EQ_CONST_EQ |
| dokimasia:c299152f5e5340767dfec6d9 | RW0001 | MACRO_BOOL_NNF_NORM | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BOOL_NNF_NORM |
| dokimasia:c4dfdc165dbc598a53552568 | RW0001 | MACRO_BV_AND_OR_XOR_CONCAT_PULLUP | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_AND_OR_XOR_CONCAT_PULLUP |
| dokimasia:b41ac6ad170a967b5cc6cbdb | RW0001 | MACRO_BV_AND_SIMPLIFY | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_AND_SIMPLIFY |
| dokimasia:176e649e6402e3956df470a1 | RW0001 | MACRO_BV_CONCAT_CONSTANT_MERGE | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_CONCAT_CONSTANT_MERGE |
| dokimasia:b5b190014cb0b4eec0b2fdfe | RW0001 | MACRO_BV_CONCAT_EXTRACT_MERGE | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_CONCAT_EXTRACT_MERGE |
| dokimasia:c3913de41354df96cf68a24b | RW0001 | MACRO_BV_EQ_SOLVE | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_EQ_SOLVE |
| dokimasia:eafbc44506c9c11f834dc7b2 | RW0001 | MACRO_BV_EXTRACT_CONCAT | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_EXTRACT_CONCAT |
| dokimasia:2969b987b8d7d58ddbe642ae | RW0001 | MACRO_BV_MULT_SLT_MULT | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_MULT_SLT_MULT |
| dokimasia:e965de0fc0bf650e0a7f610a | RW0001 | MACRO_BV_OR_SIMPLIFY | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_OR_SIMPLIFY |
| dokimasia:67109b4e1cadd09f4a40aa6f | RW0001 | MACRO_BV_XOR_SIMPLIFY | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_BV_XOR_SIMPLIFY |
| dokimasia:a5b50fe72762fc17e0ff1aff | RW0001 | MACRO_DT_CONS_EQ | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_DT_CONS_EQ |
| dokimasia:4d56c4fe96f2ec5f51f4c0f8 | RW0001 | MACRO_LAMBDA_CAPTURE_AVOID | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_LAMBDA_CAPTURE_AVOID |
| dokimasia:6d4133a4d2b1e508c51dba4b | RW0001 | MACRO_QUANT_DT_VAR_EXPAND | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_DT_VAR_EXPAND |
| dokimasia:bd5f36173968ade02c4bb1d4 | RW0001 | MACRO_QUANT_ELIM_SHADOW | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_ELIM_SHADOW |
| dokimasia:81a1443292a38b5aea74e06a | RW0001 | MACRO_QUANT_MERGE_PRENEX | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_MERGE_PRENEX |
| dokimasia:377e2305cbe3da51576b521f | RW0001 | MACRO_QUANT_MINISCOPE | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_MINISCOPE |
| dokimasia:b0909cfd48964ad1eddd7bab | RW0001 | MACRO_QUANT_PARTITION_CONNECTED_FV | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_PARTITION_CONNECTED_FV |
| dokimasia:28f196a74588a93ef92cd0d4 | RW0001 | MACRO_QUANT_PRENEX | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_PRENEX |
| dokimasia:0040b8a5e5c2cfe65c627a73 | RW0001 | MACRO_QUANT_REWRITE_BODY | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_REWRITE_BODY |
| dokimasia:705c8c48d6c9cea467fbcb4c | RW0001 | MACRO_QUANT_VAR_ELIM_EQ | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_VAR_ELIM_EQ |
| dokimasia:0f5c45cc1d03313101796204 | RW0001 | MACRO_QUANT_VAR_ELIM_INEQ | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_QUANT_VAR_ELIM_INEQ |
| dokimasia:b0a02661c4c2311d19d3fa5c | RW0001 | MACRO_RE_INTER_UNION_CONST_ELIM | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_RE_INTER_UNION_CONST_ELIM |
| dokimasia:35c4ea55cbbce539a5d10f95 | RW0001 | MACRO_RE_INTER_UNION_INCLUSION | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_RE_INTER_UNION_INCLUSION |
| dokimasia:88e84005984ffe0978c81b7d | RW0001 | MACRO_STR_COMPONENT_CTN | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_COMPONENT_CTN |
| dokimasia:d3407c9546f3f798fc3fad42 | RW0001 | MACRO_STR_CONST_NCTN_CONCAT | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_CONST_NCTN_CONCAT |
| dokimasia:e7bd4e0b5fb366e8106979c7 | RW0001 | MACRO_STR_EQ_LEN_UNIFY | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_EQ_LEN_UNIFY |
| dokimasia:6b445b23de55ce7bd641f6a7 | RW0001 | MACRO_STR_EQ_LEN_UNIFY_PREFIX | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_EQ_LEN_UNIFY_PREFIX |
| dokimasia:b97f29280bc0c7c51603c7a1 | RW0001 | MACRO_STR_IN_RE_INCLUSION | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_IN_RE_INCLUSION |
| dokimasia:0f27dda9a887d9c182375b83 | RW0001 | MACRO_STR_SPLIT_CTN | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_SPLIT_CTN |
| dokimasia:af44a693c2c8b720bc5a1108 | RW0001 | MACRO_STR_STRIP_ENDPOINTS | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_STR_STRIP_ENDPOINTS |
| dokimasia:66bddaeb1c2c5a6ebd2b4d4e | RW0001 | MACRO_SUBSTR_STRIP_SYM_LENGTH | 2026-09-16 | 2026-09-16 | Implemented rewrite is refused by the Eunoia seam: MACRO_SUBSTR_STRIP_SYM_LENGTH |
| dokimasia:05376bef2bd8ae0374028947 | RW0002 | ARITH_POW_ELIM | 2026-09-16 | 2026-09-16 | Implemented rewrite is printable only in unrestricted mode: ARITH_POW_ELIM |
| dokimasia:a28f2b53d486fed65d66b6ca | RW0002 | ARRAYS_SELECT_CONST | 2026-09-16 | 2026-09-16 | Implemented rewrite is printable only in unrestricted mode: ARRAYS_SELECT_CONST |
| dokimasia:0279332cf763ee6ee8aef680 | RW0002 | LAMBDA_ELIM | 2026-09-16 | 2026-09-16 | Implemented rewrite is printable only in unrestricted mode: LAMBDA_ELIM |
| dokimasia:062eb733a8dae724e940de73 | SEAM0001 | ARITH_POW2_DIV0 | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_POW2_DIV0 |
| dokimasia:748f82a844b0bba776736635 | SEAM0001 | ARITH_POW2_INIT | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_POW2_INIT |
| dokimasia:a7dbd1c00f5c36a649568f88 | SEAM0001 | ARITH_POW2_LOWER_BOUND | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_POW2_LOWER_BOUND |
| dokimasia:30e63cb96e565a86ab7521d3 | SEAM0001 | ARITH_POW2_MONOTONE | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_POW2_MONOTONE |
| dokimasia:8faf14d6f90a876d327e1e43 | SEAM0001 | ARITH_TRANS_EXP_APPROX_ABOVE_NEG | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_EXP_APPROX_ABOVE_NEG |
| dokimasia:161c447b117d13c88cd7c910 | SEAM0001 | ARITH_TRANS_EXP_APPROX_ABOVE_POS | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_EXP_APPROX_ABOVE_POS |
| dokimasia:971a35b60c04b4054b8296df | SEAM0001 | ARITH_TRANS_EXP_APPROX_BELOW | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_EXP_APPROX_BELOW |
| dokimasia:e4950229a979fc2bd5dcd5e6 | SEAM0001 | ARITH_TRANS_PI | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_PI |
| dokimasia:d692f8ec6d1c705297ec3f0a | SEAM0001 | ARITH_TRANS_SINE_APPROX_ABOVE_NEG | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_SINE_APPROX_ABOVE_NEG |
| dokimasia:a65a9b414b94cc27e7fef002 | SEAM0001 | ARITH_TRANS_SINE_APPROX_ABOVE_POS | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_SINE_APPROX_ABOVE_POS |
| dokimasia:36c3d21d8eb134b44ba19b1d | SEAM0001 | ARITH_TRANS_SINE_APPROX_BELOW_NEG | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_SINE_APPROX_BELOW_NEG |
| dokimasia:25f70ffd050b4be63eb97f7b | SEAM0001 | ARITH_TRANS_SINE_APPROX_BELOW_POS | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_SINE_APPROX_BELOW_POS |
| dokimasia:47d4d359d256c80fda482598 | SEAM0001 | ARITH_TRANS_SINE_SHIFT | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: ARITH_TRANS_SINE_SHIFT |
| dokimasia:77d478b81219cf5aaa18e054 | SEAM0001 | SAT_REFUTATION | 2026-09-16 | 2026-09-16 | Produced rule is refused by the Eunoia seam: SAT_REFUTATION |
| dokimasia:00b8a73a3cd2680c95cf4f9b | SIG0002 | ARITH_VTS_INFINITY | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: ARITH_VTS_INFINITY |
| dokimasia:0a509b2f776901f4ef51cf6c | SIG0002 | ARITH_VTS_INFINITY_FREE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: ARITH_VTS_INFINITY_FREE |
| dokimasia:982cb4cc6d2e637100f5a1f0 | SIG0002 | BAGS_CARD_COMBINE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_CARD_COMBINE |
| dokimasia:02d52f4152e355a3c55db097 | SIG0002 | BAGS_CHOOSE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_CHOOSE |
| dokimasia:557619b267b689db2a15999d | SIG0002 | BAGS_DISTINCT_ELEMENTS_UNION_DISJOINT | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_DISTINCT_ELEMENTS_UNION_DISJOINT |
| dokimasia:b7e0e569d686483992139a44 | SIG0002 | BAGS_FOLD_CARD | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_FOLD_CARD |
| dokimasia:d550aaabdd39e057665cc466 | SIG0002 | BAGS_FOLD_COMBINE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_FOLD_COMBINE |
| dokimasia:55d17c39575173be2fa70dd1 | SIG0002 | BAGS_FOLD_ELEMENTS | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_FOLD_ELEMENTS |
| dokimasia:f23a84b64d59214d3810e35b | SIG0002 | BAGS_FOLD_UNION_DISJOINT | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_FOLD_UNION_DISJOINT |
| dokimasia:0038491b5d6ad676263aeb3f | SIG0002 | BAGS_MAP_INDEX | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BAGS_MAP_INDEX |
| dokimasia:12251ace99cb0b2a4d6366b4 | SIG0002 | BV_TO_INT_UF | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: BV_TO_INT_UF |
| dokimasia:bd7aeb525f2ee794bb575f37 | SIG0002 | FP_TO_REAL | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: FP_TO_REAL |
| dokimasia:ad95a64fca35d65b3f552423 | SIG0002 | GROUND_TERM | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: GROUND_TERM |
| dokimasia:894bb98e4f21e242b2f87d0e | SIG0002 | HO_DEQ_DIFF | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: HO_DEQ_DIFF |
| dokimasia:886b9690c61d861b081e5ff6 | SIG0002 | RELATIONS_GROUP_PART | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: RELATIONS_GROUP_PART |
| dokimasia:39c9c9350c06442e3808ec04 | SIG0002 | RELATIONS_GROUP_PART_ELEMENT | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: RELATIONS_GROUP_PART_ELEMENT |
| dokimasia:3b4a20d9b154d327abdc1af6 | SIG0002 | SETS_CHOOSE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_CHOOSE |
| dokimasia:fd9b47439973a1235b85eee3 | SIG0002 | SETS_FOLD_CARD | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_FOLD_CARD |
| dokimasia:faca4e39c3ec3701b31152c2 | SIG0002 | SETS_FOLD_COMBINE | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_FOLD_COMBINE |
| dokimasia:1919066e2eb0ca24e4664a47 | SIG0002 | SETS_FOLD_ELEMENTS | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_FOLD_ELEMENTS |
| dokimasia:b5f3e588d1f1229581cf77af | SIG0002 | SETS_FOLD_UNION | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_FOLD_UNION |
| dokimasia:55a3d56c8b5e31782c84d4f1 | SIG0002 | SETS_MAP_DOWN_ELEMENT | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SETS_MAP_DOWN_ELEMENT |
| dokimasia:0c8f13fd774b759b177484f6 | SIG0002 | SHARED_SELECTOR | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: SHARED_SELECTOR |
| dokimasia:5246f1e99e0430d43a980b02 | SIG0002 | TRANSCENDENTAL_SINE_PHASE_SHIFT | 2026-09-16 | 2026-09-16 | Constructed skolem is refused by the Eunoia seam: TRANSCENDENTAL_SINE_PHASE_SHIFT |
| dokimasia:398b7ed5b492831606d98491 | SIG0003 | SUBS | 2026-09-16 | 2026-09-16 | Documented rule arity disagrees with detected checker arity: SUBS |
| dokimasia:e4f73244df569300580f58d7 | TRUST0001 | src/proof/conv_proof_generator.h | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/proof/conv_proof_generator.h |
| dokimasia:cd2785c4e205675be495f9d7 | TRUST0001 | src/proof/lazy_proof.h | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/proof/lazy_proof.h |
| dokimasia:2825f336e08fc307f1df6ee4 | TRUST0001 | src/prop/proof_cnf_stream.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/prop/proof_cnf_stream.cpp |
| dokimasia:d8822eb81f19767879abc3f5 | TRUST0001 | src/prop/prop_proof_manager.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/prop/prop_proof_manager.cpp |
| dokimasia:a1e56556bcf0a262b4c74ea3 | TRUST0001 | src/rewriter/rewrite_db_proof_cons.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/rewriter/rewrite_db_proof_cons.cpp |
| dokimasia:ec57ff3121bd60ab12165cfb | TRUST0001 | src/smt/proof_final_callback.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/smt/proof_final_callback.cpp |
| dokimasia:5faf78e7b42ab20ebc8a11d9 | TRUST0001 | src/smt/witness_form.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/smt/witness_form.cpp |
| dokimasia:6b32aecf7ce80879aa161dbd | TRUST0001 | src/theory/strings/infer_proof_cons.cpp | 2026-09-16 | 2026-09-16 | File constructs trust steps with no reason id: src/theory/strings/infer_proof_cons.cpp |
