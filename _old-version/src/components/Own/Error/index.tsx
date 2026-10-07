"use client";

import { FaCircleExclamation } from "react-icons/fa6";

import styles from "./style.module.scss";

type ErrorVariants = "default";

interface ErrorProps {
	variant?: ErrorVariants;
	message: string;
	hideIcon?: boolean;
}

export const Error = ({ variant = "default", message, hideIcon = false }: ErrorProps) => {
	const variantStyle = {
		default: styles.errorDefault,
	}[variant];

	return (
		<span
			className={`
        ${variantStyle} 
        ${!hideIcon ? styles.hasErrorIcon : ""}
      `}
		>
			{!hideIcon && <FaCircleExclamation size={20} style={{ color: "var(--danger)" }} />}
			{message}
		</span>
	);
};
