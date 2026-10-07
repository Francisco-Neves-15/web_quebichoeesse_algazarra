"use client";

import { useState } from "react";
import { AlertsInputType, TypeErrorCommom } from "@/types";
import AlertBase from "../base";

import { Button, Error, Input } from "@/components/Own";

import styles from "../style.module.scss";

export const AlertsInput = ({
	visible,
	title,
	message,
	html,
	resolver,
	required = true,
	placeholder,
	inputType = "string",
	btnCancelText = "Cancelar",
	btnSendText = "Enviar",
}: AlertsInputType) => {
	const [value, setValue] = useState("");
	const [valid, setValid] = useState(false);
	const [error, setError] = useState<TypeErrorCommom>({ is: false, message: "" });

	function clean() {
		setValue("");
		setValid(false);
		setError({ is: false, message: "" });
	}

	function verify(value: string) {
		if (value.length !== 0 || value || value === null) {
			setValid(true);
		} else {
			setValid(false);
		}
	}

	function cancel() {
		resolver?.({
			confirmed: false,
			value: "",
		});
		clean();
	}

	function confirm() {
		if (required && !value) {
			setError({ is: true, message: "Digite algo na areá disponível!" });
			return;
		}

		resolver?.({
			confirmed: true,
			value,
		});
		clean();
	}

	if (!visible) return null;

	return (
		<AlertBase
			type="input"
			visible={visible}
			title={title}
			message={message}
			html={
				<>
					{html}

					<div className={styles.inputArea}>
						<Input
							type={inputType}
							placeholder={placeholder}
							value={value}
							style={{ width: "100%" }}
							onChange={(e) => {
								setValue(e.target.value);
								verify(e.target.value);
							}}
						/>
						{error.is && <Error message={error.message} />}
					</div>

					<div className={styles.inputActions}>
						<Button variant="neutral" onClick={cancel}>
							{btnCancelText}
						</Button>
						{/* <Button variant="primary" onClick={confirm}> */}
						<Button variant="primary" onClick={valid ? () => confirm() : () => {}} disable={!valid}>
							{btnSendText}
						</Button>
					</div>
				</>
			}
		/>
	);
};
