import React from "react";
import { createRoot } from 'react-dom/client';
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import Users from "./components/Users"

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Users />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
const root = createRoot(rootElement);
root.render(<App />);