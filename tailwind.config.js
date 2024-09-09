/** @type {import('tailwindcss').Config} */

const colors = require("tailwindcss/colors");

module.exports = {
  content: [
    "./TextRanker/templates/**/*.html",
    "./node_modules/flowbite/**/*.js",
  ],
  plugins: [require("flowbite/plugin")({ datatables: true })],
};
