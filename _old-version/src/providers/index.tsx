"use client";

import { ReactNode } from "react";
import { AlertProvider } from "./AlertProvider";
// import { ToastProvider } from "./ToastProvider";
// import { ModalProvider } from "./ModalProvider";
// import { ThemeProvider } from "./ThemeProvider";
// import { I18nProvider } from "./I18nProvider";

export function Providers({ children }: { children: ReactNode }) {
	return (
		<>
			<AlertProvider>{children}</AlertProvider>
		</>
	);
}
