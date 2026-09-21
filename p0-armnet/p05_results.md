# ArmnetBench P0.5 Results

K=32 normalized time points; target is strict success versus failure/suboptimal; new downloaded bytes=64351279; no video/GPU/simulator.

## Gate A — single-arm

| Variant | Leave-task AUC | Leave-policy AUC | Leave-task balanced accuracy | Leave-policy balanced accuracy | Leave-task Brier | Leave-policy Brier | Leave-task ECE | Leave-policy ECE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| content-only | 0.9385738452486025 | 0.9628322055506522 | 0.8373951897616946 | 0.9229276993233304 | 0.07539377238084603 | 0.051749084407161826 | 0.03738371040046917 | 0.022985541334969595 |
| content+log(length) | 0.9523953123467687 | 0.9671692654702363 | 0.8622744434637638 | 0.9267394822006473 | 0.06628572115638168 | 0.047553640035048306 | 0.031635052159974995 | 0.01922025667866706 |

Relative-horizon summary: {'mixed_strata': 46, 'strata': [{'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'act', 'n': 30, 'successful': 15, 'non_successful': 15, 'relative_horizon_success_mean': -0.8854427278637641, 'relative_horizon_non_success_mean': 0.8854427278637639, 'relative_horizon_auc': 0.06666666666666667}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'diffusion', 'n': 30, 'successful': 7, 'non_successful': 23, 'relative_horizon_success_mean': -1.7313605230311435, 'relative_horizon_non_success_mean': 0.5269358113573047, 'relative_horizon_auc': 0.0}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 18, 'non_successful': 12, 'relative_horizon_success_mean': -0.7619912312470888, 'relative_horizon_non_success_mean': 1.1429868468706335, 'relative_horizon_auc': 0.0}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'molmoact2', 'n': 60, 'successful': 6, 'non_successful': 54, 'relative_horizon_success_mean': -2.5461464011666957, 'relative_horizon_non_success_mean': 0.28290515568518804, 'relative_horizon_auc': 0.012345679012345678}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'pi0', 'n': 30, 'successful': 5, 'non_successful': 25, 'relative_horizon_success_mean': -1.8412565348612833, 'relative_horizon_non_success_mean': 0.36825130697225644, 'relative_horizon_auc': 0.012}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'pi0.5', 'n': 30, 'successful': 14, 'non_successful': 16, 'relative_horizon_success_mean': -0.8933958543522733, 'relative_horizon_non_success_mean': 0.7817213725582395, 'relative_horizon_auc': 0.0}, {'task': 'Insert the colourful ring into the central wooden peg', 'policy_type': 'smolvla', 'n': 45, 'successful': 17, 'non_successful': 28, 'relative_horizon_success_mean': -1.2517335360731918, 'relative_horizon_non_success_mean': 0.7599810754730089, 'relative_horizon_auc': 0.0}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'act', 'n': 60, 'successful': 7, 'non_successful': 53, 'relative_horizon_success_mean': -0.23141158886452892, 'relative_horizon_non_success_mean': 0.030563794755692424, 'relative_horizon_auc': 0.4164420485175202}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'diffusion', 'n': 30, 'successful': 7, 'non_successful': 23, 'relative_horizon_success_mean': -1.3488498580123445, 'relative_horizon_non_success_mean': 0.41051952200375613, 'relative_horizon_auc': 0.16149068322981366}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 5, 'non_successful': 25, 'relative_horizon_success_mean': -0.306587671262569, 'relative_horizon_non_success_mean': 0.06131753425251467, 'relative_horizon_auc': 0.364}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'molmoact2', 'n': 60, 'successful': 5, 'non_successful': 55, 'relative_horizon_success_mean': -1.3932784729188286, 'relative_horizon_non_success_mean': 0.12666167935625697, 'relative_horizon_auc': 0.07636363636363637}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'pi0', 'n': 30, 'successful': 12, 'non_successful': 18, 'relative_horizon_success_mean': -0.8578406452568386, 'relative_horizon_non_success_mean': 0.5718937635045589, 'relative_horizon_auc': 0.12962962962962962}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'pi0.5', 'n': 30, 'successful': 16, 'non_successful': 14, 'relative_horizon_success_mean': -0.6700453090992583, 'relative_horizon_non_success_mean': 0.7657660675420095, 'relative_horizon_auc': 0.20982142857142858}, {'task': 'Insert the missing tool into the empty slot on the toolbox', 'policy_type': 'smolvla', 'n': 60, 'successful': 2, 'non_successful': 58, 'relative_horizon_success_mean': -0.5705380974923473, 'relative_horizon_non_success_mean': 0.019673727499736317, 'relative_horizon_auc': 0.3275862068965517}, {'task': 'Put the eye drops into the basket', 'policy_type': 'act', 'n': 30, 'successful': 19, 'non_successful': 11, 'relative_horizon_success_mean': -0.7580308338285099, 'relative_horizon_non_success_mean': 1.3093259857037896, 'relative_horizon_auc': 0.0}, {'task': 'Put the eye drops into the basket', 'policy_type': 'diffusion', 'n': 30, 'successful': 13, 'non_successful': 17, 'relative_horizon_success_mean': -0.9872975586123744, 'relative_horizon_non_success_mean': 0.7549922507035806, 'relative_horizon_auc': 0.01809954751131222}, {'task': 'Put the eye drops into the basket', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 20, 'non_successful': 10, 'relative_horizon_success_mean': -0.5128596581790887, 'relative_horizon_non_success_mean': 1.025719316358178, 'relative_horizon_auc': 0.085}, {'task': 'Put the eye drops into the basket', 'policy_type': 'molmoact2', 'n': 60, 'successful': 20, 'non_successful': 40, 'relative_horizon_success_mean': -1.313491700285732, 'relative_horizon_non_success_mean': 0.6567458501428659, 'relative_horizon_auc': 0.0075}, {'task': 'Put the eye drops into the basket', 'policy_type': 'pi0', 'n': 30, 'successful': 21, 'non_successful': 9, 'relative_horizon_success_mean': -0.3923336985701414, 'relative_horizon_non_success_mean': 0.9154452966636636, 'relative_horizon_auc': 0.16137566137566137}, {'task': 'Put the eye drops into the basket', 'policy_type': 'pi0.5', 'n': 30, 'successful': 20, 'non_successful': 10, 'relative_horizon_success_mean': -0.6042153098543555, 'relative_horizon_non_success_mean': 1.2084306197087114, 'relative_horizon_auc': 0.015}, {'task': 'Put the eye drops into the basket', 'policy_type': 'smolvla', 'n': 30, 'successful': 7, 'non_successful': 23, 'relative_horizon_success_mean': -1.428995372716776, 'relative_horizon_non_success_mean': 0.43491163517467113, 'relative_horizon_auc': 0.049689440993788817}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'diffusion', 'n': 30, 'successful': 5, 'non_successful': 25, 'relative_horizon_success_mean': -2.022947522390671, 'relative_horizon_non_success_mean': 0.4045895044781335, 'relative_horizon_auc': 0.0}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 13, 'non_successful': 17, 'relative_horizon_success_mean': -1.0700325024075232, 'relative_horizon_non_success_mean': 0.818260148899871, 'relative_horizon_auc': 0.004524886877828055}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'molmoact2', 'n': 60, 'successful': 14, 'non_successful': 46, 'relative_horizon_success_mean': -1.7817723509164711, 'relative_horizon_non_success_mean': 0.542278541583274, 'relative_horizon_auc': 0.0}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'pi0', 'n': 29, 'successful': 22, 'non_successful': 7, 'relative_horizon_success_mean': -0.43340282223578447, 'relative_horizon_non_success_mean': 1.3621231555981788, 'relative_horizon_auc': 0.045454545454545456}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'pi0.5', 'n': 30, 'successful': 21, 'non_successful': 9, 'relative_horizon_success_mean': -0.5476276920570798, 'relative_horizon_non_success_mean': 1.277797948133186, 'relative_horizon_auc': 0.05291005291005291}, {'task': 'Put the eye drops on the shelf', 'policy_type': 'smolvla', 'n': 60, 'successful': 4, 'non_successful': 56, 'relative_horizon_success_mean': -2.8187403749323487, 'relative_horizon_non_success_mean': 0.2013385982094534, 'relative_horizon_auc': 0.0}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'act', 'n': 30, 'successful': 18, 'non_successful': 12, 'relative_horizon_success_mean': -0.7909952382559797, 'relative_horizon_non_success_mean': 1.1864928573839697, 'relative_horizon_auc': 0.0}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'diffusion', 'n': 30, 'successful': 2, 'non_successful': 28, 'relative_horizon_success_mean': -3.487417438538015, 'relative_horizon_non_success_mean': 0.24910124560985875, 'relative_horizon_auc': 0.0}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 10, 'non_successful': 20, 'relative_horizon_success_mean': -0.7563622935669071, 'relative_horizon_non_success_mean': 0.3781811467834538, 'relative_horizon_auc': 0.3825}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'molmoact2', 'n': 60, 'successful': 17, 'non_successful': 43, 'relative_horizon_success_mean': -1.3938587110410945, 'relative_horizon_non_success_mean': 0.5510604206441535, 'relative_horizon_auc': 0.0533515731874145}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'pi0', 'n': 30, 'successful': 14, 'non_successful': 16, 'relative_horizon_success_mean': -0.7775910865967308, 'relative_horizon_non_success_mean': 0.6803922007721392, 'relative_horizon_auc': 0.10714285714285714}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'pi0.5', 'n': 30, 'successful': 21, 'non_successful': 9, 'relative_horizon_success_mean': -0.559309298600858, 'relative_horizon_non_success_mean': 1.3050550300686687, 'relative_horizon_auc': 0.023809523809523808}, {'task': 'Remove the power cable from cable holder', 'policy_type': 'smolvla', 'n': 30, 'successful': 11, 'non_successful': 19, 'relative_horizon_success_mean': -1.1977198388385626, 'relative_horizon_non_success_mean': 0.6934167488012735, 'relative_horizon_auc': 0.014354066985645933}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'act', 'n': 30, 'successful': 8, 'non_successful': 22, 'relative_horizon_success_mean': -1.3508080115418912, 'relative_horizon_non_success_mean': 0.4912029132879603, 'relative_horizon_auc': 0.05113636363636364}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'diffusion', 'n': 30, 'successful': 19, 'non_successful': 11, 'relative_horizon_success_mean': -0.5895871499568347, 'relative_horizon_non_success_mean': 1.0183778044708964, 'relative_horizon_auc': 0.05741626794258373}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 9, 'non_successful': 21, 'relative_horizon_success_mean': -1.129628741557142, 'relative_horizon_non_success_mean': 0.4841266035244884, 'relative_horizon_auc': 0.164021164021164}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'molmoact2', 'n': 60, 'successful': 6, 'non_successful': 54, 'relative_horizon_success_mean': -2.33109337369806, 'relative_horizon_non_success_mean': 0.2590103748553401, 'relative_horizon_auc': 0.016975308641975308}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'pi0', 'n': 30, 'successful': 3, 'non_successful': 27, 'relative_horizon_success_mean': -2.958142166635941, 'relative_horizon_non_success_mean': 0.32868246295954934, 'relative_horizon_auc': 0.0}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'pi0.5', 'n': 30, 'successful': 4, 'non_successful': 26, 'relative_horizon_success_mean': -1.212262539795689, 'relative_horizon_non_success_mean': 0.18650192919933645, 'relative_horizon_auc': 0.3605769230769231}, {'task': 'Remove the small middle tool (3/8 Extension Bar 75mm) from the toolbox', 'policy_type': 'smolvla', 'n': 30, 'successful': 1, 'non_successful': 29, 'relative_horizon_success_mean': -5.237257705871309, 'relative_horizon_non_success_mean': 0.18059509330590662, 'relative_horizon_auc': 0.0}, {'task': 'Stack the colouful blocks on top of each other', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 8, 'non_successful': 22, 'relative_horizon_success_mean': -1.249368940287769, 'relative_horizon_non_success_mean': 0.45431597828646114, 'relative_horizon_auc': 0.20454545454545456}, {'task': 'Stack the colouful blocks on top of each other', 'policy_type': 'molmoact2', 'n': 60, 'successful': 3, 'non_successful': 57, 'relative_horizon_success_mean': -0.9381447106460802, 'relative_horizon_non_success_mean': 0.049376037402425424, 'relative_horizon_auc': 0.24561403508771928}, {'task': 'Stack the colouful blocks on top of each other', 'policy_type': 'pi0', 'n': 30, 'successful': 10, 'non_successful': 20, 'relative_horizon_success_mean': -1.3850503453027423, 'relative_horizon_non_success_mean': 0.692525172651371, 'relative_horizon_auc': 0.0}, {'task': 'Stack the colouful blocks on top of each other', 'policy_type': 'pi0.5', 'n': 30, 'successful': 13, 'non_successful': 17, 'relative_horizon_success_mean': -1.0114715837526875, 'relative_horizon_non_success_mean': 0.7734782699285256, 'relative_horizon_auc': 0.0}, {'task': 'Stack the colouful blocks on top of each other', 'policy_type': 'smolvla', 'n': 45, 'successful': 3, 'non_successful': 42, 'relative_horizon_success_mean': -2.9259654176375562, 'relative_horizon_non_success_mean': 0.2089975298312541, 'relative_horizon_auc': 0.007936507936507936}], 'pooled_relative_horizon_auc': 0.0993803971312875, 'within_stratum_permuted_length_auc': 0.4981460701566083, 'all_strata_have_shorter_success': True}

## Gate B — bimanual

| Variant | Leave-task AUC | Leave-policy AUC | Leave-task balanced accuracy | Leave-policy balanced accuracy | Leave-task Brier | Leave-policy Brier |
|---|---:|---:|---:|---:|---:|---:|
| content-only | 0.7159312422470318 | 0.9244550770866561 | 0.5598942642802293 | 0.8296886998641384 | 0.2047373787160593 | 0.0938053071562985 |
| content+log(length) | 0.7214129600094512 | 0.9257309941520467 | 0.5665308051272964 | 0.8303059838147557 | 0.20137079942886996 | 0.09293698671767557 |

Bimanual relative-horizon summary: {'mixed_strata': 25, 'strata': [{'task': 'Fold the brown tea towel', 'policy_type': 'act', 'n': 60, 'successful': 3, 'non_successful': 57, 'relative_horizon_success_mean': -0.9287473499798383, 'relative_horizon_non_success_mean': 0.04888143947262318, 'relative_horizon_auc': 0.24561403508771928}, {'task': 'Fold the brown tea towel', 'policy_type': 'diffusion', 'n': 30, 'successful': 15, 'non_successful': 15, 'relative_horizon_success_mean': -0.849596684709874, 'relative_horizon_non_success_mean': 0.8495966847098735, 'relative_horizon_auc': 0.024444444444444446}, {'task': 'Fold the brown tea towel', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 4, 'non_successful': 26, 'relative_horizon_success_mean': -2.0326736227491384, 'relative_horizon_non_success_mean': 0.3127190188844836, 'relative_horizon_auc': 0.019230769230769232}, {'task': 'Fold the brown tea towel', 'policy_type': 'molmoact2', 'n': 60, 'successful': 6, 'non_successful': 54, 'relative_horizon_success_mean': -1.5931588776269614, 'relative_horizon_non_success_mean': 0.17701765306966186, 'relative_horizon_auc': 0.07716049382716049}, {'task': 'Fold the brown tea towel', 'policy_type': 'pi0', 'n': 30, 'successful': 15, 'non_successful': 15, 'relative_horizon_success_mean': -0.4451172052905143, 'relative_horizon_non_success_mean': 0.4451172052905142, 'relative_horizon_auc': 0.34444444444444444}, {'task': 'Fold the brown tea towel', 'policy_type': 'pi0.5', 'n': 30, 'successful': 21, 'non_successful': 9, 'relative_horizon_success_mean': -0.11941204843400621, 'relative_horizon_non_success_mean': 0.2786281130126823, 'relative_horizon_auc': 0.5238095238095238}, {'task': 'Fold the brown tea towel', 'policy_type': 'smolvla', 'n': 60, 'successful': 5, 'non_successful': 55, 'relative_horizon_success_mean': -1.6569312144081405, 'relative_horizon_non_success_mean': 0.15063011040073987, 'relative_horizon_auc': 0.08181818181818182}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'diffusion', 'n': 30, 'successful': 22, 'non_successful': 8, 'relative_horizon_success_mean': -0.5942572103490844, 'relative_horizon_non_success_mean': 1.6342073284599818, 'relative_horizon_auc': 0.0}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 4, 'non_successful': 26, 'relative_horizon_success_mean': -2.3943550731568277, 'relative_horizon_non_success_mean': 0.3683623189472049, 'relative_horizon_auc': 0.0}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'molmoact2', 'n': 60, 'successful': 10, 'non_successful': 50, 'relative_horizon_success_mean': -1.9313375390812122, 'relative_horizon_non_success_mean': 0.38626750781624225, 'relative_horizon_auc': 0.012}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'pi0', 'n': 30, 'successful': 2, 'non_successful': 28, 'relative_horizon_success_mean': -3.1356444334479603, 'relative_horizon_non_success_mean': 0.22397460238914, 'relative_horizon_auc': 0.0}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'pi0.5', 'n': 30, 'successful': 7, 'non_successful': 23, 'relative_horizon_success_mean': -1.702265807683178, 'relative_horizon_non_success_mean': 0.5180808979905323, 'relative_horizon_auc': 0.0}, {'task': 'Hold the pink lamp still with your left arm and open the door with your right gripper', 'policy_type': 'smolvla', 'n': 30, 'successful': 9, 'non_successful': 21, 'relative_horizon_success_mean': -1.480306944569098, 'relative_horizon_non_success_mean': 0.6344172619581849, 'relative_horizon_auc': 0.0}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'diffusion', 'n': 30, 'successful': 2, 'non_successful': 28, 'relative_horizon_success_mean': -0.3664127592595837, 'relative_horizon_non_success_mean': 0.026172339947113068, 'relative_horizon_auc': 0.32142857142857145}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 1, 'non_successful': 29, 'relative_horizon_success_mean': -0.4246111830044103, 'relative_horizon_non_success_mean': 0.014641764931186388, 'relative_horizon_auc': 0.3793103448275862}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'molmoact2', 'n': 60, 'successful': 1, 'non_successful': 59, 'relative_horizon_success_mean': -0.8417373136041832, 'relative_horizon_non_success_mean': 0.01426673412888451, 'relative_horizon_auc': 0.1016949152542373}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'pi0', 'n': 30, 'successful': 8, 'non_successful': 22, 'relative_horizon_success_mean': -0.725924914091003, 'relative_horizon_non_success_mean': 0.2639726960330922, 'relative_horizon_auc': 0.29261363636363635}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'pi0.5', 'n': 30, 'successful': 9, 'non_successful': 21, 'relative_horizon_success_mean': -0.8780964601001737, 'relative_horizon_non_success_mean': 0.3763270543286456, 'relative_horizon_auc': 0.16666666666666666}, {'task': 'Insert the candle inside the lantern and close the door', 'policy_type': 'smolvla', 'n': 30, 'successful': 2, 'non_successful': 28, 'relative_horizon_success_mean': -0.8595793127155462, 'relative_horizon_non_success_mean': 0.061398522336824635, 'relative_horizon_auc': 0.23214285714285715}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'diffusion', 'n': 30, 'successful': 4, 'non_successful': 26, 'relative_horizon_success_mean': -1.8739773572091494, 'relative_horizon_non_success_mean': 0.28830420880140795, 'relative_horizon_auc': 0.04326923076923077}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'grootn1.7', 'n': 30, 'successful': 14, 'non_successful': 16, 'relative_horizon_success_mean': -0.5618274466774928, 'relative_horizon_non_success_mean': 0.4915990158428062, 'relative_horizon_auc': 0.18973214285714285}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'molmoact2', 'n': 60, 'successful': 4, 'non_successful': 56, 'relative_horizon_success_mean': -1.0397241020241845, 'relative_horizon_non_success_mean': 0.07426600728744173, 'relative_horizon_auc': 0.20089285714285715}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'pi0', 'n': 30, 'successful': 14, 'non_successful': 16, 'relative_horizon_success_mean': -1.0091864640888477, 'relative_horizon_non_success_mean': 0.8830381560777418, 'relative_horizon_auc': 0.0}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'pi0.5', 'n': 29, 'successful': 25, 'non_successful': 4, 'relative_horizon_success_mean': -0.299203524329764, 'relative_horizon_non_success_mean': 1.8700220270610237, 'relative_horizon_auc': 0.06}, {'task': 'Transfer the cube between your arms and drop it into the white basket', 'policy_type': 'smolvla', 'n': 30, 'successful': 2, 'non_successful': 28, 'relative_horizon_success_mean': -2.3275855751548664, 'relative_horizon_non_success_mean': 0.16625611251106154, 'relative_horizon_auc': 0.017857142857142856}], 'pooled_relative_horizon_auc': 0.14225478468899522, 'within_stratum_permuted_length_auc': 0.4722753854332802, 'all_strata_have_shorter_success': True}

