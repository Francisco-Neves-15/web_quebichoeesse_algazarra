import { AlertType, ConfirmType, InputType, InputResult } from "@/types";

declare global {
	var alerts: {
		alert: (config: Omit<AlertType, "visible" | "type">) => void;
		confirm: (config: Omit<ConfirmType, "visible" | "type" | "resolver">) => Promise<boolean>;
		input: (config: Omit<InputType, "visible" | "type" | "resolver">) => Promise<InputResult>;
	};
}

export {};
