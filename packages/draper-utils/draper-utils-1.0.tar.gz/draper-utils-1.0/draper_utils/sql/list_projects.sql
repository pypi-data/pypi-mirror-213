SELECT
	ssm_commdep_projects.id AS project_id,
	ssm_commdep_projects.project_title,
	ssm_commdep_projects.project_code,
	ssm_commdep_projects.draper_number,
	ssm_commdep_projects.category_id,
	ssm_commdep_projects.status_id,
	ssm_commdep_projects.stage_id,
	ssm_commdep_projects.job_date,
	ssm_commdep_projects.user_id,
IF
	( internal = 0, "False", "True" ) AS is_internal
FROM
	ssm_commdep_projects