"use client";

import styles from "./style.module.scss";

type InputVariants = "default";

interface InputProps {
	variant?: InputVariants;
	id?: string;
	className?: string;
	style?: React.CSSProperties;
	type?: React.HTMLInputTypeAttribute;
	placeholder?: string;
	value?: string;
	onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
	onFocus?: (event: React.ChangeEvent<HTMLInputElement>) => void;
	onBlur?: (event: React.ChangeEvent<HTMLInputElement>) => void;
	title?: string;
	name?: string;
	inert?: boolean;
}

export const Input = ({
	variant = "default",
	id,
	className,
	style,
	type,
	placeholder,
	value,
	onChange,
	onFocus,
	onBlur,
	title,
	name,
	inert,
}: InputProps) => {
	const variantStyle = {
		default: styles.inputDefault,
	}[variant];

	return (
		<input
			id={id}
			className={`
        ${styles.inputBase}
        ${variantStyle}
        ${className || ""}
      `}
			type={type}
			placeholder={placeholder}
			value={value}
			onBlur={onBlur}
			onFocus={onFocus}
			onChange={onChange}
			style={style}
			title={title}
			name={name}
			inert={inert}
		/>
	);
};
