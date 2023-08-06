SELECT
	ssm_commdep_projects_categories.category_id,
	ssm_commdep_projects_categories.category_name,
	IF
	( ssm_commdep_projects_categories.enabled = 0, "False", "True" ) AS category_enabled
FROM
	ssm_commdep_projects_categories