import localFont from "next/font/local";

export const poppins = localFont({
	src: [
		{
			path: "./fonts/Poppins/Poppins-Regular.woff",
			weight: "400",
			style: "normal",
		},
		{
			path: "./fonts/Poppins/Poppins-Regular.ttf",
			weight: "400",
			style: "normal",
		},
	],
	variable: "--font-poppins",
	display: "swap",
});

export const yatraOne = localFont({
	src: [
		{
			path: "./fonts/Yatra_One/YatraOne-Regular.woff",
			weight: "bold",
			style: "normal",
		},
		{
			path: "./fonts/Yatra_One/YatraOne-Regular.ttf",
			weight: "bold",
			style: "normal",
		},
	],
	variable: "--font-yatra",
	display: "swap",
});

export const irishGrover = localFont({
	src: [
		{
			path: "./fonts/Irish_Grover/IrishGrover-Regular.woff",
			weight: "bold",
			style: "normal",
		},
		{
			path: "./fonts/Irish_Grover/IrishGrover-Regular.ttf",
			weight: "bold",
			style: "normal",
		},
	],
	variable: "--font-irishGrover",
	display: "swap",
});

export const alfaSlab = localFont({
	src: [
		{
			path: "./fonts/Alfa_Slab_One/AlfaSlabOne-Regular.woff",
			weight: "bold",
			style: "normal",
		},
		{
			path: "./fonts/Alfa_Slab_One/AlfaSlabOne-Regular.ttf",
			weight: "bold",
			style: "normal",
		},
	],
	variable: "--font-alfaSlab",
	display: "swap",
});
