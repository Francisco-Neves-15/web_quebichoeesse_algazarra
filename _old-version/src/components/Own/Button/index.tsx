"use client";

import { ReactNode, ReactElement } from "react";

import styles from "./style.module.scss";

type ButtonVariants = "primary" | "secondary" | "neutral" | "ghost" | "danger";

interface ButtonProps {
	children?: ReactNode;
	disable?: boolean;
	variant?: ButtonVariants;
	id?: string;
	className?: string;
	style?: React.CSSProperties;
	onClick?: () => void;
	title?: string;
	name?: string;
	inert?: boolean;
	text?: string;
	icon?: ReactElement;
}

export const Button = ({
	children,
	disable = false,
	variant = "primary",
	id,
	className,
	style,
	onClick,
	title,
	name,
	inert = false,
	text,
	icon,
}: ButtonProps) => {
	const variantStyle = {
		primary: styles.btnPrimary,
		secondary: styles.btnSecondary,
		neutral: styles.neutral,
		ghost: styles.btnGhost,
		danger: styles.btnDanger,
	}[variant];

	return (
		<button
			id={id}
			className={`
        ${styles.btnBase} 
        ${variantStyle} 
        ${icon && !text && !children ? styles.btnIcon : ""}
        ${disable ? styles.btnDisable : ""}
        ${className || ""}
      `}
			onClick={disable ? () => {} : onClick}
			disabled={disable}
			inert={disable || inert}
			style={style}
			title={title}
			name={name}
		>
			{icon && icon}
			{children && children}
			{text && <p className="btnText">{text}</p>}
		</button>
	);
};
