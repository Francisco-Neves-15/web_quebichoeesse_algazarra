"use client";

import { useEffect, useRef } from "react";
import { AlertsAlertType } from "@/types";
import { Button } from "@/components/Own";
import AlertBase from "../base";

import styles from "../style.module.scss";

export const AlertsAlert = ({
	visible,
	title,
	message,
	html,
	btnText = "OK",
	duration,
	showDuration = false,
	onClose,
}: AlertsAlertType) => {
	const barRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		if (!visible || !duration) return;

		const timer = setTimeout(() => {
			onClose?.();
		}, duration);

		if (showDuration && barRef.current) {
			const startTime = performance.now();

			const animate = (currentTime: number) => {
				const elapsed = currentTime - startTime;
				const remaining = Math.max(duration - elapsed, 0);
				const percentage = (remaining / duration) * 100;

				if (barRef.current) {
					barRef.current.style.width = `${percentage}%`;
				}

				if (remaining > 0) {
					requestAnimationFrame(animate);
				}
			};

			barRef.current.style.width = "100%";
			requestAnimationFrame(animate);
		}

		return () => clearTimeout(timer);
	}, [visible, duration, showDuration, onClose]);

	if (!visible) return null;

	return (
		<AlertBase
			type="alert"
			visible={visible}
			title={title}
			message={message}
			html={
				<>
					{html}
					<Button onClick={onClose}>{btnText}</Button>

					{duration && showDuration && (
						<>
							<div></div>
							<div className={styles.wrapperTimeBar}>
								<div ref={barRef} className={styles.fillTimeBar} style={{ width: "100%" }} />
							</div>
						</>
					)}
				</>
			}
		/>
	);
};
