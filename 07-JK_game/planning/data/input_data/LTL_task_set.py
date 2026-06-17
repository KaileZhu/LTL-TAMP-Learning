task1='<>(repairp32_p32 && <> ( ! repairp32_p32 && photop32_p32)) && <> checkt6_t6 && <> weedp10_p10 && <> washp15_p15'
task2='<>(blow_p7 && <> ( wash_p7 && <> weed_p7) && <> ( sweep_p7 && <> photo_p7)) && [](wash_p7 -> ! weed_p7)'
task3='<>(blowp1_p1 && <> ( shootp1_p1 && ! blowp1_p1  && <> (sweepp1_p1 && ! shootp1_p1))) &&' \
     ' <>(shootp12_p12 && <> sweepp12_p12) && ' \
     '<>(blowp7_p7 && <>( shootp7_p7 && ! blowp7_p7 && <> (washp7_p7 && ! shootp7_p7)))'