import { ReactNode } from "react";

export function ModalHeader({ children }: { children: ReactNode }) {
	return <header className="modal-header">{children}</header>;
}

export function ModalBody({ children }: { children: ReactNode }) {
	return <section className="modal-body">{children}</section>;
}

export function ModalFooter({ children }: { children: ReactNode }) {
	return <footer className="modal-footer">{children}</footer>;
}
