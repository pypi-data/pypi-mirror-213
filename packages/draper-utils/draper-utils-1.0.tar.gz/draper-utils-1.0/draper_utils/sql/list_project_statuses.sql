SELECT
	ssm_commdep_projects_status.status_id,
	ssm_commdep_projects_status.status_name,
	IF
	( enabled = 0, "False", "True" ) AS status_enabled
FROM
	ssm_commdep_projects_status