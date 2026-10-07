"use client";

import { AlertsConfirmType } from "@/types";
import AlertBase from "../base";
import { Button } from "@/components/Own";

import styles from "../style.module.scss";

export const AlertsConfirm = ({
	visible,
	title,
	message,
	html,
	btnCancelText = "Cancelar",
	btnConfirmText = "Confirmar",
	resolver,
}: AlertsConfirmType) => {
	if (!visible) return null;

	function resolve(value: boolean) {
		resolver?.(value);
	}

	return (
		<AlertBase
			type="confirm"
			visible={visible}
			title={title}
			message={message}
			html={
				<>
					{html}
					<div className={styles.confirmActions}>
						<Button variant="neutral" onClick={() => resolve(false)}>
							{btnCancelText}
						</Button>
						<Button variant="primary" onClick={() => resolve(true)}>
							{btnConfirmText}
						</Button>
					</div>
				</>
			}
		/>
	);
};
