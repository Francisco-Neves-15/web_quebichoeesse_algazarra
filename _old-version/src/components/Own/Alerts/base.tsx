"use client";

import { AlertsBaseType } from "@/types";

import styles from "./style.module.scss";

const AlertBase = ({ visible, title, message, html }: AlertsBaseType) => {
	if (!visible) return null;

	return (
		<div className={`${styles.alertsContainer}`}>
			<div className={`overlay ${visible ? "show" : ""}`}></div>
			<div style={{ zIndex: 1000 }} className={`${styles.alertsPopover}`}>
				{title && <h3 className={`${styles.alertsTitle}`}>{title}</h3>}
				{message && <p className={`${styles.alertsMessage}`}>{message}</p>}
				{html}
			</div>
		</div>
	);
};

export default AlertBase;
