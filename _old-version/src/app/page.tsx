"use client";
// import { useEffect, useState } from "react";

import { Button, Input } from "@/components/Own";
import { FaTrash, FaXmark } from "react-icons/fa6";

// import { Modal, ModalHeader, ModalBody, ModalFooter } from "@/components/Own"

export default function Home() {
	async function userConfirmation() {
		const confirmed = await global.alerts.confirm({
			title: "Tem certeza?",
			btnConfirmText: "Sim",
			btnCancelText: "Não",
		});
		console.log(`${confirmed}`);
	}

	async function userInsert() {
		const result = await global.alerts.input({
			title: "Digite seu nome",
			placeholder: "Nome",
		});
		if (result.confirmed) {
			console.log("Valor:", result.value);
		} else {
			console.log("Usuário cancelou");
		}
	}

	return (
		<div className="">
			<h1 className="text-primary-200">Lorem ipsum dolor sit 4444.</h1>

			<p className="font-body">
				Lorem ipsum dolor sit amet consectetur adipisicing elit. Magnam, in. Eum, nam non.
				Doloremque dolore optio vitae dolorum, quas autem, labore quibusdam natus beatae corporis,
				tempore quod!
			</p>

			<Button disable variant="danger" onClick={() => alert("AAAAA")}>
				<FaTrash size={32} />
				<p>Nome</p>
			</Button>

			<Button icon={<FaXmark size={32} />} />
			<Button variant="ghost" icon={<FaXmark size={32} />} />

			<Button variant="primary" text={`Algum texto: ${4 * 2}`} />
			<Button variant="secondary" text={`Algum texto: ${4 * 2}`} />
			<Button variant="danger" text={`Algum texto: ${4 * 2}`} />
			<Button disable text={`Desabilitado: ${4 * 4}`} />

			<Button
				onClick={() =>
					global.alerts.alert({
						title: "Alerta",
						message: "Você não pode realizar essa ação sem estar em uma conta",
						duration: 3000,
						showDuration: false,
					})
				}
				text="Alerta"
			/>

			<Button onClick={() => userConfirmation()} text="Confirmar" />
			<Button onClick={() => userInsert()} text="Inserir" />

      {/* <Button variant="primary" onClick={() => 
        global.toast.success({
          type: "",
          title: "", 
          desc: "", 
          duration: "",
          showDuration: false,
          origin: "",
          slide: false,
          id: "",
        })
      } />   */}

			<Input />
		</div>
	);
}
