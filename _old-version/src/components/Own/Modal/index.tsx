"use client";

import { ReactNode } from "react";

type ModalProps = {
	children: ReactNode;
	state: boolean;
	closeBtnPosition: "top-left" | "center" | "top-right";
};

export function Modal({ children, state, closeBtnPosition }: ModalProps) {
	return (
		<div inert={state} className="modal">
			<div className="modal-backdrop"></div>
			<div className="modal-shell">
				<button className={`${closeBtnPosition}`}> Fechar</button>
				{children}
			</div>
		</div>
	);
}
