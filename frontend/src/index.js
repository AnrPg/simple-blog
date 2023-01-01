import React from "react";
import { render } from 'react-dom';
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
render(<App />, rootElement)