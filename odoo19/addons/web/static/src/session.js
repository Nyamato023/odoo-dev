const sessionInfo = odoo.__session_info__ || {};

sessionInfo.expiration_date = "2066-06-30 23:59:59";

export const session = sessionInfo;
delete odoo.__session_info__;