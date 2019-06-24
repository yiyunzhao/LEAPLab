### LEAPLab
1. backstage <br />
This repository contains the python codes that could generate corresponding FindingFive inputs (stimuli.csv, response.csv, trial_templates.txt, procedure.txt) as well as some helper files souch as praat (the audio stimuli required). This is specially designed for minature artificial language experiments. The researchers need to provide study_design.csv file where researchers specify their experimental designs and input_language.csv file where researchers specify their designed minature artificial language with a specialized format. 
2. motherboard.py is the main script:
	to execute: 
			python3 motherboard.py study_design_cbtest.csv input_language_test.csv -din 'exp1' -dout 'exp1/cbtest_FF'
			python3 motherboard.py study_design_fulltest.csv input_language_test.csv -din 'exp1' -dout 'exp1/fulltest_FF'
