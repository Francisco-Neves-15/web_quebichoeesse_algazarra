// Next
import type { Metadata } from "next";
import Link from "next/link";

// Routes
import { ROUTES } from "@/app/routes";

export const metadata: Metadata = {
	title: "404 | Que Bicho é Esse?",
};

export default function NotFound() {
	return (
		<div className="w-full h-full">
			<div className="w-full h-full flex-center flex-col">
				<h1>Erro: 404</h1>
				<p>Página não encontrada</p>
				<Link className="hvAnim bottom mid" href={ROUTES.home}>
					→ Voltar para o Início ←
				</Link>
			</div>
		</div>
	);
}
