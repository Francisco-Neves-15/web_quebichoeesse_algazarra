"use client";

import { ReactNode, useEffect, useState } from "react";
import { AlertsAlert, AlertsConfirm, AlertsInput } from "@/components/Own";
import { AlertsAlertType, AlertsConfirmType, AlertsInputType, AlertsInputResult } from "@/types";

const defaultAlert: AlertsAlertType = {
	type: "alert",
	visible: false,
};

const defaultConfirm: AlertsConfirmType = {
	type: "confirm",
	visible: false,
};

const defaultInput: AlertsInputType = {
	type: "input",
	visible: false,
};

export function AlertProvider({ children }: { children: ReactNode }) {
	const [alert, setAlert] = useState<AlertsAlertType>(defaultAlert);

	const [confirm, setConfirm] = useState<AlertsConfirmType>(defaultConfirm);

	const [input, setInput] = useState<AlertsInputType>(defaultInput);

	useEffect(() => {
		global.alerts = {
			alert: (config) => {
				setAlert({
					type: "alert",
					visible: true,
					...config,
					onClose: () => {
						config.onClose?.();
						setAlert(defaultAlert);
					},
				});
			},

			confirm: (config) => {
				return new Promise<boolean>((resolve) => {
					setConfirm({
						type: "confirm",
						visible: true,
						...config,
						resolver: (value) => {
							resolve(value);
							setConfirm(defaultConfirm);
						},
					});
				});
			},

			input: (config) => {
				return new Promise<AlertsInputResult>((resolve) => {
					setInput({
						type: "input",
						visible: true,
						...config,
						resolver: (result) => {
							resolve(result);
							setInput(defaultInput);
						},
					});
				});
			},
		};

		return () => {
			global.alerts = undefined as unknown as typeof global.alerts;
		};
	}, []);

	return (
		<>
			{children}
			<AlertsAlert {...alert} />
			<AlertsConfirm {...confirm} />
			<AlertsInput {...input} />
		</>
	);
}
