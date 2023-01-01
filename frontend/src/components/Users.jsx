import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/react";

const UsersContext = React.createContext({
    users: [], fetchUsers: () => {}
    })

export default function Users() {

    const [users, setUsers] = useState([])

    const fetchUsers = async () => {
        fetch("http://127.0.0.1:8000/api/user/all", {
            crossDomain:true,
            method: 'GET',
            headers: {'Content-Type':'application/json'}
            })
            .then(response => response.json())
            .then(responseJson => {
                console.log(responseJson);
                setUsers(users.data)
            })
    }
    useEffect(() => {
        fetchUsers()
    }, [])
    return (
        <UsersContext.Provider value={{users, fetchUsers}}>
        <Stack spacing={5}>
            {users.map((user) => (
                <div>
                    <p>{user.firstName}</p>
                    <p>{user.lastName}</p>
                    <p>{user.email}</p>
                    <p>{user.tel}</p>
                    <p>{user.userId}</p>
                </div>
            ))}
        </Stack>
        </UsersContext.Provider>
    )
}