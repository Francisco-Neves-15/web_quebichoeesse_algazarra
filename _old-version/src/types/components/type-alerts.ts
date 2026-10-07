import { ReactNode } from "react";

export type AlertsTypes = "alert" | "confirm" | "input";

export interface AlertsBaseType {
	type: AlertsTypes;
	visible?: boolean;
	title?: string;
	message?: string;
	html?: ReactNode;
}

export interface AlertsAlertType extends AlertsBaseType {
	btnText?: string;
	onClose?: () => void;
	duration?: number;
	showDuration?: boolean;
}

export interface AlertsConfirmType extends AlertsBaseType {
	resolver?: (value: boolean) => void;
	btnCancelText?: string;
	btnConfirmText?: string;
}

export interface AlertsInputResult {
	confirmed: boolean;
	value: string;
}

export interface AlertsInputType extends AlertsBaseType {
	resolver?: (result: AlertsInputResult) => void;
	required?: boolean;
	placeholder?: string;
	inputType?: string;
	btnCancelText?: string;
	btnSendText?: string;
}
