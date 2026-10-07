// React
import { ReactNode } from "react";

// Next
import type { Metadata } from "next";

interface RoomLayoutProps {
	children: ReactNode;
}

export const metadata: Metadata = {
	title: "Room | Que Bicho é Esse?",
};

export default function RoomLayout({ children }: RoomLayoutProps) {
	return (
		<div>
			<main>{children}</main>
		</div>
	);
}
