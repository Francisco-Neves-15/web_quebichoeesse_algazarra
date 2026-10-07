// Next
import { useRouter } from "next/router";

// Routes
// import { ROUTES } from "@/app/routes"

// Types
// import { GameCodeType } from "@/types"

export default function useAppNavigation() {
	const router = useRouter();
	return {
		goHome: () => router.push("/"),
		goBack: () => router.back(),
		// enterLobby: (code: GameCodeType) => router.push(ROUTES.game(code)),
	};
}
