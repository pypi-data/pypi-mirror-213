SELECT
	ssm_commdep_projects.id,
	ssm_commdep_projects.project_title,
	ssm_commdep_projects_users.user_id,
	ssm_commdep_projects_users.is_owner
FROM
	ssm_commdep_projects_users,
	ssm_commdep_projects
WHERE
	ssm_commdep_projects_users.project_id = ssm_commdep_projects.id