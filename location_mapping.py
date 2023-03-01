keys = [
        "operations_labs", "operations_shamir", "operations_malrad", "operations_aliza", "operations_cahanov", "operations_oncology", "operations_mall",
        "labs_operations", "labs_shamir", "labs_malrad", "labs_aliza", "labs_cahanov", "labs_oncology", "labs_mall",
        "shamir_operations", "shamir_labs", "shamir_malrad", "shamir_aliza", "shamir_cahanov", "shamir_oncology", "shamir_mall",
        "malrad_operations", "malrad_labs", "malrad_shamir", "malrad_aliza", "malrad_cahanov", "malrad_oncology", "malrad_mall",
        "aliza_operations", "aliza_labs", "aliza_shamir", "aliza_malrad", "aliza_cahanov", "aliza_oncology", "aliza_mall",
        "cahanov_operations", "cahanov_labs", "cahanov_shamir", "cahanov_malrad", "cahanov_aliza", "cahanov_oncology", "cahanov_mall",
        "oncology_operations", "oncology_labs", "oncology_shamir", "oncology_malrad", "oncology_aliza", "oncology_cahanov", "oncology_mall",
        "mall_operations", "mall_labs", "mall_shamir", "mall_malrad", "mall_aliza", "mall_cahanov", "mall_oncology"
        ]

values = [
          "./more/labs_operations.png",  "./more/operations_shamir.png",  "./more/operations_malrad.png",  "./more/operations_cahanov.png",  "./more/operations_aliza.png", "./more/operations_oncology.png", "./more/operations_mall.png",
          "./more/labs_operations.png",  "./more/labs_shamir.png",  "./more/labs_malrad.png",  "./more/labs_aliza.png", "./more/labs_cahanov.png", "./more/labs_oncology.png",  "./more/labs_mall.png",
          "./more/operations_shamir.png",  "./more/labs_shamir.png",  "./more/malrad_shamir.png",  "./more/shamir_aliza.png",  "./more/shamir_cahanov.png", "./more/shamir_oncology.png",  "./more/shamir_mall.png",
          "./more/operations_malrad.png",  "./more/labs_malrad.png",  "./more/malrad_shamir.png",  "./more/aliza_malrad.png",  "./more/malrad_cahanov.png", "./more/malrad_oncology.png",  "./more/malrad_mall.png",
          "./more/operations_aliza.png",  "./more/labs_aliza.png",  "./more/shamir_aliza.png",  "./more/aliza_malrad.png",  "./more/aliza_cahanov.png", "./more/aliza_oncology.png",  "./more/aliza_mall.png",
          "./more/operations_cahanov.png",  "./more/labs_cahanov.png",  "./more/shamir_cahanov.png",  "./more/malrad_cahanov.png",  "./more/aliza_cahanov.png", "./more/cahanov_oncology.png",  "./more/cahanov_mall.png",
          "./more/operations_oncology.png",  "./more/labs_oncology.png",  "./more/shamir_oncology.png",  "./more/malrad_oncology.png",  "./more/aliza_oncology.png", "./more/cahanov_oncology.png",  "./more/oncology_mall.png",
          "./more/operations_mall.png",  "./more/labs_mall.png",  "./more/shamir_mall.png",  "./more/malrad_mall.png",  "./more/aliza_mall.png", "./more/cahanov_mall.png",  "./more/oncology_mall.png"
        ]

my_dict = {keys[i]: values[i] for i in range(len(keys))}
