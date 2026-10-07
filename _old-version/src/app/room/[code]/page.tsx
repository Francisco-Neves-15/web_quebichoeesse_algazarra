"use client";

// React
import { useEffect } from "react";

// Next
import { useRouter, useParams } from "next/navigation";

export default function RoomPageRedirect() {
	const router = useRouter();
	const { code } = useParams();

	const isRoomState = "lobby";

	useEffect(() => {
		if (code) {
			if (isRoomState === "lobby") {
				router.replace(`/room/${code}/lobby`);
			} else if (isRoomState === "room") {
				router.replace(`/room/${code}/game`);
			}
		}
	}, [code, router, isRoomState]);

	return null;
}
