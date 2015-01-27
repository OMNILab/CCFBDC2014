USE omnilab_bd;

-- Remove newlines in some fields
UPDATE t_lable_group_comp SET
	title = REPLACE(REPLACE(title, '\r', ''), '\n', ' '),
	format_content = REPLACE(REPLACE(format_content, '\r', ''), '\n', ' '),
	abs = REPLACE(REPLACE(abs, '\r', ''), '\n', ' '),
	segresult = REPLACE(REPLACE(segresult, '\r', ''), '\n', ' ');