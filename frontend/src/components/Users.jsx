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

    // // Alternative code for the same thing as below
    // const fetchUsers = async () => {
    //     fetch("http://127.0.0.1:8000/api/user/all", {
    //         crossDomain:true,
    //         method: 'GET',
    //         headers: {'Content-Type':'application/json'}
    //         })
    //         .then(response => response.json())
    //         .then(responseJson => {
    //             console.log(responseJson);
    //             setUsers(responseJson)
    //         })
    // }

    const fetchUsers = async () => {
        const response = await fetch("http://127.0.0.1:8000/api/user/all")
        const users = await response.json()
        setUsers(users)
    }
    
    useEffect(() => {
        fetchUsers()
    }, [])
    
    return (
        <UsersContext.Provider value={{users, fetchUsers}}>
        <Stack spacing={5}>
            {users?.map((user) => (
                <div key={user.userId}>
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