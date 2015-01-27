-- Login SQL server and run commands with root privileges.
USE omnilab_bd;

SELECT * FROM t_lable_group_comp INTO OUTFILE "t_lable_group_comp.csv"
	FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\r\n';