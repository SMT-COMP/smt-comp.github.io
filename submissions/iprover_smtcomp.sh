{    "name": "iProver v3.9",
    "contributors": [{ "name": "Konstantin Korovin", "website": "http://www.cs.man.ac.uk/~korovink/" }],
    "contacts": ["Konstantin Korovin <kostyakor@gmail.com>"],
    "archive": {
        "url": "https://zenodo.org/records/11636244",
        "h": { "sha256": "8f7f4bad13e87d6aaa1bb8ca78b102edaa5495caf65d5fe39c3c16d6f70003d6" }},
    "website": "https://gitlab.com/korovin/iprover",
    "system_description": "http://www.cs.man.ac.uk/~korovink/iprover-smt-comp-2024.pdf",
    "command": ["cd bin; iprover_smtcomp.sh"],    
    "solver_type": "wrapped",
    "participations": [
        { "tracks": ["SingleQuery"],
          "divisions" :["Arith","Equality","Equality+LinearArith","Equality+NonLinearArith"],        
          "logics": ["ALIA, ANIA, AUFDTLIA, AUFDTLIRA, AUFDTNIRA, AUFLIA, AUFLIRA, AUFNIA, AUFNIRA, LIA, LRA, NIA, NRA, UF, UFDT, UFDTLIA, UFDTLIRA, UFDTNIA, UFDTNIRA, UFIDL, UFLIA, UFLRA, UFNIA, UFNIRA"] },
        { "tracks": ["Parallel"],
          "divisions" :["Arith","Equality","Equality+LinearArith","Equality+NonLinearArith"],          
            "logics": ["ALIA, ANIA, AUFDTLIA, AUFDTLIRA, AUFDTNIRA, AUFLIA, AUFLIRA, AUFNIA, AUFNIRA, LIA, LRA, NIA, NRA, UF, UFDT, UFDTLIA, UFDTLIRA, UFDTNIA, UFDTNIRA, UFIDL, UFLIA, UFLRA, UFNIA, UFNIRA"]}]}
