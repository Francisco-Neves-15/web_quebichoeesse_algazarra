import type { Metadata } from "next";

import "./globals.css";
import "@/styles/themes/classic.css";
import "@/styles/utils-colors.scss";
import "@/styles/miscellaneous.scss";

import { yatraOne, poppins, irishGrover, alfaSlab } from "@/styles/fonts";

import { Providers } from "@/providers/";

export const metadata: Metadata = {
	title: "Início | Que Bicho é Esse?",
	description: "",
	keywords: "",
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en" data-theme="light" data-device="large" data-layout="regular">
			<body
				className={`
        ${poppins.variable}
        ${yatraOne.variable}
        ${irishGrover.variable}
        ${alfaSlab.variable}
        antialiased
      `}
			>
				<Providers>
					<main>{children}</main>
				</Providers>
			</body>
		</html>
	);
}
