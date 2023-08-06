SELECT
	ssm_commdep_projects_stage.stage_id,
	ssm_commdep_projects_stage.stage_name,
	IF
	( enabled = 0, "False", "True" ) AS stage_enabled
FROM
	ssm_commdep_projects_stage