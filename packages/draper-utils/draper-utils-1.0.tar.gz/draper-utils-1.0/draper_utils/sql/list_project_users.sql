SELECT DISTINCT
	ss_users.id AS user_id,
	ss_users.email,
	ss_users.company_name,
	ss_users.first_name,
	ss_users.last_name,
	ss_users.login,
	ss_users.password,
	ss_users.enabled,
		ss_users.email_notify,
		ss_users.field1 AS title,
		ss_users.field4 AS address_1

FROM
	`ss_users`,
	ssm_commdep_projects_activities

WHERE
	ss_users.id = ssm_commdep_projects_activities.creator_id

	GROUP BY
	ss_users.id,
	ss_users.email,
	ss_users.company_name,
	ss_users.first_name,
	ss_users.last_name,
	ss_users.login,
	ss_users.password,
	ss_users.enabled,
		ss_users.email_notify,
		ss_users.field1,
		ss_users.field4
