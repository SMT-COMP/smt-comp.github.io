#!/bin/bash


for name in ./*.md; do
  sed -i 's/2020/2021/g' $name
done

# sed -i 's/QF_FPLRA/QF_machine_fp/g' $1
# sed -i 's/QF_FP/QF_machine_fp/g' $1
# sed -i 's/QF_UFFP/QF_machine_fp/g' $1
# sed -i 's/QF_BVFPLRA/QF_machine_fp/g' $1
# sed -i 's/QF_BVFP/QF_machine_fp/g' $1
# sed -i 's/QF_ABVFPLRA/QF_machine_fp/g' $1
# sed -i 's/QF_ABVFP/QF_machine_fp/g' $1

# sed -i 's/QF_ABV/QF_machine_cc_bv/g' $1
# sed -i 's/QF_UFBV/QF_machine_cc_bv/g' $1
# sed -i 's/QF_AUFBV/QF_machine_cc_bv/g' $1

# # sed -i 's/QF_LIA/QF_la/g' $1
# # sed -i 's/QF_LIRA/QF_la/g' $1
# # sed -i 's/QF_IDL/QF_la/g' $1
# # sed -i 's/QF_LRA/QF_la/g' $1
# # sed -i 's/QF_RDL/QF_la/g' $1

# sed -i 's/QF_LIA/QF_lia/g' $1
# sed -i 's/QF_LIRA/QF_lia/g' $1
# sed -i 's/QF_IDL/QF_lia/g' $1
# sed -i 's/QF_LRA/QF_lra/g' $1
# sed -i 's/QF_RDL/QF_lra/g' $1

# # sed -i 's/QF_NIA/QF_na/g' $1
# # sed -i 's/QF_NIRA/QF_na/g' $1
# # sed -i 's/QF_NRA/QF_na/g' $1

# sed -i 's/QF_NIA/QF_nia/g' $1
# sed -i 's/QF_NIRA/QF_nia/g' $1
# sed -i 's/QF_NRA/QF_nra/g' $1

# sed -i 's/QF_ALIA/QF_cc_la/g' $1
# sed -i 's/QF_AUFLIA/QF_cc_la/g' $1
# sed -i 's/QF_UFLIA/QF_cc_la/g' $1
# sed -i 's/QF_UFLRA/QF_cc_la/g' $1
# sed -i 's/QF_UFIDL/QF_cc_la/g' $1

# sed -i 's/QF_ANIA/QF_cc_na/g' $1
# sed -i 's/QF_AUFNIA/QF_cc_na/g' $1
# sed -i 's/QF_UFNIA/QF_cc_na/g' $1
# sed -i 's/QF_UFNRA/QF_cc_na/g' $1

# sed -i 's/QF_UF/QF_cc/g' $1
# sed -i 's/QF_AX/QF_cc/g' $1
# sed -i 's/QF_DT/QF_cc/g' $1

# sed -i 's/QF_SLIA/QF_str/g' $1
# sed -i 's/QF_S/QF_str/g' $1

# # quantifiers + auf

# sed -i 's/ALIA/cc_la/g' $1
# sed -i 's/AUFLIA/cc_la/g' $1
# sed -i 's/UFLIA/cc_la/g' $1
# sed -i 's/UFIDL/cc_la/g' $1
# sed -i 's/AUFLIRA/cc_la/g' $1
# sed -i 's/AUFDTLIA/cc_la/g' $1
# sed -i 's/AUFDTLIRA/cc_la/g' $1
# sed -i 's/UFLRA/cc_la/g' $1
# sed -i 's/UFDTLIA/cc_la/g' $1
# sed -i 's/UFDTLIRA/cc_la/g' $1

# sed -i 's/AUFDTNIRA/cc_na/g' $1
# sed -i 's/AUFNIA/cc_na/g' $1
# sed -i 's/AUFNIRA/cc_na/g' $1
# sed -i 's/UFDTNIA/cc_na/g' $1
# sed -i 's/UFDTNIRA/cc_na/g' $1
# sed -i 's/UFNIA/cc_na/g' $1

# sed -i 's/AUFBVDTLIA/cc_machine/g' $1
# sed -i 's/AUFFPDTLIRA/cc_machine/g' $1
# sed -i 's/UFFPDTLIRA/cc_machine/g' $1
# sed -i 's/UFFPDTNIRA/cc_machine/g' $1
# sed -i 's/ABVFPLRA/cc_machine/g' $1
# sed -i 's/ABVFP/cc_machine/g' $1
# sed -i 's/UFBV/cc_machine/g' $1

# sed -i 's/UFDT/cc/g' $1
# sed -i 's/UF/cc/g' $1

# # quantifiers pure

# sed -i 's/BVFPLRA/machine/g' $1
# sed -i 's/BVFP/machine/g' $1
# sed -i 's/FPLRA/machine/g' $1
# sed -i 's/FP/machine/g' $1

# sed -i 's/LRA/arith/g' $1
# sed -i 's/LIA/arith/g' $1
# sed -i 's/NIA/arith/g' $1
# sed -i 's/NRA/arith/g' $1
