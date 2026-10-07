// Types
import { RoomCodeType } from "@/types";

export const ROUTES = {
	home: "/",
	login: "/login",
	register: "/register",
	about: "/about",
	room: (code: RoomCodeType) => `/room/${code}`,
	roomLobby: (code: RoomCodeType) => `/room/${code}/lobby`,
	roomGame: (code: RoomCodeType) => `/room/${code}/game`,
};
