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
            <AddUser />
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

function AddUser() {
    const [firstName, setFirstName] = React.useState("")
    const [lastName, setLastName] = React.useState("")
    const [nickname, setNickname] = React.useState("")
    const [email, setEmail] = React.useState("")
    const [tel, setTel] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [birthdate, setBirthdate] = React.useState("")
    const [nationality, setNationality] = React.useState("")
    const [gender, setGender] = React.useState("")

    const {users, fetchUsers} = React.useContext(UsersContext)

    const handleFirstNameInput = event  => {
        setFirstName(event.target.value)
    }
    const handleLastNameInput = event  => {
        setLastName(event.target.value)
    }
    const handleNicknameInput = event  => {
        setNickname(event.target.value)
    }
    const handleEmailInput = event  => {
        setEmail(event.target.value)
    }
    const handleTelInput = event  => {
        setTel(event.target.value)
    }
    const handlePasswordInput = event  => {
        setPassword(event.target.value)
    }
    const handleBirthdateInput = event  => {
        setBirthdate(event.target.value)
    }
    const handletNationalityInput = event  => {
        setNationality(event.target.value)
    }
    const handleGenderInput = event  => {
        setGender(event.target.value)
    }

    const handleSubmit = (event) => {
        const newUser = {
            "firstName": firstName,
            "lastName": lastName,
            "nickname": nickname,
            "email": email,
            "tel": tel,
            "password": password,
            "birthdate": birthdate,
            "nationality": [
                nationality
            ],
            "gender": gender
        }

        fetch("http://127.0.0.1:8000/api/user/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newUser)
        }).then(fetchUsers)
    }

    return (
        <form onSubmit={handleSubmit}>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add First Name" aria-label="Add First Name" onChange={handleFirstNameInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Last Name" aria-label="Add Last Name" onChange={handleLastNameInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Nickname" aria-label="Add Nickname" onChange={handleNicknameInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Email" aria-label="Add Email" onChange={handleEmailInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Tel" aria-label="Add Tel" onChange={handleTelInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Password" aria-label="Add Password" onChange={handlePasswordInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Birthdate" aria-label="Add Birthdate" onChange={handleBirthdateInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Nationality" aria-label="Add Nationality" onChange={handletNationalityInput} />
            </InputGroup>
            <InputGroup size="md">
                <Input pr="4.5rem" type="text" placeholder="Add Gender" aria-label="Add Gender" onChange={handleGenderInput} />
            </InputGroup>
            <InputGroup>
                <input type="submit" value="Submit"></input>
            </InputGroup>
        </form>
    )
}