## Ranking consequence

{
  "policy_scores": [
    {
      "policy_type": "act",
      "n": 330,
      "human_strict_success_rate": 0.20303030303030303,
      "content_only": 0.1766792302500105,
      "content_plus_length": 0.18098482827338386
    },
    {
      "policy_type": "diffusion",
      "n": 240,
      "human_strict_success_rate": 0.22083333333333333,
      "content_only": 0.23299971982177006,
      "content_plus_length": 0.22336904542453218
    },
    {
      "policy_type": "grootn1.7",
      "n": 240,
      "human_strict_success_rate": 0.3458333333333333,
      "content_only": 0.31221391276948474,
      "content_plus_length": 0.3191291754120103
    },
    {
      "policy_type": "molmoact2",
      "n": 480,
      "human_strict_success_rate": 0.14791666666666667,
      "content_only": 0.1674979679896425,
      "content_plus_length": 0.16863753906983472
    },
    {
      "policy_type": "pi0",
      "n": 239,
      "human_strict_success_rate": 0.36401673640167365,
      "content_only": 0.3155114960436389,
      "content_plus_length": 0.3186363183709567
    },
    {
      "policy_type": "pi0.5",
      "n": 240,
      "human_strict_success_rate": 0.45416666666666666,
      "content_only": 0.3555801847297913,
      "content_plus_length": 0.36428703625295833
    },
    {
      "policy_type": "smolvla",
      "n": 330,
      "human_strict_success_rate": 0.13636363636363635,
      "content_only": 0.13649171996216006,
      "content_plus_length": 0.13847592164566552
    }
  ],
  "metrics_vs_human": {
    "content_only": {
      "spearman": 1.0,
      "kendall_tau_a": 1.0,
      "pairwise_disagreement_vs_human": 0,
      "order_high_to_low": [
        "pi0.5",
        "pi0",
        "grootn1.7",
        "diffusion",
        "act",
        "molmoact2",
        "smolvla"
      ]
    },
    "content_plus_length": {
      "spearman": 0.9642857142857145,
      "kendall_tau_a": 0.9047619047619048,
      "pairwise_disagreement_vs_human": 1,
      "order_high_to_low": [
        "pi0.5",
        "grootn1.7",
        "pi0",
        "diffusion",
        "act",
        "molmoact2",
        "smolvla"
      ]
    }
  },
  "task_cluster_bootstrap_95ci": {
    "content_only": {
      "spearman": [
        0.6785714285714287,
        1.0
      ],
      "kendall_tau_a": [
        0.5238095238095238,
        1.0
      ],
      "pairwise_disagreement_vs_human": [
        0.0,
        5.0
      ]
    },
    "content_plus_length": {
      "spearman": [
        0.7500000000000002,
        1.0
      ],
      "kendall_tau_a": [
        0.6190476190476191,
        1.0
      ],
      "pairwise_disagreement_vs_human": [
        0.0,
        4.0
      ]
    }
  }
}
